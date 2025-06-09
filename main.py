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
        self.agente.pos = [4,3]
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
            print("#IF 1")
            self.agente.pos[0] = min(4, max(0, self.agente.pos[0]))
            self.agente.pos[1] = min(self.larguraMapa-1, max(0, self.agente.pos[1]))
        elif((5 <= self.agente.pos[0] ) and ( 4 <= self.agente.pos[1] <= 7)):
            print("#IF 2")
            self.agente.pos[0] = min(self.alturaMapa - 1, max(0, self.agente.pos[0]))
            self.agente.pos[1] = min(7, max(4, self.agente.pos[1]))
        elif(self.agente.pos[0]>=5 and  (7 < self.agente.pos[1] or self.agente.pos[1]<4) ):
            print("#IF 3")
            self.agente.pos[0] = min(self.alturaMapa-1, max(0, self.agente.pos[0]))
            self.agente.pos[1] = min(7, max(4, self.agente.pos[1]))
        elif (self.agente.pos[0] < 5):
            print("#IF 4")
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


# / def __init__(self, agente, width=12, height=10, tropecoValor = 0):

agt = Agente()
mp = Mapa(agt,12,10,0)

mp.resetPosicao()