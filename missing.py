#!/usr/bin/env python3

import json
import sys

LOST = "08/12/2004"

for path in sys.argv[1:]:
    with open(path) as f:
        j = json.load(f)
    for k, v in sorted((int(k), v) for k, v in j.items()):
        if v["date"] == LOST:
            print("%6d %s" % (k, v["title"]))
