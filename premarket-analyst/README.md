# AI Premarket Analyst

A free, keyless premarket pipeline. Deterministic rules pick the watchlist, two rival AI brains (Claude as analyst, Grok as independent second opinion) judge quality, and the merged report lands in your inbox before the open.

```
REPORT_TEMPLATE.md  (the shape)
        |
scan.py -> packet.json -> Claude -.
                        -> Grok  -+-> merge -> REPORT.md -> HTML -> email
```

## Files

| File | Job |
|------|-----|
| `REPORT_TEMPLATE.md` | The 12 section report skeleton every morning fills |
| `WATCHLIST_CRITERIA.md` | The two validated setups (Trend Join Long day setup, gap-up swing setup) with backtest stats |
| `scan.py` | Data gatherer only. Snapshot, movers, gap filter, RSS news, econ calendar, per gapper enrichment, deterministic `day_eligible` / `swing_eligible` flags. Zero analysis. Writes `packet.json` |
| `demo_packet.py` | Writes a sample `packet.json` (same schema) for demos or sandboxes with no market data access |
| `prompt_claude.md` | The analyst prompt (first brain) |
| `prompt_grok.md` | The blind second brain prompt for Grok |
| `bin/grok-ask.sh` | Shell wrapper that pipes a prompt to the xAI Grok API and prints only the answer (needs `XAI_API_KEY`) |
| `prompt_merge.md` | The editor prompt. Never averages the two brains |
| `render_report.py` | `REPORT.md` to clean HTML in `reports/` |
| `deliver.py` | Emails the HTML via Resend. Skips cleanly if keys are missing |

## Run it

```bash
python3 -m venv .venv && .venv/bin/pip install yfinance feedparser markdown requests
.venv/bin/python scan.py                      # gathers live data into packet.json
# run prompt_claude.md and prompt_grok.md against packet.json -> claude_view.md, grok_view.md
#   Grok: { cat prompt_grok.md; echo; echo "=== INPUT: packet.json ==="; cat packet.json; } | bin/grok-ask.sh > grok_view.md
# run prompt_merge.md against all three -> REPORT.md
.venv/bin/python render_report.py REPORT.md $(date +%F)
.venv/bin/python deliver.py reports/premarket_$(date +%F).html $(date +%F)
```

Copy `.env.example` to `.env` and add `RESEND_API_KEY`, `EMAIL_TO`, and optionally `XAI_API_KEY`.

## Honest limitations

- yfinance reports almost no premarket volume, so RVOL is a full day stand in until a real premarket feed (like Alpaca) is wired in. The packet and the report both say so.
- The repo's committed `packet.json`, view files, and `REPORT.md` were produced from `demo_packet.py` fixture data because the build sandbox blocks market data hosts. Run `scan.py` on a machine with open internet for the real thing.
- Decision support, not signals. The rules pick, the brains rank, you trade. Not financial advice.
