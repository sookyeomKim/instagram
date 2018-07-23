import pickle
from random import randint

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep as original_sleep

from selenium.webdriver.support.select import Select


def login_util(webdriver, webdriver_wait, account_id, account_password):
    try:
        webdriver.get('https://www.instagram.com')

        original_sleep(2)

        select = Select(webdriver.find_element_by_css_selector('select'))

        select.select_by_value('en')

        original_sleep(2)

        try:
            for cookie in pickle.load(open("cookies/" + account_id + "_cookie.pkl", "rb")):
                webdriver.add_cookie(cookie)
            webdriver.get('https://www.instagram.com')
            original_sleep(2)
        except:
            login_button = webdriver_wait.until(EC.presence_of_element_located((By.XPATH, "//a[text()='Log in']")))
            ActionChains(webdriver).move_to_element(login_button).click().perform()
            original_sleep(2)
            input_username = webdriver_wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@name='username']")))
            login_action = ActionChains(webdriver).move_to_element(input_username).click().send_keys(account_id)
            input_password = webdriver.find_element_by_xpath("//input[@name='password']")
            login_action.move_to_element(input_password).click().send_keys(account_password)
            login_button = webdriver.find_element_by_xpath("//form/span/button[text()='Log in']")
            login_action.move_to_element(login_button).click().perform()
            original_sleep(2)
            pickle.dump(webdriver.get_cookies(), open("cookies/" + account_id + "_cookie.pkl", "wb"))

        original_sleep(randint(1, 3))

        nav = webdriver.find_elements_by_xpath('//nav')

        # 계정 별 한글 설정으로 인해 한번 더 언어 변환
        select = Select(webdriver.find_element_by_css_selector('select'))

        select.select_by_value('en')

        original_sleep(randint(1, 3))

        if len(nav) == 2:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False
