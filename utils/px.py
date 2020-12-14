import requests
from utils.logger import logger
import base64
from utils.functions import loadSettings

class PX:

    @staticmethod
    def snipes(session, link, taskID):
        headers = {'apiKey': 'aafff4ad-930d-47a4-98f4-666e644c1fc3'}
        if session.proxies != None: params = {"proxies":session.proxies}
        if session.proxies == None: params = {}

        params["link"] = link
        
        r = requests.get('https://px.invincible.services/api/v1/px/snipes',headers=headers,params=params)
        if r.status_code == 200:
            logger.secondary('SNIPES',taskID,'Successfully Generated PX Cookies')
            return r.json()
        else:
            return {"px3":"error","vid":"error"}


    @staticmethod
    def solebox(session, link, taskID):
        headers = {'apiKey': 'aafff4ad-930d-47a4-98f4-666e644c1fc3'}
        if session.proxies != None: params = {"proxies":session.proxies}
        if session.proxies == None: params = {}

        params["link"] = link
        
        r = requests.get('https://px.invincible.services/api/v1/px/solebox',headers=headers,params=params)
        if r.status_code == 200:
            logger.secondary('SOLEBOX',taskID,'Successfully Generated PX Cookies')
            return r.json()
        else:
            return {"px3":"error","vid":"error"}


    @staticmethod
    def captchaSolve(session, link, taskID, site, blockedUrl, cs, sid):
        headers = {'apiKey': 'aafff4ad-930d-47a4-98f4-666e644c1fc3'}
        if session.proxies != None: params = {"proxies":session.proxies}
        if session.proxies == None: params = {}

        params["link"] = link
        params["twoCapKEy"] = loadSettings()["2Captcha"]

        encoded = base64.b64encode(bytes(str(blockedUrl), 'utf-8'))
        blockedUrlEncoded = str(encoded, 'utf8')
        
        r = requests.get(f'https://px.invincible.services/api/v1/px-captcha/{site.lower()}/{blockedUrlEncoded}/{cs}/{sid}',headers=headers,params=params)
        if r.status_code == 200:
            logger.secondary(site.upper(),taskID,'Successfully Solved PX Captcha')
            return r.json()
        else:
            return {"px3":"error","vid":"error"}