# encoding: utf-8

import sys
import urllib2
import re
import logging
import time

reload(sys)
sys.setdefaultencoding('utf8')

MAX_TRIES = 3
ERROR_SLEEP_TIME = 5
URL_READ_TIMEOUT = 20

def _getWebResponse(url, encoding=""):
    html = ""
    resp = urllib2.urlopen(url, timeout=URL_READ_TIMEOUT)
    try:
        html = resp.read()
        if len(encoding)>0:
            html = html.decode(encoding)
    finally:
        resp.close()
    return html

def getWebResponse(url,encoding=""):
    tries = 0
    while tries < MAX_TRIES:
        tries += 1
        html = ""
        try:
            html = _getWebResponse(url,encoding)
        except Exception as e:
            logging.error(e)
            time.sleep(ERROR_SLEEP_TIME)
            continue
        return html
    logging.error('FAILED to get HTML response, url = %s' %url)
    return ""



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

def removeHTMLTags(html,replacement=''):
    dr = re.compile(r'<[^>]+>',re.S)
    dd = dr.sub(replacement,html)
    return dd