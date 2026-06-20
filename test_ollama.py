import requests

res = requests.post("http://localhost:11434/api/generate", json={
    "model": "mistral",
    "prompt": "List 3 characteristics of a good software requirement.",
    "stream": False
})
print(res.json()["response"])