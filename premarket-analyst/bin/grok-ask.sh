#!/usr/bin/env bash
# grok-ask.sh: send a prompt to the second brain and print ONLY the answer.
# Usage: grok-ask.sh "prompt"   or   ... | grok-ask.sh
#
# The second brain is any OpenAI-compatible chat API, configured in .env:
#   SECOND_BRAIN_URL   (default https://api.x.ai/v1/chat/completions)
#   SECOND_BRAIN_MODEL (default grok-4)
#   SECOND_BRAIN_KEY   (falls back to XAI_API_KEY)
# Works with xAI Grok, Google Gemini, Kimi/Moonshot, DeepSeek, OpenRouter,
# Groq, Mistral. See .env.example for ready-made configs.
set -uo pipefail

if [ $# -ge 1 ]; then
  PROMPT="$1"
else
  PROMPT="$(cat)"
fi

env_val() {
  local name="$1"
  local v="${!name:-}"
  if [ -z "$v" ] && [ -f .env ]; then
    # Tolerate stray whitespace and spaces around the equals sign
    v="$(grep -E "^[[:space:]]*${name}[[:space:]]*=" .env | head -1 | sed -E 's/^[^=]*=[[:space:]]*//' | tr -d '"' | tr -d "'" | tr -d '\r')"
  fi
  echo "$v"
}

API_KEY="$(env_val SECOND_BRAIN_KEY)"
[ -z "$API_KEY" ] && API_KEY="$(env_val XAI_API_KEY)"
URL="$(env_val SECOND_BRAIN_URL)"
[ -z "$URL" ] && URL="https://api.x.ai/v1/chat/completions"
MODEL="$(env_val SECOND_BRAIN_MODEL)"
[ -z "$MODEL" ] && MODEL="grok-4"

if [ -z "$API_KEY" ]; then
  echo "grok-ask: no API key. Set SECOND_BRAIN_KEY (or XAI_API_KEY) in .env" >&2
  exit 1
fi

LOG="$(mktemp)"
RESP="$(mktemp)"

curl -sS --max-time 300 "$URL" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d "$(MODEL="$MODEL" python3 -c '
import json, os, sys
prompt = sys.stdin.read()
print(json.dumps({
    "model": os.environ["MODEL"],
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
  echo "grok-ask: no answer from ${MODEL}, raw response and log follow" >&2
  cat "$RESP" >&2
  cat "$LOG" >&2
  exit 1
fi
