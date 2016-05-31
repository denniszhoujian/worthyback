#encoding: utf-8
import re

REGEX_DICT = {}

def get_compiled_regex(regex_str):
    if regex_str in REGEX_DICT:
        return REGEX_DICT[regex_str]
    else:
        pt = re.compile(regex_str,re.IGNORECASE)
        REGEX_DICT[regex_str] = pt
        return pt


REGEX_DICT_U = {}

def get_compiled_regex_unicode(regex_str):
    if regex_str in REGEX_DICT_U:
        return REGEX_DICT_U[regex_str]
    else:
        pt = re.compile(regex_str,re.U)
        REGEX_DICT_U[regex_str] = pt
        return pt


def is_regex_match(str, regex):
    pt = get_compiled_regex_unicode(regex)
    pts = pt.findall(str)
    if len(pts) > 0:
        return True
    return False

def is_regex_match_list(str, regex_list):
    for regex in regex_list:
        if is_regex_match(str, regex):
            return True

    return False