from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

from CountLog.models import CountLog
from InstagramFollowerCrawling.project_info import EXECUTABLE_PATH, SERVICE_LOG_PATH, SERVICE_ARGS


class GetCount:
    def __init__(self, insta_info):
        self.insta_info = insta_info

        self.webdriver = None

        self.page_delay = 25

        self.__set_selenium_local_session()

    def __set_selenium_local_session(self):
        print("웹드라이버 셋")
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--blink-settings=imagesEnabled=false')
        options.add_argument('--window-size=1366x768')
        options.add_argument('--disable-gpu')
        options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36")
        options.add_argument('--lang=ko_KR')
        options.add_argument('--dns-prefetch-disable')
        options.add_argument('--no-sandbox')

        chrome_prefs = {
            'intl.accept_languages': 'ko-KR'
        }
        options.add_experimental_option('prefs', chrome_prefs)

        #
        self.webdriver = webdriver.Chrome(options=options)

    def __end(self):
        self.webdriver.delete_all_cookies()
        self.webdriver.quit()
        print('세션 종료')

    def crawling(self):
        try:
            self.webdriver.get("https://www.instagram.com/" + self.insta_info.insta_account)
            get_follower_count = self.webdriver.find_element_by_css_selector(
                "html > body > span > section > main > div > header > section > ul > li:nth-of-type(2) > span > span").text
            get_follow_count = self.webdriver.find_element_by_css_selector(
                "html > body > span > section > main > div > header > section > ul > li:nth-of-type(3) > span > span").text

            print(self.insta_info.insta_account + " : " + get_follow_count + " , " + get_follower_count)

            count_log = CountLog(follow_count=get_follow_count,
                                 follower_count=get_follower_count,
                                 insta_info=self.insta_info, )
            count_log.save()

            self.__end()
        except Exception as e:
            print(e)
            self.__end()
            self.webdriver.save_sreenshot("./save_images/get_count" + self.insta_info.insta_account + ".png")
        else:
            print("크롤링 종료")
            print('-------------')
            print('')
