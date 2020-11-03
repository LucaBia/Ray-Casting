import pygame
import pygame_menu
from functools import partial
from math import cos, sin, pi


BLACK = (0,0,0)
WHITE = (255,255,255)
BACKGROUND = (64,64,64)

colors = {
    '1' : (31,54,61),
    '2' : (64, 121, 140),
    '3' : (112, 169, 161)
}

textures = {
    '1' : pygame.image.load('Scifi_Wall_Black.jpg'),
    '2' : pygame.image.load('Scifi_Wall_White.jpg'),
    '3' : pygame.image.load('Scifi_Wall_Copper.jpg'),
}



class Raycaster(object):
    def __init__(self,screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()
        self.map = []
        self.blocksize = 50
        self.wallHeight = 50
        self.stepSize = 5
        # self.setColor(WHITE)
        self.player = {
            "x" : 75,
            "y" : 175,
            "angle" : 0,
            "fov" : 60
            }

    # def setColor(self, color):
    #     self.blockColor = color

    def load_map(self, filename):
        with open(filename) as f:
            for line in f.readlines():
                self.map.append(list(line))

    def drawRect(self, x, y, tex):
        tex = pygame.transform.scale(tex, (self.blocksize, self.blocksize))
        rect = tex.get_rect()
        rect = rect.move( (x,y) )
        self.screen.blit(tex, rect)


    def drawPlayerIcon(self,color):
        rect = (int(self.player['x'] - 2), int(self.player['y'] - 2), 5, 5)
        self.screen.fill(color, rect)

    def castRay(self, a):
        rads = a * pi / 180
        dist = 0
        while True:
            x = int(self.player['x'] + dist * cos(rads))
            y = int(self.player['y'] + dist * sin(rads))

            i = int(x/self.blocksize)
            j = int(y/self.blocksize)

            if self.map[j][i] != ' ':
                hitX = x - i*self.blocksize
                hitY = y - j*self.blocksize

                if 1 < hitX < self.blocksize - 1:
                    maxHit = hitX
                else:
                    maxHit = hitY

                tx = maxHit / self.blocksize
                
                return dist, self.map[j][i], tx

            self.screen.set_at((x,y), WHITE)

            # dist += 5
            dist += 2

    def render(self):

        halfWidth = int(self.width/2)
        halfHeight = int(self.height/2)

        for x in range(0, halfWidth, self.blocksize):
            for y in range(0, self.height, self.blocksize):
                
                i = int(x/self.blocksize)
                j = int(y/self.blocksize)

                if self.map[j][i] != ' ':
                    self.drawRect(x, y, textures[self.map[j][i]])

        self.drawPlayerIcon(BLACK)

        for i in range(halfWidth):
            angle = self.player['angle'] - self.player['fov']/2 + self.player['fov'] * i/halfWidth
            dist, wallType, tx = self.castRay(angle)

            x = halfWidth + i 

            h = self.height / (dist * cos( (angle - self.player['angle']) * pi / 180 )) * self.wallHeight

            start = int( halfHeight - h/2)
            end = int( halfHeight + h/2)

            img = textures[wallType]
            tx = int(tx * img.get_width())

            for y in range(start, end):
                ty = (y - start)/(end - start)
                ty = int(ty * img.get_height())
                texColor = img.get_at((tx, ty))
                self.screen.set_at((x, y), texColor)

        for i in range(self.height):
            self.screen.set_at( (halfWidth, i), BLACK)
            self.screen.set_at( (halfWidth+1, i), BLACK)
            self.screen.set_at( (halfWidth-1, i), BLACK)


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
                    # Cierra el juego
                    isRunning = False
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

        # Color del suelo
        screen.fill(pygame.Color("gray"))
        # Color del cielo
        screen.fill(pygame.Color(154, 202, 231), (int(r.width / 2), 0, int(r.width / 2),int(r.height / 2)))
        screen.fill(pygame.Color("dimgray"), (int(r.width / 2), int(r.height / 2), int(r.width / 2),int(r.height / 2)))

        r.render()

        screen.fill(pygame.Color("black"), (0,0,30,30))
        screen.blit(updateFPS(), (0,0))
        clock.tick(30)
        
        pygame.display.update()

# https://pygame-menu.readthedocs.io/en/latest/_source/widgets_image.html
background_image = pygame_menu.baseimage.BaseImage(
    image_path = 'background.jpg',
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
menu.add_image('HP_logo.png', scale=(0.5, 0.5))
paint_background(screen)
# menu.mainloop(screen)
menu.mainloop(surface=screen,
              bgfun=partial(paint_background, screen),
            #   disable_loop=test,
              fps_limit=30.0)
pygame.quit()
