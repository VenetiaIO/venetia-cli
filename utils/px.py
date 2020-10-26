import requests

class PX:
    @staticmethod
    def snipes():
        headers = {'apiKey': 'aafff4ad-930d-47a4-98f4-666e644c1fc3'}
        r = requests.get('https://px3.herokuapp.com/api/v1/snipes/cookie',headers=headers)
        if r.status_code == 200:
            return r.json()
        else:
            return {"px3":"error","vid":"error"}