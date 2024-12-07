import requests
import os
from bs4 import BeautifulSoup
import logging
from translate import Translator  # 引入翻譯庫

# 設定日誌格式
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# 輸入目標網站的 URL
url = input("請輸入網站 (例如：https://www.spotify.com): ")
# 清理輸入，去除協議部分
url = url.replace("https://", "").replace("http://", "").replace("www.", "").strip('/')
url = f"https://w3techs.com/sites/info/{url}"
print(url)
logging.debug(f"處理後的 URL: {url}")

def translate_large_text(text, chunk_size=500):
    translator = Translator(to_lang="zh")
    translated_chunks = []
    
    # 將文本分割成小段進行翻譯
    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        translated_chunk = translator.translate(chunk)
        translated_chunks.append(translated_chunk)
    
    return ''.join(translated_chunks)

def W3techs_tool(url, translate_to_chinese=False):
    try:
        # 發送請求到網站
        response = requests.get(f"{url}")
        
        # 檢查狀態碼是否為 200，表示成功
        if response.status_code == 200:
            logging.debug("成功訪問網站，正在解析內容...")

            # 解析網頁內容
            soup = BeautifulSoup(response.content, 'html.parser')

            # 獲取網頁的純文本
            plain_text = soup.get_text(separator='\n')

            # 過濾掉空行
            filtered_text = "\n".join([line for line in plain_text.splitlines() if line.strip()])

            # 如果需要翻譯成中文
            if translate_to_chinese:
                filtered_text = translate_large_text(filtered_text)  # 使用翻譯後的文本
            
            # 輸出提取的純文本
            print(filtered_text)
            return filtered_text  # 返回 filtered_text
        else:
            logging.error(f"無法訪問網站，狀態碼：{response.status_code}")
            return None  # 如果無法訪問，返回 None
    
    except Exception as e:
        logging.error(f"發生錯誤：{e}")
        return None  # 返回 None

def save_report(url, translate_to_chinese, filtered_text):
    if filtered_text is None:
        print("沒有內容可供保存。")
        return
    
    # 保存結果到報告文件，從當前目錄回到前兩層
    save_report_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../reporting/w3techs_tool')
    
    # 構建報告文件名，將 URL 替換特殊字符為合法的文件名
    safe_url = url.replace("https://", "").replace("http://", "").replace("/", "_")
    save_report_path = os.path.join(save_report_dir, f"report_{safe_url}.txt")
    
    # 檢查並創建目錄
    os.makedirs(save_report_dir, exist_ok=True)

    try:
        # 保存文件到指定路徑
        with open(save_report_path, "w", encoding="utf-8") as file:
            file.write(filtered_text)  # 確保 filtered_text 已定義
            logging.info(f"純文本內容已保存到 {save_report_path}")
    except Exception as e:
        print(f"發生錯誤：{e}")

# 問用戶是否需要翻譯成中文
translate_option = input("是否需要將文本翻譯成中文？(y/n): ").lower()

translate_to_chinese = (translate_option == "y")

# 執行 W3Techs 工具並獲取結果
filtered_text = W3techs_tool(url, translate_to_chinese)

# 保存報告
save_report(url=url, translate_to_chinese=translate_to_chinese, filtered_text=filtered_text)
