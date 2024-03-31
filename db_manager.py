from sqlalchemy import create_engine, text
from config import pg_host, pg_database, pg_user, pg_password
from daily_scrapper import posts_df

connection_string = f"postgresql://{pg_user}:{pg_password}@{pg_host}/{pg_database}"

#Create an SQLAlchemy engine
engine = create_engine(connection_string)

#SQL command to drop the existing table (if it exists)
drop_table_command = text("DROP TABLE IF EXISTS reddit_watches;")

#drop the table command
with engine.connect() as connection:
    connection.execute(drop_table_command)
    connection.commit()

#This will create a new table with the structure inferred from posts_df
posts_df.to_sql('reddit_watches', con=engine, index=False, if_exists='replace')


