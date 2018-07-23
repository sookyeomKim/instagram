#!/usr/bin/env python3
import os

import concurrent.futures
import django
import sys

sys.path.append("/Users/kimsookyeom/PycharmProjects/InstagramFollowerCrawling")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "InstagramFollowerCrawling.settings")
django.setup()

from InstaInfo.models import InstaInfo
from Cronjobs.bot.get_count import GetCount


def __try_multiple_operations(insta_info):
    GetCount(insta_info).crawling()


if __name__ == '__main__':
    insta_info_list = InstaInfo.objects.filter(onoff_trigger=True)
    executor = concurrent.futures.ThreadPoolExecutor(10)
    futures = [executor.submit(__try_multiple_operations, insta_info) for insta_info in insta_info_list]
    concurrent.futures.wait(futures, 1)
