from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import argparse
import json



def get_m3u8_links(room_id):
    # 创建Chrome浏览器选项
    options = Options()
    options.add_argument("--headless")  # 无头模式
    options.add_argument("--no-sandbox")  # 禁用沙盒模式

    # 创建浏览器实例并加载网页
    driver = webdriver.Chrome(options=options)
    driver.get("https://live.douyin.com/" + room_id)

    # 等待网页加载完全
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "html")))

    # 获取网页HTML内容
    html_content = driver.page_source
    m3u8_pattern = r"(https?://\S+\_or4.m3u8)"
    script_pattern = r"(<script\b[^>]*>(.*?)</script>)"
    tmp =  re.findall(script_pattern, html_content)
    print(tmp)
    for i in tmp:
            print(i)
            content = i[1]
            if "m3u8" in content:
               json_str = content.replace("self.__pace_f.push","")
               try:
                   json_data = json.loads(json_str)
                   print(json_data)
               except json.JSONDecodeError:
                   print("无法解析JSON字符串：", json_str)
                   print("=====================================")
            print("\n=====================================")
    print(tmp)
    m3u8_links=""
    if len(re.findall(m3u8_pattern, html_content)) > 0:
        m3u8_links = re.findall(m3u8_pattern, html_content)[0].replace("\\", "").replace("u0026", "&").split("\"hls\":\"")[1].split("\",\"cmaf\"")[0]
    else:
        print("未找到M3U8链接！")


    print("网页HTML内容：")
    print(m3u8_links)

    # 关闭浏览器实例
    driver.quit()

    return m3u8_links

if __name__ == '__main__':
    # 创建解析器
    parser = argparse.ArgumentParser(description="获取抖音直播间的M3U8链接")
    parser.add_argument("--room_id", help="抖音直播间ID")
    args = parser.parse_args()
    get_m3u8_links(args.room_id)

