#!/usr/bin/python

from __future__ import division
import numpy

nq = 20 #1. Numero de questoes de uma prova
mediaalter = int(nq / 5) #2. Media de quantidade de questoes por alternativa

import itertools

alternativas = [0, 1, 2, 3, 4] #3. Alternativas possiveis: 0=A, 1=B, 2=C, 3=D, 4=E
alt_dict = {}

for eliminadas in range(0, 4): #4. Loop da quantidade de alternativas eliminadas
    for na in range(0, nq): #5. Todas as possiveis combinacoes de quantidade de questoes marcadas na letra A
        for nb in range(0, nq): #6. Todas as possiveis combinacoes de quantidade de questoes marcadas na letra B
            for nc in range(0, nq): #7. Todas as possiveis combinacoes de quantidade de questoes marcadas na letra C
                for nd in range(0, nq): #8. Todas as possiveis combinacoes de quantidade de questoes marcadas na letra D
                    for ne in range(0, nq): #9. Todas as possiveis combinacoes de quantidade de questoes marcadas na letra E
                        gab = [na, nb, nc, nd, ne]
                        if sum(gab) != nq: #10. somente combinacoes cuja soma seja igual a nq (numero de questoes da prova)
                            continue

                        gab_std = [x / nq for x in gab]
                        std = numpy.std(gab_std)  #11. Calculo do desvio padrao

                        if std > 0.06: #12. Elimina combinacoes absurdas. Exemplo: [1, 1, 1, 1, 16]
                            continue

                        mink = min(gab)
                        maxk = max(gab)
                        mindif = abs(mediaalter - mink)
                        maxdif = abs(mediaalter - maxk)
                        difkey = 0
                        if (maxdif > mindif): #13. Encontra a maior diferenca entre a media (nq/5) e os elementos da combinacao corrente
                            difkey = maxdif
                        else:
                            difkey = mindif

                        sdifkey = str(eliminadas)+"," + str(difkey) #14. Cria a chave do mapeamento de resultados composta pela quantidade de eliminadas e o elemento de maior diferenca

                        for subset in itertools.combinations(alternativas, eliminadas): #15. Loop para testar todas as combinacoes de eliminacao de alternativas
                            gab2 = []
                            for el in range(0, 5):
                                if el not in subset: #16. Testar somente alternativas que nao foram eliminadas
                                    gab2.append(gab[el])

                            for r in range(0, len(gab2)): #17. Para todas as alternativas testar: se diminuirmos 1 da sua contagem ela indica a resposta correta?
                                gab3 = list(gab2)
                                gab3[r] -= 1
                                indice_min = gab3.index(min(gab3))
                                if sdifkey in alt_dict: #18. Testa se a chave ja existe no mapeamento de resultados
                                    values = alt_dict[sdifkey]
                                else:
                                    values = [0,0]
                                    alt_dict.update({sdifkey: values})

                                if indice_min == r: #19. Se o indice do elemento minimo coincidir com o indice do elemento diminuido
                                    values[0] += 1 #20. Sucesso
                                else:
                                    values[1] += 1 #21. Insucesso

matrix = numpy.zeros((4, 20)) #22. As linhas contem a quantidade de alternativas eliminadas e as colunas contem o modulo da maior diferenca
for key in alt_dict.keys():
    lkey = key.split(',')
    sucesso = alt_dict[key][0]
    insucesso = alt_dict[key][1]
    matrix[int(lkey[0])][int(lkey[1])] = sucesso/(sucesso+insucesso) #23. Calcula a taxa de sucesso

print matrix
