---
title: 重排序（Reranking）
type: concept
sources: [anthropic-2024, gao-2023, liu-2023]
updated: 2026-11-17
---
# 重排序（Reranking）

## 白話定義
**兩階段檢索**：先用快速的方法撈出一大批候選段落，再用較精準（但較慢）的 reranker 模型重新評分排序，只留下最好的幾段交給 LLM。

## 為什麼重要
- 第一階段要快，所以比較粗糙；reranker 能把真正相關的段落挑出來。
- 排序會影響 LLM 表現：最相關的內容應放在前面（見 [[lost-in-the-middle]]）。

## 怎麼運作（Anthropic 的設定）
1. 先檢索前 150 個 chunk。
2. 把「問題＋每個 chunk」交給 reranker 評分。
3. 留下前 20 個交給模型（[[anthropic-2024]]）。

## 出處說法
- [[anthropic-2024]]：加上 rerank 後，檢索失敗率從 2.9% 降到 1.9%（總降幅 67%）；代價是增加延遲。
- [[gao-2023]]：rerank 屬於 Advanced RAG 的「檢索後」最佳化，目的是把最相關內容放到 prompt 的邊緣。
- [[liu-2023]]：建議用 rerank 讓最相關文件排在前面，並適度截斷清單。

## 相關概念
[[retrieval]] · [[lost-in-the-middle]] · [[hybrid-search]] · [[contextual-retrieval]] · [[modular-rag]]
