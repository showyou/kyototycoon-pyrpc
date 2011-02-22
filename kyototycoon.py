#! -*- coding: utf-8 -*-
import base64
import urllib
import httplib
from lib.serializer.default import DefaultSerializer

def str2longint( string):
    n = 0
    for d in string:
        n <<= 8
        n+=ord(d)
    return n


class KyotoTycoon(object):
    VERSION = '0.0.1'

    def __init__(self, host='127.0.0.1', port = 1978, serializer="msgpack"):
        self.serializer = DefaultSerializer()
        pass

    def open(self, host = '127.0.0.1', port = 1978, timeout = 30):
        self.ua = httplib.HTTPConnection(host, port, False, timeout)
        return True

    def close(self):
        self.ua.close()

    def get(self, key):
        #if isinstance(key, str):
        key = self.serializer.encode(key.encode("UTF-8"))
        path = "/rpc/get?key="+urllib.quote(key)
        self.ua.request("GET", path)
        res = self.ua.getresponse()
        body = res.read()
        if res.status != 200: return None
        return res

    def set(self, key, value, xt = None):
        pass

    def remove(self, key):
        pass

    def cur_jump(self):
        path = "/rpc/cur_jump?CUR=1"
        self.ua.request("GET", path)
        res = self.ua.getresponse()
        body = res.read()
        if res.status != 200: return None
        return True

    def cur_get(self):
        path = "/rpc/cur_get?CUR=1&step="
        self.ua.request("GET", path)
        res = self.ua.getresponse()
        body = res.read()
        print res.msg
        if res.status != 200: return None
        b = body.split("\n")[:-1]
        for b2 in b:
            b3 = b2.split("\t")
            for bb in b3:
                # 値の処理
                print self.serializer.decode(bb)
        return False

    def vacuum(self):
        path = "/rpc/vacuum"
        self.ua.request("GET", path)
        res = self.ua.getresponse()
        body = res.read()
        print body
        for header in res.getheaders():
            print( header[0] + " " + header[1])
        if res.status != 200: return None
        return True
        


if __name__ == "__main__":
    kt = KyotoTycoon()
    kt.open(port=4130)
    kt.cur_jump()
    kt.cur_get()
    kt.cur_get()
    kt.cur_get()
