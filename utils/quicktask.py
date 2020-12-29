from flask import Flask, escape, request, Response
import csv
import json
import threading
import logging
from utils.config import *

try:
    import win32console 
except:
    pass

app = Flask(__name__)
app.logger.disabled = True
log = logging.getLogger('werkzeug')
log.disabled = True




class EndpointAction(object):

    def __init__(self, action):
        self.action = action
        self.response = Response(status=200, headers={})

    def __call__(self, *args):
        self.action()
        return self.response


class QT(object):
    app = None

    def __init__(self):
        self.app = app
        self.add_endpoint('/venetia/quicktask','venetia/quicktask',action)
        self.run()

    def run(self):
        self.app.run(port=6969,threaded=True)

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None):
        endpoint = self.app.add_url_rule(endpoint, endpoint_name, EndpointAction(handler))


def action():
    try:
        site = request.args.get("website")
        url = request.args.get("url")

        
        with open(f'./data/config.json') as settings:
            settings = json.loads(settings.read())
    
    
        row = {
            "SITE":site,
            "PRODUCT":url,
            "SIZE":settings["quickTaskSize"],
            "DELAY":settings["quickTaskDelay"],
            "PROFILE":settings["quickTaskProfile"],
            "PAYMENT":settings["quickTaskPayment"],
            "PROXIES":settings["quickTaskProxies"],
            "ACCOUNT EMAIL":settings["quickTaskEmail"],
            "ACCOUNT PASSWORD":settings["quickTaskPassword"]
        }
    
        taskName = 'QT'
        threading.Thread(target=sites.get(row["SITE"].upper()),args=(row,taskName)).start()
        try:
            win32console.SetConsoleTitle("[Version {}] VenetiaIO CLI - {} | Carted: {} | Checked Out: {}".format(VERSION(),row["SITE"].upper(),"0","0"))
        except:
            pass
    
        return 'Executing Quicktask...'

    except Exception as e:
        log.info(e)
        return 'Failed to execute quicktask'




