import os
import requests
import json
from dotenv import load_dotenv

# 加載環境變數
load_dotenv()
FIGMA_TOKEN = os.getenv("FIGMA_ACCESS_TOKEN")
FILE_KEY = "gWtCIpFgjNmB48p3WIdhce"

def get_figma_file():
    url = f"https://api.figma.com/v1/files/{FILE_KEY}"
    headers = {"X-Figma-Token": FIGMA_TOKEN}
    
    print(f"🚀 正在從 Figma 抓取檔案資料 (Key: {FILE_KEY})...")
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        # 儲存一份原始資料供分析
        with open("figma_structure.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print("✅ 成功抓取資料！")
        print(f"專案名稱: {data.get('name')}")
        
        # 簡單列出第一層的頁面和節點
        for canvas in data.get('document', {}).get('children', []):
            print(f"📄 頁面: {canvas.get('name')}")
            for node in canvas.get('children', []):
                print(f"  - 節點: [{node.get('type')}] {node.get('name')} (ID: {node.get('id')})")
    else:
        print(f"❌ 抓取失敗，狀態碼: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    if not FIGMA_TOKEN:
        print("❌ 找不到 FIGMA_ACCESS_TOKEN，請檢查 .env 檔案。")
    else:
        get_figma_file()
