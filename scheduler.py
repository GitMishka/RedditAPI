import logging
from datetime import datetime
import time
import daily_scrapper
import db_manager_daily

# Configure logging
logging.basicConfig(filename='scheduler.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S',
                    filemode='a')  # Append mode

def run_daily_tasks():
    """
    This function wraps your daily tasks such as scraping new posts and updating the database.
    It logs the start and end of the task, along with any errors that might occur.
    """
    try:
        logging.info("Starting daily scraping task")
        
        # Run the scraper and get the latest posts
        posts_df = daily_scrapper.run_scrapper()
        logging.info("Scraping completed successfully")

        # Now, with the scraped data, update the database
        logging.info("Starting database update")
        db_manager_daily.update_database(posts_df)
        logging.info("Database update completed successfully")
        
    except Exception as e:
        logging.error("An error occurred during the daily tasks", exc_info=True)

def main():
    """
    Main function to run the scheduled tasks. It logs the overall start and end of the scheduler,
    as well as catches and logs any unhandled exceptions.
    """
    logging.info("Scheduler started")
    try:
        run_daily_tasks()
        logging.info("Scheduler completed its run successfully")
    except Exception as e:
        logging.critical("An unhandled exception stopped the scheduler", exc_info=True)
    finally:
        # daily runs
        time.sleep(86400)

if __name__ == "__main__":
    while True:
        main()
