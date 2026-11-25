"""Write a valid MaxMind DB (MMDB v2) file that contains no networks. MIT, ReadyStack.

PostHog's Django app, ingestion server and feature-flags service each open /code/share/GeoLite2-City.mmdb at start, and
the feature-flags service refuses to start without it. Upstream downloads MaxMind's GeoLite2 City database into its
image; that database is distributed under MaxMind's GeoLite2 End User License Agreement, not an open licence, so this
build ships this empty database instead: every lookup answers "not found" and PostHog records no location. Mount a
GeoLite2-City or DB-IP City Lite .mmdb at the same path to turn IP geolocation on.

Format: https://maxmind.github.io/MaxMind-DB/ -- a one-node search tree whose two records both equal node_count (the
"no data" value), the 16-byte zero separator, an empty data section, then the metadata marker and a metadata map.
Deterministic: build_epoch is the argument (the release's SOURCE_DATE_EPOCH).
"""
import struct
import sys

MARKER = b"\xab\xcd\xefMaxMind.com"


def _ctrl(type_num, size):
    # control byte(s) for a data field: types 1-7 in the first byte, extended types (8+) in a second byte
    assert size < 285
    small, extra = (size, b"") if size < 29 else (29, bytes([size - 29]))
    if type_num <= 7:
        return bytes([(type_num << 5) | small]) + extra
    return bytes([small, type_num - 7]) + extra


def enc(v):
    if isinstance(v, str):
        b = v.encode()
        return _ctrl(2, len(b)) + b
    if isinstance(v, dict):
        out = _ctrl(7, len(v))
        for k, val in v.items():
            out += enc(k) + enc(val)
        return out
    if isinstance(v, list):
        out = _ctrl(11, len(v))
        for x in v:
            out += enc(x)
        return out
    if isinstance(v, tuple):  # ("uint16" | "uint32" | "uint64", value)
        kind, n = v
        width = {"uint16": 2, "uint32": 4, "uint64": 8}[kind]
        b = n.to_bytes(width, "big").lstrip(b"\x00")
        return _ctrl({"uint16": 5, "uint32": 6, "uint64": 9}[kind], len(b)) + b
    raise TypeError(type(v))


def build(epoch):
    node_count = 1
    tree = struct.pack(">I", node_count)[1:] * 2          # 24-bit records: both = node_count = "not found"
    meta = {
        "binary_format_major_version": ("uint16", 2),
        "binary_format_minor_version": ("uint16", 0),
        "build_epoch": ("uint64", int(epoch)),
        "database_type": "GeoLite2-City",
        "description": {"en": "Empty database (no networks): ReadyStack PostHog CE ships no GeoIP data"},
        "ip_version": ("uint16", 6),
        "languages": ["en"],
        "node_count": ("uint32", node_count),
        "record_size": ("uint16", 24),
    }
    return tree + b"\x00" * 16 + MARKER + enc(meta)


if __name__ == "__main__":
    out, epoch = sys.argv[1], sys.argv[2]
    with open(out, "wb") as f:
        f.write(build(epoch))
