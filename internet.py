import requests

url = "https://cdn.truefilesize.com/test/test-100mb.bin"

try:
    r = requests.head(url, timeout=10)

    print("Status:", r.status_code)
    print("Headers:", r.headers)

except Exception as e:
    print("ERROR:", repr(e))