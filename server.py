from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import os

app = FastAPI()

# 允許 React 跨域請求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 自動判定資料庫路徑
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, "cargo.db")

@app.get("/")
def health_check():
    return {"status": "ok", "db_path": db_path, "db_exists": os.path.exists(db_path)}

@app.get("/api/track")
def track_shipment(q: str):
    if not q:
        raise HTTPException(status_code=400, detail="請提供查詢號碼")
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM shipments WHERE tid = ? OR cid = ? OR taxid = ?", (q, q, q))
    row = cur.fetchone()
    conn.close()
    
    if row:
        # 將資料庫結果轉為 JSON
        data = dict(row)
        # 處理歷史軌跡字串轉為列表
        data['history'] = [item.strip() for item in data['history'].split(';')]
        return data
    else:
        raise HTTPException(status_code=404, detail="查無此貨件")

if __name__ == "__main__":
    import uvicorn
    # 讀取環境變數中的 Port，這是雲端平台要求的
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
