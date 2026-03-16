import pandas as pd
import sqlite3
import os

base_path = os.path.expanduser("~/Desktop/JennyCargo_System")
excel_path = os.path.join(base_path, "cargo_data.xlsx")
db_path = os.path.join(base_path, "cargo.db")

def sync():
    if not os.path.exists(excel_path):
        print("❌ 找不到 Excel 檔案！")
        return

    print("🔄 正在從 Excel 同步資料到資料庫...")
    df = pd.read_excel(excel_path)
    
    # 統一欄位名稱
    df.columns = ['tid', 'cid', 'taxid', 'receiver', 'status', 'location', 'eta', 'signatory', 'history']
    
    conn = sqlite3.connect(db_path)
    df.to_sql('shipments', conn, if_exists='replace', index=False)
    conn.close()
    print("✅ 同步完成！現在資料庫與 Excel 同步了。")

if __name__ == "__main__":
    sync()
