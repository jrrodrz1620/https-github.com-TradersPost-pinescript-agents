# Phantom Flow SMC (Open) — Indicator + Strategy + Walk-Forward

An open-source re-implementation of the core ideas behind the commercial
**Phantom Flow** TradingView indicator, plus a strategy version wired to feed
the [`nq-walkforward`](https://github.com/jrrodrz1620/nq-walkforward) analyzer
for out-of-sample validation.

> This is an independent, from-scratch implementation of well-known Smart Money
> Concepts (market structure, order blocks, FVGs, liquidity). It does not
> contain or copy any proprietary Phantom Flow code.

## Files

| File | Type | Purpose |
|------|------|---------|
| `phantom-flow-smc.pine` | `indicator` | Visual overlay: BOS/CHoCH, order blocks, FVGs, liquidity sweeps, premium/discount, bias dashboard. |
| `phantom-flow-smc-strategy.pine` | `strategy` | Tradable rules on the same structure; produces a TradingView trade list for backtesting. |

## What it reproduces

- **Market structure** — confirmed swing pivots drive BOS (Break of Structure)
  and CHoCH (Change of Character) labels.
- **Order blocks** — last opposing candle before a structure break, drawn as a zone.
- **Fair Value Gaps** — 3-candle imbalances with an ATR size filter and optional
  mitigation (removed once price fills the gap).
- **Liquidity** — equal highs/lows (EQH/EQL) and wick sweeps of the active level.
- **Premium / Discount** — equilibrium of the active swing range; longs favored in
  discount, shorts in premium.

### Repainting

All structure is built from `ta.pivothigh` / `ta.pivotlow`, which finalize
`swingLength` bars after the pivot and never repaint once printed. Breaks and
entries are evaluated on **bar close**. Pivot markers are plotted at the pivot's
historical location (standard, non-repainting offset).

## Strategy → Walk-Forward workflow

The strategy is the bridge to the `nq-walkforward` Streamlit app, which expects a
TradingView **"List of Trades"** export.

1. **Add the strategy** `phantom-flow-smc-strategy.pine` to a TradingView chart
   (e.g. NQ/MNQ, 1–15m).
2. **Set the contract multiplier** to match your instrument when you analyze:
   NQ = 20, MNQ = 2, ES = 50, MES = 5.
3. Open **Strategy Tester → List of Trades → Export** (XLSX or CSV).
   The export's columns (`Trade #`, `Type`, `Signal`, `Date/Time`, `Price`,
   `Profit`, …) map directly onto the analyzer's `TRADINGVIEW_COL_MAP`.
4. **Upload** the file in the `nq-walkforward` app (`streamlit run app.py`).
5. Review the **out-of-sample** results: per-fold metrics, OOS equity curve, and
   the **Overfit Check** (OOS/Train profit-factor ratio).

### Reading the overfit check

The analyzer splits trades into walk-forward folds (default 5 folds, 70% train).
The headline number is the **OOS / Train profit-factor ratio**:

- `≥ 0.80` → robust
- `0.50 – 0.80` → some degradation
- `< 0.50` → likely overfit

Tune the strategy on the *train* behavior, then judge it only by the *OOS* columns.

## Suggested tuning order

1. `swingLength` — sets how significant a swing must be (fewer, cleaner breaks at
   higher values).
2. `Reward : Risk` and `Stop Type` (Structure vs ATR) — the biggest levers on the
   trade distribution.
3. Entry filters — `Require Discount/Premium Location` and `Require Fresh FVG`
   tighten entry quality at the cost of frequency.
4. Re-export and re-run the walk-forward analyzer after each change; keep changes
   that hold up **out-of-sample**, not just in-sample.

## Note on results

Pine Script executes inside TradingView, so actual backtest numbers must be
generated there — they are not produced in this repo. The strategy is written so
its export is plug-and-play with the walk-forward analyzer; the numbers are
yours to generate per instrument, timeframe, and date range.
