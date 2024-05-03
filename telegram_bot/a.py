import requests

collection = "degods"

url = f"https://api.opensea.io/api/v2/collections/{collection}/stats"

headers = {"accept": "application/json",
    "x-api-key": "79d9f612887948faa06cd69bc0255a26"
    }

response = requests.get(url, headers=headers)
print(response.json())
