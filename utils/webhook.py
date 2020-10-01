from discord_webhook import DiscordWebhook, DiscordEmbed

publicWebhook = 'https://discordapp.com/api/webhooks/734209129035333683/3pZfyBnoSIxndJQjsrEQvDGSlKsEoRF8NzwEKggq4jaUHj-A61cGXNW6MXdJMyYX_qbH'

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
        if proxy: proxy = proxy["https"]

        try:
            webhook = DiscordWebhook(webhook)
            embed = DiscordEmbed(title='Successful Checkout 🚀', description='', color=0x2feb61)
            embed.set_footer(text='VenetiaIO CLI')
            embed.set_timestamp()
    
            if image: embed.set_thumbnail(url=f'https://imageresize.24i.com/?url={image}')
            if SITE: embed.add_embed_field(name='Site', value=SITE.title(),inline=False)
            if productTitle: embed.add_embed_field(name='Product', value=f'[{productTitle}]({product})',inline=False)
            if productSize: embed.add_embed_field(name='Size', value=str(productSize),inline=True)
            if productPrice: embed.add_embed_field(name='Product Price', value=str(productPrice),inline=True)
            if paymentMethod: embed.add_embed_field(name='Payment Method', value=paymentMethod,inline=True)
            if speed: embed.add_embed_field(name='Checkout Speed', value=str(speed),inline=True)
            if profile: embed.add_embed_field(name='Task Profile', value=f'||{profile}||',inline=True)
            if accountEmail: embed.add_embed_field(name='Account Email', value=f'||{accountEmail}||',inline=False)
            if tracking and order: embed.add_embed_field(name='Tracking', value=f'||[{order}]({tracking})||',inline=False)
            if url: embed.add_embed_field(name='Checkout Link', value=f'[Checkout Here]({url})',inline=False)
            if proxy: embed.add_embed_field(name='Proxy Used', value=f'||`{str(proxy)}`||',inline=False)
            webhook.add_embed(embed)
    
            webhook.execute()
        except Exception as e:
            pass


        try:
            webhookPublic = DiscordWebhook(publicWebhook)
            embed2 = DiscordEmbed(title='User Checkout 🚀', description='', color=0x2feb61)
            embed2.set_footer(text='VenetiaIO CLI')
            embed2.set_timestamp()
    
            if image: embed2.set_thumbnail(url=f'https://imageresize.24i.com/?url={image}')
            if SITE: embed2.add_embed_field(name='Site', value=SITE.title(),inline=False)
            if productTitle: embed2.add_embed_field(name='Product', value=f'[{productTitle}]({product})',inline=False)
            if productSize: embed2.add_embed_field(name='Size', value=str(productSize),inline=False)
            if productPrice: embed2.add_embed_field(name='Product Price', value=str(productPrice),inline=False)
    
            QT_URL = 'http://127.0.0.1:6969/venetia/quicktask?website={}&url={}'.format(SITE.lower(),product)
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
        if proxy: proxy = proxy["https"]

        try:
            webhook = DiscordWebhook(webhook)
            embed = DiscordEmbed(title='Checkout Failed ⛔', description='', color=0xeb3c2f)
            embed.set_footer(text='VenetiaIO CLI')
            embed.set_timestamp()

            if image: embed.set_thumbnail(url=f'https://imageresize.24i.com/?url={image}')
            if SITE: embed.add_embed_field(name='Site', value=SITE.title(),inline=False)
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
    def accountMade(**kwargs):
        webhook = kwargs.get('webhook')
        SITE = kwargs.get('site')
        first = kwargs.get('first')
        last = kwargs.get('last')
        email = kwargs.get('email')
        
        try:
            webhook = DiscordWebhook(webhook)
            embed = DiscordEmbed(title=f'{SITE} | Account Created', description='', color=0x1e68e7)
            embed.set_footer(text='VenetiaIO CLI')
            embed.set_timestamp()
    
            if first: embed.add_embed_field(name='First Name', value=first,inline=False)
            if last: embed.add_embed_field(name='Last Name', value=last,inline=False)
            if email: embed.add_embed_field(name='Email', value=email,inline=False)
            webhook.add_embed(embed)
            webhook.execute()
        except:
            pass