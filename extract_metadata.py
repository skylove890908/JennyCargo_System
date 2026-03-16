import json
import os

def rgb_to_hex(r, g, b):
    return "#{:02x}{:02x}{:02x}".format(int(r*255), int(g*255), int(b*255))

def extract_metadata():
    with open("node_analysis.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    colors = set()
    text_labels = set()
    
    # Recursive function to find colors and text
    def walk(node):
        # Find colors in fills
        if 'fills' in node:
            for fill in node['fills']:
                if fill.get('type') == 'SOLID' and 'color' in fill:
                    c = fill['color']
                    colors.add(rgb_to_hex(c.get('r', 0), c.get('g', 0), c.get('b', 0)))
        
        # Find colors in backgroundColor (for frames)
        if 'backgroundColor' in node:
            c = node['backgroundColor']
            if c.get('a', 0) > 0: # Only if not transparent
                colors.add(rgb_to_hex(c.get('r', 0), c.get('g', 0), c.get('b', 0)))

        # Find text content
        if node.get('type') == 'TEXT':
            text = node.get('characters', '').strip()
            if text:
                text_labels.add(text)
        
        if 'children' in node:
            for child in node['children']:
                walk(child)

    # The actual nodes are under data['nodes']['0:1']['document']
    walk(data['nodes']['0:1']['document'])
    
    print("🎨 偵測到的顏色範例：")
    for c in sorted(list(colors))[:10]:
        print(f"  - {c}")
        
    print("\n📝 偵測到的文字標籤範例：")
    for t in sorted(list(text_labels))[:15]:
        print(f"  - {t}")

if __name__ == "__main__":
    extract_metadata()
