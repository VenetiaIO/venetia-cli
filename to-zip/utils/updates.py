import requests
import shutil
import os
import sys
from colorama import Fore, Back, Style, init
import time
import threading
init()

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
        for file in os.listdir(os.getcwd()):
            if 'venetia' in file.lower():
                name = file.split('.exe')[0]
                os.rename(file, f'{name}_old.exe')


        with open('venetiaCLI.exe', 'wb') as f:
            response = requests.get('https://venetiacli.io/venetia-cli-latest/download',stream=True)

            total_length = response.headers.get('content-length')
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                f.write(data)
                dl += len(data)
                done = int(50 * dl / total_length)
                sys.stdout.write( Fore.YELLOW+ Style.DIM +"\rUpdating: {} [{}] {}".format(
                    str(int((int(dl) / int(total_length)) * 100)) + '%',
                    '=' * done + '.' * (50 - done),
                    '{}/{}'.format(str(dl),str(total_length)) 
                ))
                sys.stdout.flush()

            sys.stdout.write('\n')
                
            

        return "complete"

