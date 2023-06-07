import cv2
import os
import time
import numpy as np
import snakes.plugins
snakes.plugins.load("gv", "snakes.nets", "nets")
from nets import *

########## Variáveis
p = [] #matriz portas
t = [] #matriz lugares_X_transições
td = [] #matriz lugares_X_transições disparadas
lv = [0] #vetor lugares visitados
lugAnt = [0] #vetor lugar anterior ao lugar em que se está

class Variaveis():
    pass

var = Variaveis()
var.idLugar = 0
var.idLugarA = 0
var.qtdPortas = 0
var.idPe = 'txy'
var.i = 0
var.on = 1

def cria_matriz(n_linhas, n_colunas, valor):	    
    matriz = [] # lista vazia
    for i in range(n_linhas):
        # cria a linha i
        linha = [] # lista vazia
        for j in range(n_colunas):
            linha.append(valor)
        # coloca linha na matriz
        matriz.append(linha)

    return matriz

#Definições iniciais
t = cria_matriz(var.idLugar,var.qtdPortas,0)
td = cria_matriz(var.idLugar,var.qtdPortas,0)
rp = PetriNet("RP_Mapa")
rp.add_place(Place("p%s"%var.idLugar, [dot]))
t.append([]) #insere linha referente ao lugar inicial p0
td.append([]) #insere linha referente ao lugar inicial p0

while(1):

    #Identificação de cada porta no lugar P_x atual
    var.qtdPortas = int(input("Digite a quantidade de porta(s) do lugar atual: "))
    print ("Existe(m) %d Porta(s) no Lugar %d: " %(var.qtdPortas, var.idLugarA))

    p.clear()
    for i in range(var.qtdPortas):
        p.append(str(input("Digite o id da porta %d do lugar atual P%d: " %(i+1, var.idLugarA))))       
    print("p: ", p)
    for i in range(len(p)):
        if p[i] != var.idPe:
            var.idLugar += 1
            t.append([])
            td.append([])
            
            #Cria um lugar novo para cada porta
            rp.add_place(Place("p%s"%var.idLugar,))
            lugAnt.append(var.idLugarA)

            #Cria uma transição para cada porta   
            rp.add_transition(Transition("t%s%s"%(var.idLugarA,var.idLugar)))
            rp.add_input("p%s"%var.idLugarA,"t%s%s"%(var.idLugarA,var.idLugar), Value(1))#Arco de entrada 
            rp.add_output("p%s"%var.idLugar,"t%s%s"%(var.idLugarA,var.idLugar), Value(1))#Arco de saída

            #Armazena as transições criadas na linha[lugar atual] de uma matriz t[]
            t[var.idLugarA].insert(i,'t%s%s'%(var.idLugarA,var.idLugar))
        else:

            #Primeira transição, ou seja, porta que volta para o lugar anterior   
            print("Lugar Anterior: ", lugAnt)
            rp.add_transition(Transition("t%s%s"%(var.idLugarA,lugAnt[var.idLugarA])))
            rp.add_input("p%s"%var.idLugarA,"t%s%s"%(var.idLugarA,lugAnt[var.idLugarA]), Value(1))#Arco de entrada 
            rp.add_output("p%s"%lugAnt[var.idLugarA],"t%s%s"%(var.idLugarA,lugAnt[var.idLugarA]), Value(1))#Arco de saída            

            #Armazena a transição que volta para o lugar anterior na linha[lugar atual] de t[]
            t[var.idLugarA].insert(0,'t%s%s'%(var.idLugarA,lugAnt[var.idLugarA]))

    rp.draw("Mapa.png")
    imagem = cv2.imread("Mapa.png")
    cv2.imshow("Mapa.png", imagem)
    cv2.waitKey()                                #mantem janela aberta e código em pausa até que uma tecla seja pressionada
    #cv2.destroyAllWindows()                     #fecha janela

    while(var.idLugarA in lv):
        if len(t[var.idLugarA]) == 1 or len(t[var.idLugarA]) - len(td[var.idLugarA]) == 1:

            #Dispara t[var.idLugarA] existente
            var.c = t[var.idLugarA][0]
            print("Lugar p%s MAPEADO. Dispara transição %s" %(var.idLugarA, t[var.idLugarA][0]))
        else:

            #Dispara próxima transição da linha atual
            for i in range(len(t[var.idLugarA])):
                if i != 0:
                    if t[var.idLugarA][i] in td[var.idLugarA]:
                        pass
                    else:
                        var.c = t[var.idLugarA][i]
                        print("Dispara transição: ", t[var.idLugarA][i])
                        #rp.transition(t[var.idLugarA][i]).modes()
                        #print (rp.transition(t[var.idLugarA][i]).modes())
                        #rp.transition(t[var.idLugarA][i]).fire([])
                        #rp.place("p%s"%var.idLugar,).tokens
                        break
                    
        #Aualiza td, idPe e var.idLugarA
        td[var.idLugarA].append(var.c)
        var.idPe = str("t%s%s" %(var.c[2],var.c[1]))
        var.idLugarA = int(var.c[2])
        print ("idPe: %s. Lugar Atual: p%s. Matriz t: %s e td: %s" %(var.idPe, var.idLugarA, t, td))

        if var.idLugarA in lv:
            if var.idLugarA == 0:
                if len(td[var.idLugarA]) == len(t[var.idLugarA]):
                    rp.draw("Mapa.png")
                    Mapa = cv2.imread("Mapa.png")
                    cv2.imshow("Mapa.png", Mapa)
                    print("AMBIENTE MAPEADO")
                    break
        else:

            #Atualiza lv (lugares já visitados)
            lv.append(var.idLugarA)
            print ("lv: ", lv)
            break
