import pygame
from gl import *



def updateFPS():
    fps = str(int(clock.get_fps()))
    fps = font.render(fps, 1, pygame.Color("white"))
    return fps

def paint_background(surface):
    surface.fill((0, 0, 0))

pygame.init()
screen = pygame.display.set_mode((1000,500), pygame.DOUBLEBUF | pygame.HWACCEL)
pygame.display.set_caption("UVG Graficas por computadora")
screen.set_alpha(None)
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)


r = Raycaster(screen)
# r.setColor( (128,0,0) )
r.load_map('map.txt')

# Reproducción de música
pygame.mixer.init()
pygame.mixer.music.load('media/soundtrack.mp3')
pygame.mixer.music.play()


def start_the_game():
    isRunning = True
    while isRunning:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                isRunning = False

            newX = r.player['x']
            newY = r.player['y']

            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE: 
                    isRunning = False # Menu
                elif ev.key == pygame.K_w or ev.key == pygame.K_UP:
                    newX += cos(r.player['angle'] * pi / 180) * r.stepSize
                    newY += sin(r.player['angle'] * pi / 180) * r.stepSize
                elif ev.key == pygame.K_s or ev.key == pygame.K_DOWN:
                    newX -= cos(r.player['angle'] * pi / 180) * r.stepSize
                    newY -= sin(r.player['angle'] * pi / 180) * r.stepSize 
                elif ev.key == pygame.K_a or ev.key == pygame.K_LEFT:
                    newX -= cos((r.player['angle'] + 90) * pi / 180) * r.stepSize
                    newY -= sin((r.player['angle'] + 90) * pi / 180) * r.stepSize
                elif ev.key == pygame.K_d or ev.key == pygame.K_RIGHT:
                    newX += cos((r.player['angle'] + 90) * pi / 180) * r.stepSize
                    newY += sin((r.player['angle'] + 90) * pi / 180) * r.stepSize
                elif ev.key == pygame.K_q or ev.key == pygame.K_z:
                    r.player['angle'] -= 5
                elif ev.key == pygame.K_e or ev.key == pygame.K_x:
                    r.player['angle'] += 5

                i = int(newX/r.blocksize)
                j = int(newY/r.blocksize)

                if r.map[j][i] == ' ':
                    r.player['x'] = newX
                    r.player['y'] = newY

        # Color de fondo
        screen.fill(pygame.Color("gray"))
        # Color del cielo
        screen.fill(pygame.Color(154, 202, 231), (int(r.width / 2), 0, int(r.width / 2),int(r.height / 2)))
        # Color del suelo
        screen.fill(pygame.Color("dimgray"), (int(r.width / 2), int(r.height / 2), int(r.width / 2),int(r.height / 2)))

        r.render()

        screen.fill(pygame.Color("black"), (0,0,30,30))
        screen.blit(updateFPS(), (0,0))
        clock.tick(30)
        
        pygame.display.update()

# https://pygame-menu.readthedocs.io/en/latest/_source/widgets_image.html
background_image = pygame_menu.baseimage.BaseImage(
    image_path = 'media/menu/background.jpg',
    drawing_mode = pygame_menu.baseimage.IMAGE_MODE_FILL,
)

Theme = pygame_menu.themes.Theme

mytheme = Theme(background_color = background_image,
                title_shadow = True,
                title_background_color = (116, 0, 1),
                title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_SIMPLE,
                cursor_selection_color = (255, 255, 255),
                widget_font = pygame_menu.font.FONT_HELVETICA,
                menubar_close_button = False,
                widget_alignment = pygame_menu.locals.ALIGN_CENTER,
                title_offset = (190, 0))

menu = pygame_menu.Menu(400, 600, 
                        title = 'Harry Potter', 
                        theme = mytheme)
menu.add_button('Jugar', start_the_game)
menu.add_button('Salir', pygame_menu.events.EXIT)
menu.add_image('media/menu/HP_logo.png', scale=(0.5, 0.5))
paint_background(screen)
# menu.mainloop(screen)
menu.mainloop(surface=screen,
              bgfun=partial(paint_background, screen),
            #   disable_loop=test,
              fps_limit=30.0)
pygame.quit()
