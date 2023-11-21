from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

# 创建Chrome浏览器选项
options = Options()
options.add_argument("--headless")  # 无头模式

# 创建浏览器实例并加载网页
driver = webdriver.Chrome(options=options)
driver.get("https://live.douyin.com/75747022717")

# 等待网页加载完全
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "html")))

# 获取网页HTML内容
html_content = driver.page_source
m3u8_pattern = r"(https?://\S+\.m3u8)"
m3u8_links = re.findall(m3u8_pattern, html_content)[0].replace("\\", "").replace("u0026", "&").split("\"hls\":\"")[1].split("\",\"cmaf\"")[0]

print("网页HTML内容：")
print(m3u8_links)

# 关闭浏览器实例
driver.quit()