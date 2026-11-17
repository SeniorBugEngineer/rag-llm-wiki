# Introducing Contextual Retrieval

| 欄位 | 值 |
|---|---|
| id | anthropic-2024 |
| title | Introducing Contextual Retrieval |
| authors | Anthropic |
| year | 2024 |
| venue | Anthropic 官方文章，2024-09-19 |
| url | https://www.anthropic.com/news/contextual-retrieval |
| abstract 來源 | — |
| 內文來源 | www.anthropic.com/news/contextual-retrieval |
| fetched | 2026-11-17 |
| C1 核實 | PASS：標題／第一作者／年份與書單一致 |

## Abstract（原文）

> （非論文，無 abstract；以下擷取筆記取自原文頁面，引號內為原文短引。）

## 內文擷取筆記（[章節] 事實；數字照原文）

- [Problem] 傳統 RAG 切 chunk 後會失去上下文，例如 chunk 只寫「The company's revenue grew by 3%」，不知道是哪家公司、哪一季。
- [Contextual Embeddings] 在每個 chunk 前加上一段說明它在整份文件中位置的上下文，再做 embedding。
- [Contextual BM25] 同樣的「加上下文 chunk」也拿來建 BM25（關鍵字）索引。
- [Generating context] 用 Claude（文中為 Claude 3 Haiku）讀整份文件與該 chunk，要求產生「a short succinct context to situate this chunk within the overall document」，通常 50–100 tokens；用 prompt caching 讓整份文件只需快取一次。
- [Results] 指標為 top-20 檢索失敗率（1 − recall@20）：Contextual Embeddings 失敗率降 35%（5.7% → 3.7%）；再加 Contextual BM25 降 49%（→ 2.9%）；再加 rerank 降 67%（→ 1.9%）。
- [Cost] 產生上下文為一次性成本，約每百萬文件 tokens 1.02 美元（假設 800-token chunk、8k-token 文件）。
- [Reranking] 先取前 150 個 chunk，交給 reranker（文中用 Cohere）評分，留下前 20 個給模型；chunk 數測過 5／10／20，20 最好；rerank 會增加延遲。
- [Takeaways] embeddings + BM25 優於只用 embeddings；給模型 top-20 優於 top-10／top-5；為 chunk 加上下文大幅提升正確率；有 rerank 優於沒有；「All these benefits stack」。
- [When to skip RAG] 知識庫小於 200,000 tokens（約 500 頁）時，可以直接整份放進 prompt，不必做 RAG。
