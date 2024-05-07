import random
import time
from gameobj import Bullet,Mob001,Char001, SCREEM,CLOCK,CharEmpty,SCREEM_WIDTH,SCREEM_HEIGHT
import pygame

screen = SCREEM
clock = CLOCK
running = True

all_objs:dict = {
    "layer_001" : [],
    "layer_002" : [],
}

my_char = Char001(40,40,SCREEM_WIDTH//2-20,SCREEM_HEIGHT//2-20,max_HP=100,dame=100,fire_rate=1)
my_char.load_sprite()
all_objs["layer_001"].append(my_char)
char_empty = CharEmpty(80,80,SCREEM_WIDTH//2-40,SCREEM_HEIGHT//2-40,max_HP=1,dame=0,fire_rate=0)
char_empty.load_sprite()
all_objs["layer_001"].append(char_empty)

last_time = 0
last_time2 = 0
mouse = [0,0]

last = time.time()
fps = 0
while running:
    contex = {
        
        "events":[],
        "my_char":my_char
    }
    for event in pygame.event.get():
        contex["events"].append(event)
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                bullet = Bullet(
                    width = 30,height = 30,
                    x = SCREEM_WIDTH//2-5,y = SCREEM_HEIGHT//2-5,
                    x_taget = event.pos[0],y_taget = event.pos[1],
                    dame = 10,speed = 300,
                    producer=my_char
                )
                all_objs["layer_002"].append(bullet)
        elif event.type == pygame.MOUSEMOTION:
            mouse = event.pos
    if time.time()-last_time2>=0.5:
        bullet = Bullet(
            width = 100,height = 100,
            x = SCREEM_WIDTH//2-5,y = SCREEM_HEIGHT//2-5,
            x_taget = mouse[0],y_taget = mouse[1],
            dame = 70,speed = 300,
            producer=my_char
        )
        all_objs["layer_002"].append(bullet)
        last_time2 = time.time()
    if time.time()-last_time>=0.5:
        mob = Mob001(40,40,x=random.randint(50,SCREEM_WIDTH-100),y=random.randint(50,SCREEM_HEIGHT-100),speed = 100,max_HP=100,dame=100,fire_rate=1)
        mob.load_sprite()
        all_objs["layer_001"].append(mob)
        last_time = time.time()
    screen.fill("white")
    destroyed_list = []
    keys = list(all_objs.keys())
    keys.sort(reverse=True)
    
    contex["all_objs"] = all_objs


    for key in keys:
        for obj in all_objs[key]:
            obj.update(contex)
            obj.render(screen=screen)
            if obj.is_destroyed:
                destroyed_list.append([key,obj])
    for key,obj in destroyed_list:
        all_objs[key].remove(obj)
        del obj
    pygame.display.flip()
    clock.tick(60)
    fps+=1
    if time.time()-last>=3:
        print(f"FPS: {fps//3}")
        fps = 0
        last = time.time()

pygame.quit()