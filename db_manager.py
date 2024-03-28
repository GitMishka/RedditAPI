import psycopg2
from config import pg_host, pg_database, pg_user, pg_password
import pandas as pd
from reddit_scraper import posts_df

# Database connection
conn = psycopg2.connect(
    dbname=pg_database,
    user=pg_user,
    password=pg_password,
    host=pg_host
)
cur = conn.cursor()

# Insert data into the table from reddit_scrapper.py
insert_query = """
INSERT INTO reddit_watches (id, created_utc, title, username, num_comments, upvotes)
VALUES (%s, %s, %s, %s, %s, %s)
ON CONFLICT (id) DO NOTHING;
"""

for _, row in posts_df.iterrows():
    cur.execute(insert_query, (row["id"], row["created_utc"], row["title"], row["username"], row["num_comments"], row["upvotes"]))

conn.commit()

cur.close()
conn.close()

print("Data inserted successfully.")
