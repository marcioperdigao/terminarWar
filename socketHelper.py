import socket,pickle,threading,time,random
import basicUser
import User
import Action
createBasicUser = basicUser.UserBasic
createAction = Action.Action
createUser = User.User
socket_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
class mySocket(threading.Thread):
    
    sockets=[]
    session=[]
    bulletsSession=[]
    def __init__(self,ip,porta):
        super(mySocket,self).__init__()
        self.ip="localhost"
        # self.ip=socket.gethostname()
        self.porta=porta
    
    def findAction(self,act):
        # print("find action")
        # print(len(self.sockets))
        # print(act,self.sockets)
        for row in self.sockets:
            # print (row.actionName,act)
            if(row.actionName==act):
                return row
        return False

    def buscarSession(self,login,senha):
        # print ("Buscar session")
        # print(len(self.session))

        for row in self.session:
            # print(row._login)
            if(row._login==login):
                # print ("login existe")
                if(row._senha==senha):
                    # print ("senha confere")
                    return row
                else:
                    print("senha incorreta")
                    return False
            
        # print ("Login não existe")
        return False
    def newUser(self,login,senha,addr,s):
        print (login,senha,s)
        n = random.randrange(4)
        if(n==0):
            pStart=122
        elif(n==1):
            pStart=542
        elif(n==2):
            pStart=160
        elif(n==3):
            pStart=586
        newUser = createUser(pStart,True,login,senha,addr,s,"a")
        self.session.append(newUser)
        return newUser
    def broadcaster(self):
        while True:
            time.sleep(100/1000)
            listUsers=[]
            listBullets=[]
            for u in self.session:
                userToSend = (u._p, u._login)
                listUsers.append(userToSend)

            for b in self.bulletsSession:
                bulletsToSend = (b.position,b.id)
                listBullets.append(bulletsToSend)
            MSG = ("updateMap",(listUsers,listBullets))
            byte = pickle.dumps(MSG)
            for index in range(len(self.session)):
                try:
                    self.session[index]._addr.send(byte)
                except Exception as error:
                    print(str(error))
                    del self.session[index]
    def emitter(self,action,user):
        time.sleep(0.01)
        print("Emitter")
        print(action,user)
        userToSend = (action,user)
        byte = pickle.dumps(userToSend)
        for u in self.session:
            # print(u._login)
            u._addr.send(byte)
    
    def on(self,actionName,callback):
        print("criar action")
        print(actionName,callback)
        print(len(self.sockets))
        
        for a in self.sockets:
            print("VEIO AQUI")
            if(a.actionName==actionName):
                print ("Action já existe. Sobrescrevendo action")
                a.funAction = callback
                return
            else:
                newAction = createAction(actionName,callback)
                self.sockets.append(newAction)
                return
        if(len(self.sockets)==0):
            newAction = createAction(actionName,callback)
            self.sockets.append(newAction)
            print(len(self.sockets))
    def logar(self,user,addr):
        print("Logar")
        # user.newSession()
        # byte = pickle.dumps(user)
        # sessionString = str(user._sessionNumber)
        # socket_server.sendto(sessionString.encode("ascii"),addr)
        users = []
        for anUser in self.session:
            u = createBasicUser(anUser._p,anUser._alive,anUser._login,anUser._style)
            users.append(u)

        T = threading.Thread(target=self.emitter,args=("newUser",users))
        T.start()
    def conectado(self,con,cliente):
        print("conectando...")
        print(con,cliente)
        while True:
            try:
                byte = con.recv(1024)
                if not byte: break
                msg = pickle.loads(byte)
                action,fullMsg = msg
                # print(fullMsg)
                msg, login,senha,s = fullMsg
                # print(msg, login,senha,s)
                user = self.buscarSession(login,senha)
                if(user):
                    # print ("Usuario ja existe")
                    if(action=="on"):
                        self.logar(user,con)
                        continue
                    doAction = self.findAction(action)
                    # print(doAction)
                    if(doAction!=False):
                        doAction.funAction(msg)
                else:
                    user = self.newUser(login,senha,con,s)
                    print("Usuario criado")
                    print (msg,con)
                    self.logar(user,con)
            except Exception as error:
                print(str(error))
                break
                con.close()
        con.close()
    def listen(self):
        socket_server.bind((self.ip,self.porta))
        socket_server.listen(5)

        T = threading.Thread(target=self.broadcaster)
        T.start()
        while True:
            try:
                con,cliente = socket_server.accept()
                C = threading.Thread(target=self.conectado,args=(con,cliente))
                C.start()
            except Exception as error:
                # self.session.pop()
                print ("Error: "+str(error))
            
                    
        socket_server.close()