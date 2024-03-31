from sqlalchemy import create_engine
from config import pg_host, pg_database, pg_user, pg_password
from daily_scrapper import posts_df
import pandas as pd

connection_string = f"postgresql://{pg_user}:{pg_password}@{pg_host}/{pg_database}"

engine = create_engine(connection_string)

posts_df.to_sql('reddit_watches', con=engine, index=False, if_exists='append')
existing_ids = pd.read_sql_query("SELECT id FROM reddit_watches", con=engine)['id'].tolist()
new_posts_df = posts_df[~posts_df['id'].isin(existing_ids)]

new_posts_df.to_sql('reddit_watches', con=engine, index=False, if_exists='append')
