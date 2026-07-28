import psycopg2
from send_mail import send_email

DB_CONFIG = {
    "dbname": "news_pipeline",
    "host": "localhost",
    "port": 5432
}

def get_recent_news(limit=10):
    """DB에서 저장된 뉴스 가져오기 (새로 수집 안 함)"""
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT title, link FROM raw_news
        ORDER BY collected_at DESC
        LIMIT %s
    """, (limit,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def format_email_body(news_list):
    """뉴스 리스트를 메일 본문 텍스트로 변환"""
    lines = ["기존에 저장된 뉴스입니다.\n"]
    for i, (title, link) in enumerate(news_list, 1):
        lines.append(f"{i}. {title}")
        lines.append(f"   {link}\n")
    return "\n".join(lines)

if __name__ == "__main__":
    print("1. DB에서 기존 뉴스 조회...")
    news_list = get_recent_news(limit=5)

    print(f"   {len(news_list)}건 조회됨")
    for title, link in news_list:
        print(f"   - {title}")

    print("2. 메일 본문 생성...")
    body = format_email_body(news_list)

    print("3. 메일 발송...")
    send_email(
        subject="기존 뉴스 테스트 발송",
        body=body,
        to_email="qorskawls12@naver.com"  # 본인 실제 주소로 바꾸세요
    )

    print("완료!")