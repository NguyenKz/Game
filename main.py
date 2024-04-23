from gameobj import Bullet,Mob001,Char001, SCREEM,CLOCK
import pygame

screen = SCREEM
clock = CLOCK
running = True

all_objs:dict = {
    "layer_001" : [],
    "layer_002" : [],
}

my_char = Char001(40,40,screen.get_width()//2-20,screen.get_height()//2-20,max_HP=100,dame=100,fire_rate=1)
my_char.load_sprite()
all_objs["layer_001"].append(my_char)

mob = Mob001(40,40,x=100,y=100,max_HP=100,dame=100,fire_rate=1)
mob.load_sprite()
all_objs["layer_001"].append(mob)

while running:
    contex = {
        "all_objs":all_objs,
        "events":[]
    }
    for event in pygame.event.get():
        contex["events"].append(event)
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                bullet = Bullet(10,10,screen.get_width()//2-5,screen.get_height()//2-5,event.pos[0],event.pos[1],100,1000)
                all_objs["layer_002"].append(bullet)
        
    screen.fill("white")
    destroyed_list = []
    keys = list(all_objs.keys())
    keys.sort(reverse=True)
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
    clock.tick(120)

pygame.quit()