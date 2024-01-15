import requests
import folium
import polyline

url = "http://osrm/route/v1/driving/27.718107,85.317312;27.706190,85.316324"
r = requests.get(url, timeout=10)
res = r.json()
print(res)