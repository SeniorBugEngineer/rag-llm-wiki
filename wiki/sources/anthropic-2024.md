---
title: Introducing Contextual Retrieval
type: source
sources: [anthropic-2024]
updated: 2026-11-17
url: https://www.anthropic.com/news/contextual-retrieval
authors: Anthropic
year: 2024
---
# Introducing Contextual Retrieval

> Anthropic（2024）｜原文：https://www.anthropic.com/news/contextual-retrieval｜擷取：`raw/anthropic-2024.md`

## 一句話重點
**Contextual Retrieval**：切 chunk 前，先請 LLM 為每個 chunk 寫一小段「它在整份文件中的背景說明」，再拿來做向量與關鍵字索引，大幅降低檢索失敗率。

## 解決什麼問題
[[chunking]] 會讓 chunk 失去上下文。例如一個 chunk 只寫「The company's revenue grew by 3%」，檢索時不知道是哪家公司、哪一季。

## 怎麼做
- **Contextual Embeddings**：把 LLM 產生的 50–100 tokens 背景說明加在 chunk 前面再做 [[embedding]]。
- **Contextual BM25**：同樣加了背景的 chunk 也用來建關鍵字索引，形成 [[hybrid-search]]。
- **Reranking**：先取 150 個候選 chunk，再用 reranker 評分，留下前 20 個給模型。詳見 [[reranking]]。
- 用 prompt caching 讓整份文件只需快取一次，成本約每百萬文件 tokens 1.02 美元（一次性）。

## 關鍵結果（top-20 檢索失敗率，原本 5.7%）
| 方法 | 失敗率 | 降幅 |
|---|---|---|
| Contextual Embeddings | 3.7% | −35% |
| + Contextual BM25 | 2.9% | −49% |
| + Reranking | 1.9% | −67% |

- 「All these benefits stack」：各種改良的效果可以疊加。
- 交給模型 20 個 chunk，比 10 或 5 個好。

## 什麼時候不用 RAG
知識庫小於約 200,000 tokens（約 500 頁）時，可以直接整份放進 prompt。

## 相關概念
[[contextual-retrieval]] · [[chunking]] · [[hybrid-search]] · [[reranking]] · [[embedding]]
