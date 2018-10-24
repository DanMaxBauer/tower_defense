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
text = "HP: "+str(100)+"/"+str(100)+"\n"+"$: "+str(10)

while(True):      
    # update environment
    environmentImg = environment.updateEnvironment()    
    
    # update figure
    plt.clf()
    plt.imshow(environmentImg)        
    plt.text(1, 0.95, text, fontsize=14,
        verticalalignment='top', bbox=boxProps)
    plt.pause(0.01)

    # DEBUGGING    
#    print("num Monsters:",len(environment.monsters))
#    print("gloablIdx:",environment.globalIdx)
#    print("waveIdx:",environment.waveIdx)
#    print("monsterIdx:",environment.monsterIdx)
#    print("waveCountDown Idx:",environment.waveCountDown)
#    print("")