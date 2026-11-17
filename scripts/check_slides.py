import argparse, re, sys
from html.parser import HTMLParser
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from wikilib import wiki_pages

SKIP_KINDS = {"cover", "summary"}

class _P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.slides = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "section" and "slide" in (a.get("class") or "").split():
            src = [s.strip() for s in (a.get("data-src") or "").split(",") if s.strip()]
            self.slides.append({"n": len(self.slides) + 1, "kind": a.get("data-kind") or "content", "src": src})

def parse_slides(html: str):
    p = _P()
    p.feed(html)
    return p.slides

def check_slides(root: Path, html_path: Path):
    errors, warnings = [], []
    slides = parse_slides(html_path.read_text(encoding="utf-8"))
    if not slides:
        errors.append("no slides found")
    cited = set()
    for s in slides:
        if s["kind"] in SKIP_KINDS:
            continue
        if not s["src"]:
            errors.append(f"slide {s['n']}: missing data-src")
            continue
        for path in s["src"]:
            if not (root / path).is_file():
                errors.append(f"slide {s['n']}: source not found {path}")
            else:
                cited.add(Path(path).stem)
    for slug, p in wiki_pages(root).items():
        if p.parent.name == "concepts" and slug not in cited:
            warnings.append(f"concept not cited by any slide: {slug}")
    return errors, warnings

SRC_RE = re.compile(r"src:\s*(\S+\.md)")

def check_outline(root: Path, outline_path: Path):
    errors = []
    for i, line in enumerate(outline_path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.lstrip().startswith("- "):
            continue
        paths = SRC_RE.findall(line)
        if not paths:
            errors.append(f"outline line {i}: no src")
        for p in paths:
            if not (root / p).is_file():
                errors.append(f"outline line {i}: source not found {p}")
    return errors

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--html")
    ap.add_argument("--outline")
    a = ap.parse_args()
    root = Path(a.root)
    if a.outline:
        errs, warns, tag = check_outline(root, root / a.outline), [], "C3"
    else:
        errs, warns = check_slides(root, root / (a.html or "docs/index.html"))
        tag = "C4"
    for e in errs:
        print("ERROR", e)
    for w in warns:
        print("WARN ", w)
    if errs:
        print(f"{tag} FAIL ({len(errs)} errors, {len(warns)} warnings)")
        sys.exit(1)
    print(f"{tag} PASS ({len(warns)} warnings)")

if __name__ == "__main__":
    main()
