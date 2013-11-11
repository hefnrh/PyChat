#!/usr/bin/env python

import socket
import threading

# largest character amount the server can receive every time
MAX_BUFFER_SIZE = 8192

# abstract class to inherit
# client call the function of this class to
# handle command from server
# see file "command format.txt"
class ServerHandle:
    def __init__(self, encrypter):
        self.encrypter = encrypter
    def errorHandle(self, message):
        pass
    def onlineHandle(self, onlineList):
        pass
    def offlineHandle(self, offlineList):
        pass
    def talkHandle(self, fromUser, encrypted, content):
        pass
    # called when client fails to connect to the server
    def connectFailHandle(self):
        pass

# abstract class to inherit
# client call the function of this class to
# generate key pairs for RSA or ECC
# and key for DES or AES
# and encrypt or decrypt messages
class Encrypter:
    def generateKeyPair(self):
        pass
    def generateKey(self):
        pass
    def asymmetricEncrypt(self, message, key):
        pass
    def symmetricEncrypt(self, message, key):
        pass

class ListenThread(threading.Thread):
    # serverHandle is instance of subclass of ServerHandle 
    def __init__(self, connection, serverHandle):
        threading.Thread.__init__(self)
        threading.Thread.setDaemon(self, True)
        self.connection = connection
        self.serverHandle = serverHandle
    
    def commandMatcher(self, string):
        command = string.split(" ")
        if command[0] == "online":
            userlist = []
            for i in range(1, len(command)):
                userlist.append(command[i])
            self.serverHandle.onlineHandle(userlist)
        elif command[0] == "talk":
            user = command[1]
            encrypted = True
            if command[2] == "false":
                encrypted = False
            content = ""
            for i in range(3, len(command)):
                content = content + command[i] + " "
            self.serverHandle.talkHandle(user, encrypted, content)
        elif command[0] == "error":
            content = ""
            for i in range(1, len(command)):
                content = content + command[i] + " "
            self.serverHandle.errorHandle(content)
        elif command[0] == "offline":
            pass
        elif command[0] == "pubkey":
            pass
        elif command[0] == "start":
            pass
    
    def run(self):
        try:
            while True:
                command = self.connection.recv(MAX_BUFFER_SIZE)
                self.commandMatcher(command)
        except:
            pass
        
class Client:
    def __init__(self, host, port, username, encrypter):
        self.host = host
        self.port = port
        self.username = username
        self.encrypter = encrypter
        self.pubkey, self.privateKey = encrypter.generateKeyPair()
    
    def setUsername(self, name):
        self.username = name
    
    def connect(self, serverHandle):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((self.host, self.port))
            self.sock.send(self.username + str(self.pubkey))
            self.listenThread = ListenThread(self.sock, serverHandle)
            self.listenThread.start()
        except:
            serverHandle.connectFailHandle()
    
    def send(self, encrypted, content):
        if encrypted:
            pass
        else:
            try:
                self.sock.send("talk " + self.username + " false " + content)
            except:
                pass