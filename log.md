# 執行紀錄（append-only）

時間為 Asia/Taipei。腳本原始輸出存放於 [runs/](runs/)。

| 時間 | 節點 | 結果 | 原因 | 處置 |
|---|---|---|---|---|
| 2026-11-17 12:46 | 設計 | PASS | spec、plan 完成；check_wiki/check_slides 13 個單元測試通過 | 進入 ingest |
| 2026-11-17 12:49 | C1 取得資料 | FAIL | WebFetch 摘要模型拒絕回傳 arXiv abstract 原文（著作權引用上限），只給轉述，不符「raw 存 abstract 原文」規定 | 改用 arXiv 官方 API（export.arxiv.org/api/query）直接下載 7 篇 abstract |
| 2026-11-17 12:49 | C1 取得資料 | FAIL | arXiv API 以 http:// 呼叫回傳 0 bytes（被轉址未跟隨） | 改 https + 跟隨轉址，HTTP 200，7 筆 entry 解析成功 |
| 2026-11-17 12:49 | C1 取得資料 | FAIL | 5 篇（lewis/karpukhin/liu/asai/es）抓 PDF 只得到壓縮二進位，無可讀文字；本機 Read 工具缺 pdftoppm 也無法渲染 | 改抓 HTML 版：ar5iv（2020/2023 舊論文）與 arxiv.org/html，5 篇全部取得內文。注意：計畫寫的後備順序是 abs→html→pdf，實際執行時先試了 pdf，順序錯誤浪費一輪 |
| 2026-11-17 12:49 | C1 來源核實 | PASS | 8 篇標題、第一作者、年份與書單一致（arXiv API metadata + 頁面標題雙重比對）；anthropic-2024 標題 "Introducing Contextual Retrieval"、2024-09-19 | 寫入 raw/ |
| 2026-11-17 12:52 | C2 check_wiki（sources 階段） | FAIL | 64 錯誤：58 broken link（13 個 concept slug 尚未建立，預期內）+ 7 orphan（source 頁只被 index 引用）。輸出：runs/20261117-1252-C2-sources.txt | 進入 Task 5 建立 concept 頁 |
| 2026-11-17 12:54 | C2 check_wiki（r1） | PASS | 13 concept 頁 + index 建立後 21 頁 0 錯誤，一次通過。輸出：runs/*-C2-r1.txt | — |
| 2026-11-17 12:54 | C2-數字核對（臨時加的語意檢查） | PASS（3 筆待人工確認） | C2 只驗結構、驗不到內容；臨時寫一次性腳本比對 wiki 中所有 ≥3 位數字是否出現在 raw/。未匹配 3 筆皆為單位換算（21M→2,100 萬、1.7M→170 萬），非錯誤 | 記為 v2 候選：把數字核對做成正式檢查 |
| 2026-11-17 12:54 | C2-人工抽查 | FAIL→修正 | lost-in-the-middle.md 把 gao-2023「放到 prompt 邊緣」寫成「排在最前面」，引用歸屬不精確 | 改寫為分開歸屬；重跑 C2 PASS（runs/*-C2-r2.txt） |
| 2026-11-17 12:55 | C3 大綱覆蓋（r1） | PASS | 18 張、所有論點行都有 src 且檔案存在。輸出：runs/*-C3-r1.txt | 進行語意抽查 |
| 2026-11-17 12:55 | C3-語意抽查 | FAIL | 改用腳本逐行檢查（取代人工抽 5 點）：論點中的數字與英文術語是否出現在被引用頁面。第 27 行「top-K」引用 retrieval.md，但該頁沒有此內容（top-K 寫在 rag.md）→ C3 只驗「檔案存在」，驗不到「頁面是否支持論點」 | 改引用 rag.md；重跑 C3 PASS、語意檢查 0 筆（runs/*-C3-r2.txt）。記為 v2 候選：把語意檢查正式化 |
