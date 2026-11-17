# 簡報大綱：RAG 是什麼？給新手的檢索增強生成入門

規則：每個論點行（`- ` 開頭）都必須標 `src:`，指向支撐它的 Wiki 頁。

## 1. 封面（cover）
RAG 是什麼？讓 AI 先查資料再回答｜18 頁｜知識來源：RAG LLM Wiki

## 段落一：為什麼需要 RAG

## 2. LLM 很厲害，但有三個老毛病
- 幻覺：自信地說出錯誤或沒根據的內容 src: wiki/concepts/hallucination.md
- 知識過時：訓練完就停在那一天 src: wiki/sources/gao-2023.md
- 不透明：無法說明答案從哪來 src: wiki/sources/gao-2023.md

## 3. 原因：知識都「背」在參數裡
- 模型參數 = parametric memory，難以精確取用、無法說明出處、難更新 src: wiki/sources/lewis-2020.md
- 比喻：閉書考，只能靠記憶 src: wiki/concepts/rag.md

## 段落二：RAG 是什麼

## 4. 一句話：先查資料，再回答
- 把閉書考變成開書考 src: wiki/concepts/rag.md
- 2020 年 Lewis 等人提出：參數記憶 + 可檢索的外部索引 src: wiki/sources/lewis-2020.md

## 5. RAG 三步驟流程圖
- Indexing：切 chunk → embedding → 向量資料庫 src: wiki/concepts/rag.md
- Retrieval：問題轉向量，找 top-K 相似段落 src: wiki/concepts/rag.md
- Generation：問題 + 段落組成 prompt 給 LLM src: wiki/concepts/rag.md

## 6. RAG 帶來什麼好處（用數字說話）
- NQ Exact Match：閉卷 T5 34.5 → RAG 44.5 src: wiki/sources/lewis-2020.md
- 換索引就更新知識：年份相符 70%／68%，不符 12%／4% src: wiki/sources/lewis-2020.md
- 人工評估更符合事實：42.7% vs 7.1% src: wiki/concepts/hallucination.md

## 段落三：檢索怎麼做

## 7. Chunking：把文件切成小段
- 常見 100／256／512 tokens src: wiki/concepts/chunking.md
- 大 chunk 上下文多但雜訊多；小 chunk 精準但缺上下文 src: wiki/concepts/chunking.md

## 8. Embedding：意思相近 → 向量相近
- 文字轉成 768 維向量，用內積比相似度 src: wiki/concepts/embedding.md
- 段落向量事先算好存進索引（FAISS） src: wiki/sources/karpukhin-2020.md

## 9. 關鍵字 vs 語意：BM25 vs DPR
- NQ top-20：BM25 59.1 → DPR 78.4 src: wiki/sources/karpukhin-2020.md
- SQuAD 上 BM25 反而較好（字面重疊高） src: wiki/concepts/retrieval.md
- 結論：各有盲點 → 之後的 hybrid search src: wiki/concepts/hybrid-search.md

## 段落四：常見陷阱

## 10. 陷阱一：chunk 斷章取義
- 「The company's revenue grew by 3%」是哪家公司？ src: wiki/concepts/contextual-retrieval.md

## 11. 陷阱二：Lost in the Middle
- U 形曲線：開頭 75.8%、中間 53.8%、不給文件 56.1% src: wiki/concepts/lost-in-the-middle.md
- 20 → 50 份文件只多約 1.5% src: wiki/sources/liu-2023.md

## 段落五：怎麼改良

## 12. Contextual Retrieval：先替 chunk 補上背景
- LLM 為每個 chunk 寫 50–100 tokens 背景說明 src: wiki/concepts/contextual-retrieval.md
- 一次性成本約每百萬 tokens 1.02 美元 src: wiki/sources/anthropic-2024.md

## 13. Hybrid search + Reranking：效果可以疊加
- 失敗率 5.7% → 3.7% → 2.9% → 1.9%（−67%） src: wiki/sources/anthropic-2024.md
- Rerank：先撈 150 個，再精選 20 個 src: wiki/concepts/reranking.md
- embeddings + BM25 優於只用 embeddings src: wiki/concepts/hybrid-search.md

## 14. 地圖：Naive → Advanced → Modular RAG
- Naive：基本三步驟 src: wiki/concepts/modular-rag.md
- Advanced：檢索前改寫查詢、檢索後 rerank src: wiki/concepts/modular-rag.md
- Modular：模組可替換重組，可自適應檢索 src: wiki/sources/gao-2023.md

## 段落六：進階變體

## 15. Self-RAG：自己決定要不要查、自己檢查
- 四種 reflection tokens：Retrieve、IsRel、IsSup、IsUse src: wiki/concepts/self-rag.md
- PopQA：55.8 vs 加檢索 ChatGPT 50.8；但不是每項都贏 src: wiki/sources/asai-2023.md

## 16. GraphRAG：回答「整份資料在講什麼」
- 知識圖譜 → 分群 → 社群摘要 → map-reduce src: wiki/concepts/graphrag.md
- 完整性勝率 72–83%；向量 RAG 較直接 src: wiki/sources/edge-2024.md

## 段落七：怎麼知道好不好

## 17. RAGAS 三指標
- Faithfulness、Answer Relevance、Context Relevance src: wiki/concepts/evaluation.md
- 不需要標準答案；與人工一致率 0.95／0.78／0.70 src: wiki/sources/es-2023.md

## 18. 總結 + 自我檢測（summary）
- 重點回顧：先查再答、切塊與向量、注意擺放位置、加背景與 rerank、分開評估檢索與生成 src: wiki/index.md
- Q1：為什麼答案放中間反而比不給資料還差？ src: wiki/concepts/lost-in-the-middle.md
- Q2：BM25 和向量檢索各擅長什麼？ src: wiki/concepts/hybrid-search.md
- Q3：Faithfulness 在量什麼？ src: wiki/concepts/evaluation.md
