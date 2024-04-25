import pygame

# Initialize pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Zoom Example")

# Load the image
image = pygame.image.load("C:/Users/NguyenKz/Documents/Code/Python/Game/resource/img/bullet.png")
original_image = image.copy()  # Store the original image for zooming

# Zoom variables
zoom = 1.0
mouse = [0, 0]
camera = [0, 0]
show_img = image

# Main loop
running = True
clock = pygame.time.Clock()
box =[]
box_mouse = []
old_zoom = zoom
postions = []
list_image = []
while running:
    screen.fill((255, 255, 255))  # Clear the screen
    is_update_zoom = False
    is_update_zoom_postion = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            mouse = event.pos
            mouse_relative_to_zoomed = (mouse[0] + camera[0], mouse[1] + camera[1])
            original_x = int(mouse_relative_to_zoomed[0] // zoom)
            original_y = int(mouse_relative_to_zoomed[1] // zoom)
            if len(box)==1:
                is_update_zoom = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RETURN:
                if len(box)==2:
                    postions.append(box)
                    start = box[0]
                    end = box[1]
                    width, height = end[0]-start[0], end[1]-start[1]
                    x, y = start[0], start[1]
                    cropped_image = pygame.Surface((width, height))
                    cropped_image.blit(image, (0, 0), (x, y, width, height))
                    cropped_image.convert()
                    list_image.append(cropped_image)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                box.append([original_x,original_y])
                if len(box)>2:
                    box = []
                is_update_zoom = True
                is_update_zoom_postion = False

        elif event.type == pygame.MOUSEWHEEL:
            old_zoom = zoom
            if event.y > 0:
                zoom += 0.5
            if event.y < 0:
                zoom -= 0.5
            if zoom < 1:
                zoom = 1
            is_update_zoom = True
            is_update_zoom_postion = True

    if is_update_zoom:
        if is_update_zoom_postion:
            # Calculate the change in zoom level
            zoom_change = zoom / old_zoom
            # Update camera position based on mouse position and zoom change
            camera[0] = int((camera[0] + mouse[0]) * zoom_change - mouse[0])
            camera[1] = int((camera[1] + mouse[1]) * zoom_change - mouse[1])
        _original_image = original_image.copy()
        if len(box)==2:
            pygame.draw.rect(_original_image,(0,0,244),(box[0][0],box[0][1],box[1][0]-box[0][0],box[1][1]-box[0][1]),width=1)
        elif len(box)==1:
            pygame.draw.rect(_original_image,(0,0,244),(box[0][0],box[0][1],original_x-box[0][0],original_y-box[0][1]),width=1)
        # Calculate zoomed image size and position
        zoomed_width = int(_original_image.get_width() * zoom)
        zoomed_height = int(_original_image.get_height() * zoom)
        zoomed_image = pygame.transform.smoothscale(_original_image, (zoomed_width, zoomed_height))

        # Create a surface to hold the zoomed image
        show_img = pygame.Surface((screen_width, screen_height))

        # Calculate the visible area of the zoomed image
        visible_area = pygame.Rect(camera[0], camera[1], screen_width, screen_height)

        # Blit the visible area of the zoomed image onto the surface
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

    y = 0
    for img in list_image:
        screen.blit(img, (0,y))
        y+=img.get_height()
    

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
