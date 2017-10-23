from threading import Thread, RLock
import socket
import dijkstra
import time

"""
Created on Mon Oct 16 16:10:10 2017

@author: Quentin
2=top
1=left
-1=right
-2=bot
"""

nb_agent=5
n = 5
grid = [[0 for x in range(n)] for y in range(n)]
lock = RLock()

def checkWin() :
    for i in range(nb_agent):
        if grid[0][i] != i+1 :
            return 0
    return 1


class Agent(Thread):
    def __init__(self, ip, port, ports_lists,key, iniX, iniY, goalX, goalY): 
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.ports_lists = ports_lists
        self.key = key
        self.posX = iniX
        self.posY = iniY
        self.goalX = goalX
        self.goalY = goalY
        print("voile")
        with lock :
            grid[self.posY][self.posX] = key



    def run(self):
        global grid
        cont = 0
        while checkWin() == 0 and cont < 30 :
            if self.posX != self.goalX or self.posY != self.goalY:
                nextMoves = dijkstra.dijkstra(grid,[self.posY, self.posX], [self.goalY, self.goalX])
                if nextMoves == -1 :
                    cont += 1
                    time.sleep(1)
                    continue
                nextMove = nextMoves[0]
                with lock :
                    grid[self.posY][self.posX] = 0 
                    if nextMove == -2:
                        self.posY += 1                        
                    elif nextMove == -1 :
                        self.posX += 1
                    elif nextMove == 1 :
                        self.posX -= 1
                    elif nextMove == 2 :
                        self.posY -= 1
                    grid[self.posY][self.posX] = self.key
                cont +=1
                for z in range(len(grid)):
                    print(grid[z])
            time.sleep(1) #seconds
        print("MOI G FINI, JE MAPEL " + str(self.key))
                    
agents = [None] * nb_agent
for i in range(nb_agent) :
    agent = Agent(0,0,[0,0], i+1,4-i,4,i,0)
    agents[i] = agent
for i in range(nb_agent) :
    agents[i].start() 
for i in range(nb_agent) :
    agents[i].join()

            
        
