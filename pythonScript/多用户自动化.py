from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm
import time
import csv
import pandas as pd

# 配置ChromeDriver
chrome_driver_path = 'C://Users//Administrator//Desktop//chromedriver.exe'
chrome_options = Options()
chrome_options.add_argument('--disable-gpu')
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# 学生信息文件
csv_file_path = "pythonScript\example.csv"
students_file = pd.read_csv(csv_file_path)

login_url = "http://jsxdzj.org/index.php?m=content&c=biz_eva&a=index"

def login(student_id, student_name):
    """自动填写学生 ID 和姓名，并选择学校登录"""
    driver.get(login_url)

    try:
        # 1. 选择“学生”身份
        student_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'role=2')]"))
        )
        student_button.click()
        time.sleep(1)  # 等待页面加载

        # 2. 选择“苏州”
        suzhou_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'cmd=school&city=苏州')]"))
        )
        suzhou_button.click()
        time.sleep(1)

        # 3. 选择“苏州分院”
        suzhou_college_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'cmd=login&school=27')]"))
        )
        suzhou_college_button.click()
        time.sleep(2)  # 等待跳转到输入页面

        # 4. 填写学号和姓名
        student_id_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "mobile"))
        )
        name_input = driver.find_element(By.NAME, "name")
        submit_button = driver.find_element(By.ID, "dosubmit")

        student_id_input.clear()
        student_id_input.send_keys(str(student_id))  # ✅ 修正错误

        name_input.clear()
        name_input.send_keys(student_name)  # ✅ 修正错误

        # 5. 点击“开始评价”
        submit_button.click()

        # 6. 确保成功跳转到评价页面
        WebDriverWait(driver, 10).until(EC.url_contains("biz_eva"))
        print(f"学生 {student_name} 登录成功")

    except Exception as e:
        print(f"登录失败: {e}")
        return False
    return True

def evaluate():
    """自动完成评价流程"""

    max_pages = 12  # 最多评价 12 页
    current_page = 0  # 当前页数

    while current_page < max_pages:
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

                    time.sleep(1)

                except Exception as e:
                    print(f"Error: {e}")
                    break
            try:
                unreviewed_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[@class='a1' and text()='下一页']"))
                )
                unreviewed_button.click()
                current_page += 1
            except Exception as e:
                print(f"Error: {e}")
                break

        except Exception as e:
            print(f"Error: {e}")

def process_students():
    """循环处理多个学生"""
    for index, row in tqdm(students_file.iterrows(), total=len(students_file), desc="学生评价进度"):
        student_id = row['ID']
        student_name = row['Name']

        print(f"处理学生: {student_name} ({student_id})")

        # 登录
        if not login(student_id, student_name):
            continue

        # 评价
        evaluate()


# 执行
process_students()

# 关闭浏览器
driver.quit()
