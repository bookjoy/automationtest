#-*-coding:utf-8-*-
import unittest
import com.testcases as testcases
import com.util.htmlreport as htmlreport

from selenium import webdriver

def main():
    suite = testcases.all_testsuite()
    report = htmlreport.HTMLReport()   #call HTMLReport class
    report.genater_report(suite)
    
if __name__ == "__main__":
    main()
