# from sqlalchemy import create_engine
# from config import pg_host, pg_database, pg_user, pg_password
# from daily_scrapper import posts_df
# import pandas as pd

# connection_string = f"postgresql://{pg_user}:{pg_password}@{pg_host}/{pg_database}"

# engine = create_engine(connection_string)

# posts_df.to_sql('reddit_watches', con=engine, index=False, if_exists='append')
# existing_ids = pd.read_sql_query("SELECT id FROM reddit_watches", con=engine)['id'].tolist()
# new_posts_df = posts_df[~posts_df['id'].isin(existing_ids)]

# new_posts_df.to_sql('reddit_watches', con=engine, index=False, if_exists='append')

from sqlalchemy import create_engine
import pandas as pd
from config import pg_host, pg_database, pg_user, pg_password
from daily_scrapper import posts_df

#connection
connection_string = f"postgresql://{pg_user}:{pg_password}@{pg_host}/{pg_database}"
engine = create_engine(connection_string)

# Fetch the list of existing post IDs from the database
existing_ids_query = "SELECT id FROM reddit_watches"
existing_ids = pd.read_sql_query(existing_ids_query, con=engine)['id'].tolist()

# Filter posts_df to only include rows where the id is not in the list of existing IDs
new_posts_df = posts_df[~posts_df['id'].isin(existing_ids)]

# Check if new_posts_df is not empty
if not new_posts_df.empty:
    # Append only new entries to the 'reddit_watches' table
    new_posts_df.to_sql('reddit_watches', con=engine, index=False, if_exists='append')
    print(f"Appended {len(new_posts_df)} new rows to the database.")
else:
    print("No new rows to append.")

