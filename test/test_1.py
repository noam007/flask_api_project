import requests   # local PC client

url = "http://127.0.0.1:5000/items"

data = requests.get(url)

items = data.json()
for item in items:
    print(item)

print (data)

# python requests :    https://www.w3schools.com/python/ref_requests_post.asp
