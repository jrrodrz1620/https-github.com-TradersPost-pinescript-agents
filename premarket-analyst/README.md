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
| `bin/grok-ask.sh` | Shell wrapper (macOS/Linux) that pipes a prompt to the xAI Grok API and prints only the answer (needs `XAI_API_KEY`) |
| `bin/grok-ask.ps1` | The same wrapper for Windows PowerShell |
| `prompt_merge.md` | The editor prompt. Never averages the two brains |
| `render_report.py` | `REPORT.md` to clean HTML in `reports/` |
| `deliver.py` | Emails the HTML via Resend. Skips cleanly if keys are missing |

## Run it on Windows (PowerShell)

```powershell
py -m venv .venv
.venv\Scripts\pip install yfinance feedparser markdown requests tzdata
.venv\Scripts\python scan.py                  # gathers live data into packet.json
# run prompt_claude.md and prompt_grok.md against packet.json -> claude_view.md, grok_view.md
#   Grok: Get-Content prompt_grok.md, packet.json -Raw | .\bin\grok-ask.ps1 | Out-File grok_view.md
# run prompt_merge.md against all three -> REPORT.md
$d = Get-Date -Format yyyy-MM-dd
.venv\Scripts\python render_report.py REPORT.md $d
.venv\Scripts\python deliver.py reports\premarket_$d.html $d
```

Note the extra `tzdata` package: Windows does not ship the IANA timezone database, and the scripts pin everything to America/New_York, so `tzdata` is required there (harmless elsewhere).

## Run it on macOS / Linux

```bash
python3 -m venv .venv && .venv/bin/pip install yfinance feedparser markdown requests
.venv/bin/python scan.py                      # gathers live data into packet.json
# run prompt_claude.md and prompt_grok.md against packet.json -> claude_view.md, grok_view.md
#   Grok: { cat prompt_grok.md; echo; echo "=== INPUT: packet.json ==="; cat packet.json; } | bin/grok-ask.sh > grok_view.md
# run prompt_merge.md against all three -> REPORT.md
.venv/bin/python render_report.py REPORT.md $(date +%F)
.venv/bin/python deliver.py reports/premarket_$(date +%F).html $(date +%F)
```

Copy `.env.example` to `.env` and add `RESEND_API_KEY`, `EMAIL_TO`, and optionally `XAI_API_KEY`. On Windows: `Copy-Item .env.example .env`.

## Run it unattended on a cloud box (DigitalOcean droplet)

An always-on Ubuntu droplet turns this into a real morning routine: cron fires before the open, the report is in your inbox when you wake up, and your PC can stay off.

One-time setup on a fresh Ubuntu droplet:

```bash
sudo apt update && sudo apt install -y python3-venv git
git clone <your repo> && cd <repo>/premarket-analyst
python3 -m venv .venv && .venv/bin/pip install yfinance feedparser markdown requests
cp .env.example .env && nano .env          # paste RESEND_API_KEY, EMAIL_TO, XAI_API_KEY
curl -fsSL https://claude.ai/install.sh | bash && claude   # log in once (brain 1)
chmod +x run_morning.sh bin/grok-ask.sh
./run_morning.sh                            # test the full chain once by hand
```

Then schedule it with cron (`crontab -e`):

```cron
CRON_TZ=America/New_York
30 8 * * 1-5 /home/YOU/premarket-analyst/run_morning.sh >> /home/YOU/premarket-analyst/morning.log 2>&1
```

That is 8:30am ET on weekdays, so the report lands with time to spare before 9:30. `run_morning.sh` chains scan -> Claude pass -> Grok pass -> merge -> render -> email, and degrades gracefully: Grok down means a single-brain report that says so, missing email keys means it skips delivery instead of crashing.

Cloud caveat, honestly: Yahoo Finance sometimes throttles datacenter IPs harder than home IPs. Run `./run_morning.sh` by hand once after setup and check the packet has real gappers. If the screeners come back thin the static universe fallback kicks in automatically.

## Honest limitations

- yfinance reports almost no premarket volume, so RVOL is a full day stand in until a real premarket feed (like Alpaca) is wired in. The packet and the report both say so.
- The repo's committed `packet.json`, view files, and `REPORT.md` were produced from `demo_packet.py` fixture data because the build sandbox blocks market data hosts. Run `scan.py` on a machine with open internet for the real thing.
- Decision support, not signals. The rules pick, the brains rank, you trade. Not financial advice.
