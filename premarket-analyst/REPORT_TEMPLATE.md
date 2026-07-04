# Premarket Report Template

This is the blueprint. Every morning report fills this exact skeleton, same shape every time, so it reads in five seconds. The analyst and merge prompts build backward toward this file. Voice is casual Humbled Trader, plain talk, no em dashes anywhere.

## Conviction Key

- 🟢 **HIGH**: both brains agree AND the setup is clean. Rules passed, catalyst real, levels make sense.
- 🟡 **MED**: the brains agree but the name is extended or feels priced in, or one brain is lukewarm.
- 🔴 **LOW / SKIP**: the brains conflict, or a rule failed, or the risk is dumb. Listed so you know why we passed.

Never average the two brains. Where they disagree, that gap is the signal. Stand down or size down.

---

# 🧠 AI PREMARKET REPORT

### {{DATE}} · {{TIME_ET}} ET · Claude + Gemini, independent passes

> **Disclaimer, the one liner:** the deterministic rules pick the watchlist, both AIs judge quality, and you make the trade. Not financial advice.

## Summary

The tape in one line. The catch we are watching today. And a one line two brain verdict: where Claude and Gemini landed together and where they split.

## 📊 Pre-Market Gappers

Every gapper that survived the scan filter, each with its full catalyst headline straight from the packet. No headline, no catalyst, and it says so.

## ☀️ Day Trading Watchlist

Names where `day_eligible` is true (Trend Join Long rules, see WATCHLIST_CRITERIA.md).

| Ticker | Catalyst | Levels (live) | Plan (Trend Join) | 🤖 Gemini | Conv. |
|--------|----------|---------------|-------------------|---------|-------|

## 📈 Notable Swing Watchlist

Names where `swing_eligible` is true. Starter ideas only, swing management is still being built.

| Ticker | Catalyst (headline) | Trend context | Idea | 🤖 Gemini | Conv. |
|--------|--------------------|---------------|------|---------|-------|

## 📉 Market Trends of the Day

Bullets. What the snapshot says: indexes, VIX, oil, dollar, yields, and the one line read on each that matters.

## 📊 Technical Signals for Today

Bullets. Where price sits versus the levels that matter: VWAP, premarket highs, prior day highs, 200 day lines on the watchlist names.

## 💰 Economic Data, Rates & the Fed

From `econ_calendar.today`: each US high impact event with time ET plus forecast versus previous. Rates from the snapshot. Empty calendar means light data day, say so. Feed error means the calendar was unavailable, say that too.

## 📅 Coming Up

Tomorrow's high impact events from `econ_calendar.tomorrow` with times ET, plus notable earnings from the gappers.

## 🚫 Skips & Traps

Names that failed the screens or got flagged by either brain, each with the why. Up on bad news is a trap and gets called out here.

---

## 🤖 Where the two brains landed

- **Agreement:** the overlap, trade these.
- **Rules vs discretion:** names Gemini liked that the screen rejected, and why the screen said no.
- **Sharp catches:** the one thing each brain caught that the other missed.
- Closing line: trade where they agree; where they disagree, stand down or size down; never average.

---

*Generated {{DATE}} · Built by Claude + Gemini · Educational only, not financial advice*
