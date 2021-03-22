import requests
import time
import json

from utils.logger import logger
from utils.log import log
from utils.webhook import Webhook
from utils.webhook import Webhook
from utils.functions import (
    loadProfile,
    loadSettings
)

class threeDSecure:
    def __init__(self, session, profile, data, webhookData, taskID, referer):
        self.session = session
        self.profile = profile
        self.data = data
        self.webhookData = webhookData
        self.taskID = taskID
        self.referer = referer

        self.solve()

    
    def solve(self):
        while True:
            try:
                payerAuth = self.session.post('https://idcheck.acs.touchtechpayments.com/v1/payerAuthentication', data=self.data, headers={
                    'referer':self.referer,
                    'content-type': 'application/x-www-form-urlencoded',
                    'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                time.sleep(1)
                continue

            if payerAuth.status_code == 200:
                try:
                    transToken = payerAuth.text.split('token: "')[1].split('"')[0]
                    payload = {"transToken":transToken}
                    poll = self.session.post('https://poll.touchtechpayments.com/poll', json=payload, headers={
                        'authority': 'verifiedbyvisa.acs.touchtechpayments.com',
                        'accept-language': 'en-US,en;q=0.9',
                        'referer': 'https://verifiedbyvisa.acs.touchtechpayments.com/v1/payerAuthentication',
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                        'accept':'*/*',
                    })
                except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                    log.info(e)
                    time.sleep(1)
                    continue

                try:
                    pollStatus = poll.json()['status']
                except:
                    logger.error(self.webhookData['site'],self.taskID,'Failed to get poll status. Retrying...')
                    time.sleep(1)
                    continue


                if pollStatus == "blocked":
                    logger.error(self.webhookData['site'],self.taskID,'Card Blocked. Retrying...')
                    time.sleep(1)
                    continue
                if pollStatus == "pending":
                    Webhook.threeDS(
                        webhook=loadSettings()["webhook"],
                        site=self.webhookData['site'],
                        url=self.webhookData['url'],
                        image=self.webhookData['image'],
                        title=self.webhookData['product'],
                        size=self.webhookData['size'],
                        price=self.webhookData['price'],
                        paymentMethod="Card",
                        product=self.webhookData['product_url'],
                        profile=self.webhookData["profile"],
                        proxy=self.session.proxies,
                        speed=self.webhookData['speed']
                    )
                    logger.warning(self.webhookData['site'],self.taskID,'Polling 3DS...')
                    while poll.json()["status"] == "pending":
                        poll = self.session.post('https://poll.touchtechpayments.com/poll',headers={
                            'authority': 'verifiedbyvisa.acs.touchtechpayments.com',
                            'accept-language': 'en-US,en;q=0.9',
                            'referer': 'https://verifiedbyvisa.acs.touchtechpayments.com/v1/payerAuthentication',
                            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                            'accept':'*/*',
                        }, json=payload)
                
                try:
                    if poll.json()["status"] == "success":
                        authToken = poll.json()['authToken']
                    if poll.json()["status"] == "failure":
                        return False
                    else:
                        logger.error(self.webhookData['site'],self.taskID,'Failed to retrieve auth token for 3DS . Retrying...')
                        time.sleep(1)
                        continue
                except:
                    logger.error(self.webhookData['site'],self.taskID,'Failed to retrieve auth token for 3DS. Retrying...')
                    time.sleep(1)
                    continue


                try:
                    authToken = poll.json()['authToken']
                    logger.alert(self.webhookData['site'],self.taskID,'3DS Authorised')
            
                    data = '{"transToken":"%s","authToken":"%s"}' % (transToken, authToken)
                except:
                    logger.error(self.webhookData['site'],self.taskID,'Failed to retrieve auth token for 3DS. Retrying...')
                    time.sleep(1)
                    continue


                headers = {
                    'authority': 'macs.touchtechpayments.com',
                    'sec-fetch-dest': 'empty',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
                    'content-type': 'application/json',
                    'accept': '*/*',
                    'origin': 'https://verifiedbyvisa.acs.touchtechpayments.com',
                    'referer': 'https://verifiedbyvisa.acs.touchtechpayments.com/v1/payerAuthentication',
                    'sec-fetch-site': 'same-site',
                    'sec-fetch-mode': 'cors',
                }

                try:
                    r = self.session.post("https://macs.touchtechpayments.com/v1/confirmTransaction",headers=headers, data=data)
                except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                    time.sleep(1)
                    continue

                try:
                    pares = r.json()['Response']
                    data = {"MD":self.data['MD'], "PaRes":pares}
                except:
                    logger.error(self.webhookData['site'],self.taskID,'Failed to confirm transaction. Retrying...')
                    time.sleep(1)
                    continue


                return data

