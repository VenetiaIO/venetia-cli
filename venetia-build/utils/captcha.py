import requests
import time
import json
from utils.logger import logger
import random
import json
from utils.capMonster import capMonster
from utils.twoCaptcha import TwoCaptcha

def loadSettings():
    with open(f'./data/config.json') as settings:
        settings = json.loads(settings.read())
        return settings


class captcha:
    @staticmethod
    def v2(sitekey, url, proxy, SITE,taskID):
        try:
            if loadSettings()["captcha"].lower() == "monster":
                return capMonster.v2(sitekey, url, proxy, SITE,taskID)
            else:
                return TwoCaptcha.v2(sitekey, url, proxy, SITE,taskID)
        except:
            return None


    @staticmethod
    def Hiddenv2(sitekey, url, proxy, SITE,taskID):
        try:
            if loadSettings()["captcha"].lower() == "monster":
                logger.error(SITE,taskID,'CapMonster does not support V2 Invisible. Attempting to solve with 2Captcha')
                return TwoCaptcha.Hiddenv2(sitekey, url, proxy, SITE,taskID)
            else:
                return TwoCaptcha.Hiddenv2(sitekey, url, proxy, SITE,taskID)
        except:
            return None


    @staticmethod
    def v3(sitekey, url, proxy, SITE,taskID):
        try:
            if loadSettings()["captcha"].lower() == "monster":
                return capMonster.v3(sitekey, url, proxy, SITE,taskID)
            else:
                return TwoCaptcha.v3(sitekey, url, proxy, SITE,taskID)
        
        except:
            return None

    @staticmethod
    def hcaptcha(sitekey, url, proxy, SITE,taskID):
        try:
            if loadSettings()["captcha"].lower() == "monster":
                return capMonster.hcaptcha(sitekey, url, proxy, SITE,taskID)
            else:
                return TwoCaptcha.hcaptcha(sitekey, url, proxy, SITE,taskID)
        except:
            return None

    @staticmethod
    def geetest(gt, challenge, apiServer, pageurl, proxy, SITE, taskID):
        try:
            if loadSettings()["captcha"].lower() == "monster":
                logger.error(SITE,taskID,'CapMonster does not support Geetest. Attempting to solve with 2Captcha')
                return TwoCaptcha.hcaptcha(gt, challenge, apiServer, pageurl, proxy, SITE,taskID)
            else:
                return TwoCaptcha.hcaptcha(gt, challenge, apiServer, pageurl, proxy, SITE,taskID)
        except:
            return None

    
    @staticmethod
    def menuV2(sitekey, url, proxy, taskID, SITE):
        try:
            if loadSettings()["captcha"].lower() == "monster":
                # Cap monste doesnt support geetest yet
                return capMonster.menuV2(sitekey, url, proxy, taskID, SITE)
            else:
                return TwoCaptcha.menuV2(sitekey, url, proxy, taskID, SITE)
        except:
            return None