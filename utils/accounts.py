import requests
import random
import names
import json
from bs4 import BeautifulSoup

from utils.captcha import captcha
from utils.logger import logger
from utils.webhook import discord
from utils.functions import (loadProxy,loadProfile,loadSettings, scraper)



def genCustomer(catchall):
    gender = random.choice(['male','female'])
    firstName = names.get_first_name(gender=gender)
    lastName = names.get_last_name()
    numbers = '{}{}{}'.format(random.randint(1,9),random.randint(1,9),random.randint(1,9))
    email = firstName + lastName + numbers + catchall

    year = '19{}{}'.format(random.randint(5,9),random.randint(0,9))
    month = random.randint(1,9)
    day = random.randint(1,27)
    formatted = '{}-{}-{}'.format(year,month,day)

    return {"email":email,"first":firstName,"last":lastName,"sex":gender.upper(),"birthday":formatted}


class ACCOUNTS:

    @staticmethod
    def holypop(sitekey,proxies,SITE,catchall,password,profile):
        taskID = 'Accounts'
        logger.warning(SITE,taskID,'Getting login page...')

        session = requests.session()
        proxies = loadProxy(proxies,taskID,SITE)
        session.proxies = proxies
        session.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'referer':'https://www.holypopstore.com'
        }

        try:
            getLogin = session.get('https://www.holypopstore.com/')
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            return None
        if getLogin.status_code == 200:
            captchaResponse = captcha.Hiddenv2(sitekey,'https://www.holypopstore.com',proxies,SITE,taskID)

            try:
                version = getLogin.text.split("b.version = '")[1].split("';")[0]
                cookieVersion = getLogin.text.split("b.cookieVersion = '")[1].split("';")[0]
                region = getLogin.text.split("b.locale = '")[1].split("';")[0].upper()
            except:
                return None

            customer = genCustomer(catchall)

            payload = {
                'controller': 'auth',
                'action': 'register',
                'extension': 'holypop',
                'email': customer["email"],
                'password': password,
                'firstName': customer["first"],
                'lastName': customer["last"],
                'birthDate': customer["birthday"],
                'sex': customer["sex"],
                'privacy[1]': 1,
                'privacy[2]': 0,
                'recaptcha': captchaResponse,
                'language': region,
                'version': version,
                'cookieVersion': cookieVersion
            }


            session.headers['x-requested-with'] = 'XMLHttpRequest'
            session.headers['accept'] = 'application/json, text/javascript, */*; q=0.01'
            try:
                postInfo = session.post('https://www.holypopstore.com/index.php',data=payload)
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                return None
            if postInfo.status_code == 200:
                logger.success(SITE,taskID,'Created Account - {}'.format(customer["email"]))
                profile = loadProfile(profile)


                            
                try:
                    soup = BeautifulSoup(holypop_data,"html.parser")
                    options = soup.find_all("option")
                    for s in options:
                        if str(s.text).lower() == profile["country"].lower():
                            countryId = s["value"]
                except:
                    return None



                logger.warning(SITE,taskID,'Adding Address...')
                payload = {
                    'controller': 'users',
                    'action': 'saveAddresses',
                    'addresses[0][counter]': 'nn1',
                    'addresses[0][first_name]': customer["first"],
                    'addresses[0][last_name]': customer["last"],
                    'addresses[0][full_name]': '{} {}'.format(customer["first"], customer["last"]),
                    'addresses[0][email]': customer["email"],
                    'addresses[0][street_address]': '{} {}, {}'.format(profile["house"], profile["addressOne"], profile["addressTwo"]),
                    'addresses[0][zipcode]': profile["zip"],
                    'addresses[0][cityName]': profile["city"],
                    'addresses[0][statecode]': profile["region"],
                    'addresses[0][countryId]': countryId,
                    'addresses[0][countryName]': profile["country"],
                    'addresses[0][phone_number]': profile["phone"],
                    'addresses[0][isDefault]': 1,
                    'extension': 'holypop',
                    'language': region,
                    'version': version,
                    'cookieVersion': cookieVersion
                }
                try:
                    postInfo = session.post('https://www.holypopstore.com/index.php',data=payload)
                except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                    return None

                logger.success(SITE,taskID,'Address Added!')
                discord.accountMade(
                    webhook=loadSettings()["webhook"],
                    site=SITE,
                    first=customer["first"],
                    last=customer["last"],
                    email=customer["email"]
                )
                with open('./hoylpop/accounts.txt','a') as accounts:
                    accounts.write('\n{}:{}'.format(customer["email"],password))

                return 1
        
        else:
            logger.error(SITE,taskID,'Failed to create account')
            return None

    
    @staticmethod
    def proDirect(sitekey,proxies,SITE,catchall,password,profile):
        taskID = 'Accounts'
        logger.warning(SITE,taskID,'Creating account...')

        session = scraper()
        session.proxies = loadProxy(proxies,taskID,SITE)
        session.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'referer':'https://www.prodirectbasketball.com/accounts/MyAccount.aspx',
        }

        try:
            getPage = session.get('https://www.prodirectbasketball.com/accounts/MyAccount.aspx')
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            logger.error(SITE,taskID,'Failed to create account')
            return None

        captchaResponse = captcha.v2('6LdXsbwUAAAAAMe1vJVElW1JpeizmksakCUkLL8g',session.headers['referer'],session.proxies,SITE,taskID)
        
        customer = genCustomer(catchall)
        form = {
            'registeremail': customer['email'],
            'registerpassword': password,
            'g-recaptcha-response': captchaResponse,
            '__EVENTTARGET':'Register'
        }
        try:
            postInfo = session.post('https://www.prodirectbasketball.com/accounts/MyAccount.aspx',data=form)
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            logger.error(SITE,taskID,'Failed to create account')
            return None
        if postInfo.status_code in [200,302]:
            logger.success(SITE,taskID,'Created Account - {}'.format(customer["email"]))
            logger.warning(SITE,taskID,'Adding Address...')

            profile = loadProfile(profile)

            soup = BeautifulSoup(prodirect_data,"html.parser")
            options = soup.find_all("option")
            for s in options:
                if str(s.text).lower() == profile["country"].lower():
                    countryId = s["value"]



            session.headers = {}
            session.headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'referer':'https://www.prodirectbasketball.com/accounts/MyAccount.aspx?acc=ABOOK',
            }
            
            form2 = {
                'txtlookupprop': 'main',
                'txtlookuppostcode': profile['zip'],
                'txtAddressLine1': profile['addressOne'],
                'txtAddressLine2': profile['addressTwo'],
                'txttown': profile['city'],
                'txtcounty': profile['region'],
                'txtpostcode': profile['zip'],
                'txtAddressID': 0,
                'ddlCountry': countryId,
                'ddlState': '',
                '__EVENTTARGET': 'dlw100$SaveNewAddress'
            }
            try:
                addAddress = session.post('https://www.prodirectbasketball.com/accounts/MyAccount.aspx?acc=ABOOK',data=form2)
            except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
                logger.error(SITE,taskID,'Failed to create account')
                return None
            if addAddress.status_code == 200:
                logger.success(SITE,taskID,'Address Added!')
                discord.accountMade(
                    webhook=loadSettings()["webhook"],
                    site=SITE,
                    first=customer["first"],
                    last=customer["last"],
                    email=customer["email"]
                )
                with open('./prodirect/accounts.txt','a') as accounts:
                    accounts.write('\n{}:{}'.format(customer["email"],password))
                return 1
            
            else:
                logger.error(SITE,taskID,'Failed to add address')
                return None
        
        else:
            logger.error(SITE,taskID,'Failed to create account')
            return None

    
    @staticmethod
    def footasylum(sitekey,proxies,SITE,catchall,password,profile):
        taskID = 'Accounts'
        logger.warning(SITE,taskID,'Creating account...')

        session = scraper()
        session.proxies = loadProxy(proxies,taskID,SITE)
        session.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        }

        try:
            page = session.get('https://www.footasylum.com/page/yourdetails/')
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            return None

        customer = genCustomer(catchall)
        profile = loadProfile(profile)


        form = {
            "target": "",
            "reg_validate": 1,
            "cust_reg_type": "REGISTER",
            "email": customer['email'],
            "mobile_phone": str(profile['phone']),
            "mobile_phone_option": 0,
            "login_password": password,
            "login_password2": password,
            "title": "MR",
            "firstname": customer['first'],
            "surname": customer['last'],
            "Country": '{}|{}'.format(profile['countryCode'].upper(), profile['country']),
            "pcSearch": profile['city'],
            "address1": profile['house'] + ' ' + profile['addressOne'],
            "address2": profile['addressTwo'],
            "address4": profile['city'],
            "address5": profile['region'],
            "postcode": profile['zip'],
            "rdAddSel": "Y",
            "del_title": "MR",
            "del_firstname": customer['first'],
            "del_surname": customer['last'],
            "del_Country": '{}|{}'.format(profile['countryCode'].upper(), profile['country']),
            "pcSearch2": "",
            "del_address1": "",
            "del_address2": "",
            "del_address4": "",
            "del_address5": "",
        }

        try:
            formPost = session.post('https://www.footasylum.com/page/yourdetails/',data=form)
        except (Exception, ConnectionError, ConnectionRefusedError, requests.exceptions.RequestException) as e:
            return None

        if formPost.status_code in [200,302]:
            logger.success(SITE,taskID,'Account Created!')
            discord.accountMade(
                webhook=loadSettings()["webhook"],
                site=SITE,
                first=customer["first"],
                last=customer["last"],
                email=customer["email"]
            )
            with open('./footasylum/accounts.txt','a') as accounts:
                accounts.write('\n{}:{}'.format(customer["email"],password))

            return 1
        else:
            return None
            



holypop_data = """
<option value="3" {{if countryId}}{{if countryId == '3'}}selected="selected"{{/if}}{{/if}}>Afghanistan</option>
<option value="15" {{if countryId}}{{if countryId == '15'}}selected="selected"{{/if}}{{/if}}>Åland Islands</option>
<option value="6" {{if countryId}}{{if countryId == '6'}}selected="selected"{{/if}}{{/if}}>Albania</option>
<option value="62" {{if countryId}}{{if countryId == '62'}}selected="selected"{{/if}}{{/if}}>Algeria</option>
<option value="1" {{if countryId}}{{if countryId == '1'}}selected="selected"{{/if}}{{/if}}>Andorra</option>
<option value="8" {{if countryId}}{{if countryId == '8'}}selected="selected"{{/if}}{{/if}}>Angola</option>
<option value="5" {{if countryId}}{{if countryId == '5'}}selected="selected"{{/if}}{{/if}}>Anguilla</option>
<option value="4" {{if countryId}}{{if countryId == '4'}}selected="selected"{{/if}}{{/if}}>Antigua and Barbuda</option>
<option value="10" {{if countryId}}{{if countryId == '10'}}selected="selected"{{/if}}{{/if}}>Argentina</option>
<option value="7" {{if countryId}}{{if countryId == '7'}}selected="selected"{{/if}}{{/if}}>Armenia</option>
<option value="14" {{if countryId}}{{if countryId == '14'}}selected="selected"{{/if}}{{/if}}>Aruba</option>
<option value="13" {{if countryId}}{{if countryId == '13'}}selected="selected"{{/if}}{{/if}}>Australia</option>
<option value="12" {{if countryId}}{{if countryId == '12'}}selected="selected"{{/if}}{{/if}}>Austria</option>
<option value="16" {{if countryId}}{{if countryId == '16'}}selected="selected"{{/if}}{{/if}}>Azerbaijan</option>
<option value="32" {{if countryId}}{{if countryId == '32'}}selected="selected"{{/if}}{{/if}}>Bahamas</option>
<option value="23" {{if countryId}}{{if countryId == '23'}}selected="selected"{{/if}}{{/if}}>Bahrain</option>
<option value="19" {{if countryId}}{{if countryId == '19'}}selected="selected"{{/if}}{{/if}}>Bangladesh</option>
<option value="18" {{if countryId}}{{if countryId == '18'}}selected="selected"{{/if}}{{/if}}>Barbados</option>
<option value="36" {{if countryId}}{{if countryId == '36'}}selected="selected"{{/if}}{{/if}}>Belarus</option>
<option value="20" {{if countryId}}{{if countryId == '20'}}selected="selected"{{/if}}{{/if}}>Belgium</option>
<option value="37" {{if countryId}}{{if countryId == '37'}}selected="selected"{{/if}}{{/if}}>Belize</option>
<option value="25" {{if countryId}}{{if countryId == '25'}}selected="selected"{{/if}}{{/if}}>Benin</option>
<option value="27" {{if countryId}}{{if countryId == '27'}}selected="selected"{{/if}}{{/if}}>Bermuda</option>
<option value="33" {{if countryId}}{{if countryId == '33'}}selected="selected"{{/if}}{{/if}}>Bhutan</option>
<option value="29" {{if countryId}}{{if countryId == '29'}}selected="selected"{{/if}}{{/if}}>Bolivia</option>
<option value="30" {{if countryId}}{{if countryId == '30'}}selected="selected"{{/if}}{{/if}}>Bonaire, Sint Eustatius and Saba</option>
<option value="17" {{if countryId}}{{if countryId == '17'}}selected="selected"{{/if}}{{/if}}>Bosnia and Herzegovina</option>
<option value="35" {{if countryId}}{{if countryId == '35'}}selected="selected"{{/if}}{{/if}}>Botswana</option>
<option value="31" {{if countryId}}{{if countryId == '31'}}selected="selected"{{/if}}{{/if}}>Brazil</option>
<option value="106" {{if countryId}}{{if countryId == '106'}}selected="selected"{{/if}}{{/if}}>British Indian Ocean Territory</option>
<option value="239" {{if countryId}}{{if countryId == '239'}}selected="selected"{{/if}}{{/if}}>British Virgin Islands</option>
<option value="28" {{if countryId}}{{if countryId == '28'}}selected="selected"{{/if}}{{/if}}>Brunei Darussalam</option>
<option value="22" {{if countryId}}{{if countryId == '22'}}selected="selected"{{/if}}{{/if}}>Bulgaria</option>
<option value="21" {{if countryId}}{{if countryId == '21'}}selected="selected"{{/if}}{{/if}}>Burkina Faso</option>
<option value="24" {{if countryId}}{{if countryId == '24'}}selected="selected"{{/if}}{{/if}}>Burundi</option>
<option value="117" {{if countryId}}{{if countryId == '117'}}selected="selected"{{/if}}{{/if}}>Cambodia</option>
<option value="47" {{if countryId}}{{if countryId == '47'}}selected="selected"{{/if}}{{/if}}>Cameroon</option>
<option value="38" {{if countryId}}{{if countryId == '38'}}selected="selected"{{/if}}{{/if}}>Canada</option>
<option value="52" {{if countryId}}{{if countryId == '52'}}selected="selected"{{/if}}{{/if}}>Cape Verde</option>
<option value="124" {{if countryId}}{{if countryId == '124'}}selected="selected"{{/if}}{{/if}}>Cayman Islands</option>
<option value="41" {{if countryId}}{{if countryId == '41'}}selected="selected"{{/if}}{{/if}}>Central African Republic</option>
<option value="215" {{if countryId}}{{if countryId == '215'}}selected="selected"{{/if}}{{/if}}>Chad</option>
<option value="46" {{if countryId}}{{if countryId == '46'}}selected="selected"{{/if}}{{/if}}>Chile</option>
<option value="48" {{if countryId}}{{if countryId == '48'}}selected="selected"{{/if}}{{/if}}>China</option>
<option value="54" {{if countryId}}{{if countryId == '54'}}selected="selected"{{/if}}{{/if}}>Christmas Island</option>
<option value="39" {{if countryId}}{{if countryId == '39'}}selected="selected"{{/if}}{{/if}}>Cocos (Keeling) Islands</option>
<option value="49" {{if countryId}}{{if countryId == '49'}}selected="selected"{{/if}}{{/if}}>Colombia</option>
<option value="119" {{if countryId}}{{if countryId == '119'}}selected="selected"{{/if}}{{/if}}>Comoros</option>
<option value="40" {{if countryId}}{{if countryId == '40'}}selected="selected"{{/if}}{{/if}}>Congo</option>
<option value="42" {{if countryId}}{{if countryId == '42'}}selected="selected"{{/if}}{{/if}}>Congo</option>
<option value="45" {{if countryId}}{{if countryId == '45'}}selected="selected"{{/if}}{{/if}}>Cook Islands</option>
<option value="50" {{if countryId}}{{if countryId == '50'}}selected="selected"{{/if}}{{/if}}>Costa Rica</option>
<option value="44" {{if countryId}}{{if countryId == '44'}}selected="selected"{{/if}}{{/if}}>Cote d'Ivoire</option>
<option value="98" {{if countryId}}{{if countryId == '98'}}selected="selected"{{/if}}{{/if}}>Croatia</option>
<option value="51" {{if countryId}}{{if countryId == '51'}}selected="selected"{{/if}}{{/if}}>Cuba</option>
<option value="53" {{if countryId}}{{if countryId == '53'}}selected="selected"{{/if}}{{/if}}>Curaçao</option>
<option value="55" {{if countryId}}{{if countryId == '55'}}selected="selected"{{/if}}{{/if}}>Cyprus</option>
<option value="56" {{if countryId}}{{if countryId == '56'}}selected="selected"{{/if}}{{/if}}>Czech Republic</option>
<option value="59" {{if countryId}}{{if countryId == '59'}}selected="selected"{{/if}}{{/if}}>Denmark</option>
<option value="58" {{if countryId}}{{if countryId == '58'}}selected="selected"{{/if}}{{/if}}>Djibouti</option>
<option value="60" {{if countryId}}{{if countryId == '60'}}selected="selected"{{/if}}{{/if}}>Dominica</option>
<option value="61" {{if countryId}}{{if countryId == '61'}}selected="selected"{{/if}}{{/if}}>Dominican Republic</option>
<option value="63" {{if countryId}}{{if countryId == '63'}}selected="selected"{{/if}}{{/if}}>Ecuador</option>
<option value="65" {{if countryId}}{{if countryId == '65'}}selected="selected"{{/if}}{{/if}}>Egypt</option>
<option value="210" {{if countryId}}{{if countryId == '210'}}selected="selected"{{/if}}{{/if}}>El Salvador</option>
<option value="88" {{if countryId}}{{if countryId == '88'}}selected="selected"{{/if}}{{/if}}>Equatorial Guinea</option>
<option value="67" {{if countryId}}{{if countryId == '67'}}selected="selected"{{/if}}{{/if}}>Eritrea</option>
<option value="64" {{if countryId}}{{if countryId == '64'}}selected="selected"{{/if}}{{/if}}>Estonia</option>
<option value="69" {{if countryId}}{{if countryId == '69'}}selected="selected"{{/if}}{{/if}}>Ethiopia</option>
<option value="72" {{if countryId}}{{if countryId == '72'}}selected="selected"{{/if}}{{/if}}>Falkland Islands (Malvinas)</option>
<option value="74" {{if countryId}}{{if countryId == '74'}}selected="selected"{{/if}}{{/if}}>Faroe Islands</option>
<option value="71" {{if countryId}}{{if countryId == '71'}}selected="selected"{{/if}}{{/if}}>Fiji</option>
<option value="70" {{if countryId}}{{if countryId == '70'}}selected="selected"{{/if}}{{/if}}>Finland</option>
<option value="75" {{if countryId}}{{if countryId == '75'}}selected="selected"{{/if}}{{/if}}>France</option>
<option value="80" {{if countryId}}{{if countryId == '80'}}selected="selected"{{/if}}{{/if}}>French Guiana</option>
<option value="175" {{if countryId}}{{if countryId == '175'}}selected="selected"{{/if}}{{/if}}>French Polynesia</option>
<option value="76" {{if countryId}}{{if countryId == '76'}}selected="selected"{{/if}}{{/if}}>Gabon</option>
<option value="85" {{if countryId}}{{if countryId == '85'}}selected="selected"{{/if}}{{/if}}>Gambia</option>
<option value="79" {{if countryId}}{{if countryId == '79'}}selected="selected"{{/if}}{{/if}}>Georgia</option>
<option value="57" {{if countryId}}{{if countryId == '57'}}selected="selected"{{/if}}{{/if}}>Germany</option>
<option value="82" {{if countryId}}{{if countryId == '82'}}selected="selected"{{/if}}{{/if}}>Ghana</option>
<option value="83" {{if countryId}}{{if countryId == '83'}}selected="selected"{{/if}}{{/if}}>Gibraltar</option>
<option value="89" {{if countryId}}{{if countryId == '89'}}selected="selected"{{/if}}{{/if}}>Greece</option>
<option value="84" {{if countryId}}{{if countryId == '84'}}selected="selected"{{/if}}{{/if}}>Greenland</option>
<option value="78" {{if countryId}}{{if countryId == '78'}}selected="selected"{{/if}}{{/if}}>Grenada</option>
<option value="87" {{if countryId}}{{if countryId == '87'}}selected="selected"{{/if}}{{/if}}>Guadeloupe</option>
<option value="92" {{if countryId}}{{if countryId == '92'}}selected="selected"{{/if}}{{/if}}>Guam</option>
<option value="91" {{if countryId}}{{if countryId == '91'}}selected="selected"{{/if}}{{/if}}>Guatemala</option>
<option value="81" {{if countryId}}{{if countryId == '81'}}selected="selected"{{/if}}{{/if}}>Guernsey</option>
<option value="86" {{if countryId}}{{if countryId == '86'}}selected="selected"{{/if}}{{/if}}>Guinea</option>
<option value="93" {{if countryId}}{{if countryId == '93'}}selected="selected"{{/if}}{{/if}}>Guinea-Bissau</option>
<option value="94" {{if countryId}}{{if countryId == '94'}}selected="selected"{{/if}}{{/if}}>Guyana</option>
<option value="99" {{if countryId}}{{if countryId == '99'}}selected="selected"{{/if}}{{/if}}>Haiti</option>
<option value="236" {{if countryId}}{{if countryId == '236'}}selected="selected"{{/if}}{{/if}}>Holy See (Vatican City State)</option>
<option value="97" {{if countryId}}{{if countryId == '97'}}selected="selected"{{/if}}{{/if}}>Honduras</option>
<option value="95" {{if countryId}}{{if countryId == '95'}}selected="selected"{{/if}}{{/if}}>Hong Kong</option>
<option value="100" {{if countryId}}{{if countryId == '100'}}selected="selected"{{/if}}{{/if}}>Hungary</option>
<option value="109" {{if countryId}}{{if countryId == '109'}}selected="selected"{{/if}}{{/if}}>Iceland</option>
<option value="105" {{if countryId}}{{if countryId == '105'}}selected="selected"{{/if}}{{/if}}>India</option>
<option value="101" {{if countryId}}{{if countryId == '101'}}selected="selected"{{/if}}{{/if}}>Indonesia</option>
<option value="108" {{if countryId}}{{if countryId == '108'}}selected="selected"{{/if}}{{/if}}>Iran</option>
<option value="107" {{if countryId}}{{if countryId == '107'}}selected="selected"{{/if}}{{/if}}>Iraq</option>
<option value="102" {{if countryId}}{{if countryId == '102'}}selected="selected"{{/if}}{{/if}}>Ireland</option>
<option value="104" {{if countryId}}{{if countryId == '104'}}selected="selected"{{/if}}{{/if}}>Isle of Man</option>
<option value="103" {{if countryId}}{{if countryId == '103'}}selected="selected"{{/if}}{{/if}}>Israel</option>
<option value="110" {{if countryId}}{{if countryId == '110'}}selected="selected"{{/if}}{{/if}}>Italia</option>
<option value="112" {{if countryId}}{{if countryId == '112'}}selected="selected"{{/if}}{{/if}}>Jamaica</option>
<option value="114" {{if countryId}}{{if countryId == '114'}}selected="selected"{{/if}}{{/if}}>Japan</option>
<option value="111" {{if countryId}}{{if countryId == '111'}}selected="selected"{{/if}}{{/if}}>Jersey</option>
<option value="113" {{if countryId}}{{if countryId == '113'}}selected="selected"{{/if}}{{/if}}>Jordan</option>
<option value="125" {{if countryId}}{{if countryId == '125'}}selected="selected"{{/if}}{{/if}}>Kazakhstan</option>
<option value="115" {{if countryId}}{{if countryId == '115'}}selected="selected"{{/if}}{{/if}}>Kenya</option>
<option value="118" {{if countryId}}{{if countryId == '118'}}selected="selected"{{/if}}{{/if}}>Kiribati</option>
<option value="255" {{if countryId}}{{if countryId == '255'}}selected="selected"{{/if}}{{/if}}>Kosovo</option>
<option value="123" {{if countryId}}{{if countryId == '123'}}selected="selected"{{/if}}{{/if}}>Kuwait</option>
<option value="116" {{if countryId}}{{if countryId == '116'}}selected="selected"{{/if}}{{/if}}>Kyrgyz Republic</option>
<option value="126" {{if countryId}}{{if countryId == '126'}}selected="selected"{{/if}}{{/if}}>Laos</option>
<option value="135" {{if countryId}}{{if countryId == '135'}}selected="selected"{{/if}}{{/if}}>Latvia</option>
<option value="127" {{if countryId}}{{if countryId == '127'}}selected="selected"{{/if}}{{/if}}>Lebanon</option>
<option value="132" {{if countryId}}{{if countryId == '132'}}selected="selected"{{/if}}{{/if}}>Lesotho</option>
<option value="131" {{if countryId}}{{if countryId == '131'}}selected="selected"{{/if}}{{/if}}>Liberia</option>
<option value="136" {{if countryId}}{{if countryId == '136'}}selected="selected"{{/if}}{{/if}}>Libya</option>
<option value="129" {{if countryId}}{{if countryId == '129'}}selected="selected"{{/if}}{{/if}}>Liechtenstein</option>
<option value="133" {{if countryId}}{{if countryId == '133'}}selected="selected"{{/if}}{{/if}}>Lithuania</option>
<option value="134" {{if countryId}}{{if countryId == '134'}}selected="selected"{{/if}}{{/if}}>Luxembourg</option>
<option value="148" {{if countryId}}{{if countryId == '148'}}selected="selected"{{/if}}{{/if}}>Macao</option>
<option value="144" {{if countryId}}{{if countryId == '144'}}selected="selected"{{/if}}{{/if}}>Macedonia</option>
<option value="142" {{if countryId}}{{if countryId == '142'}}selected="selected"{{/if}}{{/if}}>Madagascar</option>
<option value="156" {{if countryId}}{{if countryId == '156'}}selected="selected"{{/if}}{{/if}}>Malawi</option>
<option value="158" {{if countryId}}{{if countryId == '158'}}selected="selected"{{/if}}{{/if}}>Malaysia</option>
<option value="155" {{if countryId}}{{if countryId == '155'}}selected="selected"{{/if}}{{/if}}>Maldives</option>
<option value="145" {{if countryId}}{{if countryId == '145'}}selected="selected"{{/if}}{{/if}}>Mali</option>
<option value="153" {{if countryId}}{{if countryId == '153'}}selected="selected"{{/if}}{{/if}}>Malta</option>
<option value="143" {{if countryId}}{{if countryId == '143'}}selected="selected"{{/if}}{{/if}}>Marshall Islands</option>
<option value="150" {{if countryId}}{{if countryId == '150'}}selected="selected"{{/if}}{{/if}}>Martinique</option>
<option value="151" {{if countryId}}{{if countryId == '151'}}selected="selected"{{/if}}{{/if}}>Mauritania</option>
<option value="154" {{if countryId}}{{if countryId == '154'}}selected="selected"{{/if}}{{/if}}>Mauritius</option>
<option value="246" {{if countryId}}{{if countryId == '246'}}selected="selected"{{/if}}{{/if}}>Mayotte</option>
<option value="157" {{if countryId}}{{if countryId == '157'}}selected="selected"{{/if}}{{/if}}>Mexico</option>
<option value="73" {{if countryId}}{{if countryId == '73'}}selected="selected"{{/if}}{{/if}}>Micronesia</option>
<option value="139" {{if countryId}}{{if countryId == '139'}}selected="selected"{{/if}}{{/if}}>Moldova</option>
<option value="138" {{if countryId}}{{if countryId == '138'}}selected="selected"{{/if}}{{/if}}>Monaco</option>
<option value="147" {{if countryId}}{{if countryId == '147'}}selected="selected"{{/if}}{{/if}}>Mongolia</option>
<option value="140" {{if countryId}}{{if countryId == '140'}}selected="selected"{{/if}}{{/if}}>Montenegro</option>
<option value="152" {{if countryId}}{{if countryId == '152'}}selected="selected"{{/if}}{{/if}}>Montserrat</option>
<option value="137" {{if countryId}}{{if countryId == '137'}}selected="selected"{{/if}}{{/if}}>Morocco</option>
<option value="159" {{if countryId}}{{if countryId == '159'}}selected="selected"{{/if}}{{/if}}>Mozambique</option>
<option value="146" {{if countryId}}{{if countryId == '146'}}selected="selected"{{/if}}{{/if}}>Myanmar</option>
<option value="160" {{if countryId}}{{if countryId == '160'}}selected="selected"{{/if}}{{/if}}>Namibia</option>
<option value="169" {{if countryId}}{{if countryId == '169'}}selected="selected"{{/if}}{{/if}}>Nauru</option>
<option value="168" {{if countryId}}{{if countryId == '168'}}selected="selected"{{/if}}{{/if}}>Nepal</option>
<option value="166" {{if countryId}}{{if countryId == '166'}}selected="selected"{{/if}}{{/if}}>Netherlands</option>
<option value="161" {{if countryId}}{{if countryId == '161'}}selected="selected"{{/if}}{{/if}}>New Caledonia</option>
<option value="171" {{if countryId}}{{if countryId == '171'}}selected="selected"{{/if}}{{/if}}>New Zealand</option>
<option value="165" {{if countryId}}{{if countryId == '165'}}selected="selected"{{/if}}{{/if}}>Nicaragua</option>
<option value="162" {{if countryId}}{{if countryId == '162'}}selected="selected"{{/if}}{{/if}}>Niger</option>
<option value="164" {{if countryId}}{{if countryId == '164'}}selected="selected"{{/if}}{{/if}}>Nigeria</option>
<option value="170" {{if countryId}}{{if countryId == '170'}}selected="selected"{{/if}}{{/if}}>Niue</option>
<option value="163" {{if countryId}}{{if countryId == '163'}}selected="selected"{{/if}}{{/if}}>Norfolk Island</option>
<option value="257" {{if countryId}}{{if countryId == '257'}}selected="selected"{{/if}}{{/if}}>Norhtern Ireland</option>
<option value="121" {{if countryId}}{{if countryId == '121'}}selected="selected"{{/if}}{{/if}}>North Korea</option>
<option value="149" {{if countryId}}{{if countryId == '149'}}selected="selected"{{/if}}{{/if}}>Northern Mariana Islands</option>
<option value="167" {{if countryId}}{{if countryId == '167'}}selected="selected"{{/if}}{{/if}}>Norway</option>
<option value="172" {{if countryId}}{{if countryId == '172'}}selected="selected"{{/if}}{{/if}}>Oman</option>
<option value="178" {{if countryId}}{{if countryId == '178'}}selected="selected"{{/if}}{{/if}}>Pakistan</option>
<option value="185" {{if countryId}}{{if countryId == '185'}}selected="selected"{{/if}}{{/if}}>Palau</option>
<option value="183" {{if countryId}}{{if countryId == '183'}}selected="selected"{{/if}}{{/if}}>Palestine</option>
<option value="173" {{if countryId}}{{if countryId == '173'}}selected="selected"{{/if}}{{/if}}>Panama</option>
<option value="176" {{if countryId}}{{if countryId == '176'}}selected="selected"{{/if}}{{/if}}>Papua New Guinea</option>
<option value="186" {{if countryId}}{{if countryId == '186'}}selected="selected"{{/if}}{{/if}}>Paraguay</option>
<option value="174" {{if countryId}}{{if countryId == '174'}}selected="selected"{{/if}}{{/if}}>Peru</option>
<option value="177" {{if countryId}}{{if countryId == '177'}}selected="selected"{{/if}}{{/if}}>Philippines</option>
<option value="181" {{if countryId}}{{if countryId == '181'}}selected="selected"{{/if}}{{/if}}>Pitcairn Islands</option>
<option value="179" {{if countryId}}{{if countryId == '179'}}selected="selected"{{/if}}{{/if}}>Poland</option>
<option value="184" {{if countryId}}{{if countryId == '184'}}selected="selected"{{/if}}{{/if}}>Portugal</option>
<option value="253" {{if countryId}}{{if countryId == '253'}}selected="selected"{{/if}}{{/if}}>Portugal (Azzorre)</option>
<option value="252" {{if countryId}}{{if countryId == '252'}}selected="selected"{{/if}}{{/if}}>Portugal (Madeira)</option>
<option value="182" {{if countryId}}{{if countryId == '182'}}selected="selected"{{/if}}{{/if}}>Puerto Rico</option>
<option value="187" {{if countryId}}{{if countryId == '187'}}selected="selected"{{/if}}{{/if}}>Qatar</option>
<option value="188" {{if countryId}}{{if countryId == '188'}}selected="selected"{{/if}}{{/if}}>Réunion</option>
<option value="189" {{if countryId}}{{if countryId == '189'}}selected="selected"{{/if}}{{/if}}>Romania</option>
<option value="191" {{if countryId}}{{if countryId == '191'}}selected="selected"{{/if}}{{/if}}>Russian Federation</option>
<option value="192" {{if countryId}}{{if countryId == '192'}}selected="selected"{{/if}}{{/if}}>Rwanda</option>
<option value="26" {{if countryId}}{{if countryId == '26'}}selected="selected"{{/if}}{{/if}}>Saint Barthélemy</option>
<option value="199" {{if countryId}}{{if countryId == '199'}}selected="selected"{{/if}}{{/if}}>Saint Helena, Ascension and Tristan da Cunha</option>
<option value="120" {{if countryId}}{{if countryId == '120'}}selected="selected"{{/if}}{{/if}}>Saint Kitts and Nevis</option>
<option value="128" {{if countryId}}{{if countryId == '128'}}selected="selected"{{/if}}{{/if}}>Saint Lucia</option>
<option value="141" {{if countryId}}{{if countryId == '141'}}selected="selected"{{/if}}{{/if}}>Saint Martin</option>
<option value="180" {{if countryId}}{{if countryId == '180'}}selected="selected"{{/if}}{{/if}}>Saint Pierre and Miquelon</option>
<option value="237" {{if countryId}}{{if countryId == '237'}}selected="selected"{{/if}}{{/if}}>Saint Vincent and the Grenadines</option>
<option value="244" {{if countryId}}{{if countryId == '244'}}selected="selected"{{/if}}{{/if}}>Samoa</option>
<option value="204" {{if countryId}}{{if countryId == '204'}}selected="selected"{{/if}}{{/if}}>San Marino</option>
<option value="209" {{if countryId}}{{if countryId == '209'}}selected="selected"{{/if}}{{/if}}>Sao Tome and Principe</option>
<option value="193" {{if countryId}}{{if countryId == '193'}}selected="selected"{{/if}}{{/if}}>Saudi Arabia</option>
<option value="205" {{if countryId}}{{if countryId == '205'}}selected="selected"{{/if}}{{/if}}>Senegal</option>
<option value="190" {{if countryId}}{{if countryId == '190'}}selected="selected"{{/if}}{{/if}}>Serbia</option>
<option value="195" {{if countryId}}{{if countryId == '195'}}selected="selected"{{/if}}{{/if}}>Seychelles</option>
<option value="203" {{if countryId}}{{if countryId == '203'}}selected="selected"{{/if}}{{/if}}>Sierra Leone</option>
<option value="198" {{if countryId}}{{if countryId == '198'}}selected="selected"{{/if}}{{/if}}>Singapore</option>
<option value="211" {{if countryId}}{{if countryId == '211'}}selected="selected"{{/if}}{{/if}}>Sint Maarten (Dutch part)</option>
<option value="202" {{if countryId}}{{if countryId == '202'}}selected="selected"{{/if}}{{/if}}>Slovakia</option>
<option value="200" {{if countryId}}{{if countryId == '200'}}selected="selected"{{/if}}{{/if}}>Slovenia</option>
<option value="194" {{if countryId}}{{if countryId == '194'}}selected="selected"{{/if}}{{/if}}>Solomon Islands</option>
<option value="206" {{if countryId}}{{if countryId == '206'}}selected="selected"{{/if}}{{/if}}>Somalia</option>
<option value="247" {{if countryId}}{{if countryId == '247'}}selected="selected"{{/if}}{{/if}}>South Africa</option>
<option value="122" {{if countryId}}{{if countryId == '122'}}selected="selected"{{/if}}{{/if}}>South Korea</option>
<option value="208" {{if countryId}}{{if countryId == '208'}}selected="selected"{{/if}}{{/if}}>South Sudan</option>
<option value="68" {{if countryId}}{{if countryId == '68'}}selected="selected"{{/if}}{{/if}}>Spain</option>
<option value="254" {{if countryId}}{{if countryId == '254'}}selected="selected"{{/if}}{{/if}}>Spain (Canarias)</option>
<option value="250" {{if countryId}}{{if countryId == '250'}}selected="selected"{{/if}}{{/if}}>Spain (Ceuta)</option>
<option value="251" {{if countryId}}{{if countryId == '251'}}selected="selected"{{/if}}{{/if}}>Spain (Melilla)</option>
<option value="130" {{if countryId}}{{if countryId == '130'}}selected="selected"{{/if}}{{/if}}>Sri Lanka</option>
<option value="196" {{if countryId}}{{if countryId == '196'}}selected="selected"{{/if}}{{/if}}>Sudan</option>
<option value="207" {{if countryId}}{{if countryId == '207'}}selected="selected"{{/if}}{{/if}}>Suriname</option>
<option value="213" {{if countryId}}{{if countryId == '213'}}selected="selected"{{/if}}{{/if}}>Swaziland</option>
<option value="197" {{if countryId}}{{if countryId == '197'}}selected="selected"{{/if}}{{/if}}>Sweden</option>
<option value="43" {{if countryId}}{{if countryId == '43'}}selected="selected"{{/if}}{{/if}}>Switzerland</option>
<option value="212" {{if countryId}}{{if countryId == '212'}}selected="selected"{{/if}}{{/if}}>Syria</option>
<option value="228" {{if countryId}}{{if countryId == '228'}}selected="selected"{{/if}}{{/if}}>Taiwan</option>
<option value="219" {{if countryId}}{{if countryId == '219'}}selected="selected"{{/if}}{{/if}}>Tajikistan</option>
<option value="229" {{if countryId}}{{if countryId == '229'}}selected="selected"{{/if}}{{/if}}>Tanzania</option>
<option value="218" {{if countryId}}{{if countryId == '218'}}selected="selected"{{/if}}{{/if}}>Thailand</option>
<option value="221" {{if countryId}}{{if countryId == '221'}}selected="selected"{{/if}}{{/if}}>Timor-Leste</option>
<option value="217" {{if countryId}}{{if countryId == '217'}}selected="selected"{{/if}}{{/if}}>Togo</option>
<option value="220" {{if countryId}}{{if countryId == '220'}}selected="selected"{{/if}}{{/if}}>Tokelau</option>
<option value="224" {{if countryId}}{{if countryId == '224'}}selected="selected"{{/if}}{{/if}}>Tonga</option>
<option value="226" {{if countryId}}{{if countryId == '226'}}selected="selected"{{/if}}{{/if}}>Trinidad and Tobago</option>
<option value="223" {{if countryId}}{{if countryId == '223'}}selected="selected"{{/if}}{{/if}}>Tunisia</option>
<option value="225" {{if countryId}}{{if countryId == '225'}}selected="selected"{{/if}}{{/if}}>Turkey</option>
<option value="222" {{if countryId}}{{if countryId == '222'}}selected="selected"{{/if}}{{/if}}>Turkmenistan</option>
<option value="214" {{if countryId}}{{if countryId == '214'}}selected="selected"{{/if}}{{/if}}>Turks and Caicos Islands</option>
<option value="227" {{if countryId}}{{if countryId == '227'}}selected="selected"{{/if}}{{/if}}>Tuvalu</option>
<option value="231" {{if countryId}}{{if countryId == '231'}}selected="selected"{{/if}}{{/if}}>Uganda</option>
<option value="230" {{if countryId}}{{if countryId == '230'}}selected="selected"{{/if}}{{/if}}>Ukraine</option>
<option value="2" {{if countryId}}{{if countryId == '2'}}selected="selected"{{/if}}{{/if}}>United Arab Emirates</option>
<option value="77" {{if countryId}}{{if countryId == '77'}}selected="selected"{{/if}}{{/if}}>United Kingdom</option>
<option value="233" {{if countryId}}{{if countryId == '233'}}selected="selected"{{/if}}{{/if}}>United States</option>
<option value="232" {{if countryId}}{{if countryId == '232'}}selected="selected"{{/if}}{{/if}}>United States Minor Outlying Islands</option>
<option value="240" {{if countryId}}{{if countryId == '240'}}selected="selected"{{/if}}{{/if}}>United States Virgin Islands</option>
<option value="234" {{if countryId}}{{if countryId == '234'}}selected="selected"{{/if}}{{/if}}>Uruguay</option>
<option value="235" {{if countryId}}{{if countryId == '235'}}selected="selected"{{/if}}{{/if}}>Uzbekistan</option>
<option value="242" {{if countryId}}{{if countryId == '242'}}selected="selected"{{/if}}{{/if}}>Vanuatu</option>
<option value="238" {{if countryId}}{{if countryId == '238'}}selected="selected"{{/if}}{{/if}}>Venezuela</option>
<option value="241" {{if countryId}}{{if countryId == '241'}}selected="selected"{{/if}}{{/if}}>Vietnam</option>
<option value="243" {{if countryId}}{{if countryId == '243'}}selected="selected"{{/if}}{{/if}}>Wallis and Futuna</option>
<option value="256" {{if countryId}}{{if countryId == '256'}}selected="selected"{{/if}}{{/if}}>West Bank and Gaza</option>
<option value="245" {{if countryId}}{{if countryId == '245'}}selected="selected"{{/if}}{{/if}}>Yemen</option>
<option value="248" {{if countryId}}{{if countryId == '248'}}selected="selected"{{/if}}{{/if}}>Zambia</option>
<option value="249" {{if countryId}}{{if countryId == '249'}}selected="selected"{{/if}}{{/if}}>Zimbabwe</option>
"""

prodirect_data = """
<select name="ddlCountry" id="ddlCountry" class="">
<option value="0">Please Select</option>
<option value="4">Afghanistan</option>
<option value="248">Åland Islands</option>
<option value="8">Albania</option>
<option value="12">Algeria</option>
<option value="16">American Samoa</option>
<option value="20">Andorra</option>
<option value="24">Angola</option>
<option value="660">Anguilla</option>
<option value="10">Antarctica</option>
<option value="28">Antigua and Barbuda</option>
<option value="32">Argentina</option>
<option value="51">Armenia</option>
<option value="533">Aruba</option>
<option value="36">Australia</option>
<option value="40">Austria</option>
<option value="31">Azerbaijan</option>
<option value="44">Bahamas</option>
<option value="48">Bahrain</option>
<option value="50">Bangladesh</option>
<option value="52">Barbados</option>
<option value="112">Belarus</option>
<option value="56">Belgium</option>
<option value="84">Belize</option>
<option value="204">Benin</option>
<option value="60">Bermuda</option>
<option value="64">Bhutan</option>
<option value="68">Bolivia</option>
<option value="535">Bonaire, Sint Eustatius and Saba</option>
<option value="70">Bosnia and Herzegovina</option>
<option value="72">Botswana</option>
<option value="74">Bouvet Island</option>
<option value="76">Brazil</option>
<option value="86">British Indian Ocean Territory</option>
<option value="92">British Virgin Islands</option>
<option value="96">Brunei</option>
<option value="100">Bulgaria</option>
<option value="854">Burkina Faso</option>
<option value="108">Burundi</option>
<option value="116">Cambodia</option>
<option value="120">Cameroon</option>
<option value="124">Canada</option>
<option value="132">Cape Verde</option>
<option value="136">Cayman Islands</option>
<option value="140">Central African Republic</option>
<option value="148">Chad</option>
<option value="152">Chile</option>
<option value="156">China</option>
<option value="162">Christmas Island</option>
<option value="166">Cocos (Keeling) Islands</option>
<option value="170">Colombia</option>
<option value="174">Comoros</option>
<option value="178">Congo - Democratic Republic of (Zaire)</option>
<option value="180">Congo - Republic of </option>
<option value="188">Costa Rica</option>
<option value="384">Cote D’Ivoire</option>
<option value="191">Croatia</option>
<option value="192">Cuba</option>
<option value="531">Curaçao</option>
<option value="196">Cyprus</option>
<option value="203">Czech Republic</option>
<option value="208">Denmark</option>
<option value="262">Djibouti</option>
<option value="212">Dominica</option>
<option value="214">Dominican Republic</option>
<option value="626">East Timor</option>
<option value="218">Ecuador</option>
<option value="818">Egypt</option>
<option value="222">El Salvador</option>
<option value="226">Equatorial Guinea</option>
<option value="232">Eritrea</option>
<option value="233">Estonia</option>
<option value="231">Ethiopia</option>
<option value="238">Falkland Islands</option>
<option value="234">Faroe Islands</option>
<option value="583">Federated States of Micronesia</option>
<option value="242">Fiji</option>
<option value="246">Finland</option>
<option value="254">France (French Guiana)</option>
<option value="258">France (French Polynesia)</option>
<option value="312">France (Guadeloupe)</option>
<option value="250">France (Mainland)</option>
<option value="474">France (Martinique)</option>
<option value="175">France (Mayotte)</option>
<option value="540">France (New Caledonia)</option>
<option value="638">France (Reunion)</option>
<option value="666">France (Saint Pierre and Miquelon)</option>
<option value="260">France (Southern Territories)</option>
<option value="652">France (St. Barthelemy)</option>
<option value="876">France (Wallis and Futuna)</option>
<option value="663">France (Saint-Martin)</option>
<option value="266">Gabon</option>
<option value="270">Gambia</option>
<option value="268">Georgia</option>
<option value="276">Germany</option>
<option value="288">Ghana</option>
<option value="292">Gibraltar</option>
<option value="300">Greece</option>
<option value="304">Greenland</option>
<option value="308">Grenada</option>
<option value="316">Guam</option>
<option value="320">Guatemala</option>
<option value="831">Guernsey</option>
<option value="324">Guinea</option>
<option value="624">Guinea-Bissau</option>
<option value="328">Guyana</option>
<option value="332">Haiti</option>
<option value="334">Heard Island and McDonald Islands</option>
<option value="340">Honduras</option>
<option value="344">Hong Kong</option>
<option value="348">Hungary</option>
<option value="352">Iceland</option>
<option value="356">India</option>
<option value="360">Indonesia</option>
<option value="364">Iran</option>
<option value="368">Iraq</option>
<option value="372">Ireland</option>
<option value="833">Isle of Man</option>
<option value="376">Israel</option>
<option value="380">Italy</option>
<option value="388">Jamaica</option>
<option value="392">Japan</option>
<option value="832">Jersey</option>
<option value="400">Jordan</option>
<option value="398">Kazakhstan</option>
<option value="404">Kenya</option>
<option value="296">Kiribat</option>
<option value="414">Kuwait</option>
<option value="417">Kyrgyzstan</option>
<option value="418">Laos</option>
<option value="428">Latvia</option>
<option value="422">Lebanon</option>
<option value="426">Lesotho</option>
<option value="430">Liberia</option>
<option value="434">Libya</option>
<option value="438">Liechtenstein</option>
<option value="440">Lithuania</option>
<option value="442">Luxembourg</option>
<option value="446">Macau</option>
<option value="807">Macedonia</option>
<option value="450">Madagascar</option>
<option value="454">Malawi</option>
<option value="458">Malaysia</option>
<option value="462">Maldives</option>
<option value="466">Mali</option>
<option value="470">Malta</option>
<option value="584">Marshall Islands</option>
<option value="478">Mauritania</option>
<option value="480">Mauritius</option>
<option value="484">Mexico</option>
<option value="498">Moldova</option>
<option value="492">Monaco</option>
<option value="496">Mongolia</option>
<option value="499">Montenegro</option>
<option value="500">Montserrat</option>
<option value="504">Morocco</option>
<option value="508">Mozambique</option>
<option value="104">Myanmar</option>
<option value="516">Namibia</option>
<option value="520">Nauru</option>
<option value="524">Nepal</option>
<option value="528">Netherlands</option>
<option value="554">New Zealand</option>
<option value="184">New Zealand (Cook Islands)</option>
<option value="558">Nicaragua</option>
<option value="562">Niger</option>
<option value="566">Nigeria</option>
<option value="570">Niue</option>
<option value="574">Norfolk Island</option>
<option value="408">North Korea</option>
<option value="580">Northern Mariana Islands</option>
<option value="578">Norway</option>
<option value="744">Norway (Svalbard and Jan Mayen)</option>
<option value="512">Oman</option>
<option value="586">Pakistan</option>
<option value="585">Palau</option>
<option value="275">Palestine, State of</option>
<option value="591">Panama</option>
<option value="598">Papua New Guinea</option>
<option value="600">Paraguay</option>
<option value="604">Peru</option>
<option value="608">Philippines</option>
<option value="612">Pitcairn</option>
<option value="616">Poland</option>
<option value="620">Portugal</option>
<option value="630">Puerto Rico</option>
<option value="634">Qatar</option>
<option value="642">Romania</option>
<option value="643">Russia</option>
<option value="646">Rwanda</option>
<option value="882">Samoa</option>
<option value="674">San Marino</option>
<option value="678">Sao Tome and Principe</option>
<option value="682">Saudi Arabia</option>
<option value="686">Senegal</option>
<option value="688">Serbia</option>
<option value="690">Seychelles</option>
<option value="694">Sierra Leone</option>
<option value="702">Singapore</option>
<option value="534">Sint Maarten (Dutch part)</option>
<option value="703">Slovakia</option>
<option value="705">Slovenia</option>
<option value="90">Solomon Islands</option>
<option value="706">Somalia</option>
<option value="710">South Africa</option>
<option value="239">South Georgia and the South Sandwich Islands</option>
<option value="410">South Korea</option>
<option value="728">South Sudan</option>
<option value="724">Spain (Mainland and Balearic Islands)</option>
<option value="144">Sri Lanka</option>
<option value="654">St. Helena</option>
<option value="659">St. Kitts and Nevis</option>
<option value="662">St. Lucia</option>
<option value="670">St. Vincent and the Grenadines</option>
<option value="729">Sudan</option>
<option value="740">Suriname</option>
<option value="748">Swaziland</option>
<option value="752">Sweden</option>
<option value="756">Switzerland</option>
<option value="760">Syria</option>
<option value="158">Taiwan</option>
<option value="762">Tajikistan</option>
<option value="834">Tanzania</option>
<option value="764">Thailand</option>
<option value="768">Togo</option>
<option value="772">Tokelau</option>
<option value="776">Tonga</option>
<option value="780">Trinidad and Tobago</option>
<option value="788">Tunisia</option>
<option value="792">Turkey</option>
<option value="795">Turkmenistan</option>
<option value="796">Turks and Caicos Islands</option>
<option value="798">Tuvalu</option>
<option value="850">U.S. Virgin Islands</option>
<option value="800">Uganda</option>
<option value="804">Ukraine</option>
<option value="784">United Arab Emirates</option>
<option value="826">United Kingdom</option>
<option value="840">United States</option>
<option value="581">United States Minor Outlying Islands</option>
<option value="858">Uruguay</option>
<option value="860">Uzbekistan</option>
<option value="548">Vanuatu</option>
<option value="336">Vatican City</option>
<option value="862">Venezuela</option>
<option value="704">Vietnam</option>
<option value="732">Western Sahara</option>
<option value="887">Yemen</option>
<option value="894">Zambia</option>
<option value="716">Zimbabwe</option>
</select>
"""