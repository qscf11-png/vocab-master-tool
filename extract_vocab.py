import pdfplumber
import re
import pandas as pd

def extract_all_vocab(pdf_path):
    vocab_list = []
    # 正則表達式：匹配單字後面跟著詞性 (n., v., adj., adv., prep., conj., pron., art., det., num., int.)
    # 單字可能包含連字號或小括號內容，如 "telephone/phone", "treat(ment)"
    # 詞性可能有多個，如 "v./n."
    pattern = re.compile(r'([A-Za-z\-\(\)/]+)\s+([a-z\.\/\(\)]+)')
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages[15:]: # 跳過前言，從 Page 16 之後開始（單字表開始處）
            text = page.extract_text()
            if not text:
                continue
            
            # 簡單清理
            lines = text.split('\n')
            for line in lines:
                # 尋找所有符合 單字 詞性 的組合
                matches = pattern.findall(line)
                for word, pos in matches:
                    # 過濾掉一些雜訊 (太短或全是符號的)
                    if len(word) > 1 and ('.' in pos or '/' in pos):
                        vocab_list.append({'單字': word, '詞類 (Parts of Speech)': pos})
    
    return pd.DataFrame(vocab_list).drop_duplicates()

if __name__ == "__main__":
    pdf_path = r"C:\Users\TK_Tsai\Downloads\高中英文參考詞彙表(111學年度起適用).pdf"
    df = extract_all_vocab(pdf_path)
    print(f"Extracted {len(df)} unique vocabulary items.")
    df.to_csv("extracted_vocab.csv", index=False, encoding='utf-8-sig')
    print("Saved to extracted_vocab.csv")
