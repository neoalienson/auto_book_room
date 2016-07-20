#!/usr/bin/python

# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re, sys, datetime

class Autobook(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = conf['url']
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_autobook(self):
        global conf
        driver = self.driver
        driver.get(self.base_url + "/owa/auth/logon.aspx?url=" + conf['url'] + "/owa/&reason=0")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys(conf['password'])
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys(conf['username'])
        driver.find_element_by_css_selector("input.btn").click()
        driver.find_element_by_id("lnkNavCal").click()
        driver.find_element_by_id("lnkHdrnewmtng").click()
        driver.find_element_by_id("txtbcc").clear()
        driver.find_element_by_id("txtbcc").send_keys(conf['room'])

        target = datetime.datetime.now()  + datetime.timedelta(days=21)
        year = target.strftime("%Y")
        month = target.strftime("%B")
        day = target.strftime("%d").strip("0")
        Select(driver.find_element_by_name("selSM")).select_by_visible_text(month)
        Select(driver.find_element_by_name("selSD")).select_by_visible_text(day)
        Select(driver.find_element_by_name("selSY")).select_by_visible_text(year)
        Select(driver.find_element_by_name("selST")).select_by_visible_text(conf['from'])
        Select(driver.find_element_by_name("selET")).select_by_visible_text(conf['to'])
        driver.find_element_by_id("txtsbj").clear()
        driver.find_element_by_id("txtsbj").send_keys("ECM")
        driver.find_element_by_id("lnkHdrsend").click()
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit('please provide configuration file')
    conf = eval(open(sys.argv[1]).read())
    del sys.argv[1:]
    unittest.main()
