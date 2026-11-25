#!/usr/bin/env python3
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from urllib.request import Request, urlopen

USERNAME = "SriShankar2006"
OUTPUT = Path("assets/generated/contribution-grid.svg")
TOKEN = os.getenv("GITHUB_TOKEN")

query = """
query($login:String!, $from:DateTime!, $to:DateTime!) {
  user(login:$login) {
    contributionsCollection(from:$from, to:$to) {
      contributionCalendar {
        weeks {
          contributionDays {
            date
            contributionCount
            color
          }
        }
      }
    }
  }
}
"""


def fetch_calendar():
    if not TOKEN:
        raise RuntimeError("GITHUB_TOKEN is required")
    now = datetime.utcnow()
    payload = json.dumps({
        "query": query,
        "variables": {
            "login": USERNAME,
            "from": (now - timedelta(days=365)).isoformat() + "Z",
            "to": now.isoformat() + "Z",
        },
    }).encode()
    req = Request(
        "https://api.github.com/graphql",
        data=payload,
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json",
            "User-Agent": "github-profile-contribution-grid",
        },
    )
    with urlopen(req, timeout=30) as response:
        data = json.loads(response.read())
    if data.get("errors"):
        raise RuntimeError(data["errors"])
    return data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]


def render(weeks):
    left, top, cell, gap = 60, 48, 11, 3
    width = left + len(weeks) * (cell + gap) + 24
    height = 160
    palette = ("#172554", "#7657E8", "#00D4FF", "#42E6B5")
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        '<title id="title">Sri Shankar N GitHub contribution calendar</title>',
        '<desc id="desc">A calendar grid of actual public GitHub contribution data.</desc>',
        '<rect width="100%" height="100%" rx="12" fill="#10172B"/>',
        '<text x="60" y="24" fill="#F8FAFC" font-family="JetBrains Mono, monospace" font-size="13">ACTUAL GITHUB CONTRIBUTIONS</text>',
    ]
    for i in range(7):
        if i in (0, 2, 4, 6):
            parts.append(f'<text x="18" y="{top + i*(cell+gap)+9}" fill="#94A3B8" font-family="JetBrains Mono, monospace" font-size="9">{"MTWTFSS"[i]}</text>')
    for wi, week in enumerate(weeks):
        x = left + wi * (cell + gap)
        for di, day in enumerate(week["contributionDays"]):
            count = day["contributionCount"]
            level = 0 if count == 0 else min(3, 1 + (count - 1) // 4)
            y = top + di * (cell + gap)
            parts.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2" fill="{palette[level]}"><title>{day["date"]}: {count} contributions</title></rect>')
    parts.append('</svg>')
    return "".join(parts)


def main():
    weeks = fetch_calendar()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(render(weeks), encoding="utf-8")
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
