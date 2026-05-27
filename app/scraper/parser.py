from bs4 import BeautifulSoup

def parse_fedan_data(html):
    if not html:
        return {
            "status": "error",
            "message": "No HTML received"
        }

    soup = BeautifulSoup(html, "html.parser")

    # -------------------------
    # 1. Extract timestamps
    # -------------------------
    t1 = soup.find(id="ContentPlaceHolder1_lbl1opm")
    t2 = soup.find(id="ContentPlaceHolder1_lbl2pm")

    time_10am = t1.get_text(strip=True) if t1 else None
    time_2pm = t2.get_text(strip=True) if t2 else None

    # -------------------------
    # 2. Extract USD rates
    # -------------------------
    tables = soup.select("table.table.table-compact")

    rates = {}

    for i, table in enumerate(tables):
        rows = table.find_all("tr")

        for row in rows:
            cols = row.find_all("td")

            if len(cols) >= 3:
                text = cols[0].get_text(strip=True)

                if "USD" in text.upper():
                    try:
                        rate = float(
                            cols[2].get_text(strip=True).replace(",", "")
                        )

                        # Table mapping:
                        # 0 = 10 AM block
                        # 1 = 2 PM block
                        if i == 0:
                            rates["10AM"] = rate
                        elif i == 1:
                            rates["2PM"] = rate

                    except Exception:
                        continue

    if not rates:
        return {
            "status": "no_data",
            "message": "No USD rate found"
        }

    return {
        "status": "success",
        "10AM": rates.get("10AM"),
        "2PM": rates.get("2PM"),
        "time_10am": time_10am,
        "time_2pm": time_2pm
    }