#!/usr/bin/env python3
"""demo_packet.py: writes a SAMPLE packet.json with the exact schema scan.py
produces, so the AI layer, merge, render, and delivery stages can be exercised
when live feeds are unavailable (sandboxed network, weekend, or a demo).

Every value below is fixture data, clearly labeled in the packet itself.
Run scan.py for the real thing.
"""

import json
from datetime import datetime
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")
now = datetime.now(ET)

packet = {
    "generated_at": now.isoformat(),
    "candidate_source": "demo_fixture",
    "trading_day_note": (
        "DEMO FIXTURE: sample data, not live quotes. Live feeds were "
        "unreachable from this environment. Run scan.py with open internet "
        "for real data."
    ),
    "scan_params": {"min_abs_gap_pct": 4.0, "min_price": 3.0, "max_gappers": 12},
    "criteria": {
        "day_eligible": (
            "Trend Join Long: gap > 3% and price > $3 and market cap > $1B "
            "and RVOL > 1.5 and price above yesterday's high "
            "(backtest 54.6% win rate, PF 1.59, 280 trades)"
        ),
        "swing_eligible": (
            "Swing: gap >= 8% and price > $3 and open > yesterday's high "
            "and open > 200-day SMA and market cap >= $800M and a real "
            "catalyst (backtest 57.6%/PF 5.34 news, 44.7%/PF 2.57 earnings)"
        ),
    },
    "market_snapshot": {
        "S&P 500": {"symbol": "^GSPC", "last": 6712.40, "prev_close": 6689.10, "change_pct": 0.35},
        "Dow": {"symbol": "^DJI", "last": 46890.22, "prev_close": 46812.55, "change_pct": 0.17},
        "Nasdaq": {"symbol": "^IXIC", "last": 23456.78, "prev_close": 23301.12, "change_pct": 0.67},
        "Russell 2000": {"symbol": "^RUT", "last": 2388.15, "prev_close": 2401.60, "change_pct": -0.56},
        "VIX": {"symbol": "^VIX", "last": 13.85, "prev_close": 14.42, "change_pct": -3.95},
        "US 10Y": {"symbol": "^TNX", "last": 4.18, "prev_close": 4.23, "change_pct": -1.18},
        "US 3M": {"symbol": "^IRX", "last": 4.32, "prev_close": 4.33, "change_pct": -0.23},
        "WTI Oil": {"symbol": "CL=F", "last": 71.34, "prev_close": 72.80, "change_pct": -2.01},
        "Dollar (DXY)": {"symbol": "DX-Y.NYB", "last": 101.22, "prev_close": 101.75, "change_pct": -0.52},
    },
    "econ_calendar": {
        "source": "https://nfs.faireconomy.media/ff_calendar_thisweek.json",
        "filter": "country=USD, impact=High",
        "today_date": str(now.date()),
        "tomorrow_date": "2026-07-05",
        "today": [
            {"time_et": "08:30", "title": "Non-Farm Employment Change", "forecast": "185K", "previous": "212K"},
            {"time_et": "08:30", "title": "Unemployment Rate", "forecast": "4.1%", "previous": "4.0%"},
            {"time_et": "10:00", "title": "ISM Services PMI", "forecast": "52.4", "previous": "53.1"},
        ],
        "tomorrow": [
            {"time_et": "14:00", "title": "FOMC Member Speech (Waller)", "forecast": "", "previous": ""},
        ],
    },
    "gappers": [
        {
            "ticker": "SMCI",
            "name": "Super Micro Computer, Inc.",
            "price": 52.80,
            "prev_close": 46.95,
            "gap_pct": 12.46,
            "market_cap": 30_500_000_000,
            "volume": 48_200_000,
            "intraday": {"vwap": 51.90, "hod": 53.40, "lod": 49.10, "premarket_high": 52.15, "premarket_volume": 3_900_000},
            "daily": {"sma_200": 41.20, "prior_day_high": 47.30, "prior_close": 46.95, "avg_volume_20d": 21_000_000, "today_open": 50.10, "today_volume": 48_200_000},
            "rvol": 2.30,
            "next_earnings": "2026-08-04",
            "catalyst_headlines": [
                {"source": "Reuters", "title": "Super Micro raises full-year revenue outlook on record AI server orders", "link": "", "published": "demo"},
                {"source": "CNBC", "title": "SMCI jumps double digits premarket after guidance hike", "link": "", "published": "demo"},
            ],
            "catalyst_found": True,
            "day_eligible": True,
            "swing_eligible": True,
        },
        {
            "ticker": "PLTR",
            "name": "Palantir Technologies Inc.",
            "price": 148.60,
            "prev_close": 139.75,
            "gap_pct": 6.33,
            "market_cap": 335_000_000_000,
            "volume": 61_500_000,
            "intraday": {"vwap": 147.20, "hod": 149.90, "lod": 144.30, "premarket_high": 147.80, "premarket_volume": 2_100_000},
            "daily": {"sma_200": 112.40, "prior_day_high": 141.10, "prior_close": 139.75, "avg_volume_20d": 38_000_000, "today_open": 145.20, "today_volume": 61_500_000},
            "rvol": 1.62,
            "next_earnings": "2026-08-10",
            "catalyst_headlines": [
                {"source": "Bloomberg", "title": "Palantir wins $1.2 billion Army software contract expansion", "link": "", "published": "demo"},
            ],
            "catalyst_found": True,
            "day_eligible": True,
            "swing_eligible": False,
        },
        {
            "ticker": "CELH",
            "name": "Celsius Holdings, Inc.",
            "price": 34.90,
            "prev_close": 31.70,
            "gap_pct": 10.09,
            "market_cap": 8_200_000_000,
            "volume": 12_800_000,
            "intraday": {"vwap": 34.10, "hod": 35.60, "lod": 33.20, "premarket_high": 34.55, "premarket_volume": 850_000},
            "daily": {"sma_200": 38.75, "prior_day_high": 32.05, "prior_close": 31.70, "avg_volume_20d": 9_500_000, "today_open": 33.80, "today_volume": 12_800_000},
            "rvol": 1.35,
            "next_earnings": "2026-08-06",
            "catalyst_headlines": [
                {"source": "MarketWatch", "title": "Celsius surges after PepsiCo expands distribution deal to Europe", "link": "", "published": "demo"},
            ],
            "catalyst_found": True,
            "day_eligible": False,
            "swing_eligible": False,
        },
        {
            "ticker": "AVXL",
            "name": "Anavex Life Sciences Corp.",
            "price": 9.84,
            "prev_close": 7.42,
            "gap_pct": 32.61,
            "market_cap": 830_000_000,
            "volume": 6_200_000,
            "intraday": {"vwap": 9.55, "hod": 10.20, "lod": 8.90, "premarket_high": 9.95, "premarket_volume": 1_400_000},
            "daily": {"sma_200": 8.10, "prior_day_high": 7.55, "prior_close": 7.42, "avg_volume_20d": 1_100_000, "today_open": 9.30, "today_volume": 6_200_000},
            "rvol": 5.64,
            "next_earnings": None,
            "catalyst_headlines": [],
            "catalyst_found": False,
            "day_eligible": False,
            "swing_eligible": False,
        },
        {
            "ticker": "RIVN",
            "name": "Rivian Automotive, Inc.",
            "price": 11.20,
            "prev_close": 12.05,
            "gap_pct": -7.05,
            "market_cap": 11_400_000_000,
            "volume": 29_000_000,
            "intraday": {"vwap": 11.35, "hod": 11.80, "lod": 11.05, "premarket_high": 11.60, "premarket_volume": 1_900_000},
            "daily": {"sma_200": 13.60, "prior_day_high": 12.20, "prior_close": 12.05, "avg_volume_20d": 24_000_000, "today_open": 11.45, "today_volume": 29_000_000},
            "rvol": 1.21,
            "next_earnings": "2026-08-07",
            "catalyst_headlines": [
                {"source": "Reuters", "title": "Rivian cuts 2026 delivery guidance, cites component shortages", "link": "", "published": "demo"},
            ],
            "catalyst_found": True,
            "day_eligible": False,
            "swing_eligible": False,
        },
    ],
    "market_news": [
        {"source": "Reuters", "title": "Wall St futures edge higher ahead of June jobs report", "summary": "Index futures rose as traders awaited nonfarm payrolls.", "link": "", "published": "demo"},
        {"source": "CNBC", "title": "Oil slides 2% as OPEC+ signals output hike", "summary": "Crude fell on supply expectations.", "link": "", "published": "demo"},
        {"source": "Bloomberg", "title": "Treasury yields dip as rate-cut bets firm for September", "summary": "The 10-year eased to 4.18%.", "link": "", "published": "demo"},
        {"source": "MarketWatch", "title": "AI server names rally premarket on Super Micro guidance", "summary": "Hardware suppliers move in sympathy.", "link": "", "published": "demo"},
    ],
    "gaps_to_fill": [
        "market-wide earnings calendar only partial (per-gapper next_earnings only)",
        "intraday levels need intraday bars; empty on non-trading days",
        "RVOL is full-day relative volume; true premarket RVOL needs a premarket feed like Alpaca",
        "THIS PACKET IS A DEMO FIXTURE, values are sample data",
    ],
}

with open("packet.json", "w", encoding="utf-8") as f:
    json.dump(packet, f, indent=2)
print(f"[demo] WROTE packet.json (demo fixture, {len(packet['gappers'])} gappers)")
