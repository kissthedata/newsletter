import os
import psycopg2
from datetime import datetime
from dotenv import load_dotenv

# 로컬 환경 테스트용 .env 로드
load_dotenv()

# 환경변수에서 DB 정보 읽기 (없으면 로컬 기본값 사용)
DB_CONFIG = {
    "dbname": os.environ.get("DB_NAME", "news_pipeline"),
    "user": os.environ.get("DB_USER", "postgres"),
    "password": os.environ.get("DB_PASSWORD", ""),
    "host": os.environ.get("DB_HOST", "localhost"),
    "port": os.environ.get("DB_PORT", "5432"),
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS raw_news (
            id SERIAL PRIMARY KEY,
            query TEXT,
            title TEXT,
            link TEXT UNIQUE,
            pub_date TEXT,
            collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

def save_news(query, news_items):
    conn = get_connection()
    cursor = conn.cursor()
    saved_count = 0

    for item in news_items:
        try:
            # ON CONFLICT (link) DO NOTHING: 중복 링크 기사는 알아서 패스
            cursor.execute("""
                INSERT INTO raw_news (query, title, link, pub_date, collected_at)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (link) DO NOTHING
            """, (
                query,
                item['title'],
                item['link'],
                item['pubDate'],
                datetime.now()
            ))
            if cursor.rowcount > 0:
                saved_count += 1
        except Exception as e:
            print(f"Error saving item: {e}")
            conn.rollback()
            continue

    conn.commit()
    cursor.close()
    conn.close()
    print(f"[{query}] {saved_count}건 신규 저장 완료")