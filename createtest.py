#-*-coding:utf-8-*-
import com.util.operatefile as opfile
import com.util.parseyaml as parseyaml
import com.util.constants as cons

class CreateTests():
    def __init__(self):
        self.assert_txt = '  assert:\n    expect_value: \n    message: \n'
        self.encoding = '#-*-coding:utf-8-*-\n'
        
    def create_case_and_data_file(self):
        
        filelist = opfile.find_files()
        self.create_case_file(filelist)
        self.create_datas_file(filelist)

    def create_datas_file(self, filelist):
        data_content = ''
        for filename in filelist.keys():
            self.create_testdata_file(filelist,filename)
            self.write_method_and_keyword(filelist,filename)

    def create_testdata_file(self, filelist,filename):
        encoding = self.encoding
        assert_txt = self.assert_txt
        content =''
        for method in filelist[filename].keys():
            content += method + ':\n' + assert_txt
            #content += assert_txt
        content = encoding + content
        result = opfile.create_testdata_file(filename,content)
        return result
            
    def write_method_and_keyword(self, filelist,filename):
        data_content = ''
        assert_txt = self.assert_txt
        test_datas = parseyaml.get_test_datas(filename)
        #print 'write_method_and_keyword_insert.test_datas=%s'%test_datas
        for method in filelist[filename]:
            text_str = ''
            assert_txt = self.assert_txt
            text_str = ''

            if method not in test_datas.keys():
                for actions  in filelist[filename][method]:
                    for (key, action) in actions.items():
                        print 'key=%s , action =%s'%(key, action)
                        if action == 'input':
                            key = '  ' + key
                            text_str += key + ': \n' 
                #if text_str !='':
                data_content += method + ':\n' + text_str + assert_txt
                #data_content += text_str + assert_txt
                #print 'data_content=%s'%data_content
                opfile.write_testdata_file(filename, method, data_content)
            else:
            #self.insert_method(filelist,filename,method,test_datas)
                self.insert_keyword(filelist,filename,method,test_datas)

#    def insert_method(self, filelist, filename, method, test_datas):
#        text_str = ''
#        data_content=''
#        assert_txt = self.assert_txt
#        for method in filelist[filename]:
#            text_str = ''
#            if method not in test_datas.keys():
#                for actions in filelist[filename][method]:
#                    for (key, action) in actions.items():
#                        if action == 'input':
#                            key = '  ' + key
#                            text_str += key +': \n'
#                if text_str !='':
#                    data_content = method + ':\n' + text_str + assert_txt
#                    data_content = data_content[0:-1]
#                    opfile.write_testdata_file(filename, method, data_content)
#            else:
#                self.insert_keyword(filelist,filename,method,test_datas)

    def insert_keyword(self, filelist, filename, method, test_datas):
        text_str = ''
        data_content=''
        assert_txt = self.assert_txt
        
        for actions  in filelist[filename][method]:
            for (key, action) in actions.items():
                if action == 'input' and (test_datas[method] is None or key not in test_datas[method].keys()):
                    key = '  ' + key
                    text_str += key +': \n' 
        #if text_str !='':
        data_content += method + ':\n' + text_str
        
        if test_datas[method] is None:
            data_content += assert_txt
        
        data_content = data_content[0:-1]
        opfile.post_keyword(filename,method+':',data_content)


#    def write_method_and_keyword_insert(self, filelist,filename):
#        data_content = ''
#        assert_txt = self.assert_txt
        
#        for method in filelist[filename]:
#            print 'write_method_and_keyword_insert.filelist[filename][method]=%s'%filelist[filename][method]
#            text_str = ''
#            for actions in filelist[filename][method]:
#                for (key, action) in actions.items():
#                    if action == 'input':
#                        key = '  ' + key
#                        text_str += key + ': \n' 
#            if text_str !='':              
#                data_content += method + ':\n'
#                data_content += text_str + assert_txt
#            
#        opfile.write_testdata_file(filename, method, data_content)
    def create_case_file_byline(self, filelist):
        
        for filename in filelist.keys():
            clazzname = filename.split(".")[0]
            
            if clazzname != cons.DEFAULT_LOGIN_CLASS:
                if opfile.is_exist(clazzname, clazzname.capitalize()) == False:
                    '''read contents from template file'''
                    content = opfile.read_lines(clazzname)
                    '''write class to testcases file'''
                    for line in content:
                        opfile.write_case_file(clazzname,str(line))
                
                for method in filelist[filename].keys(): 
                    if opfile.is_exist(clazzname, method) == False:
                        '''read contents from template file'''
                        method_content = opfile.read_lines_for_method(method)
                        '''write method to testcases file'''
                        for line in method_content:
                            opfile.write_case_file(clazzname,str(line))
            
    def create_case_file(self, filelist):
        
        for filename in filelist.keys():
            clazzname = filename.split(".")[0]
            class_text, method_text = opfile.read_tempate(clazzname)
            method_content = ''
            class_content ='' 
            if clazzname != cons.DEFAULT_LOGIN_CLASS:
                if opfile.is_exist(clazzname, clazzname.capitalize()) == False:
                    class_content = class_text.replace('CLASSNAME',clazzname.capitalize())

                for method in filelist[filename].keys():
                    if opfile.is_exist(clazzname, method) == False:
                        method_content += method_text.replace('METHOD',method)
                file = class_content + method_content
                opfile.write_case_file(clazzname,file)
                

if __name__ == "__main__":
    CreateTests().create_case_and_data_file()


