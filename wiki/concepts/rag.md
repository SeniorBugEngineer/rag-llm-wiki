---
title: RAG（檢索增強生成）
type: concept
sources: [lewis-2020, gao-2023, anthropic-2024]
updated: 2026-11-17
---
# RAG（檢索增強生成）

## 白話定義
**先查資料，再回答**。RAG（Retrieval-Augmented Generation）讓 LLM 回答前，先從外部資料庫找出相關段落，再把這些段落和問題一起交給模型生成答案。就像把「閉書考」變成「開書考」。

## 為什麼重要
- 減少 [[hallucination]]：答案有資料可依據。
- 知識可以更新：換掉資料庫就好，不必重新訓練模型。Lewis 等人換用 2016／2018 的 Wikipedia 索引，模型就能回答對應年份的世界領袖（[[lewis-2020]]）。
- 可以用在私有、模型沒看過的資料上（[[gao-2023]]）。

## 怎麼運作（三步驟）
1. **Indexing（建索引）**：把文件切成小段（[[chunking]]），轉成向量（[[embedding]]），存進向量資料庫。
2. **Retrieval（檢索）**：把問題也轉成向量，找出最相似的 top-K 段落（[[retrieval]]）。
3. **Generation（生成）**：把「問題＋檢索到的段落」組成 prompt，交給 LLM 回答。

（[[gao-2023]] 稱此基本流程為 Naive RAG 的「Retrieve-Read」。）

## 出處說法
- [[lewis-2020]]：最早提出 RAG，結合 parametric memory（模型參數）與 non-parametric memory（Wikipedia 向量索引）；在 Natural Questions 上 Exact Match 從閉卷 T5 的 34.5 提升到 44.5。
- [[gao-2023]]：RAG 的發展分為 Naive → Advanced → Modular 三種範式（見 [[modular-rag]]）。
- [[anthropic-2024]]：知識庫小於約 200,000 tokens（約 500 頁）時，可以直接整份放進 prompt，不必用 RAG。

## 相關概念
[[retrieval]] · [[embedding]] · [[chunking]] · [[modular-rag]] · [[hallucination]] · [[evaluation]]
