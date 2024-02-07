import cv2
import os
import time
import numpy as np
import snakes.pnml
import snakes.plugins
snakes.plugins.load("gv", "snakes.nets", "nets")
from nets import *

########## Variáveis
p = [] #matriz portas
t = [] #matriz lugares_X_transições
td = [] #matriz lugares_X_transições disparadas
lv = [0] #vetor lugares visitados
lc = [0] #vetor lugares criados
lugAnt = [0] #vetor lugar anterior ao lugar em que se está

class Variaveis():
    pass

var = Variaveis()
var.idLugar = 0
var.idLugarA = 0
var.qtdPortas = 0
var.idPe = 'txy'
var.x = 'A'

def cria_matriz(n_linhas, n_colunas, valor):	    
    matriz = [] # lista vazia
    for i in range(n_linhas):
        # cria a linha i
        linha = [] # lista vazia
        for j in range(n_colunas):
            linha.append(valor)
        # coloque linha na matriz
        matriz.append(linha)

    return matriz

#Definições iniciais
t = cria_matriz(var.idLugar,var.qtdPortas,0)
td = cria_matriz(var.idLugar,var.qtdPortas,0)
rp = PetriNet("RP_Mapa")
rp.add_place(Place("p%s"%var.idLugar,1))
t.append([]) #insere linha referente ao lugar inicial p0
td.append([]) #insere linha referente ao lugar inicial p0

while(1):

    #Identificação de cada porta no lugar P_x atual
    var.qtdPortas = int(input("Digite a quantidade de porta(s) do lugar atual: "))
    print ("Existe(m) %d Porta(s) no Lugar %d: " %(var.qtdPortas, var.idLugarA))

    p.clear()

    for i in range(var.qtdPortas):
        y = str(input("Digite o id da porta %d do lugar atual P%d: " %(i+1, var.idLugarA)))       

        if y in p: #verifica se há transições repetidas, ou seja, mais de uma porta ligando dois cômodos
            y = y + var.x
            var.x = chr(ord(var.x)+1)
        p.append(y)
    var.x = 'A'

    #Construção da RP    
    for i in range(len(p)):        
        pp = list(p[i])
        var.idLugar = round(float(pp[2])) #guarda índice do lugar de destino digitado pelo usuário
        pp.clear()

        if p[i] != var.idPe:
            if not var.idLugar in lc:
                #Cria um lugar novo para cada porta
                rp.add_place(Place("p%s"%var.idLugar,))
                lc.append(var.idLugar)
                lugAnt.append(var.idLugarA)

                if var.idLugarA > len(lugAnt):
                    for j in range(var.idLugarA - len(lugAnt)):
                        lugAnt.append([])
                lugAnt.pop(var.idLugar - 1)
                lugAnt.insert(var.idLugar - 1,var.idLugarA)

            #Cria uma transição para cada porta
            if len(p[i]) > 3: #Verifica se há transições cujo índice possui caracteres
                rp.add_transition(Transition("t%s%s%s"%(var.idLugarA,var.idLugar,p[i][3]), Expression('x>0')))
                rp.add_input("p%s"%var.idLugarA,"t%s%s%s"%(var.idLugarA,var.idLugar,p[i][3]), Variable('x'))#Arco de entrada 
                rp.add_output("p%s"%var.idLugar,"t%s%s%s"%(var.idLugarA,var.idLugar,p[i][3]), Expression('x*1'))#Arco de saída
            else:
                rp.add_transition(Transition("t%s%s"%(var.idLugarA,var.idLugar), Expression('x>0')))
                rp.add_input("p%s"%var.idLugarA,"t%s%s"%(var.idLugarA,var.idLugar), Variable('x'))#Arco de entrada 
                rp.add_output("p%s"%var.idLugar,"t%s%s"%(var.idLugarA,var.idLugar), Expression('x*1'))#Arco de saída    
            
            #Armazena as transições criadas na linha[lugar atual] de uma matriz t[]
            t[var.idLugarA].insert(i,'t%s%s'%(var.idLugarA,var.idLugar))

        if p[i] == var.idPe:
            lugAnt.append([])
            lugAnt.pop(var.idLugarA)
            lugAnt.insert(var.idLugarA,var.idLugar)
            
            for j in range(var.idLugarA+1):
                t.append([])
                td.append([])

            #Primeira transição é sempre equivalente a porta que volta para o lugar anterior   
            if len(p[i]) > 3:
                rp.add_transition(Transition("t%s%s%s"%(var.idLugarA,lugAnt[var.idLugarA],p[i][3]),Expression('x>0')))
                rp.add_input("p%s"%var.idLugarA,"t%s%s%s"%(var.idLugarA,lugAnt[var.idLugarA],p[i][3]), Variable('x'))#Arco de entrada 
                rp.add_output("p%s"%lugAnt[var.idLugarA],"t%s%s%s"%(var.idLugarA,lugAnt[var.idLugarA],p[i][3]), Expression('x*1'))#Arco de saída            
            else:
                rp.add_transition(Transition("t%s%s"%(var.idLugarA,lugAnt[var.idLugarA]),Expression('x>0')))
                rp.add_input("p%s"%var.idLugarA,"t%s%s"%(var.idLugarA,lugAnt[var.idLugarA]), Variable('x'))#Arco de entrada 
                rp.add_output("p%s"%lugAnt[var.idLugarA],"t%s%s"%(var.idLugarA,lugAnt[var.idLugarA]), Expression('x*1'))#Arco de saída            

            #Armazena a transição que volta para o lugar anterior na linha[lugar atual] de t[]
            if len(p[i]) > 3:
                t[var.idLugarA].insert(0,'t%s%s%s'%(var.idLugarA,lugAnt[var.idLugarA],p[i][3]))
            else:
                t[var.idLugarA].insert(0,'t%s%s'%(var.idLugarA,lugAnt[var.idLugarA]))

    rp.draw("Mapa.png")
    imagem = cv2.imread("Mapa.png")
    #cv2.imshow("Mapa.png", imagem)
    #cv2.waitKey()                                #mantém janela aberta e código em pausa até que uma tecla seja pressionada
    #cv2.destroyAllWindows()                      #fecha janela

    while(var.idLugarA in lv):
        if len(t[var.idLugarA]) == 1 or len(t[var.idLugarA]) - len(td[var.idLugarA]) == 1:

            #Dispara t[var.idLugarA] existente
            var.c = t[var.idLugarA][0]
            print("Lugar p%s MAPEADO. Dispara transição %s" %(var.idLugarA, t[var.idLugarA][0]))
            rp.transition("%s"%t[var.idLugarA][0]).fire(Substitution(x=1))
            rp.draw("Mapa.png")
            imagem = cv2.imread("Mapa.png")
            #cv2.imshow("Mapa.png", imagem)
            #cv2.waitKey()

        else:

            #Dispara próxima transição da linha atual
            for i in range(len(t[var.idLugarA])):
                if i != 0:
                    if t[var.idLugarA][i] in td[var.idLugarA]:
                        pass
                    else:
                        var.c = t[var.idLugarA][i]
                        print("Dispara transição: ", t[var.idLugarA][i])
                        rp.transition("%s"%t[var.idLugarA][i]).fire(Substitution(x=1))
                        rp.draw("Mapa.png")
                        imagem = cv2.imread("Mapa.png")
                        #cv2.imshow("Mapa.png", imagem)
                        #cv2.waitKey()
                        break
                    
        #Aualiza td, idPe e var.idLugarA
        td[var.idLugarA].append(var.c)
        var.idPe = str("t%s%s" %(var.c[2],var.c[1]))
        var.idLugarA = int(var.c[2])

        if var.idLugarA in lv:
            if var.idLugarA == 0:
                if len(td[var.idLugarA]) == len(t[var.idLugarA]):
                    rp.draw("Mapa.png")
                    #rp.draw("Mapa.svg")
                    modified_pnml = dumps(rp)
                    with open("MinhaRede3.pnml", "w") as new_pnml_file:
                        new_pnml_file.write(modified_pnml)
                    #s = StateGraph(rp)
                    #s.draw('graphviz-graph.png')#, landscape=False)
                    Mapa = cv2.imread("Mapa.png")
                    #cv2.imshow("Mapa.png", Mapa)
                    print("AMBIENTE MAPEADO")
                    break
        else:

            #Atualiza lv (lugares já visitados)
            lv.append(var.idLugarA)
            print ("lv: ", lv)
            break
