import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
FIGMA_TOKEN = os.getenv("FIGMA_ACCESS_TOKEN")
FILE_KEY = "gWtCIpFgjNmB48p3WIdhce"
NODE_ID = "0:1"

def analyze_node():
    url = f"https://api.figma.com/v1/files/{FILE_KEY}/nodes?ids={NODE_ID}"
    headers = {"X-Figma-Token": FIGMA_TOKEN}
    
    print(f"🔍 正在深度解析 Figma 節點 (ID: {NODE_ID})...")
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        with open("node_analysis.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        node_data = data['nodes'][NODE_ID]['document']
        print(f"✅ 解析成功：{node_data.get('name')}")
        
        # 簡單統計
        frames = [c for c in node_data.get('children', []) if c['type'] == 'FRAME']
        print(f"偵測到 {len(frames)} 個主要 Frame。")
        
        # 提取顏色 (簡單示範)
        # 這裡之後會寫成更複雜的邏輯來生成 Tailwind Config
    else:
        print(f"❌ 解析失敗：{response.status_code}")

if __name__ == "__main__":
    analyze_node()
