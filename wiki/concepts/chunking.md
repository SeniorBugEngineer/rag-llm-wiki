---
title: Chunking（切塊）
type: concept
sources: [gao-2023, anthropic-2024, karpukhin-2020, edge-2024]
updated: 2026-11-17
---
# Chunking（切塊）

## 白話定義
把長文件**切成小段**（chunk），每段分別建索引。檢索時找的是「段」，不是整份文件。

## 為什麼重要
LLM 的上下文有限，也不需要整份文件；但切得不好，會切斷句子或讓段落失去上下文。

## 怎麼做 & 取捨
- 常見做法：固定長度，例如 100／256／512 tokens（[[gao-2023]]）。
- **大 chunk**：上下文多，但雜訊多、成本高；**小 chunk**：精準，但可能缺上下文（[[gao-2023]]）。
- 改良：sliding window（重疊切）、Small2Big（用句子檢索，再附上前後文）（[[gao-2023]]）。

## 出處說法
- [[karpukhin-2020]]：Wikipedia 切成 21,015,324 個不重疊的 100 字段落，並加上條目標題。
- [[anthropic-2024]]：chunk 會失去上下文，例如「The company's revenue grew by 3%」不知道是哪家公司 → 解法見 [[contextual-retrieval]]。
- [[edge-2024]]：GraphRAG 用 600-token chunk；chunk 越大，LLM 抽出的實體越少（600 tokens 時約為 2,400 tokens 時的兩倍）。

## 相關概念
[[embedding]] · [[contextual-retrieval]] · [[retrieval]] · [[graphrag]]
