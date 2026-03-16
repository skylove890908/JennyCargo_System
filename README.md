# 📦 JennyCargo - 智能貨態追蹤平台

這是一個基於 **React** (前端) 與 **FastAPI** (後端) 開發的物流貨態查詢系統。

## 🌟 核心功能
- **多維度查詢**：支援 貨態單號 (TID)、客戶編號 (CID) 與 公司統編 (TaxID)。
- **即時追蹤**：視覺化呈現當前物流狀態與地理位置。
- **物流軌跡**：自動生成時間線形式的貨件運輸紀錄。
- **Excel 管理**：支援透過 Excel 檔案維護數據，並自動同步至資料庫。

## 🛠️ 技術棧
- **Frontend**: React (Vite), Tailwind CSS
- **Backend**: Python, FastAPI, SQLite
- **Tools**: Pandas (Data Processing)

## 🚀 快速啟動

### 1. 後端服務
```bash
python3 server.py
```

### 2. 前端介面
```bash
cd frontend
npm install
npm run dev
```

## 📝 資料維護
請直接修改 `cargo_data.xlsx` 並執行 `python3 sync_data.py` 即可同步至系統。

---
Developed by Jenny_First AI System.
