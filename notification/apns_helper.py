#encoding: utf-8

import time
from apns import APNs, Frame, Payload
from datasys import dbhelper

APNS_KEY_FILE = 'newkey.pem'
APNS_CERT_FILE = 'public.pem'
APNS_USE_SANDBOX = True


def _get_all_devices():
    sql = 'select device_id from user_notification_device_latest'
    retrows = dbhelper.executeSqlRead2(sql)
    vlist = []
    for row in retrows:
        device_id = row[0]
        vlist.append(device_id)
    return vlist


# updateList [ {'device_id':, 'update_list':} ]
# update_list: [ {'category_name':, 'num':} ]


# sendInfoList [ {'device_id':, 'info':} ]
# info: {'num':, 'category_string': }


# sendDeviceStringList : [ {'device_id': 'xxx', 'alert': 'xxx', 'badge':1 ]
def do_send_sms(sendDeviceStringList):
    apns = APNs(use_sandbox=APNS_USE_SANDBOX, cert_file=APNS_CERT_FILE, key_file=APNS_KEY_FILE)
    frame = Frame()
    identifier = 1
    expiry = time.time()+3600*4
    priority = 10

    for info in sendDeviceStringList:
        device_id = info['device_id']
        alert = info['alert']
        badge = info['badge']
        payload = Payload(alert=alert, sound="default", badge=badge)
        frame.add_item(device_id, payload, identifier, expiry, priority)

    # DO SEND!
    t1 = time.time()
    apns.gateway_server.send_notification_multiple(frame)
    t2 = time.time()
    print "Sending %s notifications, using seconds = %s" %(len(sendDeviceStringList),int(t2-t1))


def test2():
    feedback_connection = APNs(use_sandbox=True, cert_file='public.pem', key_file='private.pem')
    for (token_hex, fail_time) in feedback_connection.feedback_server.items():
    # do stuff with token_hex and fail_time
        print token_hex
        print fail_time

if __name__ == '__main__':
    test2()