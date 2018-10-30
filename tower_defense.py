print("#==============================#")
print("#  Load Libraries")      
print("#==============================#")
import matplotlib.pyplot as plt
from utils.environment import Environment


print("")
print("#==============================#")
print("#  Define Global Variables")      
print("#==============================#")
MAP_DIR = "./maps/test/" 
MONSTER_DIR = "./monsters/" 
WAVE_DIR = "./waves/test/"
     

print("")
print("#==============================#")
print("#  Define the Environment")      
print("#==============================#")     
environment = Environment(MAP_DIR,MONSTER_DIR,WAVE_DIR)
plt.pause(0.1)    

print("")
print("#==============================#")
print("#  Walk Monster Path")      
print("#==============================#")
print("#")
print("#  visualize the walking")      
plt.figure(1)
boxProps = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

winText = "You somehow did it ^.^"
looseText = "You lost...as suspected..."

frameRate = 0.01 # [s]
gameStat = 0

while not(gameStat):      
    # update environment
    environmentImg, gameStat = environment.updateEnvironment()    
    mapStatus = "HP: "+str(environment.health)+"/"+str(100)+"\n"+"$: "+str(environment.money)
    
    # update figure
    plt.clf()
    plt.imshow(environmentImg)
    
    # shows game status
    if (gameStat==0):
        plt.text(1, 0.95, mapStatus, fontsize=14,
            verticalalignment='top', bbox=boxProps)
        
    elif (gameStat==1):
        plt.text(1, 0.95, looseText, fontsize=14,
        verticalalignment='top', bbox=boxProps)
        
    elif(gameStat==2):
        plt.text(1, 0.95, winText, fontsize=14,
        verticalalignment='top', bbox=boxProps)    
    plt.pause(frameRate)

    # DEBUGGING    
#    print("num Monsters:",len(environment.monsters))
#    print("gloablIdx:",environment.globalIdx)
#    print("waveIdx:",environment.waveIdx)
#    print("monsterIdx:",environment.monsterIdx)
#    print("waveCountDown Idx:",environment.waveCountDown)
#    print("")