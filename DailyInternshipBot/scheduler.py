from apscheduler.schedulers.blocking import BlockingScheduler
import logging

logger = logging.getLogger(__name__)

def start_scheduler(job_function, test_mode=False):
    """Starts the blocking scheduler to run the job_function periodically."""
    scheduler = BlockingScheduler()
    
    if test_mode:
        logger.info("Starting scheduler in TEST mode (every 1 minute)")
        scheduler.add_job(job_function, 'interval', minutes=1)
    else:
        logger.info("Starting scheduler in NORMAL mode (every 24 hours)")
        scheduler.add_job(job_function, 'interval', hours=24)
        
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Scheduler stopped by user.")
