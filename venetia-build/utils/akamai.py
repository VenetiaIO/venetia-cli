import requests
from utils.logger import logger

class AKAMAI:

    @staticmethod
    def offspring(session, taskID):
        headers = {'apiKey': 'b385308c-04aa-45f1-9e6c-14e17282ab68'}
        if session.proxies != None: params = {"proxies":session.proxies}
        if session.proxies == None: params = {}
        
        # https://akamai.invincible.services/api/v1/abck/footasylum
        r = requests.get('https://akamai.invincible.services/api/v1/abck/offspring',headers=headers,params=params)
        if r.status_code == 200:
            logger.success('Offspring',taskID,'Successfully Generated Akamai Cookies')
            return r.json()
        else:
            return {"_abck":"error"}

    @staticmethod
    def converse(session, taskID):
        headers = {'apiKey': 'b385308c-04aa-45f1-9e6c-14e17282ab68'}
        if session.proxies != None: params = {"proxies":session.proxies}
        if session.proxies == None: params = {}
        
        # https://akamai.invincible.services/api/v1/abck/footasylum
        r = requests.get('https://akamai.loca.lt/api/v1/converse',headers=headers,params=params)
        if r.status_code == 200:
            logger.success('Converse',taskID,'Successfully Generated Akamai Cookies')
            return r.json()
        else:
            return {"_abck":"error"}

