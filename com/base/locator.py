#-*-coding:utf-8-*-
import time
import com.util.parseyaml as parseyaml
import com.util.constants as cons
import com.util.handleexception as exception
import com.util.operatefile as opfile
from selenium.webdriver.support.ui import Select

operator_list =['equal','notequal','true','false','is','isnot','none','isnotnone','in','notin','greater','greaterequal','less','lessequal']

class Locator():
    def __init__(self, driver, filename, method):
        self.global_datas = {}        
        self.driver = driver
        self.filename = filename.lower()
        self.method = method
        self.driver = driver
        self.case_steps = parseyaml.get_case_steps(filename) ##return a array
        self.elem_datas = parseyaml.get_elem_datas() ##return a hash
        self.test_datas = parseyaml.get_test_datas(filename) ##return a hash
        self.global_datas = parseyaml.get_global_datas()
        #print 'case_steps=',self.case_steps
        #print 'elem_datas=',self.elem_datas
        #print 'test_datas=',self.test_datas

    def get_locator(self, key):
        
        self.elem_is_present(key)
        self.wait_for_elem()
        datas = self.elem_datas
        return self.find_elem(datas[key]['locator_type'],datas[key]['locator_value'])
        
    def wait_for_elem(self):
        
        global_datas = self.global_datas
        wait_times = global_datas['common']['waittime']  
        self.driver.implicitly_wait(wait_times) # seconds
        
    def elem_is_present(self, key):
        result = True
        if key not in self.elem_datas:
            msg = 'Element Error : Element [%s] is not definded in %s file'%(key,cons.ELEM_YAML_PATH)
            print msg
            result = False
        return result
    
    def find_elem(self, elem_type, elem_value):
        driver = self.driver

        try:
            if elem_type.lower() == 'id':
                element = driver.find_element_by_id(elem_value)
            elif elem_type.lower() == 'name':
                element = driver.find_element_by_name(elem_value)
            elif elem_type.lower() == 'xpath':
                element = driver.find_element_by_xpath(elem_value)
            elif elem_type.lower() == 'link':
                element = driver.find_element_by_link_text(elem_value)
            elif elem_type.lower() == 'partial':
                element = driver.find_element_by_partial_link_text(elem_value)
            elif elem_type.lower() == 'tag':
                element = driver.find_element_by_tag_name(elem_value)
            elif elem_type.lower() == 'class':
                element = driver.find_element_by_class_name(elem_value)
            elif elem_type.lower() == 'css':
                element = driver.find_element_by_css_selector(elem_value)
        except Exception as err:
            url_title = driver.title
            msg = 'Locator Error : Element is not found with [%s] and [%s] in the page [%s]'%(elem_type, elem_value, url_title)
            print msg
        return element
    
    def locator_event(self, case_step):
        for (key, action) in case_step.items():
            if key not in('assert') and self.elem_is_present(key):
                self.do_action(key, action)
                
    def do_action(self,elem_key, action):
        try:
            
            elem_datas = self.elem_datas
            if len(action.split('-')) > 1:
                action, index = action.split('-')
                print 'index =',index
            self.wait_for_elem()
            if action == 'switchtof':
                print 'action=',elem_datas[elem_key]['locator_value']
                self.driver.switch_to_frame(elem_datas[elem_key]['locator_value'])
            elif action == 'switchtow':
                self.driver.switch_to_window(elem_datas[elem_key]['locator_value'])
            elif action == 'click':
                elem = self.find_elem(elem_datas[elem_key]['locator_type'],elem_datas[elem_key]['locator_value'])
                elem.click()
            elif action == 'input':
                value = self.get_test_data(elem_key)
                elem = self.find_elem(elem_datas[elem_key]['locator_type'],elem_datas[elem_key]['locator_value'])
                elem.send_keys(value)
            elif action in('radio','checkbox'):
                #inputs = self.find_elem('tag','input')
                inputs = self.driver.find_elements_by_tag_name('input') 
                radios = []
                if index.lower() == 'all':
                    for i in range(0, len(inputs)):
                        if inputs[i].get_attribute('type') == action:
                            inputs[i].click()
                else:
                    for i in range(0, len(inputs)):
                        if inputs[i].get_attribute('type') == action:
                            radios.append(inputs[i])
                    radios[int(index)].click()
                    #for i in len(radios):
                     #   radios[int(i)].click()
                #else:
                    

                self.driver.implicitly_wait(10)
            elif action == 'select':
                m = self.find_elem(elem_datas[elem_key]['locator_type'],elem_datas[elem_key]['locator_value'])
                time.sleep(2)
                m.find_elements_by_tag_name('option')[int(index)].click()
                
                #select = Select(driver.find_element_by_tag_name("cityId"))
                #select.deselect_all()
                #select.select_by_visible_text(u"三明市")
            elif action == 'file':
                
                value = self.get_test_data(elem_key)
                elem = self.find_elem('name',elem_datas[elem_key]['locator_value'])
                elem.send_keys(value)
                
            elif action == 'script':
                js = self.get_test_data(elem_key)
                script_exce(js)
            else:
                print '===============other============'

        except Exception as err:
            print 'Error Found : Element key is [%s]. Error:%s'%(elem_key,str(err))

    def script_exce(id):
        #js ='var obj = document.getElementById("'+ id +'");obj.setAttribute("readOnly",false);' 
        self.driver.execute_script(js)
        
    def get_test_data(self, elem_key):
        test_datas = self.test_datas
        mehtod = self.method
        value = ''
        if mehtod in test_datas.keys() and elem_key in test_datas[mehtod].keys():
            value = test_datas[mehtod][elem_key]
            if value == None:
                value = ''
        else:
            filename = opfile.is_right_path(cons.ELEM_TESTDATAS_PATH) + self.filename.lower() + '.yaml'
            msg = 'Error Found: Data for [%s:%s] is not defined in the yaml file[%s]'%(mehtod, elem_key, filename)
            print msg
        return value

    def get_expect_value(self):
        expect_value = []
        try:
            filename = self.filename + '.yaml'
            method = self.method
            test_datas = self.test_datas
            if test_datas is None:
                print 'Error Found : Assert value is not defined in the yaml file[%s]'%filename
            else:
                expect_value = test_datas[method]['assert']
        except TypeError as typeer:
            print str(typeer)
        return expect_value

    def elem_locator(self):
        case_steps = self.case_steps
        method = self.method
        for case_step in case_steps[method]:

            self.locator_event(case_step)

    def get_assert_value(self):
        method = self.method
        case_steps = self.case_steps
        array_value = case_steps[method]  ##return a array
        result = []
        elem_datas = self.elem_datas
        for action_value in array_value:
            for (assert_key,assert_value) in action_value.items():
                if assert_key == 'assert':
                    for elem_value in assert_value.values():
                        result.append(elem_value)
        return result

    def exac_assert(self,assert_value):
        operator = assert_value[0]
        by_id = assert_value[1]
        script =''
        if operator not in ['true','false','isnone','isnotnone']:
            expect_values = self.get_expect_value()
            message = expect_values['message']
            expect_value = expect_values['expect_value']

        fact_value = self.get_text(by_id)
        if operator not in operator_list:
            print 'Error Found: operator[%s] must be one of list{%s}'%(operator,operator_list)
            
        elif operator.lower() == 'equal':
            
            print 'expect_value = \'%s\', fact_value= \'%s\''%(expect_value, fact_value)
            script = 'self.assertEqual(\'%s\', \'%s\')'%(expect_value, fact_value)
        elif operator.lower() == 'notequal':
            
            script = 'self.assertNotEqual(\'%s\', \'%s\')'%(expect_value, fact_value)
        elif operator.lower() == 'true':
            
            script = 'self.assertTrue(%s)'%(fact_value)
        elif operator.lower('false'):
            
            script = 'self.assertFalse(%s)'%(fact_value)
        elif operator.lower('is'):
            
            script = 'self.assertFalse(%s)'%(fact_value)
        elif operator.lower('isnot'):
            
            script = 'self.assertIsNot(%s, %s)'%(expect_value, fact_value)
        elif operator.lower('isnone'):
            
            script = 'self.assertIsNone(%s)'%(fact_value)
        elif operator.lower('isnotnone'):
            
            script = 'self.assertIsNotNone(%s)'%(fact_value)
        elif operator.lower('in'):
            
            script = 'self.assertIn(%s, %s)'%(expect_value, fact_value)
        elif operator.lower('notin'):
            
            script = 'self.assertNotIn(%s, %s)'%(expect_value, fact_value)
        elif operator.lower('greater'):
            
            script = 'self.assertGreater(%s, %s)'%(expect_value, fact_value)
        elif operator.lower('greaterequal'):
            
            script = 'self.assertGreaterEqual(%s, %s)'%(expect_value, fact_value)
        elif operator.lower('less'):
            
            script = 'self.assertLess(%s, %s)'%(expect_value, fact_value)
        elif operator.lower('lessequal'):
            
            script = 'self.assertLessEqual(%s, %s)'%(expect_value, fact_value)

        return script

            
    def get_text(self,elem_key):
        elem_datas = self.elem_datas
        if elem_key == 'title':
            text = self.driver.title
        elif elem_key == 'url':
            text = self.driver.current_url
        else:
            text = self.find_elem(elem_datas[elem_key]['locator_type'],elem_datas[elem_key]['locator_value']).text
        
        return text