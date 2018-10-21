print("#==============================#")
print("#  Load Libraries")      
print("#==============================#")
import numpy as np
import matplotlib.pyplot as plt
from scipy import misc
from utils.monster import Monster

print("")
print("#==============================#")
print("#  Define Global Variables")      
print("#==============================#")
MAP_DIR = "./maps/test/" 
MONSTER_DIR = "./monsters/" 
     

print("")
print("#==============================#")
print("#  Compute Monster Path")      
print("#==============================#")     
print("#")
print("#  load monster path image")
monsterPathImg = misc.imread(MAP_DIR+"monster_path.png")[...,:3]

print("#")
print("#  find monster entry point")      
pathStart = np.asanyarray(np.where(monsterPathImg[...,0] == 255))

print("#")
print("#  find path points")
pathPoints = np.asanyarray(np.where(monsterPathImg[...,2] == 255))

print("#")
print("#  perform region growing to find order in which path is travelled")
sortedPathPoints = np.zeros(pathPoints.shape,dtype=int)
latestUsedIdx = 0

for it in range(pathPoints.shape[1]):
    # compute distance to current way point
    if (it==0):
        currentPoint = pathStart
        pathPoints_tmp = pathPoints
        
    else:
        currentPoint = sortedPathPoints[:,[it]]
        pathPoints_tmp = pathPoints_tmp[:,np.arange(pathPoints_tmp.shape[1])!=latestUsedIdx]
            
    dp = np.sum((pathPoints_tmp - currentPoint)**2,axis=0)
    
    # find index of closest point and store it
    latestUsedIdx = np.argmin(dp)
    sortedPathPoints[:,it] = pathPoints_tmp[:,latestUsedIdx]
    

print("")
print("#==============================#")
print("#  Walk Monster Path")      
print("#==============================#")
print("#")
print("#  load landscape image")
landscapeImg = misc.imread(MAP_DIR+"landscape.png")[...,:3]      

print("#")
print("#  define monsters")
blobbs = Monster(MONSTER_DIR+"blobb/",sortedPathPoints)
      
print("#")
print("#  visualize the walking")      
plt.figure(1)
landscapeImg_tmp = np.copy(landscapeImg)

#for it in range(sortedPathPoints.shape[1]): 
globalIdx = 0
while(True):   
    # update the monsters visual mode
    blobbs.updateMonsterVizMode(globalIdx)
    
    # draw monster partially
    dim = blobbs.getDrawingDim()
    currIdx = blobbs.getPathPoint()
    landscapeImg_tmp[currIdx[0]-dim[0]:currIdx[0],
                     currIdx[1]-dim[1]:currIdx[1],:] = blobbs.drawMonster(dim)
    
    # update figure
    plt.clf()
    plt.imshow(landscapeImg_tmp)
    plt.pause(0.01)

    # reset landscape
    landscapeImg_tmp = np.copy(landscapeImg)
    
    # update monster's path position
    blobbs.updatePathPoint(1)
    
    # update global iterator
    globalIdx += 1