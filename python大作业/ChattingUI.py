
from client import ServerCommandHandle, Encrypter, Client
import socket
import sys
import wx
from LoginFrame import LoginFrame,list

chatlist=[""]

############################################################################################################################
#it is the main window of the Chatting Room
class MainWindow(wx.Frame):
    def __init__(self, parent, id, title, client):
        wx.Frame.__init__(self, parent, id, title)
        
        self.SetBackgroundColour("White")
        self.chat = None
        self.statusBar = self.CreateStatusBar()
        self.StatusBar.SetStatusText("Local area network chatting room")
        
        #listbox list all the onlineuser and offlineuser    
        self.onlinelistBox = wx.ListBox(self, -1,  \
                             choices = [], style = wx.LB_DEFAULT)
        self.offlinelistBox = wx.ListBox(self, -1,  \
                             choices = [], style = wx.LB_DEFAULT)        
        self.onlineuser = wx.StaticText(self, -1, "online")
        self.offlineuser = wx.StaticText(self, -1, "offline")
        self.msgTextCtrl = wx.TextCtrl(self, -1,\
                                  style = wx.TE_MULTILINE | wx.TE_READONLY)
        self.statusTextCtrl = wx.TextCtrl(self, -1,"Welcome  "+ list[0],\
                                  style = wx.TE_MULTILINE | wx.TE_READONLY)
        self.editTextCtrl = wx.TextCtrl(self, -1,\
                                   style = wx.TE_MULTILINE | wx.TE_PROCESS_ENTER)
        
        self.nullLabel1 = wx.StaticText(self, -1)
        
        #buttons
        self.sendButton = wx.Button(self, -1, "Send")
        self.closeButton = wx.Button(self, -1, "Close")
        self.clearButton = wx.Button(self, -1, "Clear")
        self.recordButton = wx.Button(self, -1, "Records")
        
        #button layout
        hsizer2 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer2.Add(self.recordButton, proportion = 0, flag =wx.RIGHT)
        
        #button layout
        hsizer1 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer1.Add(self.nullLabel1, proportion = 2, flag = wx.EXPAND | wx.TOP)
        hsizer1.Add(self.clearButton, proportion = 0, flag = wx.EXPAND | wx.LEFT | wx.TOP)
        hsizer1.Add(self.sendButton, proportion = 0, flag = wx.LEFT | wx.TOP)
        hsizer1.Add(self.closeButton, proportion = 0, flag = wx.LEFT | wx.TOP)
        
        hsizer3 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer3.Add(self.statusTextCtrl,1,wx.EXPAND|wx.ALL)
        #text control layout
        vsizer1 = wx.BoxSizer(wx.VERTICAL)
        vsizer1.Add(hsizer3, 0, wx.EXPAND)
        vsizer1.Add(self.msgTextCtrl, 5, wx.EXPAND)
        vsizer1.Add(hsizer2, 0, wx.EXPAND)
        vsizer1.Add(self.editTextCtrl, 3, wx.EXPAND)
        vsizer1.Add(hsizer1, 0, wx.EXPAND)
        
        #list and button layout
        vsizer2 = wx.BoxSizer(wx.VERTICAL)
        vsizer2.Add(self.onlineuser,0)
        vsizer2.Add(self.onlinelistBox,1, wx.EXPAND)
        vsizer2.Add(self.offlineuser,0)
        vsizer2.Add(self.offlinelistBox,1, wx.EXPAND)
        #vsizer2.Add(self.msgButton, 0, wx.EXPAND)
        
        #all widgets layout
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(vsizer1, 3, wx.EXPAND|wx.RIGHT)
        sizer.Add(vsizer2, 1, wx.EXPAND)
        sizer.SetItemMinSize(vsizer1,(600,300))
        
        #add layout
        self.SetSizer(sizer)
        self.SetAutoLayout(1)
        sizer.Fit(self)
        
        #listBox action
        self.Bind(wx.EVT_LISTBOX, self.OnListBox, self.onlinelistBox)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.DListBox, self.onlinelistBox)
        
        #button action
        self.Bind(wx.EVT_BUTTON, self.OnClear, self.clearButton)
        self.Bind(wx.EVT_BUTTON, self.OnSend, self.sendButton)
        self.Bind(wx.EVT_BUTTON, self.OnClose, self.closeButton)
        
        #press enter and send the message
        self.Bind(wx.EVT_TEXT_ENTER, self.OnSend, self.editTextCtrl)
        
        
    def OnListBox(self, event):
        user = event.GetString()
        self.StatusBar.SetStatusText("Double click chat to %s" % user)
        
    def DListBox(self, event):
        user = event.GetString()
        self.chat = user
        client.startTalk(user)
        self.Title = "Chat with %s" % user
        self.msgTextCtrl.SetValue("")
        self.editTextCtrl.SetValue("")
            
        
    def OnSend(self, event): 
        data = self.editTextCtrl.GetValue()
        if data:
            if self.chat:
                import time
                now = time.localtime()
                hour, min, sec = (now.tm_hour, now.tm_min, now.tm_sec)
                if hour < 10:
                    hour = "0" + str(hour)
                if min < 10:
                    min = "0" + str(min)
                if sec < 10:
                    sec = "0" + str(sec)
                ltime = "%s:%s:%s" % (hour, min, sec)
                msgdata = list[0] + "  " + ltime + "\n" + data + "\n"
                self.editTextCtrl.SetValue("")
                self.msgTextCtrl.AppendText(msgdata)
                client.sendMessage(self.chat,True,data)
            else:
                #create a message dialogue
                d = wx.MessageDialog(self, "Please choose a user you want to chat with", style = wx.OK)
                d.ShowModal()
                d.Destroy()
            
    def OnClear(self, event):
        self.editTextCtrl.Clear()
        
    def OnClose(self, event):
        self.Close(True)

#########################################################################################################################
class HandleInstance(ServerCommandHandle):
    def errorHandle(self, message):
        print "error", message
        
        #create a message dialogue
        d = wx.MessageDialog(None, "error"+message, style = wx.OK)
        d.ShowModal()  
        d.Destroy()
        
    def onlineHandle(self, onlineList):
        print "online", onlineList
        for item in onlineList:
            win.onlinelistBox.Append(item)
            if(win.offlinelistBox.FindString(item)+1):
                win.offlinelistBox.Delete(win.offlinelistBox.FindString(item))  
        
    def offlineHandle(self, offlineList):
        print "offline", offlineList 
        for item in offlineList:       
            win.offlinelistBox.Append(item)
            if(win.onlinelistBox.FindString(item)+1):
                win.onlinelistBox.Delete(win.onlinelistBox.FindString(item))
        
    def talkHandle(self, opp, content):
        print opp, content
        import time
        now = time.localtime()
        hour, min, sec = (now.tm_hour, now.tm_min, now.tm_sec)
        if hour < 10:
            hour = "0" + str(hour)
        if min < 10:
            min = "0" + str(min)
        if sec < 10:
            sec = "0" + str(sec)
        ltime = "%s:%s:%s" % (hour, min, sec)
        msgdata = opp + "  " + ltime + "\n" + content + "\n"
        win.msgTextCtrl.AppendText(msgdata)
    def startTalkHandle(self, opp):
        print opp, "Start talk"
        win.statusTextCtrl.SetValue(opp+"Start talk")
        
    def connectFailHandle(self):
        print "connection failed"   
        
        #create a message dialogue   
        d = wx.MessageDialog(None, "connection failed", style = wx.OK)
        d.ShowModal()
        d.Destroy()
        win.Destroy()
    def connectDownHandle(self):
        print "connection down"
        
        #create a message dialogue
        d2 = wx.MessageDialog(None, "connection down", style = wx.OK)
        d2.ShowModal() 
        d2.Destroy()
        win.Destroy()

#############################################################################################################
#############################################################################################################
class MyEncrypter(Encrypter):
    def generateKeyPair(self):
        return (123, 456)
    def generateKey(self):
        return 111
    def asymmetricEncrypt(self, message, key):
        return message
    def symmetricEncrypt(self, message, key):
        return message
###############################################################################################################
###############################################################################################################
if __name__ =='__main__':
#create the Login Frame 
    app1 = wx.PySimpleApp()
    loginframe = LoginFrame()
    loginframe.Show()
    app1.MainLoop()

    if(int(list[2])):
        enc = MyEncrypter()
        client = Client(list[1], int(list[2]), list[0], enc)
        #create the main chattingroom
        app2 = wx.PySimpleApp()
        win = MainWindow(None,-1,"chatting room",client)
        win.Show()
        handle = HandleInstance()
        client.connect(handle)
        app2.MainLoop()
