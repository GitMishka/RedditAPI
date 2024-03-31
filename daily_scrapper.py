import praw
import config
import pandas as pd
from datetime import datetime, timezone
from watchBrands import watch_brands
reddit = praw.Reddit(
    client_id=config.reddit_client_id,
    client_secret=config.reddit_client_secret,
    user_agent="script:r/watches data collection:v1.0 (by u/{})".format(config.reddit_username),
    username=config.reddit_username,
    password=config.reddit_password,
)

subreddit = reddit.subreddit("watches")

start_of_day = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)

posts_data = []

for submission in subreddit.new(limit=None):  
    submission_time = datetime.fromtimestamp(submission.created_utc, tz=timezone.utc)
    
    if submission_time >= start_of_day:
        post_details = {
            "id": submission.id,
            "created_utc": submission_time.strftime('%Y-%m-%d %H:%M:%S'),  # UTC format
            "username": submission.author.name if submission.author else "N/A",
            "num_comments": submission.num_comments,
            "upvotes": submission.score,
            "title": submission.title,
        }
        posts_data.append(post_details)

posts_df = pd.DataFrame(posts_data)

def find_brand(title):
    for brand in watch_brands:
        if brand.lower() in title.lower():
            return brand
    return None  
posts_df['brand'] = posts_df['title'].apply(find_brand)

columns_order = ['id', 'created_utc', 'username', 'num_comments', 'upvotes', 'brand', 'title']
posts_df = posts_df[columns_order]

print(posts_df.head())
now = datetime.now()
datetime_str = now.strftime('%Y%m%d-%H%M%S')
filename = f'dailyPosts_{datetime_str}.csv'
posts_df.to_csv(filename, index=False)