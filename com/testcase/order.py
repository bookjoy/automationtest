#-*-coding:utf-8-*-
import time
import sys
import com.base.testbase as testbase
import com.base.locator as locator
import com.util.constants as cons
from selenium import webdriver

class Order(testbase.TestBase):

    def test_order_submit(self):

        driver = self.driver
        filename = self.__class__.__name__
        current_method = sys._getframe().f_code.co_name
        loc = locator.Locator(driver, cons.DEFAULT_LOGIN_CLASS, cons.DEFAULT_LOGIN_CLASS)
        loc.elem_locator()
        loc = locator.Locator(driver, filename, current_method)
        text = loc.elem_locator()
        assert_value = loc.get_assert_value()
        asssert_result = loc.exac_assert(assert_value)
        exec asssert_result

    def test_order_confirm(self):

        driver = self.driver
        filename = self.__class__.__name__
        current_method = sys._getframe().f_code.co_name
        loc = locator.Locator(driver, cons.DEFAULT_LOGIN_CLASS, cons.DEFAULT_LOGIN_CLASS)
        loc.elem_locator()
        loc = locator.Locator(driver, filename, current_method)
        text = loc.elem_locator()
        assert_value = loc.get_assert_value()
        asssert_result = loc.exac_assert(assert_value)
        exec asssert_result

