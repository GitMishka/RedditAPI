import praw
import config
import pandas as pd
from datetime import datetime, timezone
from watchBrands import watch_brands

# Initialize PRAW with your Reddit credentials from config
reddit = praw.Reddit(
    client_id=config.reddit_client_id,
    client_secret=config.reddit_client_secret,
    user_agent="script:r/watches data collection:v1.0 (by u/{})".format(config.reddit_username),
    username=config.reddit_username,
    password=config.reddit_password,
)

subreddit = reddit.subreddit("watches")

# Calculate the start of the current day in UTC
start_of_day = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)

posts_data = []

for submission in subreddit.new(limit=None):  # Adjust limit as necessary
    # Convert submission created_utc to a datetime object
    submission_time = datetime.utcfromtimestamp(submission.created_utc)
    
    # Check if the submission was created on the current day
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

# Convert list of posts into a DataFrame
posts_df = pd.DataFrame(posts_data)

# Function to find the first matching brand in a title
def find_brand(title):
    for brand in watch_brands:
        if brand.lower() in title.lower():
            return brand
    return None  # Returns None if no brand is found

# Add a 'brand' column to the DataFrame
posts_df['brand'] = posts_df['title'].apply(find_brand)

# Specify the desired column order, including the new 'brand' column
columns_order = ['id', 'created_utc', 'username', 'num_comments', 'upvotes', 'brand', 'title']
posts_df = posts_df[columns_order]

# Display the first few rows of the DataFrame
print(posts_df.head())
# Optionally, save the DataFrame to a CSV file
# posts_df.to_csv('watchHistory.csv')
