import wx

list = ["0","0","0"]


class LoginFrame(wx.Frame):
    

    def __init__(self):
        wx.Frame.__init__(self, None, -1, title = 'Windows for Login',
                          style = wx.DEFAULT_FRAME_STYLE^wx.MAXIMIZE_BOX^wx.RESIZE_BORDER,
                          size=(300, 200))

        self.USERNAME = ""
        self.PORT =""
        self.IP = ""
        
        panel = wx.Panel(self, -1)
        self.hintLabel = wx.StaticText(panel, -1, "     Please enter your username, your IP and port")
        self.nameLabel = wx.StaticText(panel, -1, "username:")
        self.nameText = wx.TextCtrl(panel, -1, "",
                            size=(175, -1))
        self.nameText.SetInsertionPoint(0)

        self.IpLabel = wx.StaticText(panel, -1, "         IP:")
        self.IpText = wx.TextCtrl(panel, -1, "", size=(175, -1))
        
        self.portLabel = wx.StaticText(panel, -1, "       port:")
        self.portText = wx.TextCtrl(panel, -1, "", size=(175, -1), style = wx.TE_PROCESS_ENTER)
        
        self.LoginButton = wx.Button(panel,-1,"login")
        
        nullLabel1 = wx.StaticText(panel, -1)
        nullLabel2 = wx.StaticText(panel, -1)
        buttonsizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonsizer.Add(nullLabel1,2)
        buttonsizer.Add(self.LoginButton,1)
        buttonsizer.Add(nullLabel2,1)
        
        
        namesizer = wx.BoxSizer(wx.HORIZONTAL)
        namesizer.Add(self.nameLabel,1,wx.ALL,1)
        namesizer.Add(self.nameText,3,wx.ALL,1)
        
        Ipsizer = wx.BoxSizer(wx.HORIZONTAL)
        Ipsizer.Add(self.IpLabel,1,wx.ALL,1)
        Ipsizer.Add(self.IpText,3,wx.ALL,1)
        
        namesizer = wx.BoxSizer(wx.HORIZONTAL)
        namesizer.Add(self.nameLabel,1,wx.ALL,1)
        namesizer.Add(self.nameText,3,wx.ALL,1)
        
        portsizer = wx.BoxSizer(wx.HORIZONTAL)
        portsizer.Add(self.portLabel,1,wx.ALL,1)
        portsizer.Add(self.portText,3,wx.ALL,1)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.hintLabel,1,wx.ALL,1)        
        sizer.Add(namesizer,1,wx.ALL,1)
        sizer.Add(Ipsizer,1,wx.ALL ,1)
        sizer.Add(portsizer,1,wx.ALL,1)
        sizer.Add(buttonsizer,1,wx.ALL)
        panel.SetSizer(sizer)
        
        self.Bind(wx.EVT_BUTTON, self.OnSave, self.LoginButton)
        self.Bind(wx.EVT_TEXT_ENTER,self.OnSave,self.portText)
        
    def OnSave(self,event):
        self.USERNAME =  self.nameText.GetValue()
        #list.append(self.USERNAME)
        list[0] = self.USERNAME
        self.IP = self.IpText.GetValue()
        #list.append(self.IP)
        list[1] = self.IP
        self.PORT = self.portText.GetValue()
        #list.append(self.PORT)
        list[2] = self.PORT
        self.Close(True)
        self.Destroy()
        
    
    
if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = LoginFrame()
    frame.Show()
    app.MainLoop()
    
    
