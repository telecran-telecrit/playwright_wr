import traceback

import asyncio
import time
import csv
import random
import sys
import os
import signal
import urllib.request
import requests

sys.path.append(os.path.abspath('./')) # for import helpers
sys.path.append(os.path.abspath('./playwright_stealth/')) # for import helpers
sys.path.append(os.path.abspath('./random-address/')) # for import helpers
sys.path.append(os.path.abspath('./geopy/'))
from datetime import datetime
from faker import Faker
from faker.providers import BaseProvider
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

from src.sms2 import purchase_number, receive_sms

# Lee,Elizabeth,leeelizabeth769@yahoo.com,gyzptdwexrtqikrq

UA = [
#    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.3",
#    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Safari/605.1.1",
#    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.",
#    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.3",

#"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.1",
#"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.",
#"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.",
#"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.3",
#"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.4",
#"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.",
#"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.3",
#"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.3",
#"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Avast/122.0.0.",
#"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.",
#"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/24.0 Chrome/117.0.0.0 Safari/537.3",
#"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.3",
#"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 OPR/95.0.0.",
#"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.10",
#"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 OPR/108.0.0.",
#"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.3",
]

VP = [
#    {"width": 1920, "height": 1080}, # Full HD
    {"width": 1366, "height": 768},
    {"width": 1280, "height": 1024},
    {"width": 1024, "height": 768},
    {"width": 1280, "height": 800},
    {"width": 1560, "height": 900},
    {"width": 1440, "height": 900},
    {"width": 1600, "height": 900},
    {"width": 1680, "height": 1050},
#    {"width": 2560, "height": 1440}, # QHD
#    {"width": 3840, "height": 2160}, # 4K UHD
]



cookieDir = os.path.expanduser('~')+'/.tmp/playwright/' # browser profile with cookies
cookieSimpleFile = os.path.dirname(os.path.abspath(cookieDir)) + '/' + '.cookies_pl.pkl' # exported cookies
downloadPath = os.path.abspath('./downloaded_files/')
_LOAD_COOKIES = False
_SAVE_COOKIES = True
_HEADLESS = False
_STEALTH = True ##
_EXTERNAL_PDF = True
_BLOCK_IMAGES = True ##
_PROXY = None

async def createUndetectedWebcontext (suf="https://bing.com", headless=_HEADLESS, proxy=None, extension0='./Extensions/Extension0'):
    suf = filterSuffix(suf)
    
    try:
        rm_r(cookieDir)
    except (KeyboardInterrupt, SystemExit, asyncio.exceptions.CancelledError) as e0:
        raise(e0)
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
    except (KeyboardInterrupt, SystemExit, asyncio.exceptions.CancelledError) as e0:
        raise(e0)
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


class MyPersonProvider(BaseProvider):
    first_name_females = ["food", "fruit"]
    def first_name_female(self):
        return random.choice(list(filter(lambda line: (line is not None and len(line.strip()) >= 2), list(open('femalefirstnames.txt'))))).strip()
        #return self.random_element(self.first_name_females)
    def first_name_male(self):
        return random.choice(list(filter(lambda line: (line is not None and len(line.strip()) >= 2), list(open('malefirstnames.txt'))))).strip()
    def last_name(self):
        return random.choice(list(filter(lambda line: (line is not None and len(line.strip()) >= 2), list(open('lastnames.txt'))))).strip()

fake = Faker()
#fake.add_provider(MyPersonProvider) ###

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
    failed = set()
    r = -1
    while (len(res.keys()) < 4 or not('address1' in res) or not('city' in res) or not('address1' in res) or not('postalCode' in res)):
        r = random.randint(0, 4)
        if (len(failed) >= 5):
            break
        if (r in failed):
            continue
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
                    except (KeyboardInterrupt, SystemExit, asyncio.exceptions.CancelledError) as e0:
                        raise(e0)
                    except:
                        res = random_address.real_random_address_by_state(str(res['state']))
                        pass
                        #res['address1'] = (data['timezone'].split('/')[1] if ('/' in data['timezone']) else data['timezone'].split('/')[0]) + ' street'
                    res['postalCode'] = data['zip']
            except (KeyboardInterrupt, SystemExit, asyncio.exceptions.CancelledError) as e0:
                raise(e0)
            except:
                print(traceback.format_exc())
                pass
        else:
            pass
        failed.add(r)
    
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
    except (KeyboardInterrupt, SystemExit, asyncio.exceptions.CancelledError) as e0:
        raise(e0)
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
    res['password'] = res['last_name'][0:1].lower() + res['first_name'][0:1].upper() + res['first_name'][1:-1] + fake.password() if (not userpass) else userpass + res['last_name'][0:1].lower() + res['first_name'][0:1].upper() + generate_random_string(random.randint(4, 6)) + ('^' if random.randint(0, 1) == 0 else '$') + (generate_random_string(random.randint(1, 2)).lower()) + (generate_random_string(random.randint(1, 2)).upper()) + generate_random_string(random.randint(4, 7))
    return res

def _is_safe (argvalue):
    return '(' not in argvalue and ')' not in argvalue and '{' not in argvalue and '}' not in argvalue and ':' not in argvalue and '=' not in argvalue and ';' not in argvalue and '#' not in argvalue and '*' not in argvalue and '/' not in argvalue and '\\' not in argvalue and '%' not in argvalue and '-' not in argvalue and '+' not in argvalue and '!' not in argvalue and '?' not in argvalue and '<' not in argvalue and '>' not in argvalue and 'lambda' not in argvalue

def parse_args (str_args):
    res = {}
    if ((not(str_args.find('=') >= 0)) != (not(str_args.find(':') >= 0 and str_args.find('{') >= 0 and str_args.find('}') >= 0))):
        if (str_args.find(':') >= 0):
            str_args = str_args[str_args.index('{') + 1:str_args.rindex('}')]
            str_args = str_args.replace(':', '=')
        res = {}
        for item in str_args.split(','):
            argname, argvalue = item.split('=')
            argvalue = argvalue.strip()
            if (argvalue[0] == argvalue[-1] and (argvalue[0] == '"' or argvalue[0] == "'")):
                argvalue = argvalue[1:-1]
            elif (_is_safe(argvalue)):
                argvalue = eval(argvalue)
            else:
                argvalue = None
            res.update({argname.strip(): argvalue})
    else:
        str_args = str_args.strip()
        if (len(str_args) == 0 or str_args == ','):
            return []
        res = str_args.split(',')
        res = list(map(lambda x: eval(x.strip()) if (_is_safe(x.strip())) else None, res))
    return res

def some_time (timeout=0):
    l = lambda timeout: (timeout + random.randint(0, int(timeout*(timeout+0.1)*100//10)) / 10 % (timeout+0.1))
    t = l(timeout) if (timeout >= 0) else 0
    return t

def v_sleep (timeout=0, page_locator=None, title='', method=time.sleep):
    t = some_time(timeout)
    print('*sleep:', str(t), '' if (not title) else '' + str(title))
    r = None
    if (page_locator is not None):
        r = page_locator(title)
    if (method is not None):
        method(t)
    return (t, r)
    
def w_sleep (timeout=0, page_locator=None, title='', locator_action='', method=time.sleep):
    (t, r) = v_sleep(timeout = timeout, page_locator = page_locator, title = title, method = method)
    if (locator_action is not None and locator_action.strip() != ''):
        m = getattr(r, locator_action)
        m = m()
    return r

async def a_sleep (timeout=0, page_locator=None, title='', locator_action='', method=asyncio.sleep):
    (t, r) = v_sleep(timeout = timeout, page_locator = page_locator, title = title, method = None)
    try:
        r = await r
    except (KeyboardInterrupt, SystemExit, asyncio.exceptions.CancelledError) as e0:
        raise(e0)
    except:
        pass
    if (page_locator is not None and r is not None):
        try:
            await r.scroll_into_view_if_needed(timeout=3000)
        except (KeyboardInterrupt, SystemExit, asyncio.exceptions.CancelledError) as e0:
            raise(e0)
        except Exception as locscrollError:
            print(locscrollError)
        m = r
        if (locator_action is not None and locator_action.strip() != ''):
            locator_action_args = {}
            if ('(' in locator_action and ')' in locator_action):
                locator_action_args = parse_args(locator_action[locator_action.index('(') + 1:locator_action.rindex(')')])
                locator_action = locator_action[0:locator_action.index('(')]
            else:
                locator_action_args = {}
            m = getattr(r, locator_action)
            print(locator_action_args)
            isAsync = asyncio.iscoroutinefunction(m)
            if (isinstance(locator_action_args, list)):
                m = m(*locator_action_args)
            else:
                m = m(**locator_action_args)
            if (isAsync):
                m = await m
    try:
        await method(t)
    except (KeyboardInterrupt, SystemExit, asyncio.exceptions.CancelledError) as e0:
        raise(e0)
    except:
        method(t)
    return r       

#def s_sleep (timeout=0, title='', method=asyncio.sleep):
#    loop = asyncio.get_event_loop()
#    loop.run_until_complete(a_sleep(timeout, title, method))
#    loop.close()

def generate_random_string(length):
    letters = [chr(random.randint(97, 122)) for _ in range(length)]
    return ''.join(letters)

async def randomButtonClick (page):
    target = None
    j = 0
    while (j < 100):
        j = j + 1
        t = random.randint(0, 20)
        m = ''
        if (t == 0):
            m = 'button'
            b = page.locator(m)
        elif (t == 1):
            m = 'input[type="button"]'
            b = page.locator(m)
        elif (t == 2):
            m = 'input'
            b = page.locator(m)
        else:
            m = 'a'
            b = page.locator(m+'[href*="' + '://' + (page.url.split('://')[1].split('/')[0]) + '"]')
        count = await b.count()
        if (count > 1):
            i = random.randint(0, count - 1)
        else:
            i = 0
        if (random.randint(0, 10) == 0):
            count = 0
            return
        if (await page.locator(m).nth(i).is_visible()):
            await a_sleep(2)
            #await page.locator(m).nth(i).hover()
            #await a_sleep(1)
            await page.locator(m).nth(i).click()
            await a_sleep(5)
            break
            
async def bringToFront (page):
    cdp = await page.context.new_cdp_session(page) 
    await cdp.send("Page.bringToFront", {}); # execute_cdp_cmd
    
async def randomClicks (page):
    t = random.randint(3, 5)
    j = 0
    while (j < t):
        j = j + 1
        try:
            await randomButtonClick(page)
            await a_sleep(1.5)
            await bringToFront(page)
        except (KeyboardInterrupt, SystemExit, asyncio.exceptions.CancelledError) as e0:
            raise(e0)
        except:
            pass

async def locator_press_sequentially2 (locator, data, nearDealy=100, humanErrors=True):
    print('locator_press_sequentially2: ', str(locator), str(data))
    i = 0
    try:
        await locator.clear()
    except (KeyboardInterrupt, SystemExit, asyncio.exceptions.CancelledError) as e0:
        raise(e0)
    except:
        pass
    for h in data:        
        if (humanErrors and random.randint(0, 10) == 0):
            try:
                await locator.press_sequentially(data[i + 1], delay=random.randint(nearDealy, nearDealy+200))
            except (KeyboardInterrupt, SystemExit, asyncio.exceptions.CancelledError) as e0:
                raise(e0)
            except:
                try:
                    await locator.press_sequentially(data[i - 1], delay=random.randint(nearDealy, nearDealy+200))
                except (KeyboardInterrupt, SystemExit, asyncio.exceptions.CancelledError) as e0:
                    raise(e0)
                except:
                    await locator.press_sequentially(h, delay=random.randint(nearDealy, nearDealy+200))
            await a_sleep(1)
            await locator.press('Backspace')
            await a_sleep(1.2)
        await locator.press_sequentially(h, delay=random.randint(nearDealy, nearDealy+200)) # await page.locator("#number").type(h, random.randint(nearDealy, nearDealy+200))
        i = i + 1

async def run (config):
    global _SAVE_COOKIES
    global _BLOCK_IMAGES

    if (_BLOCK_IMAGES):
        _BLOCK_IMAGES_old = True
    else:
        _BLOCK_IMAGES_old = False
    
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
            await page.goto("https://www.walmart.com/", # "https://internet.yandex.ru", 
                            timeout=random.randint(5000, 7000),  # https://www.walmart.com/account/login?vid=oaoh
                            referer="https://www.google.com/search?q=walmart&sourceid=chrome&ie=UTF-8")
        except PlaywrightTimeoutError:
            print("Slow website")
            print("Ignoring wait")
        await a_sleep(3, title = 'page.goto walmart')
        
        await randomClicks(page)
        await a_sleep(2)
        await bringToFront(page)
        
        try:
            if ((page.url.split('://')[1].split('/')[0]) != 'www.walmart.com'):
                await page.goto("https://www.walmart.com/",
                                timeout=random.randint(8000, 12000),
                                referer=page.url)
        except PlaywrightTimeoutError:
            print("Slow website 2")
            print("Ignoring wait 2")

        is_captcha = False
        try:
            await a_sleep(1)
            await a_sleep(3, page_locator = page.get_by_text, title = 'Sign InAccount', locator_action = 'click')
        except PlaywrightTimeoutError:
            is_captcha = True
        
        if (is_captcha):
            print("!captcha")
            return None
        
        await a_sleep(3)
        try:
            await a_sleep(4, page.get_by_text, "or create account", 'click(timeout=3000)')
        except PlaywrightTimeoutError:
            print("Now 2nd sign in button, ignoring")

        try:
            email_input_by_name = await a_sleep(1, page.locator, '[name="Email Address"]')
            await email_input_by_name.click(timeout=15000)
        except PlaywrightTimeoutError:
            is_captcha = True
            
        if (is_captcha):
            print("!captcha")
            return None
        
        await locator_press_sequentially2(email_input_by_name, config["email"], random.randint(200, 250))
        await email_input_by_name.fill(config["email"])
        await a_sleep(2) #await asyncio.sleep(2)
            

        await a_sleep(3, page.get_by_text, "Continue", locator_action='click()')

        try:
            first_name_input_by_name = page.locator('[name="firstName"]')
            await locator_press_sequentially2(first_name_input_by_name, config["first_name"], random.randint(140, 180))
            await a_sleep(0.5) #await asyncio.sleep(0.5)

            last_name_input_by_name = page.locator('[name="lastName"]')
            await locator_press_sequentially2(last_name_input_by_name, config["last_name"], random.randint(140, 180))
            await a_sleep(0.5) #await asyncio.sleep(0.5)

            phone = None
            leftTries = 10
            while (not(phone)):
                if ((leftTries := leftTries - 1) < 0):  break
                await a_sleep(7)
                try:
                    phone = await purchase_number()
                except (KeyboardInterrupt, SystemExit, asyncio.exceptions.CancelledError) as e0:
                    raise(e0)
                except:
                    phone = False

            phone_number_input_by_name = page.locator('[name="phoneNumber"]')
            await locator_press_sequentially2(phone_number_input_by_name, phone["phonenumber"], random.randint(140, 180))
            await a_sleep(1)

            new_password_input_by_name = page.locator('[name="newPassword"]')
        except (KeyboardInterrupt, SystemExit, asyncio.exceptions.CancelledError) as e0:
            raise(e0)
        except:
            print(traceback.format_exc())
            new_password_input_by_name = page.locator('[name="password"]')
            
        password_new_tmp = generate_random_string(random.randint(3, 5)) + str('123') + generate_random_string(random.randint(1, 2))
        await locator_press_sequentially2(new_password_input_by_name, password_new_tmp, random.randint(100, 250))
        await a_sleep(1)
        await page.get_by_text("Continue").last.click()
        await a_sleep(2)
        
        try:
            await locator_press_sequentially2(new_password_input_by_name, config["password"], random.randint(300, 450))
            await a_sleep(1)
            await page.get_by_text("Continue").last.click()
            await a_sleep(3)
        except (KeyboardInterrupt, SystemExit, asyncio.exceptions.CancelledError) as e0:
            raise(e0)
        except:
            config["password"] = password_new_tmp
            pass

        code = "0"
        leftTries = 50
        while (code is None or code == "" or code == "0"):
            if ((leftTries := leftTries - 1) < 0):  break
            code = (await receive_sms(phone["order_id"]))["code"]
            await a_sleep(3)

        for i, digit in enumerate(code):
            selector = f"#input-verificationCode"
            if i:
                selector += f"-{i}"
            await page.fill(selector, digit)

        await a_sleep(3)
        await page.click('button[type="submit"][form="verify-phone-otp-form"]')

        await a_sleep(15)

        try:
            await a_sleep(1, page.get_by_text, "I agree to", 'click(timeout=9000)')
        except PlaywrightTimeoutError:
            print("Subscription page not visible. Navigating")
            await page.goto("https://www.walmart.com/",
                                timeout=random.randint(15000, 18000),
                                referer=page.url)
            await a_sleep(3)
            try:
                await a_sleep(1, page.get_by_text, "I agree to", 'click(timeout=9000)')
            except PlaywrightTimeoutError:
                print("Subscription page not visible. Reloading")
                await page.reload()
                await a_sleep(1, page.get_by_text, "I agree to", 'click(timeout=60000)')

        await a_sleep(10, page.get_by_text, "Continue & add payment method", 'click(timeout=30000)')

        print("adding payment method")
        #return ###

        # Danger zone
        try:
            frame = page.frame_locator("#payments-wallet-chooser")
            
            await a_sleep(3, frame.get_by_text, "Add a new payment method", 'click(timeout=45000)')

            # CC
            await locator_press_sequentially2(frame.locator("#cc-number"), config["cc_number"], random.randint(140, 180))
            await a_sleep(2)

            # First name
            
            await locator_press_sequentially2(first_name_input_by_name := frame.locator('[name="firstName"]').last, config["first_name"], random.randint(140, 180), False)
            await a_sleep(2)

            # Last name
            await locator_press_sequentially2(last_name_input_by_name := frame.locator('[name="lastName"]').last, config["last_name"], random.randint(140, 180), False)
            await a_sleep(2)

            # Month
            # await frame.locator("#react-aria-8").select_option("04")
            #await frame.locator('div[data-testid="selectMMContainer"] select').select_option(config["exp_month"])
            await (await a_sleep(2, frame.locator, 'div[data-testid="selectMMContainer"] select')).select_option(config["exp_month"])

            # Year
            # await frame.locator("#react-aria-8").select_option("04")
            #await frame.locator('div[data-testid="selectYYContainer"] select').select_option(config["exp_year"])
            await (await a_sleep(2, frame.locator, 'div[data-testid="selectYYContainer"] select')).select_option(config["exp_year"])

            # CVV
            await locator_press_sequentially2(frame.locator('[name="cvv"]').first, config["cvv"], random.randint(140, 180), False)
            await a_sleep(2)

            # Phone Number
            print("PHONE HUMBER")
            await a_sleep(4)
            try:
                await locator_press_sequentially2(frame.locator('input[type="tel"]'), phone["phonenumber"], random.randint(140, 180))
            except (KeyboardInterrupt, SystemExit, asyncio.exceptions.CancelledError) as e0:
                raise(e0)
            except:
                await locator_press_sequentially2(frame.locator('input[autocomplete="tel-national"]'), phone["phonenumber"], random.randint(140, 180))
            await a_sleep(3)

            # Street address
            locatorStreeAddress = frame.locator('input[name="newBillingAddress.addressLineOne"]')
            await locator_press_sequentially2(locatorStreeAddress, config["street"], random.randint(140, 180))
            await a_sleep(1)
            try:
                await locatorStreeAddress.press('ArrowDown')
                await a_sleep(0.5)
                await locatorStreeAddress.press('Enter')
                await a_sleep(0.5)
            except (KeyboardInterrupt, SystemExit, asyncio.exceptions.CancelledError) as e0:
                raise(e0)
            except Exception as locatorStreeAddressError:
                print(locatorStreeAddressError)
                pass
            
            locatorCity = frame.locator('input[autocomplete="address-level2"]')
            await a_sleep(1)
            if (len((await locatorCity.input_value(timeout=3000)).strip()) < 2):
                await locator_press_sequentially2(locatorStreeAddress, config["street"], random.randint(140, 180))
                await a_sleep(0.5)
                
                # City
                await locator_press_sequentially2(locatorCity, config["city"], random.randint(140, 180))
                await a_sleep(1)

                # State
                await frame.locator('div[data-automation-id="state-drop-down"] select').select_option(config["state"])
                await a_sleep(2)

                # Zip code
                await locator_press_sequentially2(frame.locator('input[autocomplete="postal-code"]'), config["zip_code"], random.randint(140, 180))
                await a_sleep(3)

            #await a_sleep(3000)

            # Continue
            try:
                await (await a_sleep(5, frame.locator, "button[data-test-id='continueBtn']")).click(timeout=random.randint(9000, 11000))
            except (KeyboardInterrupt, SystemExit, asyncio.exceptions.CancelledError) as e0:
                raise(e0)
            except Exception as e:
                print(e)
            
            try:
                await a_sleep(5, page.locator, "button[data-test-id='continueBtn']", 'click(timeout='+str(random.randint(4000, 5000))+')')
            except (KeyboardInterrupt, SystemExit, asyncio.exceptions.CancelledError) as e0:
                raise(e0)
            except Exception as e:
                print(e)
                
            try:
                await a_sleep(5, page.locator, "button[data-test-id='continueBtn']", 'click(timeout='+str(random.randint(3000, 4000))+')')
            except (KeyboardInterrupt, SystemExit, asyncio.exceptions.CancelledError) as e0:
                raise(e0)
            except Exception as e:
                print(e)

            await (await a_sleep(2, page.locator, 'button[aria-label*="Claim your"]')).click(timeout=random.randint(2000, 3000))
        except (KeyboardInterrupt, SystemExit, asyncio.exceptions.CancelledError) as e0:
            raise(e0)
        except Exception as e:
            
            try:
                await a_sleep(5, frame.locator, "button[data-test-id='continueBtn']", 'click(timeout='+str(random.randint(3000, 4000))+')')
            except (KeyboardInterrupt, SystemExit, asyncio.exceptions.CancelledError) as e0:
                raise(e0)
            except Exception as e:
                print('... failed')
                pass
            
            try:
                await a_sleep(2, page.locator, 'button[aria-label="Close dialog"]', 'click(timeout=1500)')
            except (KeyboardInterrupt, SystemExit, asyncio.exceptions.CancelledError) as e0:
                raise(e0)
            except Exception as e:
                print('... failed')
                pass
            
            try:
                #await page.locator('button').filter(has_text = "Leave").first.click()
                await (await a_sleep(1.5, page.locator, 'button:has-text("Leave")')).first.click(timeout=2000)
            except (KeyboardInterrupt, SystemExit, asyncio.exceptions.CancelledError) as e0:
                raise(e0)
            except Exception as e:
                print('... failed')
                pass
            
            try:
                await (await a_sleep(2, page.get_by_text, "Continue & add payment method")).click(timeout=random.randint(2000, 3000))
            except (KeyboardInterrupt, SystemExit, asyncio.exceptions.CancelledError) as e0:
                raise(e0)
            except Exception as e:
                print('... failed')
                pass
            
            try:
                await (await a_sleep(5, page.locator, "button[data-test-id='continueBtn']")).click(timeout=random.randint(1000, 2000))
            except (KeyboardInterrupt, SystemExit, asyncio.exceptions.CancelledError) as e0:
                raise(e0)
            except Exception as e:
                print('... failed')
                pass

            await (await a_sleep(0, page.locator, 'button[aria-label*="Claim your"]')).click(timeout=random.randint(5000, 7000))
            
            
        await a_sleep(1)
            
        _BLOCK_IMAGES = False
            
        try:
            await page.goto("https://www.walmart.com/plus/offer-list", 
                            timeout=random.randint(15000, 25000),
                            referer=page.url) # TODO: scroll down to get the offer
        except PlaywrightTimeoutError:
            pass
        await a_sleep(5)
            
            
        try:
            await page.locator('button[aria-label*="months of Apple Music"]').filter(has_text = "Get offer").first.click()
        except (KeyboardInterrupt, SystemExit, asyncio.exceptions.CancelledError) as e0:
            raise(e0)
        except Exception as e:
            print('1')
            try:
                l = page.locator('div:has-text("5 free months")').filter(has = page.locator('button')).last
                if (await l.is_visible()):
                    await l.locator('button').first.click()
            except (KeyboardInterrupt, SystemExit, asyncio.exceptions.CancelledError) as e0:
                raise(e0)
            except Exception as e:
                print('2')
                try:
                    l = page.locator('h3:has-text("Apple Music")').filter(has = page.locator('button')).first
                    if (await l.is_visible()):
                        await l.get_by_role('button').first.click()
                except (KeyboardInterrupt, SystemExit, asyncio.exceptions.CancelledError) as e0:
                    raise(e0)
                except Exception as e:
                    print('3')
                    raise e
          
        await a_sleep(7)
        
        try:
            contentshort = await page.content()
            with open("contentshort.htm", 'w+', encoding='utf-8') as file:
                file.write(contentshort)
        except (KeyboardInterrupt, SystemExit, asyncio.exceptions.CancelledError) as e0:
            raise(e0)
        except:
            pass
        
        greenCode = await (await a_sleep(2, page.locator, 'div span.green')).first.text_content()
        if (not(greenCode)):
            return None
        
        try:
            await page.screenshot(path="screenshot.png", full_page=True)
        except (KeyboardInterrupt, SystemExit, asyncio.exceptions.CancelledError) as e0:
            raise(e0)
        except:
            pass

        await a_sleep(2)
        
        try:
            if (_SAVE_COOKIES):
                cookies = list()
                for cookie in list(await page.context.cookies()):
                    expiry = cookie.get('expiry', 0)
                    print(expiry)
                    #if (expiry > 0 and cookie.get('name') != 'session-cookie' and cookie.get('name') != 'session'):
                    if (expiry > 0):
                        cookies.append(cookie)
                pickle.dump(cookies, open(cookieSimpleFile, "wb+"))
        except (KeyboardInterrupt, SystemExit, asyncio.exceptions.CancelledError) as e0:
            raise(e0)
        except:
            pass
        
        await context.close() #await browser.close()
        return (0, greenCode, str("+1") + phone["phonenumber"] if (not(phone["phonenumber"][0] == '+') and not(phone["phonenumber"][0] == '1')) else phone["phonenumber"], config["email"], config["password"], config["first_name"] + ' ' + config["last_name"], config["city"], config["state"])
    except (KeyboardInterrupt, SystemExit, asyncio.exceptions.CancelledError) as ke: # avoid Playwright bug https://github.com/microsoft/playwright-python/issues/1170
        print('KeyboardInterrupt 0')
        context = None
        playwright = None
        raise ke
    else:
        print('EXCEPTION NONE.')
    finally:
        print('Closing...', context, playwright)
        _BLOCK_IMAGES = _BLOCK_IMAGES_old
        try:
            if (context is not None):
                await context.close()
                context = None
            if (playwright is not None):
                await playwright.stop()
                playwright = None
            print(context, playwright)
        except (KeyboardInterrupt, SystemExit, asyncio.exceptions.CancelledError) as e0:
            raise(e0)
        except:
            pass
        print('Done.[Closing]')

# async def main(parallel_workers=5):
#     configs = [
#         {
#             'email': 'haley_baker43@yahoo.com',
#             'password': 'ypbgkcwFDSwsmeplw.32F',
#             'first_name': 'Elizabeth',
#             'last_name': 'Lee',
#             'cc_number': '5154620017051556',
#             'cvv': '757',
#             'exp_month': '07',
#             'exp_year': '2028',
#             'street': '925 S Chugach St',
#             'city': 'Palmer',
#             'zip_code': '99645',
#             'state': 'AK',
#             'proxy_server': 'pr.oxylabs.vip:7777',
#             'proxy_username': 'username1',
#             'proxy_password': 'password1',
#         },
#     ]
#
#     async with async_playwright() as playwright:
#         tasks = [run(playwright, config) for config in configs[:parallel_workers]]
#         await asyncio.gather(*tasks)


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


def main():
    while True:
        success = None
        imaginated = None #None to disable, False to enbale imagination of accounts (for tests)
        try:
            account = None
            proxy = None
            card = None
            name = None
            try:
                account = read_and_update_txt('accounts.txt')[0].split(':') #account = read_and_update_csv('accounts.csv')
                proxy = read_and_update_txt('proxies.txt')[0].split(':')
                card = read_and_update_txt('cards.txt')
                name = generate_name(username = account[0], userpass = account[1] if (len(account) >= 2) else None)
            except (KeyboardInterrupt, SystemExit, asyncio.exceptions.CancelledError) as e0:
                raise(e0)
            except:
                #print(traceback.format_exc())
                if (not account and imaginated is not None):
                    print('WARN: Account is empty!')
                    account = None
                    name = generate_name()
                    today_year = datetime.today().year
                    #account = [(name['first_name']+(name['last_name'][0:-2])+generate_random_string(random.randint(2, 3))+str(random.randint(today_year - 70, today_year - 21))+('@yahoo.com' if (random.randint(0, 1) == 0) else '@yahoo.com')).lower(), name['password']]
                    account = [(name['first_name']+(name['last_name'])+str(random.randint(today_year - 70, today_year - 21))+('@yahoo.com' if (random.randint(0, 1) == 0) else '@yahoo.com')).lower(), name['password']]
                    imaginated = True
                    print(account)
                    print(name)
                    if (not proxy):
                        proxy = read_and_update_txt('proxies.txt')[0].split(':')
                    if (not card):
                        card = read_and_update_txt('cards.txt')
                else:
                    card = None

            if (not account or not card or not proxy):
                print("No more data available or file missing entries.")
                break
            address = generate_fake_address({'proxy_server': proxy[0] + ':' + proxy[1], 'proxy_username': proxy[2], 'proxy_password': proxy[3]})
            print('address', address) ###
            print('email', account) ###
            print('name', name) ###
            #config = {**account, 'cc_number': card[0], 'exp_month': card[1], 'exp_year': card[2], 'cvv': card[3], **proxy}       
            config = {'email': account[0], 'cc_number': card[0], 'exp_month': card[1], 'exp_year': card[2], 'cvv': card[3],
            'proxy_server': proxy[0] + ':' + proxy[1], 'proxy_username': proxy[2], 'proxy_password': proxy[3],
            **address, **name,
            }
            success = asyncio.run(run(config)) # await run(config)
        except (KeyboardInterrupt, SystemExit, asyncio.exceptions.CancelledError) as e0:
            success = None
            print('KEYBOARD INTERRUPT')
            print(e0.__class__.__name__)
        except Exception as e0:
            success = False
            print(e0)
            print(traceback.format_exc())
        print('success: ', success)
        if (not(not(success))):
            print("Process completed successfully. ", success)
            (error, greenCode, phonenumber, email, password, fullname, city, state) = success
            print(f"{bcolors.OKGREEN} SUCCESS: {greenCode}{bcolors.ENDC}")
            break
        else:
            if (not imaginated):
                restore_txt('accounts.txt', [':'.join(account)])
            restore_txt('cards.txt', ['|'.join(card)])
            #restore_txt('proxies.txt', [':'.join(proxy)]) # NO
            if (success is None):
                try:
                    sys.exit(1)
                finally:
                    os._exit(1) 
            w_sleep(60)
            print("Retrying with next available data set...")
        w_sleep(1)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ENDC = '\033[0m'


#class InterruptHandler:
#    def __init__(self):
#        self.interrupted = False
#
#    def handle_signal(self, signum, frame):
#        if self.interrupted:
#            print("Quitting now!")
#            try:
#                sys.exit(1)
#            finally:
#                os._exit(1)
#        else:
#            print("Quitting in 10 sec!")
#            self.interrupted = True
#            time.sleep(10)
#            try:
#                sys.exit(1)
#            finally:
#                os._exit(1)
#interrupt_handler = InterruptHandler()
#signal.signal(signal.SIGINT, interrupt_handler.handle_signal)

main()
