mapSize=1002
jLimit=58
j=jLimit

def createBox(m,pStart,sizeX,sizeY,style):
    creating=True

    for i in range(sizeY):
        pStart+=jLimit+1
        for j in range(sizeX):
            p = pStart+j
            m[p]=style
    return m

def createMap():
    j=jLimit
    map=[]
    for i in range(mapSize+1):
        if(jLimit==j):
            map.append("|")
            j=0
        elif (j==jLimit-1):
            j=j+1
            map.append("|")
        elif(i<jLimit):
            j=j+1
            map.append("=")
        elif(i>mapSize-jLimit):
            j=j+1
            map.append("=")
        else:
            j=j+1
            map.append(" ")
    map = createBox(map,123,5,4,"X")
    map = createBox(map,536,5,4,"X")
    map = createBox(map,167,5,4,"X")
    map = createBox(map,580,5,4,"X")
    
    return map
