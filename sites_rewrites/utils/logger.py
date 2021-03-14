#from colorama import init
#from termcolor import colored
from colorama import Fore, Back, Style, init
import datetime
import sys
import threading
import asyncio

init(autoreset=True)

# lock = threading.Lock()
LOCK = asyncio.Lock()


async def get_task(SITE,taskID,color):
    x = datetime.datetime.now()
    x = f'{x.strftime("%Y")}-{x.strftime("%m")}-{x.strftime("%d")} {x.strftime("%X")},{x.strftime("%f")}'
    #thread = threading.currentThread().getName()
    # status = '[{}{}{}{}{:<12}{}'.format(Fore.CYAN + Style.BRIGHT + x, Fore.WHITE + '][ ', Fore.YELLOW + taskID, Fore.WHITE + ' ][ ',Fore.WHITE + SITE.title(), Fore.WHITE + ' ]')
    status = '[{}{}{}{}{:<10}{}'.format(Fore.CYAN + Style.BRIGHT + x, Fore.WHITE + ']' + color + '[ ', color + taskID, ' ][ ', SITE.title(), ' ]')
    return status

    # 10:35:56.191801


class logger:
    @staticmethod
    async def success(site,taskID,message):
        try:
            async with LOCK:
                #print('{} {}'.format(get_task(site,taskID), colored(f'{message}\n', 'green',attrs=["bold"])))
                print('{} {}'.format(await get_task(site,taskID,Fore.GREEN), Fore.GREEN + message))

        except Exception as e:
            pass

    @staticmethod
    async def error(site,taskID,message):
        try:
            async with LOCK:
                #print('{} {}'.format(get_task(site,taskID), colored(f'{message}\n', 'red',attrs=["bold"])))
                print('{} {}'.format(await get_task(site,taskID,Fore.RED), Fore.RED + message))
        except Exception as e:
            pass

    @staticmethod
    async def warning(site,taskID,message):
        try:
            async with LOCK:
                #print('{} {}'.format(get_task(site,taskID), colored(f'{message}\n', 'yellow')))
                print('{} {}'.format(await get_task(site,taskID,Fore.YELLOW+ Style.DIM), Fore.YELLOW + Style.DIM + message))
        except Exception as e:
            pass

    @staticmethod
    async def info(site,taskID,message):
        try:
            async with LOCK:
                #print('{} {}'.format(get_task(site,taskID), colored(f'{message}\n', 'blue',attrs=["bold"])))
                print('{} {}'.format(await get_task(site,taskID,Fore.BLUE+ Style.BRIGHT), Fore.BLUE + Style.BRIGHT +message))
        except Exception as e:
            pass

    @staticmethod
    async def alert(site,taskID,message):
        try:
            async with LOCK:
                #print('{} {}'.format(get_task(site,taskID), colored(f'{message}\n', 'cyan',attrs=["bold"])))
                print('{} {}'.format(await get_task(site,taskID,Fore.CYAN+ Style.BRIGHT), Fore.CYAN + Style.BRIGHT + message))
        except Exception as e:
            pass

    @staticmethod
    async def secondary(site,taskID,message):
        try:
            async with LOCK:
                #print('{} {}'.format(get_task(site,taskID), colored(f'{message}\n', 'magenta',attrs=["bold"])))
                print('{} {}'.format(await get_task(site,taskID,Fore.MAGENTA), Fore.MAGENTA + message))
        except Exception as e:
            pass

    @staticmethod
    async def prepare(site,taskID,message):
        try:
            async with LOCK:
                #print('{} {}'.format(get_task(site,taskID), colored(f'{message}\n', 'magenta',attrs=["bold"])))
                print('{} {}'.format(await get_task(site,taskID,Fore.WHITE+ Style.BRIGHT), Fore.WHITE + Style.BRIGHT + message))
        except Exception as e:
            pass


    @staticmethod
    async def menu(site,taskID,message):
        async with LOCK:
            #print('{} {}'.format(get_task(site,taskID), f'{message}\n'))
            return '{} {}'.format(await get_task(site.title(),taskID,Fore.WHITE), message)
    
    @staticmethod
    async def menu2(site,taskID,message):
        async with LOCK:
            #print('{} {}'.format(get_task(site,taskID), f'{message}\n'))
            print('{} {}'.format(await get_task(site,taskID,Fore.WHITE), message))

    @staticmethod
    async def other_grey(message):
        async with LOCK:
            #print('{} {}'.format(get_task(site,taskID), f'{message}\n'))
            print(Fore.WHITE + Style.DIM + message)

    @staticmethod
    async def other_green(message):
        async with LOCK:
            #print('{} {}'.format(get_task(site,taskID), f'{message}\n'))
            print(Fore.GREEN + Style.NORMAL + message)

    @staticmethod
    async def other_yellow(message, other):
        async with LOCK:
            #print('{} {}'.format(get_task(site,taskID), f'{message}\n'))
            print('{}{} \n'.format(Fore.YELLOW + Style.DIM + message, Fore.GREEN + Style.DIM + str(other)),Fore.GREEN + Style.DIM)

    @staticmethod
    async def logo(text,VERSION):
        async with LOCK:
            print(Fore.CYAN + Style.BRIGHT + text + Fore.RED + Style.BRIGHT + 'v' + VERSION)
    