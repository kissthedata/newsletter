from save import init_db, save_news
import os
import requests
from dotenv import load_dotenv

# .env 파일에서 API 키 불러오기
load_dotenv()
CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")

def get_news(query, display=10):
    """네이버 뉴스 검색 API 호출"""
    url = "https://openapi.naver.com/v1/search/news.json"
    headers = {
        "X-Naver-Client-Id": CLIENT_ID,
        "X-Naver-Client-Secret": CLIENT_SECRET
    }
    params = {
        "query": query,
        "display": display,
        "sort": "date"  # 최신순
    }
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        print(f"에러 발생: {response.status_code}, {response.text}")
        return None
    
    return response.json()

def get_multi_news(keywords, display_per_keyword=10):
    """여러 키워드로 검색해서 하나로 합치기 (중복 제거)"""
    all_news = []
    seen_links = set()

    for keyword in keywords:
        result = get_news(keyword, display=display_per_keyword)
        if result:
            for item in result['items']:
                if item['link'] not in seen_links:
                    seen_links.add(item['link'])
                    all_news.append(item)

    return all_news

if __name__ == "__main__":
    init_db()

    result = get_news("저축은행", display=5)
    
    if result:
        save_news("저축은행", result['items']) #db저장 

        for item in result['items']:
            print(f"제목: {item['title']}")
            print(f"날짜: {item['pubDate']}")
            print(f"링크: {item['link']}")
            print("---")