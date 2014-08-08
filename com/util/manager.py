import os
import com.util.common as common
from selenium import webdriver

CHROME_BROW = 'chrome'
FIREFOX_BORW = 'firefox'
IE_BROW = 'ie'
IE_PROFILE = 'webdriver.ie.driver'
CHROME_PROFILE = 'webdriver.chrome.driver'
BROW_TITLE = 'brow'
BROW_NAME = 'name'
BROW_DRIVER = 'driver'

def driver_controll(datas):

    driverpath = common.get_sys_path() + 'driver/'
    brow = datas[BROW_TITLE][BROW_NAME]
    if brow.lower() not in(CHROME_BROW, FIREFOX_BORW, IE_BROW):
        print 'Brow[%s] must be in the list [%s, %s, %s]'%(brow, CHROME_BROW, FIREFOX_BORW, IE_BROW)

    brow_driver = driverpath + datas[BROW_TITLE][BROW_DRIVER]
    if brow.lower() == CHROME_BROW:
        
        os.environ[CHROME_PROFILE] = brow_driver
        driver = webdriver.Chrome(brow_driver)
        
    elif brow.lower() == FIREFOX_BORW:
        #firefox_driver = driverpath + 'chromedriver.exe'
        #os.environ["webdriver.ie.driver"] = firefox_driver
        print '========='
        driver = webdriver.Firefox()
        #driver = webdriver.FireFox(firefox_driver)
        
    elif brow.lower() == IE_BROW:
        os.environ[IE_PROFILE] = brow_driver
        driver = webdriver.Ie(brow_driver)
        #driver = webdriver.Ie()
    #driver.set_window_size(240, 400)
    return driver
        
