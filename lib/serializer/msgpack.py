import msgpack

#import serializer
class MsgpackSerializer(object):
    def encode(self, data):
        return packb(data)
    
    def decode(self, data):
        return unpackb(data)
