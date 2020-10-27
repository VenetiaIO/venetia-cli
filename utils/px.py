import requests

class PX:
    @staticmethod
    def snipes(session, link):
        headers = {'apiKey': 'aafff4ad-930d-47a4-98f4-666e644c1fc3'}
        if session.proxies != None: params = {"proxies":session.proxies}
        if session.proxies == None: params = {}

        params["link"] = link
        
        r = requests.get('https://px3.herokuapp.com/api/v1/px/snipes',headers=headers,params=params)
        if r.status_code == 200:
            return r.json()
        else:
            return {"px3":"error","vid":"error"}