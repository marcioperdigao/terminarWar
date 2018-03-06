import datetime

class User(object):
    
    def __init__(self,p,alive,login,senha,addr,s,side):
        self._p = p
        self._alive = alive
        self._login = login
        self._senha = senha
        self._addr = addr
        self._style = s
        self._side=side
        self._deaths = 0
        self._kills = 0
        self._bullets = 7
        self._isReloading = False
    def walkLeft():
        self.p=self.p-1
    def walkRight():
        self.p=self.p+1
    def walkUp():
        self.p=self.p-jLimit-1
    def walkDown():
        self.p=self.p+jLimit+1
    def newSession(self):
        self._sessionNumber = datetime.datetime.now().timestamp()