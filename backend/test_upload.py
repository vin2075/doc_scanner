import requests

url = "http://127.0.0.1:5000/upload"
files = {"file": open("E:/docscanner-project/backend/v.pdf", "rb")}
response = requests.post(url, files=files)

print(response.status_code)
print(response.text)
