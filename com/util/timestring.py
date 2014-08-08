#-*-coding:utf-8-*-
import datetime

def time_string():
    return datetime.datetime.now()
    

def number_of_string():
    now = time_string()
    date_string = now.strftime('%Y%m%d%H%M%S')
    return date_string

def get_time_string():
    #%Y-%m-%d %H:%M:%S
    now = time_string()
    return now.strftime('%Y-%m-%d %H:%M:%S')
