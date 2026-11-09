# 政大周邊吃飯地圖

收錄政大正門周邊與校園內的十家正餐店。可以按飯類、麵食、水餃、咖哩與素食篩選，再進店家頁看餐點、地址、導航和來源。首頁是街區示意，實際路線請點 Google Maps。

## 預覽與開發

解壓後用瀏覽器開啟 index.html。更新資料時先讀 [AGENTS.md](AGENTS.md)，修改 data/restaurants.json，再執行 `python3 build.py`。Python 只在生成頁面時使用，瀏覽網站時不需要。

## 發布 GitHub Pages

1. 建立公開 Repository，名稱可用 nccu-food-map。
2. 將解壓後的檔案和資料夾上傳到根目錄，保留 assets、data 和 shops 的結構。
3. Settings → Pages → Deploy from a branch → main → /(root) → Save。
4. 從 Visit site 開啟網站，確認分類篩選、店家頁和導航連結。

## 擴充示範

建立九家店的版本後，依 AGENTS.md 在資料陣列末尾加入小確幸，再執行 build.py。首頁增加咖哩分類下的標記與卡片，並生成 shops/little-happiness.html。第十一家店可以走相同流程，讓三處內容沿用同一筆資料。
