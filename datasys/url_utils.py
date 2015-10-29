# encoding: utf-8

import sys
import urllib2

reload(sys)
sys.setdefaultencoding('utf8')

def getWebResponse(url, encoding=""):
    html = ""
    resp = urllib2.urlopen(url)
    try:
        html = resp.read()
        if len(encoding)>0:
            html = html.decode(encoding)
    finally:
        resp.close()
    return html


def removeJsonP(jsonp_str):
    index1 = jsonp_str.find('(')+1
    index2 = len(jsonp_str) - jsonp_str[::-1].find(')')-1
    return jsonp_str[index1:index2]


def getStringBetween(str, str_begin, str_end):
    index1 = str.find(str_begin)
    index2 = str.find(str_end,index1)
    if index1 < 0 or index2 < 0:
        return str
    return str[index1+len(str_begin):index2]


