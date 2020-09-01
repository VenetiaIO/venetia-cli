from utils.logger import logger
import requests
from bs4 import BeautifulSoup
import datetime
import threading
from colorama import init
from termcolor import colored
import random
import sys
import time
import re
import json
import uuid
import os
import base64
from discord_webhook import DiscordWebhook, DiscordEmbed
import cloudscraper
import string
import urllib.parse
init()
SITE = 'END'



def createId(length):
    return ''.join(random.choice(string.digits) for i in range(length))


def loadProxy(proxies, taskID):
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
        logger.info(SITE,taskID,'Proxy Loaded')
        return proxies

def loadProfile(profile):
    with open(f'./data/profiles/profile_{profile}.json') as profile:
        profile = json.loads(profile.read())
        return profile


def loadSettings():
    with open(f'./data/config.json') as settings:
        settings = json.loads(settings.read())
        return settings


class END:
    def __init__(self, task,taskName):
        self.task = task
        self.session = requests.session()
        self.taskID = taskName
        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID)


        self.createSession()

    def createSession(self):
        logger.warning(SITE,self.taskID,'Generating Session...')
        #try:
        headBody = self.session.get('https://www.endclothing.com/headandbody.html',headers={
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        })
        src = headBody.text.split('src="')[1].split('"')[0]
        getScript = self.session.get(f'https://www.endclothing.com{src}',headers={
            'authority': 'www.endclothing.com',
            'path': src,
            'scheme': 'https',
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'referer': 'https://www.endclothing.com/headandbody.html',
            'sec-fetch-dest': 'script',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
        })
        fingerprintWrapper = json.loads(getScript.text.split('FingerprintWrapper(')[1].split(')')[0].replace('path','"path"').replace('ajax_header','"ajax_header"').replace('interval','"interval"'))
        pidUrl = fingerprintWrapper["path"]
        ajaxHeader = fingerprintWrapper["ajax_header"]

        api = requests.get('https://venetia.io/api/end/proof',headers={"apiKey":"34ba3826-21a9-4a69-b25a-6f0826da77fe"})
        payload = {
            "proof":api.json()["proof"],
            "fp2":{
                "userAgent":"Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/83.0.4103.116Safari/537.36",
                "language":"en-US",
                "screen":{
                    "width":2560,
                    "height":1440,
                    "availHeight":1400,
                    "availWidth":2560,
                    "pixelDepth":24,
                    "innerWidth":1279,
                    "innerHeight":1288,
                    "outerWidth":1294,
                    "outerHeight":1407,
                    "devicePixelRatio":1.5
                },
                "timezone":1,
                "indexedDb":True,
                "addBehavior":False,
                "openDatabase":True,
                "cpuClass":"unknown",
                "platform":"Win32",
                "doNotTrack":"unknown",
                "plugins":"ChromePDFPlugin::PortableDocumentFormat::application/x-google-chrome-pdf~pdf;ChromePDFViewer::::application/pdf~pdf;NativeClient::::application/x-nacl~,application/x-pnacl~",
                "canvas":{
                    "winding":"yes",
                    "towebp":True,
                    "blending":True,
                    "img":"c5f243ad6712baefaa5cced187489d6f8f30f04e"
                },
                "webGL":{
                    "img":"283e1be0e5ec3230a8dc0bb69e17722f16204065",
                    "extensions":"ANGLE_instanced_arrays;EXT_blend_minmax;EXT_color_buffer_half_float;EXT_disjoint_timer_query;EXT_float_blend;EXT_frag_depth;EXT_shader_texture_lod;EXT_texture_compression_bptc;EXT_texture_compression_rgtc;EXT_texture_filter_anisotropic;WEBKIT_EXT_texture_filter_anisotropic;EXT_sRGB;KHR_parallel_shader_compile;OES_element_index_uint;OES_fbo_render_mipmap;OES_standard_derivatives;OES_texture_float;OES_texture_float_linear;OES_texture_half_float;OES_texture_half_float_linear;OES_vertex_array_object;WEBGL_color_buffer_float;WEBGL_compressed_texture_s3tc;WEBKIT_WEBGL_compressed_texture_s3tc;WEBGL_compressed_texture_s3tc_srgb;WEBGL_debug_renderer_info;WEBGL_debug_shaders;WEBGL_depth_texture;WEBKIT_WEBGL_depth_texture;WEBGL_draw_buffers;WEBGL_lose_context;WEBKIT_WEBGL_lose_context",
                    "aliasedlinewidthrange":"[1,1]",
                    "aliasedpointsizerange":"[1,1024]",
                    "alphabits":8,
                    "antialiasing":"yes",
                    "bluebits":8,
                    "depthbits":24,
                    "greenbits":8,
                    "maxanisotropy":16,
                    "maxcombinedtextureimageunits":32,
                    "maxcubemaptexturesize":16384,
                    "maxfragmentuniformvectors":1024,
                    "maxrenderbuffersize":16384,
                    "maxtextureimageunits":16,
                    "maxtexturesize":16384,
                    "maxvaryingvectors":30,
                    "maxvertexattribs":16,
                    "maxvertextextureimageunits":16,
                    "maxvertexuniformvectors":4095,
                    "maxviewportdims":"[32767,32767]",
                    "redbits":8,
                    "renderer":"WebKitWebGL",
                    "shadinglanguageversion":"WebGLGLSLES1.0(OpenGLESGLSLES1.0Chromium)",
                    "stencilbits":0,
                    "vendor":"WebKit",
                    "version":"WebGL1.0(OpenGLES2.0Chromium)",
                    "vertexshaderhighfloatprecision":23,
                    "vertexshaderhighfloatprecisionrangeMin":127,
                    "vertexshaderhighfloatprecisionrangeMax":127,
                    "vertexshadermediumfloatprecision":23,
                    "vertexshadermediumfloatprecisionrangeMin":127,
                    "vertexshadermediumfloatprecisionrangeMax":127,
                    "vertexshaderlowfloatprecision":23,
                    "vertexshaderlowfloatprecisionrangeMin":127,
                    "vertexshaderlowfloatprecisionrangeMax":127,
                    "fragmentshaderhighfloatprecision":23,
                    "fragmentshaderhighfloatprecisionrangeMin":127,
                    "fragmentshaderhighfloatprecisionrangeMax":127,
                    "fragmentshadermediumfloatprecision":23,
                    "fragmentshadermediumfloatprecisionrangeMin":127,
                    "fragmentshadermediumfloatprecisionrangeMax":127,
                    "fragmentshaderlowfloatprecision":23,
                    "fragmentshaderlowfloatprecisionrangeMin":127,
                    "fragmentshaderlowfloatprecisionrangeMax":127,
                    "vertexshaderhighintprecision":0,
                    "vertexshaderhighintprecisionrangeMin":31,
                    "vertexshaderhighintprecisionrangeMax":30,
                    "vertexshadermediumintprecision":0,
                    "vertexshadermediumintprecisionrangeMin":31,
                    "vertexshadermediumintprecisionrangeMax":30,
                    "vertexshaderlowintprecision":0,
                    "vertexshaderlowintprecisionrangeMin":31,
                    "vertexshaderlowintprecisionrangeMax":30,
                    "fragmentshaderhighintprecision":0,
                    "fragmentshaderhighintprecisionrangeMin":31,
                    "fragmentshaderhighintprecisionrangeMax":30,
                    "fragmentshadermediumintprecision":0,
                    "fragmentshadermediumintprecisionrangeMin":31,
                    "fragmentshadermediumintprecisionrangeMax":30,
                    "fragmentshaderlowintprecision":0,
                    "fragmentshaderlowintprecisionrangeMin":31,
                    "fragmentshaderlowintprecisionrangeMax":30,
                    "unmaskedvendor":"GoogleInc.",
                    "unmaskedrenderer":"ANGLE(NVIDIAGeForceRTX2060SUPERDirect3D11vs_5_0ps_5_0)"
                },
                "touch":{
                    "maxTouchPoints":0,
                    "touchEvent":False,
                    "touchStart":False
                },
                "video":{
                    "ogg":"probably",
                    "h264":"probably",
                    "webm":"probably"
                },
                "audio":{
                    "ogg":"probably",
                    "mp3":"probably",
                    "wav":"probably",
                    "m4a":"maybe"
                },
                "vendor":"GoogleInc.",
                "product":"Gecko",
                "productSub":"20030107",
                "browser":{
                    "ie":False,
                    "chrome":True,
                    "webdriver":False
                },
                "window":{
                    "historyLength":1,
                    "hardwareConcurrency":4,
                    "iframe":False,
                    "battery":True
                },
                "location":{
                    "protocol":"https:"
                },
                "fonts":"Calibri;Century;Haettenschweiler;Marlett;Pristina",
                "devices":{
                    "count":2,
                    "data":{
                        "0":{
                        "deviceId":"",
                        "groupId":"c294f05ebcf2831aed2b258073a384555a8f6b730eb65318261ef4d3ebf8178a",
                        "kind":"audioinput",
                        "label":""
                        },
                        "1":{
                        "deviceId":"",
                        "groupId":"353b8551fc91cd3f9d916976ec567d0c1472b419fb75b01da7d1e61e0ef33e33",
                        "kind":"audiooutput",
                        "label":""
                        }
                    }
                }
            },
            "cookies":1,
            "setTimeout":0,
            "setInterval":0,
            "appName":"Netscape",
            "platform":"Win32",
            "syslang":"en-US",
            "userlang":"en-US",
            "cpu":"",
            "productSub":"20030107",
            "plugins":{
                "0":"ChromePDFPlugin",
                "1":"ChromePDFViewer",
                "2":"NativeClient"
            },
            "mimeTypes":{
                "0":"application/pdf",
                "1":"PortableDocumentFormatapplication/x-google-chrome-pdf",
                "2":"NativeClientExecutableapplication/x-nacl",
                "3":"PortableNativeClientExecutableapplication/x-pnacl"
            },
            "screen":{
                "width":2560,
                "height":1440,
                "colorDepth":24
            },
            "fonts":{
                "0":"Calibri",
                "1":"Cambria",
                "2":"Constantia",
                "3":"LucidaBright",
                "4":"Georgia",
                "5":"SegoeUI",
                "6":"Candara",
                "7":"TrebuchetMS",
                "8":"Verdana",
                "9":"Consolas",
                "10":"LucidaConsole",
                "11":"LucidaSansTypewriter",
                "12":"CourierNew",
                "13":"Courier"
            }
        }
        encoded = urllib.parse.quote(f'p={payload}')
        js = pidUrl.split('?')[0]
        params = pidUrl.split('?')[1]
        pid = params.split('=')[1]
        r = self.session.post(f'https://www.endclothing.com{js}',params={"PID":pid},data=encoded,headers={
            'authority': 'www.endclothing.com',
            'path': pidUrl,
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'text/plain;charset=UTF-8',
            'origin': 'https://www.endclothing.com',
            'referer': 'https://www.endclothing.com/headandbody.html',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            'x-distil-ajax': ajaxHeader
        })
        #except:
        #    logger.sessionGenResult('',False,SITE,self.taskID)
        #    self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID)
        #    time.sleep(int(self.task["DELAY"]))
        #    self.createSession()

        if r.status_code == 200:
            logger.success(SITE,self.taskID,'Successfully generated session')
            print(r)
            print(r.headers)
            print(self.session.cookies)
        else:
            logger.error(SITE,self.taskID,'Failed to generate session. Retrying...')
            time.sleep(int(self.task["DELAY"]))
            self.createSession()

        r = self.session.get('https://www.endclothing.com',headers={
            'authority': 'www.endclothing.com',
            'path': '/gb/',
            'scheme': 'https',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
        })
        print(self.session.cookies)
        #self.collect()
    



    def collect(self):
        try:
            retrieve = self.session.get(self.task["PRODUCT"],headers={
                'path': '/gb/',
                'authority': 'www.endclothing.com',
                'scheme': 'https',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-US,en;q=0.9',
                'cache-control': 'max-age=0',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
            })
        except:
            logger.error(SITE,self.taskID,'Connection Error. Retrying...')
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID)
            time.sleep(int(self.task["DELAY"]))
            self.collect()

        if retrieve.status_code == 200:
            logger.success(SITE,self.taskID,'Got product page')
            regex = r'"initialProps":.(.+"url_key")'
            matches = re.search(regex, retrieve.text, re.MULTILINE)
            if matches:
                match1 = '{' + matches.group()[:-10]
                productData = json.loads(match1 + '}}}}')["initialProps"]["pageProps"]["product"]
                self.productId = productData["id"]
                self.variantSKU = productData["sku"]
                self.productTitle = productData["name"]
                self.productImage = productData["media_gallery_entries"][0]["file"]
                allSizes = []
                sizes = []

                self.emptyPrice = productData["price_gbp"]
                self.productPrice = '£{}'.format(productData["price_gbp"])
                self.attributeId = productData["sizes"]["attribute_id"]
                for s in productData["sizes"]["values"]:
                    size = s["label"].split('UK ')[1]
                    index = s["index"]
                    fullLabel = s["label"]
                    stock = s["in_stock"]
                    sizes.append(size)
                    allSizes.append('{}:{}:{}:{}'.format(size,index,fullLabel,stock))

                
                if self.task["SIZE"].lower() != "random":
                        if self.task["SIZE"] not in sizes:
                            logger.error(SITE,self.taskID,'Size Not Found')
                            time.sleep(int(self.task["DELAY"]))
                            self.collect()
                        else:
                            for size in allSizes:
                                if size.split(':')[0] == self.task["SIZE"]:
                                    self.size = size.split(':')[0]
                                    self.indexId = size.split(':')[1]
                                    self.fullSizeLabel = size.split(":")[2]
                                    self.stockLevel = size.split(':')[3]
                                    logger.success(SITE,self.taskID,f'Found Size => {self.fullSizeLabel}')
                                    self.addToCart()
        
                    
                elif self.task["SIZE"].lower() == "random":
                    selected = random.choice(allSizes)
                    self.size = selected.split(':')[0]
                    self.indexId = selected.split(':')[1]
                    self.fullSizeLabel = selected.split(":")[2]
                    self.stockLevel = selected.split(':')[3]
                    logger.success(SITE,self.taskID,f'Found Size => {self.fullSizeLabel}')
                    self.addToCart()
            else:
                logger.error(SITE,self.taskID,'Failed to get product page. Retrying...')
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID)
                time.sleep(int(self.task["DELAY"]))
                self.collect()

        elif retrieve.status_code != 200:
            logger.error(SITE,self.taskID,'Failed to get product page. Retrying...')
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID)
            time.sleep(int(self.task["DELAY"]))
            self.collect()

    def addToCart(self):
        try:
            guestCart = self.session.post('https://api2.endclothing.com/gb/rest/V1/guest-carts',headers={
                'authority': 'api2.endclothing.com',
                'path': '/gb/rest/V1/guest-carts',
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'en-US,en;q=0.9',
                'origin': 'https://www.endclothing.com',
                'referer': self.task["PRODUCT"],
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
            })
        except:
            logger.error(SITE,self.taskID,'Connection Error. Retrying...')
            self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID)
            time.sleep(int(self.task["DELAY"]))
            self.addToCart()
        
        if guestCart.status_code == 200:
            self.quoteMask = guestCart.text.replace('"','')
            try:
                quoteMaskAssign = self.session.post('https://www.endclothing.com/gb/endclothing_frontend/quote/assign',params={"quote_mask":self.quoteMask},headers={
                    'authority': 'api2.endclothing.com',
                    'path': '/gb/rest/V1/guest-carts/assign?quote_mask={}'.format(self.quoteMask),
                    'accept': 'application/json, text/plain, */*',
                    'accept-language': 'en-US,en;q=0.9',
                    'origin': 'https://www.endclothing.com',
                    'referer': self.task["PRODUCT"],
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-site',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
                })
            except:
                logger.error(SITE,self.taskID,'Connection Error. Retrying...')
                self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID)
                time.sleep(int(self.task["DELAY"]))
                self.addToCart()

            print(quoteMaskAssign.text)

            if quoteMaskAssign.status_code == 200:
                payload = {"cartItem":{"product_option":{"extension_attributes":{"configurable_item_options":[{"option_id":self.attributeId,"option_value":self.indexId}]}},"qty":1,"quote_id":self.quoteMask,"sku":self.variantSKU}}
                try:
                    postCart = self.session.post('https://api2.endclothing.com/gb/rest/V1/guest-carts/{}/items/'.format(self.quoteMask),json=payload,headers={
                        'authority': 'api2.endclothing.com',
                        'path': '/gb/rest/V1/guest-carts/{}'.format(self.quoteMask),
                        'accept': 'application/json, text/plain, */*',
                        'accept-language': 'en-US,en;q=0.9',
                        'origin': 'https://www.endclothing.com',
                        'referer': self.task["PRODUCT"],
                        'sec-fetch-dest': 'empty',
                        'sec-fetch-mode': 'cors',
                        'sec-fetch-site': 'same-site',
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
                    })
                except:
                    logger.error(SITE,self.taskID,'Connection Error. Retrying...')
                    self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID)
                    time.sleep(int(self.task["DELAY"]))
                    self.addToCart()

                if postCart.status_code == 200 and int(postCart.json()["qty"]) > 0:
                    self.variantSKUs = postCart.json()["sku"]
                    logger.success(SITE,self.taskID,'Successfully carted')

                    try:
                        guestCart = self.session.get('https://api2.endclothing.com/gb/rest/V1/end/guest-carts/{}/GB'.format(self.quoteMask),headers={
                            'authority': 'api2.endclothing.com',
                            'path': '/gb/rest/V1/end/guest-carts/{}/GB'.format(self.quoteMask),
                            'accept': 'application/json, text/plain, */*',
                            'accept-language': 'en-US,en;q=0.9',
                            'origin': 'https://www.endclothing.com',
                            'referer': self.task["PRODUCT"],
                            'sec-fetch-dest': 'empty',
                            'sec-fetch-mode': 'cors',
                            'sec-fetch-site': 'same-site',
                            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
                        })
                    except:
                        logger.error(SITE,self.taskID,'Connection Error. Retrying...')
                        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID)
                        time.sleep(int(self.task["DELAY"]))
                        self.addToCart()


                    try:
                        payload = {"event_name":"cart_update","data":{"action":"add","application":"web","cart_total":self.emptyPrice,"cart_total_GBP":self.emptyPrice,"currency":guestCart.json()["cart_totals"]["quote_currency_code"],"language":"en","product_id":self.productId,"product_ids":[self.productId],"quantity":1,"region":"GB","store_id":guestCart.json()["extension_attributes"]["shipping_assignments"][0]["shipping"]["address"]["country_id"],"shipping_country":"United Kingdom","url":self.task["PRODUCT"],"variant_sku":self.variantSKU,"variant_skus":[self.variantSKUs]}}
                        postCart = self.session.post('https://api.endclothing.com/tracker/rest/v1/gb/event',json=payload,headers={
                            'authority': 'api2.endclothing.com',
                            'path': '/gb/rest/V1/guest-carts/{}'.format(self.quoteMask),
                            'accept': 'application/json, text/plain, */*',
                            'accept-language': 'en-US,en;q=0.9',
                            'origin': 'https://www.endclothing.com',
                            'referer': self.task["PRODUCT"],
                            'sec-fetch-dest': 'empty',
                            'sec-fetch-mode': 'cors',
                            'sec-fetch-site': 'same-site',
                            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
                        })
                    except:
                        logger.error(SITE,self.taskID,'Connection Error. Retrying...')
                        self.session.proxies = loadProxy(self.task["PROXIES"],self.taskID)
                        time.sleep(int(self.task["DELAY"]))
                        self.addToCart()

                    if postCart.status_code == 204:
                        pass

                else:
                    logger.error(SITE,self.taskID,'Failed to cart. Retrying...')

                




