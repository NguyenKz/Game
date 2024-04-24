import json
import pygame
import time

class SpriteImage:
    IMAGE_CACHE = {}
    def __init__(self) -> None:
        self.images = None
        self.time_frame = None
        self.is_reverse = None
    @staticmethod
    def factory(path:str,name:str):
        if SpriteImage.IMAGE_CACHE.get(f"{path}__{name}"):
            return SpriteImage.IMAGE_CACHE.get(f"{path}__{name}")
        sprite_img = SpriteImage()
        sprite_img.load(path,name)
        SpriteImage.IMAGE_CACHE[f"{path}__{name}"]=sprite_img
        return sprite_img
    
    def load(self,path:str,name:str):
        """Load sprite file

        Args:
            path (str): path of sprite file (json)
            name (str): name of sprite

        Raises:
            Exception: _description_
        """
        print(path,name)
        self.path = f"resource/sprite/{path}"
        with open(self.path,"r") as file:
            data = json.loads(file.read())
            sprite = None
            for item in data["sprites"]:
                if name == item["name"]:
                    sprite = item
                    break
            if sprite is None:
                raise Exception(f"Load sprite error: name [{name}] not found.")
            self.images:list[pygame.Surface] = []
            self.time = int(sprite["time"]*1000)
            self.is_reverse=sprite["is_reverse"]
            image = pygame.image.load(data["path"])
            for item in sprite["postion"]:
                start = item["start"]
                end = item["end"]
                width, height = end[0]-start[0], end[1]-start[1]
                x, y = start[0], start[1]
                cropped_image = pygame.Surface((width, height))
                cropped_image.blit(image, (0, 0), (x, y, width, height))
                cropped_image.convert()
                cropped_image.set_colorkey(image.get_at(sprite["background"]))
                self.images.append(cropped_image)
            self.time_frame = self.time//len(self.images)

class Sprite:

    def __init__(self) -> None:
        self.sprite_imgs = None
    def load(self,path:str,name:str):
        """Load sprite file

        Args:
            path (str): path of sprite file (json)
            name (str): name of sprite

        Raises:
            Exception: _description_
        """
        self.sprite_imgs = SpriteImage.factory(path=path,name=name)
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
        # pygame.draw.rect(screen,(0, 0, 255),new_rect,1)
