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
        c = loadToken(SITE.upper())
        if c != 'empty':
            return c
        else:
            try:
                cap = loadSettings()
                if cap["captcha"].strip().lower()  == "monster":
                    return capMonster.v2(sitekey, url, proxy, SITE,taskID)
                else:
                    return TwoCaptcha.v2(sitekey, url, proxy, SITE,taskID)
            except Exception as e:
                return None


    @staticmethod
    def Hiddenv2(sitekey, url, proxy, SITE,taskID):
        c = loadToken(SITE.upper())
        if c != 'empty':
            return c
        else:
            try:
                cap = loadSettings()
                if cap["captcha"].strip().lower()  == "monster":
                    logger.error(SITE,taskID,'CapMonster does not support V2 Invisible. Attempting to solve with 2Captcha')
                    return TwoCaptcha.Hiddenv2(sitekey, url, proxy, SITE,taskID)
                else:
                    return TwoCaptcha.Hiddenv2(sitekey, url, proxy, SITE,taskID)
            except:
                return None


    @staticmethod
    def v3(sitekey, url, proxy, SITE,taskID):
        c = loadToken(SITE.upper())
        if c != 'empty':
            return c
        else:
            try:
                cap = loadSettings()
                if cap["captcha"].strip().lower() == "monster":
                    return capMonster.v3(sitekey, url, proxy, SITE,taskID)
                else:
                    return TwoCaptcha.v3(sitekey, url, proxy, SITE,taskID)
            
            except Exception as e:
                print(e)
                return None

    @staticmethod
    def hcaptcha(sitekey, url, proxy, SITE,taskID):
        c = loadToken(SITE.upper())
        if c != 'empty':
            return c
        else:
            try:
                cap = loadSettings()
                if cap["captcha"].strip().lower()  == "monster":
                    return capMonster.hcaptcha(sitekey, url, proxy, SITE,taskID)
                else:
                    return TwoCaptcha.hcaptcha(sitekey, url, proxy, SITE,taskID)
            except:
                return None

    @staticmethod
    def geetest(gt, challenge, apiServer, pageurl, proxy, SITE, taskID):
        c = loadToken(SITE.upper())
        if c != 'empty':
            return c
        else:
            try:
                cap = loadSettings()
                if cap["captcha"].strip().lower() == "monster":
                    logger.error(SITE,taskID,'CapMonster does not support Geetest. Attempting to solve with 2Captcha')
                    return TwoCaptcha.hcaptcha(gt, challenge, apiServer, pageurl, proxy, SITE,taskID)
                else:
                    return TwoCaptcha.hcaptcha(gt, challenge, apiServer, pageurl, proxy, SITE,taskID)
            except:
                return None

    
    @staticmethod
    def menuV2(sitekey, url, proxy, taskID, SITE):
        try:
            cap = loadSettings()
            if cap["captcha"].strip().lower() == "monster":
                # Cap monste doesnt support geetest yet
                return capMonster.menuV2(sitekey, url, proxy, taskID, SITE)
            else:
                return TwoCaptcha.menuV2(sitekey, url, proxy, taskID, SITE)
        except:
            return None

    @staticmethod
    def menuV3(sitekey, url, proxy, taskID, SITE):
        try:
            cap = loadSettings()
            if cap["captcha"].strip().lower() == "monster":
                # Cap monste doesnt support geetest yet
                return capMonster.menuV3(sitekey, url, proxy, taskID, SITE)
            else:
                return TwoCaptcha.menuV3(sitekey, url, proxy, taskID, SITE)
        except:
            return None

    @staticmethod
    def menuV2_invisible(sitekey, url, proxy, taskID, SITE):
        try:
            cap = loadSettings()
            if cap["captcha"].strip().lower()  == "monster":
                # logger.error(SITE,taskID,'CapMonster does not support V2 Invisible. Attempting to solve with 2Captcha')
                return TwoCaptcha.menuHiddenv2(sitekey, url, proxy, SITE,taskID)
            else:
                return TwoCaptcha.menuHiddenv2(sitekey, url, proxy, SITE,taskID)
        except:
            return None


def loadToken(SITE):
  try:
    with open('./data/captcha/tokens.json','r') as tokens:

        tokens = json.loads(tokens.read())

        if len(tokens[SITE]) > 0:
            t = tokens[SITE][0]
            tokens[SITE].pop(0)
            
            with open('./data/captcha/tokens.json','w') as output:
                json.dump(tokens,output)

            return t["token"]
        
        else:
            return 'empty'
  except:
    return 'empty'