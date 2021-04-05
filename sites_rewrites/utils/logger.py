#from colorama import init
#from termcolor import colored
from colorama import Fore, Back, Style, init
import datetime
import sys
import threading

init(autoreset=True)

lock = threading.Lock()



def get_task(SITE,taskID,color):
    x = datetime.datetime.now().strftime('%Y.%m.%d | %H:%M:%S.%f')
    #thread = threading.currentThread().getName()
    # status = '[{}{}{}{}{:<12}{}'.format(Fore.CYAN + Style.BRIGHT + x, Fore.WHITE + '][ ', Fore.YELLOW + taskID, Fore.WHITE + ' ][ ',Fore.WHITE + SITE.title(), Fore.WHITE + ' ]')
    status = '[{}{}{}{}{:<10}{}'.format(Fore.CYAN + Style.BRIGHT + x, Fore.WHITE + ']' + color + '[ ', color + taskID, ' ][ ', SITE, ' ]')
    return status

    # 10:35:56.191801


class logger:
    @staticmethod
    def success(site,taskID,message):
        try:
            lock.acquire()
            try:
                #print('{} {}'.format(get_task(site,taskID), colored(f'{message}\n', 'green',attrs=["bold"])))
                print('{} {}'.format(get_task(site,taskID,Fore.GREEN), Fore.GREEN + message))
                # sys.stdout.flush()
            finally:
                lock.release()
        except Exception as e:
            print(e)
            pass

    @staticmethod
    def error(site,taskID,message):
        try:
            lock.acquire()
            try:
                #print('{} {}'.format(get_task(site,taskID), colored(f'{message}\n', 'red',attrs=["bold"])))
                print('{} {}'.format(get_task(site,taskID,Fore.RED), Fore.RED + message))
                # sys.stdout.flush()
            finally:
                lock.release()
        except Exception as e:
            print(e)
            pass

    @staticmethod
    def warning(site,taskID,message):
        try:
            lock.acquire()
            try:
                #print('{} {}'.format(get_task(site,taskID), colored(f'{message}\n', 'yellow')))
                print('{} {}'.format(get_task(site,taskID,Fore.YELLOW+ Style.DIM), Fore.YELLOW + Style.DIM + message))
                # sys.stdout.flush()
            finally:
                lock.release()
        except Exception as e:
            print(e)
            pass

    @staticmethod
    def info(site,taskID,message):
        try:
            lock.acquire()
            try:
                #print('{} {}'.format(get_task(site,taskID), colored(f'{message}\n', 'blue',attrs=["bold"])))
                print('{} {}'.format(get_task(site,taskID,Fore.BLUE+ Style.BRIGHT), Fore.BLUE + Style.BRIGHT +message))
                # sys.stdout.flush()
            finally:
                lock.release()
        except Exception as e:
            print(e)
            pass

    @staticmethod
    def alert(site,taskID,message):
        try:
            lock.acquire()
            try:
                #print('{} {}'.format(get_task(site,taskID), colored(f'{message}\n', 'cyan',attrs=["bold"])))
                print('{} {}'.format(get_task(site,taskID,Fore.CYAN+ Style.BRIGHT), Fore.CYAN + Style.BRIGHT + message))
                # sys.stdout.flush()
            finally:
                lock.release()
        except Exception as e:
            print(e)
            pass

    @staticmethod
    def secondary(site,taskID,message):
        try:
            lock.acquire()
            try:
                #print('{} {}'.format(get_task(site,taskID), colored(f'{message}\n', 'magenta',attrs=["bold"])))
                print('{} {}'.format(get_task(site,taskID,Fore.MAGENTA), Fore.MAGENTA + message))
                # sys.stdout.flush()
            finally:
                lock.release()
        except Exception as e:
            print(e)
            pass

    @staticmethod
    def prepare(site,taskID,message):
        try:
            lock.acquire()
            try:
                #print('{} {}'.format(get_task(site,taskID), colored(f'{message}\n', 'magenta',attrs=["bold"])))
                print('{} {}'.format(get_task(site,taskID,Fore.WHITE+ Style.BRIGHT), Fore.WHITE + Style.BRIGHT + message))
                # sys.stdout.flush()
            finally:
                lock.release()
        except Exception as e:
            print(e)
            pass


    @staticmethod
    def menu(site,taskID,message):
        lock.acquire()
        try:
            #print('{} {}'.format(get_task(site,taskID), f'{message}\n'))
            return '{} {}'.format(get_task(site.title(),taskID,Fore.WHITE), message)
            # sys.stdout.flush()
        finally:
            lock.release()

    @staticmethod
    def menu2(site,taskID,message):
        lock.acquire()
        try:
            #print('{} {}'.format(get_task(site,taskID), f'{message}\n'))
            print('{} {}'.format(get_task(site.title(),taskID,Fore.WHITE), message))
            # sys.stdout.flush()
        finally:
            lock.release()

    @staticmethod
    def other_grey(message):
        lock.acquire()
        try:
            #print('{} {}'.format(get_task(site,taskID), f'{message}\n'))
            print(Fore.WHITE + Style.DIM + message)
            # sys.stdout.flush()
        finally:
            lock.release()

    @staticmethod
    def other_green(message):
        lock.acquire()
        try:
            #print('{} {}'.format(get_task(site,taskID), f'{message}\n'))
            print(Fore.GREEN + Style.NORMAL + message)
            # sys.stdout.flush()
        finally:
            lock.release()

    @staticmethod
    def other_yellow(message, other):
        lock.acquire()
        try:
            #print('{} {}'.format(get_task(site,taskID), f'{message}\n'))
            print('{}{} \n'.format(Fore.YELLOW + Style.DIM + message, Fore.GREEN + Style.DIM + str(other)),Fore.GREEN + Style.DIM)
            # sys.stdout.flush()
        finally:
            lock.release()


    @staticmethod
    def logo(text,VERSION):
        print(Fore.CYAN + Style.BRIGHT + text + Fore.RED + Style.BRIGHT + 'v' + VERSION)
    