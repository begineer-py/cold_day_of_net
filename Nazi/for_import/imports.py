import os
import importlib
import sys

# 獲取當前腳本的目錄
current_dir = os.path.dirname(os.path.abspath(__file__))
# 指定要導入的目錄
nazi_dir = os.path.join(current_dir, "..", "..", "Nazi")

# 遞迴函數，導入指定目錄及其子目錄下的所有 Python 檔案
def import_all_modules(directory):
    for root, dirs, files in os.walk(directory):  # 遍歷目錄樹
        # 檢查每個檔案
        for filename in files:
            # 檢查檔案是否為 Python 檔案，並排除特定檔案
            if (filename.endswith(".py") and 
                filename != "__init__.py" and 
                filename != "imports.py" and 
                filename != "env.py" and 
                "new-env" not in root and
                "venv" not in root and
                "migrations"not in root):  # 修正這行，確保不導入虛擬環境的檔案

                # 移除檔案的 .py 擴展名
                filename = filename[:-3]
                # 將根目錄路徑添加到 sys.path 以便導入
                if root not in sys.path:  # 防止重複添加相同的路徑
                    sys.path.append(root)
                
                print(f"Trying to import module: {filename} from {root}")  # 打印即將導入的模組路徑
                try:
                    importlib.import_module(filename)  # 動態導入模組
                    print(f"Imported module: {filename}")
                except ImportError as e:
                    print(f"Failed to import module {filename}: {e}")

# 調用導入函數
import_all_modules(nazi_dir)
