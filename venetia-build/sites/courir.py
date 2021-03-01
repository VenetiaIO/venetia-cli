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
import urllib.parse
from urllib3.exceptions import HTTPError


from utils.logger import logger
from utils.webhook import discord
from utils.captcha import captcha
from utils.datadome import datadome
from utils.functions import (loadSettings, loadProfile, loadProxy, createId, loadCookie, loadToken)
SITE = 'COURIR'

class COURIR:
    def __init__(self,task,taskName,rowNumber):
        self.task = task
        self.session = requests.session()
        self.taskID = taskName

        self.session.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        }
        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
        self.collect()
    

    def collect(self):
        logger.prepare(SITE,self.taskID,'Getting product page...')
        try:
            retrieve = self.session.get(self.task["PRODUCT"])
        except:
            logger.error(SITE,self.taskID,'Connection Error. Retrying...')
            #self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID,SITE)
            time.sleep(int(self.task["DELAY"]))
            self.collect()
        print(retrieve, retrieve.url)

        if 'DDUser' in retrieve.url:
            logger.info(SITE,self.taskID,'Challenge Found, Solving...')
            del self.session.cookies["datadome"]
            self.session.cookies["datadome"] = courir_datadome(self.session.proxies,self.taskID)
            print(self.session.cookies)
            self.collect()
        else:
            if retrieve.status_code == 200:
                logger.success(SITE,self.taskID,'Got product page')
                
            else:
                logger.error(SITE,self.taskID,'Failed to get product page. Retrying...')
                time.sleep(int(self.task["DELAY"]))
                self.collect()


