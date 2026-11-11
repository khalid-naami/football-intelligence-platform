from curl_cffi import requests
import json

headers = {
    'authority': 'api.sofascore.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'origin': 'https://www.sofascore.com',
    'referer': 'https://www.sofascore.com/',
    'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
}

print("Sending request with curl_cffi impersonate='chrome124'...")
try:
    res = requests.get(
        'https://api.sofascore.com/api/v1/sport/football/events/live',
        headers=headers,
        impersonate='chrome124',
        timeout=15
    )
    print("Status code:", res.status_code)
    if res.status_code == 200:
        data = res.json()
        events = data.get('events', [])
        print(f"SUCCESS! Total live football matches right now: {len(events)}")
        for idx, ev in enumerate(events[:8], 1):
            home = ev.get('homeTeam', {}).get('name')
            away = ev.get('awayTeam', {}).get('name')
            h_score = ev.get('homeScore', {}).get('current', 0)
            a_score = ev.get('awayScore', {}).get('current', 0)
            tournament = ev.get('tournament', {}).get('name')
            status = ev.get('status', {}).get('description')
            minute = ev.get('time', {}).get('played', '')
            min_str = f" ({minute}')" if minute else ""
            print(f"  {idx}. ⚽ [{tournament}] {home} {h_score} - {a_score} {away} | Status: {status}{min_str}")
    else:
        print("Response text:", res.text[:200])
except Exception as e:
    print("Exception:", e)
