import whois
import os
import sys

def whois_target(target_web):
    """获取目标域名或IP的WHOIS信息并返回结果"""
    # 获取当前文件的绝对路径
    file_path = os.path.dirname(os.path.abspath(__file__))
    print(f"File path: {file_path}")

    try:
        w = whois.whois(target_web)
        result = {
            "Domain": w.domain_name,
            "Registrar": w.registrar,
            "Creation Date": w.creation_date,
            "Expiration Date": w.expiration_date,
            "Name Servers": w.name_servers,
        }
        return result
    except whois.parser.PywhoisError:
        print("Error: Unable to fetch WHOIS data for the specified domain.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return None

def save_report(report_data):
    """保存报告到指定文件"""
    save_report_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../reporting/whois_report.txt')
    
    try:
        with open(save_report_path, "a", encoding="utf-8") as f:
            if report_data:
                f.write("WHOIS Information:\n")
                for key, value in report_data.items():
                    f.write(f"{key}: {value}\n")
                f.write("\n")
                print(f"Report saved to {save_report_path}")
            else:
                print("No data to save.")
    except IOError as e:
        print(f"Error while writing to file: {e}")

if __name__ == "__main__":
    # 检查命令行参数
    if len(sys.argv) == 2:
        domain = sys.argv[1]  # 从命令行获取域名或IP
        report_data = whois_target(domain)  # 获取WHOIS信息
        save_report(report_data)  # 保存报告
    else:
        target_web = input("Enter target domain or IP: ")  # 从用户输入获取域名或IP
        report_data = whois_target(target_web)  # 获取WHOIS信息
        save_report(report_data)  # 保存报告
