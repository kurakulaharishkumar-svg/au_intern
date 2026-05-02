import os
import logging
# Load .env FIRST before anything else that might read env vars
from dotenv import load_dotenv
load_dotenv()

from scraper import fetch_internships
from filter import rank_and_filter
from database import init_db, is_duplicate, mark_as_sent
from notifier import notify_jobs, notify_failure, send_telegram_message
from scheduler import start_scheduler

# Configure logging to file and console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot_activity.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# User defined skills / keywords for filtering
USER_SKILLS = [
    "python", "machine learning", "data science",
    "sql", "ai", "pandas", "software", "developer", "engineer"
]

def job_pipeline():
    logger.info("Starting internship fetching pipeline...")

    # 1. Fetch from source
    jobs = fetch_internships(query="python developer", location="Remote")
    if jobs is None:
        logger.error("Failed to fetch jobs from all sources.")
        notify_failure()
        return

    if not jobs:
        logger.warning("No jobs fetched today. Trying broader search...")
        jobs = fetch_internships(query="remote", location="")
        if not jobs:
            logger.warning("Still no jobs. Skipping this cycle.")
            return

    logger.info(f"Fetched {len(jobs)} jobs. Filtering and ranking...")

    # 2. Filter & Rank
    ranked_jobs = rank_and_filter(jobs, USER_SKILLS)

    # If skill filter eliminates everything, fall back to all jobs
    if not ranked_jobs:
        logger.warning("No skill matches found. Sending top jobs without filtering.")
        ranked_jobs = jobs

    # 3. Deduplicate
    new_jobs = []
    for job in ranked_jobs:
        if not is_duplicate(job['link']):
            new_jobs.append(job)
            if len(new_jobs) == 5:
                break

    # 4. Notify
    if new_jobs:
        logger.info(f"Found {len(new_jobs)} new internships. Sending to Telegram...")
        notify_jobs(new_jobs)
        for job in new_jobs:
            mark_as_sent(job['link'])
        logger.info("Successfully sent and marked jobs as sent.")
    else:
        logger.info("No new internships found today (all were already sent).")

if __name__ == "__main__":
    # Verify env vars are loaded
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    logger.info("Initializing Daily Internship Recommender Bot...")
    logger.info(f"Telegram Token loaded: {'YES' if token else 'NO - CHECK .env FILE!'}")
    logger.info(f"Telegram Chat ID loaded: {'YES (' + str(chat_id) + ')' if chat_id else 'NO - CHECK .env FILE!'}")

    # Send a test message to confirm Telegram is working
    logger.info("Sending Telegram test message...")
    send_telegram_message("✅ <b>Bot is starting up!</b>\nInternship Recommender Bot is now active.")

    init_db()

    # Check test mode flag in .env
    test_mode = os.getenv("TEST_MODE", "False").lower() in ("true", "1", "yes")
    logger.info(f"Test mode: {test_mode}")

    # Run once immediately on startup
    job_pipeline()

    # Block and wait for scheduled intervals
    start_scheduler(job_pipeline, test_mode=test_mode)
