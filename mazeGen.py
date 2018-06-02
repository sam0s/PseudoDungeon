import random

def generate(size):
    seed=random.randrange(-99999999,999999999)
    random.seed(seed)
    print(seed)
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
    print (startpos)
    return extraMaze(maze,size),[startpos[0]+1,startpos[1]+1],[endpos[0]+1,endpos[1]+1]

def padMaze(maze,size,padNum=-1):
    #duct-taped function written by sam0s (improved)
    f=maze
    size=size
    #top and bottom
    f.insert(0,[padNum]*(size))
    f.insert(len(f),[padNum]*(size))

    #sides
    for a in f:
        a.insert(0,padNum)
        a.insert(len(a),padNum)
    return f

def extraMaze(maze,size):
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
                maze[yy][xx]=random.choice([3,4,4,4]+[1]*89)
            xx+=1
        yy+=1
        xx=0
    return padMaze(maze,size+2,0)
