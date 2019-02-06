import turtle
from math import sqrt
import time
ekran=turtle.Screen()
ekran.bgcolor("black")
ekran.title("Pacman")
ekran.setup(1000,1000)
turtle.register_shape("kucukpac.gif")

def DFS(x,y,Map): 
    if (Map[x][y]=="Y"): 
        return [(x,y)] 
    if (Map[x][y]!="P"): 
        return [] 
    Map[x][y]="explored" 
    for i in [[x-1,y],[x+1,y],[x,y-1],[x,y+1]]: 
            result = DFS(i[0],i[1],Map) 
            if len(result)>0: 
                result.append((x,y)) 
                return result 
    return [] 

def DrawMap(Map,path): 
    for x in range(0,len(Map)): 
        for y in range(0,len(Map[x])): 
            if ((x,y) in path): 
                assert Map[x][y] in ("P","Y") 
                Map[x][y]="P"

from collections import deque 
def BFS(x,y,Map): 
    queue = deque( [(x,y,None)]) 
    while len(queue)>0: 
        node = queue.popleft() 
        x = node[0] 
        y = node[1] 
        if Map[x][y] == "Y":
            return GetPathFromNodes(node) 
        if (Map[x][y]!="P"): 
            continue 
        Map[x][y]="explored" 
        for i in [[x-1,y],[x+1,y],[x,y-1],[x,y+1]]: 
            queue.append((i[0],i[1],node))
    return [] 



class Node():

    def __init__(self, parent=None, position=None):

        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0
    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end):
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0
    open_list = []
    closed_list = []
    open_list.append(start_node)

    while len(open_list) > 0:
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index
        open_list.pop(current_index)
        closed_list.append(current_node)
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] 
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: 
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue
            if maze[node_position[0]][node_position[1]] != 0:
                continue
            new_node = Node(current_node, node_position)
            children.append(new_node)
        for child in children:
            for closed_child in closed_list:
                if child == closed_child:
                    continue
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue
            open_list.append(child)
dirs = [
    lambda x, y, z, p: (x, y - 1, z + 1, p + [(x, y)]),
    lambda x, y, z, p: (x, y + 1, z + 1, p + [(x, y)]),
    lambda x, y, z, p: (x - 1, y, z + 1, p + [(x, y)]),
    lambda x, y, z, p: (x + 1, y, z + 1, p + [(x, y)]),
    lambda x, y, z, p: (x - 1, y - 1, z + sqrt(2), p + [(x, y)]),
    lambda x, y, z, p: (x + 1, y - 1, z + sqrt(2), p + [(x, y)]),
    lambda x, y, z, p: (x - 1, y + 1, z + sqrt(2), p + [(x, y)]),
    lambda x, y, z, p: (x + 1, y + 1, z + sqrt(2), p + [(x, y)])
]

def valid(grid, x, y):
    return 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] == 0

def adjacent(grid, frontier):
    for (x, y, z, p) in frontier:
        for d in dirs:
            nx, ny, nz, np = d(x, y, z, p)
            if valid(grid, nx, ny):
                yield (nx, ny, nz, np)

def flood(grid, frontier):
    res = list(adjacent(grid, frontier))
    for (x, y, z, p) in frontier:
        grid[x][y] = 1
    return res

def UCS(grid, start, end):
    start, end = tuple(start), tuple(end)
    frontier = [(start[0], start[1], 0, [])]
    res = []
    while frontier and grid[end[0]][end[1]] == 0:
        frontier = flood(grid, frontier)
        for (x, y, z, p) in frontier:
            if (x, y) == end:
                res.append((p + [(x, y)]))
    if not res:
        return ()
    return sorted(res)[0]



def GetPathFromNodes(node): 
    path = [] 
    while(node != None): 
        path.append((node[0],node[1])) 
        node = node[2] 
    return path

def HaritaDegistir(harita):
    for y in range(len(harita)):
        for x in range(len(harita[y])):
            if(harita[y][x]=="X"):
                harita[y][x]=1
            if(harita[y][x]=="P") or (harita[y][x]=="Y"):
                harita[y][x]=0
    return harita


class Kalem(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.shapesize()
        self.color("blue")
        self.penup()
        self.speed(0)
class Yol_Gosterici(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("circle")
        self.shapesize(0.1,0.1)
        self.color("orange")
        self.penup()
        self.speed(0)
class Oyuncu(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("kucukpac.gif")
        self.shapesize(24,24)
        self.penup()
        self.speed(0)
        self.altin=0
        self.goto(-144,144)
    def yukari_git(self):
        gidilen_yerin_x=oyuncu.xcor()
        gidilen_yerin_y=oyuncu.ycor()+24
        if(gidilen_yerin_x,gidilen_yerin_y) not in duvarlar:
            self.goto(gidilen_yerin_x,gidilen_yerin_y)
    def asagi_git(self):
        gidilen_yerin_x=oyuncu.xcor()
        gidilen_yerin_y=oyuncu.ycor()-24
        if(gidilen_yerin_x,gidilen_yerin_y) not in duvarlar:
            self.goto(gidilen_yerin_x,gidilen_yerin_y)
    def saga_git(self):
        gidilen_yerin_x=oyuncu.xcor()+24
        gidilen_yerin_y=oyuncu.ycor()
        if(gidilen_yerin_x,gidilen_yerin_y) not in duvarlar:
            self.goto(gidilen_yerin_x,gidilen_yerin_y)
    def sola_git(self):
        gidilen_yerin_x=oyuncu.xcor()-24
        gidilen_yerin_y=oyuncu.ycor()
        if(gidilen_yerin_x,gidilen_yerin_y) not in duvarlar:
            self.goto(gidilen_yerin_x,gidilen_yerin_y)           
    def carpisti_mi(self,other):
        a=self.xcor()-other.xcor()
        b=self.ycor()-other.ycor()
        distance=(a**2)+(b**2)
        if distance<25:
            return True
        else:
            return False
        
class Yem(turtle.Turtle):
    def __init__(self,x,y):
        turtle.Turtle.__init__(self)
        self.shape("circle")
        self.color("gold")
        self.shapesize(1/3,1/3)
        self.penup()
        self.speed(0)
        self.altin=100
        self.goto(x,y)
    def destroy(self):
        self.goto(2000,2000)
        self.hideturtle()

def Harita_Secimi(harita_boyutu):
    if(harita_boyutu=="0"):
        harita=[
    ["X","X","X","X","X","X"],
    ["X","P","P","P","P","X"],
    ["X","P","X","Y","P","X"],
    ["X","P","X","X","P","X"],
    ["X","P","X","X","P","X"],
    ["X","P","P","P","P","X"],
    ["X","X","X","X","X","X"],
    ]
        return harita

    if(harita_boyutu=="1"):
        harita=[
    ["X","X","X","X","X","X","X","X"],
    ["X","P","P","P","X","P","P","X"],
    ["X","P","X","P","X","P","P","X"],
    ["X","P","X","X","X","X","P","X"],
    ["X","P","P","P","P","P","P","X"],
    ["X","P","X","P","X","X","P","X"],
    ["X","P","X","P","P","P","Y","X"],
    ["X","X","X","X","X","X","X","X"]
    ]
        return harita
    
    if(harita_boyutu=="2"):
        harita=[
    ["X","X","X","X","X","X","X","X","X","X","X","X"],
    ["X","P","P","P","X","P","P","X","P","P","Y","X"],
    ["X","P","X","P","X","P","P","P","P","X","P","X"],
    ["X","P","X","X","X","X","P","X","X","X","X","X"],
    ["X","P","P","P","P","P","P","X","P","P","P","X"],
    ["X","P","X","P","X","X","P","P","P","P","X","X"],
    ["X","P","P","P","P","P","P","P","P","P","P","X"],
    ["X","X","P","X","X","P","X","X","X","X","P","X"],
    ["X","P","P","P","X","P","P","X","P","P","P","X"],
    ["X","P","P","P","X","P","P","X","P","P","P","X"],
    ["X","P","P","P","X","P","P","X","P","P","P","X"],
    ["X","X","X","X","X","X","X","X","X","X","X","X"]
    ]
        return harita
    
def AlgoritmaIslet(harita_boyutu,algoritma_secimi):
    if(harita_boyutu=="0"):
        bitis=(2,3)
    elif(harita_boyutu=="1"):
        bitis=(6,6)
    elif(harita_boyutu=="2"):
        bitis=(10,3)

    if(algoritma_secimi=="1"):
        bfsyol=BFS(1,1,Harita_Secimi(harita_boyutu))
        labirent_ciz(Harita_Secimi(harita_boyutu),bfsyol)
    if(algoritma_secimi=="2"):
        dfsyol=DFS(1,1,Harita_Secimi(harita_boyutu))
        labirent_ciz(Harita_Secimi(harita_boyutu),dfsyol)
    if(algoritma_secimi=="3"):
        astaryol=astar(HaritaDegistir(Harita_Secimi(harita_boyutu)),(1,1),bitis)
        labirent_ciz(Harita_Secimi(harita_boyutu),astaryol)
    if(algoritma_secimi=="4"):
        ucsyol=UCS(HaritaDegistir(Harita_Secimi(harita_boyutu)),(1,1),bitis)
        labirent_ciz(Harita_Secimi(harita_boyutu),ucsyol)
def labirent_ciz(harita,yol):
    sayac=0
    for y in range(len(harita)):
        for x in range(len(harita[y])):
            
            character=harita[y][x]
            screen_x=-168+(x*24)
            screen_y=168-(y*24)
            if (y,x) in yol:
                Yol_Gosterici.goto(screen_x,screen_y)
                Yol_Gosterici.stamp()
                yolgostericiler.append((screen_x,screen_y))
                sayac=sayac+1
                oyuncu.goto(screen_x,screen_y)
                time.sleep(0.5)
            if character == "X":
                kalem.goto(screen_x,screen_y)
                kalem.stamp()
                duvarlar.append((screen_x,screen_y))
            if character == "O":
                oyuncu.goto(screen_x,screen_y)
                oyuncu.stamp()
            if character=="Y":
                yemler.append(Yem(screen_x,screen_y))
    print(str(sayac)+" adimda cozume ulasildi.")

duvarlar=[]
yemler=[]
yolgostericiler=[]
kalem=Kalem()
Yol_Gosterici=Yol_Gosterici()
oyuncu=Oyuncu()

harita_boyutu=input("Lutfen harita boyutunu 0,1 ya da 2 olarak belirleyiniz:")
algoritma_secimi=input("BFS-->1 DFS-->2 A*-->3 UCS-->4:")

AlgoritmaIslet(harita_boyutu,algoritma_secimi)
    
ekran.tracer(0)

turtle.listen()

turtle.onkey(oyuncu.sola_git,"a")
turtle.onkey(oyuncu.saga_git,"d")
turtle.onkey(oyuncu.yukari_git,"w")
turtle.onkey(oyuncu.asagi_git,"s")


while True:
    for yem in yemler:
        if oyuncu.carpisti_mi(yem):
            oyuncu.altin+=yem.altin
            print("Oyuncunun Altin Miktari: {}".format(oyuncu.altin))
            yem.destroy()
            yemler.remove(yem)

    ekran.update()