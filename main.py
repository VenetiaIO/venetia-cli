from colorama import init
from termcolor import colored
import json
import datetime
import csv
import threading
import sys
import time
import ctypes
import requests
from pypresence import Presence
import uuid
import os
import click
init(autoreset=True)

def secho(text, file=None, nl=None, err=None, color=None, **styles):
    pass

def echo(text, file=None, nl=None, err=None, color=None, **styles):
    pass

click.echo = echo
click.secho = secho


VERSION  = '0.3.6'
os.system("title VenetiaIO CLI [Version {}]".format(VERSION))

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

#utils
from utils.quicktask import QT
from utils.captcha import captcha
from utils.logger import logger
from utils.accounts import ACCOUNTS
from utils.auth import auth
from utils.datadome import datadome
from utils.ascii import logo

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
    "EINHALB":EINHALB,
    "STARCOW":STARCOW,
    "CHMIELNA20":CHMIELNA,
    "WCH":WCH,
    "NAKED":NAKED,
    "FOOTDISTRICT":FOOTDISTRICT
}



def get_time():
    x = datetime.datetime.now()
    x = f'{x.strftime("%X")}.{x.strftime("%f")}'
    return x

def taskCount():
    with open('./data/tasks.csv','r') as csvFile:
        csv_reader = csv.DictReader(csvFile)
        length = len(list(csv_reader))
        return length

def clearTokens():
    data = {}
    data['TITOLO'] = []
    data['BSTN'] = []
    data['HOLYPOP'] = []
    with open('./data/captcha/tokens.json','w') as tokenFile:
        json.dump(data,tokenFile)
    return 'complete'

def checkTasks(site):
    tasks = []
    with open('./data/tasks.csv','r') as csvFile:
        csv_reader = csv.DictReader(csvFile)
        for r in csv_reader:
            if site.lower() in r["SITE"].lower():
                tasks.append(1)

    if len(tasks) > 0:
        return True
    elif len(tasks) == 0:
        return False

class Menu:
    def __init__(self):
        threading.Thread(target=QT,daemon=True).start()
        
        try:
            client_id = 726839544124670093
            self.RPC = Presence(client_id)
            self.RPC.connect()
            self.rpctime = int(time.time())
        except:
            pass

        time.sleep(1)
        with open('./data/config.json') as config:
            self.config = json.loads(config.read())
            self.key = self.config["key"]
        self.menu()


    def siteSelectFunc(self, availableSites, siteSelection):
        key_chosen, value_chosen = sorted(availableSites.items())[int(siteSelection) -1 ]
        with open('./data/tasks.csv','r') as csvFile:
            csv_reader = csv.DictReader(csvFile)
            i = 1
            for row in csv_reader:
                if row["SITE"].lower() == key_chosen.lower():
                    if row["PRODUCT"] != "":
                        try:
                            self.RPC.update(large_image="image", state=f"Version {VERSION}", details='Destroying {}...'.format(key_chosen.title()), start=self.rpctime,small_image="image",small_text="@venetiaIO")
                        except:
                            pass
                        taskName = f'Task {i}'
                        i = i + 1
                        threading.Thread(target=value_chosen,args=(row,taskName)).start()
        



    def menu(self):
        headers = {"apiKey":"27acc458-f01a-48f8-88b8-06583fb39056"}
        requests.post('http://venetiacli.io/api/last/opened',headers=headers,json={"key":self.config["key"],"date":str(datetime.datetime.now())})
        try:
            self.RPC.update(large_image="image", state=f"Version {VERSION}", details='Main Menu', start=self.rpctime,small_image="image",small_text="@venetiaIO")
        except:
            pass

        #logger.error('VENETIA','Menu','                 Welcome To...                   ')
        #logger.alert('VENETIA','Menu',' _    __                __  _          ________    ____')
        #logger.alert('VENETIA','Menu','| |  / /__  ____  ___  / /_(_)___ _   / ____/ /   /  _/')
        #logger.alert('VENETIA','Menu','| | / / _ \/ __ \/ _ \/ __/ / __ `/  / /   / /    / /  ')
        #logger.alert('VENETIA','Menu','| |/ /  __/ / / /  __/ /_/ / /_/ /  / /___/ /____/ /   ')
        #logger.alert('VENETIA','Menu','|___/\___/_/ /_/\___/\__/_/\__,_/   \____/_____/___/  {}'.format(colored(VERSION,'magenta',attrs=["bold"])))
        print('                 Welcome To...                  ')
        logger.logo(logo,VERSION)
        logger.menu('VENETIA','Menu','{}'.format(colored(f'Key Authorised','green', attrs=["bold"])))
        logger.menu('VENETIA','Menu','[{}] => {}'.format(colored('1','red', attrs=["bold"]), colored('Start All Tasks','red', attrs=["bold"])))
        logger.menu('VENETIA','Menu','[{}] => {}'.format(colored('2','red', attrs=["bold"]), colored('Start Specific Tasks','red', attrs=["bold"])))
        logger.menu('VENETIA','Menu','[{}] => {}'.format(colored('3','red', attrs=["bold"]), colored('View Config','red', attrs=["bold"])))
        logger.menu('VENETIA','Menu','[{}] => {}'.format(colored('4','red', attrs=["bold"]), colored('Edit Config','red', attrs=["bold"])))
        logger.menu('VENETIA','Menu','[{}] => {}'.format(colored('5','red', attrs=["bold"]), colored('Create Profile','red', attrs=["bold"])))
        logger.menu('VENETIA','Menu','[{}] => {}'.format(colored('6','red', attrs=["bold"]), colored('Generate Captchas','red', attrs=["bold"])))
        logger.menu('VENETIA','Menu','[{}] => {}'.format(colored('7','red', attrs=["bold"]), colored('Account Gen','red', attrs=["bold"])))
        logger.menu('VENETIA','Menu','[{}] => {}'.format(colored('8','red', attrs=["bold"]), colored('Cookie Gen','red', attrs=["bold"])))
        logger.menu('VENETIA','Menu','[{}] => {}'.format(colored('9','red', attrs=["bold"]), colored('Exit','red', attrs=["bold"])))
        #sys.stdout.write('\n[{}][{}]'.format(colored(get_time(),'cyan',attrs=["bold"]), colored('Venetia-Menu','white')))
        sys.stdout.write('\n[{}][{}]'.format(colored(get_time(),'cyan',attrs=["bold"]), colored('Venetia-Menu','white')))
        try:
            option = int(input(' Pick an option => '))
        except ValueError:
            logger.error('VENETIA','Menu','Please enter a number')
            self.menu()
        
        if option == 1:

            with open('./data/tasks.csv','r') as csvFile:
                csv_reader = csv.DictReader(csvFile)
                i = 1
                for row in csv_reader:
                    if [row["SITE"].upper() in sites.keys()]:
                        if sites.get(row["SITE"].upper()) != None:
                            if row["PRODUCT"] != "":
                                try:
                                    self.RPC.update(large_image="image", state=f"Version {VERSION}", details=f'Running {taskCount()} Task(s)...'.format(row["SITE"].title()), start=self.rpctime,small_image="image",small_text="@venetiaIO")
                                except:
                                    pass
                                taskName = f'Task {i}'
                                i = i + 1
                                threading.Thread(target=sites.get(row["SITE"].upper()),args=(row,taskName)).start()
 
        if option == 2:
            number = 1
            availableSites = {}
            for row in sorted(sites):
                if(checkTasks(row)):
                    availableSites[row] = sites[row]

            for s in availableSites:
                logger.menu('VENETIA','Menu','[{}] => {}'.format(colored(number,'red', attrs=["bold"]), colored(s,'red', attrs=["bold"])))
                number = number + 1
            

            

            menuNum = number
            logger.menu('VENETIA','Menu','[{}] => {}'.format(colored(menuNum,'red', attrs=["bold"]), colored('RETURN TO MAIN Menu','red', attrs=["bold"])))
            sys.stdout.write('\n[{}][{}]'.format(colored(get_time(),'cyan',attrs=["bold"]), colored('Venetia-Menu','white')))
            siteSelection = input(' Select a site => ')
            if int(siteSelection) == menuNum:
                self.menu()
            os.system("title VenetiaIO CLI Version {}   Running Tasks...".format(VERSION))
            self.siteSelectFunc(availableSites, siteSelection)

        if option == 3:
            try:
                with open('./data/config.json') as config:
                    config = json.loads(config.read())
                    k = config["key"]
                    w = config["webhook"]
                    twoC = config["2Captcha"]
                    ac = config["AntiCaptcha"]
                    qtProfile = config["quickTaskProfile"]
                    qtProxies = config["quickTaskProxies"]
                    qtDelay = config["quickTaskDelay"]
                    qtEmail = config["quickTaskEmail"]
                    qtPassword = config["quickTaskPassword"]
                    qtPayment = config["quickTaskPayment"]
                    qtSize = config["quickTaskSize"]
                    logger.menu('VENETIA','Menu','[{}] => {}'.format(colored('KEY','red', attrs=["bold"]), colored(k,'cyan')))
                    logger.menu('VENETIA','Menu','[{}] => {}'.format(colored('WEBHOOK','red', attrs=["bold"]), colored(w,'cyan')))
                    logger.menu('VENETIA','Menu','[{}] => {}'.format(colored('2 CAPTCHA','red', attrs=["bold"]), colored(twoC,'cyan')))
                    logger.menu('VENETIA','Menu','[{}] => {}'.format(colored('ANTI CAPTCHA','red', attrs=["bold"]), colored(ac,'cyan')))
                    logger.menu('VENETIA','Menu','[{}] => {}'.format(colored('QT SIZE','red', attrs=["bold"]), colored(qtSize,'cyan')))
                    logger.menu('VENETIA','Menu','[{}] => {}'.format(colored('QT PROFILE','red', attrs=["bold"]), colored(qtProfile,'cyan')))
                    logger.menu('VENETIA','Menu','[{}] => {}'.format(colored('QT PROXIES','red', attrs=["bold"]), colored(qtProxies,'cyan')))
                    logger.menu('VENETIA','Menu','[{}] => {}'.format(colored('QT DELAY','red', attrs=["bold"]), colored(qtDelay,'cyan')))
                    logger.menu('VENETIA','Menu','[{}] => {}'.format(colored('QT PAYMENT','red', attrs=["bold"]), colored(qtPayment,'cyan')))
                    logger.menu('VENETIA','Menu','[{}] => {}'.format(colored('QT ACCOUNT EMAIL','red', attrs=["bold"]), colored(qtEmail,'cyan')))
                    logger.menu('VENETIA','Menu','[{}] => {}'.format(colored('QT ACCOUNT PASSWORD','red', attrs=["bold"]), colored(qtPassword,'cyan')))
                    sys.stdout.write('\n[{}][{}]'.format(colored(get_time(),'cyan',attrs=["bold"]), colored('Venetia-Menu','white')))
                    option = input(' [ENTER] TO RETURN TO Menu ')
                    self.menu()
            except Exception as e:
                logger.error('VENETIA','Menu','Error reading config [{}]. Please edit...'.format(e))
                sys.stdout.write('\n[{}][{}]'.format(colored(get_time(),'cyan',attrs=["bold"]), colored('Venetia-Menu','white')))
                option = input(' [ENTER] TO RETURN TO Menu ')
                self.menu()

        if option == 4:
            with open('./data/config.json') as config:
                config = json.loads(config.read())
                print(colored(f"[{get_time()}] Configure Config Below (Leave blank to leave unchanged) ", "red",attrs=['bold']))

                webhook = input(f"[{get_time()}] Enter Webhook ==> ")
                if webhook == "":
                    try:
                        webhook = config["webhook"]
                    except:
                        webhook = ""

                twoCaptcha =  input(f"[{get_time()}] Enter 2 Captcha API Key ==> ")
                if twoCaptcha == "":
                    try:
                        twoCaptcha = config["2Captcha"]
                    except:
                        twoCaptcha = ""

                antiCaptcha = input(f"[{get_time()}] Enter Anti Captcha API Key ==> ")
                if antiCaptcha == "":
                    try:
                        antiCaptcha = config["AntiCaptcha"]
                    except:
                        antiCaptcha = ""

                qtSize = input(f"[{get_time()}] Enter QT Size ==> ")
                if qtSize == "":
                    try:
                        qtSize = config["quickTaskSize"]
                    except:
                        qtSize = ""

                qtProfile = input(f"[{get_time()}] Enter QT Profile ==> ")
                if qtProfile == "":
                    try:
                        qtProfile = config["quickTaskProfile"]
                    except:
                        qtProfile = ""

                qtProxies = input(f"[{get_time()}] Enter QT Proxies ==> ")
                if qtProxies == "":
                    try:
                        qtProxies = config["quickTaskProxies"]
                    except:
                        qtProxies = ""

                qtDelay = input(f"[{get_time()}] Enter QT Delay ==> ")
                if qtDelay == "":
                    try:
                        qtDelay = config["quickTaskDelay"]
                    except:
                        qtDelay = "0"

                qtPayment = input(f"[{get_time()}] Enter QT Payment ==> ")
                if qtPayment == "":
                    try:
                        qtPayment = config["quickTaskPayment"]
                    except:
                        qtPayment = ""

                qtEmail = input(f"[{get_time()}] Enter QT Account Email ==> ")
                if qtEmail == "":
                    try:
                        qtEmail = config["quickTaskEmail"]
                    except:
                        qtEmail = ""

                qtPassword = input(f"[{get_time()}] Enter QT Account Password ==> ")
                if qtPassword == "":
                    try:
                        qtPassword = config["quickTaskPassword"]
                    except:
                        qtPassword = ""


                config_updated = {"key":config["key"],"webhook":webhook,"2Captcha":twoCaptcha,"AntiCaptcha":antiCaptcha,"quickTaskSize":qtSize,"quickTaskProfile":qtProfile,"quickTaskProxies":qtProxies,"quickTaskDelay":qtDelay,"quickTaskPayment":qtPayment,"quickTaskEmail":qtEmail,"quickTaskPassword":qtPassword}

                with open("./data/config.json","w") as updated:
                    json.dump(config_updated, updated)

                sys.stdout.write('\n[{}][{}]'.format(colored(get_time(),'cyan',attrs=["bold"]), colored('Venetia-Menu','white')))
                option = input(' [ENTER] TO RETURN TO Menu ')
                self.menu()

        if option == 5:
            try:
                self.RPC.update(large_image="image", state=f"Version {VERSION}", details='Creating Profiles...', start=self.rpctime,small_image="image",small_text="@venetiaIO")
            except:
                pass
            profile = {}

            profileName = input(f"[{get_time()}] Profile Name ==> ")
            

            profile["firstName"] = input(f"[{get_time()}] First Name ==> ")

            profile["lastName"] = input(f"[{get_time()}] Last Name ==> ")

            profile["email"] = input(f"[{get_time()}] Email ==> ")

            profile["phonePrefix"] = input(f"[{get_time()}] Phone Prefix (example: +44) ==> ")

            profile["phone"] = input(f"[{get_time()}] Phone ==> ")

            profile["house"] = input(f"[{get_time()}] House (Number / Name ) ==> ")

            profile["addressOne"] = input(f"[{get_time()}] Address 1 ==> ")

            profile["addressTwo"] = input(f"[{get_time()}] Address 2 ==> ")

            profile["city"] = input(f"[{get_time()}] City ==> ")

            profile["region"] = input(f"[{get_time()}] Region/Province/State ==> ")

            profile["country"] = input(f"[{get_time()}] Country ==> ")

            profile["countryCode"] = input(f"[{get_time()}] Country Code (example: GB) ==> ")

            profile["zip"] = input(f"[{get_time()}] Zipcode/Postcode ==> ")

            profile['card'] = {}

            profile['card']["cardNumber"] = input(f"[{get_time()}] Card Number ==> ")

            profile['card']["cardMonth"] = input(f"[{get_time()}] Card Expiry Month (example: 8) ==> ")

            profile['card']["cardYear"] = input(f"[{get_time()}] Card Expiry Year (example: 2024) ==> ")

            profile['card']["cardCVV"] = input(f"[{get_time()}] Card CVV/CVC ==> ")

            with open(f'./data/profiles/profile_{profileName}.json','w') as profileDump:
                json.dump(profile, profileDump)

            logger.menu('VENETIA','Menu','PROFILE CREATED - {}'.format(colored(profileName,'green',attrs=["bold"])))

            sys.stdout.write('\n[{}][{}]'.format(colored(get_time(),'cyan',attrs=["bold"]), colored('Venetia-Menu','white')))
            option = input(' [ENTER] TO RETURN TO Menu ')
            self.menu()

        if option == 6:
            print('[{}] Would you like to clear current captcha tokens ?   Y | N'.format(colored(get_time(),'red',attrs=['bold'])))
            sys.stdout.write('\n[{}][{}]'.format(colored(get_time(),'cyan',attrs=["bold"]), colored('Venetia-Menu','white')))
            cleartokenQuestion = input(' Pick an option => ')
            if cleartokenQuestion.lower() == 'y':
                clearTokens()
            else:
                pass


            logger.menu('VENETIA','CAPTCHAS','[{}] => {}'.format(colored('1','red', attrs=["bold"]), colored('TITOLO','cyan')))
            logger.menu('VENETIA','CAPTCHAS','[{}] => {}'.format(colored('2','red', attrs=["bold"]), colored('HOLYPOP','cyan')))
            #logger.menu('VENETIA','CAPTCHAS','[{}] => {}'.format(colored('3','red', attrs=["bold"]), colored('BSTN','cyan')))
            logger.menu('VENETIA','CAPTCHAS','[{}] => {}'.format(colored('4','red', attrs=["bold"]), colored('RETURN TO Menu','cyan')))
            sys.stdout.write('\n[{}][{}]'.format(colored(get_time(),'cyan',attrs=["bold"]), colored('Venetia-Menu','white')))
            CaptchasiteSelect = input(' Select a site => ')
            if CaptchasiteSelect == "1":
                siteUrl = 'https://en.titoloshop.com/'
                siteKey = '6Ldpi-gUAAAAANpo2mKVvIR6u8nUGrInKKik8MME'
                siteName = 'TITOLO'
            if CaptchasiteSelect == "2":
                siteUrl = 'https://www.holypopstore.com/'
                siteKey = '6Lc8GBUUAAAAAKMfe1S46jE08TvVKNSnMYnuj6HN'
                siteName = 'HOLYPOP'
            if CaptchasiteSelect == "3":
                siteUrl = 'https://www.bstn.com/'
                siteKey = '6Le9G8cUAAAAANrlPVYknZGUZw8lopZAqe8_SfRQ'
                siteName = 'BSTN'
            if CaptchasiteSelect == "4":
                self.menu()

            sys.stdout.write('\n[{}][{}]'.format(colored(get_time(),'cyan',attrs=["bold"]), colored('Venetia-Menu','white')))
            amount = option = input(' Enter Amount => ')

            sys.stdout.write('\n[{}][{}]'.format(colored(get_time(),'cyan',attrs=["bold"]), colored('Venetia-Menu','white')))
            proxies = input(' Enter proxy list name (leave empty for none) => ')
            if proxies == "":
                proxies = None
            
            for i in range(int(amount)):
                threading.Thread(target=captcha.menuV2,args=(siteKey,siteUrl,proxies,'CAPTCHA',siteName)).start()

            while threading.active_count() != 2:
                pass

            if threading.active_count() == 2:
                self.menu()

        if option == 7:
            logger.menu('VENETIA','ACCOUNTS','[{}] => {}'.format(colored('1','red', attrs=["bold"]), colored('HOLYPOP','cyan')))
            logger.menu('VENETIA','ACCOUNTS','[{}] => {}'.format(colored('2','red', attrs=["bold"]), colored('RETURN TO Menu','cyan')))
            sys.stdout.write('\n[{}][{}]'.format(colored(get_time(),'cyan',attrs=["bold"]), colored('Venetia-Menu','white')))
            AccountsiteSelect = input(' Select a site => ')
            if AccountsiteSelect == "2":
                self.menu()

            proxies = input(f"[{get_time()}] Enter proxy list name (leave empty for none) ==> ")
            if proxies == "":
                proxies = None

            amount = input(f"[{get_time()}] Enter amount ==> ")

            catchall = input(f"[{get_time()}] Enter catchall (with @) ==> ")

            password = input(f"[{get_time()}] Enter Password ==> ")
            
            profile = input(f"[{get_time()}] Enter profile name (for address) ==> ")

            if AccountsiteSelect == "1":
                sitekey = '6Lc8GBUUAAAAAKMfe1S46jE08TvVKNSnMYnuj6HN'
                for i in range(int(amount)):
                    threading.Thread(target=ACCOUNTS.holypop,args=(sitekey,proxies,'HOLYPOP',catchall,password, profile)).start()

        
            while threading.active_count() != 2:
                pass

            if threading.active_count() == 2:
                self.menu()
        
        if option == 8:
            # self.menu()
            
            #logger.menu('VENETIA','COOKIES','[{}] => {}'.format(colored('1','red', attrs=["bold"]), colored('COURIR','cyan')))
            #logger.menu('VENETIA','COOKIES','[{}] => {}'.format(colored('2','red', attrs=["bold"]), colored('STARCOW','cyan')))
            logger.menu('VENETIA','COOKIES','[{}] => {}'.format(colored('1','red', attrs=["bold"]), colored('SLAM JAM','cyan')))
            logger.menu('VENETIA','COOKIES','[{}] => {}'.format(colored('2','red', attrs=["bold"]), colored('RETURN TO Menu','cyan')))
            sys.stdout.write(colored(f'\n[{get_time()}][Venetia-Menu]','cyan',attrs=["bold"]))
            cookieSiteSelect = input(' Select a site => ')
            if cookieSiteSelect == "2":
                self.menu()

            sys.stdout.write('\n[{}][{}]'.format(colored(get_time(),'cyan',attrs=["bold"]), colored('Venetia-Menu','white')))
            proxies = input(' Enter proxy list name (leave empty for none) => ')
            if proxies == "":
                proxies = None

            sys.stdout.write('\n[{}][{}]'.format(colored(get_time(),'cyan',attrs=["bold"]), colored('Venetia-Menu','white')))
            amount = input(' Enter amount => ')
            sys.stdout.write('\n[{}][{}]'.format(colored(get_time(),'cyan',attrs=["bold"]), colored('Venetia-Menu','white')))
            region = input(' Enter Site Region (example: GB) => ')

            if cookieSiteSelect == "1":
                for i in range(int(amount)):
                    threading.Thread(target=datadome.slamjam,args=(proxies,region,)).start()
            #if cookieSiteSelect == "2":
            #    for i in range(int(amount)):
            #        threading.Thread(target=datadome.starcow,args=(proxies,)).start()
            #if cookieSiteSelect == "3":
            #    for i in range(int(amount)):
            #        threading.Thread(target=datadome.slamjam,args=(proxies,region,)).start()

            while threading.active_count() != 2:
                pass

            if threading.active_count() == 2:
                self.menu()

        if option == 9:
            logger.menu('VENETIA','Menu','{}'.format(colored('Goodbye...','yellow', attrs=["bold"])))
            time.sleep(3)
            os._exit(0)
            
                


if __name__ == "__main__":
    with open('./data/config.json') as config:
        config = json.loads(config.read())
        if config["key"] == "":
            sys.stdout.write('\n[{}][{}]'.format(colored(get_time(),'cyan',attrs=["bold"]), colored('Venetia-Menu','white')))
            key = input(colored(" Enter Your License Key ==> ","yellow",attrs=["bold"]))
            config["key"] = key
            with open("./data/config.json","w") as updated:
                json.dump(config, updated)

            auth = auth.auth(config["key"], uuid.getnode())
            if auth["STATUS"] == 1:
                Menu()
            if auth["STATUS"] == 0:
                logger.menu('VENETIA','Menu','{}'.format(colored('Failed to auth key. Closing...','red', attrs=["bold"])))
                time.sleep(3)
                os._exit(0)

        else:
            auth = auth.auth(config["key"], uuid.getnode())
            if auth["STATUS"] == 1:
                Menu()
            if auth["STATUS"] == 0:
                logger.menu('VENETIA','Menu','{}'.format(colored('Failed to auth key. Closing...','red', attrs=["bold"])))
                time.sleep(3)
                os._exit(0)
