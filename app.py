import streamlit as st
import sqlite3
import os

base_path = os.path.expanduser("~/Desktop/JennyCargo_System")
db_path = os.path.join(base_path, "cargo.db")

st.set_page_config(page_title="JennyCargo 貨態查詢平台", page_icon="📦")

st.title("📦 JennyCargo 貨態查詢平台")
st.write("請輸入您的客戶編號、統編或貨態單號進行查詢")

# 查詢介面
query_input = st.text_input("輸入查詢號碼", placeholder="例如: TID20260316001")

if query_input:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    # 搜尋三個欄位
    cur.execute("SELECT * FROM shipments WHERE tid = ? OR cid = ? OR taxid = ?", (query_input, query_input, query_input))
    row = cur.fetchone()
    conn.close()
    
    if row:
        st.success("✅ 已找到您的貨件資料")
        
        # 顯示主要資訊
        col1, col2 = st.columns(2)
        with col1:
            st.metric("當前狀態", row['status'])
            st.write(f"**當前位置:** {row['location']}")
        with col2:
            st.metric("預計抵達", row['eta'])
            if row['signatory']:
                st.write(f"**簽收人:** {row['signatory']}")

        # 顯示歷史軌跡
        st.subheader("📍 貨態軌跡")
        history_list = row['history'].split(";")
        for item in history_list:
            st.info(item.strip())
            
    else:
        st.error("❌ 查無資料，請確認輸入是否正確。")

st.sidebar.markdown("---")
st.sidebar.info("💡 提示：您可以輸入 Excel 中的 TID、CID 或 TaxID 來測試。")
