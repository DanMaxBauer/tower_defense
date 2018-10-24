from scipy import misc
import numpy as np
from utils.monster import Monster


class Environment:
    def __init__(self,mapDir,monsterDir):
        '''
        initialize the monsters path, the maps background and the monster waves
        '''
        # compute the monster path
        self.monsterPath = self.computeMonsterPath(mapDir)
        
        # load the background image
        self.backgroundImg = misc.imread(mapDir+"landscape.png")[...,:3]
        
        # define the monster rounds
        self.waves = [[50,"blobb"],[50,"dot","blobb"],[50,"blobb","dot","blobb"]]
        
        # directery where all monster files are stored
        self.monsterDir = monsterDir
        
        # container for all monsters currently in the environment
        self.monsters = []
        
        # count down for next wave
        self.waveCountDown = 0
        
        # index pointing to the current wave
        self.waveIdx = -1
        
        # index pointing to the next monster in the wave
        self.monsterIdx = 1
        
        # time between monster spawns in a wave
        self.dMonsterSpawnTime = 5
        
        # global counter to track the overall program iteration
        self.globalIdx = np.uint64(0)
        
        
    def computeMonsterPath(self,mapDir):
        '''
        Find monsters entry point on the map and the path points in a sorted way
        '''
        # load monster path image
        monsterPathImg = misc.imread(mapDir+"monster_path.png")[...,:3] 
        
        # find monsters entry point
        pathStart = np.asanyarray(np.where(monsterPathImg[...,0] == 255))
        
        # find path points
        pathPoints = np.asanyarray(np.where(monsterPathImg[...,2] == 255))
        
        # perform region growing starting from the monsters entry point to determine
        # the order in which the monsters traverse the monsterspath
        sortedPathPoints = np.zeros(pathPoints.shape,dtype=int)
        latestUsedIdx = 0
        
        for it in range(pathPoints.shape[1]):
            # compute distance to current way point
            if (it==0):
                currentPoint = pathStart
                pathPoints_tmp = pathPoints
                
            else:
                currentPoint = sortedPathPoints[:,[it-1]]
                pathPoints_tmp = pathPoints_tmp[:,np.arange(pathPoints_tmp.shape[1])!=latestUsedIdx]
                    
            dp = np.sum((pathPoints_tmp - currentPoint)**2,axis=0)
            
            # find index of closest point and store it
            latestUsedIdx = np.argmin(dp)
            sortedPathPoints[:,it] = pathPoints_tmp[:,latestUsedIdx]
            
        return sortedPathPoints
    
    def spawnMonster(self,monsterName):
        '''
        add the next monster to the monsters list
        '''
        monsterName = self.waves[self.waveIdx][self.monsterIdx]
        self.monsters.insert(0,Monster(self.monsterDir+monsterName,self.monsterPath))
        
    def drawMonsters(self):
        '''
        draw all monster into the environment that are currently in the monsters 
        list.
        '''
        backgroundImg_tmp = np.copy(self.backgroundImg)
        
        for monster in self.monsters:
            currPathPoint = self.monsterPath[:,monster.pathIdx]
            dim = monster.getDrawingDim(currPathPoint)
            backgroundImg_tmp[currPathPoint[0]-dim[0]:currPathPoint[0],
                              currPathPoint[1]-dim[1]:currPathPoint[1],:] = monster.drawMonster(dim)
            
        return backgroundImg_tmp
    
    def updateMonsters(self):
        '''
        update the state of all monsters
        '''
        for monster in self.monsters:
            monster.updateMonsterVizMode(self.globalIdx)
            monster.updatePathPoint(1)
    
    def updateEnvironment(self):
        '''
        Perform all update operations
        '''
        # jumb to next waves, if there are any left
        if (self.waveCountDown == 0) and (self.waveIdx < (len(self.waves)-1) ):
            self.waveIdx += 1
            self.waveCountDown = self.waves[self.waveIdx][0]
            self.monsterIdx = 1
        
        # time since the current wave started
        waveTime = self.waves[self.waveIdx][0] - self.waveCountDown
        
        # spawn next monster, if any left in the wave
        numMonsterInWave = len(self.waves[self.waveIdx])
        if not(waveTime % self.dMonsterSpawnTime) and (self.monsterIdx < numMonsterInWave):
            self.spawnMonster(self.waves[self.waveIdx][self.monsterIdx])
            self.monsterIdx += 1                    
        
        # update all monster states
        self.updateMonsters()
        
        # draw all monsters in the environment
        environmentImg = self.drawMonsters()
        
        # update count down
        if (self.waveCountDown > 0):
            self.waveCountDown -= 1
        
        # increase global counter
        self.globalIdx += 1
        
        return environmentImg
            
     
        
        
        
        
        