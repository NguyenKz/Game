import json
import math
import time
import pygame

from utils.tool import *

pygame.init()
screen_width = 1200
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Zoom Example")



zoom = 1.0
mouse = [0, 0]
camera = [0, 0]

running = True
clock = pygame.time.Clock()
selected_box =[]
box_mouse = []
old_zoom = zoom
postions = []
list_image = []
postions = []

lines_x = []
lines_y = []
is_select_box = True
selected_box = []
old_selected_point = []
list_box = []

list_sprite = []

json_name = "bullet"
config_init = {
    "name":"bullet_02_explode",
    "time":0.3,
    "is_reverse":True,
    "is_repeat":True,
    "angle":0,
    "background":[0,0],
    "position":[]
}
json_path = f"resource/sprite/{json_name}.json"
with open(json_path,"r")as file:
    loaded_data = json.loads(file.read())
image = pygame.image.load(loaded_data["path"])
original_image = image.copy() 
show_img = original_image.copy()

temp_sprite =TempSprite()

for sprite in loaded_data["sprites"]:
    if sprite["name"]==config_init["name"]:
        boxs = [[box["start"],box["end"]] for box in sprite["position"]]
        for box in boxs:
            add_line(all_line=lines_x,point=box[0],type_line="x",image=original_image)
            add_line(all_line=lines_y,point=box[1],type_line="y",image=original_image)
                
        temp_sprite.add_img(boxs=boxs,image=image)
        list_box = boxs

        save(file_name=f"{json_name}_new",config_init=config_init,list_box=list_box,all_data=loaded_data)
        break
while running:
    screen.fill((255, 255, 255))  # Clear the screen
    is_update_zoom = False
    is_update_zoom_postion = False

    is_zoom_up = False
    is_zoom_down = False
    is_add_x_line = False
    is_add_y_line = False
    is_remove_line = False
    is_update_select_box = False
    mouse = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type ==pygame.MOUSEBUTTONUP:
            if event.button==pygame.BUTTON_LEFT:
                if is_select_box:
                    is_update_select_box = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                camera[0]-=50
                is_update_zoom = True

            if event.key == pygame.K_RIGHT:
                camera[0]+=50
                is_update_zoom = True

            if event.key == pygame.K_UP:
                camera[1]-=50
                is_update_zoom = True
            if event.key == pygame.K_DOWN:
                camera[1]+=50
                is_update_zoom = True
            if event.key == pygame.K_a:
                is_add_x_line = True
            if event.key == pygame.K_d:
                is_add_y_line = True
            if event.key == pygame.K_s:
                is_add_x_line = True
                is_add_y_line = True
            if event.key == pygame.K_f:
                is_remove_line = True
            if event.key == pygame.K_w:
                is_select_box = not is_select_box
            if event.key == pygame.K_RETURN:
                if len(selected_box)==4 and is_select_box:
                    start_p = None
                    end_p = None
                    for p in selected_box:
                        if start_p is None or start_p[0]>p[0] or start_p[1]>p[1]:
                            start_p = p
                        if end_p is None or end_p[0]<p[0] or end_p[1]<p[1]:
                            end_p = p
                    list_box.append([start_p,end_p])
                    selected_box = []
                    is_update_zoom=True
                    temp_sprite.add_img(boxs=list_box,image=original_image)
                    save(file_name=f"{json_name}_new",config_init=config_init,list_box=list_box,all_data=loaded_data)
                    print(f"save {json_name}_new.json")
            if event.key == pygame.K_g:
                delete_box = []
                for b in list_box:
                    if point_in_rectangle(point=org_mouse,rectangle=b):
                        delete_box.append(b)

                for b in delete_box:
                    list_box.remove(b)
                    is_update_zoom=True

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pass
        elif event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                is_zoom_up=True
                is_zoom_down = False
            if event.y < 0:
                is_zoom_up=False
                is_zoom_down = True
    org_mouse = get_org_postion(mouse=mouse,camera=camera,zoom=zoom)
    if is_add_x_line:
        if add_line(all_line=lines_x,point=org_mouse,image=original_image,type_line="x"):
            is_update_zoom = True

    if is_add_y_line:
        if add_line(all_line=lines_y,point=org_mouse,image=original_image,type_line="y"):
            is_update_zoom = True
        
    if is_remove_line:
        remove_lines = []
        for line in lines_x:
            if are_collinear(org_mouse,line[0],line[1]):
                remove_lines.append(line)
                is_update_zoom = True
        for line in remove_lines:
            lines_x.remove(line)
        
        remove_lines = []
        for line in lines_y:
            if are_collinear(org_mouse,line[0],line[1]):
                remove_lines.append(line)
                is_update_zoom = True
        for line in remove_lines:
            lines_y.remove(line)
        

    if is_zoom_up:
        old_zoom = zoom
        zoom+=0.5
        is_update_zoom = True
        is_update_zoom_postion = True
    if is_zoom_down:
        old_zoom = zoom
        zoom-=0.5
        if zoom<1:
            zoom = 1
        is_update_zoom = True
        is_update_zoom_postion = True

    if is_update_select_box:
        list_point = find_all_intersections(horizontal_lines=lines_y,vertical_lines=lines_x)
        for p in list_point:
            if math.sqrt((p[0]-org_mouse[0])**2+(p[1]-org_mouse[1])**2)<5:
                if p not in selected_box:
                    selected_box.append(p)
                else:
                    selected_box.remove(p)
    selected_point = []
    if is_select_box:
        list_point = find_all_intersections(horizontal_lines=lines_y,vertical_lines=lines_x)

        for point in list_point:
            
            d_m2p = math.sqrt((point[0]-org_mouse[0])**2+(point[1]-org_mouse[1])**2)
            d_m2b = 9999
            if selected_point:
                d_m2b = math.sqrt((selected_point[0]-org_mouse[0])**2+(selected_point[1]-org_mouse[1])**2)
            if d_m2p<5 and d_m2p<d_m2b:
                selected_point = point

        if selected_point!=old_selected_point:
            old_selected_point = selected_point
            is_update_zoom = True



    if is_update_zoom:
        if is_update_zoom_postion:
            zoom_change = zoom / old_zoom
            camera[0] = int((camera[0] + mouse[0]) * zoom_change - mouse[0])
            camera[1] = int((camera[1] + mouse[1]) * zoom_change - mouse[1])
        _original_image = original_image.copy()
            
        for line in lines_x:
            pygame.draw.line(_original_image,[0,255,255],line[0],line[1],1)
        for line in lines_y:
            pygame.draw.line(_original_image,[0,255,255],line[0],line[1],1)
        for box in selected_box:
            pygame.draw.rect(_original_image,[0,150,150],[box[0]-5,box[1]-5,10,10],1)
        if len(selected_box)>=2:
            pygame.draw.polygon(_original_image,[0,250,0],points=selected_box,width=1)
        if selected_point:
            pygame.draw.rect(_original_image,[0,150,150],[selected_point[0]-5,selected_point[1]-5,10,10],1)

        for bo in list_box:
            pygame.draw.rect(
                _original_image,
                [250,0,0],
                [bo[0][0],bo[0][1],abs(bo[1][0]-bo[0][0]),abs(bo[1][1]-bo[0][1])],
                1
            )
        zoomed_width = int(_original_image.get_width() * zoom)
        zoomed_height = int(_original_image.get_height() * zoom)
        zoomed_image = pygame.transform.smoothscale(_original_image, (zoomed_width, zoomed_height))
        show_img = pygame.Surface((screen_width, screen_height))
        visible_area = pygame.Rect(camera[0], camera[1], screen_width, screen_height)
        show_img.blit(zoomed_image, (0, 0), visible_area)

    screen.blit(show_img, (0, 0))

    pygame.draw.line(screen, (0, 255, 0), (mouse[0], 0), (mouse[0], screen_height))
    pygame.draw.line(screen, (0, 255, 0), (0, mouse[1]), (screen_width, mouse[1]))
    font = pygame.font.Font(None, 24)
    mouse_relative_to_zoomed = (mouse[0] + camera[0], mouse[1] + camera[1])

    original_x = mouse_relative_to_zoomed[0] // zoom
    original_y = mouse_relative_to_zoomed[1] // zoom
    zoom_text = font.render(f"Zoom: {zoom:.1f}x  {original_x}x{original_y}", True, (0, 0, 255))
    screen.blit(zoom_text, (10, 10))

    temp_sprite.render(screen=screen,start_x=0,start_y=0)
    for i,sprite in enumerate(list_sprite):
        sprite.render(screen=screen,start_x=i*70,start_y=0)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
