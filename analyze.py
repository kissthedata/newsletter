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
- emoji: 이슈 내용과 가장 잘 어울리는 이모지 딱 1개 (예: 금리 관련이면 📈 또는 🏦, 부동산이면 🏠, 환율이면 💱 등 문맥에 맞게 자유롭게 선택)
- topic: 이슈를 대표하는 짧은 제목 (한글, 15자 이내)
- count: 몇 개 기사가 이 이슈를 다뤘는지
- summary: 이 이슈에 대한 2문장 요약. 반드시 부드러운 존댓말(해요체)로 작성해줘. 예: "~했어요", "~할 전망이에요", "~오르고 있어요" (X: "~했다", "~오를 전망이다", "~오르고 있다"), 어려운 단어(근원물가 등)는 각 summary 밑에 *근원물가란, ~~를 말해요. 매우 쉽게 각주 달아줄것.
- link: 대표 기사 링크 하나

화제성이 높은(count가 큰) 순서로 정렬해서, 아래 JSON 형식으로만 답해줘. 다른 설명 붙이지 마.
그리고, 어려운 단어는 예를 들어, 서킷브레이커 이런 것들은 해당 문장 아래에 쉽게 풀어써줘.
[
  {{"emoji": "📈", "topic": "...", "count": 2, "summary": "...", "link": "..."}}
]
"""

    message = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=8000,
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
