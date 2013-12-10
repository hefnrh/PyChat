#!/usr/bin/env python

import socket
import threading

# largest character amount the client can receive every time
MAX_BUFFER_SIZE = 8192

MIN_COMMAND_LENGTH = 4
# abstract class to inherit
# client call the function of this class to
# handle command from server
# see file "command format.txt"
class ServerCommandHandle:

    def errorHandle(self, message):
        pass
    def onlineHandle(self, onlineList):
        pass
    def offlineHandle(self, offlineList):
        pass
    def talkHandle(self, opp, content):
        pass
    def startTalkHandle(self, opp):
        pass
    # called when client fails to connect to the server
    def connectFailHandle(self):
        pass
    def connectDownHandle(self):
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
    def __init__(self, connection, serverHandle, encrypter, privateKey):
        threading.Thread.__init__(self)
        threading.Thread.setDaemon(self, True)
        self.connection = connection
        self.serverHandle = serverHandle
        self.pubkeyDict = {}
        self.sessionKeyDict = {}
        self.encrypter = encrypter
        self.privateKey = privateKey
    
    def commandMatcher(self, string):
        command = string.split(" ")
        
        if command[0] == "online":
            userlist = []
            for i in range(1, len(command)):
                userlist.append(command[i])
            self.serverHandle.onlineHandle(userlist)
        
        elif command[0] == "talk":
            user = command[1]
            content = string[string.find(command[3]):]
            if command[2] == "true":
                content = self.encrypter.symmetricEncrypt(content, self.sessionKeyDict[user])
            self.serverHandle.talkHandle(user, content)
        
        elif command[0] == "error":
            content = string[string.find(command[1]):]
            self.serverHandle.errorHandle(content)
        
        elif command[0] == "offline":
            userlist = []
            for i in range(1, len(command)):
                userlist.append(command[i])
            self.serverHandle.offlineHandle(userlist)
        
        elif command[0] == "pubkey":
            self.pubkeyDict[command[1]] = command[2]
        
        elif command[0] == "start":
            sessionKey = self.encrypter.asymmetricEncrypt(command[2], self.privateKey)
            self.sessionKeyDict[command[1]] = sessionKey
            self.serverHandle.startTalkHandle(command[1])
    
    def run(self):
        try:
            while True:
                command = self.connection.recv(MAX_BUFFER_SIZE)
                if len(command) < MIN_COMMAND_LENGTH:
                    raise Exception()
                self.commandMatcher(command)
        except:
            try:
                self.connection.shutdoan()
                self.connection.close()
            except:
                pass
            self.serverHandle.connectDownHandle()
    
    def sendMessage(self, oppname, encrypted, content):
        if encrypted:
            content = self.encrypter.symmetricEncrypt(content, self.sessionKeyDict[oppname])
            self.send("talk " + oppname + " true " + content)
        else:
            self.send("talk " + oppname + " false " + content)
                
    def send(self, content):
        try:
            self.connection.send(content)
        except:
            try:
                self.connection.shutdoan()
                self.connection.close()
            except:
                pass
            self.serverHandle.connectDownHandle()
    
    def startTalk(self, oppname):
        # get session key and send start command here
        key = self.encrypter.generateKey()
        self.sessionKeyDict[oppname] = key
        self.send("getpubkey " + oppname)
        while not self.pubkeyDict.has_key(oppname):
            pass
        encryptedKey = self.encrypter.asymmetricEncrypt(key, self.pubkeyDict[oppname])
        self.send("start " + oppname + " " + str(encryptedKey))
        self.serverHandle.startTalkHandle(oppname)
        
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
            self.sock.send(self.username + " " + str(self.pubkey))
            self.listenThread = ListenThread(self.sock, serverHandle, self.encrypter, self.privateKey)
            self.listenThread.start()
        except:
            serverHandle.connectFailHandle()
    
    def sendMessage(self, oppname, encrypted, content):
        self.listenThread.sendMessage(oppname, encrypted, content)
    
    def startTalk(self, opp):
        self.listenThread.startTalk(opp)
