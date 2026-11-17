# RAG LLM Wiki

以「RAG（Retrieval-Augmented Generation，檢索增強生成）」為主題的 LLM Wiki，並以此 Wiki 為唯一知識來源產生教學型 HTML 簡報。

- 📚 Wiki 目錄：[wiki/index.md](wiki/index.md)
- 🖥️ 教學簡報：https://seniorbugengineer.github.io/rag-llm-wiki/
- 📝 作業說明（loop/graph、執行紀錄、反思）：https://seniorbugengineer.github.io/rag-llm-wiki/process.html

## 結構

| 路徑 | 內容 |
|---|---|
| `raw/` | 8 篇資料的 metadata、abstract 與簡短引文（C1 核實結果） |
| `wiki/sources/` | 每篇資料的摘要頁 |
| `wiki/concepts/` | 概念頁 |
| `work/outline.md` | 簡報大綱（每個論點標註 Wiki 出處） |
| `docs/` | 簡報與說明頁（GitHub Pages） |
| `scripts/` | 檢查腳本 C2/C3/C4 |
| `WORKFLOW.md` | loop / graph 設計 |
| `log.md`、`runs/` | 執行與檢查紀錄 |

## 重跑檢查

```bash
python -m unittest discover -s tests
python scripts/check_wiki.py
python scripts/check_slides.py --outline work/outline.md
python scripts/check_slides.py --html docs/index.html
```
