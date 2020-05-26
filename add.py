#!/usr/bin/env python3

import os
import re
import requests
import sys
import urllib.parse


DATE = re.compile(r"(https://web.archive.org/web/(\d{8})\d{6})(?:id_)?/(.*)")
# /http://www.ambrosiasw.com/cgi-bin/vftp/show.pl?product=avara&category=*&display=date&page=1

exit = 0
for url in sys.argv[1:]:
    m = DATE.match(url)
    if m is None:
        exit = 1
        print("not a good URL: %s" % url)
        continue
    q = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
    prefix, date, suffix = m.groups()
    game, = q["product"]
    page, = q["page"]
    url = f"{prefix}id_/{suffix}"
    print(url)

    r = requests.get(url)
    r.raise_for_status()
    try:
        os.makedirs(f"archive/{game}")
    except FileExistsError:
        pass
    with open(f"archive/{game}/{date}-{page}.json", "wb") as f:
        f.write(r.content)
sys.exit(exit)
