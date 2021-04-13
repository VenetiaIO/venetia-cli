import requests
import time
import threading
import json

from utils.logger import logger
from utils.log import log
from utils.webhook import Webhook
from utils.webhook import Webhook
from utils.functions import (
    loadProfile,
    loadSettings
)

def hook(webhookData,proxies):
    Webhook.threeDS(
        webhook=loadSettings()["webhook"],
        site=webhookData['site'],
        url=webhookData['url'],
        image=webhookData['image'],
        title=webhookData['product'],
        size=webhookData['size'],
        price=webhookData['price'],
        paymentMethod="Card",
        product=webhookData['product_url'],
        profile=webhookData["profile"],
        proxy=proxies,
        speed=webhookData['speed']
    )
    return

class threeDSecure:


    @staticmethod
    def solve(session, profile, data_in, webhookData, taskID, referer):
        session = requests.session()
        try:
            payerAuth = session.post('https://idcheck.acs.touchtechpayments.com/v1/payerAuthentication', data=data_in, headers={
                'referer':referer,
                'content-type': 'application/x-www-form-urlencoded',
                'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            log.info(e)
            time.sleep(1)
            return False

        if payerAuth.status_code == 200:
            try:
                transToken = payerAuth.text.split('token: "')[1].split('"')[0]
                payload = {"transToken":transToken}
                poll = session.post('https://poll.touchtechpayments.com/poll', json=payload, headers={
                    'authority': 'verifiedbyvisa.acs.touchtechpayments.com',
                    'accept-language': 'en-US,en;q=0.9',
                    'referer': 'https://verifiedbyvisa.acs.touchtechpayments.com/v1/payerAuthentication',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                    'accept':'*/*',
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                log.info(e)
                time.sleep(1)
                return False

            try:
                pollStatus = poll.json()['status']
            except:
                # logger.error(self.webhookData['site'],self.taskID,'Failed to get poll status. Retrying...')
                time.sleep(1)
                return False


            if pollStatus == "blocked":
                # logger.error(self.webhookData['site'],self.taskID,'Card Blocked. Retrying...')
                time.sleep(1)
                return False
            if pollStatus == "pending":
                logger.warning(webhookData['site'],taskID,'Polling 3DS...')

                threading.Thread(target=hook, args=(webhookData,session.proxies,),daemon=True).start()
                while poll.json()["status"] == "pending":
                    poll = session.post('https://poll.touchtechpayments.com/poll',headers={
                        'authority': 'verifiedbyvisa.acs.touchtechpayments.com',
                        'accept-language': 'en-US,en;q=0.9',
                        'referer': 'https://verifiedbyvisa.acs.touchtechpayments.com/v1/payerAuthentication',
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                        'accept':'*/*',
                    }, json=payload)
            
            try:
                if poll.json()["status"] == "success":
                    pass
                elif poll.json()["status"] == "failure":
                    raise Exception
                else:
                    raise Exception
            except Exception as e:
                # logger.error(self.webhookData['site'],self.taskID,'Failed to retrieve auth token for 3DS. Retrying...')
                time.sleep(1)
                return False


            try:
                authToken = poll.json()['authToken']
                logger.alert(webhookData['site'],taskID,'3DS Authorised')
        
                data = '{"transToken":"%s","authToken":"%s"}' % (transToken, authToken)
            except Exception as e:
                log.info(e)
                # logger.error(self.webhookData['site'],self.taskID,'Failed to retrieve auth token for 3DS. Retrying...')
                time.sleep(1)
                return False


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
                r = session.post("https://macs.touchtechpayments.com/v1/confirmTransaction",headers=headers, data=data)
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                time.sleep(1)
                return False

            try:
                pares = r.json()['Response']
                return {"MD":data_in['MD'], "PaRes":pares}
            except Exception as e:
                log.info(e)
                # logger.error(self.webhookData['site'],self.taskID,'Failed to confirm transaction. Retrying...')
                time.sleep(1)
                return False





