import psycopg2
from config import pg_host, pg_database, pg_user, pg_password

create_table_query = """
CREATE TABLE IF NOT EXISTS reddit_watches (
    id VARCHAR(20) PRIMARY KEY,
    created_utc TIMESTAMP WITH TIME ZONE,
    title TEXT,
    username VARCHAR(50),
    num_comments INT,
    upvotes INT
);
"""

try:
    conn = psycopg2.connect(
        dbname=pg_database,
        user=pg_user,
        password=pg_password,
        host=pg_host
    )

    cur = conn.cursor()

    cur.execute(create_table_query)

    conn.commit()

    cur.close()
    conn.close()

    print("Table created successfully")

except Exception as e:
    print("An error occurred:", e)
