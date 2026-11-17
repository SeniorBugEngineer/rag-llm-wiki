# RAG LLM Wiki + 教學 HTML 簡報：設計規格

日期：2026-11-17
狀態：已與使用者逐段討論並確認（先討論、後生成）

## 1. 目標

1. 建立主題為「RAG（檢索增強生成）」的 LLM Wiki，ingest 8 篇資料。
2. 只以該 Wiki 為知識來源，產生一份讓新手能理解 RAG 基本概念的教學型 HTML 簡報。
3. 用明確的 loop／graph 產生上述成果，並留下可驗證的執行與檢查紀錄，最後寫反思。

## 2. 決策紀錄

| 決策 | 選擇 | 理由 |
|---|---|---|
| 主題 | RAG | 公開資料多、概念層次清楚、與 LLM Wiki 本身相關 |
| 交付形式 | 本機 Markdown + GitHub Pages | Wiki 與簡報都有公開連結 |
| 資料來源 | 下方 8 篇書單 | 基礎 → 實務 → 進階 → 評估，完整教學弧線 |
| Graph 實作 | Claude Code 執行 LLM 節點 + Python 檢查腳本 | 不需要 API key；檢查可重跑、結果可驗證 |

## 3. 書單（ingest 對象）

| id | 資料 | 簡報角色 |
|---|---|---|
| lewis-2020 | Lewis et al. 2020, Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks, arXiv:2005.11401 | 起源與定義 |
| karpukhin-2020 | Karpukhin et al. 2020, Dense Passage Retrieval for Open-Domain Question Answering, arXiv:2004.04906 | 檢索：embedding、向量搜尋 |
| gao-2023 | Gao et al. 2023, Retrieval-Augmented Generation for Large Language Models: A Survey, arXiv:2312.10997 | Naive／Advanced／Modular RAG 地圖 |
| liu-2023 | Liu et al. 2023, Lost in the Middle: How Language Models Use Long Contexts, arXiv:2307.03172 | 長 context 的陷阱 |
| anthropic-2024 | Anthropic 2024, Introducing Contextual Retrieval | chunk 上下文、hybrid search、rerank |
| asai-2023 | Asai et al. 2023, Self-RAG, arXiv:2310.11511 | 自適應檢索、自我反思 |
| edge-2024 | Edge et al. 2024, From Local to Global: A Graph RAG Approach to Query-Focused Summarization, arXiv:2404.16130 | 全域問題、知識圖譜 |
| es-2023 | Es et al. 2023, RAGAS: Automated Evaluation of Retrieval Augmented Generation, arXiv:2309.15217 | 評估指標 |

每篇在 ingest 時必須取得原文並核實標題、作者、年份；無法核實時寫入 log.md，並且不得以記憶內容代替原文。

## 4. Repo 結構

```
rag-llm-wiki/
  raw/<id>.md            原文擷取 + metadata（url、取得時間、核實結果）
  wiki/sources/<id>.md   每篇摘要頁
  wiki/concepts/<slug>.md 概念頁（rag、retrieval、embedding、chunking、
                          hybrid-search、reranking、lost-in-the-middle、
                          contextual-retrieval、modular-rag、self-rag、
                          graphrag、evaluation 等）
  wiki/index.md          目錄
  log.md                 append-only 執行紀錄
  WORKFLOW.md            graph 規格（Mermaid）與版本變更
  scripts/check_wiki.py
  scripts/check_slides.py
  runs/                  每次檢查腳本的原始輸出
  docs/index.html        教學簡報（GitHub Pages）
  docs/process.html      作業說明頁
```

### Wiki 頁面格式

每頁開頭為 YAML frontmatter：`title`、`type`（source|concept）、`sources`（source id 清單，至少 1 個）、`updated`。內文用 `[[slug]]` 互相連結。source 頁另需 `url`、`authors`、`year`。

## 5. Graph（v1）

```
Wiki 迴圈（每篇一次）：
  取得資料 → 擷取原文 → [C1 來源核實] → 撰寫/更新 Wiki 頁 → [C2 check_wiki.py]
  C1 失敗 → 重抓／換版本（arXiv abs → html → pdf）
  C2 失敗 → 修正頁面 → 重跑 C2
全部通過後：
  查詢 Wiki → 簡報大綱 → [C3 大綱覆蓋：每點有 Wiki 出處] → 生成 HTML
  → [C4 check_slides.py] → [C5 瀏覽器開啟 + 人工通讀]
  C3 失敗 → 補查 Wiki 或刪除無出處論點
  C4/C5 失敗 → 只重做壞掉的投影片
```

### 檢查定義

- **C1 來源核實**：抓到的頁面標題／作者／年份與書單一致，且擷取文字非空。
- **C2 check_wiki.py**：frontmatter 欄位齊全；`sources` 指向存在的 `wiki/sources/<id>.md`；所有 `[[slug]]` 都能解析；index.md 列出所有頁面；沒有孤立頁面。
- **C3 大綱覆蓋**：大綱中每個論點都標註 Wiki 頁面，且該頁面存在。
- **C4 check_slides.py**：每張內容投影片（`<section class="slide">`，封面與總結除外）都有 `data-src`，且指向存在的 Wiki 頁；Wiki 中的關鍵概念頁至少被一張投影片引用（覆蓋率報告）；HTML 結構可被解析。
- **C5**：實際在瀏覽器開啟，確認翻頁、版面、手機寬度；人工通讀，確認新手是否看得懂。

所有檢查結果以「時間｜節點｜結果｜原因｜處置」寫入 log.md，腳本原始輸出存放在 runs/。

### v2 演進規則

v1 執行完後，統計 log.md 中各節點的失敗次數。把最常失敗節點的檢查往前移到更早的步驟，更新 WORKFLOW.md（保留 v1 與 v2 並列），並在 log.md 記錄修改理由。不得捏造失敗；若某檢查一次就通過，照實記錄。

## 6. 教學簡報結構（docs/index.html）

單一 HTML 檔、不依賴外部框架，用鍵盤←→或點擊翻頁，支援手機寬度與深淺色。每張內容投影片右下角以連結顯示「出處：wiki/…」。

| 段落 | 投影片 | 內容 | 出處 |
|---|---|---|---|
| 為什麼需要 RAG | 1–3 | 幻覺、知識截止、私有資料；開書考比喻 | lewis-2020 |
| RAG 是什麼 | 4–6 | 檢索→增強→生成流程圖；具體例子 | lewis-2020、rag |
| 檢索怎麼做 | 7–9 | chunking、embedding、相似度（圖解） | karpukhin-2020、embedding |
| 常見陷阱 | 10–11 | chunk 失去上下文、Lost in the Middle | liu-2023、anthropic-2024 |
| 怎麼改良 | 12–14 | Contextual Retrieval、hybrid、rerank；Naive→Advanced→Modular | anthropic-2024、gao-2023 |
| 進階變體 | 15–16 | Self-RAG、GraphRAG | asai-2023、edge-2024 |
| 評估 | 17 | RAGAS 三指標 | es-2023 |
| 總結 | 18 | 重點回顧 + 3 題自我檢測 | — |

規則：Wiki 沒有支撐的內容不寫進簡報。

## 7. 作業說明頁（docs/process.html）

依繳交項目順序：(1) 主題與簡介 (2) Wiki 連結 (3) 簡報連結 (4) graph 圖 v1/v2 + 文字說明（重複步驟、檢查與重生點、設計理由）(5) 實際執行紀錄（取自 log.md、連結 runs/）(6) 反思（最常出錯的節點、檢查前移到哪、workflow 修改與理由）。反思必須根據實際 log 撰寫。

## 8. 發布

使用者在 GitHub 網頁建立 Public 空 repo `rag-llm-wiki` 並提供網址；由 Claude commit 並 push；使用者在 Settings → Pages 選擇 `main` / `/docs`。之後把 process.html 與 index.html 中的連結更新為實際網址。

## 9. 不做的事（YAGNI）

- 不建向量資料庫、不實作真的 RAG 系統。
- 不使用 LangGraph 或 Claude API。
- 不使用簡報框架（reveal.js 等）。
