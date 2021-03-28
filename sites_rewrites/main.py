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
from pprint import pprint
import inquirer
from inquirer.themes import GreenPassion
from flask import Flask,render_template,request,redirect

import webbrowser
import names
import random
from copy import copy
# import asyncio

init(autoreset=True)

def secho(text, file=None, nl=None, err=None, color=None, **styles):
    pass

def echo(text, file=None, nl=None, err=None, color=None, **styles):
    pass

click.echo = echo
click.secho = secho

try:
    win32console.SetConsoleTitle("[Version {}] VenetiaCLI".format(VERSION()))
except:
    pass


try:
    import win32console 
except:
    pass

#utils

from utils.waterfall import WaterfallAssign
from utils.quicktask import QT
from utils.captcha import captcha
from utils.logger import logger
from utils.accounts import ACCOUNTS
from utils.auth import auth
from utils.datadome import datadome
from utils.ascii import logo
from utils.updates import Updater
from utils.functions import (loadCheckouts, getUser, loadProfile, decodeURIComponent,b64Encode)
from utils.webhook import Webhook
from utils.config import *
import utils.create_data_files as dataFiles
from utils.cartClear import cartClear

def checkUpdate():
    if VERSION() == '0.0.0':
        return True
    else:
        status = Updater.checkForUpdate(VERSION())
        if status["error"] == False:
            if status["latest"] == True:
                print(colored(f'You are on the latest version! {VERSION()}','green', attrs=["bold"]))
                return True
            if status["latest"] == False:
                download = Updater.downloadLatest(status["version"])
                if download == "complete":
                    print(colored('Update complete','cyan', attrs=["bold"]))
                    try:
                        pass
                        os.startfile("VenetiaCLI.exe".format(status['version']))
                    except:
                        pass
                    time.sleep(5)
                    sys.exit()
                else:
                    print(colored('Failed to download latest version. Please try again later.','red', attrs=["bold"]))
                    time.sleep(5)
                    sys.exit()
        if status["error"] == True:
            print(colored('Failed to download latest version. Retrying...','red', attrs=["bold"]))
            time.sleep(10)
            checkUpdate()

def taskCount():
    total = 0
    for k in sites.keys():
        with open(f'./{k.lower()}/tasks.csv','r') as csvFile:
            csv_reader = csv.DictReader(csvFile)
            total = total + len(list(csv_reader))
    
    return total

def taskCountSpecific(site):
    total = 0
    with open(f'./{site.lower()}/tasks.csv','r') as csvFile:
            csv_reader = csv.DictReader(csvFile)
            total = total + len(list(csv_reader))
    
    return total

def get_time():
    x = datetime.datetime.now().strftime('%Y.%m.%d | %H:%M:%S.%f')
    return x

def checkTasks(site):
    tasks = []
    with open(f'./{site.lower()}/tasks.csv','r') as csvFile:
        csv_reader = csv.DictReader(csvFile)
        for r in csv_reader:
            if len(r['PRODUCT']) > 1:
                tasks.append(1)
    
    if len(tasks) > 0:
        return True
    elif len(tasks) == 0:
        return False
    
def checkFootlockerTasks():
    old_ftl = []
    new_ftl = []
    with open(f'./footlocker/tasks.csv','r') as csvFile:
        csv_reader = csv.DictReader(csvFile)
        for r in csv_reader:
            if len(r['PRODUCT']) > 1:
                try:
                    prof = loadProfile(r['PROFILE'])
                    cc = prof['countryCode'].upper()
                except Exception:
                    return {
                        "status":False,
                        "old_ftl":0,
                        "new_ftl":0
                    }
                if cc in new_footlockers():
                    new_ftl.append(1)
                if cc in old_footlockers():
                    old_ftl.append(1)
                else:
                    pass
        
    if len(old_ftl) > 0 or len(new_ftl) > 0:
        return {
            "status":True,
            "old_ftl":old_ftl,
            "new_ftl":new_ftl
        }
    elif len(old_ftl) == 0 and len(new_ftl) == 0:
        return {
            "status":False,
            "old_ftl":old_ftl,
            "new_ftl":new_ftl
        }


class Menu():
    def __init__(self):
        self.port = start_server()
        pass
    
    def base(self):
        checkUpdate()

        threading.Thread(target=QT,daemon=True).start()
        

        self.user = getUser()
        
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
        
        while True:
            self.option_main_menu_choice = int(self.menu())
            if self.option_main_menu_choice == 1:
                self.startAllTasks()
                break
                # Start All Tasks

            elif self.option_main_menu_choice == 2:
                self.startSpecificTasks()
                break
                # Start Specific Tasks

            elif self.option_main_menu_choice == 3:
                webbrowser.open_new(f'http://127.0.0.1:{self.port}/configuration')
                # View / Edit Config


            elif self.option_main_menu_choice == 4:
                webbrowser.open_new(f'http://127.0.0.1:{self.port}/profiles')
                # Create Profile

            elif self.option_main_menu_choice == 5:
                webbrowser.open_new(f'http://127.0.0.1:{self.port}/captcha')
                # Generate Captchas

            elif self.option_main_menu_choice == 6:
                self.accountGen()
                # Account Generator

            elif self.option_main_menu_choice == 7:
                self.viewCheckouts()
                # View Checkouts

            elif self.option_main_menu_choice == 00:
                print(colored('Goodbye...','yellow', attrs=["bold"]))
                time.sleep(3)
                break
                os._exit(0)
            
            else:
                print(colored('Invalid Menu Choice','yellow', attrs=["bold"]))
                time.sleep(1)
                continue


    def menu(self):
        print('                 Welcome {}...                  '.format(self.user['discordName']))
        logger.logo(logo,VERSION())
        # logger.menu('VenetiaCLI','Menu','[ {} ] => {}'.format(colored('01','red', attrs=["bold"]), colored('Start All Tasks','red', attrs=["bold"])))
        # logger.menu('VenetiaCLI','Menu','[ {} ] => {}'.format(colored('02','red', attrs=["bold"]), colored('Start Specific Tasks','red', attrs=["bold"])))
        # logger.menu('VenetiaCLI','Menu','[ {} ] => {}'.format(colored('03','red', attrs=["bold"]), colored('View Config','red', attrs=["bold"])))
        # logger.menu('VenetiaCLI','Menu','[ {} ] => {}'.format(colored('04','red', attrs=["bold"]), colored('Edit Config','red', attrs=["bold"])))
        # logger.menu('VenetiaCLI','Menu','[ {} ] => {}'.format(colored('05','red', attrs=["bold"]), colored('Create Profile','red', attrs=["bold"])))
        # logger.menu('VenetiaCLI','Menu','[ {} ] => {}'.format(colored('06','red', attrs=["bold"]), colored('View|Edit Profiles','red', attrs=["bold"])))
        # logger.menu('VenetiaCLI','Menu','[ {} ] => {}'.format(colored('07','red', attrs=["bold"]), colored('Generate Captchas','red', attrs=["bold"])))
        # logger.menu('VenetiaCLI','Menu','[ {} ] => {}'.format(colored('08','red', attrs=["bold"]), colored('Account Gen','red', attrs=["bold"])))
        # logger.menu('VenetiaCLI','Menu','[ {} ] => {}'.format(colored('09','red', attrs=["bold"]), colored('Cookie Gen','red', attrs=["bold"])))
        # logger.menu('VenetiaCLI','Menu','[ {} ] => {}'.format(colored('10','red', attrs=["bold"]), colored('View Checkouts','red', attrs=["bold"])))
        # logger.menu('VenetiaCLI','Menu','[ {} ] => {}'.format(colored('99','red', attrs=["bold"]), colored('Exit','red', attrs=["bold"])))
        menu_options = []
        
        menu_options.append( colored('[ 01 ] Start All Tasks','red', attrs=["bold"]))
        menu_options.append( colored('[ 02 ] Start Specific Tasks','red', attrs=["bold"]))
        menu_options.append( colored('[ 03 ] View|Edit Config','red', attrs=["bold"]))
        menu_options.append( colored('[ 04 ] View|Create Profiles','red', attrs=["bold"]))
        menu_options.append( colored('[ 05 ] Generate Captchas','red', attrs=["bold"]))
        menu_options.append( colored('[ 06 ] Account Gen','red', attrs=["bold"]))
        menu_options.append( colored('[ 07 ] View Checkouts','red', attrs=["bold"]))
        menu_options.append( colored('[ 00 ] Exit','red', attrs=["bold"]))

        def menu_selector():
            questions = [
                inquirer.List(
                    "menu_choices",
                    message="Menu Selection",
                    choices=menu_options,
                ),
            ]
            answers = inquirer.prompt(questions)
            choi = answers['menu_choices'].split('[ ')[1].split(' ]')[0]
            return choi

        return menu_selector()   

    def startAllTasks(self):         
        try:
            win32console.SetConsoleTitle("[Version {}] VenetiaCLI - {} | Carted: {} | Checked Out: {}".format(VERSION(),"Running Tasks","0","0"))
        except:
            pass

        def menu_selector_waterfall():
            questions = [
                inquirer.List(
                    "waterfall_choices",
                    message="Use Waterfall",
                    choices=['Yes','No'],
                ),
            ]
            answers = inquirer.prompt(questions)
            choi = answers['waterfall_choices']
            return choi

        a = 0
        waterfall_tasks = []
        main_tasks = []
        for k in sites.keys():
            if k.upper() == 'FOOTLOCKER_NEW':
                pass
            elif k.upper() == 'FOOTLOCKER_OLD':
                with open(f'./footlocker/tasks.csv','r') as csvFile:
                    csv_reader = csv.DictReader(csvFile)
                    # total =  total + sum(1 for row in csv_reader)
                    i = 1
                    for row in csv_reader:
                        if row["PRODUCT"] != "":
                            try:
                                self.RPC.update(large_image="image", state=f"Version {VERSION()}", details=f'Running {taskCount()} Task(s)...'.format('Footlocker EU'), start=self.rpctime,small_image="image",small_text="@venetiaIO")
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
                            # row['PROXIES'] = 'proxies'

                            prof = loadProfile(row['PROFILE'])
                            if prof['countryCode'].upper() in new_footlockers():
                                # new_task = asyncio.create_task( sites.get('FOOTLOCKER_NEW')(row, taskName, a).tasks())
                                
                                new_task = threading.Thread(target=sites.get('FOOTLOCKER_NEW'),args=(row,taskName, a))
                                main_tasks.append(new_task)

                            if prof['countryCode'].upper() in old_footlockers():
                                # new_task = asyncio.create_task( sites.get('FOOTLOCKER_OLD')(row, taskName, a).tasks())
                                # main_tasks.append(new_task)
                                new_task = threading.Thread(target=sites.get('FOOTLOCKER_OLD'),args=(row,taskName, a))
                                main_tasks.append(new_task)
                                

                for t in main_tasks:
                    t.start()
                return

            elif k.upper() not in ['FOOTLOCKER_NEW','FOOTLOCKER_OLD']:
                allAccounts = []
                try:
                    accounts = open(f'./{k.lower()}/accounts.txt','r').readlines()
                    for a in accounts:
                        if a.strip() != '':
                            a = a.replace('\n','')
                            allAccounts.append(a)
                except:
                    pass
                
                allAccCopy = copy(allAccounts)
                if len(allAccCopy) == 0:
                    for i in range(2000):
                        allAccCopy.append(':')

                random.shuffle(allAccCopy)
                n2 = taskCountSpecific(k) 

                
                with open(f'./{k.lower()}/tasks.csv','r') as csvFile:
                    csv_reader = csv.DictReader(csvFile)
                    # total =  total + sum(1 for row in csv_reader)
    
                    i = 1
                    zip2 = zip(csv_reader, allAccCopy[:n2])
                    for row, acc in zip2:
                        if row["PRODUCT"] != "":
                            try:
                                self.RPC.update(large_image="image", state=f"Version {VERSION()}", details=f'Running {taskCount()} Task(s)...'.format(k.title()), start=self.rpctime,small_image="image",small_text="@venetiaIO")
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
                            # row['PROXIES'] = 'proxies'
                            row["ACCOUNT EMAIL"] = acc.split(':')[0]
                            row["ACCOUNT PASSWORD"] = acc.split(':')[1]
                            row["SITE"] = k
                            row["TASK_NAME"] = taskName
                            row["ROW_NUMBER"] = a
                            
                            if k.lower() in waterfall_sites():
                                # threading.Thread(target=sites.get(k.upper()),args=(row,taskName, a)).start()
                                waterfall_tasks.append(row)
                            
                            # new_task = asyncio.create_task( k.upper(row, taskName, a).tasks())
                            new_task = threading.Thread(target=sites.get(k.upper()),args=(row,taskName, a))
                            main_tasks.append(new_task)
                                
                            
                            a = a + 1

                if len(waterfall_tasks) > 0:
                    if menu_selector_waterfall() == 'yes':   
                        _delay_ =  input(f"[{get_time()}] Enter Waterfall monitor delay (in seconds) ==> ")
                        WaterfallAssign.assign(waterfall_tasks,_delay_)
                    else:
                        for t in main_tasks:
                            t.start()
                            
                else:
                    for t in main_tasks:
                        t.start()
    
    def siteSelectFunc(self, availableSites, siteSelection):
        def menu_selector_waterfall():
            questions = [
                inquirer.List(
                    "waterfall_choices",
                    message="Use Waterfall",
                    choices=['Yes','No'],
                ),
            ]
            answers = inquirer.prompt(questions)
            choi = answers['waterfall_choices']
            return choi

        try:
            waterfall__tasks = []
            all_specific_tasks = []

            key_chosen, value_chosen = sorted(availableSites.items())[int(siteSelection) -1 ]
            if  key_chosen == 'Footlocker EU':
                with open('./footlocker/tasks.csv','r') as csvFile:
                    csv_reader = csv.DictReader(csvFile)
                    i = 1
                    a = 0
                    for row in csv_reader:
                        if row["PRODUCT"] != "":
                            try:
                                try:
                                    win32console.SetConsoleTitle("[Version {}] VenetiaIO CLI - {} | Carted: {} | Checked Out: {}".format(VERSION(),key_chosen.title(),"0","0"))
                                except:
                                    pass
                                self.RPC.update(large_image="image", state=f"Version {VERSION()}", details='Destroying {}...'.format(key_chosen.title()), start=self.rpctime,small_image="image",small_text="@venetiaIO")
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
                            # row['PROXIES'] = 'proxies'

                            # new_task = asyncio.create_task( value_chosen(row, taskName, a).tasks())
                            new_task = threading.Thread(target=value_chosen,args=(row,taskName,a))
                            all_specific_tasks.append(new_task)
                            
                            a = a + 1

                # await asyncio.gather(*all_specific_tasks)
                for t in all_specific_tasks:
                    t.start()

            else:

                allAccounts = []
                try:
                    accounts = open(f'./{key_chosen.lower()}/accounts.txt','r').readlines()
                    for a in accounts:
                        if a.strip() != '':
                            a = a.replace('\n','')
                            allAccounts.append(a)
                except:
                    pass
                

                allAccCopy = copy(allAccounts)
                if len(allAccCopy) == 0:
                    for i in range(2000):
                        allAccCopy.append(':')

                random.shuffle(allAccCopy)
                n = taskCountSpecific(key_chosen) 
            

                tasks = []
                with open('./{}/tasks.csv'.format(key_chosen.lower()),'r') as csvFile:
                    csv_reader = csv.DictReader(csvFile)
                    i = 1
                    a = 0
                    zip1 = zip(csv_reader, allAccCopy[:n])
                    for row, acc in zip1:
                        if row["PRODUCT"] != "":
                            try:
                                try:
                                    win32console.SetConsoleTitle("[Version {}] VenetiaIO CLI - {} | Carted: {} | Checked Out: {}".format(VERSION(),key_chosen.title(),"0","0"))
                                except:
                                    pass
                                self.RPC.update(large_image="image", state=f"Version {VERSION()}", details='Destroying {}...'.format(key_chosen.title()), start=self.rpctime,small_image="image",small_text="@venetiaIO")
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
                            row["ACCOUNT EMAIL"] = acc.split(':')[0]
                            row["ACCOUNT PASSWORD"] = acc.split(':')[1]
                            row["SITE"] = key_chosen
                            row["TASK_NAME"] = taskName
                            row["ROW_NUMBER"] = a
                            if key_chosen.lower() in waterfall_sites():
                                waterfall__tasks.append(row)
                            
                            # new_task = asyncio.create_task( value_chosen(row, taskName, a).tasks())
                            new_task = threading.Thread(target=value_chosen,args=(row,taskName,a))
                            all_specific_tasks.append(new_task)
                            a = a + 1
                            
                if len(waterfall__tasks) > 0:
                    if menu_selector_waterfall() == 'yes':   
                        _delay_ =  input(f"[{get_time()}] Enter Waterfall monitor delay (in seconds) ==> ")
                        WaterfallAssign.assign(waterfall__tasks,_delay_)
                    else:
                        for t in all_specific_tasks:
                            t.start()
                            
                else:
                    for t in all_specific_tasks:
                        t.start()
            
        except Exception as e:
            pass


    def startSpecificTasks(self):
        number = 1
        availableSites = {}
        all_available_sites = []

        for row in sorted(sites):
            if row.upper() == 'FOOTLOCKER_NEW':
                pass
            elif row.upper() == 'FOOTLOCKER_OLD':
                check = checkFootlockerTasks()
                if check['status'] == True:
                    if len(check['old_ftl']) > 0:
                        availableSites['Footlocker EU'] = sites['FOOTLOCKER_OLD']
                    if len(check['new_ftl']) > 0:
                        availableSites['Footlocker EU'] = sites['FOOTLOCKER_NEW']

            elif checkTasks(row) and row.upper() not in ['FOOTLOCKER_NEW','FOOTLOCKER_OLD']:
                availableSites[row] = sites[row]

        for s in availableSites:
            all_available_sites.append( colored(f'[ {number} ] {s.title()}','red', attrs=["bold"]))
            # logger.menu('VENETIA','Menu','[ {} ] => {}'.format(colored(number,'red', attrs=["bold"]), colored(s.title(),'red', attrs=["bold"])))
            number = number + 1
        all_available_sites.append( colored(f'[ 00 ] Return to menu','red', attrs=["bold"]))

        def site_selector_specific():
            questions = [
                inquirer.List(
                    "specific_site_choices",
                    message="Select Site",
                    choices=all_available_sites,
                ),
            ]
            answers = inquirer.prompt(questions)
            choi = int(answers['specific_site_choices'].split('[ ')[1].split(' ]')[0])
            return choi

        siteSelection = site_selector_specific()
        if siteSelection == 00:
            return
        else:
            self.siteSelectFunc(availableSites, siteSelection)

    
    def accountGen(self):
        def site_selector_account():
            questions = [
                inquirer.List(
                    "account_select",
                    message="Select Site",
                    choices=[
                        'Holypop',
                        'Pro-Direct',
                        'Footasylum',
                        'Snipes',
                        'Naked',
                        'WorkingClassHeroes',
                        'Ambush',
                        'Return to menu...'
                    ],
                ),
            ]
            answers = inquirer.prompt(questions)
            choi = answers['account_select']
            return choi

        account_selection = site_selector_account()
        if account_selection == 'Return to menu...':
            return
        else:
            amount_account_gen = int(input("Number of accounts: "))
            catchall_account_gen = input("Enter catchall (include @): ")
            password_account_gen = input("Enter password for accounts: ")
            profile_account_gen = input("Enter profile name: ")
            proxies_account_gen = input("Enter proxylist name: ")

            before_thread = threading.active_count()
            if account_selection == 'Holypop':
                siteKey = '6Lc8GBUUAAAAAKMfe1S46jE08TvVKNSnMYnuj6HN'
                for i in range(int(amount_account_gen)):
                    threading.Thread(target=ACCOUNTS.holypop,args=(siteKey,proxies_account_gen,'Holypop',catchall_account_gen,password_account_gen, profile_account_gen)).start()
            
            elif account_selection == 'Pro-Direct':
                siteKey = '6LdXsbwUAAAAAMe1vJVElW1JpeizmksakCUkLL8g'
                for i in range(int(amount_account_gen)):
                    threading.Thread(target=ACCOUNTS.proDirect,args=(siteKey,proxies_account_gen,'ProDirect',catchall_account_gen,password_account_gen, profile_account_gen)).start()
            
            elif account_selection == 'Footasylum':
                siteKey = 'n/a'
                for i in range(int(amount_account_gen)):
                    threading.Thread(target=ACCOUNTS.footasylum,args=(siteKey,proxies_account_gen,'Footasylum',catchall_account_gen,password_account_gen, profile_account_gen)).start()

            elif account_selection == 'Snipes':
                siteKey = 'n/a'
                for i in range(int(amount_account_gen)):
                    threading.Thread(target=ACCOUNTS.snipes,args=(siteKey,proxies_account_gen,'Snipes',catchall_account_gen,password_account_gen, profile_account_gen)).start()

            elif account_selection == 'Naked':
                siteKey = '6LeNqBUUAAAAAFbhC-CS22rwzkZjr_g4vMmqD_qo'
                for i in range(int(amount_account_gen)):
                    threading.Thread(target=ACCOUNTS.naked,args=(siteKey,proxies_account_gen,'Naked',catchall_account_gen,password_account_gen, profile_account_gen)).start()
            
            elif account_selection == 'WorkingClassHeroes':
                siteKey = 'n/a'
                for i in range(int(amount_account_gen)):
                    threading.Thread(target=ACCOUNTS.wch,args=(siteKey,proxies_account_gen,'Wch',catchall_account_gen,password_account_gen, profile_account_gen)).start()
            
            elif account_selection == 'Ambush':
                siteKey = 'n/a'
                for i in range(int(amount_account_gen)):
                    threading.Thread(target=ACCOUNTS.ambush,args=(siteKey,proxies_account_gen,'Ambush',catchall_account_gen,password_account_gen, profile_account_gen)).start()
        
            while threading.active_count() != before_thread:
                pass

            return
    

    def viewCheckouts(self): 
        checkoutData = loadCheckouts()
        print(colored("Total Checkouts: [{}]".format(checkoutData['total']), 'cyan'))

        if int(checkoutData['total']) == 0:
            print(colored('No checkouts','red'))
            time.sleep(2)
            return
        
        elif int(checkoutData['total']) <= 30:
            count = int(checkoutData['total'])
        else:
            count  = 30

        options = []
        i__ = 1
        for i in checkoutData['checkouts'][-count:]:
            if i__ < 10:
                i_ = f'0{i__}'
            else:
                i_ = i__
            data = i
            i__ = i__ + 1
            # options.append('[{}]     {}                {}'.format(i_,data['site'].title(), data['product']))
            site = data['site'].title()
            prod = data['product']
            size = data['size']
            options.append(f'[{i_:<3}]   {site:<10}   {prod:<20}  | {size:<5}')
        
        options.append('[XX] Back to menu')

        def selector_checkouts():
            print("")
            questions = [
                inquirer.List(
                    "checkouts",
                    message="Select",
                    choices=options,
                ),
            ]
            answers = inquirer.prompt(questions)
            num = answers['checkouts'].split('[')[1].split(']')[0]
            if num == 'XX':
                return 'XX'

            link = checkoutData['checkouts'][int(num) -1]['checkout_url']
            webbrowser.open_new_tab(link)
            return num
        
        n = selector_checkouts()
        while n != 'XX':
            n = selector_checkouts()
        
        return




def start_server():


    def server(port):
        base_dir = '.'
        if hasattr(sys, '_MEIPASS'):
            base_dir = os.path.join(sys._MEIPASS)

        try:
            main_flask_server = Flask(
                __name__,
                static_folder=os.path.join(base_dir, 'static'),
                template_folder=os.path.join(base_dir, 'templates')
            )
        except:
            server(random.randint(1024,65535))

        # Captcha
        @main_flask_server.route('/captcha')
        def captcha_main_route():
            sites = []
            with open('./data/captcha/tokens.json') as cap_data:
                cap_data = json.loads(cap_data.read())

                for k in cap_data:
                    sites.append(k)
            
                return render_template('captcha.html',captchas=json.dumps(cap_data), sites=sites)


        @main_flask_server.route('/start_generating', methods=['POST'])
        def captcha_gen_route():
            site = request.form['site'].upper()
            amount = request.form['amount']
            proxies = request.form['proxies']


            for a in range(int(amount)):
                siteKey = captcha_configs[site]['siteKey']
                siteUrl = captcha_configs[site]['url']

                if captcha_configs[site]['type'].lower() == 'v2':
                    threading.Thread(target=captcha.menuV2,args=(siteKey,siteUrl,proxies,'CAPTCHA',site)).start()

                elif captcha_configs[site]['type'].lower() == 'v3':
                    threading.Thread(target=captcha.menuV3,args=(siteKey,siteUrl,proxies,'CAPTCHA',site)).start()
            
            return redirect('/captcha')

        @main_flask_server.route('/captchas/reset', methods=['GET'])
        def captcha_reset_route():

            
            data = {}
            for k in captcha_configs:
                if captcha_configs[k]['hasCaptcha'] == True:
                    data[k.upper()] = []

            with open('./data/captcha/tokens.json','w') as tokenFile:
                json.dump(data,tokenFile)


            
            return redirect('/captcha')

        # profiles
        @main_flask_server.route('/profiles')
        def edit_profile_route():
            with open('./data/profiles/profiles.json') as profiles_data:
                profiles_ = json.loads(profiles_data.read())
                return render_template('profiles.html',profiles=json.dumps(profiles_))

        @main_flask_server.route('/new/profile', methods=['POST'])
        def edit_profile_route_post_create():

            with open(f'./data/profiles/profiles.json','r') as profileRead:
                profiles = json.loads(profileRead.read())
            
            p = {
                "profileName":request.form['profile_name'],
                "firstName":request.form['first_name'],
                "lastName":request.form['last_name'],
                "email":request.form['email_address'],
                "phonePrefix":request.form['phone_prefix'],
                "phone": request.form['phone'],
                "house":request.form['house'],
                "addressOne":request.form['street_address'],
                "addressTwo":request.form['street_address_2'],
                "city":request.form['city'],
                "region":request.form['state'],
                "country":request.form['country'].split(':')[0],
                "countryCode":request.form['country'].split(':')[1],
                "zip":request.form['postal_code'],
                "card":{
                    "cardNumber":request.form['card_number'],
                    "cardMonth":request.form['card_month'],
                    "cardYear":request.form['card_year'],
                    "cardCVV":request.form['card_cvv']
                }
            }
            profiles["profiles"].append(p)
            with open(f'./data/profiles/profiles.json','w') as profileDump:
                json.dump(profiles, profileDump)

            return redirect('/profiles')

        @main_flask_server.route('/delete/profile', methods=['POST'])
        def edit_profile_route_delete():
            if request.method == "POST":
                arg_profile = str(decodeURIComponent(request.args.get('profile')))
                new_profiles = {
                    "profiles":[]
                }
                with open(f'./data/profiles/profiles.json','r') as profileRead:
                    profiles = json.loads(profileRead.read())
                    for p in profiles['profiles']:
                        if p['profileName'] == arg_profile:
                            pass
                        else:
                            new_profiles['profiles'].append(p)
                
                with open(f'./data/profiles/profiles.json','w') as profileDump:
                    json.dump(new_profiles, profileDump)
                
                return redirect('/profiles')

        @main_flask_server.route('/update/profile', methods=['POST'])
        def edit_profile_route_post_update():

            with open(f'./data/profiles/profiles.json','r') as profileRead:
                profiles = json.loads(profileRead.read())

            new_profile_data = {
                "profileName":request.form['profile_name'],
                "firstName":request.form['first_name'],
                "lastName":request.form['last_name'],
                "email":request.form['email_address'],
                "phonePrefix":request.form['phone_prefix'],
                "phone": request.form['phone'],
                "house":request.form['house'],
                "addressOne":request.form['street_address'],
                "addressTwo":request.form['street_address_2'],
                "city":request.form['city'],
                "region":request.form['state'],
                "country":request.form['country'].split(':')[0],
                "countryCode":request.form['country'].split(':')[1],
                "zip":request.form['postal_code'],
                "card":{
                    "cardNumber":request.form['card_number'],
                    "cardMonth":request.form['card_month'],
                    "cardYear":request.form['card_year'],
                    "cardCVV":request.form['card_cvv']
                }
            }

            new_profiles = {
                "profiles":[]
            }
            for p in profiles['profiles']:
                if str(p['profileName']) == str(new_profile_data['profileName']):
                    new_profiles['profiles'].append(new_profile_data)
                else:
                    new_profiles['profiles'].append(p)

            with open(f'./data/profiles/profiles.json','w') as profileDump:
                json.dump(new_profiles, profileDump)


            return redirect('/profiles')


        @main_flask_server.route('/import_profiles', methods=['POST'])
        def import_profiles_route():
            file = json.loads(request.files['file'].read().decode('Utf-8'))
            

            if request.form['keep_existing_profiles'] == 'true':
                # add to existing profiles
                with open(f'./data/profiles/profiles.json','r') as profileRead:
                    profiles = json.loads(profileRead.read())

                for p in file['profiles']:
                    profiles['profiles'].append(p)

                with open(f'./data/profiles/profiles.json','w') as profileDump:
                    json.dump(profiles, profileDump)

            else:
                # replace existing files
                with open(f'./data/profiles/profiles.json','w') as profileDump:
                    json.dump(file, profileDump)

            return redirect('/profiles')



        # config
        @main_flask_server.route('/configuration', methods=['GET'])
        def edit_config_route():
            with open('./data/config.json') as config:
                config = json.loads(config.read())
                return render_template('config.html',config=config)


        @main_flask_server.route('/update/config', methods=['POST'])
        def edit_config_route_post():
            if request.method == 'POST':
                with open('./data/config.json') as config:
                    config = json.loads(config.read())

                    config_updated = {
                        "key":config["key"],
                        "checkoutNoise":request.form['checkout_noise'],
                        "webhook":request.form['webhook'],
                        "2Captcha":request.form['2cap'],
                        "capMonster":request.form['cap_mon'],
                        "captcha":request.form['cap_choice'],
                        "quickTaskSize":request.form['qt_size'],
                        "quickTaskProfile":request.form['qt_profile'],
                        "quickTaskProxies":request.form['qt_proxies'],
                        "quickTaskDelay":request.form['qt_delay'],
                        "quickTaskPayment":request.form['qt_payment'],
                        "quickTaskEmail":request.form['qt_account_email'],
                        "quickTaskPassword":request.form['qt_account_password']
                    }

                    with open("./data/config.json","w") as updated:
                        json.dump(config_updated, updated)

            return redirect('/configuration')
            
        @main_flask_server.route('/config/webhook/test', methods=['POST'])
        def edit_config_route_webhook_test():
            if request.method == "POST":
                Webhook.test(webhook=decodeURIComponent(request.args.get('webhook')))
                return redirect('/configuration')

        
        main_flask_server.run(port=port)
    
    port = random.randint(1024,65535)
    t = threading.Thread(target=server,daemon=True, args=(port,)).start()
    return port



if __name__ == "__main__":
    dataFiles.execute()

    with open('./data/config.json') as config:
        config = json.loads(config.read())
        if config["key"] == "":
            key = input("Enter Your License Key ==> ")
            config["key"] = key
            with open("./data/config.json","w") as updated:
                json.dump(config, updated)

            auth = auth.auth(config["key"], uuid.getnode())
            if auth["STATUS"] == 1:
                k = config['key']
                print(colored(f'[ {k} ] Key Authorised','green', attrs=["bold"]))
                Menu().base()

            if auth["STATUS"] == 0:
                print(colored('Failed to auth key. Closing...','red', attrs=["bold"]))
                config["key"] = ""
                with open("./data/config.json","w") as updated:
                    json.dump(config, updated)

                time.sleep(3)
                os._exit(0)

        else:
            auth = auth.auth(config["key"], uuid.getnode())
            if auth["STATUS"] == 1:
                k = config['key']
                print(colored(f'[ {k} ] Key Authorised','green', attrs=["bold"]))
                Menu().base()
                # asyncio.run(Menu().base())

            if auth["STATUS"] == 0:
                print(colored('Failed to auth key. Closing...','red', attrs=["bold"]))
                config["key"] = ""
                with open("./data/config.json","w") as updated:
                    json.dump(config, updated)
                time.sleep(3)
                os._exit(0)
