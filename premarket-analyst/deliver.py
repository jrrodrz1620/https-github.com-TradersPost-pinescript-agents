#!/usr/bin/env python3
"""deliver.py: email the HTML report via Resend.

Usage: python deliver.py reports/premarket_<date>.html <date>

Reads RESEND_API_KEY and EMAIL_TO from a local .env file (tiny KEY=VALUE
parser, no extra dependency). Real environment variables win over the file.
If the keys are missing it prints a skip line and exits cleanly, so an
unattended morning run never crashes on config.
"""

import os
import sys

import requests

RESEND_URL = "https://api.resend.com/emails"
DEFAULT_FROM = "AI Premarket Analyst <onboarding@resend.dev>"


def load_env(path=".env"):
    """Tiny KEY=VALUE parser. Environment variables take precedence."""
    values = {}
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, val = line.partition("=")
                values[key.strip()] = val.strip().strip('"').strip("'")
    values.update({k: v for k, v in os.environ.items() if k in
                   ("RESEND_API_KEY", "EMAIL_TO", "EMAIL_FROM")})
    return values


def main():
    if len(sys.argv) < 3:
        print("usage: python deliver.py reports/premarket_<date>.html <date>")
        sys.exit(1)
    html_path, date = sys.argv[1], sys.argv[2]

    env = load_env()
    api_key = env.get("RESEND_API_KEY")
    to_addr = env.get("EMAIL_TO")
    from_addr = env.get("EMAIL_FROM", DEFAULT_FROM)

    if not api_key or not to_addr:
        print("[deliver] email skipped, set RESEND_API_KEY + EMAIL_TO (in .env or the environment)")
        sys.exit(0)

    with open(html_path) as f:
        html = f.read()

    resp = requests.post(
        RESEND_URL,
        headers={"Authorization": f"Bearer {api_key}",
                 "Content-Type": "application/json"},
        json={
            "from": from_addr,
            "to": [to_addr],
            "subject": f"AI Premarket Report · {date}",
            "html": html,
        },
        timeout=30,
    )
    if resp.status_code in (200, 201):
        print(f"[deliver] email sent to {to_addr} (id {resp.json().get('id', '?')})")
    else:
        print(f"[deliver] Resend returned {resp.status_code}: {resp.text}")
        sys.exit(1)


if __name__ == "__main__":
    main()
