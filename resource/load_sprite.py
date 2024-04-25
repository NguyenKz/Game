import os
import json


sprite_clsss = """
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


"""
all_line = f"{sprite_clsss}\n"
for name in os.listdir("resource/sprite"):
    
    with open(f"resource/sprite/{name}","r") as file:

        data = json.loads(file.read())
        name_file_name = f"{name.split('.')[0]}".upper()
        sprite_data = ""
        for sprite in data["sprites"]:
            sprite_data+=f"""        self.sprite_{sprite["name"]} = SpriteImage(
                file_name = "{name}",
                name = "{sprite["name"]}",
                background={sprite["background"]}, 
                time = {sprite["time"]},
                is_reverse = {sprite["is_reverse"]},
                position = {sprite["position"]}
            )\n"""
        all_line += f"""
class __{name_file_name}:
    def __init__(self):
        self.json_file = "{name}"
{sprite_data}
RES_{name_file_name} = __{name_file_name}()
\n"""    
with open("resource/resource.py","w") as file:
    file.write(all_line)