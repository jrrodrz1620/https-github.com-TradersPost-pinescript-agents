#!/usr/bin/env bash
# run_morning.sh: the whole pipeline, one command. Built for an always-on
# Linux box (DigitalOcean droplet) running from cron before the open.
#
# Needs: .venv set up, .env filled in, claude CLI logged in (brain 1),
# XAI_API_KEY in .env for Grok (brain 2, optional but recommended).
set -uo pipefail
cd "$(dirname "$0")"

D=$(TZ=America/New_York date +%F)
log() { echo "[$(TZ=America/New_York date +%H:%M:%S)] $*"; }

log "1/6 scan"
.venv/bin/python scan.py || { log "scan failed, aborting"; exit 1; }

log "2/6 brain 1: Claude analyst pass"
if command -v claude >/dev/null 2>&1; then
  claude -p "Follow prompt_claude.md against packet.json and write the result to claude_view.md. Use only packet data." \
    --permission-mode acceptEdits || log "warn: claude pass failed"
else
  log "warn: claude CLI not found, skipping brain 1"
fi

log "3/6 brain 2: Grok blind pass"
if { cat prompt_grok.md; echo; echo "=== INPUT: packet.json ==="; cat packet.json; } | bin/grok-ask.sh > grok_view.md.tmp; then
  mv grok_view.md.tmp grok_view.md
else
  rm -f grok_view.md.tmp
  log "warn: Grok unreachable, continuing single-brain (merge will say so)"
fi

log "4/6 merge"
if command -v claude >/dev/null 2>&1; then
  claude -p "Follow prompt_merge.md using packet.json, claude_view.md, and grok_view.md (if grok_view.md is missing or stale, note the report is single-brain today). Stamp today's date and current ET time. Write REPORT.md." \
    --permission-mode acceptEdits || { log "merge failed, aborting"; exit 1; }
else
  log "claude CLI not found, cannot merge, aborting"; exit 1
fi

log "5/6 render"
.venv/bin/python render_report.py REPORT.md "$D" || exit 1

log "6/6 deliver"
.venv/bin/python deliver.py "reports/premarket_${D}.html" "$D"

log "done"
