---
title: RAG 的評估
type: concept
sources: [es-2023, gao-2023, edge-2024]
updated: 2026-11-17
---
# RAG 的評估

## 白話定義
判斷一個 RAG 系統好不好，要**分開檢查「找資料」和「寫答案」兩件事**。

## 為什麼重要
RAG 出錯可能是檢索沒找到、找到了但沒用好，或答案本身離題。只看最終答案，無法知道要修哪裡。

## RAGAS 三指標（[[es-2023]]）
| 指標 | 問的問題 | 怎麼算 |
|---|---|---|
| **Faithfulness**（忠實度） | 答案有沒有亂講？ | 把答案拆成陳述，被檢索內容支持的比例 |
| **Answer Relevance**（答案相關性） | 有沒有回答到問題？ | 從答案反推問題，和原問題的 [[embedding]] 相似度 |
| **Context Relevance**（上下文相關性） | 檢索的內容精不精準？ | 真正需要的句子 ÷ 檢索到的總句數 |

特點：**reference-free**，不需要人工標準答案。與人工判斷一致率：Faithfulness 0.95、Answer Relevance 0.78、Context Relevance 0.70。

## 綜述的觀點（[[gao-2023]]）
- 同樣三個品質分數，再加上四種能力：抗雜訊、會拒答（資料不夠時不亂答）、整合多文件、抗錯誤資訊。
- 作者指出這些指標尚未標準化。

## 其他做法
GraphRAG 用 LLM-as-a-judge 兩兩比較答案的完整性、多樣性等（[[edge-2024]]）。

## 相關概念
[[hallucination]] · [[rag]] · [[retrieval]]
