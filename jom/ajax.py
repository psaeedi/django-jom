'''
Copyright PuzzleDev s.n.c.
Created on Jul 24, 2012

@author: Michele Sama (m.sama@puzzledev.com)
'''
import datetime
import json
import traceback
import sys

from django.http import HttpResponse


def parseDateTime(date_string):
    try:
        date = datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S.%f')
    except:
        date = datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
    return date

#----------------
RESULT = "result"
MESSAGE = "message"


def json_message(dictionary):
    return json.dumps(dictionary)


def json_response(result, dictionary = {}, message = None):
    dictionary[RESULT] = result
    if message:
        dictionary[MESSAGE] = message
    return json_message(dictionary)


def json_true(dictionary = {}, message = None):
    return json_response(True, dictionary, message)


def json_false(dictionary = {}, message = None):
    return json_response(False, dictionary, message)


class AjaxResponse(object):
    """ Creates an ajax response
    """ 
    
    def __call__(self, original_fz):
        def _decorated_fz(request, *args, **kwargs):         
            if request.method == 'GET':
                return HttpResponse(json_false(message = "Request should be a POST"),
                        content_type = "application/json") 
            
            try:
                result, dictionary, message = original_fz(request, *args, **kwargs)
                return HttpResponse(json_response(result, dictionary, message),
                        content_type = "application/json") 
            except Exception, err:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_tb(exc_traceback, limit = 10, file = sys.stdout)
                return HttpResponse(json_false(message = "%s" % err),
                        content_type = "application/json") 
        return _decorated_fz
    