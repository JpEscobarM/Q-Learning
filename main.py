from random import random, choice, Random
import pygame

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

    def getPosicaoAgente(self):
        return self.agente.pos.copy()
    def renderiza(self):
        for i in range(linhas):
            for j in range(colunas):
                if i >= 5 and 0 <= j < 4:
                    continue
                elif i >= 5 and 8 <= j < 12:
                    continue

                rect = pygame.Rect(
                    set_x + j * tamanhoBloco,
                    set_y + i * tamanhoBloco,
                    tamanhoBloco,
                    tamanhoBloco
                )

                if (i == 4) and (j == 11):
                    pygame.draw.rect(tela, "green", rect)
                elif (i == 0) and (j in [4, 11]):
                    pygame.draw.rect(tela, "purple", rect)
                elif (i == 1) and (j in [1, 11]):
                    pygame.draw.rect(tela, "purple", rect)
                elif (i == 2) and (j in [0, 2, 6, 8, 9]):
                    pygame.draw.rect(tela, "purple", rect)
                elif (i == 3) and (j in [1, 8]):
                    pygame.draw.rect(tela, "purple", rect)
                elif (i == 5) and (j == 6):
                    pygame.draw.rect(tela, "purple", rect)
                elif (i == 8) and (j == 6):
                    pygame.draw.rect(tela, "purple", rect)
                else:
                    pygame.draw.rect(tela, "white", rect, width=1)

        posAgente = MAPA.getPosicaoAgente()
        rectAgente = pygame.Rect(
            set_x + posAgente[1] * tamanhoBloco,
            set_y + posAgente[0] * tamanhoBloco,
            tamanhoBloco,
            tamanhoBloco
        )
        pygame.draw.rect(tela, "red", rectAgente)
        pygame.display.flip()
        clock.tick(5)


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

AGENTE = Agente()
alturaMapa = 10
larguraMapa = 12

MAPA = Mapa(AGENTE, larguraMapa, alturaMapa, 0)

QLEARNING = QLearning(epsilon=0.3, alpha=0.2, valorInicial=0, w=larguraMapa, h=alturaMapa)

MAPA.resetPosicao()
episodios = 1000

# episodios = 1000
#
# for i in range(episodios):
#     posicaoAtual = mp.resetPosicao()
#     for passos in range(larguraMapa * alturaMapa):#passos = h*w ou seja, o maximo de passos que o agente pode dar por episodio
#         acao = ql.getAcao(posicaoAtual)
#         novaPosicao, recompensa, final = mp.andar(acao)
#         ql.atualizaQtable(posicaoAtual,acao,novaPosicao,recompensa,final)
#         posicaoAtual = novaPosicao
#         if final:
#             break
# ql.printQTable()

#PYGAME

pygame.init()
tela = pygame.display.set_mode((1000, 720))
clock = pygame.time.Clock()
running = True

#JOGADOR: ???

linhas, colunas = alturaMapa,larguraMapa
tamanhoBloco = 50

totalLarguraMatriz = colunas * tamanhoBloco
totalAlturaMatriz = linhas * tamanhoBloco


set_x = (tela.get_width()  - totalLarguraMatriz) // 2
set_y = (tela.get_height() - totalAlturaMatriz) // 2



#RODA A TELA:
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False



    #QL:
    for i in range(episodios):
        posicaoAtual = MAPA.resetPosicao()
        for passos in range(larguraMapa * alturaMapa):#passos = h*w ou seja, o maximo de passos que o agente pode dar por episodio
            acao = QLEARNING.getAcao(posicaoAtual)
            novaPosicao, recompensa, final = MAPA.andar(acao)
            QLEARNING.atualizaQtable(posicaoAtual,acao,novaPosicao,recompensa,final)
            posicaoAtual = novaPosicao

            tela.fill("black")
            for i in range(linhas):
                for j in range(colunas):
                    if i >= 5 and 0 <= j < 4:
                        continue
                    elif i >= 5 and 8 <= j < 12:
                        continue

                    rect = pygame.Rect(
                        set_x + j * tamanhoBloco,
                        set_y + i * tamanhoBloco,
                        tamanhoBloco,
                        tamanhoBloco
                    )


                    if (i == 4) and (j == 11):
                        pygame.draw.rect(tela, "green", rect)
                    elif (i == 0) and (j in [4, 11]):
                        pygame.draw.rect(tela, "purple", rect)
                    elif (i == 1) and (j in [1, 11]):
                        pygame.draw.rect(tela, "purple", rect)
                    elif (i == 2) and (j in [0, 2, 6, 8, 9]):
                        pygame.draw.rect(tela, "purple", rect)
                    elif (i == 3) and (j in [1, 8]):
                        pygame.draw.rect(tela, "purple", rect)
                    elif (i == 5) and (j == 6):
                        pygame.draw.rect(tela, "purple", rect)
                    elif (i == 8) and (j == 6):
                        pygame.draw.rect(tela, "purple", rect)
                    else:
                        pygame.draw.rect(tela, "white", rect, width=1)

            posAgente = MAPA.getPosicaoAgente()
            rectAgente = pygame.Rect(
                set_x + posAgente[1] * tamanhoBloco,
                set_y + posAgente[0] * tamanhoBloco,
                tamanhoBloco,
                tamanhoBloco
            )
            pygame.draw.rect(tela, "red", rectAgente)
            pygame.display.flip()
            clock.tick(100)

            if final:
                break



pygame.quit()
QLEARNING.printQTable()
