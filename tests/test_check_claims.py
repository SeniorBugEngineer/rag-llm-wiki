import sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from check_claims import extract_numbers, allowed_numbers, missing_numbers, check_wiki_claims, check_outline_claims, check_html_claims

RAW = "# P\n| title | A |\nNQ 59.1 -> 78.4; 21,015,324 passages; 21M docs\n"
SRC_OK = """---
title: A
type: source
sources: [a-2020]
updated: 2026-11-17
---
NQ 從 59.1 到 78.4，共 21,015,324 段。
"""
SRC_BAD = SRC_OK.replace("78.4", "87.4")
SRC_CONV = SRC_OK + "約 2,100 萬份文件。<!-- num-ok: 2,100 = 21M -->\n"

def make(root, files):
    for rel, text in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")

class TestHelpers(unittest.TestCase):
    def test_extract_skips_single_digits_and_normalizes_commas(self):
        self.assertEqual(extract_numbers("第 5 步，59.1 與 21,015,324"), {"59.1", "21015324"})
    def test_allowed(self):
        self.assertEqual(allowed_numbers("x <!-- num-ok: 2,100, 170 -->"), {"2100", "170"})
    def test_missing(self):
        self.assertEqual(missing_numbers("59.1 和 87.4", "59.1"), ["87.4"])

class TestModes(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
    def tearDown(self):
        self.tmp.cleanup()
    def test_wiki_ok(self):
        make(self.root, {"raw/a-2020.md": RAW, "wiki/sources/a-2020.md": SRC_OK})
        self.assertEqual(check_wiki_claims(self.root), [])
    def test_wiki_typo_caught(self):
        make(self.root, {"raw/a-2020.md": RAW, "wiki/sources/a-2020.md": SRC_BAD})
        errs = check_wiki_claims(self.root)
        self.assertEqual(len(errs), 1)
        self.assertIn("87.4", errs[0])
    def test_wiki_conversion_allowed(self):
        make(self.root, {"raw/a-2020.md": RAW, "wiki/sources/a-2020.md": SRC_CONV})
        self.assertEqual(check_wiki_claims(self.root), [])
    def test_outline(self):
        make(self.root, {"wiki/concepts/x.md": "準確率 78.4\n",
                         "work/outline.md": "- 好 78.4 src: wiki/concepts/x.md\n- 壞 99.9 src: wiki/concepts/x.md\n"})
        errs = check_outline_claims(self.root, self.root / "work/outline.md")
        self.assertEqual(len(errs), 1)
        self.assertIn("line 2", errs[0])
    def test_html_ignores_callno_axis_and_script(self):
        make(self.root, {"wiki/concepts/x.md": "準確率 78.4\n", "docs/index.html": """
<section class="slide" data-src="wiki/concepts/x.md"><div class="callno">07</div><p>78.4</p>
<div class="axis"><span>0</span><span>50</span><span>100</span></div><script>var a=12345;</script></section>
<section class="slide" data-src="wiki/concepts/x.md"><p>66.6</p></section>"""})
        errs = check_html_claims(self.root, self.root / "docs/index.html")
        self.assertEqual(len(errs), 1)
        self.assertIn("slide 2", errs[0])
    def test_html_num_ok(self):
        make(self.root, {"wiki/concepts/x.md": "x\n", "docs/index.html":
            '<section class="slide" data-src="wiki/concepts/x.md"><!-- num-ok: 0.12 --><p>0.12</p></section>'})
        self.assertEqual(check_html_claims(self.root, self.root / "docs/index.html"), [])

if __name__ == "__main__":
    unittest.main()
