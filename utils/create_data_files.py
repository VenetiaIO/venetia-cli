import os
import json
import utils.config as CONFIG

def execute():

    try:
        os.mkdir('data')
    except:
        pass

    #check site folders
    try:
        for k in CONFIG.sites.keys():
            if k.lower() == 'footlocker_new':
                try:
                    f = open('./footlocker/tasks.csv')
                    f.readlines()
                except IOError:
                    try:
                        os.mkdir('footlocker')
                    except:
                        pass

                    print("Creating files for footlocker")
                    open('./footlocker/proxies.txt','w')
                    with open('./footlocker/tasks.csv','w') as tasks:
                        tasks.write('PRODUCT,SIZE,DELAY,PROFILE,PAYMENT')

            elif k.lower() not in ['footlocker_old','footlocker_new'] :
                try:
                    f = open('./{}/tasks.csv'.format(k.lower()))
                    f.readlines()
                except IOError:
                    try:
                        os.mkdir('{}'.format(k.lower()))
                    except:
                        pass
    
                    else:
                        print("Creating files for {}".format(k.lower()))
        
                        open('./{}/proxies.txt'.format(k.lower()),'w')
                        if k.lower() in ['holypop','naked','footasylum','snipes','wch','prodirect']:
                            # open('./data/{}/accounts.txt'.format(k.lower()),'w')
                            task = 'PRODUCT,SIZE,DELAY,PROFILE,PAYMENT,ACCOUNT EMAIL,ACCOUNT PASSWORD'
                        else:
                            task = 'PRODUCT,SIZE,DELAY,PROFILE,PAYMENT'
                        with open('./{}/tasks.csv'.format(k.lower()),'w') as tasks:
                            tasks.write(task)
    except:
        pass

    #check checkouts.json
    try:
        f = open('./data/checkouts.json')
        f.readlines()
    except IOError:
        print('Creating checkouts.json')
        with open('./data/checkouts.json','w') as checkouts:
            json.dump([], checkouts)


    #check config.json
    try:
        f = open('./data/config.json')
        f.readlines()
    except IOError:
        print('Creating config.json')
        configFile = {
            "key": "",
            "checkoutNoise":"Y",
            "webhook": "",
            "2Captcha": "",
            "AntiCaptcha": "",
            "quickTaskSize": "random",
            "quickTaskProfile": "",
            "quickTaskProxies": "",
            "quickTaskDelay": "0",
            "quickTaskPayment": "",
            "quickTaskEmail": "",
            "quickTaskPassword": ""
        }

        with open('./data/config.json','w') as config:
            json.dump(configFile, config)


    #check profiles.json
    try:
        f = open('./data/profiles/profiles.json')
        f.readlines()
    except IOError:
        print('Creating profiles.json')
        profilesFile = {
            "profiles":[]
        }
        try:
            os.mkdir('data/profiles')
        except:
            pass
        with open('./data/profiles/profiles.json','w') as profiles:
            json.dump(profilesFile, profiles)


    #check datadome.json
    try:
        f = open('./data/cookies/datadome.json')
        f.readlines()
    except IOError:
        print('Creating datadome.json')
        datadomeFile = {}
        for k in CONFIG.sites.keys():
            datadomeFile[k.upper()] = []

        try:
            os.mkdir('data/cookies')
        except:
            pass
        with open('./data/cookies/datadome.json','w') as dd:
            json.dump(datadomeFile, dd)


    #check tokens.json
    try:
        f = open('./data/captcha/tokens.json')
        f.readlines()
    except IOError:
        print('Creating tokens.json')
        tokensFile = {}
        for k in CONFIG.sites.keys():
            tokensFile[k.upper()] = []
            
        try:
            os.mkdir('data/captcha')
        except:
            pass
        with open('./data/captcha/tokens.json','w') as tokens:
            json.dump(tokensFile, tokens)

    #check holypop.txt
    try:
        f = open('./data/accounts/holypop.txt')
        f.readlines()
    except IOError:
        try:
            os.mkdir('data/accounts')
        except:
            pass
        print('Creating holypop.txt')
        open('./data/accounts/holypop.txt','w')


    #check prodirect.txt
    try:
        f = open('./data/accounts/prodirect.txt')
        f.readlines()
    except IOError:
        try:
            os.mkdir('data/accounts')
        except:
            pass
        print('Creating prodirect.txt')
        open('./data/accounts/prodirect.txt','w')

