#Auther: https://github.com/yt-koike/
#Title: 高層迷宮(Skyscraper the labyrinth)

from dataclasses import dataclass, field
from pygame_lib import PygameBasicTools
from maze import Maze

WINDOW_W=500
WINDOW_H=500
LETTER_FONT=("arias",15)

SPACE=0
WALL=1
VISITED=5
START=8
GOAL=9

@dataclass
class Player:
    pos: tuple=field(init=False, default=None)
    direction: str
    maze: Maze

    def get_pos(self):
        return self.pos

    def get_dir(self):
        return self.direction
    
    def set_pos(self, i, j):
        self.pos = (i, j)

    def forward(self):
        d={'N':(-1,0),'E':(0,1),'S':(1,0),'W':(0,-1)}
        player_move=d[self.direction]
        new_i=self.pos[0]+player_move[0]
        new_j=self.pos[1]+player_move[1]
        if self.maze.floormap[new_i][new_j]!=WALL:
            self.set_pos(new_i,new_j)
            return 0
        return -1

    def back(self):
        d={'N':(-1,0),'E':(0,1),'S':(1,0),'W':(0,-1)}
        player_move=d[self.direction]
        new_i=self.pos[0]-player_move[0]
        new_j=self.pos[1]-player_move[1]
        if self.maze.floormap[new_i][new_j]!=WALL:
            self.set_pos(new_i,new_j)
            return 0
        return -1

    def left(self):
        d=['N','W','S','E','N']
        self.direction=d[d.index(self.direction)+1]

    def right(self):
        d=['N','E','S','W','N']
        self.direction=d[d.index(self.direction)+1]

    def get_perspective(self):
        pos=self.get_pos()
        direc=self.get_dir()
        floormap=self.maze.floormap
        start_p={'N':(0,-1),'E':(-1,0),'S':(0,1),'W':(1,0)}
        start_i=pos[0]+start_p[direc][0]
        start_j=pos[1]+start_p[direc][1]
        if direc=='N':
            result=[]
            for a in range(4):
                row=[]
                for b in range(3):
                    row.append(floormap[start_i-a][start_j+b])
                result.append(row)
                if start_i-a<0:
                    break
        elif direc=='E':
            result=[]
            for a in range(4):
                row=[]
                for b in range(3):
                    if start_i+b>len(floormap)-1:
                        break
                    if start_j+a>len(floormap[0])-1:
                        row=[1,1,1]
                        break
                    row.append(floormap[start_i+b][start_j+a])
                if len(row)>0:
                    result.append(row)
        elif direc=='S':
            result=[]
            for a in range(4):
                row=[]
                for b in range(3):
                    if start_i+a>=len(floormap)-1:
                        row=[1,1,1]
                        break
                    row.append(floormap[start_i+a][start_j-b])
                result.append(row)
        elif direc=='W':
            result=[]
            for a in range(4):
                row=[]
                for b in range(3):
                    row.append(floormap[start_i-b][start_j-a])
                result.append(row)
                if start_i-a<0:
                    break
        result.reverse()
        return result

class View2d:
    def __init__(self,pbt,game):
        self.pbt = pbt
        self.game = game
        self.origin_x=100
        self.origin_y=100
        self.block_w=50
        self.block_h=50
    
    def draw_floormap(self):
        origin_x = self.origin_x
        origin_y = self.origin_y
        block_w = self.block_w
        block_h = self.block_h
        y=origin_y
        for row in self.game.maze.floormap:
            x=origin_x
            for block in row:
                if block!=SPACE and block!=VISITED:
                    cs={WALL:"blue", START:"lightgreen", GOAL:"red"}
                    self.pbt.draw_rect(x,y,
                                       x+self.block_w,y+self.block_h,
                                       cs[block])
                x += block_w
            y += block_h
            
    def camera_adjust(self):
        origin_x = self.origin_x
        origin_y = self.origin_y
        block_w = self.block_w
        block_h = self.block_h
        x=self.game.player.get_pos()[1]*block_w+origin_x
        y=self.game.player.get_pos()[0]*block_h+origin_y
        if x < block_w*2:
            self.origin_x -= x-block_w*2
        elif x > WINDOW_W-block_w*2:
            self.origin_x -= x-(WINDOW_W-block_w*2)
        if y < block_h*2:
            self.origin_y -= y-block_h*2
        elif y >= WINDOW_H-block_h*2:
            self.origin_y -= y-(WINDOW_H-block_h*2)
    
    def draw_player(self):
        origin_x = self.origin_x
        origin_y = self.origin_y
        block_w = self.block_w
        block_h = self.block_h
        x=self.game.player.get_pos()[1]*block_w+origin_x
        y=self.game.player.get_pos()[0]*block_h+origin_y
        arrows={"N":[(x+block_w/2,y),(x,y+block_h),(x+block_w,y+block_h)],
                "E":[(x+block_w,y+block_h/2),(x,y),(x,y+block_h)],
                "S":[(x+block_w/2,y+block_h),(x,y),(x+block_w,y)],
                "W":[(x,y+block_h/2),(x+block_w,y),(x+block_w,y+block_h)]}
        self.pbt.draw_polygon(arrows[self.game.player.direction])

    def draw(self):
            self.camera_adjust()
            self.draw_floormap()
            self.draw_player()

class View3d:
    def __init__(self,pbt,game):
        self.pbt = pbt
        self.game = game
        self.sizes = [70,90,120,160]
        self.guide_enable = False


    def draw_wall(self,x,y,l_length,r_length,width,c="blue"):
        if l_length<r_length:
            y+=(r_length-l_length)/2
        self.pbt.draw_polygon([(x,y),
                              (x+width,y+(l_length-r_length)/2),
                              (x+width,y+(l_length+r_length)/2),
                              (x,y+l_length)],
                              c)

    def draw_row(self,cx,cy,size,wall_row_list):
        wall_w=size
        wall_h=size
        sidewall_w=size/8
        sidewall_h=size*3/4
        self.pbt.draw_line(cx-3*wall_w/2,cy+wall_h/2,cx+3*wall_w/2,cy+wall_h/2)
        self.pbt.draw_line(cx-3*wall_w/2,cy+wall_h/2,cx-wall_w*9/8,cy+size*3/8)
        self.pbt.draw_line(cx+3*wall_w/2,cy+wall_h/2,cx+wall_w*9/8,cy+size*3/8)
        self.pbt.draw_line(cx-wall_w/2,cy+wall_h/2,cx-wall_w*3/8,cy+size*3/8)
        self.pbt.draw_line(cx+wall_w/2,cy+wall_h/2,cx+wall_w*3/8,cy+size*3/8)
        if wall_row_list[0]==WALL:
            self.draw_wall(cx-3*wall_w/2,cy-wall_h/2,wall_h,wall_h,wall_w)
            self.draw_wall(cx-wall_w/2,cy-wall_h/2,wall_h,sidewall_h,sidewall_w)
        if wall_row_list[2]==WALL:
            self.draw_wall(cx+wall_w/2,cy-wall_h/2,wall_h,wall_h,wall_w)
            self.draw_wall(cx+wall_w/2-sidewall_w,cy-wall_h/2,
                           sidewall_h,wall_h,sidewall_w)
        if wall_row_list[1]==WALL:
            self.draw_wall(cx-wall_w/2,cy-wall_h/2,wall_h,wall_h,wall_w)
        message=""
        if wall_row_list[1]==GOAL:
            message="goal"
        if wall_row_list[1]==START:
            message="start"            
        if message!="":
            sc_w,sc_h = self.pbt.get_screen_size()
            self.pbt.draw_rect(cx-wall_w/4,cy-wall_h/8,
                               cx+wall_w/4,cy+wall_h/8,"white")
            self.pbt.draw_text(cx,cy,message,anchor="CENTER")
            self.pbt.update()

    def draw_walls(self,center_x,center_y,wall_list):
        if(len(wall_list)>len(self.sizes)):
            raise Exception("wall_list has invalid row number.")
        while len(wall_list)<4:
            wall_list.insert(0,[WALL,WALL,WALL])
        for i in range(len(self.sizes)-len(wall_list)-1,len(wall_list)):
            self.draw_row(center_x,center_y,self.sizes[i],wall_list[i])

    def draw_arrow(self,cx,cy,size,direction):
        if direction == "UP":
            self.pbt.draw_polygon([(cx,cy+size*3/4),
                                  (cx-size,cy+size*9/8),
                                  (cx+size,cy+size*9/8)],
                                  "red")
        elif direction == "DOWN":
            self.pbt.draw_polygon([(cx,cy+size*9/8),
                                  (cx-size,cy+size*3/4),
                                  (cx+size,cy+size*3/4)],
                                  "red")
        elif direction == "LEFT":
            self.pbt.draw_polygon([(cx-size,cy+size),
                                  (cx+size,cy+size*7/8),
                                  (cx+size,cy+size*9/8)],
                                  "red")
        elif direction == "RIGHT":
            self.pbt.draw_polygon([(cx+size,cy+size),
                                  (cx-size,cy+size*7/8),
                                  (cx-size,cy+size*9/8)],
                                  "red")

    def draw_guide(self,center_x,center_y):
        path_to_goal=self.game.maze.path_search(self.game.player.get_pos())
        if len(path_to_goal)>0:
            v1=self.game.player.get_pos()
            v2=path_to_goal[0]
            dv=(v2[0]-v1[0],v2[1]-v1[1])
            directions={(-1,0):"N",(0,1):"E",(1,0):"S",(0,-1):"W"}        
            relative_d=self.relative_direction(directions[dv])
            self.draw_arrow(center_x,center_y,self.sizes[0],relative_d)

    def draw(self):
        player = self.game.player
        wall_list=player.get_perspective()
        sc_w,sc_h = self.pbt.get_screen_size()
        self.draw_walls(sc_w/2,sc_h/2,wall_list)
        if self.guide_enable:
            self.draw_guide(sc_w/2,sc_h/2)

    def enable_guide(self):
        self.guide_enable = True

    def disable_guide(self):
        self.guide_enable = False

    def toggle_guide(self):
        if self.guide_enable:
            self.disable_guide()
        else:
            self.enable_guide()

    def relative_direction(self,direction):
        player_d=self.game.player.get_dir()
        direcs=["N","W","S","E"]
        d=(direcs.index(player_d)-direcs.index(direction))%4
        UDLR=["UP","RIGHT","DOWN","LEFT"]
        return UDLR[d]

@dataclass
class MazeGame:
    def __init__(self,pbt):
        self.pbt = pbt
        self.pbt.set_title("main")
        self.floor = 1
        self.view2d = View2d(pbt,self)
        self.view3d = View3d(pbt,self)
        self.viewmode='3D'
        self.maze=Maze()
        levels ={"easy":(10,10,10),
                 "normal":(20,20,20),
                 "hard":(30,30,30),
                 "veryhard":(40,40,100)}
        level = self.user_select("Level = ",list(levels.keys()))
        self.maze_w,self.maze_h,self.goal_floor = levels[level]
        self.set_newmaze()
        self.mainloop()

    def set_newmaze(self):
        self.maze.create_maze(self.maze_w,self.maze_h)
        self.player=Player('S',self.maze)
        start_pos = self.maze.search(START)
        self.player.set_pos(start_pos[0],start_pos[1])
        self.redraw()

    def mainloop(self):
        while True:
            keys = self.pbt.pushed_keys()
            if "up" in keys:
                if self.player.forward() == 0:
                    self.redraw()            
            elif "down" in keys:
                if self.player.back() == 0:
                    self.redraw()
            elif "left" in keys:
                self.player.left()
                self.redraw()
            elif "right" in keys:
                self.player.right()
                self.redraw()
            elif "t" in keys:
                self.toggle_viewmode()
                self.redraw()
            elif "g" in keys:
                self.view3d.toggle_guide()
                self.redraw()
            elif "q" in keys:
                break
            elif "c" in keys:
                self.show_credit()
                self.redraw()
            if self.pbt.quit_check():
                break
            if self.check_goal():
                if self.floor == self.goal_floor:
                    sc_w,sc_h = self.pbt.get_screen_size()
                    self.pbt.draw_rect(sc_w/2-100,230,sc_w/2+100,280,"white")
                    self.pbt.draw_text(sc_w/2,sc_h/2,"Congratulations!",
                               "red","CENTER")
                    self.pbt.draw_text(sc_w/2,sc_h/2+20,
                               "Press q to exit",anchor="CENTER")
                    self.pbt.update()
                    while True:
                        keys = self.pbt.pushed_keys()
                        if "q" in keys:
                            self.pbt.end()
                            sys.exit(0)
                            break
                else:
                    while True:
                        keys = self.pbt.pushed_keys()
                        if "return" in keys:
                            self.floor += 1
                            self.set_newmaze()
                            self.redraw()
                            break
            self.pbt.sleep(10)
        self.pbt.end()

    def user_select(self,prompt,options):
        i = 0
        sc_w,sc_h = self.pbt.get_screen_size()       
        while True:
            keys = self.pbt.pushed_keys()
            if "up" in keys:
                if i>0:
                    i-=1
            elif "down" in keys:
                if i<len(options)-1:
                    i+=1
            elif "return" in keys:
                return options[i]
            self.pbt.draw_rect(sc_w/2-100,100,sc_w/2+100,120,"white")
            self.pbt.draw_text(sc_w/2,110,
                               f"{prompt}{options[i]} ({str(i+1)}/{len(options)})",
                               anchor="CENTER")
            self.pbt.update()
            self.pbt.sleep(10)

    def check_goal(self):
        p_pos=self.player.get_pos()
        if self.maze.floormap[p_pos[0]][p_pos[1]]==GOAL:
            sc_w,sc_h = self.pbt.get_screen_size()
            self.pbt.draw_rect(sc_w/2-100,230,sc_w/2+100,280,"white")
            self.pbt.draw_text(sc_w/2,sc_h/2,str(self.floor)+"F Cleared!",
                               "red","CENTER")
            self.pbt.draw_text(sc_w/2,sc_h/2+20,
                               "Press Enter to go up",anchor="CENTER")
            self.pbt.update()
            return True
        return False

    def show_help(self):
        sc_w,sc_h = self.pbt.get_screen_size()
        self.pbt.draw_rect(sc_w/2-100,40,sc_w/2+100,80,"white")
        self.pbt.draw_text(sc_w/2,55,"T=toggle viewmode, g=guide",anchor="CENTER")
        self.pbt.draw_text(sc_w/2,65,"Q=quit",anchor="CENTER")

    def show_credit(self):
        sc_w,sc_h = self.pbt.get_screen_size()
        self.pbt.draw_rect(sc_w/2-100,sc_h/2-20,sc_w/2+100,sc_h/2+20,"white")
        self.pbt.draw_text(sc_w/2,sc_h/2-10,"created by 20K1113",anchor="CENTER")
        self.pbt.draw_text(sc_w/2,sc_h/2+10,"R=resume",anchor="CENTER")
        self.pbt.update()
        input_word = ""
        keyword = "20k1113"
        while True:
            keys = self.pbt.pushed_keys()
            if "r" in keys:
                break
            if len(input_word)>len(keyword):
                input_word = ""
            if len(keys)>0:
                input_word += keys[0]
            if input_word == keyword:
                print("You found this Easter egg! You're awesome!")
                self.pbt.draw_rect(sc_w/2-100,sc_h/2-20,sc_w/2+100,sc_h/2+20,"white")
                self.pbt.draw_text(sc_w/2,sc_h/2-10,"created by Koike Yutaro",anchor="CENTER")
                self.pbt.draw_text(sc_w/2,sc_h/2+10,"R=resume",anchor="CENTER")
                self.pbt.update()
                input_word = ""

    def show_floor(self):
        self.pbt.draw_rect(0,40,100,80,"white")
        self.pbt.draw_text(50,60,f"{str(self.floor)}F/{str(self.goal_floor)}F",
                           anchor="CENTER")

    def redraw(self):
        self.pbt.clear()
        if self.viewmode=='2D':
            self.view2d.draw()
        elif self.viewmode=='3D':
            self.view3d.draw()
        self.show_help()
        self.show_floor()
        self.pbt.update()

    def toggle_viewmode(self):
        if self.viewmode=='2D':
            self.viewmode='3D'
        else:
            self.viewmode='2D'
        self.redraw()

pbt = PygameBasicTools(500,500)
game = MazeGame(pbt)
