# import all necessary modules
from selenium import webdriver
import json
import requests
import random
from subprocess import Popen
import time

# username & authkey credentials to be passed in
username = "username@mail.com"
authkey  = "demdigits"

# include CBT api
response = requests.get("https://crossbrowsertesting.com/api/v3/selenium/browsers")

# sanity checking to make sure there is a response
print(response)         

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

# create function for testing
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
   
    # if the title is the same, then print result otherwise print opposite result
    if "Megaman" == driver.title:
        test_result = 'pass'
        print('Test has passed!  :)')
    else:
        test_result = 'fail'
        print('Test has failed!')
    
    # if test result exists, set the score
    if test_result is not None:
        api_session.put('https://crossbrowsertesting.com/api/v3/selenium/' + driver.session_id,
                data={'action':'set_score', 'score':test_result})
    driver.quit()


# Run cbt_tunnel in the background while performing test
p = Popen(['C:/Users/Alakazam/Documents/SE_Assignment/cbt-tunnels-win64.exe',  '--username', 'username@mail.com', '--authkey', 'demdigits'])
time.sleep(10)          # make sure enough time to open tunnel before beginning 
runTest(winBrowsers)    # test random Windows browser
runTest(macBrowsers)    # test random Mac browser
runTest(mobileBrowsers) # test random Mobile browser
p.terminate()           # terminate tunnel after last test finishes







