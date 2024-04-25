import pygame
import time
from resource.resource import SpriteImage
class Sprite:

    def __init__(self,sprite_images:SpriteImage) -> None:
        self.sprite_imgs = sprite_images
        self.is_up = True
        self.start_time = 0
        

    def render(self,screen:pygame.Surface,x:int,y:int,width:int,height:int,d:float=0):
        x = int(x)
        y = int(y)
        width = int(width)
        height = int(height)
        if x>screen.get_width() or x<-100 or y>screen.get_height() or y<=-100:
            return
        time_d = int((time.time()-self.start_time)*1000)
        index = (time_d%self.sprite_imgs.time)//self.sprite_imgs.time_frame
        if time_d>self.sprite_imgs.time:
            self.start_time = time.time()
            if self.sprite_imgs.is_reverse:
                self.is_up = not self.is_up

        if self.sprite_imgs.is_reverse and not self.is_up:
            index = len(self.sprite_imgs.images)-index-1
        if index<0:
            index = 0
        if index>=len(self.sprite_imgs.images):
            index = len(self.sprite_imgs.images)-1
            
        img = pygame.transform.scale(self.sprite_imgs.images[index],size=(width,height))
        img = pygame.transform.rotate(surface=img,angle=d)
        new_rect = img.get_rect(center = img.get_rect(topleft = (x,y)).center)
        x = x+width//2-new_rect.width//2
        y = y+height//2-new_rect.height//2
        new_rect.x=x
        new_rect.y=y
        screen.blit(img, new_rect)
