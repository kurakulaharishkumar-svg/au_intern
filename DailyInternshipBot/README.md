# Daily Internship Recommender Bot

A Python-based automation system that scrapes internship listings, filters them based on your desired skills, and sends the top daily picks to a Telegram chat.

## Features
- **Scraping**: Fetches jobs from Indeed using `requests` and `BeautifulSoup`.
- **Filtering**: Matches job title/description with user-defined skills and calculates a match score.
- **Deduplication**: Uses SQLite to remember sent jobs and avoid duplicates.
- **Notification**: Sends a clean HTML-formatted message to Telegram.
- **Scheduling**: Runs automatically using APScheduler (every 24 hours, or every 1 minute in test mode).

## Setup Instructions

1. **Navigate to project directory**:
   ```bash
   cd DailyInternshipBot
   ```

2. **Install Requirements**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:
   - Rename `.env.example` to `.env`
   - Open Telegram and search for **@BotFather** to create a new bot and get your `TELEGRAM_BOT_TOKEN`.
   - Start a chat with your new bot.
   - Search for **@userinfobot** in Telegram to get your `TELEGRAM_CHAT_ID`.
   - Add both token and chat ID to the `.env` file.
   - Leave `TEST_MODE=True` if you want it to run every minute for testing. Change to `False` for normal 24-hour operation.

4. **Run the Bot**:
   ```bash
   python main.py
   ```

## Customizing Skills
Open `main.py` and modify the `USER_SKILLS` list to match your career interests (e.g., "react", "node.js", "frontend").

## Log Activity
The bot logs its activity and any errors to `bot_activity.log` in the same folder.
