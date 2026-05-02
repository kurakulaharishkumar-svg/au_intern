import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)


def fetch_from_remoteok(query="python"):
    """
    Fetches jobs from RemoteOK's public API.
    Returns all jobs matching a broad search tag.
    """
    logger.info("Fetching from RemoteOK public API...")

    # RemoteOK API supports tag-based filtering
    # Clean the query: use just first word as tag, or 'dev' as default
    tag = query.strip().split()[0].lower()
    url = f"https://remoteok.com/api?tag={tag}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()

        jobs = []
        for item in data:
            if not isinstance(item, dict):
                continue
            # Skip the metadata header entry
            if 'legal' in item:
                continue

            title = item.get('position', '').strip()
            company = item.get('company', 'Remote Company').strip()
            job_url = item.get('url', '')
            description = item.get('description', '') or item.get('tags', '')

            if isinstance(description, list):
                description = " ".join(description)

            if title and job_url:
                jobs.append({
                    'title': title,
                    'company': company,
                    'link': job_url,
                    'description': str(description)[:500]
                })

        logger.info(f"Fetched {len(jobs)} jobs from RemoteOK (tag: {tag}).")
        return jobs

    except Exception as e:
        logger.error(f"RemoteOK fetch failed: {e}")
        return []


def fetch_internships(query="Internship", location="Remote"):
    """
    Primary scraper: Indeed.
    Automatic fallback: RemoteOK (if Indeed is blocked).
    """
    q = query.replace(' ', '+')
    l = location.replace(' ', '+')
    indeed_url = f"https://www.indeed.com/jobs?q={q}&l={l}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/",
        "DNT": "1",
        "Connection": "keep-alive",
    }

    logger.info(f"Attempting Indeed scrape: {indeed_url}")
    try:
        response = requests.get(indeed_url, headers=headers, timeout=15)

        if response.status_code == 403:
            logger.warning("Indeed blocked with 403. Switching to RemoteOK...")
            return fetch_from_remoteok(query)

        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        cards = soup.find_all('div', class_=['job_seen_beacon', 'result', 'jobsearch-SerpJobCard'])

        if not cards:
            logger.warning("Indeed returned 200 but no job cards parsed. Switching to RemoteOK...")
            return fetch_from_remoteok(query)

        jobs = []
        for card in cards:
            title_elem = (card.find('h2', class_='jobTitle') or
                          card.find('a', class_='jcs-JobTitle') or
                          card.find('h2'))
            company_elem = (card.find('span', class_='companyName') or
                            card.find('span', {'data-testid': 'company-name'}))
            link_elem = card.find('a', class_='jcs-JobTitle') or card.find('a', href=True)
            desc_elem = card.find('div', class_='job-snippet') or card.find('div', class_='css-9446fg')

            if title_elem and company_elem and link_elem:
                href = link_elem.get('href', '')
                link = f"https://www.indeed.com{href}" if href.startswith('/') else href
                jobs.append({
                    'title': title_elem.get_text(strip=True),
                    'company': company_elem.get_text(strip=True),
                    'link': link,
                    'description': desc_elem.get_text(strip=True) if desc_elem else ""
                })

        logger.info(f"Fetched {len(jobs)} jobs from Indeed.")
        return jobs

    except requests.RequestException as e:
        logger.error(f"Indeed request failed: {e}. Trying RemoteOK...")
        return fetch_from_remoteok(query)
