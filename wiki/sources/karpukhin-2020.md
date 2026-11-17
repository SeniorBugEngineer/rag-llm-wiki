---
title: Dense Passage Retrieval for Open-Domain Question Answering
type: source
sources: [karpukhin-2020]
updated: 2026-11-17
url: https://arxiv.org/abs/2004.04906
authors: Vladimir Karpukhin et al.
year: 2020
---
# Dense Passage Retrieval for Open-Domain Question Answering

> Vladimir Karpukhin et al.（2020）｜原文：https://arxiv.org/abs/2004.04906｜擷取：`raw/karpukhin-2020.md`

## 一句話重點
證明「只用向量（dense embedding）做檢索」就能贏過傳統關鍵字檢索 BM25。這就是 RAG 裡「R」最常用的做法。

## 解決什麼問題
開放域問答以前靠 TF-IDF／BM25 這類比對關鍵字的稀疏方法；同義但用字不同的問題就找不到。

## 怎麼做
- **雙編碼器（dual encoder）**：一個 BERT 把問題變成 768 維向量，另一個 BERT 把段落變成向量，用**內積**當相似度。詳見 [[embedding]]。
- **訓練**：同一批次中其他問題的答案段落當作負例（in-batch negatives），再加 1 個「字面很像但沒有答案」的 BM25 段落當困難負例。
- **索引**：Wikipedia 切成 21,015,324 個 100 字段落，事先算好向量，用 FAISS 快速搜尋。詳見 [[retrieval]]、[[chunking]]。

## 關鍵結果
- Top-20 檢索正確率（BM25 → DPR）：Natural Questions 59.1 → 78.4；WebQuestions 55.0 → 73.2。
- 只要 1,000 筆訓練資料就已超過 BM25。
- 查詢速度：DPR 每秒約 995 題，BM25 每執行緒約 23.7 題；但建向量索引要花數小時（算 embedding 約 8.8 小時、建 FAISS 索引約 8.5 小時），Lucene 索引約 30 分鐘。

## 限制
在 SQuAD 上 BM25 反而較好（68.8 vs 63.2）：題目是看著段落出的，字面重疊高，關鍵字比對占優勢。這也是後來 [[hybrid-search]] 把兩者結合的理由。

## 相關概念
[[embedding]] · [[retrieval]] · [[hybrid-search]] · [[chunking]]
