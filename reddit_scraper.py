import praw
import config
import pandas as pd

#credentials from config
reddit = praw.Reddit(
    client_id=config.reddit_client_id,
    client_secret=config.reddit_client_secret,
    user_agent="script:r/watches data collection:v1.0 (by u/{})".format(config.reddit_username),
    username=config.reddit_username,
    password=config.reddit_password,
)

subreddit = reddit.subreddit("watches")

#empty list
posts_data = []

#Fetch entire history of r/watches
for submission in subreddit.new(limit=None):  #Remove 'limit=None' 
    post_details = {
        "id": submission.id,
        "created_utc": submission.created_utc,
        "title": submission.title,
        "username": submission.author.name if submission.author else None,
        "num_comments": submission.num_comments,
        "upvotes": submission.score,
    }
    posts_data.append(post_details)

#Create a DataFrame from the collected data
posts_df = pd.DataFrame(posts_data)

#Display the first few rows of the DataFrame
print(posts_df.head()) 