from psaw import PushshiftAPI
import pandas as pd
from datetime import datetime

# Initialize PushshiftAPI
api = PushshiftAPI()

# Define the subreddit and potentially the time range
subreddit_name = 'Watches'  # replace with your target subreddit
start_epoch = int(datetime(2019, 1, 1).timestamp())  # Start date: January 1, 2019

# Search submissions in the defined subreddit starting from 'start_epoch'
submissions = api.search_submissions(after=start_epoch, subreddit=subreddit_name, limit=5000)

posts_data = []

for submission in submissions:
    try:
        # Ensure the submission has not been deleted and contains all necessary data
        if submission.author and not submission.removed_by_category:
            post_details = {
                "id": submission.id,
                "created_utc": datetime.utcfromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                "username": submission.author.name,
                "num_comments": submission.num_comments,
                "upvotes": submission.score,
                "title": submission.title,
            }
            posts_data.append(post_details)
    except Exception as e:
        print(f"Error processing submission {submission.id}: {str(e)}")

# Convert the list of post details into a DataFrame
posts_df = pd.DataFrame(posts_data)

# Display the first few rows of the DataFrame
print(posts_df.head())

# Optionally, save the DataFrame to a CSV file for later analysis
posts_df.to_csv('extended_subreddit_posts.csv', index=False)
