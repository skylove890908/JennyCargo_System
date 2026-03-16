import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
FIGMA_TOKEN = os.getenv("FIGMA_ACCESS_TOKEN")
FILE_KEY = "gWtCIpFgjNmB48p3WIdhce"

def extract_styles():
    url = f"https://api.figma.com/v1/files/{FILE_KEY}/styles"
    headers = {"X-Figma-Token": FIGMA_TOKEN}
    
    print(f"🎨 正在提取 Figma 設計規範 (Styles)...")
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        styles = response.json()
        with open("figma_styles.json", "w", encoding="utf-8") as f:
            json.dump(styles, f, indent=2, ensure_ascii=False)
        print(f"✅ 成功提取 {len(styles.get('meta', {}).get('styles', []))} 個樣式定義。")
    else:
        print(f"❌ 提取失敗：{response.status_code}")

if __name__ == "__main__":
    extract_styles()
