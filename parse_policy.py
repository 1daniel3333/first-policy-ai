# parse_policy.py
import sys
import os
import pypdf

def extract_pdf_text(file_path):
    """
    Extract raw text from PDF file or read directly if it's a TXT file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
        
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    elif ext == ".pdf":
        reader = pypdf.PdfReader(file_path)
        full_text = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                full_text.append(f"--- Page {i+1} ---")
                full_text.append(text)
        return "\n".join(full_text)
    else:
        raise ValueError(f"Unsupported file format: {ext}. Only .pdf and .txt are supported.")

def build_normalization_prompt(raw_text):
    """
    Build prompt to normalize raw policy text into policy_schema.json structure.
    """
    prompt = (
        "請解析以下保單條款/內容之文本，並將其嚴格正規化格式化為單一 JSON 物件。\n"
        "必須符合以下 Schema 欄位：\n"
        "- policy_name (string): 保單名稱\n"
        "- insurer (string): 保險公司名稱\n"
        "- policy_type (string): 必須為以下之一: Accident, Reimbursement_Medical, Term_Life, Critical_Illness, Disability, Other\n"
        "- is_main_policy (boolean): 是否為主約 (true/false)\n"
        "- annual_premium (integer): 年繳保費(TWD)\n"
        "- coverage_amount (integer): 主要保額(TWD)\n"
        "- key_benefits (array of string): 主要理賠與保障項目摘要\n"
        "- exclusions (array of string): 除外責任與不給付項目摘要\n"
        "- waiting_period_days (integer): 等待期天數\n\n"
        f"--- 原始文本開始 ---\n{raw_text}\n--- 原始文本結束 ---"
    )
    return prompt

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python parse_policy.py <pdf_or_txt_file>")
        sys.exit(1)
        
    path = sys.argv[1]
    raw_text = extract_pdf_text(path)
    print(f"Successfully extracted {len(raw_text)} characters.")
    print("Sample extracted text:")
    print("=" * 40)
    print(raw_text[:500])
    print("=" * 40)
