import HTMLTestRunner
import unittest
import operatefile
import timestring

class HTMLReport:
	def __init__(self):
                pass

	def genater_report(self, testsuite):
		path = operatefile.get_sys_path()
		name = 'report' + timestring.number_of_string() + '.html'
		filename = path +'report/' + name
		print 'HTMLReport.path =',path
		try:
                        fp = file(filename,'wb')
                        runner = HTMLTestRunner.HTMLTestRunner(stream=fp,title='Result',description='Test_Report')
                        runner.run(testsuite)
			fp.close()
                except IOError as err:
                        print('File Error:',str(err))

                        

