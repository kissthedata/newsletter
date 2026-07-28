import psycopg2
from datetime import datetime

DB_CONFIG = {
    "dbname": "news_pipeline",
    "host": "localhost",
    "port": 5432
}

def init_db():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS raw_news (
            id SERIAL PRIMARY KEY,
            query TEXT,
            title TEXT,
            link TEXT,
            pub_date TEXT,
            collected_at TIMESTAMP
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

def save_news(query, news_items):
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    for item in news_items:
        cursor.execute("""
            INSERT INTO raw_news (query, title, link, pub_date, collected_at)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            query,
            item['title'],
            item['link'],
            item['pubDate'],
            datetime.now()
        ))

    conn.commit()
    cursor.close()
    conn.close()
    print(f"{len(news_items)}건 저장 완료")