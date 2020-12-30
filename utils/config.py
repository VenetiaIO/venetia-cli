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

sites = {
    "SVD":SVD,
    "QUEENS":QUEENS,
    "TITOLO":TITOLO,
    "AIRNESS":AIRNESS,
    "FOOTASYLUM":FOOTASYLUM,
    "HOLYPOP":HOLYPOP,
    "ALLIKE":ALLIKE,
    "GROSBASKET":GROSBASKET,
    "SCHUH":SCHUH,
    "SLAMJAM":SLAMJAM,
    "AWLAB":AWLAB,
    #"EINHALB":EINHALB,
    #"STARCOW":STARCOW,
    "CHMIELNA20":CHMIELNA,
    "WCH":WCH,
    "NAKED":NAKED,
    #"FOOTDISTRICT":FOOTDISTRICT,
    "PRODIRECT":PRODIRECT,
    "DISNEY":DISNEY,
    #"CORNERSTREET":CORNERSTREET,
    #"BSTN":BSTN,
    "SNIPES":SNIPES,
    #"COURIR":COURIR,
    #"SOLEBOX":SOLEBOX,
    #"FENOM":FENOM,
    "OFFSPRING":OFFSPRING,
    "OFFICE":OFFICE
}

def VERSION(): return '0.5.2'