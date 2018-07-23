import urllib.parse
from random import randint

from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from InstagramFollowerCrawling.project_info import *
from Message.models import Message
from Cronjobs.bot.util import sleep, diff_second_cal
from ActivityLog.models import ActivityLog

from time import sleep as original_sleep


def filtered_a_tag_list(crawling_list, compare_a_tag_list):
    for a_tag_text in {a_tag.text for a_tag in crawling_list}:
        if a_tag_text not in compare_a_tag_list:
            yield a_tag_text
            compare_a_tag_list.append(a_tag_text)


def tab_close(webdriver):
    webdriver.close()
    webdriver.switch_to_window(webdriver.window_handles[0])


def follow_util(webdriver, insta_info, tag_list):
    try:
        message_list = Message.objects.filter(insta_info=insta_info)

        for tag in tag_list:
            hash_tag = str(tag.tag_name)
            parsed_hash_tag = urllib.parse.quote(hash_tag)
            print(hash_tag + " 팔로우 시작")
            try:
                webdriver.get("https://www.instagram.com/explore/tags/" + parsed_hash_tag)
                sleep(3)

                thumbnail_list = webdriver.find_elements_by_xpath("/html/body/span/section/main/article/div[2]//a")

                thumbnail_url_genarator = (item.get_attribute("href").split("?")[0].split("/")[4] for item in
                                           thumbnail_list)

                while True:
                    try:
                        thumbnail_num = str(next(thumbnail_url_genarator))
                        print(hash_tag + thumbnail_num)
                        webdriver.execute_script(
                            "window.open('https://www.instagram.com/p/" + thumbnail_num + "','_blank');")
                        webdriver.switch_to_window(webdriver.window_handles[1])
                        webdriver.set_window_size(1920, 1080)
                        original_sleep(3)
                        try:
                            prevent_check = False
                            follow_button = webdriver.find_element_by_xpath(
                                "//header/div[2]/div[1]/div[2]/button")

                            if follow_button.text == "팔로잉":
                                print(insta_info.insta_account + hash_tag + thumbnail_num + " - 팔로우 중")
                                tab_close(webdriver)
                                continue
                            else:
                                print(insta_info.insta_account + hash_tag + thumbnail_num + " - 팔로우 가능")

                            user_account = webdriver.find_element_by_xpath(
                                "//article/header/div[2]/div[1]/div[1]/a").text
                            account_check = ActivityLog.objects.filter(insta_info=insta_info,
                                                                       account_id=user_account)

                            if account_check.exists():
                                last_activity_info = list(account_check).pop()
                                if last_activity_info.activity_type == "follow":
                                    diff_second = diff_second_cal(last_activity_info)
                                    if diff_second < 604800:
                                        print(insta_info.insta_account + hash_tag + thumbnail_num + " - 최근 팔로우한 이력이 있음")
                                        tab_close(webdriver)
                                        continue
                                    else:
                                        print(insta_info.insta_account + hash_tag + thumbnail_num + " - 오래전에 팔로우를 했었음")
                                else:
                                    print(insta_info.insta_account + hash_tag + thumbnail_num + " - 최근 언팔로우한 이력이 있음")
                            else:
                                print(insta_info.insta_account + hash_tag + thumbnail_num + " - 팔로우한 이력이 없음")

                            keyword_text = webdriver.find_element_by_xpath(
                                "//article/div[2]/div[1]/ul/li[1]/div/div/div/span")
                            keyword_text = keyword_text.text

                            print(keyword_text)

                            f = open(PREVENT_TEXT_PATH, 'r')
                            get_prevent_keyword = f.readline()
                            f.close()
                            get_prevent_keyword_list = get_prevent_keyword.split(",")
                            if keyword_text is not "":
                                for prevent_keyword in get_prevent_keyword_list:
                                    if keyword_text.__contains__(prevent_keyword):
                                        print(
                                            insta_info.insta_account + hash_tag + thumbnail_num + "금지어 포착 : " + keyword_text + ">" + prevent_keyword)
                                        prevent_check = True

                            if prevent_check:
                                tab_close(webdriver)
                                continue
                            else:
                                print(insta_info.insta_account + hash_tag + thumbnail_num + " - 금지어 없음")

                            user_hash_tag_list = webdriver.find_elements_by_xpath(
                                "//article/div[2]/div[1]/ul/li[1]/div/div/div/span/a")

                            f = open(PREVENT_TEXT_PATH, 'r')
                            get_prevent_hash_tag = f.readline()
                            get_prevent_hash_tag_list = get_prevent_hash_tag.split(",")
                            f.close()
                            for user_hash_tag in (user_hash_tag.text for user_hash_tag in user_hash_tag_list):
                                user_hash_tag = str(user_hash_tag).replace("#", "")
                                if user_hash_tag in get_prevent_hash_tag_list:
                                    print(
                                        insta_info.insta_account + hash_tag + thumbnail_num + "금지 해쉬태그 포착" + " - " + hash_tag)
                                    prevent_check = True
                                    break

                            if prevent_check:
                                tab_close(webdriver)
                                continue
                            else:
                                print(insta_info.insta_account + hash_tag + thumbnail_num + " - 금지 해쉬태그 없음")

                        except Exception as e:
                            print(e)
                            webdriver.save_screenshot(
                                "./save_images/error/" + insta_info.insta_account + hash_tag + thumbnail_num + "error1.png")
                            print("팔로우 못 함 : " + insta_info.insta_account + hash_tag + thumbnail_num)
                            tab_close(webdriver)
                            continue
                        else:
                            try:
                                activity_log = ActivityLog(
                                    activity_type='follow',
                                    account_id=user_account,
                                    insta_info_id=insta_info.id)
                                activity_log.save()
                            except Exception as e:
                                print(e)
                            else:
                                if message_list.exists():
                                    true_n_false = [True, False]
                                    if true_n_false[randint(0, 1)]:
                                        ran_num = randint(1, 4)
                                        ran__list_num = randint(0, 7)
                                        sleep(ran_num)
                                        random_text_list = ["!", "~", "!!", "~!", "!!!", "!@!@", "!_!", "!~", "^^!"]
                                        message = message_list[randint(0, len(message_list) - 1)]
                                        get_textarea = webdriver.find_element_by_css_selector("textarea")
                                        action = ActionChains(webdriver)
                                        action.move_to_element(get_textarea).click().send_keys(
                                            str(message.message_content) + str(
                                                random_text_list[ran__list_num]))
                                        action.send_keys(Keys.ENTER).perform()
                                        ran_num = randint(3, 4)
                                        sleep(ran_num)
                                else:
                                    sleep(5)
                                true_n_false = [True, False]
                                if true_n_false[randint(0, 1)]:
                                    try:
                                        like_button = webdriver.find_element_by_xpath(
                                            "//article/div[2]/section/span[1]/button")
                                        like_button.click()
                                    except:
                                        pass
                                follow_button.click()
                                print("팔로우 함 : " + insta_info.insta_account + hash_tag + thumbnail_num)
                                sleep(10)
                    except Exception as e:
                        print(e)
                        break
                    else:
                        tab_close(webdriver)
            except Exception as e:
                print(e)
                webdriver.save_screenshot(
                    "./save_images/error/" + insta_info.insta_account + "error3.png")
    except Exception as e:
        print("팔로우 루프 에러 \n", e)
    finally:
        print("팔로우 끝")
        sleep(3)
