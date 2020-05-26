#!/usr/bin/env python3

import bs4
import collections
import glob
import json
import os
import re
import sys
import urllib.parse

LOST = "08/12/2004"
FILE = re.compile(r"[^/]*/\d+_(.*)")
DATE = re.compile(r"\d+/\d+/\d+")

for game in sys.argv[1:]:
    print(game)
    missing = {}
    with open(f"json/{game}.json") as f:
        j = json.load(f, object_pairs_hook=collections.OrderedDict)
    for k, v in j.items():
        if v["filepath"] == "FileNotFound":
            continue
        filepath = urllib.parse.unquote(FILE.match(v["filepath"]).group(1))
        if v["date"] == LOST:
            missing[filepath] = v

    found = {}
    for path in glob.glob(f"archive/{game}/*"):
        with open(path, encoding='macroman') as f:
            data = f.read()
        soup = bs4.BeautifulSoup(data, "html.parser")
        links = soup.find_all("a")
        links = [l for l in links if l.text == "Get It"]
        for link in links:
            url = urllib.parse.urlparse(link["href"])
            q = urllib.parse.parse_qs(url.query)
            filepath, = q["file"]

            ancestor = link.parent
            while ancestor.name != "table":
                ancestor = ancestor.parent
            date = DATE.search(ancestor.get_text()).group(0)
            if date == LOST:
                print("WARNING: lost date in %s" % path)

            if filepath in missing:
                found[filepath] = missing[filepath]
                found[filepath]["date"] = date
                del(missing[filepath])

    if os.path.isfile(f"manual/{game}.tsv"):
        with open(f"manual/{game}.tsv") as f:
            keys = f.readline().split("\t")
            for line in f.readlines():
                data = dict(zip(keys, line.split("\t")))
                date = data["date"]
                filepath = data["filepath"]
                if filepath in missing:
                    found[filepath] = missing[filepath]
                    found[filepath]["date"] = date
                    del(missing[filepath])

    if found:
        print()
        print("FOUND:")
        for k, v in found.items():
            print("%14s %s" % (v["date"], k))

    print()
    if missing:
        print("STILL MISSING:")
        for k, v in missing.items():
            print("%14s %s" % (v["date"], k))
    else:
        print("ALL FOUND! YAY!")

    with open(f"json/{game}.json", "w") as f:
        json.dump(j, f)
