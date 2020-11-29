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
try:
    import win32console 
except:
    pass
from utils.config import VERSION
init(autoreset=True)

def secho(text, file=None, nl=None, err=None, color=None, **styles):
    pass

def echo(text, file=None, nl=None, err=None, color=None, **styles):
    pass

click.echo = echo
click.secho = secho


# os.system("title VenetiaIO CLI [Version {}]".format(VERSION))
try:
    win32console.SetConsoleTitle("[Version {}] VenetiaIO CLI".format(VERSION))
except:
    pass

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
from sites.solebox import SOLEBOX
from sites.fenom import FENOM

#utils
from utils.quicktask import QT
from utils.captcha import captcha
from utils.logger import logger
from utils.accounts import ACCOUNTS
from utils.auth import auth
from utils.datadome import datadome
from utils.ascii import logo
from utils.updates import Updater

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
    "SNIPES":SNIPES,
    #"COURIR":COURIR,
    #"SOLEBOX":SOLEBOX,
    #"FENOM":FENOM

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
    #data['BSTN'] = []
    data['HOLYPOP'] = []
    data['NAKED'] = []
    data['PRODIRECT'] = []
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

def checkUpdate():
    status = Updater.checkForUpdate(VERSION)
    if status["error"] == False:
        if status["latest"] == True:
            logger.menu('VENETIA','Menu','{}'.format(colored(f'You are on the latest version! {VERSION}','green', attrs=["bold"])))
            return True
        if status["latest"] == False:
            logger.menu('VENETIA','Menu','{}'.format(colored(f'Updating...','magenta', attrs=["bold"])))
            download = Updater.downloadLatest(status["version"])
            if download == "complete":
                logger.menu('VENETIA','Menu','{}'.format(colored(f'Update complete. Please delete the old file named "venetiaCLI_old.exe" and open the new one name "venetiaCLI.exe"','cyan', attrs=["bold"])))
            else:
                logger.menu('VENETIA','Menu','{}'.format(colored('Failed to download latest version. Please try again later.','red', attrs=["bold"])))
    if status["error"] == True:
        logger.menu('VENETIA','Menu','{}'.format(colored('Failed to check version. Retrying...','red', attrs=["bold"])))
        time.sleep(10)
        checkUpdate()

class Menu:
    def __init__(self):
        checkUpdate()
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
                            try:
                                win32console.SetConsoleTitle("[Version {}] VenetiaIO CLI - {} | Carted: {} | Checked Out: {}".format(VERSION,key_chosen.title(),"0","0"))
                            except:
                                pass
                            self.RPC.update(large_image="image", state=f"Version {VERSION}", details='Destroying {}...'.format(key_chosen.title()), start=self.rpctime,small_image="image",small_text="@venetiaIO")
                        except:
                            pass
                        
                        if len(str(i)) == 1:
                            taskName = f'Task 000{i}'
                        if len(str(i)) == 2:
                            taskName = f'Task 00{i}'
                        if len(str(i)) == 3:
                            taskName = f'Task 0{i}'
                        if len(str(i)) == 4:
                            taskName = f'Task {i}'
                        i = i + 1
                        threading.Thread(target=value_chosen,args=(row,taskName)).start()
        



    def menu(self):
        headers = {"apiKey":"27acc458-f01a-48f8-88b8-06583fb39056"}
        requests.post('https://venetiacli.io/api/last/opened',headers=headers,json={"key":self.config["key"],"date":str(datetime.datetime.now())})
        try:
            self.RPC.update(large_image="image", state=f"Version {VERSION}", details='Main Menu', start=self.rpctime,small_image="image",small_text="@venetiaIO")
        except:
            pass

     
        print('                 Welcome To...                  ')
        logger.logo(logo,VERSION)
        logger.menu('VENETIA','Menu','[ {} ] => {}'.format(colored('01','red', attrs=["bold"]), colored('Start All Tasks','red', attrs=["bold"])))
        logger.menu('VENETIA','Menu','[ {} ] => {}'.format(colored('02','red', attrs=["bold"]), colored('Start Specific Tasks','red', attrs=["bold"])))
        logger.menu('VENETIA','Menu','[ {} ] => {}'.format(colored('03','red', attrs=["bold"]), colored('View Config','red', attrs=["bold"])))
        logger.menu('VENETIA','Menu','[ {} ] => {}'.format(colored('04','red', attrs=["bold"]), colored('Edit Config','red', attrs=["bold"])))
        logger.menu('VENETIA','Menu','[ {} ] => {}'.format(colored('05','red', attrs=["bold"]), colored('Create Profile','red', attrs=["bold"])))
        logger.menu('VENETIA','Menu','[ {} ] => {}'.format(colored('06','red', attrs=["bold"]), colored('View|Edit Profiles','red', attrs=["bold"])))
        logger.menu('VENETIA','Menu','[ {} ] => {}'.format(colored('07','red', attrs=["bold"]), colored('Generate Captchas','red', attrs=["bold"])))
        logger.menu('VENETIA','Menu','[ {} ] => {}'.format(colored('08','red', attrs=["bold"]), colored('Account Gen','red', attrs=["bold"])))
        logger.menu('VENETIA','Menu','[ {} ] => {}'.format(colored('09','red', attrs=["bold"]), colored('Cookie Gen','red', attrs=["bold"])))
        logger.menu('VENETIA','Menu','[ {} ] => {}'.format(colored('10','red', attrs=["bold"]), colored('Exit','red', attrs=["bold"])))
        #sys.stdout.write('\n[{}][{}]'.format(colored(get_time(),'cyan',attrs=["bold"]), colored('Venetia-Menu','white')))
        sys.stdout.write('\n[{}][{}]'.format(colored(get_time(),'cyan',attrs=["bold"]), colored('Venetia-Menu','white')))
        option = ''
        try:
            option = int(input(' Pick an option => '))
        except ValueError:
            logger.error('VENETIA','Menu','Please enter a number')
            self.menu()
        
        if option == 1:
            try:
                win32console.SetConsoleTitle("] Version {}] VenetiaIO CLI - {} | Carted: {} | Checked Out: {}".format(VERSION,"Running Tasks","0","0"))
            except:
                pass

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
                            
                                if len(str(i)) == 1:
                                    taskName = f'Task 000{i}'
                                if len(str(i)) == 2:
                                    taskName = f'Task 00{i}'
                                if len(str(i)) == 3:
                                    taskName = f'Task 0{i}'
                                if len(str(i)) == 4:
                                    taskName = f'Task {i}'
                                i = i + 1
                                threading.Thread(target=sites.get(row["SITE"].upper()),args=(row,taskName)).start()
 
        elif option == 2:
            number = 1
            availableSites = {}
            for row in sorted(sites):
                if(checkTasks(row)):
                    availableSites[row] = sites[row]

            for s in availableSites:
                logger.menu('VENETIA','Menu','[ {} ] => {}'.format(colored(number,'red', attrs=["bold"]), colored(s.title(),'red', attrs=["bold"])))
                number = number + 1
            

            

            menuNum = number
            logger.menu('VENETIA','Menu','[ {} ] => {}'.format(colored(menuNum,'red', attrs=["bold"]), colored('RETURN TO MAIN Menu','red', attrs=["bold"])))
            sys.stdout.write('\n[{}][{}]'.format(colored(get_time(),'cyan',attrs=["bold"]), colored('Venetia-Menu','white')))
            siteSelection = input(' Select a site => ')
            if int(siteSelection) == menuNum:
                self.menu()
            self.siteSelectFunc(availableSites, siteSelection)

        elif option == 3:
            try:
                with open('./data/config.json') as config:
                    config = json.loads(config.read())
                    k = config["key"]
                    checkoutN = config["checkoutNoise"]
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
                    logger.menu('VENETIA','Menu','[{}] => {}'.format(colored('CHECKOUT NOISE','red', attrs=["bold"]), colored(checkoutN,'cyan')))
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

        elif option == 4:
            with open('./data/config.json') as config:
                config = json.loads(config.read())
                print(colored(f"[{get_time()}] Configure Config Below (Leave blank to leave unchanged) ", "red",attrs=['bold']))

                checkoutNoise = input(f"[{get_time()}] Checkout Noise (Y / N) ==> ")
                if checkoutNoise == "":
                    try:
                        checkoutNoise = config["checkoutNoise"]
                    except:
                        checkoutNoise = "Y"

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


                config_updated = {"key":config["key"],"checkoutNoise":checkoutNoise.upper(),"webhook":webhook,"2Captcha":twoCaptcha,"AntiCaptcha":antiCaptcha,"quickTaskSize":qtSize,"quickTaskProfile":qtProfile,"quickTaskProxies":qtProxies,"quickTaskDelay":qtDelay,"quickTaskPayment":qtPayment,"quickTaskEmail":qtEmail,"quickTaskPassword":qtPassword}

                with open("./data/config.json","w") as updated:
                    json.dump(config_updated, updated)

                sys.stdout.write('\n[{}][{}]'.format(colored(get_time(),'cyan',attrs=["bold"]), colored('Venetia-Menu','white')))
                option = input(' [ENTER] TO RETURN TO Menu ')
                self.menu()

        elif option == 5:
            try:
                self.RPC.update(large_image="image", state=f"Version {VERSION}", details='Creating Profiles...', start=self.rpctime,small_image="image",small_text="@venetiaIO")
            except:
                pass

            with open(f'./data/profiles/profiles.json','r') as profileRead:
                profiles = json.loads(profileRead.read())
            

            profileName = input(f"[{get_time()}] Profile Name ==> ")

            
            profiles["profiles"].append({
                "profileName":profileName,
                "firstName":input(f"[{get_time()}] First Name ==> "),
                "lastName":input(f"[{get_time()}] Last Name ==> "),
                "email":input(f"[{get_time()}] Email ==> "),
                "phonePrefix":input(f"[{get_time()}] Phone Prefix (example: +44) ==> "),
                "phone": input(f"[{get_time()}] Phone ==> "),
                "house":input(f"[{get_time()}] House (Number / Name ) ==> "),
                "addressOne":input(f"[{get_time()}] Address 1 ==> "),
                "addressTwo":input(f"[{get_time()}] Address 2 ==> "),
                "city":input(f"[{get_time()}] City ==> "),
                "region":input(f"[{get_time()}] Region/Province/State ==> "),
                "country":input(f"[{get_time()}] Country (example: United Kingdom) ==> "),
                "countryCode":input(f"[{get_time()}] Country Code (example: GB) ==> "),
                "zip":input(f"[{get_time()}] Zipcode/Postcode ==> "),
                "card":{
                    "cardNumber":input(f"[{get_time()}] Card Number ==> "),
                    "cardMonth": input(f"[{get_time()}] Card Expiry Month (example: 8) ==> "),
                    "cardYear":input(f"[{get_time()}] Card Expiry Year (example: 2024) ==> "),
                    "cardCVV":input(f"[{get_time()}] Card CVV/CVC ==> ")
                }
            })


            with open(f'./data/profiles/profiles.json','w') as profileDump:
                json.dump(profiles, profileDump)

            logger.menu('VENETIA','Menu','PROFILE CREATED - {}'.format(colored(profileName,'green',attrs=["bold"])))

            sys.stdout.write('\n[{}][{}]'.format(colored(get_time(),'cyan',attrs=["bold"]), colored('Venetia-Menu','white')))
            option = input(' [ENTER] TO RETURN TO Menu ')
            self.menu()

        elif option == 6:
            with open(f'./data/profiles/profiles.json','r') as profileRead:
                profiles = json.loads(profileRead.read())

            num_profiles = len(profiles['profiles'])
            index = 0
            for p in profiles['profiles']:
                index += 1
                logger.menu('VENETIA','Profiles','[{}] => {}'.format(colored(index,'red', attrs=["bold"]), colored(p['profileName'],'cyan')))

            logger.menu('VENETIA','Profiles','[{}] => {}'.format(colored(index + 1,'red', attrs=["bold"]), colored('RETURN TO MAIN Menu','cyan')))

            sys.stdout.write('\n[{}][{}]'.format(colored(get_time(),'cyan',attrs=["bold"]), colored('Venetia-Menu','white')))
            try:
                option_profile = int(input(' Pick a profile => '))
            except ValueError:
                logger.error('VENETIA','Menu','Please enter a number')
                self.menu()
            
            if option_profile == num_profiles + 1:
                self.menu()
            else:
                selected_p = profiles['profiles'][option_profile -1]
                logger.menu('VENETIA','Menu','[{}] => {}'.format(colored('PROFILE NAME','red', attrs=["bold"]), colored(selected_p['profileName'],'cyan')))
                logger.menu('VENETIA','Menu','[{}] => {}'.format(colored('FIRST NAME','red', attrs=["bold"]), colored(selected_p['firstName'],'cyan')))
                logger.menu('VENETIA','Menu','[{}] => {}'.format(colored('LAST NAME','red', attrs=["bold"]), colored(selected_p['lastName'],'cyan')))
                logger.menu('VENETIA','Menu','[{}] => {}'.format(colored('EMAIL','red', attrs=["bold"]), colored(selected_p['email'],'cyan')))
                logger.menu('VENETIA','Menu','[{}] => {}'.format(colored('PHONE PREFIX','red', attrs=["bold"]), colored(selected_p['phonePrefix'],'cyan')))
                logger.menu('VENETIA','Menu','[{}] => {}'.format(colored('PHONE','red', attrs=["bold"]), colored(selected_p['phone'],'cyan')))
                logger.menu('VENETIA','Menu','[{}] => {}'.format(colored('HOUSE NUMBER/NAME','red', attrs=["bold"]), colored(selected_p['house'],'cyan')))
                logger.menu('VENETIA','Menu','[{}] => {}'.format(colored('ADDRESS 1','red', attrs=["bold"]), colored(selected_p['addressOne'],'cyan')))
                logger.menu('VENETIA','Menu','[{}] => {}'.format(colored('ADDRESS 2','red', attrs=["bold"]), colored(selected_p['addressTwo'],'cyan')))
                logger.menu('VENETIA','Menu','[{}] => {}'.format(colored('CITY','red', attrs=["bold"]), colored(selected_p['city'],'cyan')))
                logger.menu('VENETIA','Menu','[{}] => {}'.format(colored('REGION','red', attrs=["bold"]), colored(selected_p['region'],'cyan')))
                logger.menu('VENETIA','Menu','[{}] => {}'.format(colored('COUNTRY','red', attrs=["bold"]), colored(selected_p['country'],'cyan')))
                logger.menu('VENETIA','Menu','[{}] => {}'.format(colored('COUNTRY CODE','red', attrs=["bold"]), colored(selected_p['countryCode'],'cyan')))
                logger.menu('VENETIA','Menu','[{}] => {}'.format(colored('ZIP/POSTCODE','red', attrs=["bold"]), colored(selected_p['zip'],'cyan')))
                logger.menu('VENETIA','Menu','[{}] => {}'.format(colored('CARD NUMBER','red', attrs=["bold"]), colored(selected_p['card']['cardNumber'],'cyan')))
                logger.menu('VENETIA','Menu','[{}] => {}'.format(colored('CARD MONTH','red', attrs=["bold"]), colored(selected_p['card']['cardMonth'],'cyan')))
                logger.menu('VENETIA','Menu','[{}] => {}'.format(colored('CARD YEAR','red', attrs=["bold"]), colored(selected_p['card']['cardYear'],'cyan')))
                logger.menu('VENETIA','Menu','[{}] => {}'.format(colored('CARD CVV','red', attrs=["bold"]), colored(selected_p['card']['cardCVV'],'cyan')))

                sys.stdout.write('\n[{}][{}]'.format(colored(get_time(),'cyan',attrs=["bold"]), colored('Venetia-Menu','white')))
                option_edit_prof = input(' Edit Profile? Y/N => ')

                if option_edit_prof.lower() == "y":
                    with open(f'./data/profiles/profiles.json','r') as profileRead:
                        profiles = json.loads(profileRead.read())
            

                    print(colored(f"[{get_time()}] Configure Config Below (Leave blank to leave unchanged) ", "red",attrs=['bold']))
                    for p in profiles['profiles']:
                        if p['profileName'] == selected_p['profileName']:
                            profileName =  input(f"[{get_time()}] Profile Name ==> ")
                            if profileName == "":
                                try:
                                    profileName = p['profileName']
                                except:
                                    profileName = ""
                            else:
                                p['profileName'] = profileName

                            firtn =  input(f"[{get_time()}] First Name ==> ")
                            if firtn == "":
                                try:
                                    firtn = p['firstName']
                                except:
                                    firtn = ""
                            else:
                                p['firstName'] = firtn

                            lastn =  input(f"[{get_time()}] Last Name ==> ")
                            if lastn == "":
                                try:
                                    lastn = p['lastName']
                                except:
                                    lastn = ""
                            else:
                                p['lastName'] = lastn

                            email =  input(f"[{get_time()}] Email ==> ")
                            if email == "":
                                try:
                                    email = p['email']
                                except:
                                    email = ""
                            else:
                                p['email'] = email

                            prefix =  input(f"[{get_time()}] Phone Prefix (example: +44) ==> ")
                            if prefix == "":
                                try:
                                    prefix = p['phonePrefix']
                                except:
                                    prefix = ""
                            else:
                                p['phonePrefix'] = prefix

                            phone =  input(f"[{get_time()}] Phone ==> ")
                            if phone == "":
                                try:
                                    phone = p['phone']
                                except:
                                    phone = ""
                            else:
                                p['phone'] = phone

                            house =  input(f"[{get_time()}] House (Number / Name ) ==> ")
                            if house == "":
                                try:
                                    house = p['house']
                                except:
                                    house = ""
                            else:
                                p['house'] = house

                            add1 =  input(f"[{get_time()}] Address 1 ==> ")
                            if add1 == "":
                                try:
                                    add1 = p['addressOne']
                                except:
                                    add1 = ""
                            else:
                                p['addressOne'] = add1

                            add2 =  input(f"[{get_time()}] Address 2 ==> ")
                            if add2 == "":
                                try:
                                    add2 = p['addressTwo']
                                except:
                                    add2 = ""
                            else:
                                p['addressTwo'] = add2
                                    
                            city =  input(f"[{get_time()}] City ==> ")
                            if city == "":
                                try:
                                    city = p['city']
                                except:
                                    city = ""
                            else:
                                p['city'] = city

                            region =  input(f"[{get_time()}] Region/Province/State ==> ")
                            if region == "":
                                try:
                                    region = p['region']
                                except:
                                    region = ""
                            else:
                                p['region'] = region

                            country =  input(f"[{get_time()}] Country (example: United Kingdom) ==> ")
                            if country == "":
                                try:
                                    country = p['country']
                                except:
                                    country = ""
                            else:
                                p['country'] = country
                            
                            countryC =  input(f"[{get_time()}] Country Code (example: GB) ==> ")
                            if countryC == "":
                                try:
                                    countryC = p['countryCode']
                                except:
                                    countryC = ""
                            else:
                                p['countryCode'] = countryC

                            zip =  input(f"[{get_time()}] Zipcode/Postcode ==> ")
                            if zip == "":
                                try:
                                    zip = p['zip']
                                except:
                                    zip = ""
                            else:
                                p['zip'] = zip

                            cn =  input(f"[{get_time()}] Card Number ==> ")
                            if cn == "":
                                try:
                                    cn = p['card']['cardNumber']
                                except:
                                    cn = ""
                            else:
                                p['card']['cardNumber'] = cn

                            expm =  input(f"[{get_time()}] Card Expiry Month (example: 8) ==> ")
                            if expm == "":
                                try:
                                    expm = p['card']['cardMonth']
                                except:
                                    expm = ""
                            else:
                                p['card']['cardMonth'] = expm

                            expy =  input(f"[{get_time()}] Card Expiry Year (example: 2024) ==> ")
                            if expy == "":
                                try:
                                    expy = p['card']['cardYear']
                                except:
                                    expy = ""
                            else:
                                p['card']['cardYear'] = expy

                            cvv =  input(f"[{get_time()}] Card CVV/CVC ==> ")
                            if cvv == "":
                                try:
                                    cvv = p['card']['cardCVV']
                                except:
                                    cvv = ""
                            else:
                                p['card']['cardCVV'] = cvv
                            
                            

        
                    with open(f'./data/profiles/profiles.json','w') as profileDump2:
                        json.dump(profiles, profileDump2)
        
                    logger.menu('VENETIA','Menu','PROFILE Updated - {}'.format(colored(profileName,'green',attrs=["bold"])))
        
                    sys.stdout.write('\n[{}][{}]'.format(colored(get_time(),'cyan',attrs=["bold"]), colored('Venetia-Menu','white')))
                    option = input(' [ENTER] TO RETURN TO Menu ')
                    self.menu()
                else:
                    self.menu()

            

        elif option == 7:
            print('[{}] Would you like to clear current captcha tokens ?   Y | N'.format(colored(get_time(),'red',attrs=['bold'])))
            sys.stdout.write('\n[{}][{}]'.format(colored(get_time(),'cyan',attrs=["bold"]), colored('Venetia-Menu','white')))
            cleartokenQuestion = input(' Pick an option => ')
            if cleartokenQuestion.lower() == 'y':
                clearTokens()
            else:
                pass


            logger.menu('VENETIA','CAPTCHAS','[{}] => {}'.format(colored('1','red', attrs=["bold"]), colored('TITOLO','cyan')))
            logger.menu('VENETIA','CAPTCHAS','[{}] => {}'.format(colored('2','red', attrs=["bold"]), colored('HOLYPOP','cyan')))
            logger.menu('VENETIA','CAPTCHAS','[{}] => {}'.format(colored('3','red', attrs=["bold"]), colored('NAKED','cyan')))
            logger.menu('VENETIA','CAPTCHAS','[{}] => {}'.format(colored('4','red', attrs=["bold"]), colored('PRO-DIRECT','cyan')))
            logger.menu('VENETIA','CAPTCHAS','[{}] => {}'.format(colored('5','red', attrs=["bold"]), colored('RETURN TO Menu','cyan')))
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
                siteUrl = 'https://www.nakedcph.com/'
                siteKey = '6LeNqBUUAAAAAFbhC-CS22rwzkZjr_g4vMmqD_qo'
                siteName = 'NAKED'
            if CaptchasiteSelect == "4":
                siteUrl = 'https://www.prodirectbasketball.com/'
                siteKey = '6LdXsbwUAAAAAMe1vJVElW1JpeizmksakCUkLL8g'
                siteName = 'PRO-DIRECT'
            if CaptchasiteSelect == "5":
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

        if option == 8:
            logger.menu('VENETIA','ACCOUNTS','[{}] => {}'.format(colored('1','red', attrs=["bold"]), colored('HOLYPOP','cyan')))
            # logger.menu('VENETIA','ACCOUNTS','[{}] => {}'.format(colored('2','red', attrs=["bold"]), colored('PRO-DIRECT','cyan')))
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
            
            if AccountsiteSelect == "9999":
                sitekey = '6LdXsbwUAAAAAMe1vJVElW1JpeizmksakCUkLL8g'
                for i in range(int(amount)):
                    threading.Thread(target=ACCOUNTS.proDirect,args=(sitekey,proxies,'PRO-DIRECT',catchall,password, profile)).start()

        
            while threading.active_count() != 2:
                pass

            if threading.active_count() == 2:
                self.menu()
        
        elif option == 9:
            # self.menu()
            
            logger.menu('VENETIA','Cookies','[{}] => {}'.format(colored('1','red', attrs=["bold"]), colored('COURIR','cyan')))
            logger.menu('VENETIA','Cookies','[{}] => {}'.format(colored('2','red', attrs=["bold"]), colored('SLAM JAM','cyan')))
            logger.menu('VENETIA','COOKIES','[{}] => {}'.format(colored('3','red', attrs=["bold"]), colored('STARCOW','cyan')))
            logger.menu('VENETIA','Cookies','[{}] => {}'.format(colored('4','red', attrs=["bold"]), colored('RETURN TO Menu','cyan')))
            sys.stdout.write(colored(f'\n[{get_time()}][Venetia-Menu]','cyan',attrs=["bold"]))
            cookieSiteSelect = input(' Select a site => ')
            if cookieSiteSelect == "4":
                self.menu()

            sys.stdout.write('\n[{}][{}]'.format(colored(get_time(),'cyan',attrs=["bold"]), colored('Venetia-Menu','white')))
            proxies = input(' Enter proxy list name (leave empty for none) => ')
            if proxies == "":
                proxies = None

            sys.stdout.write('\n[{}][{}]'.format(colored(get_time(),'cyan',attrs=["bold"]), colored('Venetia-Menu','white')))
            amount = input(' Enter amount => ')

            if cookieSiteSelect == "1":
                for i in range(int(amount)):
                    threading.Thread(target=datadome.courir,args=(proxies,'Cookies','save')).start()

            if cookieSiteSelect == "2":
                sys.stdout.write('\n[{}][{}]'.format(colored(get_time(),'cyan',attrs=["bold"]), colored('Venetia-Menu','white')))
                region = input(' Enter Site Region (example: GB) => ')

                for i in range(int(amount)):
                    threading.Thread(target=datadome.slamjam,args=(proxies,'Cookies','save')).start()

            if cookieSiteSelect == "3":
                sys.stdout.write('\n[{}][{}]'.format(colored(get_time(),'cyan',attrs=["bold"]), colored('Venetia-Menu','white')))

                for i in range(int(amount)):
                    threading.Thread(target=datadome.starcow,args=(proxies,'Cookies','save')).start()


            while threading.active_count() != 2:
                pass

            if threading.active_count() == 2:
                self.menu()

        elif option == 10:
            logger.menu('VENETIA','Menu','{}'.format(colored('Goodbye...','yellow', attrs=["bold"])))
            time.sleep(3)
            os._exit(0)
        
        elif option > 10:
            logger.menu('VENETIA','Menu','{}'.format(colored('Invalid menu choice. Try again','yellow', attrs=["bold"])))
            time.sleep(3)
            self.menu()
            
                


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
                logger.menu('VENETIA','Menu','{}'.format(colored(f'Key Authorised','green', attrs=["bold"])))
                Menu()
            if auth["STATUS"] == 0:
                logger.menu('VENETIA','Menu','{}'.format(colored('Failed to auth key. Closing...','red', attrs=["bold"])))
                time.sleep(3)
                os._exit(0)

        else:
            auth = auth.auth(config["key"], uuid.getnode())
            if auth["STATUS"] == 1:
                logger.menu('VENETIA','Menu','{}'.format(colored(f'Key Authorised','green', attrs=["bold"])))
                Menu()
            if auth["STATUS"] == 0:
                logger.menu('VENETIA','Menu','{}'.format(colored('Failed to auth key. Closing...','red', attrs=["bold"])))
                time.sleep(3)
                os._exit(0)
