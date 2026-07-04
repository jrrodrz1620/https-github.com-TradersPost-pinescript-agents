# Watchlist Criteria

These are my two validated watchlist setups. They are backtested, they are the source of truth, and the scanner encodes them as pass or fail flags. The code never has an opinion, it just checks boxes. The AI layer judges quality afterward, but a name that fails a hard rule never makes the list.

---

## Setup 1: Day Trading Watchlist, "Trend Join Long"

**Backtest: 54.6% win rate, profit factor 1.59, 280 trades.**

The idea is simple. A real gapper with size behind it breaks yesterday's high, and we join the trend instead of guessing the top.

### Premarket selection rules (ALL required)

| # | Rule | Threshold |
|---|------|-----------|
| 1 | Gap % vs previous close | > 3% |
| 2 | Price | > $3 |
| 3 | Market cap | > $1B |
| 4 | Premarket relative volume (RVOL) | > 1.5 |
| 5 | Price action | Breaking above yesterday's high |

The scanner encodes this as the `day_eligible` flag. All five pass or the name is out.

### Intraday plan

- **Window:** 10:00am to 3:30pm ET. No entries outside it.
- **Trigger:** price > premarket high AND price > prior high of day.
- **Stop:** 1% below the premarket high or the low of day, whichever is lower. That distance is 1R.
- **Scaling:** take 1/3 off at +1R, take 1/3 off at +2R, trail the last 1/3 on the 21 EMA.
- **Hard rule:** flat by 3:51pm. No overnight, no exceptions.

### RVOL honesty note

yfinance reports basically zero premarket volume, so the pipeline's RVOL is a full day relative volume stand in until a real premarket feed (like Alpaca) is wired in. The packet says so, the report says so, and now this file says so too.

---

## Setup 2: Swing Watchlist

**Backtest: 57.6% win rate / profit factor 5.34 on news catalysts. 44.7% win rate / profit factor 2.57 on earnings catalysts.**

Gap ups with a real catalyst, opening above yesterday's high and above the 200 day line. News catalysts have been the stronger group by a wide margin, earnings catalysts are playable but weaker, and the stats above keep that honest.

### Premarket selection rules (ALL required)

| # | Rule | Threshold |
|---|------|-----------|
| 1 | Gap % vs previous close | >= 8% |
| 2 | Price | > $3 |
| 3 | Open | > yesterday's high |
| 4 | Open | > 200 day SMA |
| 5 | Market cap | >= $800M |
| 6 | Catalyst | A real one: earnings on the gap day, or news with no earnings |

The scanner encodes this as the `swing_eligible` flag.

### Management note

Swing entry and exit management is still being built. Swing names in the report are starter ideas only. No fake stops, no fake targets, and the report is not allowed to invent them.

---

## The whole point

Membership is deterministic. These rules decide who makes the watchlist, computed in code from real data. The two AI brains only judge quality: catalyst strength, macro fit, where price sits on the levels. Rules pick, brains rank, I trade. In that order.
