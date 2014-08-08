#-*- coding: utf-8 -*-
import sys,time,datetime,os,logging
import handleexception as exception

def setting():
    log_format='%(filename)s [%(asctime)s] [%(levelname)s] %(message)s'
    logging.basicConfig(format=log_format,datefmt='%Y-%m-%d %H:%M:%S %p',level=logging.DEBUG)


def get_sys_path():
	_syspath = sys.path[0]
	_syspath = _syspath.replace("\\","/") + '/'
	return _syspath

def is_right_path(path):
        
        ##if path[0] is not '/':
        #if not path.startswith('/'):
        #        msg = 'The path \''+ path+'\' must end with \'/\' !'
        #        raise exception.HandleException().NOT_FOUND_ERR(msg)

        ##if path[len(path)-1] is not '/':
        #if not path.endswith('/'):
                
         #       msg = 'The path \''+ path+'\' must begin with \'/\' !'
          #      raise exception.HandleException().NOT_FOUND_ERR(msg)
        if not path.startswith('/'):
                path = '/' + path
                
        if not path.endswith('/'):
                path = path + '/'
        return path

if __name__ =='__main__':
        is_right_path('/test/')



