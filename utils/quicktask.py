from flask import Flask, escape, request, Response
import csv
import json
import threading
import logging
from utils.config import VERSION

try:
    import win32console 
except:
    pass

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
from sites.chmielna import CHMIELNA
from sites.workingClassHeroes import WCH
from sites.naked import NAKED
from sites.footdistrict import FOOTDISTRICT
from sites.prodirect import PRODIRECT
from sites.disney import DISNEY
from sites.cornerstreet import CORNERSTREET
from sites.snipes import SNIPES

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
    #"EINHALB":EINHALB,
    #"STARCOW":STARCOW,
    "CHMIELNA20":CHMIELNA,
    "WCH":WCH,
    "NAKED":NAKED,
    #"FOOTDISTRICT":FOOTDISTRICT,
    "PRODIRECT":PRODIRECT,
    "DISNEY":DISNEY,
    #"CORNERSTREET":CORNERSTREET,
    #"BSTN":BSTN,
    "SNIPES":SNIPES

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
    
        taskName = 'QT'
        threading.Thread(target=sites.get(row["SITE"].upper()),args=(row,taskName)).start()
        try:
            win32console.SetConsoleTitle("[Version {}] VenetiaIO CLI - {} | Carted: {} | Checked Out: {}".format(VERSION,row["SITE"].upper(),"0","0"))
        except:
            pass
    
        return 'Executing Quicktask...'

    except Exception as e:
        log.info(e)
        return 'Failed to execute quicktask'




