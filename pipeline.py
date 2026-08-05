from collect import get_multi_news
from analyze import group_and_summarize
from save import init_db, save_news
from send_mail import send_email
from datetime import datetime

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
    "esther7949@naver.com",
    "bommolsun@naver.com",
    "030823ab@naver.com",
    "iss7574@naver.com",
    "jiseocean@gmail.com",
    "seomingi649@gmail.com",
    "ggeum2@kakao.com"
]

FEEDBACK_FORM_URL = "https://forms.gle/dTDGEgD1UgmV2BfA6"


def format_email_body(topics):
    """그룹핑+요약된 이슈 리스트를 CLI 스타일 HTML로 변환"""

    news_html = ""
    last_index = len(topics)
    for i, t in enumerate(topics, 1):
        emoji = t.get("emoji", "")
        # 마지막 아이템만 구분선 제거
        border_style = "border-bottom:1px dashed #e2e2e5;" if i != last_index else ""

        news_html += f"""
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="{border_style}">
                <tr>
                  <td style="padding: 16px 0;">
                    <div style="font-family:'SF Mono', Menlo, monospace; font-size:11px; color:#16a34a; margin-bottom:6px;">
                      [{i:02d}] <span style="color:#999;">{t['count']}건 보도</span>
                    </div>
                    <a href="{t['link']}" style="text-decoration:none;">
                      <div style="font-size:15.5px; color:#111; font-weight:700; margin-bottom:5px;">
                        {emoji} <span style="background: linear-gradient(transparent 60%, #d9f99d 60%);">{t['topic']}</span>
                      </div>
                    </a>
                    <p style="font-size:12.5px; color:#71717a; line-height:1.6; margin:0;">
                      {t['summary']}
                    </p>
                  </td>
                </tr>
              </table>
        """

    today_str = datetime.now().strftime("%Y.%m.%d")

    html = f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>머니픽 - 오늘의 금융 뉴스 요약</title>
    </head>
    <body style="margin:0; padding:0; background-color:#f4f4f5; font-family:-apple-system, 'Apple SD Gothic Neo', sans-serif;">
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color:#f4f4f5; padding: 20px 12px;">
        <tr>
          <td align="center">
            <table role="presentation" width="100%" style="max-width:600px; background-color:#ffffff; border-radius:16px; overflow:hidden; box-shadow:0 2px 16px rgba(0,0,0,0.06);" cellpadding="0" cellspacing="0">

              <!-- 터미널 헤더 -->
              <tr>
                <td style="padding: 20px 20px 16px;">
                  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color:#0e0e10; border-radius:12px;">
                    <tr>
                      <td style="padding: 14px 18px 6px;">
                        <span style="display:inline-block; width:8px; height:8px; border-radius:50%; background:#ff5f57; margin-right:6px;">&nbsp;</span>
                        <span style="display:inline-block; width:8px; height:8px; border-radius:50%; background:#febc2e; margin-right:6px;">&nbsp;</span>
                        <span style="display:inline-block; width:8px; height:8px; border-radius:50%; background:#28c840;">&nbsp;</span>
                      </td>
                    </tr>
                    <tr>
                      <td style="padding: 6px 18px 16px;">
                        <div style="font-family:'SF Mono', Menlo, monospace; font-size:14px; color:#3ee06a; font-weight:700;">
                          머니픽 오늘의 브리핑
                        </div>
                        <div style="font-family:'SF Mono', Menlo, monospace; font-size:11px; color:#888; margin-top:6px;">
                          {today_str} · 이슈 {len(topics)}건 · 화제성 순 정렬<span style="color:#3ee06a;">_</span>
                        </div>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>

              <!-- 뉴스 아이템 -->
              <tr>
                <td style="padding: 4px 20px 0;">
                  {news_html}
                </td>
              </tr>

              <!-- 피드백 버튼 -->
              <tr>
                <td style="padding: 22px 20px 8px; text-align:center;">
                  <a href="{FEEDBACK_FORM_URL}"
                     style="display:inline-block; padding:10px 20px; background-color:#0e0e10; color:#3ee06a; font-family:'SF Mono', Menlo, monospace; font-size:12px; text-decoration:none; border-radius:8px;">
                    피드백 제출하기 &rsaquo;
                  </a>
                </td>
              </tr>

              <!-- 푸터 -->
              <tr>
                <td style="padding: 16px 20px 26px; text-align:center;">
                  <p style="font-family:'SF Mono', Menlo, monospace; font-size:10.5px; color:#bbb; margin:0;">
                  </p>
                </td>
              </tr>

            </table>
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

    print(f"파이프라인 완료! ({len(SUBSCRIBERS)}명 발송)")


if __name__ == "__main__":
    run_pipeline()
