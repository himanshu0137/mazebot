import requests
import json
import os
import time

baseURL = 'https://api.noopschallenge.com'
mazeURL = '/mazebot'
directionURL = '/directbot'
randomMaze = '/random?minSize=10&mazSize=10'
walls = '■║║║═╝╗╣═╚╔╠═╩╦╬'
player = '8'


def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')


def drawMaze(maze):
    width = len(maze[0])
    height = len(maze)
    result = [[' ' for i in range(width)] for j in range(height)]
    result[0][0] = walls[5]
    result[0][width-1] = walls[2]
    result[height-1][0] = walls[4]
    result[height-1][width-1] = walls[3]
    for i in range(height):
        for j in range(width):
            if maze[i][j] in [' ', 'A', 'B']:
                result[i][j] = maze[i][j]
            else:
                wallFlag = 0
                if i-1 >= 0 and maze[i-1][j] is 'X':
                    wallFlag |= 1
                if i+1 < height and maze[i+1][j] is 'X':
                    wallFlag |= 2
                if j-1 >= 0 and maze[i][j-1] is 'X':
                    wallFlag |= 4
                if j+1 < width and maze[i][j+1] is 'X':
                    wallFlag |= 8

                result[i][j] = walls[wallFlag]

    return result


def printMaze(map):
    for row in map:
        print(''.join(row))


def addWalls(maze):
    width = len(maze[0]) + 2
    for i in range(len(maze)):
        maze[i] = ['X'] + maze[i] + ['X']
    wall = ['X' for i in range(width)]
    maze = [wall] + maze + [wall]
    return maze


def getDirection():
    return requests.get(baseURL + directionURL).json()['directions']


def move(map, position, step):
    newPostion = [] + position
    if step == 'up':
        newPostion[0] -= 1
    elif step == 'down':
        newPostion[0] += 1
    elif step == 'left':
        newPostion[1] -= 1
    else:
        newPostion[1] += 1

    if newPostion[0] < 0 or newPostion[0] >= len(map):
        return position
    if newPostion[1] < 0 or newPostion[1] >= len(map[0]):
        return position
    if map[newPostion[0]][newPostion[1]] is 'X':
        return position
    return newPostion


def main():
    d = requests.get(baseURL + mazeURL + randomMaze).json()
    map = d['map']
    map = addWalls(map)
    playerPosition = [d['startingPosition'][1] + 1, d['startingPosition'][0] + 1]
    endPosition = [d['endingPosition'][1] + 1, d['endingPosition'][0] + 1]

    while playerPosition[0] != endPosition[0] or playerPosition[1] != endPosition[1]:
        clearScreen()
        map[playerPosition[0]][playerPosition[1]] = player
        newMaze = drawMaze(map)
        printMaze(newMaze)
        step = getDirection()[0]['direction']
        playerPosition = move(map, playerPosition, step)
        time.sleep(0.1)


main()
