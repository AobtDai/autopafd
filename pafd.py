from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from io import BytesIO
from PIL import Image
import pytesseract
import sys

firefox_options = webdriver.FirefoxOptions()
firefox_options.add_argument('--headless')
firefox_options.add_argument('--disable-gpu')
# firefox_options.add_argument("start-maximized")
# firefox_options.add_argument("--window-size=1827,1080")
# ProfileDir = r"C:\Users\25705\AppData\Roaming\Mozilla\Firefox\Profiles"
# ProfileDir = r"C:\Users\25705\AppData\Roaming\Mozilla\Firefox\Profiles\qvxutacy.default"
# ProfileDir = r"C:\Users\25705\AppData\Roaming\Mozilla\Firefox\Profiles\c9nmsxz7.default-release"
# profile1 = webdriver.FirefoxProfile(ProfileDir)
# time.sleep(1)
# browser = webdriver.Firefox(options=firefox_options, firefox_profile=profile1)
browser = webdriver.Firefox(options=firefox_options)
WAIT = WebDriverWait(browser, 10)
WAITPos = WebDriverWait(browser, 30)
browser.maximize_window()
# browser.set_window_size(1400,900)

if __name__ == '__main__':
    url = "https://uis.fudan.edu.cn/authserver/login"
    browser.get(url)

    try:
        username = WAIT.until(EC.presence_of_element_located(((By.XPATH, '//*[@id="username"]'))))
        username.send_keys('')
        passwd = WAIT.until(EC.presence_of_element_located(((By.XPATH, '//*[@id="password"]'))))
        passwd.send_keys('')
        signin = WAIT.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="idcheckloginbtn"]')))
        signin.click()
        print("Perfect signin")
    except:
        print("Have been signin\n")

    url = "https://zlapp.fudan.edu.cn/site/ncov/fudanDaily"
    browser.get(url)

    ExitOrNot = 0
    try:
        HaveDone = WAIT.until(EC.presence_of_element_located((By.XPATH, '//*[@class="wapcf-btn-qx"]')))
        print("Have done today")
        browser.quit()
        ExitOrNot = 1
    except:
        pass
    if ExitOrNot==1:
        sys.exit()

    # window = browser.find_element(By.XPATH, '//*[@class="modal_close"]')
    cnfr = WAIT.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="wapat-btn wapat-btn-ok"]')))
    cnfr.click()

    # will set a flag there
    IfOnCampus = WAIT.until(EC.element_to_be_clickable((By.XPATH, '//*[@name="sfzx"]/div/div[1]/span/i')))
    IfOnCampus.click()
    print("You've chose YES on IfOnCampus")

    Position = WAITPos.until(EC.element_to_be_clickable((By.XPATH, '//*[@placeholder="点击获取地理位置"]')))
    Position.click()
    print("Obtained your postion successfully")
    time.sleep(2)
    flg = 0

    # browser.execute_script("window.scrollTo(0, 100000);")
    for k in range(0, 5):
        try:
            HaveDone = WAIT.until(EC.presence_of_element_located((By.XPATH, '//*[@class="wapcf-btn-qx"]')))
            print("Finished")
            browser.quit()
            ExitOrNot = 1
        except:
            pass
        if ExitOrNot==1:
            sys.exit()

        Sbmt1 = WAIT.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="footers"]/a')))
        # Sbmt1.click()
        browser.execute_script("arguments[0].click();", Sbmt1)

        Sbmt2 = WAIT.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="wapcf-btn wapcf-btn-ok"]')))
        Sbmt2.click()

        chngimg =  WAIT.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="wapat-title-img"]/span')))
        chngimg.click()

        # element = browser.find_element_by_xpath('//img[@src="/backend/default/code"]')
        element = browser.find_element_by_xpath('//img[@alt=""]')
        # windowsize = browser.get_window_size()
        # x, y = element.location.values() # x = element.location.get('x') # y = element.location.get('y')
        x = 617; y = 243
        # x = 819; y = 337 # nonheadless使用
        h, w = element.size.values()
        # Up to the setting of your screen
        # h = h*1.5; w = w*1.5 # nonheadless使用

        time.sleep(2)
        image_data = browser.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(image_data))
        screenshot.save('screenshot.png')
        result = screenshot.crop((x, y, x+w, y+h))
        result.save('captcha.png')

        captcha = Image.open("captcha.png")
        result = captcha.convert('L')
        result.save('captcha_L.png')

        captcha = Image.open("captcha_L.png")
        capstr = pytesseract.image_to_string(captcha)
        num=1
        capstr = capstr.upper()
        capstr0 = ""
        for c in capstr :
            if c>='A' and c<='Z':
                num+=1
                capstr0+=c
                continue
        capstr0 = capstr0[0:4]
        print(capstr0)

        sendcap = WAIT.until(EC.presence_of_element_located(((By.XPATH, '//*[@placeholder="请输入验证码"]'))))
        sendcap.send_keys(capstr0)

        # time.sleep(60)
        FinlSbmt = WAIT.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="wapat-btn wapat-btn-ok"]')))
        FinlSbmt.click()

        # time.sleep(2)
        ErrSbmt = WAIT.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="hint-show show"]/a')))
        ErrSbmt.click()

    if flg==0 :
        print("Failed")
    browser.quit()
input()

