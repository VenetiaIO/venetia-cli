from flask import Flask, escape, request, Response
import csv
import json
import threading
import logging

app = Flask(__name__)
app.logger.disabled = True
log = logging.getLogger('werkzeug')
log.disabled = True

#sites
from sites.svd import SVD
from sites.queens import QUEENS
from sites.allike import ALLIKE
from sites.titolo import TITOLO
from sites.grosbasket import GROSBASKET
from sites.airness import AIRNESS
from sites.footasylum import FOOTASYLUM
from sites.holypop import HOLYPOP
from sites.schuh import SCHUH
from sites.starcow import STARCOW
from sites.slamjam import SLAMJAM
from sites.consortium import CONSORTIUM
from sites.courir import COURIR
from sites.bstn import BSTN
from sites.overkill import OVERKILL
from sites.awlab import AWLAB
from sites.einhalb import EINHALB

sites = {
    "SVD":SVD,
    "QUEENS":QUEENS,
    "TITOLO":TITOLO,
    "AIRNESS":AIRNESS,
    "FOOTASYLUM":FOOTASYLUM,
    "HOLYPOP":HOLYPOP,
    "ALLIKE":ALLIKE,
    "GROSBASKET":GROSBASKET,
    "SCHUH":SCHUH,
    "SLAMJAM":SLAMJAM,
    "AWLAB":AWLAB,
    "EINHALB":EINHALB
}

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
    
        taskName = 'QUICK-TASK'
        threading.Thread(target=sites.get(row["SITE"].upper()),args=(row,taskName)).start()
    
        return 'Executing Quicktask...'

    except Exception as e:
        log.info(e)
        return 'Failed to execute quicktask'




