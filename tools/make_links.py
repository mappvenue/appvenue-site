#!/usr/bin/env python3
"""Writes the short-link pages appvenue.io/go/<app>/<channel>/[<content id>/].
Each page forwards to the Google Play listing with an install referrer, so Play Console shows which channel and post brought the install."""
import os, urllib.parse
APP = {"heartprint": "io.appvenue.chatwrapped"}
CHANNELS = ["tt", "ig", "x", "fb", "yt", "th", "rd", "web"]
CONTENT_IDS = [f"c{n:03d}" for n in range(1, 41)]
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "go")

def play(pkg, ch, campaign, cid=None):
    ref = {"utm_source": ch, "utm_medium": "social", "utm_campaign": campaign}
    if cid: ref["utm_content"] = cid
    return "https://play.google.com/store/apps/details?id=%s&referrer=%s" % (pkg, urllib.parse.quote(urllib.parse.urlencode(ref), safe=""))

def page(url):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex"><title>Opening Google Play</title>
<meta http-equiv="refresh" content="0;url={url}"><link rel="canonical" href="{url}"></head>
<body><p><a href="{url}">Open in Google Play</a></p><script>location.replace({url!r});</script></body></html>
'''

for app, pkg in APP.items():
    for ch in CHANNELS:
        d = os.path.join(ROOT, app, ch); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w").write(page(play(pkg, ch, "bio")))
        for cid in CONTENT_IDS:
            d2 = os.path.join(d, cid); os.makedirs(d2, exist_ok=True)
            open(os.path.join(d2, "index.html"), "w").write(page(play(pkg, ch, "post", cid)))
print("ok")
