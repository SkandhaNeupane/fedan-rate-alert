import requests

#URL = "http://www.fedan.com.np/"
URL = "http://fedan.com.np/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
}

def fetch_fedan_page():
    try:
        response = requests.get(URL, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.text

    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch FEDAN page: {e}")
        return None