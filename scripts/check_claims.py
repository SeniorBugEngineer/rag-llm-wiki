"""C2+/C3+/C4+ 數字對應檢查（v2 新增）。

每個 Wiki 頁、大綱論點、投影片中出現的數字，都必須能在它引用的來源中找到：
  Wiki 頁    → frontmatter sources 對應的 raw/<id>.md
  大綱論點   → 該行 src: 指向的 Wiki 頁
  投影片     → data-src 指向的 Wiki 頁
單位換算等刻意的改寫，用 <!-- num-ok: 2,100 --> 明確標示後放行。
"""
import argparse, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from wikilib import parse_frontmatter, wiki_pages

NUM_RE = re.compile(r"\d+(?:[.,]\d+)*")
OK_RE = re.compile(r"<!--\s*num-ok:\s*(.*?)-->", re.S)
SRC_RE = re.compile(r"src:\s*(\S+\.md)")

def _norm(n):
    return n.replace(",", "")

def extract_numbers(text):
    out = set()
    for m in NUM_RE.findall(text):
        n = _norm(m).rstrip(".")
        if "." in n or len(n) >= 2:
            out.add(n)
    return out

def allowed_numbers(text):
    out = set()
    for block in OK_RE.findall(text):
        for part in re.split(r"[，;；]|,\s+", block):
            m = re.match(r"\d+(?:[.,]\d+)*", part.strip())
            if m:
                out.add(_norm(m.group(0)))
    return out

def missing_numbers(text, evidence, allowed=frozenset()):
    ev = _norm(evidence)
    return sorted(n for n in extract_numbers(OK_RE.sub(" ", text)) if n not in allowed and n not in ev)

def check_wiki_claims(root: Path):
    errors = []
    for slug, path in wiki_pages(root).items():
        text = path.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(text)
        srcs = meta.get("sources", [])
        if isinstance(srcs, str):
            srcs = [srcs]
        evidence = "".join((root / "raw" / f"{s}.md").read_text(encoding="utf-8")
                           for s in srcs if (root / "raw" / f"{s}.md").is_file())
        miss = missing_numbers(body, evidence, allowed_numbers(body))
        if miss:
            errors.append(f"{slug}: numbers not in raw/{{{','.join(srcs)}}}: {miss}")
    return errors

def check_outline_claims(root: Path, outline_path: Path):
    errors = []
    for i, line in enumerate(outline_path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.lstrip().startswith("- "):
            continue
        paths = SRC_RE.findall(line)
        claim = SRC_RE.sub(" ", line)
        evidence = "".join((root / p).read_text(encoding="utf-8") for p in paths if (root / p).is_file())
        miss = missing_numbers(claim, evidence)
        if miss:
            errors.append(f"outline line {i}: numbers not in cited pages: {miss}")
    return errors

_STRIP = [re.compile(p, re.S | re.I) for p in (
    r"<script\b.*?</script>", r"<style\b.*?</style>", r"<!--.*?-->",
    r'<div class="callno">.*?</div>', r'<div class="axis">.*?</div>')]
_SECTION = re.compile(r'<section\b[^>]*class="[^"]*\bslide\b[^"]*"[^>]*>(.*?)</section>', re.S)
_DATASRC = re.compile(r'data-src="([^"]*)"')

def check_html_claims(root: Path, html_path: Path):
    errors = []
    html = html_path.read_text(encoding="utf-8")
    for n, m in enumerate(_SECTION.finditer(html), 1):
        tag = m.group(0)[: m.group(0).find(">") + 1]
        ds = _DATASRC.search(tag)
        paths = [p.strip() for p in (ds.group(1) if ds else "").split(",") if p.strip()]
        if not paths:
            continue
        body = m.group(1)
        ok = allowed_numbers(body)
        for rx in _STRIP:
            body = rx.sub(" ", body)
        text = re.sub(r"<[^>]+>", " ", body)
        evidence = "".join((root / p).read_text(encoding="utf-8") for p in paths if (root / p).is_file())
        miss = missing_numbers(text, evidence, ok)
        if miss:
            errors.append(f"slide {n}: numbers not in cited pages: {miss}")
    return errors

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--wiki", action="store_true")
    g.add_argument("--outline")
    g.add_argument("--html")
    a = ap.parse_args()
    root = Path(a.root)
    if a.wiki:
        errs, tag = check_wiki_claims(root), "C2+"
    elif a.outline:
        errs, tag = check_outline_claims(root, root / a.outline), "C3+"
    else:
        errs, tag = check_html_claims(root, root / a.html), "C4+"
    for e in errs:
        print("ERROR", e)
    if errs:
        print(f"{tag} FAIL ({len(errs)} errors)")
        sys.exit(1)
    print(f"{tag} PASS")

if __name__ == "__main__":
    main()
