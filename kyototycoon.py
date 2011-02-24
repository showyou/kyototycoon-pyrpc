#! -*- coding: utf-8 -*-
import base64
import urllib
import httplib
from lib.serializer.default import DefaultSerializer
from lib.serializer.msgpacks import MsgpackSerializer

def str2longint( string):
    n = 0
    for d in string:
        n <<= 8
        n+=ord(d)
    return n


class KyotoTycoon(object):
    VERSION = '0.0.1'

    def __init__(self, host='127.0.0.1', port = 1978, serializer="default"):
        if serializer == "msgpack":
            self.serializer = MsgpackSerializer()
        else:
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
        print body
        return body

    def set(self, key, value, xt = None):
        key = self.serializer.encode(key.encode("UTF-8"))
        if isinstance(value,str): 
            value = urllib.quote(self.serializer.encode(value.encode("UTF-8")))
        else:
            value = str(value)
        print "key",key, "value",value
        path = "/rpc/set?key="+urllib.quote(key)+"&value="+urllib.quote(value)
        self.ua.request("GET", path)
        res = self.ua.getresponse()
        body = res.read()
        if res.status != 200: return None
        print body
        return True

    def remove(self, key):
        key = self.serializer.encode(key.encode("UTF-8"))
        path = "/rpc/remove?key="+urllib.quote(key)
        self.ua.request("GET", path)
        res = self.ua.getresponse()
        body = res.read()
        if res.status != 200: return None
        return "ok"

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
        # 1行分の処理->分割すべき
        i = 0
        for b2 in b:
            b3 = b2.split("\t")
            for bb in b3:
                if i == 3:
                    # 値の処理
                    bb2 = self.serializer.decode(bb),
                    if isinstance(bb2[0],int):
                        print bb2[0],
                    else:
                        for val in bb2[0]:
                            print val,",",
                    i=-1
                else:
                    print bb,
                i+=1
        print ""
        return body

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
    kt = KyotoTycoon(serializer="msgpack")
    kt.open(port=1978)
    #kt.set("usa",1)
    kt.cur_jump()
    b = kt.cur_get()
    while b != None:
        b = kt.cur_get()
