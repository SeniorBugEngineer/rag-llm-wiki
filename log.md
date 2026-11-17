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
| 2026-11-17 13:01 | C4 投影片出處（r1） | PASS | 18 張，16 張內容頁皆有 data-src 且檔案存在；13 個 concept 全部被引用，0 warning。輸出：runs/*-C4-r1.txt | 進行語意數字核對 |
| 2026-11-17 13:01 | C4-數字核對（臨時語意檢查） | PASS | 每張投影片上的數字是否出現在其 data-src 頁面：第一版腳本誤報 12 張（卡片編號、座標軸、HTML 文字黏連），修正腳本後剩 2 筆，皆非錯誤（第 8 張示意向量已標「示意」；第 18 張為卡片編號） | — |
| 2026-11-17 13:01 | C5 瀏覽器（r1） | FAIL | headless Edge 截圖：(1) 桌面版段落標籤被 overflow 裁掉不見 (2) 手機寬度出處連結（absolute）蓋到內文 (3) 手機寬度疑似橫向溢出 | 只修 CSS：標籤改為卡內懸掛式、出處改為 flex 底部、deck 改 minmax(0,1fr) |
| 2026-11-17 13:01 | C5 瀏覽器（r2） | PASS（含一次誤判） | (3) 經量測為工具假象：headless 視窗最小寬度 496px，非頁面溢出（doc 481 ≤ inner 496，各 slide scrollWidth=clientWidth）；改用 400px iframe 實測 #5/#13/#15 正常。另修第 15 張表格多餘垂直捲軸 | — |
| 2026-11-17 13:01 | C5 新手通讀 | 修正 2 處、保留 1 處 | 第 5 張「top-K」補白話；第 5 張英國首相例子 Wiki 無出處 → 標「示意」；「token」一詞未解釋，但 Wiki 無定義，依「無出處不寫」規則保留，記為 Wiki 待補 | 重跑 C4 PASS（runs/*-C4-r2.txt） |
| 2026-11-17 13:03 | 反思統計 | — | FAIL 次數：C1 取得資料 3；語意錯誤（結構檢查放行、臨時檢查才抓到）2（C2-人工抽查 1、C3-語意 1）；C5 版面 1；C2 sources 階段 1（設計上預期） | 決定 v2：C1 預檢前移、語意檢查正式化並前移到 Wiki 撰寫 |
| 2026-11-17 13:03 | v2 TDD：check_claims.py | PASS | 新增 9 個測試（含 1 個發現實作錯誤：num-ok 清單把千分位逗號當分隔符）；全部 22 測試通過 | — |
| 2026-11-17 13:03 | v2 首次執行 C2+/C3+/C4+ | FAIL→PASS | C2+ 抓到 3 頁單位換算（2,100 萬、170 萬）、C4+ 抓到第 8 張示意向量；C3+ PASS。皆為刻意改寫，以 `<!-- num-ok -->` 明確標註後重跑 C2+/C3+/C4+/C2/C4 全部 PASS（runs/*-v2*.txt） | — |
| 2026-11-17 13:05 | process.html 生成 + C5 | FAIL→PASS | build_process.py 從 log.md／WORKFLOW.md 產生；截圖發現 v1/v2 並排時 v2 圖過小難讀，且 mermaid 把 `raw/<id>.md` 的 <id> 當 HTML 標籤吃掉 | 圖改上下排列、改用 mermaid 跳脫 #lt;id#gt;，重建後截圖正常 |
| 2026-11-17 13:14 | 發布 | FAIL→PASS | 第一次 git push 認證失敗（GitHub 不支援密碼）→ 使用者登入後推送成功；設定 Pages（main /docs）。curl 確認 index.html 與 process.html 皆 HTTP 200，簡報 18 張 slide | — |
