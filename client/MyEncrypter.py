from des import *
from rabin import *

class MyEncrypter:
    def __init__(self):
        self.des = DES()
        self.rabin = rabin()
        
    def generateKey(self):
        return self.des.generateKey()
    
    def symmetricEncode(self, message, key):
        self.des.input_key(key)
        return self.des.encode(message)
        
    def symmetricDecode(self, message, key):
        self.des.input_key(key)
        return self.des.decode(message)
    
    def generateKeyPair(self):
        return self.rabin.getrabinkey()
    
    def asymmetricEncode(self, message, key):
        return self.rabin.encode(message, long(key))
    
    def asymmetricDecode(self, message, key):
        return self.rabin.decode(message, key[0], key[1])
