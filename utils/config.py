#sites
from sites.svd import SVD
from sites.queens import QUEENS
from sites.allike import ALLIKE
from sites.titolo import TITOLO
from sites.grosbasket import GROSBASKET
from sites.airness import AIRNESS
from sites.footasylum import FOOTASYLUM
from sites.holypop import HOLYPOP
from sites.schuh import SCHUH
from sites.starcow import STARCOW
from sites.slamjam import SLAMJAM
from sites.consortium import CONSORTIUM
from sites.courir import COURIR
from sites.bstn import BSTN
from sites.overkill import OVERKILL
from sites.awlab import AWLAB
from sites.einhalb import EINHALB
from sites.chmielna import CHMIELNA
from sites.workingClassHeroes import WCH
from sites.naked import NAKED
from sites.footdistrict import FOOTDISTRICT
from sites.prodirect import PRODIRECT
from sites.disney import DISNEY
from sites.cornerstreet import CORNERSTREET
from sites.snipes import SNIPES
from sites.solebox import SOLEBOX
from sites.fenom import FENOM
from sites.offspring import OFFSPRING
from sites.office import OFFICE
from sites.footlocker_old import FOOTLOCKER_OLD
from sites.footlocker_new import FOOTLOCKER_NEW
from sites.ambush import AMBUSH

# from sites.mesh.jd import JD

sites = {
    "SVD":SVD, #WATERFALL MONITOR
    "QUEENS":QUEENS,
    "TITOLO":TITOLO, #WATERFALL MONITOR
    "AIRNESS":AIRNESS,
    "FOOTASYLUM":FOOTASYLUM, #WATERFALL MONITOR
    "HOLYPOP":HOLYPOP,
    "ALLIKE":ALLIKE, #WATERFALL MONITOR
    "GROSBASKET":GROSBASKET,
    "SCHUH":SCHUH, #WATERFALL MONITOR
    "SLAMJAM":SLAMJAM,
    "AWLAB":AWLAB, #WATERFALL MONITOR
    #"EINHALB":EINHALB,
    #"STARCOW":STARCOW,
    "CHMIELNA20":CHMIELNA, #WATERFALL MONITOR
    "WCH":WCH, 
    "NAKED":NAKED,
    #"FOOTDISTRICT":FOOTDISTRICT,
    "PRODIRECT":PRODIRECT,
    "DISNEY":DISNEY,
    #"CORNERSTREET":CORNERSTREET,
    #"BSTN":BSTN,
    "SNIPES":SNIPES, #WATERFALL MONITOR
    #"COURIR":COURIR,
    #"SOLEBOX":SOLEBOX,
    # "FENOM":FENOM,
    "OFFSPRING":OFFSPRING, #WATERFALL MONITOR
    "OFFICE":OFFICE, #WATERFALL MONITOR
    "FOOTLOCKER_OLD":FOOTLOCKER_OLD,
    "FOOTLOCKER_NEW":FOOTLOCKER_NEW,
    "AMBUSH":AMBUSH, #WATERFALL MONITOR,
    # "JD":JD
}

def VERSION(): return '0.6.2.5'

def new_footlockers(): return ['IT','BE','AT','LU','CZ','DK','PL','GR','PT','HU','ES','IE','NO','SE','DE']
def old_footlockers(): return ['FR','NL','GB','AU','SG','MY','HK']

def account_sites(): return ['holypop','naked','footasylum','snipes','wch','prodirect']