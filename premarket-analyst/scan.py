#!/usr/bin/env python3
"""scan.py: the data gatherer.

One job only: collect raw premarket data into packet.json.
ZERO analysis. No conviction, no buckets, no opinions.
All judgment happens later in the AI prompt files.

Free and keyless: yfinance + feedparser + requests. zoneinfo is stdlib.
"""

import json
import os
import re
import time
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import feedparser
import requests
import yfinance as yf

ET = ZoneInfo("America/New_York")

# ---------------------------------------------------------------- constants

SNAPSHOT_SYMBOLS = {
    "S&P 500": "^GSPC",
    "Dow": "^DJI",
    "Nasdaq": "^IXIC",
    "Russell 2000": "^RUT",
    "VIX": "^VIX",
    "US 10Y": "^TNX",
    "US 3M": "^IRX",
    "WTI Oil": "CL=F",
    "Dollar (DXY)": "DX-Y.NYB",
}

# Static fallback universe if the live screeners come back thin.
UNIVERSE = [
    "NVDA", "AMD", "AVGO", "SMCI", "MRVL", "TSLA", "AAPL", "MSFT", "META",
    "AMZN", "GOOGL", "NFLX", "DELL", "SNOW", "PLTR", "COIN", "MSTR", "SOFI",
    "RIVN", "NIO", "MARA", "RIOT", "BA", "DIS", "JPM", "BAC", "XOM", "CVX",
    "HOOD", "UBER", "CRWD", "PANW", "CELH", "LULU", "NKE", "CAVA", "DKNG",
    "ARM", "INTC", "MU",
]

MIN_ABS_GAP = 4.0   # keep movers with abs gap pct >= this
MIN_PRICE = 3.0     # and price >= this
MAX_GAPPERS = 12

RSS_FEEDS = {
    "MarketWatch Top": "https://feeds.content.dowjones.io/public/rss/mw_topstories",
    "MarketWatch RealTime": "https://feeds.content.dowjones.io/public/rss/mw_realtimeheadlines",
    "CNBC": "https://www.cnbc.com/id/100003114/device/rss/rss.html",
    "Yahoo Finance": "https://finance.yahoo.com/news/rssindex",
    "Google News Markets": (
        "https://news.google.com/rss/search?"
        "q=stock%20market%20OR%20earnings%20when:1d&hl=en-US&gl=US&ceid=US:en"
    ),
}

# Titles that are SEO spam, not news.
SPAM_RE = re.compile(r"price prediction|20\d\d-20\d\d", re.IGNORECASE)

# Primary publishers rank first when picking catalyst headlines.
PRIMARY_PUBLISHERS = [
    "bloomberg", "reuters", "cnbc", "marketwatch", "barron", "yahoo finance",
    "wsj", "wall street journal", "financial times", "associated press",
]

# Generic company-name words that must NEVER match a company on their own.
# Naive matching is a trap: "Applied" alone would tag both Applied
# Optoelectronics and Applied Digital, so generic tokens are stopped here.
NAME_STOP = {
    "the", "inc", "incorporated", "corp", "corporation", "co", "company",
    "holdings", "holding", "group", "plc", "ltd", "limited", "technologies",
    "technology", "tech", "digital", "applied", "advanced", "strategy",
    "strategies", "motors", "motor", "energy", "platforms", "platform",
    "systems", "system", "solutions", "solution", "industries", "industrial",
    "international", "global", "national", "american", "united", "first",
    "new", "capital", "financial", "services", "service", "brands", "labs",
    "media", "entertainment", "communications", "class", "common", "stock",
    "shares", "adr", "trust", "fund", "acquisition", "resources", "partners",
    "pharmaceuticals", "pharma", "therapeutics", "sciences", "science",
    "health", "medical", "bio", "data", "software", "semiconductor", "micro",
    "devices", "enterprise", "enterprises", "interactive", "dynamics", "air",
    "lines", "airlines", "and", "of",
}

ECON_URL = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"
ECON_CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".ff_calendar_cache.json")
ECON_CACHE_TTL = 4 * 3600  # the feed rate-limits (429) on rapid calls

HEADERS = {"User-Agent": "Mozilla/5.0 (premarket-analyst scan.py)"}


def log(msg):
    print(f"[scan] {msg}", flush=True)


def safe(fn, fallback=None, label=""):
    """Run fn(), never raise. One bad ticker must not crash the run."""
    try:
        return fn()
    except Exception as e:
        if label:
            log(f"  warn: {label}: {type(e).__name__}: {e}")
        return fallback


# ---------------------------------------------------------- market snapshot

def get_market_snapshot():
    log("market snapshot...")
    snap = {}
    for name, sym in SNAPSHOT_SYMBOLS.items():
        def pull(sym=sym):
            hist = yf.Ticker(sym).history(period="5d", interval="1d")
            closes = hist["Close"].dropna()
            if len(closes) < 2:
                return None
            last, prev = float(closes.iloc[-1]), float(closes.iloc[-2])
            return {
                "symbol": sym,
                "last": round(last, 2),
                "prev_close": round(prev, 2),
                "change_pct": round((last - prev) / prev * 100, 2),
            }
        row = safe(pull, label=f"snapshot {sym}")
        if row:
            snap[name] = row
    log(f"  snapshot: {len(snap)}/{len(SNAPSHOT_SYMBOLS)} instruments")
    return snap


# ------------------------------------------------------------- top movers

def screen_quotes(kind):
    def pull():
        res = yf.screen(kind, count=25)
        return res.get("quotes", []) if isinstance(res, dict) else []
    return safe(pull, fallback=[], label=f"screener {kind}") or []


def get_candidates():
    """Live keyless screeners first, static universe as the fallback."""
    log("top movers via yfinance screeners...")
    quotes, seen = [], set()
    for kind in ("day_gainers", "most_actives"):
        for q in screen_quotes(kind):
            sym = q.get("symbol")
            if not sym or sym in seen:
                continue
            seen.add(sym)
            quotes.append({
                "ticker": sym,
                "name": q.get("shortName") or q.get("longName") or sym,
                "price": q.get("regularMarketPrice"),
                "prev_close": q.get("regularMarketPreviousClose"),
                "gap_pct": q.get("regularMarketChangePercent"),
                "market_cap": q.get("marketCap"),
                "volume": q.get("regularMarketVolume"),
            })
    if len(quotes) >= 5:
        log(f"  screeners returned {len(quotes)} names")
        return quotes, "live_screener"

    log(f"  screeners thin ({len(quotes)}), falling back to static universe")
    quotes = []
    for sym in UNIVERSE:
        def pull(sym=sym):
            t = yf.Ticker(sym)
            hist = t.history(period="5d", interval="1d")
            closes = hist["Close"].dropna()
            if len(closes) < 2:
                return None
            last, prev = float(closes.iloc[-1]), float(closes.iloc[-2])
            info = t.fast_info
            return {
                "ticker": sym,
                "name": sym,
                "price": round(last, 2),
                "prev_close": round(prev, 2),
                "gap_pct": round((last - prev) / prev * 100, 2),
                "market_cap": getattr(info, "market_cap", None),
                "volume": int(hist["Volume"].iloc[-1]),
            }
        row = safe(pull, label=f"universe {sym}")
        if row:
            quotes.append(row)
    return quotes, "static_universe"


def filter_gappers(candidates):
    kept = [
        c for c in candidates
        if c.get("gap_pct") is not None and c.get("price") is not None
        and abs(c["gap_pct"]) >= MIN_ABS_GAP and c["price"] >= MIN_PRICE
    ]
    kept.sort(key=lambda c: abs(c["gap_pct"]), reverse=True)
    log(f"gap filter: {len(kept)} of {len(candidates)} pass, keeping top {MAX_GAPPERS}")
    return kept[:MAX_GAPPERS]


# ---------------------------------------------------------------- RSS news

def strip_html(text):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", text or "")).strip()


def get_market_news():
    log("market news from RSS...")
    items = []
    for source, url in RSS_FEEDS.items():
        def pull(source=source, url=url):
            feed = feedparser.parse(url, request_headers=HEADERS)
            out = []
            for e in feed.entries[:20]:
                title = strip_html(e.get("title", ""))
                if not title or SPAM_RE.search(title):
                    continue
                out.append({
                    "source": source,
                    "title": title,
                    "summary": strip_html(e.get("summary", ""))[:280],
                    "link": e.get("link", ""),
                    "published": e.get("published", e.get("updated", "")),
                })
            return out
        got = safe(pull, fallback=[], label=f"rss {source}") or []
        log(f"  {source}: {len(got)} items")
        items.extend(got)
    return items


# --------------------------------------------------------- economic calendar

def get_econ_calendar():
    """US High-impact events for today and tomorrow (ET) from the
    ForexFactory data-partner weekly JSON feed. Cached locally because the
    feed 429s on rapid calls. Fully defensive: never raises."""
    log("economic calendar...")
    note = ""
    raw, fetched_at = None, None

    if os.path.exists(ECON_CACHE):
        cached = safe(lambda: json.load(open(ECON_CACHE, encoding="utf-8")), label="econ cache read")
        if cached and time.time() - cached.get("fetched_at", 0) < ECON_CACHE_TTL:
            raw, fetched_at = cached["events"], cached["fetched_at"]
            log("  using cached weekly feed")

    if raw is None:
        def pull():
            r = requests.get(ECON_URL, headers=HEADERS, timeout=20)
            r.raise_for_status()
            return r.json()
        raw = safe(pull, label="econ fetch")
        if raw is not None:
            fetched_at = time.time()
            safe(lambda: json.dump({"fetched_at": fetched_at, "events": raw},
                                   open(ECON_CACHE, "w", encoding="utf-8")), label="econ cache write")
        else:
            cached = safe(lambda: json.load(open(ECON_CACHE, encoding="utf-8")), label="econ cache fallback")
            if cached:
                raw, fetched_at = cached["events"], cached["fetched_at"]
                note = "live fetch failed, using stale cached week"

    today = datetime.now(ET).date()
    tomorrow = today + timedelta(days=1)
    cal = {
        "source": ECON_URL,
        "filter": "country=USD, impact=High",
        "today_date": str(today),
        "tomorrow_date": str(tomorrow),
        "today": [],
        "tomorrow": [],
    }
    if note:
        cal["note"] = note
    if raw is None:
        cal["error"] = "calendar feed unavailable"
        return cal

    for ev in raw:
        try:
            if ev.get("country") != "USD" or ev.get("impact") != "High":
                continue
            dt = datetime.fromisoformat(ev["date"]).astimezone(ET)
            row = {
                "time_et": dt.strftime("%H:%M"),
                "title": ev.get("title", ""),
                "forecast": ev.get("forecast", ""),
                "previous": ev.get("previous", ""),
            }
            if dt.date() == today:
                cal["today"].append(row)
            elif dt.date() == tomorrow:
                cal["tomorrow"].append(row)
        except Exception:
            continue
    cal["today"].sort(key=lambda r: r["time_et"])
    cal["tomorrow"].sort(key=lambda r: r["time_et"])
    log(f"  today: {len(cal['today'])} high-impact, tomorrow: {len(cal['tomorrow'])}")
    return cal


# ----------------------------------------------------- catalyst matching

def name_tokens(company_name):
    """Distinctive tokens (4+ letters, not in NAME_STOP) from a company name.
    Generic words like Applied or Digital never match a company alone."""
    tokens = re.findall(r"[A-Za-z]{4,}", company_name or "")
    return [t for t in tokens if t.lower() not in NAME_STOP]


def headline_matches(ticker, company_name, title):
    if re.search(rf"\b{re.escape(ticker)}\b", title):
        return True
    for tok in name_tokens(company_name):
        if re.search(rf"\b{re.escape(tok)}\b", title, re.IGNORECASE):
            return True
    return False


def rank_headlines(headlines):
    def key(h):
        pub = (h.get("source") or "").lower()
        primary = any(p in pub for p in PRIMARY_PUBLISHERS)
        return (0 if primary else 1, h.get("published", ""))
    return sorted(headlines, key=key)


def get_catalysts(ticker, company_name, market_news):
    headlines = []
    def pull_yf():
        out = []
        for n in (yf.Ticker(ticker).news or [])[:10]:
            content = n.get("content", n)
            title = strip_html(content.get("title", ""))
            if not title or SPAM_RE.search(title):
                continue
            prov = content.get("provider") or {}
            out.append({
                "source": prov.get("displayName", "Yahoo Finance"),
                "title": title,
                "link": (content.get("canonicalUrl") or {}).get("url", n.get("link", "")),
                "published": content.get("pubDate", n.get("published", "")),
            })
        return out
    headlines.extend(safe(pull_yf, fallback=[], label=f"news {ticker}") or [])

    for item in market_news:
        if headline_matches(ticker, company_name, item["title"]):
            headlines.append(item)

    seen, unique = set(), []
    for h in rank_headlines(headlines):
        k = h["title"].lower()
        if k not in seen:
            seen.add(k)
            unique.append(h)
    return unique[:5]


# ------------------------------------------------------- gapper enrichment

def enrich_gapper(g, market_news):
    t = yf.Ticker(g["ticker"])
    now_et = datetime.now(ET)

    # Intraday levels from 5-min bars including premarket.
    def intraday():
        bars = t.history(period="1d", interval="5m", prepost=True)
        if bars.empty:
            return {}
        bars = bars[bars.index.tz_convert(ET).date == now_et.date()] if hasattr(bars.index, "tz_convert") else bars
        if bars.empty:
            return {}
        idx_et = bars.index.tz_convert(ET)
        typ = (bars["High"] + bars["Low"] + bars["Close"]) / 3
        vol = bars["Volume"]
        vwap = float((typ * vol).sum() / vol.sum()) if vol.sum() > 0 else None
        pm = bars[idx_et.time < datetime.strptime("09:30", "%H:%M").time()]
        return {
            "vwap": round(vwap, 2) if vwap else None,
            "hod": round(float(bars["High"].max()), 2),
            "lod": round(float(bars["Low"].min()), 2),
            "premarket_high": round(float(pm["High"].max()), 2) if not pm.empty else None,
            "premarket_volume": int(pm["Volume"].sum()) if not pm.empty else 0,
        }
    g["intraday"] = safe(intraday, fallback={}, label=f"intraday {g['ticker']}") or {}

    # Daily metrics from 1y of dailies, excluding today's partial bar.
    def daily():
        hist = t.history(period="1y", interval="1d")
        if hist.empty:
            return {}
        idx_dates = hist.index.tz_convert(ET).date if hist.index.tz is not None else hist.index.date
        prior = hist[[d < now_et.date() for d in idx_dates]]
        todays = hist[[d == now_et.date() for d in idx_dates]]
        if prior.empty:
            return {}
        closes = prior["Close"].dropna()
        out = {
            "sma_200": round(float(closes.tail(200).mean()), 2),
            "prior_day_high": round(float(prior["High"].iloc[-1]), 2),
            "prior_close": round(float(closes.iloc[-1]), 2),
            "avg_volume_20d": int(prior["Volume"].tail(20).mean()),
            "today_open": round(float(todays["Open"].iloc[0]), 2) if not todays.empty else None,
            "today_volume": int(todays["Volume"].sum()) if not todays.empty else 0,
        }
        return out
    g["daily"] = safe(daily, fallback={}, label=f"daily {g['ticker']}") or {}

    # RVOL: yfinance reports about 0 premarket volume, so a true premarket
    # RVOL needs a premarket feed (e.g. Alpaca). Full-day relative volume
    # is the keyless stand-in.
    d = g["daily"]
    if d.get("today_volume") and d.get("avg_volume_20d"):
        g["rvol"] = round(d["today_volume"] / d["avg_volume_20d"], 2)
    else:
        g["rvol"] = None

    def earnings():
        cal = t.calendar
        dates = cal.get("Earnings Date") if isinstance(cal, dict) else None
        return str(dates[0]) if dates else None
    g["next_earnings"] = safe(earnings, label=f"earnings {g['ticker']}")

    g["catalyst_headlines"] = get_catalysts(g["ticker"], g.get("name", ""), market_news)
    g["catalyst_found"] = len(g["catalyst_headlines"]) > 0

    # Deterministic eligibility flags. These encode the validated rules in
    # WATCHLIST_CRITERIA.md, computed in code, NOT by an AI.
    gap = g.get("gap_pct") or 0
    price = g.get("price") or 0
    mcap = g.get("market_cap") or 0
    rvol = g.get("rvol") or 0
    prior_high = d.get("prior_day_high")
    open_ = d.get("today_open")
    sma200 = d.get("sma_200")

    g["day_eligible"] = bool(
        gap > 3 and price > 3 and mcap > 1_000_000_000 and rvol > 1.5
        and prior_high is not None and price > prior_high
    )
    g["swing_eligible"] = bool(
        gap >= 8 and price > 3
        and open_ is not None and prior_high is not None and open_ > prior_high
        and sma200 is not None and open_ > sma200
        and mcap >= 800_000_000
        and g["catalyst_found"]
    )
    return g


# --------------------------------------------------------------------- main

def main():
    started = datetime.now(ET)
    log(f"scan starting {started.strftime('%Y-%m-%d %H:%M:%S %Z')}")

    snapshot = get_market_snapshot()
    market_news = get_market_news()
    econ = get_econ_calendar()

    candidates, source = get_candidates()
    gappers = filter_gappers(candidates)
    log(f"enriching {len(gappers)} gappers...")
    for g in gappers:
        log(f"  {g['ticker']} (gap {g['gap_pct']:+.1f}%)")
        enrich_gapper(g, market_news)

    wd = started.weekday()
    trading_day_note = (
        "weekend run, quotes are last session's" if wd >= 5
        else "weekday run, data as of scan time"
    )

    packet = {
        "generated_at": started.isoformat(),
        "candidate_source": source,
        "trading_day_note": trading_day_note,
        "scan_params": {
            "min_abs_gap_pct": MIN_ABS_GAP,
            "min_price": MIN_PRICE,
            "max_gappers": MAX_GAPPERS,
        },
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
        "market_snapshot": snapshot,
        "econ_calendar": econ,
        "gappers": gappers,
        "market_news": market_news[:20],
        "gaps_to_fill": [
            "market-wide earnings calendar only partial (per-gapper next_earnings only)",
            "intraday levels need intraday bars; empty on non-trading days",
            "RVOL is full-day relative volume; true premarket RVOL needs a premarket feed like Alpaca",
        ],
    }

    # Explicit UTF-8 everywhere: Windows defaults to cp1252 and chokes on
    # emoji and curly quotes in headlines.
    with open("packet.json", "w", encoding="utf-8") as f:
        json.dump(packet, f, indent=2, default=str)
    log(f"WROTE packet.json ({len(gappers)} gappers, "
        f"{len(econ.get('today', []))} econ events today, {len(market_news)} news items)")


if __name__ == "__main__":
    main()
