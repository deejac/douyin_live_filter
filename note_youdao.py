from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import argparse
import json
from bs4 import BeautifulSoup


def get_youdao_note():
    # 创建Chrome浏览器选项
    options = Options()
    options.add_argument("--headless")  # 无头模式
    options.add_argument("--no-sandbox")  # 禁用沙盒模式

    # 创建浏览器实例并加载网页
    driver = webdriver.Chrome(options=options)
    driver.get("https://note.youdao.com/s/OCsFoUGA")
    # seconds
    #driver.get("https://note.youdao.com/ynoteshare/index.html?id=224b5c6f231b612ec40f90d764105867&type=note&_time=1701241218158")
    # 等待网页加载完全
    iframe = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//iframe[@id='content-body']")))

    # 切换到iframe的上下文
    driver.switch_to.frame(iframe)

    # 获取iframe中的内容
    html_content = driver.page_source
    # 解析HTML内容
    soup = BeautifulSoup(html_content, 'html.parser')

    # 找到id为note-view的元素
    note_view = soup.find(id='note-view')

    # 找到note-view中的所有span元素
    spans = note_view.find_all('span')

    # 获取所有span元素的文本内容
    span_texts = [span.get_text() for span in spans]

    # 打印所有span元素的文本内容
    for text in span_texts:
      print(text)
    #print(html_content)
    # 关闭浏览器实例


    driver.quit()


if __name__ == '__main__':
    get_youdao_note()