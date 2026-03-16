import pandas as pd
import sqlite3
import os

# 設定路徑
base_path = os.path.expanduser("~/Desktop/JennyCargo_System")
excel_path = os.path.join(base_path, "cargo_data.xlsx")
db_path = os.path.join(base_path, "cargo.db")

# 1. 建立 Excel 範本資料
data = {
    '貨態單號(TID)': ['TID20260316001', 'TID20260316002'],
    '客戶編號(CID)': ['CUST001', 'CUST002'],
    '公司統編(TaxID)': ['12345678', '87654321'],
    '收件人': ['林小姐', '陳先生'],
    '當前狀態': ['運送中', '已簽收'],
    '當前位置': ['台北轉運站', '台中門市'],
    '預計抵達時間': ['2026-03-17 14:00', '2026-03-16 10:30'],
    '簽收人姓名': ['', '陳大文'],
    '歷史軌跡(請用分號隔開)': [
        '2026-03-15 08:00 收到貨件;2026-03-16 12:00 抵達台北轉運站',
        '2026-03-14 10:00 收到貨件;2026-03-15 09:00 抵達台中門市;2026-03-16 10:30 已簽收'
    ]
}

df = pd.DataFrame(data)
df.to_excel(excel_path, index=False)
print(f"✅ 已建立 Excel 範本: {excel_path}")

# 2. 初始化資料庫
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 建立貨件主表
cursor.execute('''
CREATE TABLE IF NOT EXISTS shipments (
    tid TEXT PRIMARY KEY,
    cid TEXT,
    taxid TEXT,
    receiver TEXT,
    status TEXT,
    location TEXT,
    eta TEXT,
    signatory TEXT,
    history TEXT
)
''')

# 將 Excel 資料匯入資料庫
df.columns = ['tid', 'cid', 'taxid', 'receiver', 'status', 'location', 'eta', 'signatory', 'history']
df.to_sql('shipments', conn, if_exists='replace', index=False)

conn.commit()
conn.close()
print(f"✅ 已初始化 SQLite 資料庫並匯入資料: {db_path}")
