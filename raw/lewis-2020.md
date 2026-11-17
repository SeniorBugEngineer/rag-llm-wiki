# Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks

| 欄位 | 值 |
|---|---|
| id | lewis-2020 |
| title | Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks |
| authors | Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih, Tim Rocktäschel, Sebastian Riedel, Douwe Kiela |
| year | 2020 |
| venue | NeurIPS 2020 |
| url | https://arxiv.org/abs/2005.11401 |
| abstract 來源 | arXiv API（export.arxiv.org）原文 |
| 內文來源 | ar5iv.labs.arxiv.org/html/2005.11401 |
| fetched | 2026-11-17 |
| C1 核實 | PASS：標題／第一作者／年份與書單一致 |

## Abstract（原文）

> Large pre-trained language models have been shown to store factual knowledge in their parameters, and achieve state-of-the-art results when fine-tuned on downstream NLP tasks. However, their ability to access and precisely manipulate knowledge is still limited, and hence on knowledge-intensive tasks, their performance lags behind task-specific architectures. Additionally, providing provenance for their decisions and updating their world knowledge remain open research problems. Pre-trained models with a differentiable access mechanism to explicit non-parametric memory can overcome this issue, but have so far been only investigated for extractive downstream tasks. We explore a general-purpose fine-tuning recipe for retrieval-augmented generation (RAG) -- models which combine pre-trained parametric and non-parametric memory for language generation. We introduce RAG models where the parametric memory is a pre-trained seq2seq model and the non-parametric memory is a dense vector index of Wikipedia, accessed with a pre-trained neural retriever. We compare two RAG formulations, one which conditions on the same retrieved passages across the whole generated sequence, the other can use different passages per token. We fine-tune and evaluate our models on a wide range of knowledge-intensive NLP tasks and set the state-of-the-art on three open domain QA tasks, outperforming parametric seq2seq models and task-specific retrieve-and-extract architectures. For language generation tasks, we find that RAG models generate more specific, diverse and factual language than a state-of-the-art parametric-only seq2seq baseline.

## 內文擷取筆記（[章節] 事實；數字照原文）

- [Methods] Retriever 為 DPR bi-encoder（BERT-base 查詢／文件編碼器）；Generator 為 BART-large（約 400M 參數）。
- [Methods] 兩種形式：RAG-Sequence 整段輸出使用同一份檢索文件；RAG-Token 每個輸出 token 可使用不同文件，能綜合多份文件內容。
- [Methods] 論文把模型內部參數稱為 parametric memory，外部可檢索的文件索引稱為 non-parametric memory。
- [Experimental Setup] 知識來源：2018 年 12 月 Wikipedia dump，切成不重疊的 100 字 chunk，約 21M 份文件，以 FAISS（HNSW 近似）搜尋。
- [Appendix A] 訓練時 k ∈ {5, 10}；開放域 QA 測試時 RAG-Token 取 15 份、RAG-Sequence 取 50 份。
- [Table 1] Exact Match：NQ — T5-11B（閉卷）34.5、T5-11B+SSM 36.6、RAG-Token 44.1、RAG-Sequence 44.5；WQ — T5-11B+SSM 44.7、RAG-Seq 45.2；TQA(Wiki) — T5-11B+SSM 60.5、RAG-Seq 68.0。
- [Index hot-swapping] 用 2016 與 2018 兩份索引詢問 82 位職位有變動的世界領袖：索引年份相符時正確率 70%／68%；不相符時只有 12%／4% → 只要換索引就能更新知識，不需重新訓練。
- [Human evaluation, Jeopardy] 452 組比較：RAG 較符合事實 42.7%，BART 較符合 7.1%；RAG 較具體 37.4%，BART 16.8%。
- [Broader Impact] 外部知識來源「will probably never be entirely factual and completely devoid of bias」。
- [Appendix H] 部分任務（如故事生成）出現 retrieval collapse：檢索器不論輸入都回傳相同文件。
