"""Koliko je govorio po danu u 15. sazivu, za "Ukupno je pričao" na strani: samo završeni dani.

Iz zapisa mikrofona (mikrofon.zailiprotiv.rs), po istom pravilu kao mikrofon: govor sa bar dva kadra. Za dan
pročitan iz celog snimka (zailiprotiv.rs/mikrofon-dan.json) taj zapis, potpuniji od uživo. Današnji dan (po
beogradskom vremenu) strana broji sama, sa mikrofona. Pokreće ga GitHub Actions (pages.yml) i piše JSON na izlaz;
kad mikrofon ne radi, ne piše ništa i izlazi sa greškom, pa ostaje ono što je već objavljeno.
"""
from __future__ import annotations

import json
import sys
import urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo

MIKROFON = "https://mikrofon.zailiprotiv.rs/"
SNIMAK = "https://zailiprotiv.rs/mikrofon-dan.json"
SAZIV_OD = "2026-11-17"
SLUG = "vucic-aleksandar"


def fetch(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "daliprica/1", "Cache-Control": "no-cache"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read().decode("utf-8"))
    if data.get("radi") is False:  # računar sa mikrofonom ugašen: Cloudflare-ov radnik odgovara umesto njega
        raise RuntimeError(f"{url}: mikrofon ne radi")
    return data


def by_day(today: str, get=fetch) -> dict[str, int]:
    try:
        whole = get(SNIMAK)
    except Exception:
        whole = {}
    days = set(get(MIKROFON + "dani.json").get("dani", [])) | ({whole["dan"]} if whole.get("dan") else set())
    out = {}
    for day in sorted(days):
        if day < SAZIV_OD or day >= today:  # samo 15. saziv, i samo završeni dani
            continue
        turns = whole.get("govori", []) if day == whole.get("dan") else get(f"{MIKROFON}dan/{day}.json").get("govori", [])
        out[day] = int(sum(t["do"] - t["od"] for t in turns if t.get("adresa") == SLUG and t.get("okvira", 2) >= 2))
    return out


if __name__ == "__main__":
    today = datetime.now(ZoneInfo("Europe/Belgrade")).strftime("%Y-%m-%d")
    json.dump({"po_danu": by_day(today)}, sys.stdout, sort_keys=True)
    print()
