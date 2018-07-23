import datetime
from random import gauss, randint, uniform
from time import sleep as original_sleep
from django.utils.timezone import localtime

# Amount of variance to be introduced
# i.e. random time will be in the range: TIME +/- STDEV %
STDEV = 0.5


def randomize_time(mean):
    allowed_range = mean * STDEV
    stdev = allowed_range / 3  # 99.73% chance to be in the allowed range

    t = 0
    while abs(mean - t) > allowed_range:
        t = gauss(mean, stdev)

    return t


def sleep(t):
    # print(randomize_time(t))
    original_sleep(randomize_time(t))


def scroll_bottom_move(browser, element, count):
    for i in range(count):
        browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", element)
        sleep(uniform(2, 2.5))
    return


def diff_second_cal(get_account):
    now_date_time = datetime.datetime.now()
    now_date_time = datetime.datetime.strptime(now_date_time.strftime('%Y-%m-%d %H:%M:%S'),
                                               '%Y-%m-%d %H:%M:%S')
    activity_date_time = localtime(get_account.create_date)
    activity_date_time = datetime.datetime.strptime(
        activity_date_time.strftime('%Y-%m-%d %H:%M:%S'),
        '%Y-%m-%d %H:%M:%S')
    diff_time = now_date_time - activity_date_time
    diff_second = int(diff_time.total_seconds())
    return diff_second
