import pygame
import time
from resource.resource import SpriteImage
from gameobj.screen import SCREEM_WIDTH,SCREEM_HEIGHT
class Sprite:
    CHACHE_IMG = {}
    def __init__(self,sprite_images:SpriteImage) -> None:
        self.sprite_imgs = sprite_images
        self.is_up = True
        self.start_time = 0
        self.first_time_render = 0
        self._is_done = False
        self.cache = {}
    @property
    def is_done(self):
        if self.sprite_imgs.is_repeat:
            return False
        return self._is_done
    
    def reset(self):
        self.is_up = True
        self.start_time = 0
        self.first_time_render = 0
        self._is_done = False
        print("-------------------------------")
        
    def render(self,screen:pygame.Surface,x:int,y:int,width:int,height:int,d:float=0):
        if self.first_time_render==0:
            self.first_time_render = time.time()
        x = int(x)
        y = int(y)
        width = int(width)
        height = int(height)
        if x>SCREEM_WIDTH+300 or x<-300 or y>SCREEM_HEIGHT+300 or y<=-300:
            return
        if self.start_time==0:
            self.start_time = time.time()
        time_d = int((time.time()-self.start_time)*1000)
        index = (time_d%self.sprite_imgs.time)//self.sprite_imgs.time_frame
        if time_d>self.sprite_imgs.time:
            self.start_time = time.time()
            if self.sprite_imgs.is_reverse:
                self.is_up = not self.is_up
        if index>=len(self.sprite_imgs.images)-1:
            if self.sprite_imgs.is_repeat==False:
                self._is_done = True
        if index>=len(self.sprite_imgs.images):
            index = len(self.sprite_imgs.images)-1
            

        if self.sprite_imgs.is_reverse and not self.is_up:
            index = len(self.sprite_imgs.images)-index-1
        if index<0:
            index = 0
        
        cache_key = f"{self.sprite_imgs.id}_{index}_{width}_{height}_{int(d)}"
        # print(cache_key)
        if not Sprite.CHACHE_IMG.get(cache_key):
            img = pygame.transform.scale(self.sprite_imgs.images[index],size=(width,height))
            img = pygame.transform.rotate(surface=img,angle=d)
            Sprite.CHACHE_IMG[cache_key] = img

       
        img:pygame.Surface=  Sprite.CHACHE_IMG.get(cache_key)
        new_rect = img.get_rect(center = img.get_rect(topleft = (x,y)).center)
        x = x+width//2-new_rect.width//2
        y = y+height//2-new_rect.height//2
        new_rect.x=x
        new_rect.y=y
        screen.blit(img, new_rect)
