# -*- coding: utf-8 -*-
"""Однократная генерация SVG-иконок в assets/ic (Fluent Emoji, MIT + собственные иллюстрации)."""
import json, re, sys
from pathlib import Path
from pest_art import CUSTOM, wrap
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "ic"; OUT.mkdir(parents=True, exist_ok=True)
F = json.load(open(sys.argv[1]))
MAP = {"s_insect": "cockroach", "s_virus": "microbe", "s_rat": "rat", "s_fumig": "dashing-away", "s_odor": "leaf-fluttering-in-wind",
       "s_weed": "herb", "s_biz": "office-building", "s_pest": "magnifying-glass-tilted-left",
       "cockroach": "cockroach", "beetle": "beetle", "fly": "fly", "ant": "ant", "rat": "rat", "mouse": "mouse",
       "doc": "clipboard", "shield": "shield", "time": "alarm-clock", "check": "check-mark-button", "card": "credit-card", "map": "world-map",
       "house": "house-with-garden", "people": "handshake"}
def fluent(n, prefix):
    ic = F["icons"][n]; body = ic["body"]
    ids = set(re.findall(r'id="([^"]+)"', body))
    for i in ids: body = body.replace(f'id="{i}"', f'id="{prefix}{i}"').replace(f"url(#{i})", f"url(#{prefix}{i})")
    return body
for k, n in MAP.items():
    (OUT / f"{k}.svg").write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">{fluent(n, k[:3])}</svg>', encoding="utf-8")
for k, v in CUSTOM.items():
    (OUT / f"{k}.svg").write_text(v, encoding="utf-8")
(OUT / "s_tick.svg").write_text(CUSTOM["tick"], encoding="utf-8")
# озонирование: облако + O3
cloud = fluent("cloud", "oz")
(OUT / "s_ozone.svg").write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">{cloud}<text x="16" y="21.5" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-weight="700" font-size="9" fill="#2B7FC4">O<tspan font-size="5.5" dy="1.6">3</tspan></text></svg>', encoding="utf-8")
print(sorted(p.name for p in OUT.iterdir()))
