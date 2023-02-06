# tetris.py
# klon tetrisu
# autor: Kateřina Finková, finkovak@jirovcovka.net

# importování modulů
import pygame
import random

# barvy tetrimin
barvy = [
    (0, 0, 0),
    (251, 248, 204),
    (255, 207, 210),
    (241, 192, 232),
    (207, 186, 240),
    (163, 196, 243),
    (180, 243, 248),
    (185, 251, 192)
]
# třídy
class Tetrimino(object):
    ## tvary tetrimin
    tvary = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],                                  # I_tetrimino
        [[4, 5, 9, 10], [2, 6, 5, 9]],                                  # Z1_tetrimino 
        [[6, 7, 9, 10], [1, 5, 6, 10]],                                 # Z2_tetrimino 
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 8, 9], [4, 5, 6, 10]],      # L1_tetrimino
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],    # L2_tetrimino
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],       # T_tetrimino
        [[1, 2, 5, 6]]                                                  # O_tetrimino
    ]
    ## konstruktor
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.typ = random.randint(0, len(self.tvary) - 1)
        self.barva = self.typ + 1
        self.r = 0    
    ## pole tetrimina
    def okoli(self):
        return self.tvary[self.typ][self.r]
    ## otáčení
    ### po směru hodinových ručiček
    def otoc_R(self):
        self.r = (self.r + 1) % len(self.tvary[self.typ])
    ### proti směru hodinových ručiček
    def otoc_L(self):
        self.r = (self.r - 1) % len(self.tvary[self.typ])


class Tetris(object):
    highscore = 0
    x = 100
    y = 60
    zoom = 20
    tetrimino = None
    ## konstruktor
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.pole = []
        self.score = 0
        self.status = "game"
        ### vytvoření herní plochy
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.pole.append(new_line)
    ## generování nového tetrimina
    def new_tetrimino(self):
        self.tetrimino = Tetrimino(3, 0)
    ## překrýtí tetrimina s jiným/tetrimino mimo herní plochu
    def prekryti(self):
        kryt = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.tetrimino.okoli():
                    if i + self.tetrimino.y > self.height - 1 or j + self.tetrimino.x > self.width - 1 or j + self.tetrimino.x < 0 or \
                        self.pole[i + self.tetrimino.y][j + self.tetrimino.x] > 0:
                            kryt = True
        return kryt
    ## vyplnění řádky
    def plna_line(self):
        lines = 0
        for i in range(1, self.height):
            nuly = 0
            for j in range(self.width):
                if self.pole[i][j] == 0:
                    nuly += 1
            if nuly == 0:
                lines += 1
                for k in range(i, 1, -1):
                    for l in range(self.width):
                        self.pole[k][l] = self.pole[k - 1][l]
        self.score += lines
        if self.score > self.highscore:
            self.highscore = self.score
    ## slam
    def slam(self):
        while not self.prekryti():
            self.tetrimino.y += 1
        self.tetrimino.y -= 1
        self.stop()
    ## pohyb dolů
    def go_down(self):
        self.tetrimino.y += 1
        if self.prekryti():
            self.tetrimino.y -= 1
            self.stop()
    ## zastevení pohybu
    def stop(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.tetrimino.okoli():
                    self.pole[i + self.tetrimino.y][j + self.tetrimino.x] = self.tetrimino.barva
        self.plna_line()
        self.new_tetrimino()
        if self.prekryti():
            self.status = "gameover"
    ## pohyb do stran
    def go_side_R(self):
        x = self.tetrimino.x
        self.tetrimino.x += 1
        if self.prekryti():
            self.tetrimino.x = x
    def go_side_L(self):
        x = self.tetrimino.x
        self.tetrimino.x -= 1
        if self.prekryti():
            self.tetrimino.x = x
    ## otáčení
    ### po směru hodinových ručiček
    def otoc_R(self):
        old_r = self.tetrimino.r
        self.tetrimino.otoc_R()
        if self.prekryti():
            self.tetrimino.r = old_r
    ### proti směru hodinových ručiček
    def otoc_L(self):
        old_r = self.tetrimino.r
        self.tetrimino.otoc_L()
        if self.prekryti():
            self.tetrimino.r = old_r


# pygame
pygame.init()

## příprava hry
BARVA1 = (50, 50, 50)       # šedá
BARVA2 = (0, 0, 0)          # černá
BARVA3 = (161, 121, 226)    # tmavší fialová
BARVA4 = (207, 186, 240)    # světlá fialová
BARVA5 = (255, 173, 179)    # růžová
size = (400, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tetris")

konec = False
hodiny = pygame.time.Clock()
fps = 25
hra = Tetris(20, 10)
pocitadlo = 0
zmacknuti = False

## HLAVNÍ SMYČKA
while not konec:
    ### generování tetrimin
    if (hra.tetrimino is None) and (hra.status == "start"):
        hra.new_tetrimino()
    ### počátek hry
    pocitadlo += 1
    if (pocitadlo % fps == 0 or zmacknuti) and hra.status == "start":
        hra.go_down()
    ### zmáčknutí tlačítka
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            konec = True
        if event.type == pygame.KEYDOWN:
            if hra.status != "gameover":
                if event.key == pygame.K_d:
                    hra.otoc_R()
                if event.key == pygame.K_a:
                    hra.otoc_L()
                if event.key == pygame.K_DOWN:
                    zmacknuti = True
                if event.key == pygame.K_LEFT:
                    hra.go_side_L()
                if event.key == pygame.K_RIGHT:
                    hra.go_side_R()
                if event.key == pygame.K_s:
                    hra.slam()
            if hra.status == "gameover" or hra.status == "menu2":
                if event.key == pygame.K_ESCAPE:
                    hra.__init__(20, 10)
                    hra.status = "start"
        if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    zmacknuti = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mys = pygame.mouse.get_pos()
            if hra.status == "menu" or hra.status == "game":
                if 5 <= mys[0] <= 70 and 30 <= mys[1] <= 50:
                    hra.status = "start"
            
            if 5 <= mys[0] <= 70 and 60 <= mys[1] <= 80:
                if hra.status == "game":    
                    hra.status = "menu"
                if hra.status == "gameover":    
                    hra.status = "menu2"
    ### kreslení
    screen.fill(BARVA1)     #### pozadí
    for i in range(hra.height):
        for j in range(hra.width):
            #### mřížka
            pygame.draw.rect(screen, BARVA2, [hra.x + hra.zoom * j, hra.y + hra.zoom * i, hra.zoom, hra.zoom], 1)
            #### nakreslení čtverečku tetrimina
            if hra.pole[i][j] > 0:
                pygame.draw.rect(screen, barvy[hra.pole[i][j]], [hra.x + hra.zoom * j + 1, hra.y + hra.zoom * i + 1, hra.zoom - 2, hra.zoom - 2]) 
                    # +1, aby to divně neodskočilo
                    # -2, aby to bylo hezký, až to zůstane ve mřížce
    #### kreslení pohybu tetrimina
    if hra.tetrimino is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in hra.tetrimino.okoli():
                    pygame.draw.rect(screen, barvy[hra.tetrimino.barva], [hra.x + hra.zoom * (j + hra.tetrimino.x) + 1,
                        hra.y + hra.zoom * (i + hra.tetrimino.y) + 1, hra.zoom - 2, hra.zoom - 2])
    ### nápisy
    font = pygame.font.SysFont('rockwell', 25, True, False)                 # font větší
    font1 = pygame.font.SysFont('rockwell', 12, True, False)                # font menší
    text = font.render(f"Score: {str(hra.score)}", False, BARVA3)            # score
    text_start = font.render("Start", False, BARVA3)                         # tlačítko start
    text_menu = font.render("Menu", False, BARVA3)                           # tlačítko menu
    #### menu ovládání
    text_controls_A = font1.render("A - turn left", False, BARVA3)
    text_controls_D = font1.render("D - turn right", False, BARVA3)
    text_controls_S = font1.render("S - slam", False, BARVA3)
    text_controls_Move = font1.render("use arrows to move", False, BARVA3)
    #### game over
    text_controls_New = font1.render("Esc - play again", False, BARVA3)
    text_game_over = font.render("Game Over", False, BARVA5) 
    text_highscore = font1.render(f"Highcore: {str(hra.highscore)}", False, BARVA5)               
    ### nakreslení score
    screen.blit(text, [5, 0])
    ### ostatní kreslení
    if hra.status == "gameover":
        screen.blit(text_game_over, [135, 20])
        pygame.draw.rect(screen, BARVA4, [5,60,70,20])
        screen.blit(text_menu, [7,54])
        screen.blit(text_controls_New, [5, 24])
        screen.blit(text_highscore, [5, 36])
    if hra.status == "game":
        pygame.draw.rect(screen, BARVA4, [5,30,70,20])
        screen.blit(text_start, [11,24])
        pygame.draw.rect(screen, BARVA4, [5,60,70,20])
        screen.blit(text_menu, [7,54])
    if hra.status == "menu":
        pygame.draw.rect(screen, BARVA4, [5,30,70,20])
        screen.blit(text_start, [11,24])
        screen.blit(text_controls_A, [5, 54])
        screen.blit(text_controls_D, [5, 64])
        screen.blit(text_controls_S, [5, 74])
        screen.blit(text_controls_Move, [5, 84])
    if hra.status == "menu2":
        screen.blit(text_controls_A, [5, 54])
        screen.blit(text_controls_D, [5, 64])
        screen.blit(text_controls_S, [5, 74])
        screen.blit(text_controls_Move, [5, 84])
        screen.blit(text_controls_New, [5, 104])
        screen.blit(text_highscore, [5, 116])

    pygame.display.flip()
    hodiny.tick(fps)

pygame.quit()
