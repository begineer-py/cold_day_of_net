import os

def list_files_in_directory(directory):
    # 列出指定目錄下的所有文件和子目錄
    for root, dirs, files in os.walk(directory):
        for file in files:
            # 生成相對路徑
            relative_path = os.path.relpath(os.path.join(root, file), start=directory)
            print(relative_path)

if __name__ == "__main__":
    # 設置要搜索的目錄
    base_directory = os.path.dirname(os.path.abspath(__file__))  # 獲取當前文件的路徑
    base_directory = os.path.join(base_directory,"security-tools")
    list_files_in_directory(base_directory)
