from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# 配置ChromeDriver路径和选项
chrome_driver_path = 'C://Users//Administrator//Desktop//chromedriver.exe'
chrome_options = Options()
chrome_options.add_argument('--disable-gpu')  # 如果在Windows操作系统下，可以加上这一行
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

url = "http://jsxdzj.org/index.php?m=content&c=biz_eva&a=index"
driver.get(url)

# 打开浏览器并等待用户手动输入信息
print("Please manually input the required information and navigate to the desired page.")
input("Press Enter to continue after you have completed the manual input...")

page_content = driver.page_source

try:
    while True:
        try:
            while True:
                try:
                    unreviewed_button = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//a[@class='btn_eva' and text()='未评价']"))
                    )
                    unreviewed_button.click()

                    driver.execute_script("arguments[0].click();", unreviewed_button)

                    # 等待弹出层加载完成
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, "eva_div"))
                    )

                    # 找到所有单选按钮并选择值为3的按钮
                    radio_buttons = driver.find_elements(By.XPATH, "//input[@type='radio'][@value='3']")
                    for radio_button in radio_buttons:
                        driver.execute_script("arguments[0].click();", radio_button)

                    # 提交表单
                    submit_button = driver.find_element(By.ID, "eva_form_submit")
                    driver.execute_script("arguments[0].click();", submit_button)

                    # 确认提交成功
                    WebDriverWait(driver, 10).until(
                        EC.alert_is_present()
                    )
                    alert = driver.switch_to.alert
                    print(alert.text)  # 输出弹窗内容
                    alert.accept()

                    time.sleep(2)

                    final_page_content = driver.page_source
                    print(final_page_content)

                except Exception as e:
                    print(f"Error: {e}")
                    break
            try:
                unreviewed_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[@class='a1' and text()='下一页']"))
                )
                unreviewed_button.click()
            except Exception as e:
                print(f"Error: {e}")
                break

        except Exception as e:
            print(f"Error: {e}")
finally:
    driver.quit()
