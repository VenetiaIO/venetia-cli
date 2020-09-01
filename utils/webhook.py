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

        try:
            webhook = DiscordWebhook(webhook)
            embed = DiscordEmbed(title=f'{SITE} | Checkout Ready', description='', color=0x1e68e7)
            embed.set_footer(text='VenetiaIO CLI')
            embed.set_timestamp()
    
            if url: embed.set_url(url=url)
            if image: embed.set_thumbnail(url=image)
            if productTitle: embed.add_embed_field(name='Product', value=f'[{productTitle}]({product})',inline=False)
            if productSize: embed.add_embed_field(name='Size', value=productSize,inline=False)
            if productPrice: embed.add_embed_field(name='Product Price', value=productPrice,inline=False)
            if paymentMethod: embed.add_embed_field(name='Payment Method', value=paymentMethod,inline=False)
            if profile: embed.add_embed_field(name='Task Profile', value=f'||{profile}||',inline=False)
            if accountEmail: embed.add_embed_field(name='Account', value=f'||{accountEmail}||',inline=False)
            if tracking and order: embed.add_embed_field(name='Tracking', value=f'||[{order}]({tracking})||',inline=False)
            webhook.add_embed(embed)
    
            webhook.execute()
        except:
            pass


        try:
            webhookPublic = DiscordWebhook(publicWebhook)
            embed2 = DiscordEmbed(title=f'{SITE} | User Checkout', description='', color=0x1e68e7)
            embed2.set_footer(text='VenetiaIO CLI')
            embed2.set_timestamp()
    
            if url: embed.set_url(url=url)
            if image: embed2.set_thumbnail(url=image)
            if productTitle: embed2.add_embed_field(name='Product', value=f'[{productTitle}]({product})',inline=False)
            if productSize: embed2.add_embed_field(name='Size', value=productSize,inline=False)
            if productPrice: embed2.add_embed_field(name='Product Price', value=productPrice,inline=False)
            if paymentMethod: embed2.add_embed_field(name='Payment Method', value=paymentMethod,inline=False)
    
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

        try:
            webhook = DiscordWebhook(webhook)
            embed = DiscordEmbed(title=f'{SITE} Checkout Failed', description='', color=0xffffff)
            embed.set_footer(text='VenetiaIO CLI')
            embed.set_timestamp()
    
            if url: embed.set_url(url=url)
            if image: embed.set_thumbnail(url=image)
            if productTitle: embed.add_embed_field(name='Product', value=productTitle,inline=False)
            if productSize: embed.add_embed_field(name='Size', value=productSize,inline=False)
            if productPrice: embed.add_embed_field(name='Product Price', value=productPrice,inline=False)
            if paymentMethod: embed.add_embed_field(name='Payment Method', value=paymentMethod,inline=False)
            if profile: embed.add_embed_field(name='Task Profile', value=f'||{profile}||',inline=False)
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