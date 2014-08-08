#import com.util.parseyaml as yaml
import unittest
import com.util.operatefile as opfile
#import com.testcase.login as login

#m_index = {'login':login.Login}

def add_test_method(methods):
        suite = unittest.TestSuite()
        for key in methods.keys():
                if key.lower() in m_index:
                        for val in methods[key.lower()].values():
                                suite.addTest(m_index[key.lower()](val))
        return suite
        
def all_tests(methods):
        suites = []
        for key in methods.keys():
                if key.lower() in m_index:
                        suite = unittest.TestLoader().loadTestsFromTestCase(m_index[key.lower()])
                        suites.append(suite)
        alltest = unittest.TestSuite(suites)
        return alltest

def all_testsuite():
    
    path = opfile.get_sys_path() #+ 'com/testcase'
    discover = unittest.defaultTestLoader.discover(path, pattern='*.py',top_level_dir=None)
    print 'discover = %s'%discover
    suite = unittest.TestSuite()
    for tests in discover:
        for test_case in tests:
            suite.addTests(test_case)
    return suite
