from selenium import webdriver
import json
import requests
import random
from subprocess import Popen
import time


username = "wright.alan88@gmail.com"
authkey  = "u934d2edac9ad5a0"



# include CBT api
response = requests.get("https://crossbrowsertesting.com/api/v3/selenium/browsers")

# create dictionary for devices
device_list = json.loads(response.text)

# create function to filter dictionaries
def filterList(criteriaKey, criteriaValue, collection):
        return list(filter(lambda x: x[criteriaKey] == criteriaValue, collection))

# filter dictionaries 
mobileList = filterList('device', 'mobile', device_list)
desktopList = filterList('device', 'desktop', device_list)
macList = filterList('type', 'Mac', desktopList)
windowsList = filterList('type', 'Windows', desktopList)

# grab random browser for each category
winBrowsers = random.choice((random.choice(windowsList))['browsers'])
macBrowsers = random.choice((random.choice(macList))['browsers'])
mobileBrowsers = random.choice((random.choice(mobileList))['browsers'])


def runTest(browser):
    api_session = requests.Session()
    api_session.auth = (username, authkey)
    test_result = None
    caps = {}
    caps['browser_api_name'] = browser['api_name']
        
    driver = webdriver.Remote(
        desired_capabilities=caps,
        command_executor="http://%s:%s@hub.crossbrowsertesting.com:80/wd/hub"%(username, authkey)
    )
    driver.implicitly_wait(20)
    driver.get('http://local:8000/Megaman.html')
    if "Megaman" == driver.title:
        test_result = 'pass'
        print('Test has passed!  :)')
    else:
        test_result = 'fail'
        print('Test has failed!')
    
    if test_result is not None:
        api_session.put('https://crossbrowsertesting.com/api/v3/selenium/' + driver.session_id,
                data={'action':'set_score', 'score':test_result})
    driver.quit()

p = Popen(['C:/Users/Alakazam/Documents/SE_Assignment/cbt-tunnels-win64.exe',  '--username', 'wright.alan88@gmail.com', '--authkey', 'u934d2edac9ad5a0'])
time.sleep(30)
print(response)
runTest(winBrowsers)
print(response)
runTest(macBrowsers)
print(response)
runTest(mobileBrowsers)
print(response)
p.terminate()
