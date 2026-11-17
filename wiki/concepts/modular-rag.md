---
title: RAG 三種範式：Naive／Advanced／Modular
type: concept
sources: [gao-2023, asai-2023]
updated: 2026-11-17
---
# RAG 三種範式：Naive／Advanced／Modular

## 白話定義
Gao 等人把 RAG 的演進整理成三代（[[gao-2023]]）：
| 範式 | 一句話 | 例子 |
|---|---|---|
| **Naive RAG** | 最基本的「建索引 → 檢索 → 生成」 | 基本 [[rag]] 流程 |
| **Advanced RAG** | 在檢索**前後**加最佳化 | 查詢改寫、[[hybrid-search]]、[[reranking]]、上下文壓縮 |
| **Modular RAG** | 把 RAG 拆成可替換、可重組的模組 | Search、Routing、Memory、RAG-Fusion、自適應檢索 |

## 為什麼重要
這張地圖幫助新手把各種 RAG 技術「歸位」：每個新技巧都是在改善某個步驟。

## Naive RAG 的問題（[[gao-2023]]）
- 檢索不準或漏掉關鍵資訊
- 仍會產生 [[hallucination]]
- 多份內容重複、拼接不連貫
- 一次檢索對複雜問題不夠

## 檢索流程的三種進階型態（[[gao-2023]]）
- **Iterative**：檢索與生成交替進行。
- **Recursive**：逐步細化查詢、拆解子問題。
- **Adaptive**：由模型自己決定要不要、何時檢索，例如 [[self-rag]]（[[asai-2023]]）。

## RAG vs Fine-tuning（[[gao-2023]]）
RAG 適合會變動的知識、可即時更新；fine-tuning 適合改變模型的行為、風格與格式。兩者可以互補。

## 相關概念
[[rag]] · [[reranking]] · [[hybrid-search]] · [[self-rag]] · [[graphrag]]
