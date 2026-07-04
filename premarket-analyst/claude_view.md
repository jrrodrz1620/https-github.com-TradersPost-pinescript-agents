# Claude View: Premarket Analysis

*Analyst pass on packet.json (demo fixture data). Rules pick membership, I judge quality.*

## Summary

Tape is quietly risk-on: Nasdaq futures leading at +0.67%, VIX asleep at 13.85, yields drifting lower into the 8:30 jobs print. The catch is exactly that print: NFP at 8:30 ET can flip this whole board before the open, so every plan below is written in pencil until the number hits. Best idea on the desk is SMCI, a clean guidance-raise gapper that passes both rule sets.

## Pre-Market Gappers

- **SMCI +12.5% ($52.80)**: "Super Micro raises full-year revenue outlook on record AI server orders" (Reuters). Also CNBC: "SMCI jumps double digits premarket after guidance hike." Real catalyst, the good kind.
- **CELH +10.1% ($34.90)**: "Celsius surges after PepsiCo expands distribution deal to Europe" (MarketWatch). Real news, but the chart has baggage, see below.
- **PLTR +6.3% ($148.60)**: "Palantir wins $1.2 billion Army software contract expansion" (Bloomberg). Institutional-grade catalyst.
- **AVXL +32.6% ($9.84)**: no catalyst found. Biggest gap on the board and nobody knows why. That is not a mystery to solve, that is a skip.
- **RIVN -7.1% ($11.20)**: "Rivian cuts 2026 delivery guidance, cites component shortages" (Reuters). Down on bad news, at least it is honest.

## Day Trading Watchlist

Flag rule: `day_eligible` = gap > 3%, price > $3, market cap > $1B, RVOL > 1.5, price above yesterday's high (backtest 54.6% win rate, PF 1.59, 280 trades).

| Ticker | Catalyst | Levels | Plan | Conviction |
|--------|----------|--------|------|------------|
| SMCI | Guidance raise on AI server orders | PMH 52.15, HOD 53.40, LOD 49.10, VWAP 51.90. Price 52.80, above VWAP and PMH, just under HOD | Trigger: break of 53.40 (prior HOD, already through PMH) in the 10:00 to 3:30 window. Stop 1% below PMH = 51.63 (LOD lower but PMH stop is tighter reference, take the lower: 48.61 off LOD is too wide, use 51.63). Scale 1/3 at +1R, 1/3 at +2R, trail rest on 21 EMA. Flat 3:51 | 🟢 |
| PLTR | $1.2B Army contract expansion | PMH 147.80, HOD 149.90, LOD 144.30, VWAP 147.20. Price 148.60, above VWAP and PMH | Trigger: break of 149.90 in window. Stop 1% below PMH = 146.32. Same scaling, flat 3:51 | 🟡 |

PLTR gets yellow not green: RVOL 1.62 barely clears the bar, and a 6% gap on a 335B name has less room to run than the backtest's typical candidate.

## Swing Watchlist

Flag rule: `swing_eligible` = gap >= 8%, price > $3, open > yesterday's high, open > 200-day SMA, market cap >= $800M, real catalyst (backtest 57.6% WR / PF 5.34 news, 44.7% / PF 2.57 earnings).

| Ticker | Catalyst | Theme | Trend | Conviction |
|--------|----------|-------|-------|------------|
| SMCI | Guidance raise, record AI server orders (news catalyst, the strong bucket) | AI infrastructure | Open 50.10 well above prior high 47.30 and miles above the 200d at 41.20. Uptrend confirmed | 🟢 |

Starter idea only: swing management is still being built, so no fake stops or targets. The stat that matters: news catalysts backtest at PF 5.34, and this is a news catalyst.

## Market Trends

- Growth over value: Nasdaq +0.67% vs Russell -0.56%. Small caps are getting left at the station.
- Vol is cheap: VIX 13.85 and falling. Complacent or correct, we find out at 8:30.
- Oil -2% on OPEC+ supply talk, a quiet tailwind for the soft-landing crowd.
- Dollar and yields both easing, the market is leaning toward rate cuts.

## Technical Signals

- SMCI trading above VWAP, above PMH, 1.1% under HOD. Strongest tape on the board.
- PLTR above VWAP and PMH, 0.9% under HOD. Constructive but extended off the 200d (148 vs 112).
- CELH above its VWAP but still 10% below its 200-day line at 38.75. Rallies into overhead supply until that reclaims.
- RIVN below VWAP, below prior day high, downtrend intact.

## Economic Data, Rates and the Fed

- 8:30 ET: Non-Farm Employment Change, forecast 185K vs previous 212K.
- 8:30 ET: Unemployment Rate, forecast 4.1% vs previous 4.0%.
- 10:00 ET: ISM Services PMI, forecast 52.4 vs previous 53.1.
- Rates: 10Y at 4.18% and drifting down, 3M at 4.32%. Curve still inverted but the long end is behaving.

This is not a light data day. Jobs Friday. Do not size up before 8:30.

## Coming Up

- Tomorrow 14:00 ET: FOMC Member Speech (Waller).
- Earnings on deck from the watchlist: SMCI 8/4, CELH 8/6, RIVN 8/7, PLTR 8/10.

## Skips and Traps

- **AVXL 🔴**: +32.6% with catalyst_found false. No news, no trade. RVOL 5.64 means somebody is playing it, but without a catalyst you are the exit liquidity.
- **CELH 🔴 (for the rules)**: real Pepsi catalyst but RVOL 1.35 fails the day screen and the open below the 200-day SMA fails the swing screen. Watch, do not chase.
- **RIVN 🔴**: down 7% on a guidance cut. If it goes green intraday, that is a bad-news-green-candle trap, not a reversal story.
