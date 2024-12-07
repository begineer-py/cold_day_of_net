import nmap
import socket

def port_scanner():
    print("歡迎使用 Nmap 自動化工具")
    print("<----------------------------------------------------->")

    # 初始化掃描器
    scanner = nmap.PortScanner()

    # 輸入網址並格式化
    url = input("請輸入您要掃描的網址（例如：open.spotify.com）：")
    url = url.replace("https://", "").replace("http://", "").split("/")[0]
    print(f"您輸入的網址是：{url}")

    try:
        # 將網址解析為 IP 地址
        ip = socket.gethostbyname(url)
        print(f"解析的 IP 地址是：{ip}")
    except socket.gaierror:
        print("無效的網址，請檢查並重試。")
        return

    # 定義掃描選項
    resp_dict = {
        '1': ['-v -sS', 'tcp'],
        '2': ['-v -sU', 'udp'],
        '3': ['-v -sS -sV -sC -A -O', 'tcp']
    }

    # 選擇掃描類型
    resp = input("""\n請選擇您想要進行的掃描類型：
                    1) SYN ACK 掃描
                    2) UDP 掃描
                    3) 綜合掃描 \n""")
    
    if resp not in resp_dict:
        print("選擇無效，退出程序。")
        return

    # 獲取掃描類型和協議
    scan_type, protocol = resp_dict[resp]

    # 定義要掃描的端口範圍
    ports = "1-1024"  # 掃描 1 到 1024 的端口範圍

    try:
        print(f"Nmap 版本: {scanner.nmap_version()}")
        scanner.scan(ip, ports, scan_type)

        # 檢查 IP 是否在掃描結果中
        if ip in scanner.all_hosts():
            print(f"{ip} 的掃描狀態：", scanner[ip].state())
            print("可用協議：", scanner[ip].all_protocols())

            # 檢查選定協議的開放端口
            if protocol in scanner[ip]:
                open_ports = scanner[ip][protocol].keys()
                print("開放的端口：", sorted(open_ports))
            else:
                print(f"未找到 {protocol.upper()} 協議的開放端口")
        else:
            print("錯誤：掃描結果中找不到主機。請檢查 IP 或重試。")

    except Exception as e:
        print(f"掃描過程中發生錯誤：{e}")

if __name__ == "__main__":
    port_scanner()
