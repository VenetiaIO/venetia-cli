import requests
import shutil
import os

class Updater:
    @staticmethod
    def checkForUpdate(currentVersion):
        response = requests.get('https://venetiacli.io/venetia-cli-latest')
        if response.status_code == 200:
            if currentVersion == response.json()["version"]:
                return {"latest":True, "error":False}
            else:
                return {"latest":False, "error":False, "version":response.json()["version"]}
        else:
            return {"latest":False, "error":True}

    @staticmethod
    def downloadLatest(VERSION):
        #print(os.path.realpath(__file__))
        os.rename('venetiCLI.exe', 'venetiaCLI_old.exe')
        response = requests.get('https://venetiacli.io/venetia-cli-latest/download',stream=True)
        with open(f'venetiaCLI.exe', 'wb') as f:
            shutil.copyfileobj(response.raw, f)

        return "complete"

