#!/usr/bin/env python3

import datetime, os
from collections import OrderedDict

LONDON_TERMS = {
    "BLFR":    "Blackfriars",
    "CANONST": "Cannon Street",
    "CHRX":    "Charing Cross",
    "EUSTON":  "Euston",
    "FENCHRS": "Fenchurch Street",
    "KNGX":    "Kings Cross",
    "LIVST":   "Liverpool Street",
    "LNDNBDC": "London Bridge (Central)",
    "LNDNBDE": "London Bridge (Eastern)",
    "LNDNBDG": "London Bridge (Main)",
    "MARYLBN": "Marylebone",
    "MRGT":    "Moorgate",
    "PADTON":  "Paddington",
    "STPXBOX": "St Pancras (Thameslink)",
    "STPANCI": "St Pancras (Channel Tunnel Rail Link)",
    "STPX":    "St Pancras (Midland Main Line)",
    "VICTRIC": "Victoria (Central)",
    "VICTRIA": "Victoria",
    "VICTRIE": "Victoria (Southeastern)",
    "WATRLMN": "Waterloo"
    }

def process_time(unix_time):
    out = OrderedDict([("ut",None), ("iso", None), ("short", "")])
    if unix_time:
        dt = datetime.datetime.fromtimestamp(float(unix_time))
        out["ut"] = unix_time
        out["iso"] = dt.strftime("%Y-%m-%dT%H:%M:%S")
        out["date"] = dt.strftime("%Y-%m-%d")
        out["short"] = dt.strftime("%H%M") #+ "½"*(dt.second==30)
    return out

insertion = ""

all_lines = []
by_tiploc = OrderedDict()
with open("rushhourdata.csv") as f:
    for line in f:
        all_lines.append({x:y for x,y in zip(["tiploc", "cat", "pow", "tl", "toc", "ut", "time_hr"],line.split(","))})

for a in sorted(LONDON_TERMS.keys()):
    by_tiploc[a] = []

for x in all_lines:
    x["arrival"] = process_time(int(x["ut"]))
    if x["tiploc"] not in by_tiploc:
        by_tiploc[x["tiploc"]] = []
    by_tiploc[x["tiploc"]].append(x)

x_start, y_start = 80,120
x_step, y_step = 170,105
x,y = x_start,y_start
x_limit = 2850
color = True
for k,v in by_tiploc.items():
    color = not color
    if x > x_limit - 200 or x > x_limit:
        y += y_step
        x = x_start
    if len(v):
        insertion += '<tspan x="{}" y="{}" class="br time {}">{}</tspan>\n'.format(x,y-56, color*"grey" or "grey2", LONDON_TERMS[k])
    for call in v:
        if x>x_limit:
            y += y_step
            x = x_start

        insertion += '<tspan x="{}" y="{}" class="mono time {}">{}</tspan>\n'.format(x,y, color*"grey" or "grey2", call["arrival"]["short"])
        x += x_step

with open("eleven-poster.svg") as f:
    body = f.read()

body = body.replace("{{times}}", insertion)

with open("/tmp/eleven-poster-stage.svg", "w") as f:
    f.write(body)

os.system("inkscape -z -e out-eleven.png /tmp/eleven-poster-stage.svg")
