import pygame

pygame.font.init()

MX, MY = 50, 65

SX = 8 * MX-1
SY = 9 * MY-1

pygame.init()
screen = pygame.display.set_mode((SX, SY))
clock = pygame.time.Clock()

running = True

WIN = False
buffer = -1
Boxes = []
IcanseetheText = True

Text1 = pygame.font.Font(None, 36)
text1 = Text1.render('Space to start', True, (255, 255, 255))
text2 = Text1.render('F to test', True, (255, 255, 255))
text3 = Text1.render('You WIN!', True, (255, 255, 255))


def drawBox(x, y, color):
    pygame.draw.rect(screen, color, (int(x) * 50, int(y) * 65, 49, 64))

class Box:
    def __init__(self, sx, sy, color):
        self.sx = sx
        self.sy = sy
        if (sx + sy) % 2 == 0:
            self.const = True
        else:
            self.const = False
        self.Gcolor = color
        self.Lcolor = [0, 0, 0]
        self.color = [0, 0, 0]
        self.GReSelect()
        self.ReSelect()
    def Select(self):
        for i in range(len(self.color)):
            self.color[i] += 50
            if self.color[i]>255:
                self.color[i] = 255
    def GReSelect(self):
        self.Lcolor = [0, 0, 0]
        for i in range(3):
            self.Lcolor[i] += self.Gcolor[i]
    def ReSelect(self):
        self.color = [0, 0, 0]
        for i in range(3):
            self.color[i] += self.Lcolor[i]

for j in range(9):
    for i in range(8):
        box = Box(i, j, [220,i*21,j*21])
        Boxes.append(box)

def Mixing():
    global IcanseetheText
    IcanseetheText = False
    from random import shuffle
    Colors = []
    for i in Boxes:
        if i.const:
            continue
        Colors.append(i.Gcolor)
    shuffle(Colors)
    j = 0
    for i in Boxes:
        if i.const:
            continue
        i.Lcolor = Colors[j]
        i.ReSelect()
        j+=1

def Test():
    z = 0
    for i in Boxes:
        if i.Gcolor != i.Lcolor:
            z+=1
    if z == 0:
        global IcanseetheText, WIN
        IcanseetheText = True
        WIN = True

while running:
    screen.fill((255, 120, 15)) #global color
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE:
                Mixing()
            if event.key == pygame.K_f:
                Test()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                #print(event.pos[0] // 50, event.pos[1] // 65)
                if buffer == -1:
                    if not(Boxes[event.pos[1] // 65 * 8 + event.pos[0] // 50].const):
                        Boxes[event.pos[1] // 65 * 8 + event.pos[0] // 50].Select()
                        buffer = event.pos[1] // 65 * 8 + event.pos[0] // 50
                        #print(Boxes[buffer])
                else:
                    if not (Boxes[event.pos[1] // 65 * 8 + event.pos[0] // 50].const):
                        Boxes[buffer].color = Boxes[event.pos[1] // 65 * 8 + event.pos[0] // 50].Lcolor
                        Boxes[event.pos[1] // 65 * 8 + event.pos[0] // 50].Lcolor = Boxes[buffer].Lcolor
                        Boxes[buffer].Lcolor = Boxes[buffer].color
                        Boxes[buffer].ReSelect()
                        Boxes[event.pos[1] // 65 * 8 + event.pos[0] // 50].ReSelect()
                        buffer = -1


    for i in range(len(Boxes)):
        drawBox(Boxes[i].sx, Boxes[i].sy, Boxes[i].color)
        if Boxes[i].const:
            pygame.draw.rect(screen, (Boxes[i].Gcolor[0]//30*25,Boxes[i].Gcolor[1]//30*25,Boxes[i].Gcolor[2]//30*25), (int(Boxes[i].sx) * 50 + 19, int(Boxes[i].sy) * 65 + 25, 12, 15))

    if IcanseetheText:
        if not(WIN):
            screen.blit(text1, (117, 530))
            screen.blit(text2, (152, 555))
        else:
            screen.blit(text3, (152, 555))

    clock.tick(45)
    pygame.display.flip()

pygame.quit()
