#20K1113 小池優太郎

import pygame
pygame.init()

FONTNAME = "arias"
FONTSIZE = 20

class PygameBasicTools:
    def __init__(self,screen_w = 500, screen_h = 500, bg = (255,255,255)):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.screen = pygame.display.set_mode((screen_w,screen_h))
        self.bg = bg
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(FONTNAME, FONTSIZE)
        self.clear()

    def get_screen_size(self):
        return (self.screen_w,self.screen_h)

    def str2RGB(self,colorname):
        d = {"red":(255,0,0),
             "green":(0,255,0),
             "blue":(0,0,255),
             "yellow":(255,255,0),
             "black":(0,0,0),
             "white":(255,255,255),
             "lightgreen":(0,128,0),
             "grey":(128,128,128)}
        return d[colorname]

    def set_font(self,fontname,fontsize):
        self.font = pygame.font.SysFont(fontname, fontsize)

    def draw_line(self,x1,y1,x2,y2,color = (0,0,0)):
        if type(color)==type("string"):
            color = self.str2RGB(color)
        pygame.draw.line(self.screen,color,(x1,y1),(x2,y2))

    def draw_rect(self,x1,y1,x2,y2,color = (0,0,0)):
        w = abs(x2 - x1)
        h = abs(y1 - y2)
        if type(color)==type("string"):
            color = self.str2RGB(color)
        pygame.draw.rect(self.screen,color,(x1,y1,w,h))
        pygame.draw.rect(self.screen,(0,0,0),(x1,y1,w,h),1)

    def draw_ellipse(self,x1,y1,x2,y2,color = (0,0,0)):
        w = abs(x2 - x1)
        h = abs(y1 - y2)
        if type(color)==type("string"):
            color = self.str2RGB(color)
        pygame.draw.ellipse(self.screen,color,(x1,y1,w,h))

    def draw_polygon(self,pointlist,color = (0,0,0)):
        if type(color)==type("string"):
            color = self.str2RGB(color)
        pygame.draw.polygon(self.screen,color,pointlist)
        pygame.draw.polygon(self.screen,(0,0,0),pointlist,1)

    def draw_text(self,x,y,text,color="black",anchor="NW"):
        if type(color)==type("string"):
            color = self.str2RGB(color)
        text_pic=self.font.render(text,True,color)
        w,h=text_pic.get_size()
        pos_dict={"NW":(0,0),
                  "N":(w/2,0),
                  "NE":(w,0),
                  "W":(0,h/2),
                  "CENTER":(w/2,h/2),
                  "E":(w,h/2),
                  "SW":(0,h),
                  "S":(w/2,h),
                  "SE":(w,h),}
        pos=pos_dict[anchor]
        self.screen.blit(text_pic,(x-pos[0],y-pos[1]))

    def clear(self):
        self.screen.fill(self.bg)

    def update(self):
        pygame.display.flip()

    def pushed_keys(self):
        result = []
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                key_name = pygame.key.name(event.key)
                result.append(key_name)
        return result

    def mouse_pos(self):
        return pygame.mouse.get_pos()

    def clicked_buttons(self):
        result=[]
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                result.append(event.button)
        return result

    def set_title(self,title):
        pygame.display.set_caption(title)

    def keys_and_mouse(self):
        keys = []
        mouse_buttons = []
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                key_name = pygame.key.name(event.key)
                keys.append(key_name)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_buttons.append(event.button)
        return (keys,mouse_buttons)

    def sleep(self,n):
        self.clock.tick(n)

    def quit_check(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        return False

    def end(self):
        pygame.display.quit()
        pygame.quit()
