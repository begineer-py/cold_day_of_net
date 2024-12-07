import requests  # 導入 requests 模塊，用於發送 HTTP 請求
import os  # 導入 os 模塊，用於與操作系統互動
import subprocess  # 導入 subprocess 模塊，用於執行系統命令
from concurrent.futures import ThreadPoolExecutor, as_completed  # 導入多執行緒處理模組

# 設置輸出文件名
script_dir = os.path.dirname(os.path.abspath(__file__))  # 獲取當前腳本的目錄

# 用戶輸入攻擊的主域名
attack_web = str(input("請輸入攻擊的主域名: "))  # 用戶輸入要攻擊的主域名
# 用戶輸入子域名深度
depths = int(input("請輸入子域名枚舉深度: "))  # depths 表示 amass 子域名掃描深度

# 定義子域名收集和檢查函數
def attack_start(attack_web, depths):
    # 輸出子域名文件的路徑
    file = os.path.join(script_dir, f"amass_subdomains_depth_{attack_web}_{depths}.txt")  
    print(f"正在使用 amass 收集子域名, 結果將保存到: {file}")
    
    # 使用 amass 枚舉子域名，指定深度，將結果輸出到文件
    os.system(f"amass enum -d {attack_web} -max-depth {depths} -o {file}")
    
    if not os.path.exists(file):  # 檢查文件是否存在
        print(f"找不到 amass 輸出文件: {file}")
        return []

    # 讀取 amass 的輸出文件，檢查每個子域名的有效性
    with open(file, "r", encoding="utf-8") as f:
        subdomains = f.readlines()  # 讀取所有子域名

    # 檢查每個子域名是否有效
    verified_file = os.path.join(script_dir, f"verified_subdomains_{depths}.txt")  # 保存有效子域名的文件
    with open(verified_file, "a", encoding="utf-8") as verified_f:
        for subdomain in subdomains:
            subdomain = subdomain.strip()  # 去除前後空白
            full_url = f"http://{subdomain}"
            try:
                response = requests.get(full_url, timeout=5)  # 設置超時
                if response.status_code in (200, 301, 302):  # 檢查有效的子域名
                    print(f"成功找到有效子域名: {full_url}")
                    verified_f.write(full_url + "\n")  # 將成功的子域名寫入文件
            except requests.RequestException:
                pass  # 忽略請求錯誤

    print("子域名檢測完成")
    return subdomains  # 返回子域名列表

# Nmap 攻擊函數
def nmap_attack(subdomain):
    file = os.path.join(script_dir, f"nmap_{subdomain}.txt")  # 根據子域名創建文件名
    result = subprocess.run(
        ["nmap", subdomain, "-T4", "-oN", file, "-p-", "-A", "--script=default"],
        stdout=subprocess.PIPE,  # 捕獲標準輸出
        stderr=subprocess.PIPE,   # 捕獲錯誤輸出
        text=True                  # 將輸出轉換為字串
    )
    
    if result.returncode != 0:  # 檢查命令是否成功執行
        print(f"nmap 掃描失敗，請檢查命令是否正確")
        print(f"錯誤信息: {result.stderr}")  # 輸出錯誤信息
    else:
        print(f"nmap 掃描結果已保存到: {file}")

# 開始攻擊
def main():
    # 收集子域名
    subdomains = attack_start(attack_web, depths)
    
    if not subdomains:  # 如果沒有收集到子域名，則結束
        return

    # 使用 ThreadPoolExecutor 來並行處理 Nmap 掃描
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(nmap_attack, subdomain): subdomain for subdomain in subdomains}
        for future in as_completed(futures):
            subdomain = futures[future]
            try:
                future.result()  # 觸發執行，並檢查異常
            except Exception as exc:
                print(f"{subdomain} 生成異常: {exc}")

    print("Nmap 掃描完成")

if __name__ == "__main__":  # 確保主程式運行
    main()
