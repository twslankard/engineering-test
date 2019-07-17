import requests

data = {"type": "Point", "coordinates": [-73.748751, 40.9185483]}
response = requests.get(
    'http://localhost:5000/find?search_distance=0.1',
    json=data
)
print(response.status_code)
print(response.text)
