import os
import sys
import logging
from concurrent.futures import ThreadPoolExecutor
from requests.exceptions import RequestException
from webtech import WebTech
from webtech.utils import ConnectionException, WrongContentTypeException
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# 設定日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# 導入數據庫和模型
# 導入數據庫和模型
file_path = os.path.dirname(os.path.abspath(__file__))  # 獲取當前腳本的絕對路徑
real_path = os.path.join(file_path, "..", "for_import")  # 修正路徑設定
print(f"url {real_path}")  # 輸出完整的 real_path
sys.path.append(real_path)  # 將 real_path 添加到系統路徑
import imports
"""code by a hopeless teenager
Code Disclaimer
Use of this code is at your own risk. This code is subject to continuous updates and may not be suitable for all situations, and its accuracy, completeness, or reliability is not guaranteed. The author assumes no responsibility for any direct or indirect losses arising from the use of this code.

Please carefully check the applicability of this code before use and make adjustments according to your actual needs. Users are responsible for complying with all relevant laws and regulations.

"""
