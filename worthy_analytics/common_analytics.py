# encoding: utf-8

def _dedup_leave_max(text_list):

    vlist = []
    for item in text_list:
        vlist.append(item)

    for i in xrange(len(text_list)-1):
        for j in range(i+1,len(text_list)):
            if text_list[i] in text_list[j]:
                vlist[i] = ""

    rlist = []
    for item in vlist:
        if len(item) > 0:
            rlist.append(item)

    return rlist

def dedup_leave_max(text_list):
    text_list.reverse()
    alist = _dedup_leave_max(text_list)
    alist.reverse()
    return _dedup_leave_max(alist)

if __name__ == '__main__':
    print dedup_leave_max(['abc','abcd','acde','abcde','a'])