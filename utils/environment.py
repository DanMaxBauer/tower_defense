from scipy import misc
import numpy as np
from utils.monster import Monster
import json


class Environment:
    def __init__(self,mapDir,monsterDir,waveDir):
        '''
        initialize the monsters path, the maps background and the monster waves
        '''
        # compute the monster path
        self.monsterPath = self.computeMonsterPath(mapDir)
        
        # load the background image
        self.backgroundImg = misc.imread(mapDir+"landscape.png")[...,:3]
        
        # define the monster rounds
        with open(waveDir+"wave.txt", "rb") as fp:
#            # example
#            self.waves = [[50,"blobb"],[50,"dot","blobb"],[50,"blobb","dot","blobb"]]
            self.waves = json.load(fp)
        
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
        
        # indicates how much damage you can take before you loose
        self.health = 100
        
        # amount of money the play has to buy stuff
        self.money = 10
        
        # indicates whether the game is over
        self.gameStat = 0
        
        
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
    
    def spawnMonster(self):
        '''
        add the next monster to the monsters list
        '''
        # time since the current wave started
        waveTime = self.waves[self.waveIdx][0] - self.waveCountDown
        
        # amount of monsters left in the wave
        numMonsterInWave = len(self.waves[self.waveIdx])
        
        # spawn next monster, if enough time has past AND any monsters are left in the wave
        if not(waveTime % self.dMonsterSpawnTime) and (self.monsterIdx < numMonsterInWave):
            monsterName = self.waves[self.waveIdx][self.monsterIdx]
            self.monsters.insert(0,Monster(self.monsterDir+monsterName,self.monsterPath))
            self.monsterIdx += 1
            
    def killMonster(self,idx):
        '''
        remove monster from monster list if killed or reached end of path
        '''
        del self.monsters[idx]
        
        
        
    def drawMonsters(self,monster,backgroundImg):
        '''
        draw the given monster into the environment 
        '''
        currPathPoint = self.monsterPath[:,monster.pathIdx]
        dim = monster.getDrawingDim(currPathPoint)
        backgroundImg[currPathPoint[0]-dim[0]:currPathPoint[0],
                      currPathPoint[1]-dim[1]:currPathPoint[1],:] = monster.drawMonster(dim)
            
        return backgroundImg
    
    def updateMonsters(self):
        '''
        update the state of all monsters
        '''
        # spawn next monster
        self.spawnMonster() 
        
        # update monsters in map
        backgroundImg_tmp = np.copy(self.backgroundImg)
        
        for it in range(len(self.monsters)):
            # get current monster
            monster = self.monsters[it]
            
            # update its position, appearance and draw it on the map
            endPointFlag = monster.updatePathPoint(1)
            monster.updateMonsterVizMode(self.globalIdx,endPointFlag)            
            backgroundImg_tmp = self.drawMonsters(monster,backgroundImg_tmp)
            
            
            if (endPointFlag) and (monster.despawnTimer>0):
                monster.despawnTimer -= 1
            
            # remove monster if despawn timer is run to zero
            if not(monster.despawnTimer):
                self.health -= monster.damage
                self.killMonster(it)
            
        return backgroundImg_tmp
    
    def updateGameState(self):
        '''
        set game state to over
        if all monsters are dead and no more monsters are in queue 
        OR if health has reached zero
        '''
        areMonstersLeftInGame = len(self.monsters)
        areMonstersLeftInWave = self.monsterIdx < len(self.waves[self.waveIdx])
        isItLastWave = not(self.waveIdx < (len(self.waves)-1))
        
        # you loose
        if (self.health==0):
            self.gameStat = 1
            
        # you win
        elif (not(areMonstersLeftInGame) and 
            not(areMonstersLeftInWave) and
            (isItLastWave)):            
            self.gameStat = 2
        
        
    
    def updateEnvironment(self):
        '''
        Perform all update operations
        '''
        # jumb to next waves, if there are any left
        if (self.waveCountDown == 0) and (self.waveIdx < (len(self.waves)-1) ):
            self.waveIdx += 1
            self.waveCountDown = self.waves[self.waveIdx][0]
            self.monsterIdx = 1             
        
        # update all monster states
        environmentImg = self.updateMonsters()
        
        # test whether the game is already over
        self.updateGameState()
        
        # update count down
        if (self.waveCountDown > 0):
            self.waveCountDown -= 1
        
        # increase global counter
        self.globalIdx += 1
        
        return environmentImg, self.gameStat
            
     
        
        
        
        
        