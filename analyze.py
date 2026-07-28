import os
import json
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def group_and_summarize(news_items):
    """뉴스 제목들을 LLM에 보내서 이슈별로 그룹핑 + 요약"""
    
    titles_text = "\n".join([f"- {item['title']} ({item['link']})" for item in news_items])
    
    prompt = f"""다음은 오늘 수집된 금융 뉴스 제목 목록이야.

{titles_text}

같은 사건/이슈를 다루는 제목끼리 그룹으로 묶어줘. 각 그룹마다:
- topic: 이슈를 대표하는 짧은 제목 (한글, 15자 이내)
- count: 몇 개 기사가 이 이슈를 다뤘는지
- summary: 이 이슈에 대한 2문장 요약
- link: 대표 기사 링크 하나

화제성이 높은(count가 큰) 순서로 정렬해서, 아래 JSON 형식으로만 답해줘. 다른 설명 붙이지 마.

[
  {{"topic": "...", "count": 2, "summary": "...", "link": "..."}}
]
"""

    message = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=4500,
        messages=[{"role": "user", "content": prompt}]
    )
    
    result_text = message.content[0].text.strip()
    result_text = result_text.replace("```json", "").replace("```", "").strip()
    
    try:
        return json.loads(result_text)
    except json.JSONDecodeError:
        print("JSON 파싱 실패:", result_text)
        return []


if __name__ == "__main__":
    from collect import get_multi_news
    
    keywords = ["기준금리", "주택담보대출", "부동산 규제", "코스피", "환율"]
    news = get_multi_news(keywords, display_per_keyword=10)
    
    print(f"총 {len(news)}건 수집")
    
    topics = group_and_summarize(news)
    
    for t in topics:
        print(f"[{t['count']}건] {t['topic']}")
        print(f"  {t['summary']}")
        print(f"  {t['link']}\n")