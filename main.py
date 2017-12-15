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

nb_agent=15
n = 5
grid = [[0 for x in range(n)] for y in range(n)]
lock = RLock()
sharedMails = {}

def checkWin() :
    for i in range(nb_agent):
        if grid[0][i] != i+1 :
            return 0
    return 1


class Agent(Thread):
    def __init__(self,key, iniX, iniY, goalX, goalY): 
        Thread.__init__(self)
        self.key = key
        self.posX = iniX
        self.posY = iniY
        self.goalX = goalX
        self.goalY = goalY
        with lock :
            grid[self.posY][self.posX] = key



    def run(self):
        global grid
        global sharedMails
        sharedMails[self.key] = []
        cont = 0
        while checkWin() == 0 and cont < 30 :
            if self.key == 1:
                for i in range(n):
                    print(grid[i])
                print("\n")
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
            time.sleep(1) #seconds
                    
agents = [None] * nb_agent
for i in range(nb_agent) :
    agent = Agent(i+1,(n-1-i)%n,i//n,(i+1)%n,n-(i//n)-1)
    agents[i] = agent
for i in range(nb_agent) :
    agents[i].start() 
for i in range(nb_agent) :
    agents[i].join()

            
        
