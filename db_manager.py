from sqlalchemy import create_engine
import pandas as pd
from config import pg_host, pg_database, pg_user, pg_password
from reddit_scraper import posts_df


# PostgreSQL connection string using variables from config.py
connection_string = f"postgresql://{pg_user}:{pg_password}@{pg_host}/{pg_database}"

# Create an SQLAlchemy engine
engine = create_engine(connection_string)

# Insert the DataFrame into the database
posts_df.to_sql('reddit_watches', con=engine, index=False, if_exists='replace')


