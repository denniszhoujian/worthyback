# encoding: utf-8

from datasys import dbhelper,timeHelper,crawler_helper
from notification import apns_helper, notification_config

def record_device_id(deviceid, platform, original_deviceid):

    tnow = timeHelper.getNowLong()
    if platform not in [notification_config.CONST_DEVICE_PLATFORM_ANDROID, notification_config.CONST_DEVICE_PLATFORM_IOS]:
        platform = notification_config.CONST_DEVICE_PLATFORM_IOS

    if len(deviceid) < 5:
        return {
            'status': -1,
            'msg': 'invalid device_id = %s' %deviceid,
        }

    # record in db
    vlist = [
        [deviceid,platform,tnow,original_deviceid,""]
    ]

    ret = crawler_helper.persist_db_history_and_latest(
        table_name='user_notification_device',
        num_cols=len(vlist[0]),
        value_list=vlist,
        is_many=True,
        need_history=True,
        need_flow=False,
    )

    return ret



if __name__ == '__main__':

    print record_device_id('aceefddg','_IOS_')
