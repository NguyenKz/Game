
import json
import pygame
from gameobj.screen import *
class SpriteImage:
    def __init__(self,file_name:str,name:str,background:list[int],time:float,is_reverse:bool,position:list[dict]):
        self.name = name
        self.file_name = file_name
        self.background = background
        self.time = time
        self.is_reverse = is_reverse
        self.position = position
        self.images = []
        self.__load()
    
    def __load(self):
        print(self.file_name,self.name)
        self.path = f"resource/sprite/{self.file_name}"
        with open(self.path,"r") as file:
            data = json.loads(file.read())
            sprite = None
            for item in data["sprites"]:
                if self.name == item["name"]:
                    sprite = item
                    break
            if sprite is None:
                raise Exception(f"Load sprite error: name [{self.file_name}] not found.")
            self.images:list[pygame.Surface] = []
            self.time = int(sprite["time"]*1000)
            self.is_reverse=sprite["is_reverse"]
            image = pygame.image.load(data["path"])
            for item in sprite["position"]:
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




class __BULLET:
    def __init__(self):
        self.json_file = "bullet.json"
        self.sprite_bullet_01 = SpriteImage(
                file_name = "bullet.json",
                name = "bullet_01",
                background=[0, 0], 
                time = 0.1,
                is_reverse = True,
                position = [{'start': [5, 296], 'end': [45, 336]}, {'start': [53, 296], 'end': [93, 336]}, {'start': [101, 296], 'end': [141, 336]}, {'start': [149, 296], 'end': [189, 336]}, {'start': [197, 296], 'end': [237, 336]}]
            )

RES_BULLET = __BULLET()


class __HERO:
    def __init__(self):
        self.json_file = "hero.json"
        self.sprite_hero_01 = SpriteImage(
                file_name = "hero.json",
                name = "hero_01",
                background=[150, 480], 
                time = 0.1,
                is_reverse = False,
                position = [{'start': [172, 80], 'end': [376, 284]}]
            )

RES_HERO = __HERO()


class __MOB:
    def __init__(self):
        self.json_file = "mob.json"
        self.sprite_mob_01_down = SpriteImage(
                file_name = "mob.json",
                name = "mob_01_down",
                background=[0, 0], 
                time = 0.5,
                is_reverse = True,
                position = [{'start': [2, 0], 'end': [28, 32]}, {'start': [34, 0], 'end': [62, 32]}, {'start': [66, 0], 'end': [93, 32]}]
            )
        self.sprite_mob_01_left = SpriteImage(
                file_name = "mob.json",
                name = "mob_01_left",
                background=[0, 0], 
                time = 0.5,
                is_reverse = True,
                position = [{'start': [2, 32], 'end': [28, 64]}, {'start': [34, 32], 'end': [62, 64]}, {'start': [66, 32], 'end': [93, 64]}]
            )
        self.sprite_mob_01_right = SpriteImage(
                file_name = "mob.json",
                name = "mob_01_right",
                background=[0, 0], 
                time = 0.5,
                is_reverse = True,
                position = [{'start': [2, 64], 'end': [28, 96]}, {'start': [34, 64], 'end': [62, 96]}, {'start': [66, 64], 'end': [93, 96]}]
            )
        self.sprite_mob_01_up = SpriteImage(
                file_name = "mob.json",
                name = "mob_01_up",
                background=[0, 0], 
                time = 0.5,
                is_reverse = True,
                position = [{'start': [2, 96], 'end': [28, 128]}, {'start': [34, 96], 'end': [62, 128]}, {'start': [66, 96], 'end': [93, 128]}]
            )

RES_MOB = __MOB()

