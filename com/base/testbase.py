#-*-coding:utf-8-*-
import unittest
import com.util.parseyaml as parseyaml
import com.util.manager as manager
import inspect
import sys
from selenium import webdriver

class TestBase(unittest.TestCase):

        def setUp(self):
            #run_class = self.__class__.__name__

            datas = parseyaml.get_global_datas()
            self.driver = manager.driver_controll(datas)
            url = datas['common']['url']
            self.driver.get(url)
            #self.driver.maximize_window(d)
            #self.driver.set_window_size(240, 400)
                        
        def tearDown(self):
            driver = self.driver
            driver.close()
            driver.quit()
        

		
