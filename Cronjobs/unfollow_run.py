#!/usr/bin/env python3

import os
import urllib.parse

import concurrent.futures
import django
import sys

sys.path.append("/Users/kimsookyeom/PycharmProjects/InstagramFollowerCrawling")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "InstagramFollowerCrawling.settings")
django.setup()

from HashTag.models import HashTag
from InstaInfo.models import InstaInfo

from Cronjobs.bot.instabot import InstaBot


def __try_multiple_operations(insta_info):
    hash_tag_list = HashTag.objects.filter(insta_info__insta_account=insta_info)
    InstaBot(insta_info=insta_info,
             tag_name_list=hash_tag_list) \
        .login() \
        .un_follow() \
        .end()


if __name__ == '__main__':
    insta_info_list = InstaInfo.objects.filter(onoff_trigger=True)
    executor = concurrent.futures.ThreadPoolExecutor(10)
    futures = [executor.submit(__try_multiple_operations, insta_info) for insta_info in insta_info_list]
    concurrent.futures.wait(futures, 1)
    # for insta_info in insta_info_list:
    #     hash_tag_list = HashTag.objects.filter(insta_info__insta_account=insta_info)
    #     InstaBot(account_id=insta_info.insta_account, account_password=insta_info.insta_passwd,
    #              account_seq=insta_info.id,
    #              tag_name_list=hash_tag_list) \
    #         .login() \
    #         .un_follow() \
    #         .end()
    # for hash_tag in hash_tag_list:
    #     InstaBot(account_id=insta_info.insta_account, account_password=insta_info.insta_passwd,
    #              account_seq=insta_info.id,
    #              tag_name=hash_tag) \
    #         .login() \
    #         .follow() \
    #         .end()
    # executor = concurrent.futures.ThreadPoolExecutor(10)
    # futures = [executor.submit(__try_multiple_operations, insta_info) for insta_info in insta_info_list]
    # concurrent.futures.wait(futures, 1)
