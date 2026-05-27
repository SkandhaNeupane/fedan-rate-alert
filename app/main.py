from app.scraper.fedan_scraper import fetch_fedan_page
from app.scraper.parser import parse_fedan_data
from app.storage.rate_store import has_changed, save_today_rates
from app.notifier.email_sender import send_alert


def main():
    html = fetch_fedan_page()
    data = parse_fedan_data(html)

    print("Fetched:", data)

    if data.get("status") != "success":
        print("No valid data today.")
        return

    new_rates = {
        "10AM": data.get("10AM"),
        "2PM": data.get("2PM")
    }

    if has_changed(new_rates):
        print("Rates changed → updating storage")
        save_today_rates(new_rates)

        print("Sending EMAIL alerts")
        send_alert(new_rates)

    else:
        print("No change in rates")


if __name__ == "__main__":
    main()