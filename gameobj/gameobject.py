import math
import time
import pygame
from resource.resource import *
from gameobj.sprite import Sprite
from gameobj.screen import SCREEM
class BaseGameObject:
        
    def __init__(self,width:int,height:int,x:int,y:int) -> None:
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.animations = {}
        self.state = None
        self.last_time = 0
        self.time_diff = 0
        self.animation_angle = 0

    @property    
    def is_destroyed(self)->bool:
        raise Exception("Impletment is_destroyed function")
    
    @staticmethod
    def collision(object_1,object_2)->bool:
        retVal = BaseGameObject.__collision(point=[object_1.x,object_1.y],object_other=object_2)
        if retVal:
            return True
        retVal = BaseGameObject.__collision(point=[object_1.x+object_1.width,object_1.y],object_other=object_2)
        if retVal:
            return True
        retVal = BaseGameObject.__collision(point=[object_1.x+object_1.width,object_1.y+object_1.height],object_other=object_2)
        if retVal:
            return True
        retVal = BaseGameObject.__collision(point=[object_1.x,object_1.y+object_1.height],object_other=object_2)
        if retVal:
            return True
        return False
    
    @staticmethod
    def __collision(point,object_other)->bool:
        x = point[0]
        y = point[1]
        return not (x<=object_other.x or x>=object_other.x+object_other.width or y<=object_other.y or y>=object_other.y+object_other.height)
    def load_sprite(self):
        raise Exception("Impletment _load_sprite function")
    
    def all_obj(self,contex:dict):
        objs = contex["all_objs"]
        keys = list(objs.keys())
        keys.sort(reverse=True)
        for key in keys:
            for obj in objs[key]:
                yield obj

    def update(self,contex:dict):
        if self.last_time<=0:
            self.last_time = time.time()
        self.time_diff = time.time()-self.last_time         
        self._update(contex)
        self.last_time = time.time()
    
    def _update(self,contex:dict):
        raise Exception("Impletment _update function")
    
    def render(self,screen:pygame.Surface):

        animation:Sprite = self.animations.get(self.state)
        if animation is None:
            return
        animation.render(screen=screen,x = self.x,y=self.y,width=self.width,height=self.height,d=self.animation_angle)    

class Bullet(BaseGameObject):

    def __init__(self, width: int, height: int, x: int, y: int,x_taget:int,y_taget:int,dame:float,speed:float) -> None:
        super().__init__(width, height, x, y)
        self.x_taget = x_taget
        self.y_taget = y_taget
        self.dame = dame
        self.speed = speed
        self.load_sprite()  
        self.is_stoped = False
        self.vector_AB = (x_taget-x, y_taget-y)
        self.length_AB = math.sqrt(self.vector_AB[0] ** 2 + self.vector_AB[1] ** 2)
        self._is_destroyed = False

    def load_sprite(self):
        file_name = FILE_BULLET
        name = NAME_BULLET_BULLET_01
        state = "normal"
        sprite = Sprite()
        sprite.load(path=file_name,name=name)
        self.animations[state] = sprite
        self.state = state


    def _update(self,contex:dict):
        if self.is_stoped:
            return
        s = self.speed*self.time_diff
        k = s/self.length_AB
        self.x = self.x+self.vector_AB[0]*k
        self.y = self.y+self.vector_AB[1]*k


    @property    
    def is_destroyed(self)->bool:
        if self._is_destroyed:
            return True
        if self.x>SCREEM.get_width() or self.x<=-100 or self.y>SCREEM.get_height() or self.y<=-100:
            return True
        return False
    
class CharBase(BaseGameObject):

    def __init__(self, width: int, height: int, x: int, y: int,max_HP,dame:int,fire_rate:float) -> None:
        super().__init__(width, height, x, y)
        self.max_HP = max_HP
        self.current_HP = max_HP
        self.dame = dame
        self.fire_rate = fire_rate
        self.effects = []

    def find_angle(self,taget:list[int]):
        p1 = [self.x,0]
        p2 = [self.x,self.y]
        p3 = taget
        v1 = (p1[0] - p2[0], p1[1] - p2[1])
        v2 = (p3[0] - p2[0], p3[1] - p2[1])
        angle_rad = math.atan2(v1[1], v1[0]) - math.atan2(v2[1], v2[0])
        angle_deg = math.degrees(angle_rad)

        return angle_deg
    
    def do_effect(self,other):
        pass

    def attacked(self,attacker):
        for effect in attacker.effects:
            effect.do_effect(self)
    
class Char001(CharBase):

    def __init__(self, width: int, height: int, x: int, y: int, max_HP, dame: int, fire_rate: float) -> None:
        super().__init__(width, height, x, y, max_HP, dame, fire_rate)

    def load_sprite(self):
        file_name = FILE_HERO
        name = NAME_HERO_HERO_001
        state = "normal"
        sprite = Sprite()
        sprite.load(path=file_name,name=name)
        self.animations[state] = sprite
        self.state = state

    
    def _update(self, contex:dict):
        events = contex["events"]
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                self.animation_angle = self.find_angle(taget=event.pos)
                break
    

    @property    
    def is_destroyed(self)->bool:
        return False


class Mob001(CharBase):


    def load_sprite(self):
        file_name = FILE_MOB

        name = NAME_MOB_MOB_01_LEFT
        state = "LEFT"
        sprite = Sprite()
        sprite.load(path=file_name,name=name)
        self.animations[state] = sprite
        self.state = state

        name = NAME_MOB_MOB_01_RIGHT
        state = "RIGHT"
        sprite = Sprite()
        sprite.load(path=file_name,name=name)
        self.animations[state] = sprite
        self.state = state

        name = NAME_MOB_MOB_01_UP
        state = "UP"
        sprite = Sprite()
        sprite.load(path=file_name,name=name)
        self.animations[state] = sprite
        self.state = state

        name = NAME_MOB_MOB_01_DOWN
        state = "DOWN"
        sprite = Sprite()
        sprite.load(path=file_name,name=name)
        self.animations[state] = sprite
        self.state = state

    def _update(self, contex:dict):
        my_char:Char001 = None
        for obj in self.all_obj(contex=contex):
            if isinstance(obj,Char001):
                my_char = obj
                break
        if not my_char:
            return
        de = self.find_angle(taget=[my_char.x,my_char.y])
        self.animation_angle=180+de

    @property    
    def is_destroyed(self)->bool:
        return False

