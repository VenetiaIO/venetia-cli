import requests
from utils.logger import logger

class AKAMAI:

    @staticmethod
    def footasylum(session, taskID):
        headers = {'apiKey': '01836a61-ddd6-4062-a8e4-79edd8f0a5f1'}
        if session.proxies != None: params = {"proxies":session.proxies}
        if session.proxies == None: params = {}
        
        # https://akamai.invincible.services/api/v1/abck/footasylum
        r = requests.get('https://akamai.invincible.services/api/v1/abck/footasylum',headers=headers,params=params)
        if r.status_code == 200:
            logger.secondary('FOOTASYLUM',taskID,'Successfully Generated Akamai Cookies')
            return r.json()
        else:
            return {"cookies":"error"}

