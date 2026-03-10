import urllib.request
import json
import csv
import sys
import time

# Flush print output immediately
sys.stdout.reconfigure(line_buffering=True)

API_URL = "https://belowthemarket.ca/api/marketplace-listings"
LIMIT = 8
OMIT_FIELDS = {"images", "thumbnails"}
THROTTLE_DELAY = 2  # seconds between requests


def fetch_page(offset):
    url = f"{API_URL}?limit={LIMIT}&offset={offset}&filter=all&v=1773110921873"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())


def matches_filter(listing):
    return (
        listing.get("isRentControlled") is True
        and listing.get("closestSubwayStation") == "Dundas West"
    )


def main():
    all_listings = []
    offset = 0

    while True:
        print(f"Fetching offset={offset} ...")
        data = fetch_page(offset)

        # API may return a list directly or wrap in an object
        if isinstance(data, list):
            page = data
        elif isinstance(data, dict):
            page = data.get("listings", data.get("data", []))
        else:
            break

        if not page:
            print("No more results.")
            break

        for listing in page:
            if matches_filter(listing):
                clean = {k: v for k, v in listing.items() if k not in OMIT_FIELDS}
                all_listings.append(clean)

        print(f"  Got {len(page)} listings, {len(all_listings)} matched so far.")

        if len(page) < LIMIT:
            break

        offset += LIMIT
        print(f"  Throttling {THROTTLE_DELAY}s ...")
        time.sleep(THROTTLE_DELAY)

    if not all_listings:
        print("No listings matched the filters.")
        return

    # Collect all field names across results
    fieldnames = list(dict.fromkeys(k for row in all_listings for k in row.keys()))

    out_path = "listings.csv"
    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_listings)

    print(f"\nWrote {len(all_listings)} listings to {out_path}")


if __name__ == "__main__":
    main()
