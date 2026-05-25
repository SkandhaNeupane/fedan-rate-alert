'''
from bs4 import BeautifulSoup

def parse_usd_rate(html):
    if not html:
        return None

    soup = BeautifulSoup(html, "html.parser")

    # Find all tables
    tables = soup.find_all("table")

    usd_rate = None

    for table in tables:
        rows = table.find_all("tr")

        for row in rows:
            cols = row.find_all("td")

            if len(cols) >= 3:
                text = cols[0].get_text(strip=True)

                # Look for USD row
                if "USD" in text:
                    try:
                        usd_rate = float(cols[2].get_text(strip=True))
                    except:
                        usd_rate = None

    return usd_rate'''



from bs4 import BeautifulSoup

def parse_usd_rate(html):
    if not html:
        return {"status": "error", "message": "No HTML received"}

    soup = BeautifulSoup(html, "html.parser")

    tables = soup.find_all("table")

    for table in tables:
        rows = table.find_all("tr")

        for row in rows:
            cols = row.find_all("td")

            if len(cols) >= 3:
                text = cols[0].get_text(strip=True)

                if "USD" in text:
                    try:
                        rate = float(cols[2].get_text(strip=True))

                        return {
                            "status": "success",
                            "currency": "USD",
                            "buy_rate": rate
                        }
                    except:
                        pass

    # 👇 IMPORTANT: graceful fallback
    return {
        "status": "no_data",
        "message": "No USD rate found (market closed or holiday)"
    }