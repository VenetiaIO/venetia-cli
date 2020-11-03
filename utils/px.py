import requests
from utils.logger import logger

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