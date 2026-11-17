---
title: 幻覺（Hallucination）
type: concept
sources: [gao-2023, lewis-2020, asai-2023, es-2023]
updated: 2026-11-17
---
# 幻覺（Hallucination）

## 白話定義
LLM 用很有自信的語氣，說出**錯誤或沒有根據**的內容。

## 為什麼重要
這是 RAG 想解決的第一個問題。Gao 等人把它和「知識過時」「推理不透明、無法追溯」並列為 LLM 的三大挑戰（[[gao-2023]]）。

## 怎麼發生
- 模型只靠參數裡記住的知識（parametric memory）回答，而這些知識難以精確取用、無法說明出處（[[lewis-2020]]）。
- 即使有檢索，Naive RAG 仍可能產生檢索內容不支持的答案（[[gao-2023]]）。

## 出處說法
- [[lewis-2020]]：RAG 生成的內容比純參數模型更符合事實（人工評估 42.7% vs 7.1%）。
- [[asai-2023]]：Self-RAG 用 IsSup token 讓模型自我檢查「答案有沒有被資料支持」。
- [[es-2023]]：RAGAS 的 Faithfulness 指標專門量測回答中有多少比例被檢索內容支持。

## 相關概念
[[rag]] · [[self-rag]] · [[evaluation]]
