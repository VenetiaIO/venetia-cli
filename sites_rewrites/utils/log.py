import logging

logging.basicConfig(filename='log.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.ERROR)


class log:
    @staticmethod
    def info(msg):
        logging.error(msg)


#CRITICAL
#ERROR
#WARNING
#INFO
#DEBUG
#NOTSET