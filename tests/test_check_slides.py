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
