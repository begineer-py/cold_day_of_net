# 使用 Beautiful Soup 的爬蟲
import requests 
from bs4 import BeautifulSoup
import os
import logging
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from requests.exceptions import RequestException
# 設定日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
search = input("WEB:")
# 導入數據庫和模型
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from reporting.control_reconnaissance import query_links, LinksCom, LinksNotCom,Links_desigm_Com ,Links_desigm_not_Com
from reporting.control_reconnaissance import remove_duplicates,add_link
# 初始化 Flask 應用和數據庫
app = Flask(__name__)
save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "reporting", "database", "site.db")
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{save_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)  # 這裡將 db 實例與 app 關聯

