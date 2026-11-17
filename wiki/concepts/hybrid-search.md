---
title: 混合檢索（Hybrid Search）
type: concept
sources: [anthropic-2024, karpukhin-2020, gao-2023]
updated: 2026-11-17
---
# 混合檢索（Hybrid Search）

## 白話定義
**同時用「關鍵字比對」（BM25）和「語意向量」（embedding）兩種方法檢索**，再把結果合併。

## 為什麼重要
兩種方法各有盲點：向量檢索擅長同義改寫，但可能漏掉精確的專有名詞或代碼；BM25 擅長字面精準比對，但遇到換句話說就找不到。

## 出處說法
- [[karpukhin-2020]]：Dense 檢索在多數資料集贏過 BM25，但在問題和段落字面重疊高的 SQuAD 上，BM25 反而較好（68.8 vs 63.2）。
- [[anthropic-2024]]：重點結論之一是「embeddings + BM25 優於只用 embeddings」；加入 Contextual BM25 後，失敗率從只用 Contextual Embeddings 的 3.7% 降到 2.9%。
- [[gao-2023]]：hybrid retrieval 列為 Advanced／Modular RAG 的技巧之一。

## 相關概念
[[retrieval]] · [[embedding]] · [[contextual-retrieval]] · [[reranking]]
