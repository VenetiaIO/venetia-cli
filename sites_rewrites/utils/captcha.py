import requests
import time
import json
from utils.logger import logger
import random
import json
from utils.capMonster import capMonster
from utils.twoCaptcha import TwoCaptcha

async def loadSettings():
    with open(f'./data/config.json') as settings:
        settings = json.loads(settings.read())
        return settings


class captcha:
    @staticmethod
    async def v2(sitekey, url, proxy, SITE,taskID):
        try:
            cap = await loadSettings()
            if cap["captcha"].lower()  == "monster":
                return await capMonster.v2(sitekey, url, proxy, SITE,taskID)
            else:
                return await TwoCaptcha.v2(sitekey, url, proxy, SITE,taskID)
        except:
            return None


    @staticmethod
    async def Hiddenv2(sitekey, url, proxy, SITE,taskID):
        try:
            cap = await loadSettings()
            if cap["captcha"].lower()  == "monster":
                logger.error(SITE,taskID,'CapMonster does not support V2 Invisible. Attempting to solve with 2Captcha')
                return await TwoCaptcha.Hiddenv2(sitekey, url, proxy, SITE,taskID)
            else:
                return await TwoCaptcha.Hiddenv2(sitekey, url, proxy, SITE,taskID)
        except:
            return None


    @staticmethod
    async def v3(sitekey, url, proxy, SITE,taskID):
        try:
            cap = await loadSettings()
            if cap["captcha"].lower() == "monster":
                return await capMonster.v3(sitekey, url, proxy, SITE,taskID)
            else:
                return await TwoCaptcha.v3(sitekey, url, proxy, SITE,taskID)
        
        except:
            return None

    @staticmethod
    async def hcaptcha(sitekey, url, proxy, SITE,taskID):
        try:
            cap = await loadSettings()
            if cap["captcha"].lower()  == "monster":
                return await capMonster.hcaptcha(sitekey, url, proxy, SITE,taskID)
            else:
                return await TwoCaptcha.hcaptcha(sitekey, url, proxy, SITE,taskID)
        except:
            return None

    @staticmethod
    async def geetest(gt, challenge, apiServer, pageurl, proxy, SITE, taskID):
        try:
            cap = await loadSettings()
            if cap["captcha"].lower()  == "monster":
                logger.error(SITE,taskID,'CapMonster does not support Geetest. Attempting to solve with 2Captcha')
                return await TwoCaptcha.hcaptcha(gt, challenge, apiServer, pageurl, proxy, SITE,taskID)
            else:
                return await TwoCaptcha.hcaptcha(gt, challenge, apiServer, pageurl, proxy, SITE,taskID)
        except:
            return None

    
    @staticmethod
    async def menuV2(sitekey, url, proxy, taskID, SITE):
        try:
            cap = await loadSettings()
            if cap["captcha"].lower() == "monster":
                # Cap monste doesnt support geetest yet
                return await capMonster.menuV2(sitekey, url, proxy, taskID, SITE)
            else:
                return await TwoCaptcha.menuV2(sitekey, url, proxy, taskID, SITE)
        except:
            return None