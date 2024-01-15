import requests
import folium
import polyline

url = "http://osrm:5000/route/v1/driving/-117.851364,33.698206;-117.838925,33.672260"
r = requests.get(url)
res = r.json()
print(res)