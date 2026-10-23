# CardScope

CardScope is a mobile-friendly trading-card collection and price-tracking web app built with Python, Flask, HTML, CSS, and JavaScript. The interface is designed to work on desktop and phones and includes Progressive Web App (PWA) support.

## What works

- Dashboard with collection value, owned-card count, watchlist count, and estimated gain/loss.
- Add, edit, and delete cards.
- Track Pokémon, sports cards, Magic: The Gathering, Yu-Gi-Oh!, Disney Lorcana, One Piece, Digimon, and other collectibles.
- Save card name, set, number, rarity, condition/grade, image URL, purchase cost, and market estimate.
- Search by name, set, number, rarity, or game; filter by game; sort by name or price.
- Move cards between owned collection and watchlist.
- Export your collection to CSV.
- Download and import a JSON backup.
- Price-discovery interface connected to the optional PriceCharting API adapter.
- Installable-style PWA manifest and offline caching for the app shell.
- JSON REST endpoints for cards and provider lookup.

## Run it on your computer

Requires Python 3.10 or newer.

```bash
git clone https://github.com/Jackson202-svg/card-price-tracker.git
cd card-price-tracker
python -m venv .venv
```

Activate the environment:

**Windows PowerShell**
```powershell
.venv\Scripts\Activate.ps1
```

**macOS/Linux**
```bash
source .venv/bin/activate
```

Install and start:

```bash
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000 in your browser. Keep the terminal window open while using the app.

## Live price data

The app never pretends its demo or manually entered values are live quotes. Price lookup requires a valid, authorized PriceCharting API subscription/token. Add `PRICECHARTING_API_TOKEN` as a server environment variable in your hosting provider's secret settings. Do not put the token in JavaScript, HTML, or a public repository.

**macOS/Linux**
```bash
export PRICECHARTING_API_TOKEN="your_private_token"
python app.py
```

**Windows PowerShell**
```powershell
$env:PRICECHARTING_API_TOKEN="your_private_token"
python app.py
```

Coverage, field names, and commercial display rights depend on the provider plan and terms. Verify the current API documentation and permissions before public or commercial use. Prices vary by card condition, grade, geography, and marketplace.

## Deploy it as a website

Use a Python/Flask-compatible host. Typical settings:

- Build/install command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app`
- Health-check path (if supported): `/api/health`
- Environment variable: `PRICECHARTING_API_TOKEN` only when authorized.

Set `PORT` if your host requires it. The included JSON file storage is suitable for a local starter/single-user demo, **not a multi-user production service**. Many hosts use ephemeral filesystems, which can reset saved cards during redeploys. Before relying on a live public site, move data to a persistent database (for example PostgreSQL) and add accounts, authorization, backups, and rate limiting. A persistent disk can be an interim option where your host supports it.

## API routes

- `GET /api/health` — health and provider configuration status.
- `GET /api/cards?q=&game=&owned=` — list/search cards.
- `POST /api/cards` — add a card.
- `PATCH /api/cards/<card_id>` — edit card fields or ownership.
- `DELETE /api/cards/<card_id>` — delete a card.
- `GET /api/price-search?q=` — search the configured provider.

## Current limitations

This is a working MVP, not yet a full commercial PriceCharting replacement. It currently has no user login, shared cloud collection, production database, automatic scheduled repricing, historical price charts, push notifications, or barcode scanner. These require additional backend services, provider access, and security work before a public multi-user launch.
