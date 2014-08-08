# -*- coding: utf-8 -*-
import os,sys,copy,shutil
import com.util.common as common
import com.util.timestring as timestring
import com.util.constants as cons
import com.util.handleexception as exception
import parseyaml

file_suffix = '.py'
def get_sys_path():
	_syspath = sys.path[0]
	_syspath = _syspath.replace("\\","/") + '/'
	return _syspath

def is_right_path(path):
	if path.startswith('/'):
		path = path[1:] #remove bias which is at the begin

	lenght = len(path.split('.'))
	if lenght == 1 and not path.endswith('/'):#add bias at the end if 'path' is not a file
		path = path + '/'
	return path

def read_file(filepath):
	content = ''
	try:
		content = file(filepath,'r').read()
	except IOError as err:
		print "IOError:",str(err)
	return content 

def read_tempate(classname):
	filepath = get_sys_path() + is_right_path(cons.TEMPLATE_FILEPATH)

	contents = read_file (filepath)
	lineNum = contents.find('METHOD')
	if lineNum > -1:
		class_contents = contents[:lineNum-8]
		method_contents = contents[lineNum-8:]
	#lineNum = contents.find('METHOD')
	#if lineNum > -1:
		method_contents = contents[lineNum-8:]
		#print 'method_contents=%s'%method_contents

	class_text,method_text = class_contents,method_contents
	return class_text,method_text
		
			
def is_exist(filename, pattern):

	path = get_sys_path() + is_right_path(cons.CREATE_TESTClASS_FILEPATH) + is_right_path(filename + file_suffix)
	
	result = False
	if not os.path.exists(path):
		#content = read_lines(filename)
		return result
	else:
		content = read_file(path)
		if content.find(pattern) > -1 :

			result = True
		return result
	
def read_lines(classname):
	filepath = get_sys_path() + is_right_path(cons.TEMPLATE_FILEPATH)
	file_content = list()
	
	try:
		f = open(filepath,'r')
		for line in f.readlines():

			if line.find('CLASSNAME') > -1:
				line = line.replace("CLASSNAME",classname.capitalize())
				file_content.append(line)
				file_content.append('\n')
				break
			file_content.append(line)

	except IOError as err:
			raise exception.HandleException().NOT_FOUND_ERR(str(err))
	return file_content

def find_files():
	path = get_sys_path() + is_right_path(cons.CASE_STEP_PATH)
	filelist = {}
	for file in os.listdir(path): 
		if file.split('.')[1] == 'yaml':# and file not in 'logininit.yaml':
			datas = parseyaml.get_case_steps(file)
			filelist[file] = datas

	return filelist

def get_key_from_dic(datas):
	keys = []
	for key in datas.keys():
		keys.append(key)
	return keys

def get_line_num(filepath):
	
	try:
		f = open(filepath,'r')
		#file = copy.deepcopy(f)
		lineNum = 0
		for line in f.readlines():
			
			lineNum = lineNum + 1
			if line.find('METHOD') > -1:
				break
		f.close()
	except IOError as err:
			raise exception.HandleException().NOT_FOUND_ERR(str(err))
	
	return lineNum

def read_lines_for_method(methodname):
	filepath = get_sys_path() + is_right_path(cons.TEMPLATE_FILEPATH)
	file_content = list()
	lineNum = get_line_num(filepath)
	
	try:
		f = open(filepath,'r')
		for line in f.readlines()[lineNum-1:]:

			if line.find('METHOD') > -1:
				line = line.replace('METHOD',methodname)
			file_content.append(line)
		#file_content.append('\n')
		f.close()

	except IOError as err:
		raise exception.HandleException().NOT_FOUND_ERR(str(err))
	
	return file_content


def create_file(filepath):

	try:
		f = open (filepath, 'w' )
		f.close()
	except IOError as err:
		#raise exception.HandleException().NOT_FOUND_ERR(str(err))
		print "Error Found:%s"%str(err)
			

def is_dir(filepath):
	try:
		os.path.isdir(filepath)
	except IOError as err:
		msg = 'Folder Error : [%s] is not a folder! Detail error:%s'%(filepath,str(err))
		raise exception.HandleException().NOT_FOUND_ERR(msg)
        
def is_file(filepath):
	try:
		result = os.path.isfile(filepath)
	except IOError as err:
		msg = 'File Error : [%s] is not a file! Detail error:%s'%(filepath,str(err))
		raise exception.HandleException().NOT_FOUND_ERR(msg)
	return result

def make_dirs(filepath):
	try:
		if not os.path.exists(filepath):
			result =  os.makedirs(filepath)
		else:
			result = True
	except IOError as err:
		msg = 'Make Directs Error : ',str(err)
		raise exception.HandleException().NOT_FOUND_ERR(msg)
	return result

def create_case_file(filename):
	path = get_sys_path() + is_right_path(cons.CREATE_TESTClASS_FILEPATH)       
	if make_dirs(path):
		filepath = path + is_right_path(filename + file_suffix) 
		#print 'create_case_file =',filepath
		create_file(filepath)
        
def write_case_file(filename, contents):
	path = get_sys_path() + is_right_path(cons.CREATE_TESTClASS_FILEPATH)
	filepath = path + is_right_path(filename + file_suffix)
	write_file(filepath, contents) #create testcases files
                        
def write_file(filepath, contents):
	try:
		f = open(filepath, 'a+')  #a     以追加模式打开 
		f.write(contents)
		f.close()
	except IOError as err:
		raise exception.HandleException().NOT_FOUND_ERR(str(err))

def write_testdata_file(filename, method, contents):
	filepath = get_sys_path() + is_right_path(cons.ELEM_TESTDATAS_PATH) + filename
	#contents = read_file(filepath)
	#print 'write_testdata_file.contents=',contents
	#if contents.find(method) > -1:
	write_file(filepath, contents) #create testdata files


def create_testdata_file(filename,contents):
	filepath = get_sys_path() + is_right_path(cons.ELEM_TESTDATAS_PATH)+ filename  
	if not is_file(filepath):
		write_file(filepath,contents)
		return False
	else:
		return True	

def post_keyword(filename,method,post_content):
	filepath = get_sys_path() + is_right_path(cons.ELEM_TESTDATAS_PATH)+ filename  
	contents = read_file(filepath)
	
	if contents.find(method) > -1:
		contents = contents.replace(method,post_content)
		write_file_byw(filepath, contents)

def write_file_byw(filepath, contents):
	try:
		f = open(filepath, 'w')
		f.write(contents)
		f.close()
	except IOError as err:
		raise exception.HandleException().NOT_FOUND_ERR(str(err))
	
def back_cases_file():
	source_dir = get_sys_path() + is_right_path(cons.CREATE_TESTClASS_FILEPATH)
	backup_dir = get_sys_path() + is_right_path(cons.BACKUP_TESTClASS_FILEPATH)
	folder = timestring.number_of_string()

	backup_dir = backup_dir + is_right_path(folder)
	shutil.copytree(source_dir,backup_dir)
        
if __name__ == "__main__":
        print is_right_path('com')
