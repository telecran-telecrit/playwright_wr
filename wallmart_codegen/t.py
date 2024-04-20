'''
$cd /c/Program Files/Google/Chrome/Application/
$mv 109.0.5414.120 123.0.6312.132
$cp -a 123.0.6312.132/109.0.5414.120.manifest 123.0.6312.132/123.0.6312.132.manifest
$sed -bi 's/109\.0\.5414\.120/123\.0\.6312\.132/g' "123.0.6312.132/123.0.6312.132.manifest"
$grep -ERn '123\.0\.6312\.132' /c/Program\ Files/Google/Chrome/Application/ | grep chrom
$sed -bi 's/109\.0\.5414\.120/123\.0\.6312\.132/g' "/c/Program Files/Google/Chrome/Application/chrome.exe"
$sed -bi 's/109\.0\.5414\.120/123\.0\.6312\.132/g' "/c/Program Files/Google/Chrome/Application/123.0.6312.132/chrome.dll"
$sed -bi 's/109\.0\.5414\.120/123\.0\.6312\.132/g' "/c/Program Files/Google/Chrome/Application/123.0.6312.132/chrome_elf.dll"
>C:\Users\User\Downloads\rc_edit_64.exe "chrome.exe" --set-version-string "ProductVersion" 123.0.6312.132
>C:\Users\User\Downloads\rc_edit_64.exe "chrome.exe" --set-file-version 123.0.6312.132
>C:\Users\User\Downloads\rc_edit_64.exe "chrome.exe" --set-product-version 123.0.6312.132
>C:\Users\User\Downloads\rc_edit_64.exe "123.0.6312.132\chrome.dll" --set-product-version 123.0.6312.132
>C:\Users\User\Downloads\rc_edit_64.exe "123.0.6312.132\chrome.dll" --set-file-version 123.0.6312.132
>C:\Users\User\Downloads\rc_edit_64.exe "123.0.6312.132\chrome_elf.dll" --set-file-version 123.0.6312.132
>C:\Users\User\Downloads\rc_edit_64.exe "123.0.6312.132\chrome_elf.dll" --set-product-version 123.0.6312.132

>wmic datafile where name="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" get Version /value
'''

import traceback
from threading import Thread 

import asyncio
import time
import csv
import random
import sys
import os
import urllib.request
import requests

sys.path.append(os.path.abspath('./')) # for import helpers
sys.path.append(os.path.abspath('./playwright_stealth/')) # for import helpers
sys.path.append(os.path.abspath('./random-address/')) # for import helpers
sys.path.append(os.path.abspath('./geopy/'))
from faker import Faker
import random_address
from geopy.geocoders import Nominatim
geocoder = Nominatim(user_agent="open_python")

from playwright.async_api import async_playwright, Playwright, TimeoutError as PlaywrightTimeoutError
from playwright_stealth import stealth_async
import re
import base64
import shutil
import json
import pickle

from src.sms import purchase_number, receive_sms

# Lee,Elizabeth,leeelizabeth769@yahoo.com,gyzptdwexrtqikrq

UA = [
#    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.3",
#    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Safari/605.1.1",
#    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.",
#    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.3"
]

VP = [
    {"width": 1920, "height": 1080},
    {"width": 1280, "height": 1024},
    {"width": 1280, "height": 800},
    {"width": 1560, "height": 900},
]



cookieDir = os.path.expanduser('~')+'/.tmp/playwright/' # browser profile with cookies
cookieSimpleFile = os.path.dirname(os.path.abspath(cookieDir)) + '/' + '.cookies_pl.pkl' # exported cookies
downloadPath = os.path.abspath('./downloaded_files/')
_LOAD_COOKIES = False
_SAVE_COOKIES = True
_HEADLESS = False
_STEALTH = True
_EXTERNAL_PDF = True
_BLOCK_IMAGES = True
_PROXY = None

async def createUndetectedWebcontext (suf="https://bing.com", headless=_HEADLESS, proxy=None, extension0='./Extensions/Extension0'):
    suf = filterSuffix(suf)
    try:
        rm_r(cookieDir)
    except:
        pass
    os.makedirs(os.path.abspath(cookieDir+'Default/'), exist_ok=True) # for default_preferences
    os.makedirs(os.path.dirname(cookieDir), exist_ok=True) # for cookieSimpleFile
    os.makedirs(downloadPath, exist_ok=True)
    global _LOAD_COOKIES
    global _SAVE_COOKIES
    global _HEADLESS
    global _STEALTH
    global _EXTERNAL_PDF
    global _BLOCK_IMAGES
    global _PROXY ###
    if (proxy is None):
        proxy = _PROXY 
    default_preferences = {
        "alternate_error_pages": {
            "backup": False
        },
        "autocomplete": {
            "retention_policy_last_version": 109
        },
        "autofill": {
            "orphan_rows_removed": True,
            "credit_card_enabled": False,
        },
        "browser": {
            "check_default_browser": False,
        },
        "credentials_enable_service": False,
        "distribution": {
            "import_bookmarks": False,
            "import_history": False,
            "import_search_engine": False,
            "make_chrome_default_for_user": False,
            "skip_first_run_ui": True
        },
        "dns_prefetching": {
            "enabled": False
        },
        "download": {
            "default_directory": downloadPath,
            "directory_upgrade": True,
            "prompt_for_download": False
        },
        "intl": {
            "selected_languages": "en-US,en"
        },
        "ntp": {
            "num_personal_suggestions": 1
        },
        "optimization_guide": {
            "hintsfetcher": {
                "hosts_successfully_fetched": {}
            },
            "previously_registered_optimization_types": {
                "HISTORY_CLUSTERS": True
            },
            "store_file_paths_to_delete": {}
        },
        "plugins": {
            "always_open_pdf_externally": _EXTERNAL_PDF,
            "plugins_list": []
        },
        "profile": {
            "avatar_index": 26,
            "content_settings": {
            },
            "creation_time": "13357906733907147",
            "default_content_setting_values": {
                "geolocation": 1
            },
            "default_content_settings": {
                "geolocation": 1,
                "images": 2 if (_BLOCK_IMAGES) else 0,
                "mouselock": 1,
                "notifications": 1,
                "popups": 1,
                "ppapi-broker": 1
            },
            "exit_type": "none",
            "exited_cleanly": True,
            "managed_user_id": "",
            "name": "User 1",
            "password_manager_enabled": False
        },
        "safebrowsing": {
            "enabled": False,
            "event_timestamps": {},
            "metrics_last_log_time": "13357906735"
        },
        "safebrowsing_for_trusted_sources_enabled": False,
        "search": {
            "suggest_enabled": False
        },
        "sessions": {
            "event_log": [
                {
                    "crashed": False,
                    "time": "13357906734991768",
                    "type": 0
                }
            ],
            "session_data_status": 1
        },
        "settings": {
            "a11y": {
                "apply_page_colors_only_on_increased_contrast": True
            }
        },
        "signin": {
            "allowed": True
        },
        "translate": {
            "enabled": False
        },
        "translate_site_blacklist": [],
        "translate_site_blocklist_with_time": {},
    }
    with open(os.path.abspath(cookieDir+'Default/Preferences'), 'w+') as f:
        json.dump(default_preferences, f)
    context = None
    page = None
    try:
        #options.args("disable-infobars")
        #async with async_playwright() as playwright:
        playwright = await async_playwright().start()
        #browser = await playwright.chromium.launch(
        context = await playwright.chromium.launch_persistent_context( 
            cookieDir,
            headless = headless,
            user_agent = random.choice(UA) if (len(UA) > 0) else None,
            viewport = random.choice(VP) if (len(VP) > 0) else None,
            proxy = {
                "server": proxy['proxy_server'],
                "username": proxy['proxy_username'],
                "password": proxy['proxy_password']
            } if (proxy is not None) else None,
            bypass_csp = True,
            accept_downloads = True,
            ignore_default_args = [ #excludeSwitches
                '--disable-extensions',
                '--enable-automation',
            ],
            args = [
                f"--disable-extensions-except={os.path.abspath(extension0)}" if (extension0 is not None) else "",
                f"--load-extension={os.path.abspath(extension0)}" if (extension0 is not None) else "",
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-notifications",
                "--disable-infobars",
                "--disable-blink-features=AutomationControlled",
                "--ignore-ssl-errors=yes", "--ignore-certificate-errors",
            ],
        )    
        page = await context.new_page()
        if (_STEALTH):
            await stealth_async(page)
        async def routing (route):
            global _BLOCK_IMAGES
            requestUrl = route.request.url
            resourceType = route.request.resource_type
            #if (_BLOCK_IMAGES and resourceType in ['image', 'stylesheet', 'font']):
            if (_BLOCK_IMAGES and resourceType in ['image']):
                await route.abort()
            else:
                await route.continue_()
        await page.route('**/*', routing)
        if (_LOAD_COOKIES):
            nice = load_cookies2(page, suf, False)
    except:
        print(traceback.format_exc())
        playwright = None # TODO close
        context = None
    if (context is not None):
        if (len(context.background_pages) == 0):
            background_page = context.wait_for_event('backgroundpage')
        else:
            background_page = context.background_pages[0]
    else:
        background_page = None
    return (context, page, background_page, playwright)

def filterSuffix (suf):
    suf = suf.replace('\\', '/')
    if ('//' in suf):
        suf = suf.split('//')[1]
    suf = suf.split('/')[0].split('?')[0]
    return suf

def load_cookies1 (driver, suf, changeTimeout=False):
    print("Loading 1 cookies from " + cookieSimpleFile)
    if (changeTimeout == True):
        changeTimeout = 1000
    nice = False
    cookies = pickle.load(open(cookieSimpleFile, "rb"))
    # Enables network tracking so we may use Network.setCookie method
    driver.execute_cdp_cmd('Network.enable', {})
    # Iterate through pickle dict and add all the cookies
    for cookie in cookies:
        expiry = cookie.get('expiry', None)
        if (expiry and changeTimeout != False):
            cookie['expiry'] = int((1.0+expiry) * changeTimeout)
        # Fix issue Chrome exports 'expiry' key but expects 'expire' on import
        if 'expiry' in cookie:
            cookie['expires'] = cookie['expiry']
            del cookie['expiry']
        # Set the actual cookie
        driver.execute_cdp_cmd('Network.setCookie', cookie)
        if (cookie['domain'] == suf):
            nice = True
    # Disable network tracking
    driver.execute_cdp_cmd('Network.disable', {})
    return nice
    
def load_cookies2 (driver, suf, changeTimeout=False):
    nice = True
    try:
        print("Loading 2 cookies from " + cookieSimpleFile)
        if (changeTimeout == True):
            changeTimeout = 1000
        if (not(hasattr(driver, "current_url"))):
            driver.current_url = driver.url
        if (driver.current_url is None or driver.current_url == '' or driver.current_url.split('//')[1].split('/')[0].split('?')[0] != suf):
            driver.get('https://' + suf)
        cookies = pickle.load(open(cookieSimpleFile, "rb"))
        for cookie in cookies:
            try:
                expiry = cookie.get('expiry', None)
                if (expiry and changeTimeout != False):
                    cookie['expiry'] = int((1.0+expiry) * changeTimeout)
                if (cookie['domain'] != suf):
                    continue
                cookie['domain'] = suf
                print(json.dumps(cookie))
                driver.add_cookie(cookie)
            except Exception as e0545467653:
                nice = False
                print(e0545467653)
        driver.refresh()
    except Exception as e0545467654:
        nice = False
        print(e0545467654)
    return nice

# path2 is optional any child within path; path is file or directory to remove
def rm_r(path, path2 = None):
    if (path == '.' or path == './' or path == '.\\' or path.startswith('..')) or (not(path2 is None) and path2.startswith('..')):
        warnings.warn('Remove denied: ' + path)
        return
    if os.path.isdir(path) and not os.path.islink(path):
        shutil.rmtree(path)
    elif os.path.exists(path):
        os.remove(path)

async def tmp_loader_json (url, proxy):
    (context, page, background_page, playwright) = await createUndetectedWebcontext("https://example.com/", proxy = proxy, headless = True)
    data = None
    await page.goto(url)
    data = await page.content()
    await a_sleep(3)
    await context.close() #await browser.close()
    await playwright.stop()
    data = '{' + data.split('>{')[1].split('}<')[0] + '}'
    return data
    
def async_to_sync (awaitable):
    class MyThread (Thread):
        def run (self):
            self.res = None
            loop = asyncio.new_event_loop() #loop = asyncio.get_event_loop()
            self.res = loop.run_until_complete(self._run())
            loop.close()
            #self.res = asyncio.run(self._run())
        async def _run (self):
            self.res = await awaitable
            return self.res
    t = MyThread()
    t.start()
    try:
        t.join()
    except KeyboardInterrupt:
        pass
    return t.res
                            

fake = Faker()
def generate_fake_address(proxy = None): # {'address1': '37600 Sycamore Street', 'address2': '', 'city': 'Newark', 'state': 'CA', 'postalCode': '94560', 'coordinates': {'lat': 37.5261943, 'lng': -122.0304698}}
    if (proxy is not None):
        if ('proxy_username' in proxy and 'proxy_password' in proxy):
            os.environ['HTTP_PROXY'] = 'http://' + proxy['proxy_username'] + ':' + proxy['proxy_password'] + '@' + proxy['proxy_server']
            os.environ['HTTPS_PROXY'] = 'http://' + proxy['proxy_username'] + ':' + proxy['proxy_password'] + '@' + proxy['proxy_server']
            os.environ['http_proxy'] = 'http://' + proxy['proxy_username'] + ':' + proxy['proxy_password'] + '@' + proxy['proxy_server']
            os.environ['https_proxy'] = 'http://' + proxy['proxy_username'] + ':' + proxy['proxy_password'] + '@' + proxy['proxy_server']
        else:
            os.environ['HTTP_PROXY'] = 'http://' + proxy['proxy_server']
            os.environ['HTTPS_PROXY'] = 'http://' + proxy['proxy_server']
            os.environ['http_proxy'] = 'http://' + proxy['proxy_server']
            os.environ['https_proxy'] = 'http://' + proxy['proxy_server']
    res = {}
    while (len(res.keys()) < 4 or not('address1' in res) or not('city' in res) or not('address1' in res) or not('postalCode' in res)):
        r = random.randint(0, 4)
        if (r == 0):
            res = random_address.real_random_address_by_state(str(fake.state_abbr()))
        elif (r == 1):
            res = random_address.real_random_address_by_postal_code(str(fake.zipcode()))
        elif (r == 2):
            res = random_address.real_random_address_by_postal_code(str(random.randint(55001, 99950)))
        elif (r == 3):
            try:
                ###data = async_to_sync(tmp_loader_json('http://ip-api.com/json', proxy))
                with urllib.request.urlopen('http://ip-api.com/json') as data:
                ##with requests.get('http://ip-api.com/json') as data:
                    data = json.load(data)
                    ##data = json.loads(data)
                    res['state'] = data['region']
                    res['city'] = data['city']
                    try:
                        res['address1'] = random_address.real_random_address_by_postal_code(data['zip'])['address1'] 
                        res['state'] = random_address.real_random_address_by_postal_code(data['zip'])['state']
                    except:
                        res = random_address.real_random_address_by_state(str(res['state']))
                        pass
                        #res['address1'] = (data['timezone'].split('/')[1] if ('/' in data['timezone']) else data['timezone'].split('/')[0]) + ' street'
                    res['postalCode'] = data['zip']
                    print('res', res)
            except:
                print(traceback.format_exc())
                pass
        else:
            try:
                with urllib.request.urlopen('https://api.ipify.org/?format=json') as data0:
                ##with requests.get('https://api.ipify.org/?format=json') as data0:
                    ip = json.load(data0)['ip']
                    ##ip = json.loads(data0.text)['ip']
                    print(ip)
                    with urllib.request.urlopen('https://get.geojs.io/v1/ip/geo/' + str(ip) + '.json') as data:
                        data = json.load(data)
                        res['state'] = data['region'] if ('region' in data) else data['country_code']
                        res['address1'] = (data['timezone'].split('/')[1] if ('/' in data['timezone']) else data['timezone'].split('/')[0]) + ' street'
                        data = geocoder.reverse('' + str(data['latitude']) + ', ' + str(data['longitude']), language = 'en-us,en')
                        address = str(data)
                        data = data.raw['address']
                        if ('postcode' in data):
                            res['postalCode'] = data['postcode']
                        else:
                            data['postcode'] = ','
                        res['country'] = data['country']
                        res['city'] = data['city'] if ('city' in data) else data['county']
                        res['state'] = data['state'] if ('state' in data) else data['region']
                        if (res['country'] != '' and res['country'] == address.split(',')[-1].strip()):
                            address = address.split(data['postcode'])[0].strip()
                            address = address.split(',')[::-1]
                            address = list(filter(lambda e: not(not(e)), map(lambda e: e.strip(), address)))
                            res['address2'] = address[-1]
                            if (address[0] == res['state'] or (len(address) >= 2 and address[1] == res['city'])):
                                address = ', '.join(address[2:-1])
                            else:
                                address = ', '.join(address)
                            res['address1'] = address
                        print(res)
            except:
                print(traceback.format_exc())
                pass            
    
    if (r == 0):
        print(str(r) + ' way: by_state')
    elif (r == 1):
        print(str(r) + ' way: by_postal_code')
    elif (r == 2):
        print(str(r) + ' way: by randint code')
    elif (r == 3):
        print(str(r) + ' way: by ip api json')
    else:
        print(str(r) + ' way: by geo json')
            
    res['street'] = res['address1'] if ('address1' in res) else fake.street_address()
    res['city'] = res['city'] if ('city' in res) else fake.city()
    res['state'] = res['state'] if ('state' in res) else fake.state_abbr()
    res['zip_code'] = res['postalCode'] if ('postalCode' in res) else fake.zipcode()
    try:
        del res['postalCode']
        del res['address1']
        del res['address2']
    except:
        pass
    os.environ['HTTP_PROXY'] = ''
    del os.environ['HTTP_PROXY']
    os.environ['HTTPS_PROXY'] = ''
    del os.environ['HTTPS_PROXY']
    os.environ['http_proxy'] = ''
    del os.environ['http_proxy']
    os.environ['https_proxy'] = ''
    del os.environ['https_proxy']
    return res
    
def generate_name(username=None, userpass=None):
    res = {
        'first_name': fake.first_name_male() if (random.randint(0, 1) == 0) else fake.first_name_female(),
        'last_name': fake.last_name(), # TODO: last_name from email username (if exists)
    }
    res['password'] = res['last_name'][0:1].lower() + res['first_name'][0:1].upper() + res['first_name'][1:-1] + fake.password() if (not userpass) else userpass + res['last_name'][0:1].lower() + res['first_name'][0:1].upper() + fake.password()
    return res

def w_sleep (timeout=0, method=time.sleep):
    l = lambda timeout: (timeout + random.randint(0, int(timeout*(timeout+0.1)*100//10)) / 10 % (timeout+0.1))
    t = l(timeout) if (timeout >= 0) else 0
    print('*sleep:', str(t))
    if (method is not None):
        method(t)
    return t

async def a_sleep (timeout=0, method=asyncio.sleep):
    t = w_sleep(timeout, None)
    await method(t)
    return t

#def s_sleep (timeout=0, method=asyncio.sleep):
#    loop = asyncio.get_event_loop()
#    loop.run_until_complete(a_sleep(timeout, method))
#    loop.close()

page = None
async def run(config):
    global _SAVE_COOKIES
    global page
    
    #async with async_playwright() as playwright:
        #browser = await playwright.chromium.launch(
        #    headless=False,
        #    proxy={
        #        "server": config['proxy_server'],
        #        "username": config['proxy_username'],
        #        "password": config['proxy_password']
        #    }
        #)
        #page = await browser.new_page(
        #    user_agent=random.choice(UA) if (len(UA) > 0) else None,
        #    viewport=random.choice(VP) if (len(VP) > 0) else None,
        #)
        #await stealth_async(page)

    
    (context, page, background_page, playwright) = await createUndetectedWebcontext("https://walmart.com/", proxy = config) 
    try:    
        try:
            await page.goto("https://theylied.net.by/test.html", # "https://internet.yandex.ru", 
                            timeout=random.randint(25000, 45000),  # https://www.walmart.com/account/login?vid=oaoh
                            referer="https://www.google.com/search?q=walmart&sourceid=chrome&ie=UTF-8")
        except PlaywrightTimeoutError:
            print("Slow website")
            print("Ignoring wait")
        await a_sleep(3)

        
            
        try:
            await page.locator('button[aria-label*="months of Apple Music"]').filter(has_text = "Get offer").first.click()
        except Exception as e:
            print('1', e)
            try:
                l = page.locator('div:has-text("5 free months")').filter(has = page.locator('button')).last
                if (await l.is_visible()):
                    await l.locator('button').first.click()
            except Exception as e:
                print('2', e)
                try:
                    l = page.locator('h3:has-text("Apple Music")').filter(has = page.locator('button')).first
                    if (await l.is_visible()):
                        await l.get_by_role('button').first.click()
                except Exception as e:
                    print('3', e)
                    raise e
            
        try:
            await page.screenshot(path="screenshot.png", full_page=True)
        except:
            pass

        await a_sleep(10)
        
        await a_sleep(600) ###
        
        
        await context.close() #await browser.close()
        return True
    finally:
        if (context is not None):
            await context.close()
        if (playwright is not None):
            await playwright.stop()



def update_file_lines(file_path, lines, write_mode='w+'):
    with open(file_path, write_mode, newline='', encoding='utf-8') as file:
        for line in lines:
            file.write(line + '\n')


def read_and_update_csv(file_path):
    with open(file_path, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = list(reader)
    remaining_data = data[1:]

    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(remaining_data)

    return data[0] if data else None


def read_and_update_txt(file_path):
    lines = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if (not line or len(line) == 0):
                continue
            else:
                lines.append(line)

    if (not lines or (len(lines) == 0)):
        return None
    remaining_lines = lines[1:]

    update_file_lines(file_path, [line.strip() for line in remaining_lines], 'w+')

    return lines[0].strip().split('|')

def restore_txt (file_path, remaining_lines):
    #print(len(remaining_lines))
    #print(remaining_lines)
    update_file_lines(file_path, [line.strip() for line in remaining_lines], 'a+')

# async def main():
#     accounts = read_and_update_csv("accounts.csv")
#     cards = read_and_update_txt('cards.txt')
#     proxies = read_and_update_txt('proxies.txt')
#
#     configs = []
#     for account, card, proxy in zip(accounts, cards, proxies):
#         config = {**account, 'cc_number': card[0], 'exp_month': card[1], 'exp_year': card[2], 'cvv': card[3], **proxy}
#         configs.append(config)
#
#     tasks = [run(config) for config in configs]
#     await asyncio.gather(*tasks)


async def main():
    while True:
        success = None
        imaginated = None #None to disable, False to enbale imagination of accounts (for tests)
        try:
            account = None
            proxy = None
            card = None
            name = None
            try:
                pass
                #account = read_and_update_txt('accounts.txt')[0].split(':') #account = read_and_update_csv('accounts.csv')
                #proxy = read_and_update_txt('proxies.txt')[0].split(':')
                #card = read_and_update_txt('cards.txt')
                #name = generate_name(username = account[0], userpass = account[1] if (len(account) >= 2) else None)
            except:
                #print(traceback.format_exc())
                if (not account and imaginated is not None):
                    print('WARN: Account is empty!')
                    account = None
                    name = generate_name()
                    account = [(name['first_name']+name['last_name']+str(random.randint(1950, 2002))+'@yahoo.com').lower(), name['password']]
                    imaginated = True
                    print(account)
                    print(name)
                    if (not proxy):
                        proxy = read_and_update_txt('proxies.txt')[0].split(':')
                    if (not card):
                        card = read_and_update_txt('cards.txt')
                else:
                    card = None

            #if (not account or not card or not proxy):
            #    print("No more data available or file missing entries.")
            #    break
            
            proxy = 'gate.smartproxy.vip:7000:user-2TiYUv5E2gLB2_10015146-country-US-session-99435212:AeLSFo67K4QdJ'.split(':')
            proxy = {'proxy_server': proxy[0] + ':' + proxy[1], 'proxy_username': proxy[2], 'proxy_password': proxy[3]}
            
            name = generate_name()
            address = generate_fake_address(proxy)
            print('address', address) ###
            print('email', account) ###
            print('name', name) ###
            
            
            
            #config = {**account, 'cc_number': card[0], 'exp_month': card[1], 'exp_year': card[2], 'cvv': card[3], **proxy}       
            config = {**address, **name, **proxy
            }
            success = await run(config)
        except (Exception, KeyboardInterrupt) as e0:
            success = False
            print(e0)
            print(traceback.format_exc())
        print('success: ', success)
        if success:
            print("Process completed successfully.")
            break
        else:
            await a_sleep(60)
            print("Retrying with next available data set...")
        await a_sleep(1)


asyncio.run(main())
