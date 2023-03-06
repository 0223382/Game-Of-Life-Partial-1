"""
conway.py 
A simple Python/matplotlib implementation of Conway's Game of Life.
"""

import sys, argparse
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.animation as animation

ON = 255
OFF = 0
vals = [ON, OFF]


class configuration:
  def __init__(self, name, config):
    self.name = name
    self.config = config

#-------------------Still Lifes----------------------
block = [[ON, ON],
          [ON, ON]]
BLOCK = configuration("block", [block])

beehive = [[OFF, ON, ON, OFF],
            [ON, OFF, OFF, ON],
            [OFF, ON, ON, OFF]]
BEEHIVE = configuration("beehive", [beehive])

loaf = [[OFF, ON, ON, OFF],
        [ON, OFF, OFF, ON],
        [OFF, ON, OFF, ON],
        [OFF, OFF, ON, OFF]]
LOAF = configuration("loaf", [loaf])

boat = [[ON, ON, OFF],
        [ON, OFF, ON],
        [OFF, ON, OFF]]
BOAT = configuration("boat", [boat])

tub = [[OFF, ON, OFF],
        [ON, OFF, ON],
        [OFF, ON, OFF]]
TUB = configuration("tub", [tub])

STILL = [BLOCK, BEEHIVE, LOAF, BOAT, TUB]

#-------------------Oscilators-----------------------
blinker = list()
blinker.append([[ON],
                [ON],
                [ON]])
blinker.append([[ON, ON, ON]])
BLINKER = configuration("blinker", blinker)

toad = list()
toad.append([[OFF, OFF, ON, OFF],
            [ON, OFF, OFF, ON],
            [ON, OFF, OFF, ON],
            [OFF, ON, OFF, OFF]])
toad.append([[OFF, ON, ON, ON],
             [ON, ON, ON, OFF]])
TOAD = configuration("toad", toad)

beacon = list()
beacon.append([[ON, ON, OFF, OFF],
                [ON, ON, OFF, OFF],
                [OFF, OFF, ON, ON],
                [OFF, OFF, ON, ON]])
beacon.append([[ON, ON, OFF, OFF],
                [ON, OFF, OFF, OFF],
                [OFF, OFF, OFF, ON],
                [OFF, OFF, ON, ON]])
BEACON = configuration("beacon", beacon)

OSC = [BLINKER, TOAD, BEACON]

#-----------------Spaceships---------------
glider = list()
glider.append([[OFF, ON, OFF],
                [OFF, OFF, ON],
                [ON, ON, ON]])
glider.append([[ON, OFF, ON],
                [OFF, ON, ON],
                [OFF, ON, OFF]])
glider.append([[OFF, OFF, ON],
                [ON, OFF, ON],
                [OFF, ON, ON]])
glider.append([[ON, OFF, OFF],
                [OFF, ON, ON],
                [ON, ON, OFF]])
GLIDER = configuration("glider", glider)

light = list()
light.append([[ON, OFF, OFF, ON, OFF],
              [OFF, OFF, OFF, OFF, ON],
              [ON, OFF, OFF, OFF, ON],
              [OFF, ON, ON, ON, ON]])
light.append([[OFF, OFF, ON, ON, OFF],
              [ON, ON, OFF, ON, ON],
              [ON, ON, ON, ON, OFF],
              [OFF, ON, ON, OFF, OFF]])
light.append([[OFF, ON, ON, ON, ON],
              [ON, OFF, OFF, OFF, ON],
              [OFF, OFF, OFF, OFF, ON],
              [ON, OFF, OFF, ON, OFF]])
light.append([[OFF, ON, ON, OFF, OFF],
              [ON, ON, ON, ON, OFF],
              [ON, ON, OFF, ON, ON],
              [OFF, OFF, ON, ON, OFF]])
LIGHT = configuration("light-w", light)

SPACE1 = [GLIDER]
SPACE2 = [LIGHT]

ALL_CONFIGS = STILL + OSC + SPACE1 + SPACE2
counters = dict()

filename = "config1.txt"
outFile = "outconfig1.txt"
gens = 200 # generations
current = 0

def initCounters():
    # initialize counter
    for elem in ALL_CONFIGS:
        counters[elem.name] = 0

def sameMatrix(A,B,x,y):
    for i in range(x):
        for j in range(y):
            if (A[i][j] != B[i][j]):
                return False
    return True

def randomGrid(N):
    """returns a grid of NxN random values"""
    return np.random.choice(vals, N*N, p=[0.2, 0.8]).reshape(N, N)

def addGlider(i, j, grid):
    """adds a glider with top left cell at (i, j)"""
    glider = np.array([[0,    0, 255], 
                       [255,  0, 255], 
                       [0,  255, 255]])
    grid[i:i+3, j:j+3] = glider

def update(frameNum, img, grid, visited, N):
    global current
    if current > gens:
        exit()

    # copy grid 8 neighbors
    newGrid = grid.copy()
    initCounters()

    #check configurations
    for i in range(N):
        for j in range(N):
            if not visited[i,j]:
                visited[i, j] = 1
                for elem in ALL_CONFIGS:
                    for configuracion in elem.config:
                        width, heigth = len(configuracion), len(configuracion[0])

                        if i + width + 1 > N or j + heigth + 1 > N: 
                            continue

                        newArr = np.zeros((width+2, heigth+2))
                        newArr[1:width+1, 1:heigth+1] = np.array(configuracion)

                        if sameMatrix(newArr, grid[i:i+width+2, j:j+heigth+2],width+1,heigth+1):
                            counters[elem.name] += 1
                            for x in range(i, i+width+1):
                                for y in range(j, j + heigth + 1):
                                    visited[x,y]=1

            # compute 8-neighbor sum
            total = int((grid[i, (j - 1) % N] + grid[i, (j + 1) % N] +
                         grid[(i - 1) % N, j] + grid[(i + 1) % N, j] +
                         grid[(i - 1) % N, (j - 1) % N] + grid[(i - 1) % N, (j + 1) % N] +
                         grid[(i + 1) % N, (j - 1) % N] + grid[(i + 1) % N, (j + 1) % N]) / 255)

            # Rules
            if grid[i, j] == ON: #less than 2 or more than 3 == die
                if (total < 2) or (total > 3):
                    newGrid[i, j] = OFF
            else:
                if total == 3: #3 neighbor == live
                    newGrid[i, j] = ON

    current += 1

    # save report
    f = open(outFile, "a")
    total = 0
    for key in counters:
        total += counters[key]
    f.write("iteration: {}\n".format(current))
    f.write("---------------------------------------------\n")
    f.write("|			|	count   	|	percent	    |\n")
    f.write("|-----------+---------------+---------------|\n")
    for key, value in counters.items():
        name = key.ljust(10)
        itemCount = str(value).ljust(4)
        percent = 0.0
        if total > 0:
            percent = float(value)  / total *  100
        itempercent = "{:.2f}".format(percent).ljust(6)
        f.write("|{}\t|\t{}\t\t|\t{}\t\t|\n".format(name, itemCount, itempercent))
    f.write("|-----------+---------------+---------------|\n")
    totalitems = str(total).ljust(6)
    f.write("|total      |\t{}\t\t|               |\n".format(totalitems))
    f.write("---------------------------------------------\n")
    f.write("\n")
    print("GENERATION:", str(current), "   -Total:", totalitems)
    f.close()

    # restart visited
    for i in range(N):
        for j in range(N):
            visited[i,j]=0

    # update data
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img,

# main() function
def main():
    global gens
    f = open(filename, "r")
    
    # Command line args are in sys.argv[1], sys.argv[2] ..
    # sys.argv[0] is the script name itself and can be ignored
    # parse arguments
    parser = argparse.ArgumentParser(description="Runs Conway's Game of Life system.py.")
    # TODO: add arguments

    # set grid size
    N = 100
        
    # set animation update interval
    updateInterval = 50

    # declare grid
    grid = np.array([])
    visited = np.array([])

    f = open(filename, "r")
    lines = f.readlines()

    x= lines[0].split()
    x = int(x[0])
    N = x
    gens = lines[1].split()
    gens = int(gens[0])
    grid = np.zeros(x * x).reshape(x, x)
    visited = np.zeros(x * x).reshape(x, x)

    #split to coordinates
    for line in lines[2:]:
        i, j = line.split()
        i,j = int(i), int(j)
        grid[i,j] = ON

    # set up animation
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, visited, N, ),
                                  frames = 10,
                                  interval=updateInterval,
                                  save_count=50)

    plt.show()
    f.close()
# call main
if __name__ == '__main__':
    main()