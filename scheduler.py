from datetime import datetime
import time
import daily_scrapper
import db_manager_daily

def run_daily_tasks():
    print(f"Starting daily tasks at {datetime.now()}")
    # Run scrapper
    posts_df = daily_scrapper.run_scrapper()
    # Update database
    db_manager_daily.update_database(posts_df)
    print(f"Finished daily tasks at {datetime.now()}")

if __name__ == "__main__":
    # This is a simple loop to run the task daily, adjust as needed
    while True:
        run_daily_tasks()
        # Sleep for a day (24h * 60min * 60sec)
        time.sleep(86400)
