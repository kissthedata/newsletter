from collect import get_multi_news
from analyze import group_and_summarize
from save import init_db, save_news
from send_mail import send_email

KEYWORDS = ["기준금리", "주택담보대출", "부동산 규제", "코스피", "환율"]

SUBSCRIBERS = [
    "qorskawls12@naver.com",
    "kwoo1790@naver.com",
    "kimkim12322@naver.com",
    "changhyun_95@naver.com",
    "hongsu9978@naver.com",
    "rael517@naver.com",
    "fbdudtj1@naver.com",
    "ksj911@knu.ac.kr",
    "sds550808@gmail.com",
    "asktheme@naver.com",
    "esther7949@naver.com"
]

def format_email_body(topics):
    """그룹핑+요약된 이슈 리스트를 HTML로 변환"""
    
    news_html = ""
    for i, t in enumerate(topics, 1):
        news_html += f"""
        <tr>
          <td style="padding: 16px 0; border-bottom: 1px solid #eee;">
            <span style="color: #999; font-size: 13px;">{i:02d} · {t['count']}건 보도</span><br>
            <a href="{t['link']}" style="color: #222; font-size: 16px; font-weight: 600; text-decoration: none;">
              {t.get('emoji', '')} <span style="background: linear-gradient(transparent 55%, #fff59d 55%);">{t['topic']}</span>
            </a>
            <p style="color: #555; font-size: 14px; margin: 8px 0 0; line-height: 1.5;">
              {t['summary']}
            </p>
          </td>
        </tr>
        """
      
    html = f"""
    <html>
    <body style="font-family: 'Apple SD Gothic Neo', sans-serif; background-color: #f5f5f5; padding: 20px;">
      <table style="max-width: 600px; margin: 0 auto; background: white; border-radius: 8px; overflow: hidden;">
        <tr>
          <td style="background-color: #1a1a2e; padding: 24px; text-align: center;">
            <h1 style="color: white; margin: 0; font-size: 20px;">오늘의 금융 뉴스</h1>
            <p style="color: #aaa; margin: 8px 0 0; font-size: 13px;">화제성 순 요약 브리핑</p>
          </td>
        </tr>
        <tr>
          <td style="padding: 24px;">
            <table style="width: 100%; border-collapse: collapse;">
              {news_html}
            </table>
          </td>
        </tr>
        <tr>
          <td style="padding: 16px 24px; background: #fafafa; text-align: center;">
            <p style="color: #999; font-size: 12px; margin: 0;">매일 오전 8시 30분에 발송해드려요.</p>
            <a href="https://forms.gle/dTDGEgD1UgmV2BfA6"
               style="display: inline-block; padding: 8px 16px; background: #1a1a2e; color: white; font-size: 12px; text-decoration: none; border-radius: 20px;">
              💬 피드백 남기기
            </a>
          </td>
        </tr>
      </table>
    </body>
    </html>
    """
    return html

def run_pipeline():
    print("1. 뉴스 수집...")
    news = get_multi_news(KEYWORDS, display_per_keyword=10)

    print("2. DB 저장...")
    init_db()
    save_news("multi_keyword", news)

    print("3. 화제성 그룹핑 + 요약...")
    topics = group_and_summarize(news)

    print("4. 메일 본문 생성...")
    body = format_email_body(topics)

    print("5. 메일 발송...")
    send_email(
        subject="오늘의 금융 뉴스 요약",
        body=body,
        to_email=SUBSCRIBERS,
        is_html=True
    )

    print("파이프라인 완료!")

if __name__ == "__main__":
    run_pipeline()