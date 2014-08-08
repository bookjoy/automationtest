import yaml
import operatefile as operatefile
import com.util.constants as cons
import handleexception as exception

file_suffix = '.yaml'
def readyaml(filepath):

        f = open(filepath)
        dataMap = yaml.load(f)
        f.close()
        return dataMap                   

def get_global_datas():
        filepath = operatefile.get_sys_path() + operatefile.is_right_path(cons.GLOBAL_FILEPATH)
        datas = readyaml(filepath)
        return datas

def get_all_tests():
        filepath = operatefile.get_sys_path() + operatefile.is_right_path(cons.TESTSUITE_FILEPATH)
        datas = readyaml(filepath)
        return datas

def get_test_datas(filename):
        
        if len(filename.split('.')) == 1:
            filename = filename.lower() + file_suffix
        path = operatefile.get_sys_path() + operatefile.is_right_path(cons.ELEM_TESTDATAS_PATH) + filename
        
        datas = readyaml(path)
        return datas

def get_elem_datas():
        
        path = operatefile.get_sys_path() + operatefile.is_right_path(cons.ELEM_YAML_PATH)
        datas = readyaml(path)
        return datas

def get_case_steps(filename):
        if len(filename.split('.')) == 1:
            filename = filename.lower() + file_suffix
        path = operatefile.get_sys_path() + operatefile.is_right_path(cons.CASE_STEP_PATH) + filename
        
        datas = readyaml(path)
        return datas


#def is_right_path(path):
        
#        if path[0] is not '/':
#                msg = 'The path \''+ path+'\' must end with \'/\' !'
#                raise exception.HandleException().NOT_FOUND_ERR(msg)

#        if path[len(path)-1] is not '/':
#                msg = 'The path \''+ path+'\' must begin with \'/\' !'
#                raise exception.HandleException().NOT_FOUND_ERR(msg)
        
#        return path

if __name__ == '__main__':
        is_right_path('login')

