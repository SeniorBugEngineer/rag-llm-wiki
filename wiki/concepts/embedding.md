---
title: Embedding（向量表示）
type: concept
sources: [karpukhin-2020, gao-2023, anthropic-2024, es-2023]
updated: 2026-11-17
---
# Embedding（向量表示）

## 白話定義
把一段文字轉成一串數字（向量），讓**意思相近的文字，向量也相近**。電腦就能用「算距離」來判斷兩段文字像不像。

## 為什麼重要
這是 dense [[retrieval]] 的基礎。問題和文件都轉成向量後，檢索就變成「找最近的向量」。

## 怎麼運作
1. **編碼**：DPR 用兩個 BERT 模型，一個把問題轉成 768 維向量，一個把段落轉成 768 維向量（[[karpukhin-2020]]）。
2. **比相似度**：兩個向量做**內積**，數值越大越相關（[[karpukhin-2020]]）。
3. **事先建索引**：所有段落的向量先算好存起來（如 FAISS），查詢時只需算問題的向量（[[karpukhin-2020]]）。

## 出處說法
- [[karpukhin-2020]]：只用 1,000 筆訓練資料，向量檢索就能贏過 BM25；查詢速度每秒約 995 題，但建索引要花數小時。
- [[gao-2023]]：Naive RAG 的索引流程是 切 chunk → embedding → 存入向量資料庫。
- [[anthropic-2024]]：在 chunk 前加上背景說明再做 embedding（Contextual Embeddings），檢索失敗率降 35%。
- [[es-2023]]：RAGAS 的 Answer Relevance 也是用 embedding 相似度計算。

## 相關概念
[[retrieval]] · [[chunking]] · [[contextual-retrieval]] · [[hybrid-search]]
