---
title: Contextual Retrieval（情境化檢索）
type: concept
sources: [anthropic-2024]
updated: 2026-11-17
---
# Contextual Retrieval（情境化檢索）

## 白話定義
在把 chunk 存進索引前，**先請 LLM 幫每個 chunk 寫一小段背景說明**（它出自哪份文件、在講什麼），讓 chunk 不再「斷章取義」。

## 為什麼重要
[[chunking]] 會讓 chunk 失去上下文：「The company's revenue grew by 3%」單獨看，不知道是哪家公司、哪一季，檢索時就找不到它（[[anthropic-2024]]）。

## 怎麼運作
1. 把整份文件和某個 chunk 一起給 LLM，請它寫「a short succinct context to situate this chunk within the overall document」，通常 50–100 tokens。
2. 把這段背景加在 chunk 前面。
3. 用加了背景的 chunk 同時建立：向量索引（Contextual Embeddings）與 BM25 索引（Contextual BM25）。這就是 [[hybrid-search]]。
4. 再搭配 [[reranking]]。
5. 用 prompt caching，整份文件只需快取一次；成本約每百萬文件 tokens 1.02 美元，而且只需付一次。

## 效果（top-20 檢索失敗率，基準 5.7%）
- + Contextual Embeddings → 3.7%（−35%）
- + Contextual BM25 → 2.9%（−49%）
- + Reranking → 1.9%（−67%）

「All these benefits stack」：效果可以疊加（[[anthropic-2024]]）。

## 相關概念
[[chunking]] · [[embedding]] · [[hybrid-search]] · [[reranking]]
