from urllib.parse import urlparse
import socket
import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# 輸入 URL
url = input("請輸入目標 IP 或域名（可以是完整的 URL）: ")

# 解析主機名稱
parsed_url = urlparse(url)
target = parsed_url.netloc if parsed_url.netloc else parsed_url.path  # 提取主機名稱

# 顯示主機名稱
logging.info(f"目標主機名稱: {target}")

# 獲取目標的 IP 地址
try:
    target_ip = socket.gethostbyname(target)
    logging.info(f"解析的目標 IP 地址: {target_ip}")
except socket.gaierror:
    logging.error("無法解析目標，請檢查輸入的域名或 IP 地址")
    exit()

# 其他掃描代碼...

# 自動獲取 IP 地址
try:
    target_ip = socket.gethostbyname(target)
    logging.info(f"解析的目標 IP 地址: {target_ip}")

except socket.gaierror:
    logging.error("無法解析目標，請檢查輸入的域名或 IP 地址")
    exit()

ports_to_scan = [
    20,   # FTP（數據傳輸）
    21,   # FTP（控制通道）
    22,   # SSH
    23,   # Telnet
    25,   # SMTP
    53,   # DNS
    67,   # DHCP（伺服器）
    68,   # DHCP（客戶端）
    80,   # HTTP
    110,  # POP3
    143,  # IMAP
    443,  # HTTPS
    3306, # MySQL
    5432, # PostgreSQL
    6379, # Redis
    8080, # HTTP（替代端口）
    27017 # MongoDB
]

def scan_web(port, target):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(2)
            result = sock.connect_ex((target, port))
            if result == 0:
                logging.info(f"端口 {port} 是開放的")
            else:
                logging.info(f"端口 {port} 是關閉的")
    except Exception as e:
        logging.error(f"掃描端口 {port} 時發生錯誤: {e}")

# 對所有端口進行掃描
for port in ports_to_scan:
    scan_web(port, target_ip)
