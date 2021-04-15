import requests
from bs4 import BeautifulSoup
from utils.functions import (scraper, loadProxy)
import time
from tls.client import Session

class cartClear:
    @staticmethod
    def footasylum(taskID,accountE,accountP):
        SITE = 'FOOTASYLUM'
        s = Session()
        s.proxies = loadProxy('proxies',taskID,SITE)
         

        try:
            GETlogin = s.get('https://www.footasylum.com/page/login/',headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            time.sleep(2)
            return
        
        if GETlogin.status_code == 200:
            try:
                soup = BeautifulSoup(GETlogin.text,"html.parser")
                preLog = soup.find('input',{'name':'prelog'})["value"]
            except Exception as e:
                time.sleep(2)
                return
        else:
            time.sleep(2)
            return


        # payload = {
        #     'target': '',
        #     'targetar': '',
        #     'pf_id': '',
        #     'sku': '',
        #     'rdPassword': 'LOGIN',
        #     'prelog':self.preLog,
        #     'lookup_Validate': 1,
        #     'email2': self.task["ACCOUNT EMAIL"],
        #     'password': self.task["ACCOUNT PASSWORD"]
        # }
        payload = "target=&targetar=&pf_id=&sku=&rdPassword=LOGIN&prelog={}&lookup_Validate=1&email2={}&password={}".format(
            preLog,
            accountE,
            accountP
        )

        try:
            login = s.post('https://www.footasylum.com/page/login/',data=payload,headers={
                'origin': 'https://www.footasylum.com',
                'referer': 'https://www.footasylum.com/page/login/',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-US,en;q=0.9',
                'content-type': 'application/x-www-form-urlencoded'
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            time.sleep(2)
            return

        if login.status_code != 200 and '?sessionid=' not in login.headers: 
            return


        try:
            getBasket = s.get('https://www.footasylum.com/page/basket/',headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            })
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            time.sleep(2)
            return

        print(accountE)
        if getBasket.status_code == 200:
            try:
                soup = BeautifulSoup(getBasket.text,"html.parser")
                divs = soup.find_all('div',{'class':'nogaps mt f-textlink f-12'})
                print(divs)
                for d in divs:
                    so = BeautifulSoup(d,"html.parser")
                    a = so.find_all('a')[0]
                    print(a)
            except Exception as e:
                print(e)
                pass