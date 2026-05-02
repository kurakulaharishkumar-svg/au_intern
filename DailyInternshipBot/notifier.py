import requests
import os
import logging
import html

logger = logging.getLogger(__name__)

def send_telegram_message(text):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not token or not chat_id:
        logger.error("Telegram credentials missing! Check your .env file.")
        return
        
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code != 200:
            logger.error(f"Telegram API Error ({response.status_code}): {response.text}")
        response.raise_for_status()
        logger.info("Successfully sent message to Telegram.")
    except requests.RequestException as e:
        logger.error(f"Failed to send Telegram message: {e}")

def notify_jobs(jobs):
    if not jobs:
        return
        
    msg = "🔥 <b>Daily Internship Picks</b>\n\n"
    for i, job in enumerate(jobs, 1):
        msg += f"{i}. <b>{html.escape(job['title'])}</b> – {html.escape(job['company'])}\n"
        if 'score' in job:
            msg += f"   <i>Match Score: {job['score']}%</i>\n"
        msg += f"   Apply: <a href='{html.escape(job['link'])}'>Link</a>\n\n"
        
    send_telegram_message(msg)

def notify_failure():
    send_telegram_message("⚠️ <b>Failed to fetch internships today</b>\nCould be a network issue or anti-scraping blocks.")
