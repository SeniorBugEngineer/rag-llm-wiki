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
