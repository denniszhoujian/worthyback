#encoding: utf-8

def expand_list(str_list, splitter_list):
    rlist = []
    for str in str_list:
        for splitter in splitter_list:
            strs = str.split(splitter)
            rlist += strs
            if len(str) > 1:
                break
    return list(set(rlist))

if __name__ == '__main__':
    print u'sd 存储卡、sdhc 存储卡'.split(u'、')