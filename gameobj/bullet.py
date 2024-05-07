

import math
import time
from gameobj.gameobject import BaseDameEffect, BaseGameObject, DestroyedBulletEffect, Effect, ThroughBulletEffect
from gameobj.screen import SCREEM
from gameobj.sprite import Sprite
from resource.resource import RES_BULLET


class Bullet(BaseGameObject):
    
    def __init__(self,producer:BaseGameObject,*args,**kwargs) -> None:
        super().__init__(*args,**kwargs)

        self.is_stoped = False
        self.vector_AB = (self.x_taget-self.x, self.y_taget-self.y)
        self.length_AB = math.sqrt(self.vector_AB[0] ** 2 + self.vector_AB[1] ** 2)
        self.producer = producer
        self.effects:list[Effect] = [BaseDameEffect(producer=self), ThroughBulletEffect(producer=self)]
        self.cache_obj:list[BaseGameObject] = []
        self.destroy_state_animation = None
        self.animation_angle = self.find_angle(taget=[self.x_taget,self.y_taget])
    def load_sprite(self):
        state = "creating"
        sprite = Sprite(RES_BULLET.sprite_bullet_02_fire)
        self.animations[state] = sprite
        self.state = state
        self.state_table[state] = "flying"
        state = "flying"
        sprite = Sprite(RES_BULLET.sprite_bullet_02_fly)
        self.animations[state] = sprite
        self.state = state
        self.state_table[state] = "destroying"
        state = "destroying"
        sprite = Sprite(RES_BULLET.sprite_bullet_02_explode)
        self.animations[state] = sprite
        self.state = state
        self.state_table[state] = "destroying"

        state = "destroying_before_through"
        sprite = Sprite(RES_BULLET.sprite_bullet_02_explode)
        self.animations[state] = sprite
        self.state = state
        self.state_table[state] = "flying"

        self.state = "creating"
    def destroy(self):
        self.destroy_time = time.time()
        self._is_destroying = True
        self.state = "destroying"
        
    def _update(self,contex:dict):
        if self.is_stoped:
            return
        if self._is_destroying:
            if self.animations[self.state].is_done:
                self._is_destroyed = True
            return
        
        for obj in self.all_obj(contex=contex):
            obj:BaseGameObject = obj
            if not obj.can_be_attacked:
                continue
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