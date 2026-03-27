"""
下載並轉換成語資料為 JS 格式
資料來源：https://github.com/pwxcoo/chinese-xinhua
"""
import json
import urllib.request
import os

RAW_URL = "https://raw.githubusercontent.com/pwxcoo/chinese-xinhua/master/data/idiom.json"
LOCAL_RAW = "idiom_raw.json"
OUTPUT_JS = "idiom_data.js"


def download_idiom_data():
    """從 GitHub 下載成語原始資料"""
    if os.path.exists(LOCAL_RAW):
        print(f"已存在 {LOCAL_RAW}，跳過下載")
        return
    print("正在下載成語資料...")
    urllib.request.urlretrieve(RAW_URL, LOCAL_RAW)
    print(f"下載完成：{LOCAL_RAW}")


def convert_to_js():
    """將原始 JSON 轉換為精簡 JS 格式"""
    with open(LOCAL_RAW, "r", encoding="utf-8") as f:
        raw = json.load(f)

    print(f"原始資料筆數：{len(raw)}")

    # 轉換為精簡格式
    idioms = []
    for item in raw:
        word = item.get("word", "").strip()
        if not word:
            continue

        # 清理例句（移除 ★ 後面的出處標記）
        example = item.get("example", "").strip()
        if example == "无" or example == "無":
            example = ""

        # 清理出處
        derivation = item.get("derivation", "").strip()
        if derivation == "无" or derivation == "無":
            derivation = ""

        idioms.append({
            "w": word,
            "py": item.get("pinyin", "").strip(),
            "d": item.get("explanation", "").strip(),
            "o": derivation,
            "x": example,
        })

    print(f"轉換後筆數：{len(idioms)}")

    # 輸出為 JS 格式
    js_content = "const IDIOM_DB = " + json.dumps(idioms, ensure_ascii=False, separators=(",", ":")) + ";"
    with open(OUTPUT_JS, "w", encoding="utf-8") as f:
        f.write(js_content)

    # 計算檔案大小
    size_mb = os.path.getsize(OUTPUT_JS) / (1024 * 1024)
    print(f"輸出完成：{OUTPUT_JS}（{size_mb:.1f} MB，{len(idioms)} 筆成語）")


if __name__ == "__main__":
    download_idiom_data()
    convert_to_js()
