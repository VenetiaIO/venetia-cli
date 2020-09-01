import requests
import random
import names
import json
from bs4 import BeautifulSoup

from utils.captcha import captcha
from utils.logger import logger
from utils.webhook import discord




def genCustomer(catchall):
    gender = random.choice(['male','female'])
    firstName = names.get_first_name(gender=gender)
    lastName = names.get_last_name()
    numbers = '{}{}{}'.format(random.randint(1,9),random.randint(1,9),random.randint(1,9))
    email = firstName + lastName + numbers + catchall

    year = '19{}{}'.format(random.randint(5,9),random.randint(0,9))
    month = random.randint(1,9)
    day = random.randint(1,27)
    formatted = '{}-{}-{}'.format(year,month,day)

    return {"email":email,"first":firstName,"last":lastName,"sex":gender.upper(),"birthday":formatted}

def loadSettings():
    with open(f'./data/config.json') as settings:
        settings = json.loads(settings.read())
        return settings

def loadProfile(profile):
    with open(f'./data/profiles/profile_{profile}.json') as profile:
        profile = json.loads(profile.read())
        return profile

def loadProxy(proxies,taskID):
    if proxies == "":
        return None
    elif proxies != "":
        with open(f'./data/{proxies}.txt', 'r') as proxyIn:
            proxyInput = proxyIn.read().splitlines()
    
        proxyList = [i for i in proxyInput]
        p = random.choice(proxyList)
        p = p.split(':')
        try:
            proxies = {
                'http': f'http://{p[2]}:{p[3]}@{p[0]}:{p[1]}',
                'https': f'https://{p[2]}:{p[3]}@{p[0]}:{p[1]}'
            }
        except:
            proxies = {
                'http': f'http://{p[0]}:{p[1]}',
                'https': f'https://{p[0]}:{p[1]}'
            }
        return proxies

class ACCOUNTS:

    @staticmethod
    def holypop(sitekey,proxies,SITE,catchall,password,profile):
        taskID = 'ACCOUNTS'
        logger.warning(SITE,taskID,'Getting login page...')

        session = requests.session()
        proxies = loadProxy(proxies,taskID)
        session.proxies = proxies
        session.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'referer':'https://www.holypopstore.com'
        }

        getLogin = session.get('https://www.holypopstore.com/')
        if getLogin.status_code == 200:
            captchaResponse = captcha.Hiddenv2(sitekey,'https://www.holypopstore.com',proxies,SITE,taskID)

            version = getLogin.text.split("b.version = '")[1].split("';")[0]
            cookieVersion = getLogin.text.split("b.cookieVersion = '")[1].split("';")[0]
            region = getLogin.text.split("b.locale = '")[1].split("';")[0].upper()

            customer = genCustomer(catchall)

            payload = {
                'controller': 'auth',
                'action': 'register',
                'extension': 'holypop',
                'email': customer["email"],
                'password': password,
                'firstName': customer["first"],
                'lastName': customer["last"],
                'birthDate': customer["birthday"],
                'sex': customer["sex"],
                'privacy[1]': 1,
                'privacy[2]': 0,
                'recaptcha': captchaResponse,
                'language': region,
                'version': version,
                'cookieVersion': cookieVersion
            }


            session.headers['x-requested-with'] = 'XMLHttpRequest'
            session.headers['accept'] = 'application/json, text/javascript, */*; q=0.01'
            postInfo = session.post('https://www.holypopstore.com/index.php',data=payload)
            if postInfo.status_code == 200:
                logger.success(SITE,taskID,'Created Account - {}'.format(customer["email"]))
                profile = loadProfile(profile)

                with open('./data/holypop.txt','r') as holypop:
                    holypop = holypop.read()
                            
                soup = BeautifulSoup(holypop,"html.parser")
                options = soup.find_all("option")
                for s in options:
                    if str(s.text).lower() == profile["country"].lower():
                        countryId = s["value"]



                logger.warning(SITE,taskID,'Adding Address...')
                payload = {
                    'controller': 'users',
                    'action': 'saveAddresses',
                    'addresses[0][counter]': 'nn1',
                    'addresses[0][first_name]': customer["first"],
                    'addresses[0][last_name]': customer["last"],
                    'addresses[0][full_name]': '{} {}'.format(customer["first"], customer["last"]),
                    'addresses[0][email]': customer["email"],
                    'addresses[0][street_address]': '{} {}, {}'.format(profile["house"], profile["addressOne"], profile["addressTwo"]),
                    'addresses[0][zipcode]': profile["zip"],
                    'addresses[0][cityName]': profile["city"],
                    'addresses[0][statecode]': profile["region"],
                    'addresses[0][countryId]': countryId,
                    'addresses[0][countryName]': profile["country"],
                    'addresses[0][phone_number]': profile["phone"],
                    'addresses[0][isDefault]': 1,
                    'extension': 'holypop',
                    'language': region,
                    'version': version,
                    'cookieVersion': cookieVersion
                }
                postInfo = session.post('https://www.holypopstore.com/index.php',data=payload)
                logger.success(SITE,taskID,'Address Added!')
                discord.accountMade(
                    webhook=loadSettings()["webhook"],
                    site=SITE,
                    first=customer["first"],
                    last=customer["last"],
                    email=customer["email"]
                )
                with open('./data/accounts/holypop.txt','a') as accounts:
                    accounts.write('\n{}:{}'.format(customer["email"],password))

            


