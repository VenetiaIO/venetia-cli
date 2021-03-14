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
import asyncio

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
from utils.functions import (loadCheckouts, getUser, loadProfile, decodeURIComponent)
from utils.webhook import Webhook
from utils.config import *
import utils.create_data_files as dataFiles
from utils.cartClear import cartClear

async def checkUpdate():
    status = await Updater.checkForUpdate(VERSION())
    if status["error"] == False:
        if status["latest"] == True:
            await logger.menu('VENETIA','Menu','{}'.format(colored(f'You are on the latest version! {VERSION()}','green', attrs=["bold"])))
            return True
        if status["latest"] == False:
            await logger.menu('VENETIA','Menu','{}'.format(colored(f'Updating...','magenta', attrs=["bold"])))
            download = await Updater.downloadLatest(status["version"])
            if download == "complete":
                await logger.menu('VENETIA','Menu','{}'.format(colored(f'Update complete. Please delete the old file named "venetiaCLI_old.exe" and open the new one name "venetiaCLI.exe"','cyan', attrs=["bold"])))
                await asyncio.sleep(5)
                sys.exit()
            else:
                await logger.menu('VENETIA','Menu','{}'.format(colored('Failed to download latest version. Please try again later.','red', attrs=["bold"])))
    if status["error"] == True:
        await logger.menu('VENETIA','Menu','{}'.format(colored('Failed to check version. Retrying...','red', attrs=["bold"])))
        await asyncio.sleep(10)
        await checkUpdate()

async def taskCount():
    total = 0
    for k in sites.keys():
        with open(f'./{k.lower()}/tasks.csv','r') as csvFile:
            csv_reader = csv.DictReader(csvFile)
            total = total + len(list(csv_reader))
    
    return total

async def taskCountSpecific(site):
    total = 0
    with open(f'./{site.lower()}/tasks.csv','r') as csvFile:
            csv_reader = csv.DictReader(csvFile)
            total = total + len(list(csv_reader))
    
    return total

async def get_time():
    x = datetime.datetime.now().strftime('%Y.%m.%d | %H:%M:%S.%f')
    return x

async def checkTasks(site):
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
    
async def checkFootlockerTasks():
    old_ftl = []
    new_ftl = []
    with open(f'./footlocker/tasks.csv','r') as csvFile:
        csv_reader = csv.DictReader(csvFile)
        for r in csv_reader:
            if len(r['PRODUCT']) > 1:
                try:
                    prof = await loadProfile(r['PROFILE'])
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
        pass
    
    async def base(self):
        await checkUpdate()

        threading.Thread(target=QT,daemon=True).start()

        self.user = await getUser()
        
        try:
            client_id = 726839544124670093
            self.RPC = await Presence(client_id)
            await self.RPC.connect()
            self.rpctime = int(time.time())
        except:
            pass

        await asyncio.sleep(1)

        with open('./data/config.json') as config:
            self.config = json.loads(config.read())
            self.key = self.config["key"]
        
        while True:
            self.option_main_menu_choice = int(await self.menu())
            if self.option_main_menu_choice == 1:
                await self.startAllTasks()
                # Start All Tasks

            elif self.option_main_menu_choice == 2:
                await self.startSpecificTasks()
                # Start Specific Tasks

            elif self.option_main_menu_choice == 3:
                await self.edit_view_config()
                # View / Edit Config


            elif self.option_main_menu_choice == 4:
                await self.view_edit_create_profiles()
                # Create Profile

            elif self.option_main_menu_choice == 5:
                pass
                # Generate Captchas

            elif self.option_main_menu_choice == 6:
                pass
                # Account Generator

            elif self.option_main_menu_choice == 7:
                pass
                # Cookie Generator

            elif self.option_main_menu_choice == 8:
                pass
                # View Checkouts

            elif self.option_main_menu_choice == 00:
                await logger.menu2('VENETIA','Menu','{}'.format(colored('Goodbye...','yellow', attrs=["bold"])))
                await asyncio.sleep(3)
                break
                os._exit(0)
            
            else:
                await logger.menu2('VENETIA','Menu','{}'.format(colored('Invalid menu choice...','yellow', attrs=["bold"])))
                await asyncio.sleep(3)
                os._exit(0)


    async def menu(self):
        print('                 Welcome {}...                  '.format(self.user['discordName']))
        await logger.logo(logo,VERSION())
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
        menu_options.append( colored('[ 07 ] Cookie Gen','red', attrs=["bold"]))
        menu_options.append( colored('[ 08 ] View Checkouts','red', attrs=["bold"]))
        menu_options.append( colored('[ 00 ] Exit','red', attrs=["bold"]))

        async def menu_selector():
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

        return await menu_selector()   

    async def startAllTasks(self):         
        try:
            win32console.SetConsoleTitle("[Version {}] VenetiaCLI - {} | Carted: {} | Checked Out: {}".format(VERSION(),"Running Tasks","0","0"))
        except:
            pass

        async def menu_selector_waterfall():
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

                            prof = await loadProfile(row['PROFILE'])
                            if prof['countryCode'].upper() in new_footlockers():
                                new_task = asyncio.create_task( sites.get('FOOTLOCKER_NEW')(row, taskName, a).tasks())
                                main_tasks.append(new_task)
                                # threading.Thread(target=sites.get('FOOTLOCKER_NEW'),args=(row,taskName, a)).start()

                            if prof['countryCode'].upper() in old_footlockers():
                                new_task = asyncio.create_task( sites.get('FOOTLOCKER_OLD')(row, taskName, a).tasks())
                                main_tasks.append(new_task)
                                # threading.Thread(target=sites.get('FOOTLOCKER_OLD'),args=(row,taskName, a)).start()

                await asyncio.gather(*main_tasks)
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
                            
                            new_task = asyncio.create_task( k.upper(row, taskName, a).tasks())
                            main_tasks.append(new_task)
                                
                            
                            a = a + 1

                if len(waterfall_tasks) > 0:
                    if await menu_selector_waterfall() == 'yes':   
                        _delay_ =  input(f"[{get_time()}] Enter Waterfall monitor delay (in seconds) ==> ")
                        WaterfallAssign.assign(waterfall_tasks,_delay_)
                    else:
                        await asyncio.gather(*main_tasks)
                            
                else:
                    await asyncio.gather(*main_tasks)
    
    async def siteSelectFunc(self, availableSites, siteSelection):
        async def menu_selector_waterfall():
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

                            new_task = asyncio.create_task( value_chosen(row, taskName, a).tasks())
                            all_specific_tasks.append(new_task)
                            # threading.Thread(target=value_chosen,args=(row,taskName,a)).start()
                            a = a + 1

                await asyncio.gather(*all_specific_tasks)

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
                n = await taskCountSpecific(key_chosen) 
            

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
                            row['PROXIES'] = 'proxies'
                            row["ACCOUNT EMAIL"] = acc.split(':')[0]
                            row["ACCOUNT PASSWORD"] = acc.split(':')[1]
                            row["SITE"] = key_chosen
                            row["TASK_NAME"] = taskName
                            row["ROW_NUMBER"] = a
                            if key_chosen.lower() in waterfall_sites():
                                waterfall__tasks.append(row)
                            
                            new_task = asyncio.create_task( value_chosen(row, taskName, a).tasks())
                            all_specific_tasks.append(new_task)
                            a = a + 1
                            
                if len(waterfall__tasks) > 0:
                    if await menu_selector_waterfall() == 'yes':   
                        _delay_ =  input(f"[{get_time()}] Enter Waterfall monitor delay (in seconds) ==> ")
                        WaterfallAssign.assign(waterfall__tasks,_delay_)
                    else:
                        await asyncio.gather(*all_specific_tasks)
                            
                else:
                    await asyncio.gather(*all_specific_tasks)
            
        except Exception as e:
            pass


    async def startSpecificTasks(self):
        number = 1
        availableSites = {}
        all_available_sites = []
        for row in sorted(sites):
            if row.upper() == 'FOOTLOCKER_NEW':
                pass
            elif row.upper() == 'FOOTLOCKER_OLD':
                check = await checkFootlockerTasks()
                if check['status'] == True:
                    if len(check['old_ftl']) > 0:
                        availableSites['Footlocker EU'] = sites['FOOTLOCKER_OLD']
                    if len(check['new_ftl']) > 0:
                        availableSites['Footlocker EU'] = sites['FOOTLOCKER_NEW']

            elif await checkTasks(row) and row.upper() not in ['FOOTLOCKER_NEW','FOOTLOCKER_OLD']:
                availableSites[row] = sites[row]

        for s in availableSites:
            all_available_sites.append( colored(f'[ {number} ] {s.title()}','red', attrs=["bold"]))
            # logger.menu('VENETIA','Menu','[ {} ] => {}'.format(colored(number,'red', attrs=["bold"]), colored(s.title(),'red', attrs=["bold"])))
            number = number + 1
        all_available_sites.append( colored(f'[ 00 ] Return to menu','red', attrs=["bold"]))

        async def site_selector_specific():
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

        siteSelection = await site_selector_specific()
        if siteSelection == 00:
            return
        else:
            await self.siteSelectFunc(availableSites, siteSelection)



    async def edit_view_config(self):
        
        def flask_app_edit_config():
            edit_config_app = Flask(__name__)

            edit_config_app_port = random.randint(1024,65535)
            webbrowser.open_new(f'http://127.0.0.1:{edit_config_app_port}')

            @edit_config_app.route('/')
            def edit_config_route():
                with open('./data/config.json') as config:
                    config = json.loads(config.read())
                    return render_template('config.html',config=config)

    
            @edit_config_app.route('/update/config', methods=['POST'])
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
                
                # with open('./data/config.json') as config:
                #     config = json.loads(config.read())
                #     return render_template('config.html',config=config)
                return redirect('/')
            
            @edit_config_app.route('/config/webhook/test', methods=['GET'])
            def edit_config_route_webhook_test():
                Webhook.test(webhook=decodeURIComponent(request.args.get('webhook')))
                
                return redirect('/')
                        

            edit_config_app.run(port=edit_config_app_port)


            
        
        t = threading.Thread(target=flask_app_edit_config,daemon=True).start()

        input('[ENTER] to return to menu...')
        threading.currentThread().handled = True
        await self.menu()


    async def view_edit_create_profiles(self):

        def flask_app_profiles():
            profiles_config_app = Flask(__name__)

            profiles_config_app_port = random.randint(1024,65535)
            webbrowser.open_new(f'http://127.0.0.1:{profiles_config_app_port}')

            @profiles_config_app.route('/')
            def edit_config_route():
                with open('./data/profiles/profiles.json') as profiles_data:
                    profiles_ = json.loads(profiles_data.read())
                    return render_template('profiles.html',profiles=profiles_)

    
                        

            profiles_config_app.run(port=profiles_config_app_port)


            
        
        t = threading.Thread(target=flask_app_profiles,daemon=True).start()

        input('[ENTER] to return to menu...')
        threading.currentThread().handled = True
        await self.menu()


async def main():
    asyncio.run(Menu())


if __name__ == "__main__":
    asyncio.run(Menu().base())