#!/usr/bin/env python3
# coding=utf-8
#
# Generate a domain list from multiple gfwlist upstreams (for dnsmasq/ipset rules generation)
# Upstreams: gfwlist-by-loukky, pexcn, gfwlist (official)
#
# Copyright (C) 2014 http://www.shuyz.com
# Ref https://code.google.com/p/autoproxy-gfwlist/wiki/Rules

import base64
import io
import re
import sys
from urllib.request import Request, urlopen

# (name, url) of each upstream, in merge order
UPSTREAMS = [
    ("gfwlist-by-loukky", "https://raw.githubusercontent.com/Loukky/gfwlist-by-loukky/master/gfwlist.txt"),
    ("pexcn", "https://raw.githubusercontent.com/pexcn/daily/gh-pages/gfwlist/gfwlist.txt"),
    ("gfwlist", "https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt"),
]

TIMEOUT = 30


def _usage() -> None:
    print("usage: update_gfwlist.py <outfile>", file=sys.stderr)


def _decode_gfwlist(raw: bytes) -> str:
    try:
        decoded = base64.b64decode(raw)
        text = decoded.decode("utf-8", "ignore")
        if text.lstrip().startswith("[AutoProxy"):
            return text
    except Exception:
        pass
    return raw.decode("utf-8", "ignore")


def _fetch(url: str) -> str:
    request = Request(url, headers={"User-Agent": "fancyss-update-gfwlist/1.0"})
    with urlopen(request, timeout=TIMEOUT) as response:
        return _decode_gfwlist(response.read())


def _extract_domains(content: str, comment_re, domain_re, domains, seen) -> int:
    """Append domains from one source to `domains` (deduped in `seen`), return new count.

    One domain is taken per whitespace token, so URL-rule lines such as
    "|http://a.com/path/file.html" yield only "a.com", while plain lists
    with several domains per line are still fully expanded.
    """
    added = 0
    for line in content.splitlines():
        if comment_re.search(line):
            continue
        for token in line.split():
            match = domain_re.search(token)
            if not match:
                continue
            domain = match.group(1)
            if domain in seen:
                continue
            seen.add(domain)
            domains.append(domain)
            added += 1
    return added


def main(argv) -> int:
    if len(argv) != 2:
        _usage()
        return 2

    outfile = argv[1]

    comment_re = re.compile(r"^\!|\[|^@@|^\d+\.\d+\.\d+\.\d+")
    domain_re = re.compile(r"([\w\-\_]+\.[\w\.\-\_]+)[\/\*]*")

    domains = []
    seen = set()
    ok_sources = []

    print("fetching lists...")
    for name, url in UPSTREAMS:
        try:
            content = _fetch(url)
        except Exception as exc:
            print(f"warning: failed to fetch {name} ({url}): {exc}", file=sys.stderr)
            continue
        added = _extract_domains(content, comment_re, domain_re, domains, seen)
        ok_sources.append(name)
        print(f"{name}: +{added} new domains (total {len(domains)})")

    if not ok_sources:
        print("error: all upstreams failed to fetch, no file written", file=sys.stderr)
        return 1

    with io.open(outfile, "w", encoding="utf-8", newline="\n") as out_fp:
        for domain in domains:
            out_fp.write(f"{domain}\n")

    print(f"merged {len(domains)} unique domains from {len(ok_sources)}/{len(UPSTREAMS)} upstreams: {', '.join(ok_sources)}")
    print("saving to file:", outfile)
    print("done!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
