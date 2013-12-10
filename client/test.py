#!/usr/bin/env python

from client import ServerCommandHandle, Encrypter, Client
import sys
from MyEncrypter import *

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
        

enc = MyEncrypter()
handle = HandleInstance()
username = sys.stdin.readline()
username = username[0:len(username) - 1]
client = Client("127.0.0.1", 12700, username, enc)
client.connect(handle)
name = sys.stdin.readline()
name = name[0:len(name) - 1]
client.startTalk(name)
while True:
    line = sys.stdin.readline()
    line = line[0:len(line) - 1]
    client.sendMessage(name, True, line)
