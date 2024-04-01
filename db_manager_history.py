from sqlalchemy import create_engine, text
from config import pg_host, pg_database, pg_user, pg_password
from daily_scrapper import posts_df

connection_string = f"postgresql://{pg_user}:{pg_password}@{pg_host}/{pg_database}"

engine = create_engine(connection_string)

drop_table_command = text("DROP TABLE IF EXISTS reddit_watches;")

with engine.connect() as connection:
    connection.execute(drop_table_command)
    connection.commit()

posts_df.to_sql('reddit_watches', con=engine, index=False, if_exists='replace')


