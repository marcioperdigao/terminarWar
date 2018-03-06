import socketHelper,sys,bullet, threading, time, datetime, Map
sessionMap = Map.createMap()
a = sys.stdin.readline(1)
print(" ",end='\n',flush=True)
print(a,end=" ",flush=True)
#servidor
WALKS_DISCTIONARY = {"a":-1,"d":+1,"w":-59,"s":59}
def chat(msg):
    print("chat")
    print(msg)
    l,m = msg
    socket.emitter("chat",(l,m))
def walk(msg):
    # print(msg)
    login, walkingTo = msg
    for user in socket.session:
        if(user._login==login):
            print(user._login,user._alive)
            if(user._alive!=True): return
            if(sessionMap[user._p+WALKS_DISCTIONARY[walkingTo]]!=" "):
                break
            sessionMap[user._p]=" "
            user._p=user._p+WALKS_DISCTIONARY[walkingTo]
            sessionMap[user._p]="9"
            user._side = walkingTo
def shot(msg):
    # print(msg)
    
    login,nothing = msg
    for user in socket.session:
        
        if(user._login==login):
            if(user._bullets<=0): return
            if(user._alive!=True): return
            user._bullets-=1
            position=user._p
            side = user._side
    theId = datetime.datetime.now().timestamp()
    stringId = str(theId)
    b = bullet.Bullet(login,1/15,30,position,side,stringId)
    socket.emitter("newBullet",(position,stringId))
    socket.bulletsSession.append(b)
    T = threading.Thread(target=bulletInTheWay,args=[stringId])
    T.start()

def bulletInTheWay(id):
    # print("bullet in the way: "+id)
    bId=id
    # print(str(len(socket.bulletsSession)))
    for index in range(len(socket.bulletsSession)):
        # print(socket.bulletsSession[index])
        if(socket.bulletsSession[index].id==bId):
            bullet = socket.bulletsSession[index]
            # print(bullet)
            flying = WALKS_DISCTIONARY[bullet.side]
            bullet.position+=flying
            while True:
                # print("Bullet while true")
                if(bullet.distancia<=0):
                    break
                # if(bullet.position<=58): break
                # elif(bullet.position>=944): break
                # elif(bullet.position): break
                # elif(): break
                if(sessionMap[bullet.position]!=" "):
                    # print(sessionMap[bullet.position])
                    if(sessionMap[bullet.position]=="="):
                        break
                    elif(sessionMap[bullet.position]=="|"):
                        break
                    elif(sessionMap[bullet.position]=="X"):
                        break
                    elif(sessionMap[bullet.position]=="9"):
                        # print("Entrou aqui")
                        for user in socket.session:
                            # print(str(user._p)+" "+str(bullet.position))
                            if(user._p==bullet.position):
                                # print("DEAD")
                                user._alive=False
                                user._deaths+=1
                                dead = user._login
                                sessionMap[bullet.position]=" "
                                for userKiller in socket.session:
                                    if(userKiller._login==bullet.login):
                                        userKiller._kills+=1
                                        socket.emitter("userDead",(userKiller._login,userKiller._kills,
                                        userKiller._deaths, user._login,user._kills,user._deaths))
                                bullet.distancia=0
                                break
                bullet.distancia-=1
                # print("distancia: "+str(bullet.distancia))
                bullet.position+=flying
                time.sleep(bullet.velocidade)
            socket.emitter("delBullet",bullet.id)
            for i in range(len(socket.bulletsSession)-1):
                if(socket.bulletsSession[i].id==bId):
                    del socket.bulletsSession[i]
            
            break
def reborn(msg):
    print(msg)
    l,s = msg
    for i in range(len(socket.session)):
        if(socket.session[i]._login==l):
            socket.session[i]._alive = True
            socket.emitter("reborn",l)
            print(str(len(socket.session)))
def disconnect(msg):
    print(msg)
    l,s = msg
    for i in range(len(socket.session)):
        if(socket.session[i]._login==l):
            if(socket.session[i]._senha==s):
                print("Achou")
                socket.session[i]._addr.close()
                del socket.session[i]
                # print(str(len(socket.session)))
def reloadGun(msg):
    l,s = msg
    T = threading.Thread(target=threadReloadGun,args=[l])
    T.start()
def threadReloadGun(l):
    for i in range(len(socket.session)):
        if(socket.session[i]._login==l):
            if(socket.session[i]._alive!=True): return
            if(socket.session[i]._isReloading):
                # print("Ainda carregando")
                return
            socket.session[i]._isReloading=True
            # print("Carregar")
            time.sleep(3)
            
            socket.session[i]._isReloading=False
            socket.session[i]._bullets = 7
IP='localhost'
porta=12397
socket = socketHelper.mySocket(IP,porta)
socket.on("chat",chat)
socket.on("walk",walk)
socket.on("disconnect",disconnect)
socket.on("shot",shot)
socket.on("reborn",reborn)
socket.on("reload",reloadGun)
socket.listen()