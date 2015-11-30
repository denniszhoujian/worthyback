# encoding: utf-8

import time
import datetime
import math

HOURS_OFFSET = 8

FORMAT_LONG = '%Y-%m-%d %H:%M:%S'
FORMAT_SHORT = '%Y-%m-%d'

def getTimeAheadOfNowDays(num_days, format='%Y-%m-%d'):
    d1 = datetime.datetime.now()
    d3 = d1 - datetime.timedelta(days=num_days)
    ago = d3.strftime(format)
    return ago

def getTimeAheadOfNowHours(num_days, format='%Y-%m-%d'):
    d1 = datetime.datetime.now()
    d3 = d1 - datetime.timedelta(hours=num_days)
    ago = d3.strftime(format)
    return ago

def getNow(format="%Y-%m-%d"):
    d1 = datetime.datetime.now()
    return d1.strftime(format)

def getNowLong():
    d1 = datetime.datetime.now()
    return d1.strftime("%Y-%m-%d %H:%M:%S")

def compareTime(time1, time2, format='%Y-%m-%d %H:%M:%S'):
    timeArray1 = time.strptime(time1, format)
    timeStamp1 = int(time.mktime(timeArray1))
    timeArray2 = time.strptime(time2, format)
    timeStamp2 = int(time.mktime(timeArray2))
    return time1>time2

def compareTime2(time1, time2, format1='%Y-%m-%d %H:%M:%S',format2='%Y-%m-%d'):
    timeArray1 = time.strptime(time1, format1)
    timeStamp1 = int(time.mktime(timeArray1))
    timeArray2 = time.strptime(time2, format2)
    timeStamp2 = int(time.mktime(timeArray2))
    return time1>=time2

def isDateEqual(time1,time2,format1='%Y-%m-%d %H:%M:%S',format2='%Y-%m-%d'):
    timeArray1 = time.strptime(time1, format1)
    dt1 = time.strftime('%Y-%m-%d',timeArray1)
    timeArray2 = time.strptime(time2, format2)
    dt2 = time.strftime('%Y-%m-%d',timeArray2)
    return dt1==dt2

def getTimeString(timeStamp, format=0):
    timeArray = time.localtime(timeStamp)
    if format == 0:
        fstr = '%Y-%m-%d %H:%M:%S'
    else:
        fstr = '%Y-%m-%d'

    strt = time.strftime(fstr, timeArray)
    return strt

def getTimeDropMinuteSecond():
    now = int(time.mktime(datetime.datetime.now().timetuple()))
    now2 = int(math.floor(now/3600)*3600)
    update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now2))
    return update_time

def getTimeLeftTillNextHour():
    now = int(time.time())
    next = int(now/3600) * 3600 + 3600
    return next - now

def getTimeLeftTillTomorrow():
    now = int(time.time())
    next = int((now)//86400) * 86400 + 86400 - 8*3600
    #print getTimeStringFromTimeStamp(next,"%Y-%m-%d %H:%M:%S")
    diff = next - now
    if diff < 0:
        diff += 86400
    return diff

def getStartTimeDaysBefore(days):
    start = 2
    dt1 = getTimeAheadOfNowHours(24*(days-(2-start))) + ' 0:00:00'
    return dt1

def getWebDateAheadOf(days, long=1):
    start = 2
    dt1 = getTimeAheadOfNowHours(24*(days-(2-start))+HOURS_OFFSET)
    if long==1:
        dt1 = dt1 + ' 0:00:00'
    return dt1

def getStartTimeYesterday():
    return getStartTimeDaysBefore(1)

def getTimeStampFromTimeString(timestring, fmt='%Y-%m-%d %H:%M:%S'):
    timeArray = time.strptime(timestring, fmt)
    return int(time.mktime(timeArray))

def getTimeStringFromTimeStamp(timestamp, fmt):
    timeArray = time.localtime(timestamp)
    return time.strftime(fmt, timeArray)

# format string like '2015-4-29 20'
# return a list of consecutive date-hours, in ascending order
def getDateHourRange(start,end,fmt):
    sp = getTimeStampFromTimeString(start,fmt)
    ep = getTimeStampFromTimeString(end,fmt)
    tlist = []
    tt = sp
    while True:
        if tt > ep:
            break
        tlist.append(getTimeStringFromTimeStamp(tt,fmt))
        tt = tt + 3600
    return tlist

def getDateDayRange(start,end,fmt='%Y-%m-%d'):
    sp = getTimeStampFromTimeString(start,fmt)
    ep = getTimeStampFromTimeString(end,fmt)
    tlist = []
    tt = sp
    while True:
        if tt > ep:
            break
        tlist.append(getTimeStringFromTimeStamp(tt,fmt))
        tt = tt + 3600*24
    return tlist

def changeFormat(timestring, currentfmt, newfmt):
    tarray = time.strptime(timestring, currentfmt)
    return time.strftime(newfmt, tarray)

def getSQLTableSuffix(daysago=0):
    d1 = datetime.datetime.now()
    if daysago > 0:
        d1 = datetime.datetime.now()
        d3 = d1 - datetime.timedelta(days=daysago)
        ago = d3.strftime('%Y_%m')
        return ago
    return d1.strftime('%Y_%m')

def getWeekDay_Time(ostime):
    ostime = '%s' %ostime
    wdlist = ['星期一','星期二','星期三','星期四','星期五','星期六','星期日']
    fmt = "%Y-%m-%d %H:%M:%S"
    timeArray = time.strptime(ostime,fmt)
    timestr = time.strftime("%H:%M:%S",timeArray)
    wd = datetime.datetime.strptime(ostime,fmt).weekday()
    return wdlist[wd] + ' ' + timestr

def getDateAheadOfTargetDate(target_date, days_ago):
    ts = getTimeStampFromTimeString(target_date,'%Y-%m-%d')
    newts = ts - 24*3600*days_ago
    newdt = getTimeStringFromTimeStamp(newts,'%Y-%m-%d')
    return newdt

def getEnabledDateRange(target_date,min_dt,max_dt,num_days):

    tplus7_enabled = 0
    tminus7_enabled = 0
    try:
        min_dt = '%s' %min_dt
        max_dt = '%s' %max_dt
        tplus7 = getDateAheadOfTargetDate(target_date,0-num_days)
        tminus7 = getDateAheadOfTargetDate(target_date,num_days)
        tplus7_enabled = 1
        tminus7_enabled = 1
        if compareTime(tplus7,max_dt,'%Y-%m-%d'):
            tplus7_enabled = 0
        else:
            tplus7_enabled = 1
        if compareTime(min_dt,tminus7,'%Y-%m-%d'):
            tminus7_enabled = 0
        else:
            tminus7_enabled = 1
    except:
        pass

    return {'tplus_enabled':tplus7_enabled,'tminus_enabled':tminus7_enabled}

def getDateRemovedYear(dt):
    str = "%s" %dt
    str2 = str[5::]
    return str2

# def getTimeStringFromDateTime():
#     pass
#
# def getDateStrWeekOfYear(year_str,num_week):
#     datestr = '%s-1-1 0:00:00' %(year_str)
#     timestamp = getTimeStampFromTimeString(datestr,'%Y-%m-%d %H:%M:%S') + num_week*7*86400
#     newdate = getTimeStringFromTimeStamp(timestamp,'%Y-%m-%d %H:%M:%S')
#     return newdate

if __name__ == "__main__":

    #print getDateDayRange('2015-5-10','2015-5-24')
    #print getTimeLeftTillTomorrow()
    # print getStartTimeYesterday()
    # print getStartTimeDaysBefore(0)
    # print getStartTimeDaysBefore(3)
    # print getTimeAheadOfNowDays(1)
    # print getWebDateAheadOf(1,0)
    # print getTimeLeftTillTomorrow()
    # print getTimeStringFromTimeStamp(1432276813,'%Y-%m-%d %H:%M:%S')
    # # print getDateStrWeekOfYear('2015',1)
    # # print getDateStrWeekOfYear('2015',2)
    # # print getDateStrWeekOfYear('2015',3)
    # print getDateAheadOfTargetDate('2016-6-14',-1)
    # print getDateAheadOfTargetDate('2016-6-14',7)
    # print getDateRemovedYear('2015-4-3 20:33:33')
    print getDateAheadOfTargetDate('2015-4-3',1)