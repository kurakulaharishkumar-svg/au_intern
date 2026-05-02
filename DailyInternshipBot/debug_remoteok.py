import requests
url = 'https://remoteok.com/api'
headers = {'User-Agent': 'Mozilla/5.0'}
r = requests.get(url, headers=headers)
data = r.json()
print(f'Items: {len(data)}')
for item in data[:10]:
    if isinstance(item, dict):
        print(f"TITLE: {item.get('position')} | COMPANY: {item.get('company')}")
        print(f"TAGS: {item.get('tags')}")
        print("-" * 20)
