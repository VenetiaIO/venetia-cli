#from colorama import init
#from termcolor import colored
from colorama import Fore, Back, Style, init
import datetime
import sys
import threading

init(autoreset=True)

lock = threading.Lock()
sys.setrecursionlimit(9999)


def get_task(SITE,taskID):
    x = datetime.datetime.now()
    x = f'{x.strftime("%X")}.{x.strftime("%f")}'
    #thread = threading.currentThread().getName()
    status = '[{}{}{}{}{}{}'.format(Fore.CYAN + Style.BRIGHT + x, Fore.WHITE + '][ ', Fore.YELLOW + taskID, Fore.WHITE + ' ][ ',Fore.WHITE + SITE.title(), Fore.WHITE + ' ]')
    return status


class logger:
    @staticmethod
    def success(site,taskID,message):
        lock.acquire()
        try:
            #sys.stdout.write('{} {}'.format(get_task(site,taskID), colored(f'{message}\n', 'green',attrs=["bold"])))
            sys.stdout.write('{} {}'.format(get_task(site,taskID), Fore.GREEN + message + '\n'))
        finally:
            lock.release()

    @staticmethod
    def error(site,taskID,message):
        lock.acquire()
        try:
            #sys.stdout.write('{} {}'.format(get_task(site,taskID), colored(f'{message}\n', 'red',attrs=["bold"])))
            sys.stdout.write('{} {}'.format(get_task(site,taskID), Fore.RED + message + '\n'))
        finally:
            lock.release()

    @staticmethod
    def warning(site,taskID,message):
        lock.acquire()
        try:
            #sys.stdout.write('{} {}'.format(get_task(site,taskID), colored(f'{message}\n', 'yellow')))
            sys.stdout.write('{} {}'.format(get_task(site,taskID), Fore.YELLOW + Style.DIM + message + '\n'))
        finally:
            lock.release()

    @staticmethod
    def info(site,taskID,message):
        lock.acquire()
        try:
            #sys.stdout.write('{} {}'.format(get_task(site,taskID), colored(f'{message}\n', 'blue',attrs=["bold"])))
            sys.stdout.write('{} {}'.format(get_task(site,taskID), Fore.BLUE + Style.BRIGHT +message + '\n'))
        finally:
            lock.release()

    @staticmethod
    def alert(site,taskID,message):
        lock.acquire()
        try:
            #sys.stdout.write('{} {}'.format(get_task(site,taskID), colored(f'{message}\n', 'cyan',attrs=["bold"])))
            sys.stdout.write('{} {}'.format(get_task(site,taskID), Fore.CYAN + Style.BRIGHT + message + '\n'))
        finally:
            lock.release()

    @staticmethod
    def secondary(site,taskID,message):
        lock.acquire()
        try:
            #sys.stdout.write('{} {}'.format(get_task(site,taskID), colored(f'{message}\n', 'magenta',attrs=["bold"])))
            sys.stdout.write('{} {}'.format(get_task(site,taskID), Fore.MAGENTA + message + '\n'))
        finally:
            lock.release()

    @staticmethod
    def prepare(site,taskID,message):
        lock.acquire()
        try:
            #sys.stdout.write('{} {}'.format(get_task(site,taskID), colored(f'{message}\n', 'magenta',attrs=["bold"])))
            sys.stdout.write('{} {}'.format(get_task(site,taskID), Fore.WHITE + Style.BRIGHT + message + '\n'))
        finally:
            lock.release()


    @staticmethod
    def menu(site,taskID,message):
        lock.acquire()
        try:
            #sys.stdout.write('{} {}'.format(get_task(site,taskID), f'{message}\n'))
            sys.stdout.write('{} {}'.format(get_task(site,taskID), message + '\n'))
        finally:
            lock.release()

    @staticmethod
    def other_grey(message):
        lock.acquire()
        try:
            #sys.stdout.write('{} {}'.format(get_task(site,taskID), f'{message}\n'))
            sys.stdout.write(Fore.WHITE + Style.DIM + message + '\n')
        finally:
            lock.release()

    @staticmethod
    def other_green(message):
        lock.acquire()
        try:
            #sys.stdout.write('{} {}'.format(get_task(site,taskID), f'{message}\n'))
            sys.stdout.write(Fore.GREEN + Style.NORMAL + message + '\n')
        finally:
            lock.release()

    @staticmethod
    def other_yellow(message, other):
        lock.acquire()
        try:
            #sys.stdout.write('{} {}'.format(get_task(site,taskID), f'{message}\n'))
            sys.stdout.write('{}{} \n'.format(Fore.YELLOW + Style.DIM + message, Fore.GREEN + Style.DIM + str(other)))
        finally:
            lock.release()


    @staticmethod
    def logo(text,VERSION):
        print(Fore.CYAN + Style.BRIGHT + text + Fore.RED + Style.BRIGHT + 'v' + VERSION)
    