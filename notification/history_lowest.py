#encoding: utf-8

from datasys import dbhelper,crawler_helper,timeHelper
from worthy_service import sku_service
from sms import sms_api

NOTIFICATION_JOB_NAME = "NOTIFICATION_HOT"

####### USAGE #########
# (1) update_history_lowest_store() in pipeline
# (2) temp_sendSMS() to notify users


def getHistoryLowest_SkuIds():
    skulist = sku_service.getSku_ID_ListByCatalogID(category_id = "_HISTORY_LOWEST_")
    return skulist

# def get_max_round():
#     sql = 'select max(round) as max_round from jd_notification_history_lowest'
#     try:
#         retrows = dbhelper.executeSqlRead(sql)
#         return int(retrows[0]['max_round'])
#     except:
#         return 0
#     return 0

def get_job_update_time():
    sql = 'select job_time from jd_notification_job_status where job_name="%s"' %(NOTIFICATION_JOB_NAME)
    retrows = dbhelper.executeSqlRead2(sql)
    ret = '0000-00-00 0:00:00'
    if len(retrows) > 0:
        ret = retrows[0][0]
    return ret

def update_history_lowest_store():
    skulist = getHistoryLowest_SkuIds()
    # max_round = get_max_round() + 1
    dt = timeHelper.getNowLong()
    vlist = []
    for sku_id in skulist:
        vlist.append([sku_id, dt])
    sql = 'insert ignore into jd_notification_history_lowest values (%s,%s)'
    afr = dbhelper.executeSqlWriteMany(sql,vlist)
    sql2 = 'replace into jd_notification_job_status values("%s","%s")'%(NOTIFICATION_JOB_NAME,dt)
    afr2 = dbhelper.executeSqlWrite1(sql2)
    afr3 = _removeOldNotifications()
    return [afr,afr2,afr3]

# def getUpdatedSkuIds():
#     max_round = get_max_round()
#     sql = '''
#     select sku_id from jd_notification_history_lowest where round=%s and sku_id not in (select sku_id from jd_notification_history_lowest where round=%s)
#     ''' %(max_round, max_round-1)
#     retrows = dbhelper.executeSqlRead(sql)
#     vlist = []
#     for row in retrows:
#         vlist.append(row['sku_id'])
#     ret = {
#         'round': max_round,
#         'num': len(vlist),
#         'data': vlist,
#     }
#     return ret

def getUpdatedSkuIds():
    ut = get_job_update_time()
    sql = '''
    select distinct sku_id FROM
    jd_notification_history_lowest
    WHERE
    update_time >= "%s"
    ''' %(ut)
    retrows = dbhelper.executeSqlRead2(sql)
    vlist = []
    for row in retrows:
        vlist.append(row[0])
    ret = {
        'num': len(vlist),
        'data': vlist,
    }
    return ret

def _removeOldNotifications():
    ut = timeHelper.getTimeAheadOfNowHours(24,format=timeHelper.FORMAT_LONG)
    sql = 'delete from jd_notification_history_lowest where update_time <= "%s"' %ut
    afr = dbhelper.executeSqlWrite1(sql)
    return afr

def getMaxRoundSkuIds():
    ret = getUpdatedSkuIds()
    return ret['data']

def temp_sendSMS():
    ret = getUpdatedSkuIds()
    num = int(ret['num'])
    myret = {}
    if num > 0:
        info_dict = {'num':num}
        myret = sms_api.sendSMS_Worthy(info_dict=info_dict)
    return myret


if __name__ == '__main__':
    # print getHistoryLowest_SkuIds()
    # print get_max_round()
    # print update_history_lowest_store()
    # print getUpdatedSkuIds()
    print temp_sendSMS()