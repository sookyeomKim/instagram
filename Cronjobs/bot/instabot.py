from datetime import datetime
from time import sleep as original_sleep

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

from Cronjobs.bot.follow_util import follow_util
from Cronjobs.bot.login_util import login_util
from Cronjobs.bot.unfollow_util import unfollow_util


class InstaBot:
    def __init__(self, insta_info, tag_name_list):
        self.insta_info = insta_info
        self.account_id = insta_info.insta_account
        self.account_password = insta_info.insta_passwd
        self.account_seq = insta_info.id
        self.tag_name_list = tag_name_list

        self.webdriver = None
        self.webdriver_wait = None

        self.aborting = False

        self.page_delay = 10

        self.set_selenium_local_session()

    def login(self):
        if not login_util(self.webdriver, self.webdriver_wait, self.account_id, self.account_password):
            self.webdriver.save_screenshot("login_error.png")
            print(self.account_id + ' : 로그인 실패!')
            self.aborting = True
        else:
            print(self.account_id + ' : 로그인 성공!')

        return self

    def follow(self):
        if self.aborting:
            return self

        follow_util(self.webdriver, self.insta_info, self.tag_name_list)
        return self

    def un_follow(self):
        if self.aborting:
            return self

        unfollow_util(self.webdriver,self.webdriver_wait, self.insta_info)
        return self

    def end(self):
        self.webdriver.delete_all_cookies()
        self.webdriver.quit()

        print('')
        print('세션 종료')
        print('-------------')

    def set_selenium_local_session(self):
        try:
            if self.aborting:
                return self
            print("웹드라이버 셋")
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument(
                '--no-sandbox')  # sandbox를 사용하지 않는다 보안 이슈가 있어 권고사항이 아니지만 크롤링목적으로 띄우는 브라우저에서는 딱히 무관한 이슈라고나 할까 무튼 헤드리스 동작시키려면 필수 옵션
            options.add_argument('--disable-gpu')  # gpu를 사용x 윈도우에서는 실행 시 필요한 옵션, for headless
            options.add_argument('--blink-settings=imagesEnabled=false')  # 이미지 방지
            options.add_argument('--window-size=1920x3840')
            options.add_argument("--disable-infobars")  # 정보바 끄기
            options.add_argument("--disable-extensions")  # 확장기능 끄기
            options.add_argument("--disable-dev-shm-usage")  # 리소스 제한 문제 끄기
            options.add_argument('--ignore-certificate-errors')
            options.add_argument(
                "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36")

            self.webdriver = webdriver.Chrome(options=options)
            self.webdriver_wait = WebDriverWait(self.webdriver, self.page_delay)
            print("웹드라이버 셋팅 완료")
            return self
        except Exception as e:
            print(e)
            self.aborting = True
            return self
