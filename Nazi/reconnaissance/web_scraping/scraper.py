import requests
from bs4 import BeautifulSoup
import csv
import os
from urllib.parse import urljoin, urlparse
import logging

# 初始化集合存储已访问链接
visited_links = set()

# 设置日志
logging.basicConfig(filename='web_scrape.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def web_connect(url):
    """连接网页并返回网页内容"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        logging.info(f"成功连接到 {url}")
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"连接 {url} 时出错: {e}")
        logging.error(f"连接 {url} 时出错: {e}")
    return None

def parse_html(content, base_url):
    """解析 HTML 内容并提取标题和链接"""
    soup = BeautifulSoup(content, 'html.parser')
    title = soup.title.string if soup.title else '無標題'
    # 仅提取有效的 .com 链接，并去重
    links = {urljoin(base_url, a['href']) for a in soup.find_all('a', href=True) if ".com" in urlparse(urljoin(base_url, a['href'])).netloc}
    return title, links

def save_results(title, links, depth):
    """保存当前深度的抓取结果到 CSV 文件"""
    current_directory = os.path.dirname(os.path.abspath(__file__))
    target_directory = os.path.join(current_directory, "..", "..", 'reporting')
    os.makedirs(target_directory, exist_ok=True)
    file_path = os.path.join(target_directory, f'depth_{depth}_results.csv')
    
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["标题", "链接"])
        writer.writerow([title, ""])
        for link in links:
            writer.writerow(["", link])
    print(f"深度 {depth} 的结果已保存到 {file_path}")

def scrape_links(url, depth, max_depth):
    """递归抓取链接直到达到最大深度"""
    if depth > max_depth or url in visited_links:
        return
    visited_links.add(url)  # 将链接标记为已访问

    # 抓取页面内容
    content = web_connect(url)
    if content is None:
        return
    
    # 解析页面内容
    title, links = parse_html(content, url)
    
    print(f"深度 {depth} - 标题: {title}")
    print(f"深度 {depth} - 找到 {len(links)} 个 .com 链接")
    
    # 保存抓取结果
    save_results(title, links, depth)
    
    # 递归处理所有新链接
    for link in links:
        if link not in visited_links:
            scrape_links(link, depth + 1, max_depth)

# 主函数
def main():
    start_url = input("请输入起始网址: ")
    max_depth = int(input("请输入最大搜索深度: "))
    
    if ".com" not in urlparse(start_url).netloc:
        print("输入的网址格式无效。请提供一个有效的 .com URL。")
        return

    # 开始抓取
    scrape_links(start_url, 0, max_depth)

if __name__ == "__main__":
    main()
