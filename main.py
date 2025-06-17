from random import random, choice, Random
import pygame
from pygame import Rect

BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)
RED = (232, 63, 66)
GREEN = (17, 158, 32)
BLUE = (37, 150, 190)
SAND= (234,182,118)

HEIGHT = 10
WIDTH = 12

RECT_HEIGHT = 60
RECT_WIDTH = 60

SCREEN_SIZE = 720, 600

class Agente:
    def __init__(self):
        self.pos = [None,None]

class Mapa:
    def __init__(self, agente, width=12, height=10, tropecoValor = 0):
        self.larguraMapa = width
        self.alturaMapa = height
        self.tropeco = tropecoValor
        self.agente = agente

    def resetPosicao(self): #def reset(self)
        self.agente.pos = [9,4]
        return self.agente.pos.copy()

    def andar(self, direcaoEscolhida): # def act(self, action):
        if direcaoEscolhida == 0: #cima
            self.agente.pos[0] -=1
        elif direcaoEscolhida == 1: #direita
            self.agente.pos[1] +=1
        elif direcaoEscolhida == 2: #baixo
            self.agente.pos[0] +=1
        elif direcaoEscolhida == 3: #esquerda
            self.agente.pos[1] -=1
        else:
            print("Erro de acao invalida durante andar(<Mapa>)")

        #Tropeço
        if random() < self.tropeco:
            self.agente.pos[0] += choice([-1,0,1])
            self.agente.pos[1] += choice([-1,0,1])


        #LOGICA DE LIMITAÇÃO DE PAREDES DO MAPA

        if((self.agente.pos[1] < 4) or (self.agente.pos[1] > 7) ) and ( self.agente.pos[0] < 5) :
            self.agente.pos[0] = min(4, max(0, self.agente.pos[0]))
            self.agente.pos[1] = min(self.larguraMapa-1, max(0, self.agente.pos[1]))
        elif((5 <= self.agente.pos[0] ) and ( 4 <= self.agente.pos[1] <= 7)):
            self.agente.pos[0] = min(self.alturaMapa - 1, max(0, self.agente.pos[0]))
            self.agente.pos[1] = min(7, max(4, self.agente.pos[1]))
        elif(self.agente.pos[0]>=5 and  (7 < self.agente.pos[1] or self.agente.pos[1]<4) ):
            self.agente.pos[0] = min(self.alturaMapa-1, max(0, self.agente.pos[0]))
            self.agente.pos[1] = min(7, max(4, self.agente.pos[1]))
        elif (self.agente.pos[0] < 5):
            self.agente.pos[0] = min(self.alturaMapa - 1, max(0, self.agente.pos[0]))
            self.agente.pos[1] = min(self.larguraMapa-1, max(0, self.agente.pos[1]))

        recompensa = 0
        final = False

        #RECOMPENSAS E PENALIDADES NO MAPA
        if(self.agente.pos[0] == 4) and (self.agente.pos[1] == 11):
             recompensa = 100
             final = True

        elif(( self.agente.pos[0] == 0) and (self.agente.pos[1] == 4 or  self.agente.pos[1] == 11)):
            recompensa = -100
            final = True
        elif ((self.agente.pos[0] == 1) and (self.agente.pos[1] == 1 or self.agente.pos[1] == 11)):
            recompensa = -100
            final = True
        elif ((self.agente.pos[0] == 2) and (self.agente.pos[1] in [0,2,6,8,9])):
            recompensa = -100
            final = True
        elif ((self.agente.pos[0] == 3) and (self.agente.pos[1] in [1,8])):
            recompensa = -100
            final = True
        elif ((self.agente.pos[0] == 5) and (self.agente.pos[1] == 6 )):
            recompensa = -100
            final = True
        elif ((self.agente.pos[0] == 8) and (self.agente.pos[1] == 6 )):
            recompensa = -100
            final = True
        return self.agente.pos.copy(), recompensa, final

class QLearning:
    def __init__(self, epsilon=0.1, alpha=0.1, gamma=0.9, valorInicial=0, w=12, h=10, a=4):
        self.epsilon = epsilon #TAXA DE ALEATORIEDADE
        self.alpha = alpha #TAXA DE APRENDIZAGEM
        self.gamma = gamma #FATOR DE DESCONTO CONFORME ATUALIZA ESTADOS ANTERIRES
        self.larguraMapa = w
        self.alturaMapa = h
        self.acoes = a
        self.inicialQtable = valorInicial
        self.criaQTable()

    def criaQTable(self):  # reinicia a Qtable com 0,0,0,0 (#up #right, #down #left)
        #formando uma matriz em "3D"
        self.qtable = [[[self.inicialQtable] * self.acoes for j in range(self.larguraMapa)] for i in range(self.alturaMapa)]

    def printQTable(self):  # self.qtable[i][j][X] i,j = posicao no mapa | X = valor da ação escolhida
        print("Pos   |   Up   |  Right |  Down  |  Left  |")
        for i in range(self.alturaMapa):
            for j in range(self.larguraMapa):
                if i >= 5 and (0 <= j <= 3 or 8 <= j <= 11):
                    continue
                print("{:>2},{:<2} | {:>6} | {:>6} | {:>6} | {:>6} |".format(
                    i, j,
                    self.qtable[i][j][0],
                    self.qtable[i][j][1],
                    self.qtable[i][j][2],
                    self.qtable[i][j][3]
                ))

    def getMaximoPosicao(self,pos):#retorna o maior valor entre 0|1|2|3 na posicao Y X da qtable
        return max(self.qtable[pos[0]][pos[1]])

    def getMelhorAcao(self,pos):
        posicao = self.qtable[pos[0]][pos[1]] #vetor de valores da Qtable
        m = max(posicao) #valores mais altos
        melhoresCaminhos =  [i for i, j in enumerate(posicao) if j == m] #cria um vetor de melhoresEscolhas caso
        #possua mais de um caminho com o valor igual
        return choice(melhoresCaminhos) #escolhe um de forma aleatoria com choice

    def getAcaoAleatoria(self):
        return int (random() * self.acoes)

    def getAcao(self,pos):
        if random() < self.epsilon: #epsilion é a taxa de "tropeço" ou "aleatoriedade do ambiente" que pode ocorrer
            return self.getAcaoAleatoria()
        else:
            return self.getMelhorAcao(pos)

    def atualizaQtable(self,posOld,acao,posNew,recompensa,final):
        if final:
            self.qtable[posOld[0]][posOld[1]][acao] += self.alpha * (recompensa - self.qtable[posOld[0]][posOld[1]][acao])
        else:
            self.qtable[posOld[0]][posOld[1]][acao] += self.alpha * (recompensa + self.gamma * self.getMaximoPosicao(posNew) - self.qtable[posOld[0]][posOld[1]][acao])

agt = Agente()
alturaMapa = 10
larguraMapa = 12

mp = Mapa(agt,larguraMapa,alturaMapa,0)

ql = QLearning(epsilon=0.3, alpha=0.5, valorInicial=1, w=larguraMapa, h=alturaMapa)

episodios = 1000

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)

imgChao = pygame.image.load("./assets/img/tile_0001.png")
imgRecompensa = pygame.image.load("./assets/img/tile_0029.png")
imgParede = pygame.image.load("./assets/img/tile_0005.png")
imgPersonagem = pygame.image.load("./assets/img/tile_0019.png")
imgPenalidade = pygame.image.load("./assets/img/tile_0105.png")



chao = pygame.transform.scale(imgChao, (RECT_WIDTH, RECT_HEIGHT))
recompensaIMG =  pygame.transform.scale(imgRecompensa, (RECT_WIDTH, RECT_HEIGHT))
parede =  pygame.transform.scale(imgParede, (RECT_WIDTH, RECT_HEIGHT))
personagem = pygame.transform.scale(imgPersonagem, (RECT_WIDTH, RECT_HEIGHT))
penalidade =   pygame.transform.scale(imgPenalidade, (RECT_WIDTH, RECT_HEIGHT))

font = pygame.font.Font('freesansbold.ttf', 12)
def desenhar_mapa(qlearning, mapa, agente):
    screen.fill(WHITE)
    clock = pygame.time.Clock()
    for y in range(alturaMapa):
        for x in range(larguraMapa):
            rect = Rect(x * RECT_WIDTH, y * RECT_HEIGHT, RECT_WIDTH, RECT_HEIGHT)

            cor = WHITE
            valor = 0
            screen.blit(chao, (x * RECT_WIDTH, y * RECT_HEIGHT))
            if (0 <= x <= 3) or (x >= 8 and y <= 11):
                if 5 <= y <= 9:
                    valor = -1000.0
                    screen.blit(parede, (x * RECT_WIDTH, y * RECT_HEIGHT))

            if (y == 4) and (x == 11):
                valor = 100
                screen.blit(recompensaIMG, (x * RECT_WIDTH, y * RECT_HEIGHT))


            elif (y == 0) and (x == 4 or x == 11):
                valor = -100
                screen.blit(penalidade, (x * RECT_WIDTH, y * RECT_HEIGHT))

            elif (y == 1) and (x == 1 or x == 11):
                valor = -100
                screen.blit(penalidade, (x * RECT_WIDTH, y * RECT_HEIGHT))

            elif (y == 2) and (x in [0, 2, 6, 8, 9]):
                valor = -100
                screen.blit(penalidade, (x * RECT_WIDTH, y * RECT_HEIGHT))

            elif (y == 3) and (x in [1, 8]):
                valor = -100
                screen.blit(penalidade, (x * RECT_WIDTH, y * RECT_HEIGHT))

            elif (y == 5) and (x == 6):
                valor = -100
                screen.blit(penalidade, (x * RECT_WIDTH, y * RECT_HEIGHT))

            elif (y == 8) and (x == 6):
                valor = -100
                screen.blit(penalidade, (x * RECT_WIDTH, y * RECT_HEIGHT))

            elif x == 4 and y == 9:
                cor = RED



            if [y, x] == agente.pos:
                screen.blit(personagem, (x * RECT_WIDTH, y * RECT_HEIGHT))


            pygame.draw.rect(screen, BLACK, rect, 1)

            try:
                if valor not in [-100, 100, -1000]:
                    valor = qlearning.getMaximoPosicao([y, x])

                if valor != -1000:
                    texto = font.render(f"{valor:.2f}", True, BLACK)
                    texto_rect =  texto.get_rect(center=rect.center)
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            if dx != 0 or dy != 0:  # evita o centro
                                borda_surface = font.render(f"{valor:.2f}", True, WHITE)
                                borda_rect = texto_rect.copy()
                                borda_rect.x += dx
                                borda_rect.y += dy
                                screen.blit(borda_surface, borda_rect)


                    screen.blit(texto, texto_rect)
            except:
                pass

    pygame.display.flip()
    clock.tick(20)

for i in range(episodios):
    posicaoAtual = mp.resetPosicao()
    for passos in range(larguraMapa * alturaMapa):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        desenhar_mapa(ql, mp, agt)
        acao = ql.getAcao(posicaoAtual)
        novaPosicao, recompensa, final = mp.andar(acao)
        ql.atualizaQtable(posicaoAtual, acao, novaPosicao, recompensa, final)
        posicaoAtual = novaPosicao



        if final:
            break

pygame.quit()
ql.printQTable()