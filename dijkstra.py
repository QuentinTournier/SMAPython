# -*- coding: utf-8 -*-
from collections import deque
import math
"""
Created on Mon Oct 16 16:10:10 2017

@author: Quentin
2=top
1=left
-1=right
-2=bot
"""



def getDirectionGrid(grid,start,end):
    n = len(grid)
    gridCopy = [[0 for x in range(n)] for y in range(n)]
    gridCopy[end[0]][end[1]] = 10
    
    list = deque([])
    list.append(end)
    while(len(list)>0):
        current = list.popleft()
        for i in range(-1,2):
            for j in range (-1,2):
                if (i!=0 and j!=0) or (i==0 and j==0):
                    continue
                if current[0]+i >=n or current[0]+i<0 or current[1]+j >=n or current[1]+j<0:
                    continue
                if grid[current[0]+i][current[1]+j] !=0 and (current[0]+i != start[0] or current[1]+j != start[1] ):
                    continue
                if gridCopy[current[0]+i][current[1]+j] == 0:
                    gridCopy[current[0]+i][current[1]+j] = 2*i+j
                    if start[0]==current[0]+i and start[1]==current[1]+j:
                        list.clear
                        return gridCopy
                    list.append([current[0]+i,current[1]+j])
    return gridCopy
                    

def dijkstra(grid,start,end):
    gridCopy =  getDirectionGrid(grid,start,end)
    current = start.copy()
    path = []
    if gridCopy[current[0]][current[1]] == 0:
        diffY = end[0] - start[0]
        diffX = end[1] - start[1]
        move = 0;
        if current[0]==end[0] and current[1]==end[1]:
            return -1
        
        if math.fabs(diffX) < math.fabs(diffY):
            move = int(round( diffY/math.fabs(diffY)))
            if gridCopy[current[0]][current[1]-move] == 0:
                move = 0
            move *= -2
        else :
            move = int(round( diffX/math.fabs(diffX)))
            if gridCopy[current[0]-move][current[1]] == 0:
                move = 0
        if move == 0:
            return -1
        else :
            path.append(move)
            return path
        
    while current[0]!=end[0] or current[1]!=end[1]:
        path.append(gridCopy[current[0]][current[1]])
        temp = current[0]
        current[0] = current[0] - int(round(gridCopy[temp][current[1]]/3))
        current[1] = current[1] - int(math.copysign(gridCopy[temp][current[1]]%2,gridCopy[current[0]][current[1]])) 
               
        
    return path

        


