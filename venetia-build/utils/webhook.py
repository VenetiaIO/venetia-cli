from discord_webhook import DiscordWebhook, DiscordEmbed
import utils.config as CONFIG
from utils.log import log
import pymongo
from utils.logger import logger
from utils.functions import (getUser, updateCheckouts)
publicWebhook = 'https://discordapp.com/api/webhooks/734209129035333683/3pZfyBnoSIxndJQjsrEQvDGSlKsEoRF8NzwEKggq4jaUHj-A61cGXNW6MXdJMyYX_qbH'
mongoConnect = "mongodb+srv://charlieaio:87g[VyhEnY$F?uf8@cluster-main.sqapr.mongodb.net/mydb?retryWrites=true&w=majority"


class discord:
    @staticmethod
    #def success(webhook, SITE, url, image, productTitle, productSize, productPrice, profile, paymentMethod):
    def success(**kwargs):
        webhook = kwargs.get('webhook')
        SITE = kwargs.get('site')
        url = kwargs.get('url')
        image = kwargs.get('image')
        productTitle = kwargs.get('title')
        productSize = kwargs.get('size')
        productPrice = kwargs.get('price')
        paymentMethod = kwargs.get('paymentMethod')
        profile = kwargs.get('profile')
        accountEmail = kwargs.get('account')
        tracking = kwargs.get('tracking')
        order = kwargs.get('order')
        product = kwargs.get('product')
        speed = kwargs.get('speed')
        proxy = kwargs.get('proxy')
        region = kwargs.get('region')
        if proxy:
            try:
                proxy = proxy["https"]
            except:
                proxy = proxy["http"]


        logger.secondary(SITE,'Task Link',url)

        user = getUser()
        try:                
            webhook = DiscordWebhook(webhook)
            embed = DiscordEmbed(title=':rocket: Successful Checkout :rocket:', description='', color=0x2feb61)
            embed.set_footer(text='VenetiaIO CLI | {}'.format(CONFIG.VERSION()))
            embed.set_timestamp()    
            if image:
                try:
                    embed.set_thumbnail(url=image)
                except Exception as e:
                    log.info(e)

            if SITE and region: embed.add_embed_field(name='Site', value='{}  :flag_{}:'.format(SITE.title(), region.lower()) ,inline=False)
            else: embed.add_embed_field(name='Site', value=SITE.title(),inline=False)

            if productTitle: embed.add_embed_field(name='Product', value=f'[{productTitle}]({product})',inline=False)
            if productSize: embed.add_embed_field(name='Size', value=str(productSize),inline=True)
            if productPrice: embed.add_embed_field(name='Product Price', value=str(productPrice),inline=True)
            if paymentMethod: embed.add_embed_field(name='Payment Method', value=paymentMethod,inline=True)
            if speed: embed.add_embed_field(name='Checkout Speed', value=str(speed),inline=True)
            if profile: embed.add_embed_field(name='Task Profile', value=f'||{profile}||',inline=True)
            if accountEmail and accountEmail != '': embed.add_embed_field(name='Account Email', value=f'||{accountEmail}||',inline=False)
            if tracking and order: embed.add_embed_field(name='Tracking', value=f'||[{order}]({tracking})||',inline=False)
            if url: embed.add_embed_field(name='Checkout Link', value=f'[Checkout Here]({url})',inline=False)
            if proxy: embed.add_embed_field(name='Proxy Used', value=f'||`{str(proxy)}`||',inline=False)
            webhook.add_embed(embed)
            webhook.execute()

            myclient = pymongo.MongoClient(mongoConnect)
            mydb = myclient["mydb"]
            collection = mydb["collection"]

            user = getUser()["discordName"]
            data = { "image":image, "site":SITE, "url":product, "product":productTitle, "size":productSize, "price":productPrice, "user":user }
            updateCheckouts(productTitle,SITE,productSize,productPrice,image,product,url)
            x = collection.insert_one(data)
            
        except Exception as e:
            print(e)
            log.info(e)
            pass


        try:
            webhookPublic = DiscordWebhook(publicWebhook)
            embed2 = DiscordEmbed(title=':rocket: User Checkout :rocket:', description='', color=0x2feb61)
            embed.set_footer(text='VenetiaIO CLI | {}'.format(CONFIG.VERSION()))
            embed2.set_timestamp()
    
            if image:
                try:
                    embed2.set_thumbnail(url=image)
                except Exception as e:
                    log.info(e)

            if SITE and region: embed2.add_embed_field(name='Site', value='{}  :flag_{}:'.format(SITE.title(),region.lower()) ,inline=False)
            else: embed2.add_embed_field(name='Site', value=SITE.title(),inline=False)

            if productTitle: embed2.add_embed_field(name='Product', value=f'[{productTitle}]({product})',inline=False)
            if productSize: embed2.add_embed_field(name='Size', value=str(productSize),inline=False)
            if productPrice: embed2.add_embed_field(name='Product Price', value=str(productPrice),inline=False)
    
            QT_URL = 'http://127.0.0.1:6969/venetia/quicktask?website={}&url={}'.format(SITE.lower().replace(' ',''),product)
            embed2.add_embed_field(name='Quick Task',value=f'[Start QT]({QT_URL})')
    
            webhookPublic.add_embed(embed2)
            webhookPublic.execute()
        except:
            pass
    @staticmethod
    def failed(**kwargs):
        webhook = kwargs.get('webhook')
        SITE = kwargs.get('site')
        url = kwargs.get('url')
        image = kwargs.get('image')
        productTitle = kwargs.get('title')
        productSize = kwargs.get('size')
        productPrice = kwargs.get('price')
        paymentMethod = kwargs.get('paymentMethod')
        profile = kwargs.get('profile')
        accountEmail = kwargs.get('account')
        tracking = kwargs.get('tracking')
        order = kwargs.get('order')
        product = kwargs.get('product')
        speed = kwargs.get('speed')
        proxy = kwargs.get('proxy')
        region = kwargs.get('region')
        if proxy:
            try:
                proxy = proxy["https"]
            except:
                proxy = proxy["http"]

        try:
            webhook = DiscordWebhook(webhook)
            embed = DiscordEmbed(title='⛔ Checkout Failed ⛔', description='', color=0xeb3c2f)
            embed.set_footer(text='VenetiaIO CLI | {}'.format(CONFIG.VERSION()))
            embed.set_timestamp()

            if image: embed.set_thumbnail(url=image)
            if SITE and region: embed.add_embed_field(name='Site', value='{}  :flag_{}:'.format(SITE.title(), region) ,inline=False)
            else: embed.add_embed_field(name='Site', value=SITE.title(),inline=False)

            if productTitle: embed.add_embed_field(name='Product', value=f'[{productTitle}]({product})',inline=False)
            if productSize: embed.add_embed_field(name='Size', value=productSize,inline=True)
            if productPrice: embed.add_embed_field(name='Product Price', value=productPrice,inline=True)
            if paymentMethod: embed.add_embed_field(name='Payment Method', value=paymentMethod,inline=True)
            if profile: embed.add_embed_field(name='Task Profile', value=f'||{profile}||',inline=True)
            if accountEmail: embed.add_embed_field(name='Account Email', value=f'||{accountEmail}||',inline=False)
            if tracking and order: embed.add_embed_field(name='Tracking', value=f'||[{order}]({tracking})||',inline=False)
            if url: embed.set_url(url=url)
            if proxy: embed.add_embed_field(name='Proxy Used', value=f'||`{proxy}`||',inline=False)
    

            webhook.add_embed(embed)
            webhook.execute()
        except:
            pass

    @staticmethod
    def threeDS(**kwargs):
        webhook = kwargs.get('webhook')
        SITE = kwargs.get('site')
        url = kwargs.get('url')
        image = kwargs.get('image')
        productTitle = kwargs.get('title')
        productSize = kwargs.get('size')
        productPrice = kwargs.get('price')
        paymentMethod = kwargs.get('paymentMethod')
        profile = kwargs.get('profile')
        accountEmail = kwargs.get('account')
        tracking = kwargs.get('tracking')
        order = kwargs.get('order')
        product = kwargs.get('product')
        speed = kwargs.get('speed')
        proxy = kwargs.get('proxy')
        region = kwargs.get('region')
        if proxy:
            try:
                proxy = proxy["https"]
            except:
                proxy = proxy["http"]


        logger.secondary(SITE,'Task Link',url)

        user = getUser()
        try:                
            webhook = DiscordWebhook(webhook)
            embed = DiscordEmbed(title=':rocket: Confirm 3DS Payment :rocket:', description='', color=0xf0e24d)
            embed.set_footer(text='VenetiaIO CLI | {}'.format(CONFIG.VERSION()))
            embed.set_timestamp()    
            if image:
                try:
                    embed.set_thumbnail(url=image)
                except Exception as e:
                    log.info(e)

            if SITE and region: embed.add_embed_field(name='Site', value='{}  :flag_{}:'.format(SITE.title(), region.lower()) ,inline=False)
            else: embed.add_embed_field(name='Site', value=SITE.title(),inline=False)

            if productTitle: embed.add_embed_field(name='Product', value=f'[{productTitle}]({product})',inline=False)
            if productSize: embed.add_embed_field(name='Size', value=str(productSize),inline=True)
            if productPrice: embed.add_embed_field(name='Product Price', value=str(productPrice),inline=True)
            if paymentMethod: embed.add_embed_field(name='Payment Method', value=paymentMethod,inline=True)
            if speed: embed.add_embed_field(name='Checkout Speed', value=str(speed),inline=True)
            if profile: embed.add_embed_field(name='Task Profile', value=f'||{profile}||',inline=True)
            if accountEmail and accountEmail != '': embed.add_embed_field(name='Account Email', value=f'||{accountEmail}||',inline=False)
            if tracking and order: embed.add_embed_field(name='Tracking', value=f'||[{order}]({tracking})||',inline=False)
            # if url: embed.add_embed_field(name='Checkout Link', value=f'[Checkout Here]({url})',inline=False)
            if proxy: embed.add_embed_field(name='Proxy Used', value=f'||`{str(proxy)}`||',inline=False)
            webhook.add_embed(embed)
            webhook.execute()

            myclient = pymongo.MongoClient(mongoConnect)
            mydb = myclient["mydb"]
            collection = mydb["collection"]

            user = getUser()["discordName"]
            data = { "image":image, "site":SITE, "url":product, "product":productTitle, "size":productSize, "price":productPrice, "user":user }
            updateCheckouts(productTitle,SITE,productSize,productPrice,image,product,url)
            x = collection.insert_one(data)
            
        except Exception as e:
            print(e)
            log.info(e)
            pass



    @staticmethod
    def accountMade(**kwargs):
        webhook = kwargs.get('webhook')
        SITE = kwargs.get('site')
        first = kwargs.get('first')
        last = kwargs.get('last')
        email = kwargs.get('email')
        
        try:
            webhook = DiscordWebhook(webhook)
            embed = DiscordEmbed(title=f'{SITE} | Account Created', description='', color=0x1e68e7)
            embed.set_footer(text='VenetiaIO CLI | {}'.format(CONFIG.VERSION()))
            embed.set_timestamp()
    
            if first: embed.add_embed_field(name='First Name', value=first,inline=False)
            if last: embed.add_embed_field(name='Last Name', value=last,inline=False)
            if email: embed.add_embed_field(name='Email', value=email,inline=False)
            webhook.add_embed(embed)
            webhook.execute()
        except:
            pass