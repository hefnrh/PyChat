#!/usr/bin/env python

from client import ServerCommandHandle, Encrypter, Client
import sys

# change code here to implement your own client
class HandleInstance(ServerCommandHandle):
    def errorHandle(self, message):
        print "error", message
    def onlineHandle(self, onlineList):
        print "online", onlineList
    def offlineHandle(self, offlineList):
        print "offline", offlineList
    def talkHandle(self, opp, content):
        print opp, content
    def startTalkHandle(self, opp):
        print opp, "start talk"
    def connectFailHandle(self):
        print "connection failed"
    def connectDownHandle(self):
        print "connection down"
        
# change code here to implement your own encrypt system
class MyEncrypter(Encrypter):
    def generateKeyPair(self):
        return (123, 456)
    def generateKey(self):
        return 111
    def asymmetricEncrypt(self, message, key):
        return message
    def symmetricEncrypt(self, message, key):
        return message

enc = MyEncrypter()
handle = HandleInstance()
username = sys.stdin.readline()
client = Client("127.0.0.1", 12700, username, enc)
client.connect(handle)
name = sys.stdin.readline()
client.startTalk(name)
while True:
    line = sys.stdin.readline()
    client.sendMessage(name, True, line)
