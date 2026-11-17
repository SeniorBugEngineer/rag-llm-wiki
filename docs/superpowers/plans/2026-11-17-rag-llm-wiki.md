# RAG LLM Wiki + 教學簡報 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 建立 8 篇資料的 RAG LLM Wiki，以 Wiki 為唯一來源產生教學 HTML 簡報與作業說明頁，全程有可驗證的檢查紀錄。

**Architecture:** Wiki 與簡報都是 repo 內的純文字檔。LLM 節點（擷取、撰寫、生成）由 Claude Code 執行；檢查節點 C2、C3、C4 是只用 Python 標準函式庫寫的腳本，輸出存到 `runs/`，結論 append 到 `log.md`。GitHub Pages 從 `/docs` 發布。

**Tech Stack:** Python 3.12 標準函式庫（unittest、html.parser、pathlib、re）、純 HTML/CSS/JS、Mermaid（只在 process.html 用 CDN 載入）、git。

## Global Constraints

- 只用 Python 標準函式庫（本機沒有 pytest 和 PyYAML）；測試用 `python -m unittest`。
- 文字內容使用繁體中文（台灣用語）；專有名詞保留英文。
- 簡報只能寫 Wiki 有支撐的內容；每張內容投影片都要有 `data-src`。
- 不得捏造檢查失敗；log.md 為 append-only。
- 8 個 source id：`lewis-2020 karpukhin-2020 gao-2023 liu-2023 anthropic-2024 asai-2023 edge-2024 es-2023`。
- raw/ 只存 metadata、摘要原文（abstract）與簡短引文；不全文轉存論文。
- log.md 每行格式：`| 時間 | 節點 | 結果 | 原因 | 處置 |`。
- 遠端：`https://github.com/SeniorBugEngineer/rag-llm-wiki.git`，分支 `main`。

## File Structure

| 檔案 | 責任 |
|---|---|
| `scripts/wikilib.py` | 共用：解析 frontmatter、抽出 `[[link]]`、列出 Wiki 頁 |
| `scripts/check_wiki.py` | C2 |
| `scripts/check_slides.py` | C3（`--outline`）與 C4 |
| `tests/test_check_wiki.py`、`tests/test_check_slides.py` | 單元測試（使用暫存目錄 fixture） |
| `raw/<id>.md` | C1 產物 |
| `wiki/sources/*.md`、`wiki/concepts/*.md`、`wiki/index.md` | Wiki |
| `work/outline.md` | 簡報大綱（C3 輸入） |
| `docs/index.html` | 教學簡報 |
| `docs/process.html` | 作業說明頁 |
| `WORKFLOW.md`、`log.md`、`runs/` | graph 規格與紀錄 |

### Wiki frontmatter 格式（所有任務共用）

```
---
title: Lost in the Middle
type: source            # source | concept
sources: [liu-2023]     # 至少一個 source id
updated: 2026-11-17
url: https://arxiv.org/abs/2307.03172   # 只有 source 頁需要
authors: Nelson F. Liu et al.           # 只有 source 頁需要
year: 2023                              # 只有 source 頁需要
---
```

---

### Task 1: 共用函式庫與 C2 check_wiki.py

**Files:**
- Create: `scripts/wikilib.py`, `scripts/check_wiki.py`, `tests/test_check_wiki.py`, `tests/__init__.py`（空檔）

**Interfaces:**
- Produces:
  - `wikilib.parse_frontmatter(text: str) -> tuple[dict, str]`：值若為 `[a, b]` 則轉成 `list[str]`，否則為 str；沒有 frontmatter 時回傳 `({}, text)`
  - `wikilib.find_links(body: str) -> list[str]`：`[[slug]]` 與 `[[slug|顯示文字]]` 都只取 slug
  - `wikilib.wiki_pages(root: Path) -> dict[str, Path]`：slug → 路徑，範圍是 `wiki/sources/*.md` 與 `wiki/concepts/*.md`
  - `check_wiki.check_wiki(root: Path) -> list[str]`：錯誤訊息清單
  - CLI：`python scripts/check_wiki.py --root .`，全部通過時印 `C2 PASS (N pages)` 並 exit 0，否則逐行印錯誤，最後印 `C2 FAIL (k errors)` 並 exit 1

- [ ] **Step 1: 寫失敗測試** `tests/test_check_wiki.py`

```python
import sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from wikilib import parse_frontmatter, find_links
from check_wiki import check_wiki

SRC = """---
title: Paper A
type: source
sources: [a-2020]
updated: 2026-11-17
url: https://example.org/a
authors: X et al.
year: 2020
---
See [[rag]].
"""
CON = """---
title: RAG
type: concept
sources: [a-2020]
updated: 2026-11-17
---
From [[a-2020|Paper A]].
"""
IDX = "# Index\n- [[a-2020]]\n- [[rag]]\n"

def make(root, files):
    for rel, text in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")

class TestLib(unittest.TestCase):
    def test_frontmatter_list_and_body(self):
        meta, body = parse_frontmatter(CON)
        self.assertEqual(meta["sources"], ["a-2020"])
        self.assertEqual(meta["type"], "concept")
        self.assertIn("From", body)
    def test_no_frontmatter(self):
        self.assertEqual(parse_frontmatter("hi"), ({}, "hi"))
    def test_links_alias(self):
        self.assertEqual(find_links("[[a]] and [[b|B]]"), ["a", "b"])

class TestCheckWiki(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.ok = {"wiki/sources/a-2020.md": SRC, "wiki/concepts/rag.md": CON, "wiki/index.md": IDX}
    def tearDown(self):
        self.tmp.cleanup()
    def test_valid_wiki_passes(self):
        make(self.root, self.ok)
        self.assertEqual(check_wiki(self.root), [])
    def test_broken_link(self):
        make(self.root, {**self.ok, "wiki/concepts/rag.md": CON + "[[nope]]\n"})
        self.assertTrue(any("broken link [[nope]]" in e for e in check_wiki(self.root)))
    def test_missing_field(self):
        make(self.root, {**self.ok, "wiki/sources/a-2020.md": SRC.replace("year: 2020\n", "")})
        self.assertTrue(any("missing field 'year'" in e for e in check_wiki(self.root)))
    def test_unknown_source_id(self):
        make(self.root, {**self.ok, "wiki/concepts/rag.md": CON.replace("[a-2020]", "[zz-1999]")})
        self.assertTrue(any("unknown source 'zz-1999'" in e for e in check_wiki(self.root)))
    def test_type_mismatch(self):
        make(self.root, {**self.ok, "wiki/concepts/rag.md": CON.replace("type: concept", "type: source")})
        self.assertTrue(any("type 'source' does not match folder" in e for e in check_wiki(self.root)))
    def test_not_in_index(self):
        make(self.root, {**self.ok, "wiki/index.md": "- [[a-2020]]\n"})
        self.assertTrue(any("rag: not listed in index" in e for e in check_wiki(self.root)))
    def test_orphan(self):
        src = SRC.replace("See [[rag]].", "")
        make(self.root, {**self.ok, "wiki/sources/a-2020.md": src, "wiki/concepts/rag.md": CON.replace("From [[a-2020|Paper A]].", "")})
        errs = check_wiki(self.root)
        self.assertTrue(any("rag: orphan" in e for e in errs))

if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: 執行，確認失敗**

Run: `python -m unittest tests.test_check_wiki -v`
Expected: `ModuleNotFoundError: No module named 'wikilib'`

- [ ] **Step 3: 實作** `scripts/wikilib.py`

```python
import re
from pathlib import Path

LINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]*)?\]\]")

def parse_frontmatter(text: str):
    text = text.lstrip("﻿")
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    meta = {}
    for line in text[4:end].splitlines():
        line = line.split("#", 1)[0].rstrip() if " #" in line else line.rstrip()
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
```

`scripts/check_wiki.py`

```python
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
    listed = set(find_links(index.read_text(encoding="utf-8"))) if index.exists() else set()
    if not index.exists():
        errors.append("index.md: missing")
    for link in listed - set(pages):
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
```

- [ ] **Step 4: 執行，確認通過**

Run: `python -m unittest tests.test_check_wiki -v`
Expected: 10 tests OK

- [ ] **Step 5: Commit**

```bash
git add scripts/wikilib.py scripts/check_wiki.py tests/
git commit -m "feat: add C2 wiki checker"
```

---

### Task 2: C3/C4 check_slides.py

**Files:**
- Create: `scripts/check_slides.py`, `tests/test_check_slides.py`

**Interfaces:**
- Consumes: `wikilib.wiki_pages`
- Produces:
  - `parse_slides(html: str) -> list[dict]`：每個 `<section class="slide ...">` 對應 `{"n": 1-based, "kind": data-kind 或 "content", "src": [路徑...]}`；`data-src` 以逗號分隔
  - `check_slides(root: Path, html_path: Path) -> tuple[list[str], list[str]]`：(errors, warnings)。kind 為 `cover` 或 `summary` 的投影片不檢查 data-src；沒被引用的 concept 頁列為 warning
  - `check_outline(root: Path, outline_path: Path) -> list[str]`：每行 `- ` 開頭的論點都必須含 `src: wiki/...md`，且檔案存在
  - CLI：`python scripts/check_slides.py --root . --html docs/index.html` → `C4 PASS/FAIL`；`--outline work/outline.md` → `C3 PASS/FAIL`

- [ ] **Step 1: 寫失敗測試** `tests/test_check_slides.py`

```python
import sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from check_slides import parse_slides, check_slides, check_outline

HTML = """<html><body>
<section class="slide" data-kind="cover"><h1>RAG</h1></section>
<section class="slide" data-src="wiki/concepts/rag.md, wiki/sources/a-2020.md"><p>x</p></section>
<section class="slide"><p>no src</p></section>
<section class="slide" data-src="wiki/concepts/ghost.md"><p>y</p></section>
</body></html>"""

class T(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        for rel in ["wiki/concepts/rag.md", "wiki/concepts/unused.md", "wiki/sources/a-2020.md"]:
            p = self.root / rel; p.parent.mkdir(parents=True, exist_ok=True); p.write_text("x", encoding="utf-8")
        self.html = self.root / "docs/index.html"; self.html.parent.mkdir(); self.html.write_text(HTML, encoding="utf-8")
    def tearDown(self):
        self.tmp.cleanup()
    def test_parse(self):
        s = parse_slides(HTML)
        self.assertEqual(len(s), 4)
        self.assertEqual(s[0]["kind"], "cover")
        self.assertEqual(s[1]["src"], ["wiki/concepts/rag.md", "wiki/sources/a-2020.md"])
    def test_errors_and_warnings(self):
        errs, warns = check_slides(self.root, self.html)
        self.assertEqual(len(errs), 2)
        self.assertTrue(any("slide 3: missing data-src" in e for e in errs))
        self.assertTrue(any("slide 4: source not found wiki/concepts/ghost.md" in e for e in errs))
        self.assertTrue(any("unused" in w for w in warns))
    def test_outline(self):
        o = self.root / "work/outline.md"; o.parent.mkdir()
        o.write_text("# 大綱\n- 定義 src: wiki/concepts/rag.md\n- 沒出處\n- 壞的 src: wiki/concepts/ghost.md\n", encoding="utf-8")
        errs = check_outline(self.root, o)
        self.assertEqual(len(errs), 2)

if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: 執行，確認失敗**

Run: `python -m unittest tests.test_check_slides -v`
Expected: `ModuleNotFoundError: No module named 'check_slides'`

- [ ] **Step 3: 實作** `scripts/check_slides.py`

```python
import argparse, re, sys
from html.parser import HTMLParser
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from wikilib import wiki_pages

SKIP_KINDS = {"cover", "summary"}

class _P(HTMLParser):
    def __init__(self):
        super().__init__(); self.slides = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "section" and "slide" in (a.get("class") or "").split():
            src = [s.strip() for s in (a.get("data-src") or "").split(",") if s.strip()]
            self.slides.append({"n": len(self.slides) + 1, "kind": a.get("data-kind") or "content", "src": src})

def parse_slides(html: str):
    p = _P(); p.feed(html); return p.slides

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
            errors.append(f"slide {s['n']}: missing data-src"); continue
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
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--html")
    ap.add_argument("--outline")
    a = ap.parse_args(); root = Path(a.root)
    if a.outline:
        errs = check_outline(root, root / a.outline); tag = "C3"; warns = []
    else:
        errs, warns = check_slides(root, root / (a.html or "docs/index.html")); tag = "C4"
    for e in errs: print("ERROR", e)
    for w in warns: print("WARN ", w)
    if errs:
        print(f"{tag} FAIL ({len(errs)} errors, {len(warns)} warnings)"); sys.exit(1)
    print(f"{tag} PASS ({len(warns)} warnings)")

if __name__ == "__main__":
    main()
```

- [ ] **Step 4: 執行全部測試**

Run: `python -m unittest discover -s tests -v`
Expected: 13 tests OK

- [ ] **Step 5: Commit**

```bash
git add scripts/check_slides.py tests/test_check_slides.py
git commit -m "feat: add C3/C4 outline and slide checkers"
```

---

### Task 3: WORKFLOW.md v1、log.md、runs/

**Files:**
- Create: `WORKFLOW.md`, `log.md`, `runs/.gitkeep`, `README.md`

- [ ] **Step 1:** 寫 `WORKFLOW.md`：spec 第 5 節的 graph 改成 Mermaid `flowchart TD`，列出 C1–C5 的定義（逐字取自 spec），以及執行指令：
  - C2：`python scripts/check_wiki.py --root . > runs/<YYYYMMDD-HHMM>-C2.txt`
  - C3：`python scripts/check_slides.py --outline work/outline.md > runs/<ts>-C3.txt`
  - C4：`python scripts/check_slides.py --html docs/index.html > runs/<ts>-C4.txt`
  - 標題寫「## v1（初版）」，並預留「## v2」段落，寫「待 v1 執行完後依 log 統計填入」。
- [ ] **Step 2:** 寫 `log.md`：表頭 `| 時間 | 節點 | 結果 | 原因 | 處置 |`，第一列記錄 `設計 | PASS | spec 與 plan 完成 | 進入 ingest`。
- [ ] **Step 3:** 寫 `README.md`：專題簡介、目錄說明、Wiki／簡報／說明頁的連結（Pages 網址 `https://seniorbugengineer.github.io/rag-llm-wiki/`）。
- [ ] **Step 4: Commit** `git add WORKFLOW.md log.md runs/.gitkeep README.md && git commit -m "docs: add workflow v1 and log"`

---

### Task 4: Wiki 迴圈：ingest 8 篇（C1 + source 頁 + C2）

**Files:**
- Create: `raw/<id>.md` ×8、`wiki/sources/<id>.md` ×8、`wiki/index.md`（先只列 sources）

對每個 id 依書單順序執行**同一個迴圈**：

- [ ] **Step 1: 取得資料**：用 WebFetch 抓 `https://arxiv.org/abs/<arxiv-id>`（anthropic-2024 抓 `https://www.anthropic.com/news/contextual-retrieval`）。失敗時依序改抓 `arxiv.org/html/<id>`、`arxiv.org/pdf/<id>`。
- [ ] **Step 2: C1 來源核實**：比對抓到的標題、第一作者、年份與書單是否一致，擷取文字是否非空。結果 append 到 log.md（PASS，或 FAIL＋原因＋重抓）。若三種 URL 都失敗，記錄 FAIL、跳過該篇並告知使用者；不得用記憶補寫。
- [ ] **Step 3:** 寫 `raw/<id>.md`：metadata（title、authors、year、url、fetched、C1 結果）＋ abstract 原文＋ 3～6 段簡短引文（標出所在章節）。
- [ ] **Step 4:** 寫 `wiki/sources/<id>.md`：frontmatter（source 版）；段落依序為「一句話重點」「解決什麼問題」「怎麼做」「關鍵結果（含數字，取自 raw）」「限制」「相關概念」（`[[concept-slug]]`，用 Task 5 會建立的 slug：`rag retrieval embedding chunking hybrid-search reranking lost-in-the-middle contextual-retrieval modular-rag self-rag graphrag evaluation hallucination`）。每項主張都必須能在 raw/ 找到依據。
- [ ] **Step 5:** 8 篇全部完成後，將 index.md 加上 8 個 source。接著跑 C2：`python scripts/check_wiki.py --root . > runs/<ts>-C2-sources.txt`。此時因為 concept 頁尚未建立，**預期會出現 broken link**。照實記錄到 log.md，處置寫「進入 Task 5 建立概念頁」。
- [ ] **Step 6: Commit** `git add raw wiki runs log.md && git commit -m "feat: ingest 8 RAG sources"`

---

### Task 5: 概念頁 + index + C2 迴圈

**Files:**
- Create: `wiki/concepts/<slug>.md` ×13（slug 見 Task 4 Step 4）
- Modify: `wiki/index.md`

- [ ] **Step 1:** 每個概念頁依序寫入：frontmatter（concept 版，sources 列出實際引用的 id）、「白話定義」（給新手看）、「為什麼重要」、「怎麼運作」、「出處說法」（每點標 `[[source-id]]`）、「相關概念」。只綜合 wiki/sources 與 raw/ 的內容。
- [ ] **Step 2:** 更新 index.md：分「概念（建議閱讀順序）」與「資料」兩區，列出全部頁面。
- [ ] **Step 3: C2 迴圈**：跑 `python scripts/check_wiki.py --root . > runs/<ts>-C2.txt`。FAIL 時逐項修正，重跑直到 PASS；**每一輪**都 append 一行 log（含錯誤數與錯誤類型）。
- [ ] **Step 4: Commit** `git add wiki runs log.md && git commit -m "feat: add concept pages; C2 pass"`

---

### Task 6: 簡報大綱 + C3

**Files:**
- Create: `work/outline.md`

- [ ] **Step 1: 查詢 Wiki**：依 spec 第 6 節的 18 張結構，每張寫 1 行標題，加上 2～4 個論點行。格式為 `- 論點文字 src: wiki/concepts/x.md`（可附多個 src）。論點只能來自所引用的頁面。
- [ ] **Step 2: C3**：`python scripts/check_slides.py --root . --outline work/outline.md > runs/<ts>-C3.txt`。FAIL 時補查 Wiki 找出處，找不到就刪掉該論點，重跑直到 PASS，每輪都寫 log。
- [ ] **Step 3:** 人工抽查 5 個論點，確認被引用的頁面確實支撐該論點（腳本只能確認檔案存在），結果寫進 log（`C3-語意抽查`）。
- [ ] **Step 4: Commit** `git add work runs log.md && git commit -m "feat: slide outline; C3 pass"`

---

### Task 7: 生成教學簡報 + C4 + C5

**Files:**
- Create: `docs/index.html`

- [ ] **Step 1:** 先載入 `artifact-design` skill 以取得設計準則（色彩 token、深淺色、手機寬度），再依 outline.md 生成單一 HTML：
  - 每張投影片是 `<section class="slide" data-src="...">`，封面加 `data-kind="cover"`，總結加 `data-kind="summary"`
  - ←／→、空白鍵、點擊翻頁；網址 hash `#n` 對應頁碼；顯示頁碼與進度條
  - 右下角出處連結指向 `https://github.com/SeniorBugEngineer/rag-llm-wiki/blob/main/<path>`
  - 流程圖用 inline SVG，不依賴外部 JS
  - 總結頁附 3 題自我檢測，點擊後顯示答案
- [ ] **Step 2: C4 迴圈**：`python scripts/check_slides.py --root . --html docs/index.html > runs/<ts>-C4.txt`。有 error 時只重做壞掉的投影片並重跑；warning（未被引用的概念）要在 log 寫明保留或補上的理由。
- [ ] **Step 3: C5**：用 `start docs/index.html` 在瀏覽器開啟，確認翻頁、第 1／9／18 頁版面、視窗縮到約 400px 時沒有橫向捲動。人工通讀，記錄任何新手可能看不懂的詞，修改後在 log 記一行。
- [ ] **Step 4: Commit** `git add docs/index.html runs log.md && git commit -m "feat: teaching slides; C4/C5 pass"`

---

### Task 8: 反思、WORKFLOW v2、process.html

**Files:**
- Modify: `WORKFLOW.md`, `log.md`
- Create: `docs/process.html`

- [ ] **Step 1:** 統計 log.md 各節點的 FAIL 次數，以表格寫入 WORKFLOW.md。
- [ ] **Step 2:** 依統計結果決定 v2：把最常失敗節點的檢查前移（例如若 C2 broken link 最多，就在撰寫 source 頁時先確認 slug 清單存在）。在 WORKFLOW.md 的「## v2」寫入新的 Mermaid 圖與修改理由。若 v2 前移需要新的腳本參數，在此任務以 TDD 加入。若統計顯示沒有值得前移的點，照實寫出。
- [ ] **Step 3:** 生成 `docs/process.html`：依 spec 第 7 節的 6 個區塊；Mermaid 使用 `https://cdn.jsdelivr.net/npm/mermaid@10.9.1/dist/mermaid.min.js`；執行紀錄表直接取自 log.md；反思依據 Step 1 的統計。
- [ ] **Step 4:** 跑全部檢查，確認仍通過：`python -m unittest discover -s tests && python scripts/check_wiki.py && python scripts/check_slides.py --html docs/index.html`
- [ ] **Step 5: Commit** `git add WORKFLOW.md log.md docs/process.html && git commit -m "docs: workflow v2, reflection, process page"`

---

### Task 9: 發布

- [ ] **Step 1:** 新增 `docs/.nojekyll`（避免 Jekyll 處理 docs/superpowers 內的 md）。
- [ ] **Step 2:** `git push -u origin main`。若需要認證，請使用者在終端機完成登入。
- [ ] **Step 3:** 請使用者在 GitHub 的 Settings → Pages 選擇 Source `main`、資料夾 `/docs`。
- [ ] **Step 4:** 用 WebFetch 確認 `https://seniorbugengineer.github.io/rag-llm-wiki/` 與 `/process.html` 回應 200 且有內容，在 log 記錄 `發布 | PASS`，commit 並 push。
