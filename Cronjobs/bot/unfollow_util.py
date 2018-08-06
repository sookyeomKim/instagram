import datetime
from random import randint

from django.utils.timezone import localtime
from time import sleep as original_sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from Cronjobs.bot.util import sleep, scroll_bottom_move

from ActivityLog.models import ActivityLog


def unfollow_util(webdriver, webdriver_wait, insta_info):
    print("언팔로우 시작")
    try:

        webdriver.get("https://www.instagram.com/" + str(insta_info.insta_account))
        print("프로필 이동 완료")
        sleep(2)
        util_list = webdriver_wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "html > body > span > section > main > div > header > section > ul")))

        follower_list_button = util_list.find_element_by_css_selector("li:nth-of-type(2) a")
        follower_list_button.click()
        print("팔로워 팝업창 오픈")

        sleep(2)

        # follower_list_scroll_wrap = webdriver.find_element_by_xpath("/html/body/div[4]/div/div[2]/div/div[2]")
        follower_list_scroll_wrap = webdriver.find_element_by_css_selector(
            "html > body > div:nth-of-type(3) > div > div:nth-of-type(2) > div > div:nth-of-type(2)")
        scroll_bottom_move(webdriver, follower_list_scroll_wrap, 70)
        print("팔로워 팝업창 스크롤 이동")

        sleep(2)
        followers_el_list = follower_list_scroll_wrap.find_elements_by_css_selector(
            "li > div > div:nth-of-type(1) > div > div:nth-of-type(1) > a")

        follwer_list = []
        for follower_el in followers_el_list:
            follower_user_account = follower_el.text
            follwer_list.append(follower_user_account)
        print("팔로워 리스트 생성")
        print(str(insta_info.insta_account) + "\n", len(follwer_list))
        webdriver.execute_script("window.history.go(-1)")

        sleep(2)

        ##############

        follow_list_button_el = util_list.find_element_by_css_selector(
            "li:nth-of-type(3) a")
        follow_list_button_el.click()
        print("팔로우 팝업창 오픈")

        sleep(2)

        follow_list_scroll_wrap = webdriver.find_element_by_css_selector(
            "html > body > div:nth-of-type(3) > div > div:nth-of-type(2) > div > div:nth-of-type(2)")
        scroll_bottom_move(webdriver, follow_list_scroll_wrap, 35)
        print("팔로우 팝업창 스크롤 이동")

        sleep(2)

        follow_list = follow_list_scroll_wrap.find_elements_by_css_selector("li")
        print("팔로우 리스트 생성")

        print(str(insta_info.insta_account) + "\n", len(follow_list))
        break_count = 0
        sleep_count = 0
        sleep_count_limit = randint(3, 7)
        while follow_list:
            try:
                if break_count >= 10:
                    print(str(insta_info.insta_account) + "언팔 루프 멈춤")
                    break
                following_user = follow_list.pop()
                follow_user_account = following_user.find_elements_by_css_selector("a")[1].text
                if follow_user_account not in follwer_list:
                    get_account = ActivityLog.objects.filter(insta_info=insta_info, account_id=follow_user_account)
                    if get_account.exists():
                        get_account = get_account[::-1]
                        get_account = get_account[0]
                        if get_account.activity_type is not "unfollow":
                            try:
                                following_button = following_user.find_element_by_css_selector("button")
                                if following_button.text == "Follow":
                                    try:
                                        activity_log = ActivityLog(
                                            activity_type='unfollow',
                                            account_id=get_account.account_id,
                                            insta_info_id=insta_info.id)
                                        activity_log.save()
                                    except Exception as e:
                                        print(e)
                                    continue

                                now_date_time = datetime.datetime.now()
                                now_date_time = datetime.datetime.strptime(now_date_time.strftime('%Y-%m-%d %H:%M:%S'),
                                                                           '%Y-%m-%d %H:%M:%S')
                                activity_date_time = localtime(get_account.create_date)
                                activity_date_time = datetime.datetime.strptime(
                                    activity_date_time.strftime('%Y-%m-%d %H:%M:%S'),
                                    '%Y-%m-%d %H:%M:%S')
                                diff_time = now_date_time - activity_date_time
                                diff_second = int(diff_time.total_seconds())
                                if diff_second > 10800 or get_account.activity_type == "init":
                                    original_sleep(randint(0, 2))
                                    following_button.click()
                                    original_sleep(1)

                                    try:
                                        follow_cancel_button = webdriver.find_element_by_css_selector(
                                            "html > body > div:nth-of-type(4) > div > div > div > div:nth-of-type(3) > button:nth-of-type(1)")
                                        follow_cancel_button.click()
                                    except:
                                        pass
                                    original_sleep(2)
                                    button_text = following_user.find_element_by_css_selector("button").text
                                    if button_text == "Follow":
                                        activity_log = ActivityLog(
                                            activity_type='unfollow',
                                            account_id=get_account.account_id,
                                            insta_info_id=insta_info.id)
                                        activity_log.save()
                                        print(str(follow_user_account) + "언팔 완료 - " + str(insta_info.insta_account))
                                        sleep_count = sleep_count + 1
                                    else:
                                        webdriver.save_screenshot(
                                            "./save_images/unfollow/error/" + str(
                                                insta_info.insta_account) + "error.png")
                                        print(str(follow_user_account) + "엇 락이 의심된다 - " + str(insta_info.insta_account))

                                else:
                                    print(str(follow_user_account) + "아직 시간이 안 됨 - " + str(insta_info.insta_account))
                                    break_count = break_count + 1
                                    continue

                            except Exception as e:
                                print(e)
                        else:
                            print(str(follow_user_account) + "어라 이미 언팔한 녀석이네? - " + str(insta_info.insta_account))

                    else:
                        print(str(follow_user_account) + "는 팔로우 이력이 없음 - " + str(insta_info.insta_account))
                        # 다음 언팔 진행 때 이용
                        activity_log = ActivityLog(
                            activity_type="init",
                            account_id=follow_user_account,
                            insta_info_id=insta_info.id)
                        activity_log.save()
                        continue
                else:
                    continue

                if sleep_count >= sleep_count_limit:
                    sleep_count = 0
                    sleep_count_limit = randint(2, 5)
                    ran_num = randint(60, 120)
                    print(str(insta_info.insta_account) + " " + str(ran_num) + "초만 언팔 쉼")
                    sleep(ran_num)
                else:
                    sleep(randint(10, 15))
            except Exception as e:
                print(e)
                break
    except Exception as e:
        print("언팔로우 루프 에러 \n", e)
        webdriver.save_screenshot("./save_images/unfollow/error/" + str(insta_info.insta_account) + "error.png")
    finally:
        print("언팔로우 끝")
        sleep(3)
