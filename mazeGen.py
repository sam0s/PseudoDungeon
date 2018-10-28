import random
def generate(size):
    seed=random.randrange(-99999999,999999999)

    #seed = 1621449147
    random.seed(seed)
    #print(seed)
    go=1
    size=size

    cellList=[]
    maze=[]

    for numb in range(size):
        maze.append([0]*(size))
    maze=padMaze(maze,size)

    startpos=(random.randrange(1,size),random.randrange(1,size))
    endpos=(0,0)
    maze[startpos[1]][startpos[0]]=-2

    #right,down,left,up
    dx=[1,0,-1,0]
    dy=[0,1,0,-1]
    #cell count
    cc=0
    for cell in range(4):
        cellCheck=maze[startpos[1]+dy[cc]][startpos[0]+dx[cc]]
        if cellCheck == 0:
            cellList.append((startpos[0]+dx[cc],startpos[1]+dy[cc]))
        cc+=1

    while len(cellList)>0:

        #confirm adrules
        good=0
        timeout=0
        while good<1:
            timeout+=1
            adjacents=0
            chosenID=random.randint(0,len(cellList)-1)
            chosen=cellList[chosenID]
            cc=0
            for cell in range(4):
                cellCheck=maze[chosen[1]+dy[cc]][chosen[0]+dx[cc]]
                if cellCheck == 1:
                    adjacents+=1
                cc+=1
            if adjacents<=1:
                good=2
            if timeout>999:
                good=2
                cellList=[]


        if len(cellList)>0:
            maze[chosen[1]][chosen[0]]=1
            endpos=(chosen[0],chosen[1])
            cc=0
            for cell in range(4):
                cellCheck=maze[chosen[1]+dy[cc]][chosen[0]+dx[cc]]
                if cellCheck == 0:
                    cellList.append((chosen[0]+dx[cc],chosen[1]+dy[cc]))
                cc+=1
            cellList.pop(chosenID)
    endpos=[endpos[0]+1,endpos[1]+1]
    startpos=[startpos[0]+1,startpos[1]+1]

    maze,endpos,startpos=extraMaze(maze,size,endpos,startpos)

    maze[endpos[1]][endpos[0]]=99
    maze[startpos[1]][startpos[0]]=98

    #test spots around enterance for non-wall
    playerPlacement={0:[startpos[0]+1,startpos[1]],1:[startpos[0]-1,startpos[1]],2:[startpos[0],startpos[1]-1],3:[startpos[0],startpos[1]+1]}
    playerPlacementTest={0:maze[startpos[1]][startpos[0]+1]!=0,1:maze[startpos[1]][startpos[0]-1]!=0,2:maze[startpos[1]-1][startpos[0]]!=0,3:maze[startpos[1]+1][startpos[0]]!=0}

    for place in range(4):
        #print (playerPlacementTest[place],place)
        #place player in front of door
        if(playerPlacementTest[place]):startpos=playerPlacement[place];maze[(playerPlacement[place])[1]][(playerPlacement[place])[0]]=1




    return maze,startpos,endpos

def padMaze(maze,size,padNum=-1):
    #duct-taped function written by sam0s (improved)
    f,size=maze,size
    #top and bottom
    f.insert(0,[padNum]*(size))
    f.insert(len(f),[padNum]*(size))
    #sides
    for a in f:
        a.insert(0,padNum)
        a.insert(len(a),padNum)
    return f

def wallPlacement(maze,size,endpos):
    a=[(25-endpos[0]),(25-endpos[1]),(endpos[0]),(endpos[1])]
    side=['r','b','l','t'][a.index(min(a))]

    chosen=-2

    while chosen == -2:
        #print (chosen)
        if side == "r":
            for a in range(len(maze)):
                chosen=random.choice([(maze[a][25])]+[-2]*25)
                if chosen==1: endpos=(26,a+1);break

        if side == "b":
            for x in maze[25]:
                chosen=random.choice([x]+[-2]*25)
                if chosen==1: endpos=(maze[25].index(x)+1,26);break

        if side == "l":
            for a in range(len(maze)):
                chosen=random.choice([(maze[a][1])]+[-2]*25)
                if chosen==1: endpos=(2,a+1);break

        if side == "t":
            for x in maze[1]:
                chosen=random.choice([x]+[-2]*25)
                if chosen==1: endpos=(maze[1].index(x)+1,2);break
        if chosen==1:break
        chosen=-2

    #push point into wall
    endpos={'r':(endpos[0]+1,endpos[1]),'b':(endpos[0],endpos[1]+1),'l':(endpos[0]-1,endpos[1]),'t':(endpos[0],endpos[1]-1)}[side]
    return endpos
def extraMaze(maze,size,endpos,startpos):

    endpos=wallPlacement(maze,size,endpos)
    startpos=wallPlacement(maze,size,startpos)

    #place crates
    xx=0
    yy=0

    for x in maze:
        for y in x:
            if y==-1:
                maze[yy][xx]=0
            if y==-2:
                maze[yy][xx]=1
            if y==1:
                maze[yy][xx]=random.choice([3,4,4,4,4,4,4,4,4]+[1]*89)
            xx+=1
        yy+=1
        xx=0
    return padMaze(maze,size+2,0),endpos,startpos
