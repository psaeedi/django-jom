'''
Created on Aug 5, 2012

@author: Michele Sama (m.sama@puzzledev.com)
'''
from django.conf.urls import patterns, url
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    url('^test/$', direct_to_template, {
        'template': 'foo/test.html'
    }));