from scipy import misc
import numpy as np

class Monster:
    def __init__(self,imgDir,path):
        '''
        initialize the monsters images and the path its going to traverse
        '''
        # load first monster image to get the shape 
        img_1 = misc.imread(imgDir+"/m_1.png")[...,:3]
        
        # store first and additionally load second monster image
        img = np.zeros((2,)+img_1.shape)
        img[0,...] = img_1
        img[1,...] = misc.imread(imgDir+"/m_2.png")[...,:3]
        
        # initialize the classes content
        self.img = img
        self.dim = np.asarray(img.shape[1:3]).reshape(2,1)
        self.path = path
        self.pathIdx = 0
        self.vizMode = int(0)
        
    def getPathPoint(self):
        '''
        return the current path point the monster is located at
        '''
        return self.path[:,self.pathIdx]
    
    def getDrawingDim(self):
        '''
        return the dimensional portion of the monster that fits in the image
        based on the current path position
        '''
        dimensions = np.append(self.dim,self.getPathPoint().reshape(2,1), axis=1)
        
        return np.min(dimensions,axis=1)
    
    def drawMonster(self,dim):
        '''
        draw the portion of the monster that fits into the image. chose which 
        monster image to draw based on its state
        '''
        
        return self.img[self.vizMode,-dim[0]:,-dim[1]:]

    def updateMonsterVizMode(self,globalIterator):
        '''
        switch between monsters visual modes
        '''
        if not(globalIterator%2):
            self.vizMode = 1
        else:
            self.vizMode = 0
            
    def updatePathPoint(self,it):
        '''
        update the monsters current path point
        '''
        self.pathIdx = np.clip(self.pathIdx+it,0,self.path.shape[1]-1)