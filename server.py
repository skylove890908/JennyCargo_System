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
    TextMessage,
    FlexMessage,
    FlexContainer
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

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

def create_flex_message(data):
    # 設計漂亮卡片的 JSON 結構
    flex_json = {
      "type": "bubble",
      "header": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {"type": "text", "text": "📦 貨態查詢結果", "weight": "bold", "color": "#FFFFFF", "size": "sm"},
          {"type": "text", "text": data['status'], "weight": "bold", "size": "xxl", "margin": "md", "color": "#FFFFFF"}
        ],
        "backgroundColor": "#126eb4"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {"type": "box", "layout": "horizontal", "contents": [
            {"type": "text", "text": "單號", "size": "sm", "color": "#aaaaaa", "flex": 1},
            {"type": "text", "text": data['tid'], "size": "sm", "color": "#666666", "flex": 2, "align": "end"}
          ]},
          {"type": "separator", "margin": "md"},
          {"type": "box", "layout": "vertical", "margin": "lg", "spacing": "sm", "contents": [
            {"type": "box", "layout": "horizontal", "contents": [
              {"type": "text", "text": "目前位置", "size": "sm", "color": "#555555", "flex": 1},
              {"type": "text", "text": data['location'], "size": "sm", "color": "#111111", "flex": 2, "align": "end", "weight": "bold"}
            ]},
            {"type": "box", "layout": "horizontal", "contents": [
              {"type": "text", "text": "預計抵達", "size": "sm", "color": "#555555", "flex": 1},
              {"type": "text", "text": data['eta'], "size": "sm", "color": "#111111", "flex": 2, "align": "end", "weight": "bold"}
            ]}
          ]},
          {"type": "box", "layout": "vertical", "margin": "xl", "contents": [
            {"type": "text", "text": "📍 最新物流軌跡", "size": "xs", "color": "#aaaaaa", "weight": "bold"},
            {"type": "text", "text": data['history'][-1], "size": "sm", "color": "#126eb4", "margin": "xs", "wrap": True}
          ]}
        ]
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {"type": "button", "style": "link", "height": "sm", "action": {
            "type": "uri", "label": "查看詳細軌跡", "uri": f"https://jenny-cargo-system.vercel.app/?q={data['tid']}"
          }}
        ]
      }
    }
    return FlexContainer.from_json(json.dumps(flex_json))

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
            flex_content = create_flex_message(data)
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[FlexMessage(alt_text="📦 貨態查詢結果", contents=flex_content)]
                )
            )
        else:
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text="查無此貨件，請重新輸入。🤖")]
                )
            )

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
