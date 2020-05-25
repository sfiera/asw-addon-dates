#!/usr/bin/env python3

import json
import requests

ADDONS = "http://www.cytheraguides.com/archives/ambrosia_addons"

for game in [
        "aki",
        "apeiron",
        "apeironx",
        "ares",
        "avara",
        "barrack",
        "bt",
        "chiral",
        "cythera",
        "darwinia",
        "defcon",
        "dr",
        "ev",
        "evn",
        "evo",
        "ferazel",
        "harry",
        "maelstrom",
        "mr",
        "pop-pop",
        "redline",
        "sketchfighter",
        "slithereens",
        "swoop",
        "uplink",
]:
    r = requests.get(f"{ADDONS}/{game}/_contents.json")
    r.raise_for_status()
    with open(f"json/{game}.json", "w") as f:
        json.dump(r.json(), f)
