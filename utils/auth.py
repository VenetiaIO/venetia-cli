import requests

headers = {"apiKey":"27acc458-f01a-48f8-88b8-06583fb39056"}

class auth:
    @staticmethod
    def auth(key, uuid):
        return {'STATUS':1,'MESSAGE':'Key Authorised'}
        # validateMachine = requests.post('https://venetiacli.io/api/v1/users/machine/validate',headers=headers,json={"key":key,"machine":uuid})
        # if validateMachine.status_code == 200:
        #     return {'STATUS':1,'MESSAGE':'Key Authorised'}
        # if validateMachine.status_code == 201:
        #     r = requests.post('https://venetiacli.io/api/v1/users/machine/update',headers=headers,json={"key":key,"machine":uuid})
        #     return {'STATUS':1,'MESSAGE':'Key Authorised'}
        # if validateMachine.status_code == 404:
        #     return {'STATUS':0,'MESSAGE':'Key doesnt exist.'}
        # else:
        #     return {'STATUS':0,'MESSAGE':'Machine could not be validated, please reset it on the dashboard'}
