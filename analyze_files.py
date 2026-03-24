import pandas as pd
import pdfplumber
import os

def analyze():
    output = []
    
    # Excel 範本分析
    excel_path = r"C:\Users\TK_Tsai\Downloads\高中英文參考詞彙表數據提取.xlsx"
    if os.path.exists(excel_path):
        try:
            df = pd.read_excel(excel_path)
            output.append(f"Excel Columns: {df.columns.tolist()}")
            output.append("Excel Head (First 5 rows):")
            output.append(df.head(5).to_string())
        except Exception as e:
            output.append(f"Excel Read Error: {str(e)}")
    else:
        output.append(f"Error: {excel_path} not found.")

    # PDF 分析
    pdf_path = r"C:\Users\TK_Tsai\Downloads\高中英文參考詞彙表(111學年度起適用).pdf"
    if os.path.exists(pdf_path):
        try:
            with pdfplumber.open(pdf_path) as pdf:
                output.append(f"Total Pages: {len(pdf.pages)}")
                # 讀取第 1, 5, 10, 20 頁看結構
                for page_idx in [0, 4, 9, 19]:
                    if page_idx < len(pdf.pages):
                        output.append(f"\n--- Page {page_idx + 1} Content Sample ---")
                        text = pdf.pages[page_idx].extract_text()
                        if text:
                            # 抓取前 2000 字
                            output.append(text[:2000])
                        else:
                            output.append("No text found on this page.")
        except Exception as e:
            output.append(f"PDF Read Error: {str(e)}")
    else:
        output.append(f"Error: {pdf_path} not found.")

    with open("analysis.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(output))

if __name__ == "__main__":
    analyze()
