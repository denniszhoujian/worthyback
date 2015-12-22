# encoding: utf-8

import uuid

UUID_COOKIE_NAME = "UUID_COOKIE_NAME"

def getClientUUID(request):

    if UUID_COOKIE_NAME in request.COOKIES:
        return request.COOKIES[UUID_COOKIE_NAME]
    else:
        id = uuid.uuid1()
        return id