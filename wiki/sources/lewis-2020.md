---
title: Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks
type: source
sources: [lewis-2020]
updated: 2026-11-17
url: https://arxiv.org/abs/2005.11401
authors: Patrick Lewis et al.
year: 2020
---
# Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks

> Patrick Lewis et al.（2020）｜原文：https://arxiv.org/abs/2005.11401｜擷取：`raw/lewis-2020.md`

## 一句話重點
RAG 這個名詞的起點：把「模型參數裡的知識」（parametric memory）和「可檢索的外部文件索引」（non-parametric memory）接在一起，讓模型先查資料再生成。

## 解決什麼問題
大型預訓練模型雖然把知識存在參數裡，但難以精確取用、無法說明答案出處，也很難更新知識。這些都是 [[hallucination]] 與知識過時的根源。

## 怎麼做
- **Retriever**：DPR bi-encoder（見 [[karpukhin-2020]]），在約 2,100 萬個 100 字 Wikipedia chunk 中找出最相關的 k 份。
- **Generator**：BART-large，把問題與檢索到的文件一起當輸入來生成答案。
- **兩種組合方式**：RAG-Sequence 整段答案用同一份文件；RAG-Token 每個字都可以參考不同文件。
- 詳見 [[rag]]、[[retrieval]]、[[embedding]]。

## 關鍵結果
- Natural Questions Exact Match：閉卷 T5-11B 34.5 → RAG-Sequence 44.5。
- **換索引就能更新知識**：用 2016 與 2018 兩份 Wikipedia 索引問 82 位換過人的世界領袖，年份相符時正確率約 70%／68%，不相符時只剩 12%／4%。
- 人工評估 Jeopardy 出題：RAG 被評為較符合事實 42.7%，BART 只有 7.1%。

## 限制
- 外部知識來源本身不可能完全正確、沒有偏誤。
- 某些任務（如故事生成）出現 retrieval collapse：不論輸入，檢索器都回傳同樣文件。

## 相關概念
[[rag]] · [[retrieval]] · [[embedding]] · [[hallucination]]
