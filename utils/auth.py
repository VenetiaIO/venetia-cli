import requests

headers = {"apiKey":"27acc458-f01a-48f8-88b8-06583fb39056"}

class auth:
    @staticmethod
    def auth(key, uuid):
        checkKey = requests.post('http://venetiacli.io/api/get/key',headers=headers,json={"key":key})
        if checkKey.status_code == 423:
            validateMachine = requests.post('http://venetiacli.io/api/machine/validate',headers=headers,json={"key":key,"machine":uuid})
            if validateMachine.status_code == 200:
                return {'STATUS':1,'MESSAGE':'Key Authorised'}
            if validateMachine.status_code == 201:
                requests.post('http://venetiacli.io/api/machine/update',headers=headers,json={"key":key,"machine":uuid})
                return {'STATUS':1,'MESSAGE':'Key Authorised'}
            else:
                return {'STATUS':0,'MESSAGE':'Machine could not be validated, please reset it on the dashboard'}
        else:
            return {'STATUS':0,'MESSAGE':'Key does not exist or is not bound'}