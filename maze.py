#20K1113 小池優太郎

import copy
import random
from dataclasses import dataclass, field

SPACE=0
WALL=1
VISITED=5
START=8
GOAL=9

@dataclass
class Maze:
    row_num: int=field(init=False, default=None)
    line_num: int=field(init=False, default=None)
    floormap: list=field(init=False, default=None)

    def get_block(self, x, y):
        return self.floormap[y][x]

    def set_block(self, x, y, block):
        self.floormap[y][x] = block

    def set_floormap(self, row_num, line_num, floormap):
        self.row_num=row_num
        self.line_num=line_num
        self.floormap=floormap

    def save_file(self,filename):
        with open(filename,mode='w') as file:
            file.write(f"{self.line_num},{self.row_num}\n")
            for row in self.floormap:
                for ch in row:
                    file.write(str(ch))
                file.write('\n')

    def from_file(self,filename):
        with open(filename,mode='r',encoding="utf-8-sig") as file:
            first_line= file.readline().rstrip('\n')
            fields=first_line.split(',')
            self.line_num=int(fields[0])
            self.row_num=int(fields[1])
            self.floormap=[]
            for line in file:
                row=[int(ch) for ch in line.rstrip('\n')]
                self.floormap.append(row)
            if len(self.floormap) != self.row_num:
                raise Exception("mismatch map data (row_num)")

    def duplicate(self):
        new_floormap=copy.deepcopy(self.floormap)
        new_maze=Maze()
        new_maze.set_floormap(self.row_num,self.line_num,new_floormap)
        return new_maze

    def search(self,block_type):
        for i in range(len(self.floormap)):
            for j in range(len(self.floormap[0])):
                if self.floormap[i][j] == block_type:
                    return (i,j)
        return (-1,-1)

    def create_maze(self, line_num, row_num):
        if line_num%2 == 0:
            line_num += 1
        if row_num%2 == 0:
            row_num += 1
        self.line_num = line_num
        self.row_num = row_num
        self.floormap=[[SPACE for i in range(line_num)] for j in range(row_num)]
        for x in range(line_num):
            self.set_block(x,0,WALL)
            self.set_block(x,row_num-1,WALL)
        for y in range(row_num):
            self.set_block(0,y,WALL)
            self.set_block(line_num-1,y,WALL)
        for y in range(0,row_num,2):
            for x in range(0,line_num,2):
                self.set_block(x,y,WALL)
        built=[]
        for y in range(row_num):
            row=[]
            for x in range(line_num):
                row.append(x==0 or x==line_num-1 or y==0 or y==row_num-1)
            built.append(row)
        finished=False
        while not finished:
            finished=True
            for y in range(2,row_num-1,2):
                for x in range(2,line_num-1,2):
                    if built[y][x]:
                        continue
                    finished=False
                    direction = random.choice(['L','R','U','D'])
                    if direction=='L' and built[y][x-2]:
                        self.set_block(x-1,y,WALL)
                        built[y][x]=True
                    elif direction=='R' and built[y][x+2]:
                        self.set_block(x+1,y,WALL)
                        built[y][x]=True
                    elif direction=='U' and built[y-2][x] and y==2 :
                        self.set_block(x,y-1,WALL)
                        built[y][x]=True
                    elif direction=='D' and built[y+2][x]:
                        self.set_block(x,y+1,WALL)
                        built[y][x]=True
        self.set_block(1,1,START)
        self.set_block(line_num-2,row_num-2,GOAL)

    def is_next_to(self,place1,place2):
        return ((place1[0]==place2[0] and abs(place1[1]-place2[1])==1)
                 or (place1[1]==place2[1] and abs(place1[0]-place2[0])==1))

    def path_search(self,start_v):
        backup = copy.deepcopy(self.floormap)
        if self.floormap[start_v[0]][start_v[1]] == GOAL:
            return []
        to_visit = [start_v]
        visited_places=[]
        while len(to_visit) > 0:
            v = to_visit.pop(0)
            visited_places.append(v)
            if self.floormap[v[0]][v[1]] == SPACE:
                self.floormap[v[0]][v[1]] = VISITED
            for dv in [(-1,0),(0,1),(1,0),(0,-1)]:
                new_v=(v[0]+dv[0],v[1]+dv[1])
                block = self.floormap[new_v[0]][new_v[1]]
                if block == WALL:
                    continue
                elif block == SPACE:
                    to_visit.append(new_v)
                elif block == GOAL:
                    to_visit=[]
                    visited_places.append(new_v)
                    break
        for i in range(len(self.floormap)):
            for j in range(len(self.floormap[0])):
                if self.floormap[i][j]==VISITED:
                    self.floormap[i][j]=SPACE
        path_to_start=[visited_places.pop()]
        for i in range(len(visited_places)-1):
            place=visited_places.pop()
            if place==start_v:
                break
            if self.is_next_to(place,path_to_start[len(path_to_start)-1]):
                path_to_start.append(place)
        path_to_goal=[]
        for i in range(len(path_to_start)):
            path_to_goal.append(path_to_start.pop())
        self.floormap = backup
        return path_to_goal
