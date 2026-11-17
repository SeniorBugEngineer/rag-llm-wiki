import re
from pathlib import Path

LINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]*)?\]\]")

def parse_frontmatter(text: str):
    text = text.lstrip("﻿").replace("\r\n", "\n")
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    meta = {}
    for line in text[4:end].splitlines():
        line = line.split(" #", 1)[0].rstrip()
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        val = val.strip()
        if val.startswith("[") and val.endswith("]"):
            val = [v.strip() for v in val[1:-1].split(",") if v.strip()]
        meta[key.strip()] = val
    body = text[end + 4:].lstrip("\n")
    return meta, body

def find_links(body: str):
    return [m.group(1).strip() for m in LINK_RE.finditer(body)]

def wiki_pages(root: Path):
    pages = {}
    for sub in ("sources", "concepts"):
        for p in sorted((root / "wiki" / sub).glob("*.md")):
            pages[p.stem] = p
    return pages
