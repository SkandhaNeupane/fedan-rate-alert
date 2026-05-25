'''
from app.scraper.fedan_scraper import fetch_fedan_page
from app.scraper.parser import parse_usd_rate


def main():
    html = fetch_fedan_page()
    usd = parse_usd_rate(html)

    if usd:
        print({
            "currency": "USD",
            "buy_rate": usd
        })
    else:
        print("Failed to extract USD rate")


if __name__ == "__main__":
    main()'''  


from app.scraper.fedan_scraper import fetch_fedan_page
from app.scraper.parser import parse_usd_rate

def main():
    html = fetch_fedan_page()
    result = parse_usd_rate(html)

    print(result)

if __name__ == "__main__":
    main()