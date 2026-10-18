# -*- coding: utf-8 -*-
"""CSV для импорта в Google Ads Editor (UTF-16, табуляция — родной формат Editor)."""
import ads
from ads import G, CITIES, SITE, COMMON_H, COMMON_D, NEG_PHRASE, NEG_EXACT_BASE, SITELINKS, CALLOUTS, SNIPPET, chk, ERR
from pathlib import Path

COLS = ["Campaign", "Campaign Type", "Networks", "Budget", "Budget type", "Bid Strategy Type", "Campaign Status",
        "Ad Group", "Ad Group Status", "Keyword", "Criterion Type", "Status", "Ad type", "Final URL"] + \
       [f"Headline {i}" for i in range(1, 16)] + [f"Description {i}" for i in range(1, 5)] + \
       ["Path 1", "Path 2", "Link Text", "Description Line 1", "Description Line 2", "Callout text", "Header", "Snippet Values",
        "Phone Number", "Country of Phone"]
BUDGET = "10"

rows = []
def row(**kw):
    r = {c: "" for c in COLS}
    for k, v in kw.items():
        k = k.replace("_", " ")
        assert k in r, k
        r[k] = v
    rows.append(r)

for slug, c in CITIES.items():
    camp = f"DezClub — {c['nom']} — Поиск"
    row(Campaign=camp, **{"Campaign Type": "Search", "Networks": "Google search", "Budget": BUDGET, "Budget type": "Daily",
                          "Bid Strategy Type": "Maximize clicks", "Campaign Status": "Paused"})
    for n in NEG_PHRASE + c["neg"]:
        row(Campaign=camp, Keyword=n, **{"Criterion Type": "Negative Phrase"})
    for n in NEG_EXACT_BASE:
        row(Campaign=camp, Keyword=n.format(c=c["kw"]), **{"Criterion Type": "Negative Exact"})
    for t, d1, d2, u in SITELINKS:
        row(Campaign=camp, **{"Link Text": chk(t, 25, "sl"), "Description Line 1": chk(d1, 35, "d1"), "Description Line 2": chk(d2, 35, "d2"),
                              "Final URL": f"{SITE}{u}{c['q']}"})
    for x in CALLOUTS:
        row(Campaign=camp, **{"Callout text": chk(x, 25, "co")})
    row(Campaign=camp, Header="Services", **{"Snippet Values": ";".join(chk(x, 25, "sn") for x in SNIPPET)})
    row(Campaign=camp, **{"Phone Number": "+77005250108", "Country of Phone": "KZ"})
    for name, url, kws, kws_nc, hs, ds, p1, p2 in G:
        ag = f"{name}"
        row(Campaign=camp, **{"Ad Group": ag, "Ad Group Status": "Enabled"})
        seen = set()
        for k in kws:
            k = k.format(c=c["kw"])
            for t in ("Phrase", "Exact"):
                if (k, t) in seen: continue
                seen.add((k, t)); row(Campaign=camp, Keyword=k, Status="Enabled", **{"Ad Group": ag, "Criterion Type": t})
        for k in kws_nc:
            if (k, "Exact") in seen: continue
            seen.add((k, "Exact")); row(Campaign=camp, Keyword=k, Status="Enabled", **{"Ad Group": ag, "Criterion Type": "Exact"})
        heads = [h.format(**{"in": c["inn"]}) for h in hs] + COMMON_H
        descs = [d.format(**{"in": c["inn"]}) for d in ds] + COMMON_D
        assert len(heads) == 15 and len(set(heads)) == 15 and len(descs) == 4, name
        ad = {"Ad Group": ag, "Ad type": "Responsive search ad", "Status": "Enabled", "Final URL": f"{SITE}{url}{c['q']}",
              "Path 1": chk(p1, 15, "p1"), "Path 2": chk(c["kw"] if p2 == "{p2}" else p2, 15, "p2")}
        for i, h in enumerate(heads, 1): ad[f"Headline {i}"] = chk(h, 30, "h")
        for i, d in enumerate(descs, 1): ad[f"Description {i}"] = chk(d, 90, "d")
        row(Campaign=camp, **ad)

# проверки
for r in rows:
    for v in r.values():
        assert "\t" not in v and "\n" not in v and '"' not in v, v
if ERR:
    print("\n".join(ERR)); raise SystemExit(1)
out = Path(__file__).resolve().parent.parent / "dezclub-google-ads-editor.csv"
lines = ["\t".join(COLS)] + ["\t".join(r[c] for c in COLS) for r in rows]
out.write_bytes(("\r\n".join(lines) + "\r\n").encode("utf-16"))
print("ok rows", len(rows), out)
import collections
print(collections.Counter(r["Criterion Type"] or ("AD" if r["Ad type"] else "other") for r in rows))
