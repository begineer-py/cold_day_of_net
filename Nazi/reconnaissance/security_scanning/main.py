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

# 初始化 WebTech 實例
wt = WebTech()
wt.timeout = 6  # 設定默認超時值

# 提取檢測到的技術堆疊的函數
def extract_detected_technologies(result, start_header="Detected technologies:", end_header="Detected the following interesting custom headers:"):
    try:
        # 查找檢測到的技術的開始位置
        tech_start = result.find(start_header)
        if tech_start == -1:
            return ""  # 如果未找到開始標題，返回空字串

        # 查找檢測到的技術部分的結束位置
        tech_end = result.find(end_header, tech_start)
        if tech_end == -1:
            tech_end = len(result)  # 如果未找到結束標題，則讀取到字串末尾

        # 從結果中提取技術
        technologies = result[tech_start:tech_end].strip().split("\n")[1:]  # 跳過標題行
        technologies = [tech.strip().replace("-", "") for tech in technologies if tech.strip()]  # 去除連字符並過濾空行

        return ", ".join(technologies)
    except Exception as e:
        # 記錄或打印錯誤以進行調試
        print(f"提取技術時出錯: {e}")
        return ""

# 處理單個域名的函數
def process_domain(serial_number, domain):
    domain_with_https = f"https://{domain.strip()}"
    try:
        result = wt.start_from_url(domain_with_https)
        technology_stack = extract_detected_technologies(result)
        logging.info(f"處理域名: {domain_with_https}")
        
        # 檢查技術堆疊是否為空
        if not technology_stack:
            technology_stack = '未找到'  # 設置預設值
            
        return {'序號': serial_number, '域名': domain_with_https, '技術堆疊': technology_stack}
    except ConnectionException as e:
        logging.error(f"域名 {domain_with_https} 的連接錯誤: {e}")
    except WrongContentTypeException as e:
        logging.error(f"域名 {domain_with_https} 的內容類型錯誤: {e}")
    except RequestException as e:
        logging.error(f"域名 {domain_with_https} 的請求錯誤: {e}")
    
    return {'序號': serial_number, '域名': domain_with_https, '技術堆疊': '未找到'}


def get_domains_from_db():
    with app.app_context():
        # 獲取所有域名，包括 .com 和非 .com
        com_domains = query_links(LinksCom)
        not_com_domains = query_links(LinksNotCom)

        # 檢查返回值是否為 None
        if com_domains is None:
            logging.error("從數據庫獲取 .com 域名時發生錯誤，返回值為 None。")
            com_domains = []  # 設置為空列表以避免後續錯誤

        if not_com_domains is None:
            logging.error("從數據庫獲取非 .com 域名時發生錯誤，返回值為 None。")
            not_com_domains = []  # 設置為空列表以避免後續錯誤

        # 紀錄獲取的域名
        logging.info(f"從數據庫獲取的 .com 域名: {[domain.name for domain in com_domains]}")
        logging.info(f"從數據庫獲取的非 .com 域名: {[domain.name for domain in not_com_domains]}")

        # 返回所有域名的平面列表
        return [domain.name for domain in com_domains] + [domain.name for domain in not_com_domains]


# 保存報告的函數
def save_report(results):
    with app.app_context():
        for result in results:
            domain_name = result['域名']
            technology_stack = result['技術堆疊']

            # 檢查 technology_stack 是否為空
            if not technology_stack:
                logging.warning(f"域名 {domain_name} 的技術堆疊為空，將不會保存到數據庫。")
                continue  # 跳過這個條目
            
            if domain_name.endswith('.com'):
                new_link = Links_desigm_Com(name=domain_name, technology_stack=technology_stack)
                db.session.add(new_link)
                logging.info(f"保存到 Links_desigm_Com: {domain_name}")
            else:
                new_link = Links_desigm_not_Com(name=domain_name, technology_stack=technology_stack)
                db.session.add(new_link)
                logging.info(f"保存到 Links_desigm_not_Com: {domain_name}")
        
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(f"保存數據時出錯: {e}")

def process_domains(domains):
    total_domains = len(domains)
    logging.info(f"待處理的總域名數量: {total_domains}")

    with ThreadPoolExecutor() as executor:
        results = executor.map(process_domain, range(1, total_domains + 1), domains)
    if search.endswith(".com"):
        add_link(search, is_com=True) 
    else:
        add_link(search, is_com=False) 
    save_report(results)  # 將結果保存到數據庫
    remove_duplicates("Links_desigm_not_Com")
    remove_duplicates("Links_desigm_Com")
    query_links(Links_desigm_not_Com)
    query_links(Links_desigm_Com)
    logging.info("腳本完成。")
def main():
    domains = get_domains_from_db()
    process_domains(domains)

if __name__ == "__main__":
    main()

