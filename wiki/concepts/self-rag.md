---
title: Self-RAG（自我反思檢索）
type: concept
sources: [asai-2023, gao-2023]
updated: 2026-11-17
---
# Self-RAG（自我反思檢索）

## 白話定義
讓模型**自己判斷要不要查資料**，並在回答後**自我檢查**：資料相關嗎？答案有被資料支持嗎？答案有用嗎？

## 為什麼重要
傳統 RAG 每次都固定檢索 k 份資料，不管需不需要；不相關的資料反而會讓回答變差（[[asai-2023]]）。

## 怎麼運作：四種 reflection tokens（[[asai-2023]]）
| Token | 問題 | 值 |
|---|---|---|
| Retrieve | 需要查資料嗎？ | yes／no／continue |
| IsRel | 資料相關嗎？ | relevant／irrelevant |
| IsSup | 答案有被支持嗎？ | fully／partially／no support |
| IsUse | 答案有用嗎？ | 5～1 |

流程：判斷 Retrieve → 若要查，就對每段資料平行生成候選答案 → 用 IsRel、IsSup、IsUse 打分 → 選出最佳片段。

## 效果（[[asai-2023]]）
- PopQA：Self-RAG 13B 55.8，加檢索的 ChatGPT 50.8，不檢索的 ChatGPT 29.3。
- 傳記事實分數：Self-RAG 7B 81.2，ChatGPT 71.8。
- 不是所有指標都贏：長文引用 recall 71.3，低於加檢索 ChatGPT 的 76.6。

## 在地圖上的位置
屬於 [[modular-rag]] 中的 **adaptive retrieval**（[[gao-2023]]）。

## 相關概念
[[modular-rag]] · [[hallucination]] · [[evaluation]]
