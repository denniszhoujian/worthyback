#encoding: utf-8

import time
from apns import APNs, Frame, Payload

def test():
    apns = APNs(use_sandbox=True, cert_file='public.pem', key_file='newkey.pem')

    # Send a notification
    token_hex = '2eb2265f e06bc619 6aa41d3e 7428cf0e 4d32e70c 592977b5 c9b8e012 7da40b24'.replace(' ','')
    payload = Payload(alert="Hello World!", sound="default", badge=1)
    apns.gateway_server.send_notification(token_hex, payload)

    # # Send multiple notifications in a single transmission
    # frame = Frame()
    # identifier = 1
    # expiry = time.time()+3600
    # priority = 10
    # frame.add_item('2eb2265f e06bc619 6aa41d3e 7428cf0e 4d32e70c 592977b5 c9b8e012 7da40b24', payload, identifier, expiry, priority)
    # apns.gateway_server.send_notification_multiple(frame)

def test2():
    feedback_connection = APNs(use_sandbox=True, cert_file='public.pem', key_file='private.pem')
    for (token_hex, fail_time) in feedback_connection.feedback_server.items():
    # do stuff with token_hex and fail_time
        print token_hex
        print fail_time

if __name__ == '__main__':
    test()