#!/usr/bin/env python

import socket
import threading

# put usernames and their public keys
userDict = {}
# put usernames and their connections
threadDict = {}

HOST = ''
PORT = 12700

# socket queue size
MAX_QUEUE_SIZE = 5
# largest character amount the server can receive every time
MAX_BUFFER_SIZE = 8192

MIN_COMMAND_LENGTH = 4

class MyThread(threading.Thread):
    def __init__(self, connection, username):
        threading.Thread.__init__(self)
        threading.Thread.setDaemon(self, True)
        self.connection = connection
        self.username = username
    
    # send string to the client, string begins with command
    def send(self, string):
        try:
            self.connection.send(string)
        except:
            print self.username + " exception in send()"
            try:
                self.connection.shutdown()
                self.connection.close()
            except:
                pass
            global userDict
            global threadDict
            del userDict[self.username]
            del threadDict[self.username]
            for thr in threadDict.itervalues():
                thr.send("offline " + self.username)
    
    def getUsername(self, username):
        return self.username
    
    # execute command from client
    def commandMatcher(self, string):
        global userDict
        global threadDict
        command = string.split(" ")
        # add code here to add more command
        if command[0] == "talk":
            if not threadDict.has_key(command[1]):
                self.send("error user not exist")
                return None
            thr = threadDict[command[1]]
            content = "talk " + self.username + " "
            content = content + string[string.find(command[2]):]
            thr.send(content)
        elif command[0] == "getpubkey":
            if userDict.has_key(command[1]):
                self.send("pubkey " + command[1] + " " + userDict[command[1]])
            else:
                self.send("error user not exist")
        elif command[0] == "start":
            if not threadDict.has_key(command[1]):
                self.send("error user not exist")
                return None
            thr = threadDict[command[1]]
            content = "start " + self.username + " " + string[string.find(command[2]):]
            thr.send(content)
        else:
            self.send("error no such command")
    
    def run(self):
        try:
            while True:
                command = self.connection.recv(MAX_BUFFER_SIZE)
                if len(command) < MIN_COMMAND_LENGTH:
                    raise Exception()
                print "receive from " + self.username + ": " + command
                self.commandMatcher(command)
        except:
            print self.username + " exception in run()"
            try:
                self.connection.shutdown()
                self.connection.close()
            except:
                pass
            global userDict
            global threadDict
            del userDict[self.username]
            del threadDict[self.username]
            for thr in threadDict.itervalues():
                thr.send("offline " + self.username)
            return None

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(MAX_QUEUE_SIZE)

print "server start"
while True:
    conn, addr = s.accept()
    logReq = conn.recv(MAX_BUFFER_SIZE)
    logParam = logReq.split(" ")
    # deal with duplicate user name
    if userDict.has_key(logParam[0]):
        conn.send("error username already in use!")
        conn.shutdown()
        conn.close()
        continue
    print logParam[0] + " log in with public key: " + logParam[1]
    # announce a new user log in
    for thr in threadDict.itervalues():
        thr.send("online " + logParam[0])
    userDict[logParam[0]] = logParam[1]
    # send user list to the new user
    nameList = "online"
    for name in userDict.iterkeys():
        nameList = nameList + " " + name
    conn.send(nameList)
    # start a new thread
    thread = MyThread(conn, logParam[0])
    thread.start()
    threadDict[logParam[0]] = thread
    