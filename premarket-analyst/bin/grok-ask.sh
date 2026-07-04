#!/usr/bin/env bash
# grok-ask.sh: send a prompt to xAI's Grok API and print ONLY the answer.
# Usage: grok-ask.sh "prompt"   or   ... | grok-ask.sh
# Needs XAI_API_KEY in the environment or in a local .env file.
set -uo pipefail

if [ $# -ge 1 ]; then
  PROMPT="$1"
else
  PROMPT="$(cat)"
fi

if [ -z "${XAI_API_KEY:-}" ] && [ -f .env ]; then
  XAI_API_KEY="$(grep -E '^XAI_API_KEY=' .env | head -1 | cut -d= -f2-)"
fi
if [ -z "${XAI_API_KEY:-}" ]; then
  echo "grok-ask: XAI_API_KEY not set (env or .env), cannot reach Grok" >&2
  exit 1
fi

LOG="$(mktemp)"
RESP="$(mktemp)"

curl -sS --max-time 300 https://api.x.ai/v1/chat/completions \
  -H "Authorization: Bearer ${XAI_API_KEY}" \
  -H "Content-Type: application/json" \
  -d "$(python3 -c '
import json, sys
prompt = sys.stdin.read()
print(json.dumps({
    "model": "grok-4",
    "messages": [{"role": "user", "content": prompt}],
    "temperature": 0.3,
}))
' <<<"$PROMPT")" >"$RESP" 2>>"$LOG"

ANSWER="$(python3 -c '
import json, sys
try:
    data = json.load(open(sys.argv[1]))
    print(data["choices"][0]["message"]["content"])
except Exception:
    pass
' "$RESP")"

if [ -n "$ANSWER" ]; then
  echo "$ANSWER"
else
  echo "grok-ask: no answer from Grok, raw response and log follow" >&2
  cat "$RESP" >&2
  cat "$LOG" >&2
  exit 1
fi
