import praw
import config
import pandas as pd
from datetime import datetime
from watchBrands import watch_brands
#credentials from config
reddit = praw.Reddit(
    client_id=config.reddit_client_id,
    client_secret=config.reddit_client_secret,
    user_agent="script:r/watches data collection:v1.0 (by u/{})".format(config.reddit_username),
    username=config.reddit_username,
    password=config.reddit_password,
)

subreddit = reddit.subreddit("watches")

posts_data = []

for submission in subreddit.new(limit=None):  # Adjust limit as necessary
    post_details = {
        "id": submission.id,
        "created_utc": datetime.utcfromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S'),  #UTC format

        "username": submission.author.name if submission.author else "N/A",
        "num_comments": submission.num_comments,
        "upvotes": submission.score,
        "title": submission.title, 
    }
    posts_data.append(post_details)

# Convert list of posts into a DataFrame
posts_df = pd.DataFrame(posts_data)

# Reorder the DataFrame columns to move 'title' to the last position
# columns_order = [col for col in posts_df.columns if col != 'title'] + ['title']
# posts_df = posts_df[columns_order]

# print(posts_df.head())
# posts_df.to_csv('watchHistory.csv')
def find_brand(title):
    for brand in watch_brands:
        if brand.lower() in title.lower():
            return brand
    return None  
posts_df['brand'] = posts_df['title'].apply(find_brand)
columns_order = ['id', 'created_utc', 'username', 'num_comments', 'upvotes', 'brand', 'title']
posts_df = posts_df[columns_order]
print(posts_df.head())
posts_df.to_csv('watchHistory.csv')
