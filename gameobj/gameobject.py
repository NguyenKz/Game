import math
import random
import time
import pygame
from resource.resource import *
from gameobj.sprite import Sprite
from gameobj.screen import SCREEM
class BaseGameObject:
    def __init__(self,width:int,
                 height:int,
                 x:int,
                 y:int,
                 x_taget:int = 0,
                 y_taget:int = 0,
                 dame:float = 0,
                 speed:float = 0,
                 max_HP:int = 0,
                 fire_rate: float = 0,
                 critical_chance:float = 0,
                 critical_dame:float = 0,
                 armor:float = 0
        ) -> None:
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.animations = {}
        self.state = None
        self.last_time = 0
        self.time_diff = 0
        self.animation_angle = 0
        self.x_taget = x_taget
        self.y_taget = y_taget
        self.dame = dame
        self.max_HP = max_HP
        self.hp = max_HP
        self.speed = speed
        self.fire_rate = fire_rate
        self.critical_chance = critical_chance
        self.critical_dame = critical_dame
        self.armor = armor
        self.effects = []
        self._is_destroyed = False
        self.load_sprite()  


    def get_dame(self)->float:
        return self.dame
    
    def attacked(self,dame:float):
        self.hp-=dame+self.armor

    @property    
    def is_destroyed(self)->bool:
        raise Exception("Impletment is_destroyed function")
    
    @staticmethod
    def collision(object_1,object_2)->bool:
        rect1 = [object_1.x,object_1.y,object_1.x+object_1.width,object_1.y+object_1.height]
        rect2 = [object_2.x,object_2.y,object_2.x+object_2.width,object_2.y+object_2.height]
        if rect1[0] > rect2[2] or rect2[0] > rect1[2]:
            return False

        if rect1[1] > rect2[3] or rect2[1] > rect1[3]:
            return False

        return True
            
   
    def load_sprite(self):
        raise Exception("Impletment _load_sprite function")
    
    def all_obj(self,contex:dict):
        for key in contex["all_objs"]:
            for obj in contex["all_objs"][key]:
                if math.sqrt((self.x-obj.x)**2 +(self.y-obj.y)**2)<200:
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
        font = pygame.font.Font('freesansbold.ttf', 20)
        green = (0, 255, 0)
        text = font.render(f'HP: {self.hp}', True, green, None)
        textRect = text.get_rect()
        textRect.center = (self.x, self.y )
        screen.blit(text, textRect)
        pygame.draw.rect(surface=screen,color=green,rect=[self.x,self.y,self.width,self.height],width=1)

class Effect:
    def __init__(self,producer:BaseGameObject) -> None:
        self.producer:BaseGameObject = producer

    def do_effect(self,taget:BaseGameObject):
        raise Exception("Implement do_effect")

class BaseDameEffect(Effect):
    def do_effect(self,taget:BaseGameObject):
        dame = self.producer.get_dame()
        taget.attacked(dame=dame)

class DestroyedBulletEffect(Effect):
    def do_effect(self, taget: BaseGameObject):
        self.producer._is_destroyed = True

class Bullet(BaseGameObject):
    
    def __init__(self,producer:BaseGameObject,*args,**kwargs) -> None:
        super().__init__(*args,**kwargs)

        self.is_stoped = False
        self.vector_AB = (self.x_taget-self.x, self.y_taget-self.y)
        self.length_AB = math.sqrt(self.vector_AB[0] ** 2 + self.vector_AB[1] ** 2)
        self.producer = producer
        self.effects:list[Effect] = [BaseDameEffect(producer=self), DestroyedBulletEffect(producer=self)]
        self.cache_obj:list[BaseGameObject] = []

    def load_sprite(self):
        state = "normal"
        sprite = Sprite(RES_BULLET.sprite_bullet_01)
        self.animations[state] = sprite
        self.state = state


    def _update(self,contex:dict):
        if self.is_stoped:
            return
        
        for obj in self.all_obj(contex=contex):
            obj:BaseGameObject = obj
            if obj == self.producer or obj == self:
                continue
            if BaseGameObject.collision(object_1=obj,object_2=self):
                if obj not in self.cache_obj:
                    self.cache_obj.append(obj)
                    for effect in self.effects:
                        effect.do_effect(taget=obj)
            elif obj in self.cache_obj:
                self.cache_obj.remove(obj)
                

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

    def find_angle(self,taget:list[int]):
        p1 = [self.x,0]
        p2 = [self.x,self.y]
        p3 = taget
        v1 = (p1[0] - p2[0], p1[1] - p2[1])
        v2 = (p3[0] - p2[0], p3[1] - p2[1])
        angle_rad = math.atan2(v1[1], v1[0]) - math.atan2(v2[1], v2[0])
        angle_deg = math.degrees(angle_rad)

        return angle_deg
    
    @property
    def is_destroyed(self):
        if self.hp<=0:
            return True
        self._is_destroyed = True

class Char001(CharBase):

    def load_sprite(self):
        state = "normal"
        sprite = Sprite(RES_HERO.sprite_hero_01)
        self.animations[state] = sprite
        self.state = state

    
    def _update(self, contex:dict):
        events = contex["events"]
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                self.animation_angle = self.find_angle(taget=event.pos)
                break
    



class Mob001(CharBase):

    def __init__(self, *args,**kwargs) -> None:
        super().__init__(*args,**kwargs)
        self.is_stoped = False
        self.x_taget = SCREEM.get_width()//2
        self.y_taget = SCREEM.get_height()//2
        self.vector_AB = (self.x_taget-self.x, self.y_taget-self.y)
        self.length_AB = math.sqrt(self.vector_AB[0] ** 2 + self.vector_AB[1] ** 2)

    def load_sprite(self):
        state = "LEFT"
        sprite = Sprite(RES_MOB.sprite_mob_01_left)
        self.animations[state] = sprite
        self.state = state

        state = "RIGHT"
        sprite = Sprite(RES_MOB.sprite_mob_01_right)
        self.animations[state] = sprite
        self.state = state

        state = "UP"
        sprite = Sprite(RES_MOB.sprite_mob_01_up)
        self.animations[state] = sprite
        self.state = state

        state = "DOWN"
        sprite = Sprite(RES_MOB.sprite_mob_01_down)
        self.animations[state] = sprite
        self.state = state

    def _update(self, contex:dict):

        s = self.speed*self.time_diff
        k = s/self.length_AB
        new_x = self.vector_AB[0]*k
        new_y = self.vector_AB[1]*k
        if abs(new_x)>abs(new_y):
            if self.x>self.x_taget:
                self.state = "LEFT"
            else:
                self.state = "RIGHT"
        else:
            if self.y<self.y_taget:
                self.state = "DOWN"
            else:
                self.state = "UP"

        self.x += new_x
        self.y += new_y



