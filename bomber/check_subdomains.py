import os

# 生成檔案路徑
script_dir = os.path.dirname(os.path.abspath(__file__))
# 生成檔案路徑，將檔案放在與腳本同一目錄下
file_path = os.path.join(script_dir, "end_return.txt")
try:
    # 創建並寫入檔案
    with open(file_path, 'w', encoding='utf-8') as file:  # 確保使用 utf-8 編碼
        file.write("這是測試內容\n")
    print(f"檔案已生成: {file_path}")

except Exception as e:
    print(f"寫入檔案時發生錯誤: {e}")
