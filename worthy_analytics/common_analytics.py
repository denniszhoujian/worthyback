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

def make_space_separated(text):
    text = text.strip()
    # ts = ""
    # while ts != text:
    #     ts = text
    #     text = text.replace("  "," ")
    ts = text.split(" ")
    vlist = []
    for part in ts:
        if len(part) > 0:
            vlist.append(part)
    ret_text = ' '.join(vlist)
    return ret_text

def dedup_inline(text):
    text2 = make_space_separated(text)
    ts = text.split(" ")
    ts2 = dedup_leave_max(ts)
    return ' '.join(ts2)

def remove_string_from_list(text,text_list):
    vlist = []
    for item in text_list:
        if item != text:
            vlist.append(item)
    return vlist

if __name__ == '__main__':
    print dedup_leave_max(['abc','abcd','acde','abcde','a'])
    print make_space_separated(" 我们  是  中国 的/年轻人   ")
    print dedup_inline('大事 大使 试试 大事 大事 大师 大湿 大使')