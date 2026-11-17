---
title: 檢索（Retrieval）
type: concept
sources: [karpukhin-2020, lewis-2020, gao-2023, liu-2023]
updated: 2026-11-17
---
# 檢索（Retrieval）

## 白話定義
從一大堆文件中，**找出和問題最相關的幾段**。它是 RAG 的「R」。

## 為什麼重要
檢索找錯，後面生成得再好也沒用。Gao 等人指出 Naive RAG 的第一個缺點就是檢索的精確率與召回率不足（[[gao-2023]]）。

## 兩大類做法
| | 稀疏檢索（Sparse） | 稠密檢索（Dense） |
|---|---|---|
| 代表 | TF-IDF、BM25 | DPR |
| 比對方式 | 關鍵字是否出現 | 語意向量是否相近（[[embedding]]） |
| 強項 | 專有名詞、字面精準比對 | 同義改寫、語意相近 |

把兩者結合就是 [[hybrid-search]]。

## 出處說法
- [[karpukhin-2020]]：Dense 檢索 top-20 正確率在 Natural Questions 上從 BM25 的 59.1 提升到 78.4；但在字面重疊高的 SQuAD 上 BM25 仍較好。
- [[lewis-2020]]：RAG 用 DPR 從約 2,100 萬個 Wikipedia 段落中<!-- num-ok: 2,100 = 原文 21M -->檢索 k 份文件。
- [[liu-2023]]：檢索數量不是越多越好，從 20 份加到 50 份，GPT-3.5-Turbo 只進步約 1.5%。

## 相關概念
[[embedding]] · [[hybrid-search]] · [[reranking]] · [[chunking]] · [[rag]]
