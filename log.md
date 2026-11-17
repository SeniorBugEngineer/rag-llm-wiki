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
