# encoding: utf-8


# def read_Promo_Items_Quan() :
#
#     sql = '''
#         select * from jd_promo_item_latest where quan_json is not NULL
#     '''
#     retrows = dbhelper.executeSqlRead(sql)
#
#     adict = {}
#
#     for row in retrows:
#         obj = json.loads(row['quan_json'])
#         url = "http://item.jd.com/%s.html" %row['sku_id']
#         # print "%s\t\t%s" %(obj['title'],url)
#         # print ("\n")
#         adict[obj['title']] = url
#     pass
#
#     for item in adict:
#         print item
#         print adict[item]
#
# def read_Promo_Items_Ads():
#     sql = '''
#     select sku_id, ads_json from jd_promo_item_latest limit 1000
#     '''
#     retrows = dbhelper.executeSqlRead(sql)
#     for row in retrows:
#         js = row['ads_json']
#         obj = json.loads(js)
#         for item in obj:
#             if len(item['ad'])>0:
#                 print item['ad']
#                 print row['sku_id']
#
#
# def read_Promo_Items_Promo() :
#
#     sql = '''
#         select sku_id, promo_json from jd_promo_item_latest
#         where promo_json is not NULL
#     '''
#     retrows = dbhelper.executeSqlRead(sql)
#
#     adict = {}
#     for row in retrows:
#         json_str = row['promo_json'].strip()
#         if json_str not in adict:
#             adict[json_str] = []
#         vlist = adict[json_str]
#         vlist.append(row['sku_id'])
#
#     for key in adict:
#         obj = json.loads(key)
#         pots = obj['pickOneTag']
#         for pot in pots:
#             if pot['code'] == '19':
#                 name = pot['name']
#                 content = pot['content']
#                 adurl = pot['adurl']
#                 print "name"
#                 print name
#                 print content
#                 print adurl
#
#         ending = obj['ending']
#         tags = obj['tags']
#         skus = adict[key]
#
#         print "ending = %s" %ending
#         print "tags"
#         for tag in tags:
#             for k in tag:
#                 print "%s :: %s" %(k,tag[k])
#         print skus
#         print '-'*60
#
#     # print json.dumps(adict)
#     print "ok"

# PROCESS_RAW_PROMO_RECENCY_HOURS = 12
# PROCESS_PROMO_DETAIL_RECENCY_HOURS = 12