#sites
from sites.svd import SVD
# from sites.queens import QUEENS
from sites.allike import ALLIKE
from sites.titolo import TITOLO
# from sites.grosbasket import GROSBASKET
# from sites.airness import AIRNESS
from sites.footasylum import FOOTASYLUM
# from sites.holypop import HOLYPOP
# from sites.schuh import SCHUH
# from sites.starcow import STARCOW
from sites.slamjam import SLAMJAM
# from sites.consortium import CONSORTIUM
# from sites.courir import COURIR
# from sites.bstn import BSTN
# from sites.overkill import OVERKILL
from sites.awlab import AWLAB
# from sites.einhalb import EINHALB
# from sites.chmielna import CHMIELNA
# from sites.workingClassHeroes import WCH
# from sites.naked import NAKED
# from sites.footdistrict import FOOTDISTRICT
# from sites.prodirect import PRODIRECT
from sites.disney import DISNEY
# from sites.cornerstreet import CORNERSTREET
from sites.snipes import SNIPES
# from sites.solebox import SOLEBOX
# from sites.fenom import FENOM
from sites.offspring import OFFSPRING
# from sites.office import OFFICE
from sites.footlocker_old import FOOTLOCKER_OLD
from sites.footlocker_new import FOOTLOCKER_NEW
# from sites.ambush import AMBUSH
from sites.converse import CONVERSE
from sites.jd import JD
from sites.size import SIZE
from sites.footpatrol import FOOTPATROL
from sites.asos import ASOS

sites = {
    "SVD":SVD, #WATERFALL MONITOR
    # "QUEENS":QUEENS,
    "TITOLO":TITOLO, #WATERFALL MONITOR
    # "AIRNESS":AIRNESS,
    "FOOTASYLUM":FOOTASYLUM, #WATERFALL MONITOR
    # "HOLYPOP":HOLYPOP,
    "ALLIKE":ALLIKE, #WATERFALL MONITOR
    # "GROSBASKET":GROSBASKET,
    # "SCHUH":SCHUH, #WATERFALL MONITOR
    # "SLAMJAM":SLAMJAM,
    "AWLAB":AWLAB, #WATERFALL MONITOR
    #"EINHALB":EINHALB,
    #"STARCOW":STARCOW,
    # "CHMIELNA20":CHMIELNA, #WATERFALL MONITOR
    # "WCH":WCH, 
    # "NAKED":NAKED,
    #"FOOTDISTRICT":FOOTDISTRICT,
    # "PRODIRECT":PRODIRECT,
    "DISNEY":DISNEY,
    #"CORNERSTREET":CORNERSTREET,
    #"BSTN":BSTN,
    "SNIPES":SNIPES, #WATERFALL MONITOR
    #"COURIR":COURIR,
    #"SOLEBOX":SOLEBOX,
    # "FENOM":FENOM,
    # "OFFSPRING":OFFSPRING, #WATERFALL MONITOR
    # "OFFICE":OFFICE, #WATERFALL MONITOR
    # "FOOTLOCKER_OLD":FOOTLOCKER_OLD,
    "FOOTLOCKER":FOOTLOCKER_NEW,
    # "AMBUSH":AMBUSH, #WATERFALL MONITOR,
    "JD":JD,
    "SIZE":SIZE,
    "FOOTPATROL":FOOTPATROL,
    "CONVERSE":CONVERSE,
    # "ASOS":ASOS
}

def VERSION(): return '0.10.0'

def new_footlockers(): return ['IT','BE','AT','LU','CZ','DK','PL','GR','PT','HU','ES','IE','NO','SE','DE','FR','NL','GB']
def old_footlockers(): return ['AU','SG','MY','HK']

def account_sites(): return ['holypop','naked','footasylum','snipes','wch','prodirect']


def waterfall_sites(): return [
                                'allike',
                                'ambush',
                                'awlab',
                                'chmielna20',
                                'footasylum',
                                'office',
                                'offspring',
                                'schuh',
                                'snipes',
                                'svd',
                                'titolo'
                            ]


# types
# V2, V3, V2_INVISIBLE
captcha_configs = {
    "SVD":{
        "hasCaptcha":False,
        "siteKey":"",
        "type":"",
        "url":""
    },
    "TITOLO":{
        "hasCaptcha":False,
        "siteKey":"",
        "type":"",
        "url":""
    },
    "FOOTASYLUM":{
        "hasCaptcha":True,
        "siteKey":"6LfENJwUAAAAANpLoBFfQG7BbAR4iQd-FvXSUzO8",
        "type":"V3",
        "url":"https://www.footasylum.com/"
    },
    "ALLIKE":{
        "hasCaptcha":True,
        "siteKey":"6LfMDQEaAAAAAK2OeOZtpVHc4gTPjAdZ8kHcXHCR",
        "type":"V3",
        "url":"https://www.allikestore.com/"
    },
    "SLAMJAM":{
        "hasCaptcha":False,
        "siteKey":"",
        "type":"",
        "url":""
    },
    "AWLAB":{
        "hasCaptcha":True,
        "siteKey":"6Lf7htIZAAAAAKVu_e4Hyg3nhCXfVh2tlQbOjzYT",
        "type":"V2",
        "url":"https://www.aw-lab.com/"
    },
    # "NAKED":{
    #     "hasCaptcha":True,
    #     "siteKey":"6LeNqBUUAAAAAFbhC-CS22rwzkZjr_g4vMmqD_qo",
    #     "type":"V2",
    #     "url":"https://www.nakedcph.com/"
    # },
    "DISNEY":{
        "hasCaptcha":False,
        "siteKey":"",
        "type":"",
        "url":""
    },
    "SNIPES":{
        "hasCaptcha":False,
        "siteKey":"",
        "type":"",
        "url":""
    },
    # "OFFSPRING":{
    #     "hasCaptcha":True,
    #     "siteKey":"6Ld-VBsUAAAAABeqZuOqiQmZ-1WAMVeTKjdq2-bJ",
    #     "type":"V2",
    #     "url":"https://www.offspring.co.uk/"
    # },
    # "OFFICE":{
    #     "hasCaptcha":True,
    #     "siteKey":"6Ld-VBsUAAAAABeqZuOqiQmZ-1WAMVeTKjdq2-bJ",
    #     "type":"V2",
    #     "url":"https://www.office.co.uk/"
    # },
    "FOOTLOCKER_OLD":{
        "hasCaptcha":False,
        "siteKey":"",
        "type":"",
        "url":""
    },
    "FOOTLOCKER_NEW":{
        "hasCaptcha":False,
        "siteKey":"",
        "type":"",
        "url":""
    },
    "JD":{
        "hasCaptcha":False,
        "siteKey":"",
        "type":"",
        "url":""
    },
    "SIZE":{
        "hasCaptcha":False,
        "siteKey":"",
        "type":"",
        "url":""
    },
    "FOOTPATROL":{
        "hasCaptcha":True,
        "siteKey":"6LfEwHQUAAAAACTyJsAICi2Lz2oweGni8QOhV-Yl",
        "type":"V2_INVISIBLE",
        "url":"https://www.footpatrol.com/"
    },
}