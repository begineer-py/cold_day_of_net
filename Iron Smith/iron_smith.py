import os

# 獲取當前腳本所在的目錄
script_dir = os.path.dirname(os.path.abspath(__file__))
input_file_path = os.path.join(script_dir, "list.txt")
write_file = os.path.join(script_dir, "write.txt")

# 讀取要寫入的內容
def get_write_content():
    if os.path.exists(write_file):
        with open(write_file, "r", encoding="utf-8") as file:
            return file.read()
    return ""  # 若檔案不存在，回傳空字串

# 創建文件和文件夾
def create_paths_from_file(file_path):
    if not os.path.exists(file_path):
        print(f"指定的路徑清單文件不存在: {file_path}")
        return
    
    write_content = get_write_content()  # 讀取要寫入的內容
    
    with open(file_path, "r", encoding="utf-8") as file:
        paths = file.readlines()
        for path in paths:
            path = path.strip()
            if not path:
                continue
            full_path = os.path.join(script_dir, path)
            directory = os.path.dirname(full_path)

            # 創建目錄及文件
            if not os.path.exists(directory):
                os.makedirs(directory)
            if not os.path.exists(full_path):
                with open(full_path, "w", encoding="utf-8") as new_file:
                    new_file.write(write_content)
                print(f"創建檔案: {full_path}")
            else:
                print(f"檔案已存在，跳過: {full_path}")

# 主函數
if __name__ == "__main__":
    create_paths_from_file(input_file_path)
