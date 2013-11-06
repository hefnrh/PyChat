#!/usr/bin/env python

import socket
import threading

# put usernames and their public keys
userDict = {}

HOST = ''
PORT = 12700
MAX_QUEUE_SIZE = 5
MAX_BUFFER_SIZE = 8192

# execute command in string
def commandMatcher(string, myThread):
    return 0
    
class MyThread(threading.Thread):
    def __init__(self, connection):
        self.connection = connection
        threading.Thread.setDaemon(True)
    
    # send string to the client, string begins with command
    def send(self, string):
        self.connection.send(string)
    
    def setUsername(self, username):
        self.username = username
        
    def getUsername(self, username):
        return self.username
    
    def run(self):
        try:
            while True:
                command = self.connection.recv(MAX_BUFFER_SIZE)
                commandMatcher(command, self)
        except:
            global userDict
            del userDict[self.username]
            return None

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(MAX_QUEUE_SIZE)

while True:
    conn, addr = s.accept()
    logReq = conn.recv(MAX_BUFFER_SIZE)
    logParam = logReq.split()
    if userDict.has_key(logParam[0]):
        conn.send("error username already in use!")
        conn.close()
        continue
    userDict[logParam[0]] = logParam[1]