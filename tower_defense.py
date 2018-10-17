print("#==============================#")
print("#  Load Libraries")      
print("#==============================#")
import numpy as np
import matplotlib.pyplot as plt
from scipy import misc

print("")
print("#==============================#")
print("#  Define Global Variables")      
print("#==============================#")
MAP_DIR = "./maps/test/" 
ENEMY_DIR = "./enemies/" 
     

print("")
print("#==============================#")
print("#  Compute Enemy Path")      
print("#==============================#")     
print("#")
print("#  load enemy path image")
enemyPathImg = misc.imread(MAP_DIR+"enemy_path.png")[...,:3]

print("#")
print("#  find enemy entry point")      
pathStart = np.asanyarray(np.where(enemyPathImg[...,0] == 255))

print("#")
print("#  find path points")
pathPoints = np.asanyarray(np.where(enemyPathImg[...,2] == 255))

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
print("#  Walk Enemy Path")      
print("#==============================#")
print("#")
print("#  load landscape image")
landscapeImg = misc.imread(MAP_DIR+"landscape.png")[...,:3]      

print("#")
print("#  load enemy image")
# load first enemy image to get the shape 
enemy_blobb_tmp = misc.imread(ENEMY_DIR+"blobb/blobb_1.png")[...,:3]

# store first and additionally load second enemy image
enemy_blobb = np.zeros((2,)+enemy_blobb_tmp.shape)
enemy_blobb[0,...] = enemy_blobb_tmp
enemy_blobb[1,...] = misc.imread(ENEMY_DIR+"blobb/blobb_2.png")[...,:3]
      
print("#")
print("#  visualize the walking")      
plt.figure(1)
landscapeImg_tmp = np.copy(landscapeImg)

for it in range(sortedPathPoints.shape[1]):
    # get current path point
    currIdx = sortedPathPoints[:,it]
    
    # define enemy mode
    if not(it%2):
        enMode = 1
    else:
        enMode = 0
    
    # draw monster partially
    xDim = np.min([enemy_blobb.shape[1],currIdx[0]])
    yDim = np.min([enemy_blobb.shape[2],currIdx[1]])
    landscapeImg_tmp[currIdx[0]-xDim:currIdx[0],
                         currIdx[1]-yDim:currIdx[1],:] = enemy_blobb[enMode,-xDim:,-yDim:]       
    
    # update figure
    plt.clf()
    plt.imshow(landscapeImg_tmp)
    plt.pause(0.01)

    # reset landscape
    landscapeImg_tmp = np.copy(landscapeImg)