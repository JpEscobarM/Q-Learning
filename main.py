from random import random, choice, Random


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
    def __init__(self, epsilon=0.1, alpha=0.1, gamma=0.9, init=0, w=12, h=10, a=4):
        self.epsilon = epsilon #TAXA DE ALEATORIEDADE
        self.alpha = alpha #TAXA DE APRENDIZAGEM
        self.gamma = gamma #FATOR DE DESCONTO CONFORME ATUALIZA ESTADOS ANTERIRES
        self.larguraMapa = w
        self.alturaMapa = h
        self.a = a
        self.init = init
        self.criaQTable()

    def criaQTable(self):  # reinicia a Qtable com 0,0,0,0 (#up #right, #down #left)
        #formando uma matriz em "3D"
        self.qtable = [[[self.init] * self.a for j in range(self.larguraMapa)] for i in range(self.alturaMapa)]

    def printQTable(self):# self.qtable[i][j][X] i,j = posicao no mapa | X = valor da ação escolhida
        print("Pos   |   Up   |  Right |  Down  |  Left  |")
        for i in range(self.alturaMapa):
            for j in range(self.larguraMapa):
                print("{:>2},{:<2} | {:>6} | {:>6} | {:>6} | {:>6} |".format(
                    i, j,
                    self.qtable[i][j][0],
                    self.qtable[i][j][1],
                    self.qtable[i][j][2],
                    self.qtable[i][j][3]
                ))

agt = Agente()
mp = Mapa(agt,12,10,0)

mp.resetPosicao()

ql = QLearning()
ql.printQTable()