import pygame
import pygame_menu
from functools import partial
from math import cos, sin, pi, atan2


BLACK = (0,0,0)
WHITE = (255,255,255)
BACKGROUND = (64,64,64)
SPRITE_BACKGROUND = (152, 0, 136, 255)


textures = {
    '1' : pygame.image.load('media/game/wall.png'),
    '2' : pygame.image.load('media/game/wallFrames2.png'),
    '3' : pygame.image.load('media/game/devilWall.png'),
}

enemies = [
    {
        "x": 100,
        "y": 200,
        "texture" : pygame.image.load('media/game/enemy1.png')
    },
    {
        "x": 270,
        "y": 200,
        "texture" : pygame.image.load('media/game/enemy2.png')
    },
    {
        "x": 270,
        "y": 420,
        "texture" : pygame.image.load('media/game/enemy3.png')   
    }    
]


class Raycaster(object):
    def __init__(self,screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()
        self.map = []
        self.zbuffer = [-float('inf') for z in range(int(self.width / 2))]
        self.blocksize = 50
        self.wallHeight = 50
        self.stepSize = 5
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
        rect = rect.move((x,y))
        self.screen.blit(tex, rect)


    def drawPlayerIcon(self,color):
        rect = (int(self.player['x'] - 2), int(self.player['y'] - 2), 5, 5)
        self.screen.fill(color, rect)

    def drawSprite(self, sprite, size):
        # Pitagoras
        spriteDist = ((self.player['x'] - sprite['x'])**2 + (self.player['y'] - sprite['y'])**2) ** 0.5
        
        # Angulo entre el personaje y el sprite, arco tangente 2
        spriteAngle = atan2(sprite['y'] - self.player['y'], sprite['x'] - self.player['x'])

        aspectRatio = sprite["texture"].get_width() / sprite["texture"].get_height()
        spriteHeight = (self.height / spriteDist) * size
        spriteWidth = spriteHeight * aspectRatio

        #Convertir a radianes
        angleRads = self.player['angle'] * pi / 180
        fovRads = self.player['fov'] * pi / 180

        #Buscamos el punto inicial para dibujar el sprite
        startX = (self.width * 3 / 4) + (spriteAngle - angleRads)*(self.width/2) / fovRads - (spriteWidth/2)
        startY = (self.height / 2) - (spriteHeight / 2)
        startX = int(startX)
        startY = int(startY)

        for x in range(startX, int(startX + spriteWidth)):
            for y in range(startY, int(startY + spriteHeight)):
                if (self.width / 2) < x < self.width:
                    if self.zbuffer[ x - int(self.width/2)] >= spriteDist:
                        tx = int( (x - startX) * sprite["texture"].get_width() / spriteWidth )
                        ty = int( (y - startY) * sprite["texture"].get_height() / spriteHeight )
                        texColor = sprite["texture"].get_at((tx, ty))
                        if texColor[3] > 128 and texColor != SPRITE_BACKGROUND:
                            self.screen.set_at((x,y), texColor)
                            self.zbuffer[ x - int(self.width/2)] = spriteDist

    def castRay(self, a):
        rads = a * pi / 180
        dist = 0
        while True:
            x = int(self.player['x'] + dist * cos(rads))
            y = int(self.player['y'] + dist * sin(rads))

            i = int(x/self.blocksize)
            j = int(y/self.blocksize)

            if self.map[j][i] != ' ':
                hitX = x - i * self.blocksize
                hitY = y - j * self.blocksize

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

            self.zbuffer[i] = dist

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

        for enemy in enemies:
            self.screen.fill(pygame.Color("black"), (enemy['x'], enemy['y'], 3,3))
            self.drawSprite(enemy, 30)

        for i in range(self.height):
            self.screen.set_at( (halfWidth, i), BLACK)
            self.screen.set_at( (halfWidth + 1, i), BLACK)
            self.screen.set_at( (halfWidth - 1, i), BLACK)