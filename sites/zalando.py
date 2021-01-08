import requests
from bs4 import BeautifulSoup
import datetime
import threading
import random
import sys
import time
import re
import json
import os
import base64
import cloudscraper
import string
from urllib3.exceptions import HTTPError

from utils.logger import logger
from utils.webhook import discord
from utils.log import log
from utils.functions import (loadSettings, loadProfile, loadProxy, createId, loadCookie, loadToken, sendNotification, injection,storeCookies, updateConsoleTitle)
SITE = 'ZALANDO'


class ZALANDO:
    def __init__(self,task,taskName,rowNumber):
        self.task = task
        self.session = requests.session()
        self.taskID = taskName

        twoCap = loadSettings()["2Captcha"]
        # self.session = cloudscraper.create_scraper(
            # requestPostHook=injection,
            # sess=self.sess,
            # interpreter='nodejs',
            # browser={
                # 'browser': 'chrome',
                # 'mobile': False,
                # 'platform': 'windows'
                # 'platform': 'darwin'
            # },
            # captcha={
                # 'provider': '2captcha',
                # 'api_key': twoCap
            # }
        # )
        
        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)

        self.collect()