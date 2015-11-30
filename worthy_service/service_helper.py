# encoding: utf-8

from datasys import timeHelper

def fill_missing_dates_output_double_lists(retrows,col_name_dt,col_name_val,mandatory_min_total_days = -1):
    datelist = []
    pricelist = []

    min_dt = retrows[0][col_name_dt]
    max_dt = retrows[len(retrows)-1][col_name_dt]

    i = 0
    dt = min_dt
    last_val = "%s" %(retrows[0][col_name_val])
    while True:

        datelist.append("%s" %timeHelper.getDateRemovedYear(dt))
        if "%s" %retrows[i][col_name_dt] == "%s" %dt:
            last_val = "%s" %(retrows[i][col_name_val])
            i += 1

        pricelist.append(last_val)

        dt = timeHelper.getDateAheadOfTargetDate("%s"%dt,-1)
        if timeHelper.compareTime("%s" %dt,"%s"%max_dt,timeHelper.FORMAT_SHORT):
            break

    if len(datelist) < mandatory_min_total_days:
        datelist2 = []
        pricelist2 = []
        fill_num = mandatory_min_total_days - len(datelist)
        for i in range(fill_num,0,-1):
            dt = timeHelper.getDateAheadOfTargetDate("%s" %min_dt,i)
            dt_str = "%s"%dt
            dt_str2 = timeHelper.getDateRemovedYear(dt_str)
            # print dt_str2
            datelist2.append(dt_str2)
            pricelist2.append(None)
        datelist = datelist2 + datelist
        pricelist = pricelist2 + pricelist

    return {
        'dates': datelist,
        'values': pricelist,
    }