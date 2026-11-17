import argparse, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from wikilib import parse_frontmatter, find_links, wiki_pages

COMMON = ["title", "type", "sources", "updated"]
SOURCE_ONLY = ["url", "authors", "year"]

def check_wiki(root: Path):
    errors = []
    pages = wiki_pages(root)
    source_ids = {s for s, p in pages.items() if p.parent.name == "sources"}
    inbound = {s: set() for s in pages}
    for slug, path in pages.items():
        meta, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        folder = "source" if path.parent.name == "sources" else "concept"
        required = COMMON + (SOURCE_ONLY if folder == "source" else [])
        for f in required:
            if not meta.get(f):
                errors.append(f"{slug}: missing field '{f}'")
        if meta.get("type") and meta["type"] != folder:
            errors.append(f"{slug}: type '{meta['type']}' does not match folder '{folder}'")
        srcs = meta.get("sources", [])
        if isinstance(srcs, str):
            srcs = [srcs]
        for s in srcs:
            if s not in source_ids:
                errors.append(f"{slug}: unknown source '{s}'")
        for link in find_links(body):
            if link not in pages:
                errors.append(f"{slug}: broken link [[{link}]]")
            elif link != slug:
                inbound[link].add(slug)
    index = root / "wiki" / "index.md"
    if index.exists():
        listed = set(find_links(index.read_text(encoding="utf-8")))
    else:
        listed = set()
        errors.append("index.md: missing")
    for link in sorted(listed - set(pages)):
        errors.append(f"index.md: broken link [[{link}]]")
    for slug in pages:
        if slug not in listed:
            errors.append(f"{slug}: not listed in index.md")
        if not inbound[slug]:
            errors.append(f"{slug}: orphan (no inbound links from other pages)")
    return errors

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    root = Path(ap.parse_args().root)
    errors = check_wiki(root)
    for e in errors:
        print(e)
    if errors:
        print(f"C2 FAIL ({len(errors)} errors)")
        sys.exit(1)
    print(f"C2 PASS ({len(wiki_pages(root))} pages)")

if __name__ == "__main__":
    main()
