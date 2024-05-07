
import time
import pygame
import json

def get_org_postion(mouse,camera,zoom):
    mouse_relative_to_zoomed = (mouse[0] + camera[0], mouse[1] + camera[1])
    original_x = int(mouse_relative_to_zoomed[0] // zoom)
    original_y = int(mouse_relative_to_zoomed[1] // zoom)
    return [original_x,original_y]
def slope(x1, y1, x2, y2):
    return (y2 - y1) / (x2 - x1) if (x2 - x1) != 0 else None

def are_collinear(a,b,c):
    slope_AB = slope(a[0], a[1], b[0], b[1])
    slope_BC = slope(b[0], b[1], c[0], c[1])
    
    if slope_AB is None or slope_BC is None:
        return slope_AB == slope_BC
    return abs(slope_AB - slope_BC) < 1e-9

def find_intersection(line1, line2):
    x1, y1, x2, y2 = line1[0][0], line1[0][1],line1[1][0], line1[1][1]
    x3, y3, x4, y4 = line2[0][0], line2[0][1],line2[1][0], line2[1][1]
    
    if x2 - x1 == 0:
        m1 = None
        b1 = x1
    else:
        m1 = (y2 - y1) / (x2 - x1)
        b1 = y1 - m1 * x1
    
    if x4 - x3 == 0: 
        m2 = None
        b2 = x3
    else:
        m2 = (y4 - y3) / (x4 - x3)
        b2 = y3 - m2 * x3
    
    if m1 is None:
        x = b1
        y = m2 * x + b2
    elif m2 is None:
        x = b2
        y = m1 * x + b1
    else:
        x = (b2 - b1) / (m1 - m2)
        y = m1 * x + b1
    
    if (min(x1, x2) <= x <= max(x1, x2) and
        min(y1, y2) <= y <= max(y1, y2) and
        min(x3, x4) <= x <= max(x3, x4) and
        min(y3, y4) <= y <= max(y3, y4)):
        return [int(x), int(y)]
    return None

def find_all_intersections(horizontal_lines, vertical_lines):
    intersections = []
    for h_line in horizontal_lines:
        for v_line in vertical_lines:
            intersection = find_intersection(h_line, v_line)
            if intersection is not None:
                intersections.append(intersection)
    return intersections

def point_in_rectangle(point, rectangle):
    x, y = point[0],point[1]
    x1, y1, x2, y2 = rectangle[0][0],rectangle[0][1],rectangle[1][0],rectangle[1][1]
    
    if (min(x1, x2) <= x <= max(x1, x2) and
        min(y1, y2) <= y <= max(y1, y2)):
        return True
    else:
        return False
    

class TempSprite:

    def __init__(self) -> None:
        self.sprite_imgs:list[pygame.Surface] = []
        self.start_time = time.time()
        self.is_up = False
        self.is_reverse = False
        self.time = 1000
        self.time_frame = 1
    def add_img(self,boxs:list[list] ,image:pygame.Surface):
        if len(boxs)<=0:
            return
        self.sprite_imgs = []
        for box in boxs:
            width = box[1][0]-box[0][0]
            height = box[1][1]-box[0][1]
            x = box[0][0]
            y = box[0][1]
            cropped_image = pygame.Surface((width, height))
            cropped_image.blit(image, (0, 0), (x, y, width, height))
            cropped_image.convert()
            self.sprite_imgs.append(cropped_image)
        self.time_frame = self.time/len(self.sprite_imgs)
    
    def render(self,screen:pygame.Surface,start_x:int,start_y:int):
        if len(self.sprite_imgs)<=0:
            return
        time_d = int((time.time()-self.start_time)*1000)
        index = (time_d%self.time)//self.time_frame
        if time_d>self.time:
            self.start_time = time.time()
            if self.is_reverse:
                self.is_up = not self.is_up

        if self.is_reverse and not self.is_up:
            index = len(self.sprite_imgs)-index-1
        if index<0:
            index = 0
        if index>=len(self.sprite_imgs):
            index = len(self.sprite_imgs)-1
        index = int(index)
        y = start_y

        for img in self.sprite_imgs:
            pygame.draw.rect(screen,[0,255,0],[start_x-5,y-5,img.get_width()+10,img.get_height()+10],width=0)
            screen.blit(img,[start_x,y])
            y+=img.get_height()+10
        
        screen.blit(self.sprite_imgs[index],[start_x,y])


def add_line(all_line,point,image:pygame.Surface,type_line="x"):
    is_add = True
    for line in all_line:
        if are_collinear(point,line[0],line[1]):
            is_add = False
            break
    if is_add:
        if type_line == "x":
            all_line.append([
                [0,point[1]],
                [image.get_width(),point[1]],
            ])
        if type_line == "y":
            all_line.append([
                [point[0],0],
                [point[0],image.get_height()],
            ])
        return True
    return  False
    
def save(file_name,config_init:dict,list_box:list[list],all_data:dict):
    sprite = None
    for org_sprite in all_data.get("sprites",[]):
        if org_sprite["name"] ==config_init["name"]:
            sprite = org_sprite
            break
    if sprite is None:
        sprite = config_init.copy()
        all_data["sprites"] = all_data.get("sprites",[])
        all_data["sprites"].append(sprite)
        
    print(sprite)
    sprite["position"] = [{"start":box[0],"end":box[1]} for box in list_box]
    with open(f"resource/sprite/{file_name}.json","w")as file:
        file.write(json.dumps(all_data,indent=4))