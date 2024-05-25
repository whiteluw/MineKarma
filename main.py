import os
import random
import time
import yaml
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def generate_random_number():
    return ''.join(random.choices('0123456789', k=10))

def load_config():
    config_file_path = 'config.yaml'
    if not os.path.exists(config_file_path):
        config = {
            'account': '',
            'password': '',
            'editpage': '',
            'cishu': 10
        }
        with open(config_file_path, 'w') as file:
            yaml.dump(config, file)
    with open(config_file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def save_config(config):
    config_file_path = 'config.yaml'
    with open(config_file_path, 'w') as file:
        yaml.dump(config, file, sort_keys=False, default_flow_style=False)

def login(driver, account, password):
    driver.get("https://www.wikidot.com/default--flow/login__LoginPopupScreen?originSiteId=648902&openerUri=https://www.wikidot.com")
    print("[INFO]正在执行账号登录...")
    username_input = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//*[@id='html-body']/div[2]/div[2]/div/div[1]/div[1]/form/div[1]/div/input"))
    )
    username_input.send_keys(account)
    password_input = driver.find_element(By.XPATH, "//*[@id='html-body']/div[2]/div[2]/div/div[1]/div[1]/form/div[2]/div/input")
    password_input.send_keys(password)
    sign_in_button = driver.find_element(By.XPATH, "//*[@id='html-body']/div[2]/div[2]/div/div[1]/div[1]/form/div[4]/div/button")
    sign_in_button.click()
    WebDriverWait(driver, 20).until(EC.url_changes("https://www.wikidot.com"))
    print("[INFO]登录完成，正在前往编辑页")

def edit_page(driver, editpage):
    driver.get(editpage)
    print("[INFO]正在编辑页面")
    edit_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "edit-button"))
    )
    edit_button.click()
    textarea = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, "edit-page-textarea"))
    )
    textarea.clear()
    random_number = generate_random_number()
    textarea.send_keys(random_number)
    save_button = driver.find_element(By.ID, "edit-save-button")
    save_button.click()
    print(f"[INFO]编辑页面成功")
    time.sleep(1)
    print("[INFO]Saving page...")
    time.sleep(4)

def main():
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')
    options.add_argument('--start-maximized')
    options.add_argument('--blink-settings=imagesEnabled=false')
    options.add_argument('--log-level=2')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(options=options)

    config = load_config()

    editpage = config['editpage']
    account = config['account']
    password = config['password']
    cishu = config['cishu']

    try:
        os.system("cls")
        print ("-"*30)
        print ("配置文件")
        print ("账号："+str(account))
        print ("密码："+"*"*10)
        print ("编辑页："+str(editpage))
        print ("循环次数："+str(cishu))
        print ("预计完成时间："+str(float((cishu*7+10)/60))+"min")
        print ("MineKarma Power by whitelu")
        print ("-"*30)
        login(driver, account, password)
        for i in range(1,cishu+1):
            print("-"*30)
            print("[INFO]开始第"+str(i)+"次编辑")
            edit_page(driver, editpage)
            print("[INFO]第"+str(i)+"次编辑结束")
        print("-"*30)
    except Exception as e:
        exception_message = str(e)
        if "invalid argument" in exception_message:
            print("[WARN]程序在登录后发生异常，请检查编辑页面链接地址或是否正确！")
            print ("-"*30)
        elif "Stacktrace" in exception_message:
            print("[WARN]程序无编辑页面的权限，请检查账号密码是否正确或页面是否存在编辑锁！")
            print ("-"*30)
        else:
            print(f"[WARN]发生异常: {exception_message}")
    finally:
        print("[EXIT]程序运行结束，程序退出")
        driver.quit()
        os.system("pause")
        print ("-"*30)

if __name__ == "__main__":
    main()
