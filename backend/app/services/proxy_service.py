import requests

def request_through_proxy(url: str):
    proxies = {
        "http": "http://127.0.0.1:8080",
        "https": "http://127.0.0.1:8080",
    }

    try:
        resp = requests.get(url, proxies=proxies, timeout=5)
        return {"content": resp.text[:200]}
    except Exception as e:
        return {"error": str(e)}
