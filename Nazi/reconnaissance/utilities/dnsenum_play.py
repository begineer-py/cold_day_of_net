import dns.resolver
from urllib.parse import urlparse

def dns_enum(domain):
    print(f"正在進行 DNS 枚舉：{domain}")

    # 獲取 A 記錄
    try:
        a_records = dns.resolver.resolve(domain, 'A')
        for record in a_records:
            print(f"A 記錄: {record}")
    except dns.resolver.NoAnswer:
        print(f"該域名 {domain} 沒有 A 記錄。")
    except Exception as e:
        print(f"獲取 A 記錄時發生錯誤：{e}")

    # 獲取 MX 記錄
    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        for record in mx_records:
            print(f"MX 記錄: {record}")
    except dns.resolver.NoAnswer:
        print(f"該域名 {domain} 沒有 MX 記錄。")
    except Exception as e:
        print(f"獲取 MX 記錄時發生錯誤：{e}")

    # 獲取 NS 記錄
    try:
        ns_records = dns.resolver.resolve(domain, 'NS')
        for record in ns_records:
            print(f"NS 記錄: {record}")
    except dns.resolver.NoAnswer:
        print(f"該域名 {domain} 沒有 NS 記錄。")
    except Exception as e:
        print(f"獲取 NS 記錄時發生錯誤：{e}")

if __name__ == "__main__":
    target = input("請輸入目標域名：")
    parsed_url = urlparse(target)
    real_target  = parsed_url.netloc if parsed_url.netloc else parsed_url.path
    dns_enum(real_target)
