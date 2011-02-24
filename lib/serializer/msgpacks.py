import msgpack

#import serializer
class MsgpackSerializer(object):
    def encode(self, data):
        return msgpack.packb(data)
    
    def decode(self, data):
        return msgpack.unpackb(data)
