from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
browser = webdriver.Chrome(options=chrome_options)
WAIT = WebDriverWait(browser, 10)
browser.set_window_size(1400,900)

if __name__ == '__main__':
    url = "https://zlapp.fudan.edu.cn/site/ncovfudan/daily"
    # url = "https://uis.fudan.edu.cn/"
    browser.get(url)

    username = WAIT.until(EC.presence_of_element_located(((By.XPATH, '//*[@id="username"]'))))
    username.send_keys('')
    passwd = WAIT.until(EC.presence_of_element_located(((By.XPATH, '//*[@id="password"]'))))
    passwd.send_keys('')
    signin = WAIT.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="idcheckloginbtn"]')))
    signin.click()

    submit = WAIT.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="tab-title-desc-little"]')))
    submit.click()

print("Perfect signin")
input()

