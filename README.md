# CardScope

A responsive trading-card collection tracker built with Python Flask, HTML, CSS, and JavaScript.

## Features
- Mobile-friendly collector dashboard
- Add, edit, delete, search, filter, and sort cards
- Track Pokémon, sports cards, Magic: The Gathering, Yu-Gi-Oh!, Disney Lorcana, One Piece, Digimon, and other cards
- Record set, number, rarity, condition, owned status, purchase price, and saved market value
- Watchlist, collection value, estimated gain/loss, and CSV export
- Flask JSON API with local JSON storage
- Optional server-side PriceCharting API adapter
- Basic Progressive Web App support

## Run locally
Requires Python 3.10 or newer.

```bash
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000.

## Market data and API permissions
Sample prices are illustrative, not live quotes. Card prices vary by condition, grade, region, and sales venue. The optional PriceCharting adapter requires an active API subscription. Confirm the provider's current terms and get any required written permission before showing its data to other users or using it commercially. Keep API credentials on the server in environment variables; never place secrets in browser JavaScript or commit them to GitHub.

Set `PRICECHARTING_API_TOKEN` only if you are authorized. Coverage across sports and trading card games may be incomplete, and the adapter may need adjustment to match your subscription and current API documentation.

macOS/Linux:
```bash
export PRICECHARTING_API_TOKEN="your_private_token"
python app.py
```

Windows PowerShell:
```powershell
$env:PRICECHARTING_API_TOKEN="your_private_token"
python app.py
```

## Deploy
Use a host that supports Python/Flask. Configure the start command `python app.py`, set `PORT` if your host requires it, and add your API token in the host's secret/environment settings.

## Before a public launch
This starter does not include login, multi-user accounts, a production database, automated price history, or scheduled alerts. The JSON storage is intended for a starter project; add authentication and a database before serving multiple users.
