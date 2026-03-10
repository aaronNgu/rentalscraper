# Listings Scraper

Fetches rental listings from the BelowTheMarket API and saves matching results to a CSV file.

## Filters

- `isRentControlled = true`
- `closestSubwayStation = "Dundas West"`
- Omits `images` and `thumbnails` fields from output

## Setup

```bash
python -m venv env
```

No external dependencies required — uses Python standard library only.

## Usage

```bash
./env/bin/python listings.py
```

Results are saved to `listings.csv` in the current directory.

## Configuration

Edit the constants at the top of `listings.py` to adjust:

- `LIMIT` — number of listings per API request (default: 8)
- `THROTTLE_DELAY` — seconds between requests to avoid rate limiting (default: 2)
