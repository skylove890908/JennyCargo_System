from fastapi import FastAPI, HTTPException, Request, Header
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import os
import json
from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# LINE Bot 設定
line_secret = os.getenv('LINE_CHANNEL_SECRET')
line_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
configuration = Configuration(access_token=line_token)
handler = WebhookHandler(line_secret)

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

def get_shipment_data(q: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM shipments WHERE tid = ? OR cid = ? OR taxid = ?", (q, q, q))
    row = cur.fetchone()
    conn.close()
    if row:
        data = dict(row)
        data['history'] = [item.strip() for item in data['history'].split(';')]
        return data
    return None

@app.get("/")
def health_check():
    return {"status": "ok", "db_exists": os.path.exists(db_path)}

@app.get("/api/track")
def track_shipment(q: str):
    data = get_shipment_data(q)
    if data:
        return data
    else:
        raise HTTPException(status_code=404, detail="查無此貨件")

@app.post("/callback")
async def callback(request: Request, x_line_signature: str = Header(None)):
    body = await request.body()
    try:
        handler.handle(body.decode("utf-8"), x_line_signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    return "OK"

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    user_msg = event.message.text.strip()
    data = get_shipment_data(user_msg)
    
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        if data:
            reply_text = f"📦 貨態查詢成功！\n---\n"
            reply_text += f"狀態：{data['status']}\n"
            reply_text += f"位置：{data['location']}\n"
            reply_text += f"預計抵達：{data['eta']}\n"
            reply_text += f"---\n最新進度：\n{data['history'][-1]}"
        else:
            reply_text = "查無此貨件，請重新輸入單號、客戶編號或統編。🤖"
            
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reply_text)]
            )
        )

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
