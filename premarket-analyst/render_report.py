#!/usr/bin/env python3
"""render_report.py: turn the Markdown report into a clean HTML page.

Usage: python render_report.py REPORT.md [YYYY-MM-DD]
Writes reports/premarket_<date>.html
"""

import os
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

import markdown

CSS = """
:root { color-scheme: light; }
* { box-sizing: border-box; }
body {
  margin: 0;
  background: #f4f5f7;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    Helvetica, Arial, sans-serif;
  color: #1f2430;
  line-height: 1.6;
}
.page {
  max-width: 900px;
  margin: 0 auto;
  padding: 32px 24px 64px;
}
header.report-header {
  border-bottom: 2px solid #d9dce3;
  padding-bottom: 16px;
  margin-bottom: 28px;
}
header.report-header h1 { margin: 0 0 4px; font-size: 1.6rem; }
header.report-header .date { color: #5a6072; font-size: 0.95rem; }
article h1 { font-size: 1.45rem; margin-top: 1.6em; }
article h2 {
  font-size: 1.15rem;
  margin-top: 1.8em;
  padding-bottom: 6px;
  border-bottom: 1px solid #e3e5ea;
}
article h3 { font-size: 1.0rem; color: #3a4152; }
article blockquote {
  margin: 1em 0;
  padding: 10px 16px;
  background: #fdf6e3;
  border-left: 4px solid #d4a72c;
  color: #4a4a3a;
  font-size: 0.92rem;
}
article table {
  border-collapse: collapse;
  width: 100%;
  margin: 1em 0;
  font-size: 0.9rem;
  background: #ffffff;
}
article th {
  background: #eceef2;
  text-align: left;
  padding: 8px 10px;
  border: 1px solid #d9dce3;
}
article td { padding: 8px 10px; border: 1px solid #e3e5ea; vertical-align: top; }
article tr:nth-child(even) td { background: #f9fafb; }
article code {
  background: #eceef2;
  padding: 1px 5px;
  border-radius: 4px;
  font-size: 0.88em;
}
article pre { background: #eceef2; padding: 12px; overflow-x: auto; border-radius: 6px; }
article hr { border: none; border-top: 1px solid #d9dce3; margin: 2em 0; }
footer.report-footer {
  margin-top: 40px;
  padding-top: 16px;
  border-top: 1px solid #d9dce3;
  color: #7a8093;
  font-size: 0.85rem;
}
@media (max-width: 640px) {
  .page { padding: 20px 12px 48px; }
  article table { display: block; overflow-x: auto; }
}
"""


def main():
    if len(sys.argv) < 2:
        print("usage: python render_report.py REPORT.md [YYYY-MM-DD]")
        sys.exit(1)
    md_path = sys.argv[1]
    date = sys.argv[2] if len(sys.argv) > 2 else str(datetime.now(ZoneInfo("America/New_York")).date())

    with open(md_path, encoding="utf-8") as f:
        body = markdown.markdown(f.read(), extensions=["tables", "fenced_code", "sane_lists"])

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI Premarket Report · {date}</title>
<style>{CSS}</style>
</head>
<body>
<div class="page">
  <header class="report-header">
    <h1>AI Premarket Report</h1>
    <div class="date">{date}</div>
  </header>
  <article>
{body}
  </article>
  <footer class="report-footer">
    Generated {date} · Built by Claude + Grok · Educational only, not financial advice
  </footer>
</div>
</body>
</html>
"""

    os.makedirs("reports", exist_ok=True)
    out = os.path.join("reports", f"premarket_{date}.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[render] wrote {out}")
    return out


if __name__ == "__main__":
    main()
