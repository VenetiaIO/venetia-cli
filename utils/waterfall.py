from utils.config import sites
import requests
from utils.functions import (scraper, loadProxy, loadProfile, randomString)
import threading
from utils.logger import logger
import time
from bs4 import BeautifulSoup
import json
import re
import random
from utils.px import PX
import sys

class WaterfallAssign:
    @staticmethod
    def assign(tasks,delay):

        data = {}
        for t in tasks:
            data[t['PRODUCT']] = {
                "SITE":t['SITE'],
                "PRODUCT":t['PRODUCT'],
                "PROXIES":'proxies',
                "TASK NAME":[],
                "ROW NUMBER":[],
                "PROFILES":[],
                "SIZES":[],
                "DELAYS":[],
                "PAYMENTS":[],
                "ACCOUNT EMAILS":[],
                "ACCOUNT PASSWORDS":[],
            }
        
        for t in tasks:
            p = t['PRODUCT']
            data[p]['PROFILES'].append(t['PROFILE'])
            data[p]['TASK NAME'].append(t['TASK_NAME'])
            data[p]['ROW NUMBER'].append(t['ROW_NUMBER'])
            data[p]['SIZES'].append(t['SIZE'])
            data[p]['DELAYS'].append(t['DELAY'])
            data[p]['PAYMENTS'].append(t['PAYMENT'])
            data[p]['ACCOUNT EMAILS'].append(t['ACCOUNT EMAIL'])
            data[p]['ACCOUNT PASSWORDS'].append(t['ACCOUNT PASSWORD']) 

        
        # print(data)
        for a in data:
            d = json.dumps(data[a])
            threading.Thread(target=Waterfall, args=(d,delay) ).start()



class Waterfall:
    def __init__(self, data, delay):
        self.data = json.loads(data)
        self.delay = int(delay)
        self.s = scraper()
        self.SITE = self.data['SITE']
        self.taskID = 'Waterfall'
        self.s.proxies = loadProxy(self.data["PROXIES"],self.taskID,self.SITE)

        self.counter = 1


        if self.SITE.lower() == 'allike': self.allike()
        if self.SITE.lower() == 'ambush': self.ambush()
        if self.SITE.lower() == 'awlab': self.awLab()
        if self.SITE.lower() == 'chmielna20': self.chmielna()
        if self.SITE.lower() == 'footasylum': self.footasylum()
        if self.SITE.lower() == 'office': self.office()
        if self.SITE.lower() == 'offspring': self.offspring()
        if self.SITE.lower() == 'schuh': self.schuh()
        if self.SITE.lower() == 'snipes': self.snipes()
        if self.SITE.lower() == 'svd': self.svd()
        if self.SITE.lower() == 'titolo': self.titolo()

    def allike(self):
        while True:
            logger.info(self.SITE,self.taskID,'Monitoring...')
            try:
                retrieve = self.s.get(self.data["PRODUCT"])
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                self.s.proxies = loadProxy(self.data["PROXIES"],self.taskID,self.SITE)
                time.sleep(self.delay)
                continue

            if retrieve.status_code == 200:
                try:
                    soup = BeautifulSoup(retrieve.text,"html.parser")
                    attributeId = soup.find("select", {"class": "required-entry super-attribute-select no-display swatch-select"})["id"].split("attribute")[1]
                    regex = r"{\"attributes\":(.*?)}}\)"
                    matches = re.search(regex, retrieve.text, re.MULTILINE)
                    if matches:
                        productData = json.loads(
                            matches.group()[:-1])["attributes"][attributeId]

                        sizes = []

                        for s in productData['options']:
                            try:
                                sizes.append(s["label"])
                            except:
                                pass
                        
                        if len(sizes) > 0:
                            if 'random' in [ x.lower() for x in self.data['SIZES'] ] or any(size in sizes for size in self.data['SIZES']):

                                for o in range(len(self.data['PROFILES'])):
                                    row = {
                                        "PRODUCT":self.data['PRODUCT'],
                                        "PROFILE":self.data['PROFILES'][o],
                                        "SIZE":self.data['SIZES'][o],
                                        "DELAY":self.data['DELAYS'][o],
                                        "PAYMENT":self.data['PAYMENTS'][o],
                                        "PROXIES":'proxies',
                                        "ACCOUNT EMAIL":self.data['ACCOUNT EMAILS'][o],
                                        "ACCOUNT PASSWORD":self.data['ACCOUNT PASSWORDS'][o],
                                    }
                                    threading.Thread(target=sites.get(self.SITE.upper()),args=(row,self.data['TASK NAME'][o], self.data['ROW NUMBER'][o])).start()
                                break
                        else:
                            time.sleep(self.delay)
                            continue

                    else:
                        time.sleep(self.delay)
                        continue
                            
                except Exception as e:
                    time.sleep(self.delay)
                    continue
            else:
                time.sleep(self.delay)
                continue

    def ambush(self):
        while True:
            logger.info(self.SITE,self.taskID,'Monitoring...')
            try:
                retrieve = self.s.get(self.data["PRODUCT"])
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                self.s.proxies = loadProxy(self.data["PROXIES"],self.taskID,self.SITE)
                time.sleep(self.delay)
                continue

            if retrieve.status_code == 200:
                try:
                    regex = r"__PRELOADED_STATE__ = {(.+)}"
                    matches = re.search(regex, retrieve.text, re.MULTILINE)
                    if matches:
                        prodData = json.loads(matches.group().split('__PRELOADED_STATE__ = ')[1])
                        productId = [*prodData['entities']['products'].keys()][0]
                        availableSizes = prodData['entities']['products'][productId]['sizes']

                        sizes = []

                        for s in availableSizes:
                            try:
                                sizes.append(s["name"])
                            except:
                                pass
                        
                        if len(sizes) > 0:
                            if 'random' in [ x.lower() for x in self.data['SIZES'] ] or any(size in sizes for size in self.data['SIZES']):

                                for o in range(len(self.data['PROFILES'])):
                                    row = {
                                        "PRODUCT":self.data['PRODUCT'],
                                        "PROFILE":self.data['PROFILES'][o],
                                        "SIZE":self.data['SIZES'][o],
                                        "DELAY":self.data['DELAYS'][o],
                                        "PAYMENT":self.data['PAYMENTS'][o],
                                        "PROXIES":'proxies',
                                        "ACCOUNT EMAIL":self.data['ACCOUNT EMAILS'][o],
                                        "ACCOUNT PASSWORD":self.data['ACCOUNT PASSWORDS'][o],
                                    }
                                    threading.Thread(target=sites.get(self.SITE.upper()),args=(row,self.data['TASK NAME'][o], self.data['ROW NUMBER'][o])).start()
                                break
                        else:
                            time.sleep(self.delay)
                            continue
                            
                    else:
                        time.sleep(self.delay)
                        continue

                except Exception as e:
                    time.sleep(self.delay)
                    continue
            else:
                time.sleep(self.delay)
                continue


    def awLab(self):
        while True:
            logger.info(self.SITE,self.taskID,'Monitoring...')
            try:
                retrieve = self.s.get(self.data["PRODUCT"])
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                self.s.proxies = loadProxy(self.data["PROXIES"],self.taskID,self.SITE)
                time.sleep(self.delay)
                continue

            if retrieve.status_code == 200:
                try:
                    soup = BeautifulSoup(retrieve.text, "html.parser")
                    foundSizes = soup.find('ul',{'class':'swatches b-size-selector__list b-size-selector_large b-size-selector_large-sticky'})
                    sizes = []
                    
                    for s in foundSizes:
                        try:
                            s = s.find('a')
                            sizes.append(s["title"])
                        except:
                            pass
                    
                    if len(sizes) > 0:
                        if 'random' in [ x.lower() for x in self.data['SIZES'] ] or any(size in sizes for size in self.data['SIZES']):

                            for o in range(len(self.data['PROFILES'])):
                                row = {
                                    "PRODUCT":self.data['PRODUCT'],
                                    "PROFILE":self.data['PROFILES'][o],
                                    "SIZE":self.data['SIZES'][o],
                                    "DELAY":self.data['DELAYS'][o],
                                    "PAYMENT":self.data['PAYMENTS'][o],
                                    "PROXIES":'proxies',
                                    "ACCOUNT EMAIL":self.data['ACCOUNT EMAILS'][o],
                                    "ACCOUNT PASSWORD":self.data['ACCOUNT PASSWORDS'][o],
                                }
                                threading.Thread(target=sites.get(self.SITE.upper()),args=(row,self.data['TASK NAME'][o], self.data['ROW NUMBER'][o])).start()
                            break
                    else:
                        time.sleep(self.delay)
                        continue
                            
                except Exception as e:
                    time.sleep(self.delay)
                    continue
            else:
                time.sleep(self.delay)
                continue


    def chmielna(self):
        while True:
            logger.info(self.SITE,self.taskID,'Monitoring...')
            print(self.s.proxies)
            try:
                retrieve = self.s.get(self.data["PRODUCT"])
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                self.s.proxies = loadProxy(self.data["PROXIES"],self.taskID,self.SITE)
                time.sleep(self.delay)
                # hCaptcha solving requires proxies to be set on the session.
                continue
            
            if retrieve.status_code == 200:
                try:
                    soup = BeautifulSoup(retrieve.text,"html.parser")
                    foundSizes = soup.find('div',{'class':'selector'})
                    foundSizes = foundSizes.find('ul')
                    foundSizes = foundSizes.find_all('li')

                    sizes = []

                    for s in foundSizes:
                        try:
                            soup = BeautifulSoup(str(s),"html.parser")
                            sizes.append(soup.find('li')["data-sizeus"])
                        except:
                            pass
                    
                    print(sizes)
                    if len(sizes) > 0:
                        if 'random' in [ x.lower() for x in self.data['SIZES'] ] or any(size in sizes for size in self.data['SIZES']):

                            for o in range(len(self.data['PROFILES'])):
                                row = {
                                    "PRODUCT":self.data['PRODUCT'],
                                    "PROFILE":self.data['PROFILES'][o],
                                    "SIZE":self.data['SIZES'][o],
                                    "DELAY":self.data['DELAYS'][o],
                                    "PAYMENT":self.data['PAYMENTS'][o],
                                    "PROXIES":'proxies',
                                    "ACCOUNT EMAIL":self.data['ACCOUNT EMAILS'][o],
                                    "ACCOUNT PASSWORD":self.data['ACCOUNT PASSWORDS'][o],
                                }
                                threading.Thread(target=sites.get(self.SITE.upper()),args=(row,self.data['TASK NAME'][o], self.data['ROW NUMBER'][o])).start()
                            break
                    else:
                        time.sleep(self.delay)
                        continue
                            
                except Exception as e:
                    time.sleep(self.delay)
                    continue
            else:
                time.sleep(self.delay)
                continue

    def footasylum(self):
        while True:
            logger.info(self.SITE,self.taskID,'Monitoring...')
            try:
                retrieve = self.s.get(self.data["PRODUCT"])
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                self.s.proxies = loadProxy(self.data["PROXIES"],self.taskID,self.SITE)
                time.sleep(self.delay)
                continue

            if retrieve.status_code == 200:
                try:
                    soup = BeautifulSoup(retrieve.text,"html.parser")
                    pf_id = soup.find("input",{"name":"pf_id"})["value"]

                    regex = r"variants = {(.+)}"
                    matches = re.search(regex, retrieve.text, re.MULTILINE)
                    if matches:
                        productData = json.loads(matches.group().split('variants = ')[1].replace("'",'"'))

                        pids = []
                        sizes = []
                        for s in productData:
                            pids.append(s)

                        for s in pids:
                            p = productData[s]
                            if p["stock_status"] == "in stock":
                                if p["pf_id"] == pf_id:
                                    size = p["option2"]
                                    sizes.append(size)
        
                    
                        if len(sizes) > 0:
                            if 'random' in [ x.lower() for x in self.data['SIZES'] ] or any(size in sizes for size in self.data['SIZES']):

                                for o in range(len(self.data['PROFILES'])):
                                    row = {
                                        "PRODUCT":self.data['PRODUCT'],
                                        "PROFILE":self.data['PROFILES'][o],
                                        "SIZE":self.data['SIZES'][o],
                                        "DELAY":self.data['DELAYS'][o],
                                        "PAYMENT":self.data['PAYMENTS'][o],
                                        "PROXIES":'proxies',
                                        "ACCOUNT EMAIL":self.data['ACCOUNT EMAILS'][o],
                                        "ACCOUNT PASSWORD":self.data['ACCOUNT PASSWORDS'][o],
                                    }
                                    threading.Thread(target=sites.get(self.SITE.upper()),args=(row,self.data['TASK NAME'][o], self.data['ROW NUMBER'][o])).start()
                                break
                        else:
                            time.sleep(self.delay)
                            continue
                    else:
                        time.sleep(self.delay)
                        continue
                            
                except Exception as e:
                    time.sleep(self.delay)
                    continue
            else:
                time.sleep(self.delay)
                continue

    
    def office(self):
        while True:
            logger.info(self.SITE,self.taskID,'Monitoring...')

            if 'office' not in self.data['PRODUCT']:
                self.data['PRODUCT'] = 'https://www.office.co.uk/view/product/office_catalog/1,21/' + self.data['PRODUCT'] 
            
            

            try:
                retrieve = self.s.get(self.data["PRODUCT"])
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                self.s.proxies = loadProxy(self.data["PROXIES"],self.taskID,self.SITE)
                time.sleep(self.delay)
                continue

            currentVal = self.data['PRODUCT'].split('/office_catalog/')[1].split(',')[0]
            self.data['PRODUCT'] = self.data['PRODUCT'].replace(currentVal + ',', str(random.randint(1,99)) + ',')

            if retrieve.status_code == 503:
                for o in range(len(self.data['PROFILES'])):
                    row = {
                        "PRODUCT":self.data['PRODUCT'],
                        "PROFILE":self.data['PROFILES'][o],
                        "SIZE":self.data['SIZES'][o],
                        "DELAY":self.data['DELAYS'][o],
                        "PAYMENT":self.data['PAYMENTS'][o],
                        "PROXIES":'proxies',
                        "ACCOUNT EMAIL":self.data['ACCOUNT EMAILS'][o],
                        "ACCOUNT PASSWORD":self.data['ACCOUNT PASSWORDS'][o],
                    }
                    threading.Thread(target=sites.get(self.SITE.upper()),args=(row,self.data['TASK NAME'][o], self.data['ROW NUMBER'][o])).start()

            if retrieve.status_code == 200:
                try:
                    soup = BeautifulSoup(retrieve.text,"html.parser")
                    foundSizes = soup.find('ul',{'data-locale':'UK'})

                    sizes = []
                    for s in foundSizes:
                        try:
                            size = s['data-name']
                            sizes.append(size)
                        except:
                            pass

                    if len(sizes) > 0:
                        if 'random' in [ x.lower() for x in self.data['SIZES'] ] or any(size in sizes for size in self.data['SIZES']):

                            for o in range(len(self.data['PROFILES'])):
                                row = {
                                    "PRODUCT":self.data['PRODUCT'],
                                    "PROFILE":self.data['PROFILES'][o],
                                    "SIZE":self.data['SIZES'][o],
                                    "DELAY":self.data['DELAYS'][o],
                                    "PAYMENT":self.data['PAYMENTS'][o],
                                    "PROXIES":'proxies',
                                    "ACCOUNT EMAIL":self.data['ACCOUNT EMAILS'][o],
                                    "ACCOUNT PASSWORD":self.data['ACCOUNT PASSWORDS'][o],
                                }
                                threading.Thread(target=sites.get(self.SITE.upper()),args=(row,self.data['TASK NAME'][o], self.data['ROW NUMBER'][o])).start()
                            break
                    else:
                        time.sleep(self.delay)
                        continue

                            
                except Exception as e:
                    time.sleep(self.delay)
                    continue
            else:
                time.sleep(self.delay)
                continue


    def offspring(self):
        while True:
            logger.info(self.SITE,self.taskID,'Monitoring...')

            if 'offspring' not in self.data['PRODUCT']:
                self.data['PRODUCT'] = 'https://www.offspring.co.uk/view/product/offspring_catalog/1,21/' + self.data['PRODUCT'] 
            
            cookie = '4F04B3A4B98DEDEDA61982F45AD8E5FA~0~YAAQhkISArUy6bt3AQAARC41wAXuaEFsb0EcY8WZSUKjWoI9QX4btVmsBn2qBmZIVCb3lKWP74rOXYgcrexc8ZzQvHkKaKCbpI757FYJE+DmWzcbIDFFJxGcZMa/NH6P6D+zKr9Xt36w/qcc9dPJY7cL/87+wcFO9I+hWzsNEkv/vd7VgKL+uqcPAwp1fxnPcLVKpNAIzsLH7x0qKxB4pZJhBVbhx3OQftm+WVqic/rcfFyxwutEc8CG2qCPFzqTR2tli/JZZhLsHbFWuRgVHj5+/LRZbBBnvi64S0kmTcFQa9RufbtkibD4PbsS1H78WToKpvB9qPZLSl5CC6aycXKXWH2aD2HNHMXIe/xBUtNzECEiUoQRStkAkAiTJzoiL7vJSCrKecZX13wcq79pc+P7jBMEUdn33XlqVDxJ8f6I+res5TDOJsJUqgKzbKt675lNAg==~-1~-1~-1'
            cookie_obj = requests.cookies.create_cookie(domain=f'.offspring.co.uk',name='_abck',value=cookie)
            self.s.cookies.set_cookie(cookie_obj)

            try:
                retrieve = self.s.get(self.data["PRODUCT"])
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                self.s.proxies = loadProxy(self.data["PROXIES"],self.taskID,self.SITE)
                time.sleep(self.delay)
                continue

            currentVal = self.data['PRODUCT'].split('/offspring_catalog/')[1].split(',')[0]
            self.data['PRODUCT'] = self.data['PRODUCT'].replace(currentVal + ',', str(random.randint(1,99)) + ',')

            if retrieve.status_code == 503:
                for o in range(len(self.data['PROFILES'])):
                    row = {
                        "PRODUCT":self.data['PRODUCT'],
                        "PROFILE":self.data['PROFILES'][o],
                        "SIZE":self.data['SIZES'][o],
                        "DELAY":self.data['DELAYS'][o],
                        "PAYMENT":self.data['PAYMENTS'][o],
                        "PROXIES":'proxies',
                        "ACCOUNT EMAIL":self.data['ACCOUNT EMAILS'][o],
                        "ACCOUNT PASSWORD":self.data['ACCOUNT PASSWORDS'][o],
                    }
                    threading.Thread(target=sites.get(self.SITE.upper()),args=(row,self.data['TASK NAME'][o], self.data['ROW NUMBER'][o])).start()

            if retrieve.status_code == 200:
                try:
                    soup = BeautifulSoup(retrieve.text,"html.parser")
                    foundSizes = soup.find('ul',{'data-locale':'UK'})

                    sizes = []
                    for s in foundSizes:
                        try:
                            size = s['data-name']
                            sizes.append(size)
                        except:
                            pass

                    if len(sizes) > 0:
                        if 'random' in [ x.lower() for x in self.data['SIZES'] ] or any(size in sizes for size in self.data['SIZES']):

                            for o in range(len(self.data['PROFILES'])):
                                row = {
                                    "PRODUCT":self.data['PRODUCT'],
                                    "PROFILE":self.data['PROFILES'][o],
                                    "SIZE":self.data['SIZES'][o],
                                    "DELAY":self.data['DELAYS'][o],
                                    "PAYMENT":self.data['PAYMENTS'][o],
                                    "PROXIES":'proxies',
                                    "ACCOUNT EMAIL":self.data['ACCOUNT EMAILS'][o],
                                    "ACCOUNT PASSWORD":self.data['ACCOUNT PASSWORDS'][o],
                                }
                                threading.Thread(target=sites.get(self.SITE.upper()),args=(row,self.data['TASK NAME'][o], self.data['ROW NUMBER'][o])).start()
                            break
                    else:
                        time.sleep(self.delay)
                        continue

                            
                except Exception as e:
                    time.sleep(self.delay)
                    continue
            else:
                time.sleep(self.delay)
                continue


    def schuh(self):
        while True:
            logger.info(self.SITE,self.taskID,'Monitoring...')

            try:
                retrieve = self.s.get(self.data["PRODUCT"])
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                self.s.proxies = loadProxy(self.data["PROXIES"],self.taskID,self.SITE)
                time.sleep(self.delay)
                continue

            if retrieve.status_code == 200:
                try:
                    soup = BeautifulSoup(retrieve.text,"html.parser")
                    sizeSelect = soup.find('select',{'id':'sizes'})

                    sizes = []
                    for s in sizeSelect:
                        try:
                            size = s["data-dispsize"]
                            try:
                                size = size.split(' ')[1]
                            except:
                                pass
                            sizes.append(size)
                        except:
                            pass

                    if len(sizes) > 0:
                        if 'random' in [ x.lower() for x in self.data['SIZES'] ] or any(size in sizes for size in self.data['SIZES']):

                            for o in range(len(self.data['PROFILES'])):
                                row = {
                                    "PRODUCT":self.data['PRODUCT'],
                                    "PROFILE":self.data['PROFILES'][o],
                                    "SIZE":self.data['SIZES'][o],
                                    "DELAY":self.data['DELAYS'][o],
                                    "PAYMENT":self.data['PAYMENTS'][o],
                                    "PROXIES":'proxies',
                                    "ACCOUNT EMAIL":self.data['ACCOUNT EMAILS'][o],
                                    "ACCOUNT PASSWORD":self.data['ACCOUNT PASSWORDS'][o],
                                }
                                threading.Thread(target=sites.get(self.SITE.upper()),args=(row,self.data['TASK NAME'][o], self.data['ROW NUMBER'][o])).start()
                            break
                    else:
                        time.sleep(self.delay)
                        continue

                            
                except Exception as e:
                    time.sleep(self.delay)
                    continue
            else:
                time.sleep(self.delay)
                continue


    def snipes(self):
        countryCode = loadProfile(self.data['PROFILES'][0])["countryCode"]
        if 'https' in self.data['PRODUCT']:
            try:
                self.snipesRegion = self.data["PRODUCT"].split('snipes.')[1].split('/')[0]
                self.pid = '00' + self.data['PRODUCT'].split('-00')[1].split('.html')[0]
            except:
                logger.error(SITE,self.taskID,'Failed to parse PID. Please check it is a valid SNIPES url.')
                time.sleep(5)
                sys.exit()
        else:
            if countryCode.upper() == "DE":
                self.snipesRegion = 'com'
            if countryCode.upper() == "AT":
                self.snipesRegion = 'at'
            if countryCode.upper() == "NL":
                self.snipesRegion = 'nl'
            if countryCode.upper() == "FR":
                self.snipesRegion = 'fr'
            if countryCode.upper() == "CH":
                self.snipesRegion = 'ch'
            if countryCode.upper() == "IT":
                self.snipesRegion = 'it'
            if countryCode.upper() == "ES":
                self.snipesRegion = 'es'
            if countryCode.upper() == "BE":
                self.snipesRegion = 'be'
                
            self.pid = self.data['PRODUCT']
      
        cookies = PX.snipes(self.s, f'https://www.snipes.{self.snipesRegion}', self.taskID)
        while cookies["px3"] == "error":
            cookies = PX.snipes(self.s, f'https://www.snipes.{self.snipesRegion}', self.taskID)

        self.cs = cookies['cs']
        self.sid = cookies['sid']
        cookie_obj = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_px3',value=cookies['px3'])
        cookie_obj2 = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_pxvid',value=cookies['vid'])
        self.s.cookies.set_cookie(cookie_obj)
        self.s.cookies.set_cookie(cookie_obj2)

        queryUrl = 'https://www.snipes.{}/p/{}.html?dwvar_{}_color=a&format=ajax'.format(self.snipesRegion,self.pid,self.pid)

        # https://www.snipes.com/p/00013801883852.html?dwvar_00013801883852_color=a&format=ajax

        self.s.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'referer': f'https://www.snipes.{self.snipesRegion}/',
        }

        while True:
            logger.info(self.SITE,self.taskID,'Monitoring...')
            try:
                retrieve = self.s.get(queryUrl)
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                self.s.proxies = loadProxy(self.data["PROXIES"],self.taskID,self.SITE)
                time.sleep(self.delay)
                continue

            if retrieve.status_code == 200:
                try:
                    data = retrieve.json()
                    sizes = []

                    # print(data["product"]["variationAttributes"][0]["values"])
                    for s in data["product"]["variationAttributes"][0]["values"]:
                        try:
                            sizes.append(s["value"])
                        except:
                            pass


                    if len(sizes) > 0:
                        if 'random' in [ x.lower() for x in self.data['SIZES'] ] or any(size in sizes for size in self.data['SIZES']):

                            for o in range(len(self.data['PROFILES'])):
                                row = {
                                    "PRODUCT":self.data['PRODUCT'],
                                    "PROFILE":self.data['PROFILES'][o],
                                    "SIZE":self.data['SIZES'][o],
                                    "DELAY":self.data['DELAYS'][o],
                                    "PAYMENT":self.data['PAYMENTS'][o],
                                    "PROXIES":'proxies',
                                    "ACCOUNT EMAIL":self.data['ACCOUNT EMAILS'][o],
                                    "ACCOUNT PASSWORD":self.data['ACCOUNT PASSWORDS'][o],
                                }
                                threading.Thread(target=sites.get(self.SITE.upper()),args=(row,self.data['TASK NAME'][o], self.data['ROW NUMBER'][o])).start()
                            break
                    else:
                        time.sleep(self.delay)
                        continue

                            
                except Exception as e:
                    time.sleep(self.delay)
                    continue

            if retrieve.status_code == 412:
                cookies = PX.snipes(self.s, f'https://www.snipes.{self.snipesRegion}', self.taskID)
                while cookies["px3"] == "error":
                    cookies = PX.snipes(self.s, f'https://www.snipes.{self.snipesRegion}', self.taskID)

                self.cs = cookies['cs']
                self.sid = cookies['sid']
                cookie_obj = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_px3',value=cookies['px3'])
                cookie_obj2 = requests.cookies.create_cookie(domain=f'www.snipes.{self.snipesRegion}',name='_pxvid',value=cookies['vid'])
                self.s.cookies.set_cookie(cookie_obj)
                self.s.cookies.set_cookie(cookie_obj2)

            else:
                time.sleep(self.delay)
                continue



    def svd(self):
        while True:
            logger.info(self.SITE,self.taskID,'Monitoring...')
            url = '{}{}'.format(self.data["PRODUCT"],f"#%253F_={randomString(20)}")
            try:
                retrieve = self.s.get(url,headers={
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                })
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                self.s.proxies = loadProxy(self.data["PROXIES"],self.taskID,self.SITE)
                time.sleep(self.delay)
                continue

            if retrieve.status_code == 200:
                try:
                    regexSwatch = r'"jsonSwatchConfig":(.+)"}}'
                    regexAttributes = r'{"attributes":(.+)}}'
                    regexOption = r'"optionConfig":(.+)}}'

                    matches = re.search(regexSwatch, retrieve.text, re.MULTILINE)
                    matches2 = re.search(
                        regexAttributes, retrieve.text, re.MULTILINE)
                    matches3 = re.search(regexOption, retrieve.text, re.MULTILINE)
                    if matches and matches2 and matches3:
                        jsonSwatch = json.loads('{' + matches.group() + '}')["jsonSwatchConfig"]

                        dictt = list(jsonSwatch.keys())
                        SuperAttribute = dictt[0]
                        jsonAttributes = json.loads(matches2.group())["attributes"]

                        sizes = []

                        for s in jsonAttributes[SuperAttribute]["options"]:
                            try:
                                sizes.append(s["label"])
                            except:
                                pass
                        
                        if len(sizes) > 0:
                            if 'random' in [ x.lower() for x in self.data['SIZES'] ] or any(size in sizes for size in self.data['SIZES']):

                                for o in range(len(self.data['PROFILES'])):
                                    row = {
                                        "PRODUCT":self.data['PRODUCT'],
                                        "PROFILE":self.data['PROFILES'][o],
                                        "SIZE":self.data['SIZES'][o],
                                        "DELAY":self.data['DELAYS'][o],
                                        "PAYMENT":self.data['PAYMENTS'][o],
                                        "PROXIES":'proxies',
                                        "ACCOUNT EMAIL":self.data['ACCOUNT EMAILS'][o],
                                        "ACCOUNT PASSWORD":self.data['ACCOUNT PASSWORDS'][o],
                                    }
                                    threading.Thread(target=sites.get(self.SITE.upper()),args=(row,self.data['TASK NAME'][o], self.data['ROW NUMBER'][o])).start()
                                break
                        else:
                            time.sleep(self.delay)
                            continue

                    else:
                        time.sleep(self.delay)
                        continue
                            
                except Exception as e:
                    time.sleep(self.delay)
                    continue
            else:
                time.sleep(self.delay)
                continue

    
    def titolo(self):
        while True:
            logger.info(self.SITE,self.taskID,'Monitoring...')
            try:
                retrieve = self.s.get(self.data["PRODUCT"])
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                
                self.s.proxies = loadProxy(self.data["PROXIES"],self.taskID,self.SITE)
                time.sleep(self.delay)
                continue
            

            if retrieve.status_code == 200:
                try:
                    soup = BeautifulSoup(retrieve.text,"html.parser")
                    sizeSelect = soup.find("select",{"id":"attributesize-size_eu"})
                    if sizeSelect == None or len(sizeSelect) == 0:
                        time.sleep(self.delay)
                        continue
                    sizes = []

                    for s in sizeSelect:
                        try:
                            sizes.append(s.text)
                        except:
                            pass
                    
                    if len(sizes) > 0:
                        if 'random' in [ x.lower() for x in self.data['SIZES'] ] or any(size in sizes for size in self.data['SIZES']):

                            for o in range(len(self.data['PROFILES'])):
                                row = {
                                    "PRODUCT":self.data['PRODUCT'],
                                    "PROFILE":self.data['PROFILES'][o],
                                    "SIZE":self.data['SIZES'][o],
                                    "DELAY":self.data['DELAYS'][o],
                                    "PAYMENT":self.data['PAYMENTS'][o],
                                    "PROXIES":'proxies',
                                    "ACCOUNT EMAIL":self.data['ACCOUNT EMAILS'][o],
                                    "ACCOUNT PASSWORD":self.data['ACCOUNT PASSWORDS'][o],
                                }
                                threading.Thread(target=sites.get(self.SITE.upper()),args=(row,self.data['TASK NAME'][o], self.data['ROW NUMBER'][o])).start()
                            break
                    else:
                        time.sleep(self.delay)


                            
                except Exception as e:
                    time.sleep(self.delay)
                    continue
            else:
                time.sleep(self.delay)
                continue


    

    
