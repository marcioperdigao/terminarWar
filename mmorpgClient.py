import socket, pickle,time,os,threading,msvcrt,sys,random
import Action, basicBullet, Map, chatListUsers
createBullet = basicBullet.BasicBullet
createAction = Action.Action

#servidor
IP_server='localhost'
porta_server=12397
ACTION_DICTIONARY = {"a":"walk","w":"walk","s":"walk","d":"walk"," ":"shot","l":"reborn","r":"reload","i":"chat"}
socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# a = (20,20)
# map = numpy.chararray(a)
isRunning=True
isDrawing=True
mapSize=1002
jLimit=58
j=jLimit
class User(object):
    def __init__(self,position,style,alive,login):
        self.p=position
        self.lastPosition=[position-1]
        self.style=style
        self.login=login
        self.alive=alive
        self.kills=0
        self.deaths=0

def filterKeys(key):
    if(key=="a"):
        return True
    elif(key=="d"):
        return True
    elif(key=="s"):
        return True
    elif(key=="w"):
        return True
    elif(key==" "):
        return True
    elif(key=="p"):
        return True
    elif(key=="r"):
        return True
    elif(key=="l"):
        return True
    elif(key=="i"):
        return True    
    else:
        return False
map = Map.createMap()

# map  = createMap()
def cleanMap(position,map):
    map[position]=" "
    return map
def killerAnimation(killer,dead):
    i = random.randrange(4)
    painel = []
    theString1 = killer +" just Killed "+dead+" with a kind of, i don't know, a gun."
    painel.append(theString1)
    theString2 = killer +" matou o "+dead+" de forma implacável. e está imparável!"
    painel.append(theString2)
    painel.append(killer+" matou o "+dead+". A galera enlouqueceu!")
    painel.append(killer+" killed "+dead+". But don't fell like you're the coolest kid in the place or what ever!")
    return painel[i]
def painelCreate():
    i = random.randrange(3)
    painel=[]
    painel.append("                     Ubisoft Apresenta o game que a garotada toda estava esperando, direto do parque da xuxa")
    painel.append("                     Ofecimento Skol, a única que desce redondo. Volkswagen, você conhece, você confia!. Coca-Cola, Sinta o Sabor!")
    painel.append("                     Creditos Marcio Perdigão e Yagolicia")
    return painel[i]
currentStringPainel=""
def animationThread():
    while isRunning:
        time.sleep(2)
        global currentStringPainel
        currentStringPainel = painelCreate()
        while isRunning:
            time.sleep(0.2)
            # print(len(currentStringPainel))
            # print(currentStringPainel)
            if(len(currentStringPainel)==1): break
            currentStringPainel = currentStringPainel[1:]
            
animationT = threading.Thread(target=animationThread)
animationT.start()
listUsers = []
listBullets = []
chatList = []
linha = int(mapSize/jLimit)
def startDrawing():
    print ("Digite (W) para subir, (D) para ir à direita\n"
        +"(S) para descer, (A) para ir à esquerda\n"
        +"(Space) para atirar e(I) para abrir o chat")
    fps=100/1000
    while True:
        
        while isDrawing:

            map = Map.createMap()
            print(currentStringPainel)
            for bullet in listBullets:
                # print(bullet)
                map[bullet.position]="*"
            # print(len(listUsers))
            for user in listUsers:
                if(user.alive):
                    print(" login: "+user.login+": kills: "+str(user.kills)+" deaths: "+str(user.deaths)+" foto: "+user.style)
                    map[user.p]=user.style
                else:
                    if(l==user.login):
                        print("Press (L) to reborn, or just watch the game like a loooooosseeerrr!")
            # map = cleanMap(personagem.p,map)
            j=0
            
            for i in range(mapSize+1):
                if(j==jLimit):
                    j=0
                    theEnd='\n'
                    theFlush=False
                else:
                    j=j+1
                    theEnd=" "
                    theFlush=True
                # print(position)
                # map[personagem.p]=personagem.style
                print(map[i],end=theEnd,flush=theFlush)
            
            print("FPS: "+str(fps))
            for c in chatList:
                print(" "+c.login+"\> "+c.msg)
            time.sleep(fps)
            os.system('cls')
        time.sleep(1)
def sendMessage():
    global isRunning
    global isDrawing
    global l
    global p
    while True:
        
        a = msvcrt.getch()
        # print(a)
        
        if(str(a)==str(b'\xe0')):
            # print("VALOR INVALIDO")
            continue
        if(filterKeys(a.decode("utf-8"))!=True):
            # print("VALOR INVALIDO")
            continue
        if(a.decode("utf-8")=="p"):
            print(a)
            isRunning=False
            isDrawing=False
            sys.exit()
        m = a.decode("utf-8")
        if(a.decode("utf-8")=="i"):
            isDrawing=False
            time.sleep(0.5)
            m = input("Digite a mensagem: ")
            isDrawing=True
        mSend = (ACTION_DICTIONARY[a.decode("utf-8")],((l,m),l,p,""))
        byte = pickle.dumps(mSend)
        socket_cliente.send(byte)
        time.sleep(0.1)
def receive():
    global isRunning
    global isDrawing
    global l
    global p
    global listActions
    while True:
        rec = socket_cliente.recv(1024)
        if(isRunning):
            # print(rec)
            action,msg = pickle.loads(rec)
            # print(action,msg)
            for act in listActions:
                # print(act.actionName,action)
                if(act.actionName==action):
                    act.funAction(msg)
        else:
            mSend = ("disconnect",((l,p),l,p,""))
            byte = pickle.dumps(mSend)
            socket_cliente.send(byte)
            socket_cliente.close()
            sys.exit()

def chat(msg):
    l,m = msg
    global chatList
    # print("chat")
    for user in listUsers:
        if(user.login==l):
            if(len(chatList)>7):
                chatList.pop(0)
            c = chatListUsers.chat(l,m)
            chatList.append(c)
def reborn(login):
    global listUsers
    # print("User is Reborn")
    for index in range(len(listUsers)):
        try:
            if(index>len(listUsers)): break
            if(listUsers[index].login==login):
                listUsers[index].alive=True
                # listUsers.pop(index)
        except Exception as error:
            print("")
def userDead(users):
    global listUsers
    global currentStringPainel
    # print("User is Dead")
    killer,kKills,kDeaths,dead,dKills,dDeaths = users
    currentStringPainel = killerAnimation(killer,dead)
    for index in range(len(listUsers)):
        try:
            if(index>len(listUsers)): break
            if(listUsers[index].login==dead):
                listUsers[index].alive=False
                listUsers[index].kills=dKills
                listUsers[index].deaths=dDeaths
            if(listUsers[index].login==killer):
                listUsers[index].kills=kKills
                listUsers[index].deaths=kDeaths
                # listUsers.pop(index)
        except Exception as error:
            print("")
def delBullet(bID):
    global listBullets
        
    # print(len(listBullets))
    for index in range(len(listBullets)):
        try:
            if(index>len(listBullets)): break
            if(listBullets[index].id==bID):
                listBullets.pop(index)
        except Exception as error:
            print("")
def newBullet(bullet):
    global listBullets
    position,id = bullet
    b = createBullet(position,id)
    listBullets.append(b)

def receiverNewUser(users):
    global listUsers
    listUsers=[]
    for user in users:
        # print("New user "+user._login,user._p,user._style)
        personagem = User(user._p,user._style,user._alive,user._login)
        listUsers.append(personagem)

def receiverUpdateMap(msg):
    users,bullets = msg
    for b in bullets:
        position,id = b
        for bullet in listBullets:
            # print("b.id :",b)
            # print("bullet update: "+bullet.id)
            if(bullet.id==id):
                bullet.position=position
    for u in users:
        position,login = u
        for clientUser in listUsers:
            # print("update login: "+clientUser.login)
            if(clientUser.login==login):
                # for p in clientUser.lastPosition:
                #     if(p!=position):
                #         clientUser.lastPosition.append(clientUser.p)
                clientUser.login = login
                clientUser.p = position

listActions=[]
newUserAction = createAction("newUser",receiverNewUser)
listActions.append(newUserAction)
userDeadAction = createAction("userDead",userDead)
listActions.append(userDeadAction)
userRebornAction = createAction("reborn",reborn)
listActions.append(userRebornAction)
updateMapAction = createAction("updateMap",receiverUpdateMap)
listActions.append(updateMapAction)
newBulletAction = createAction("newBullet",newBullet)
listActions.append(newBulletAction)
delBulletAction = createAction("delBullet",delBullet)
listActions.append(delBulletAction)
chatAction = createAction("chat",chat)
listActions.append(chatAction)
# socket_cliente.bind((IP,porta))
try:
    print("MMORPG, ESSE É O NOME, É O QUE TÁ ESCRITO!")
    l = input("Login: ")
    p = input("Senha: ")
    while True:
        s = input("Digite uma letra para ser seu style: ")
        if(s=="|"):
            print("Este não é um estilo valido.")
        elif(s=="*"):
            print("Este não é um estilo valido.")
        elif(s=="="):
            print("Este não é um estilo valido.")
        elif(s=="X"):
            print("Este não é um estilo valido.")
        else:
            break
    # IP_server = input("Entre com o endereço de IP do servidor: ")
    MSG= ("on",("logando",l,p,s))
    byte = pickle.dumps(MSG)

    socket_cliente.connect((IP_server,porta_server))
    thread_send = threading.Thread(target=sendMessage)
    thread_send.start()
    thread_receive = threading.Thread(target=receive)
    thread_receive.start()
    socket_cliente.send(byte)
    startDrawing()
    # rec=socket_cliente.recv(1024)

    # print(rec)
except Exception as error:
    print(str(error))
    print("Algum erro foi gerado e sei lá! Ignore e provavelmente o erro suma com o tempo")
    socket_cliente.close()
    isRunning=False
    isDrawing=False
    sys.exit()
