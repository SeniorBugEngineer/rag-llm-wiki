# Dense Passage Retrieval for Open-Domain Question Answering

| 欄位 | 值 |
|---|---|
| id | karpukhin-2020 |
| title | Dense Passage Retrieval for Open-Domain Question Answering |
| authors | Vladimir Karpukhin, Barlas Oğuz, Sewon Min, Patrick Lewis, Ledell Wu, Sergey Edunov, Danqi Chen, Wen-tau Yih |
| year | 2020 |
| venue | EMNLP 2020 |
| url | https://arxiv.org/abs/2004.04906 |
| abstract 來源 | arXiv API（export.arxiv.org）原文 |
| 內文來源 | ar5iv.labs.arxiv.org/html/2004.04906 |
| fetched | 2026-11-17 |
| C1 核實 | PASS：標題／第一作者／年份與書單一致 |

## Abstract（原文）

> Open-domain question answering relies on efficient passage retrieval to select candidate contexts, where traditional sparse vector space models, such as TF-IDF or BM25, are the de facto method. In this work, we show that retrieval can be practically implemented using dense representations alone, where embeddings are learned from a small number of questions and passages by a simple dual-encoder framework. When evaluated on a wide range of open-domain QA datasets, our dense retriever outperforms a strong Lucene-BM25 system largely by 9%-19% absolute in terms of top-20 passage retrieval accuracy, and helps our end-to-end QA system establish new state-of-the-art on multiple open-domain QA benchmarks.

## 內文擷取筆記（[章節] 事實；數字照原文）

- [Dual encoder] 兩個獨立的 BERT（base, uncased）分別編碼問題與段落，取 [CLS] 得 768 維向量；相似度 = 兩向量內積 sim(q,p)=E_Q(q)ᵀE_P(p)。
- [Training] in-batch negatives：同一批次其他問題的正確段落當負例，批次大小 128；再加 1 個 BM25 hard negative（字面很像但不含答案）可大幅提升，加 2 個沒有更好。
- [Passages] 2018-12-20 英文 Wikipedia，切成不重疊的 100 字段落並加上條目標題，共 21,015,324 段。
- [Run-time efficiency] 以 FAISS 建索引；DPR 每秒約 995 個問題，BM25/Lucene 每 CPU 執行緒每秒約 23.7 個。代價：計算 embedding 約 8.8 小時（8 GPU）、建 FAISS 索引約 8.5 小時；Lucene 索引約 30 分鐘。
- [Table 2] Top-20 檢索正確率（BM25 → DPR）：NQ 59.1 → 78.4；TriviaQA 66.9 → 79.4；WebQuestions 55.0 → 73.2；CuratedTREC 70.9 → 79.8；SQuAD 68.8 → 63.2（BM25 勝）。
- [Analysis] SQuAD 上 BM25 較好：標註者看著段落出題，問題與段落字面重疊高；資料只來自 500 多篇條目，分布偏差大。
- [Sample efficiency] NQ 上只用 1,000 筆訓練資料，DPR 就已超過 BM25。
