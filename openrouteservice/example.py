import requests
import folium
import polyline

url = "http://osrm/route/v1/driving/27.718107,85.317312;27.706190,85.316324"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
    'Accept': 'application/json',
    'Accept-Language': 'en-USen;q=0.5',
    'Referer': 'https://stats.nba.com/',
    'Accept-Encoding': 'gzip,deflate br',
    'Connection': 'keep-alive',
    'x-nba-stats-origin': 'stats',
    'x-nba-stats-token': 'true'
}

r = requests.get(url, timeout=10, headers=headers, allow_redirects=False)
res = r.json()
print(res)