#!/usr/bin/python

from __future__ import division
import numpy

nq = 20
nq1 = nq - 1
nq2 = nq - 2
nq3 = nq - 3
nq4 = nq - 4
mediaalter = int(nq / 5)

import itertools

alternativas = [0, 1, 2, 3, 4]
alt_dict = {}

for eliminadas in range(0, 4):
    ncombinacoes = 0
    sucesso = 0
    insucesso = 0
    for na in range(0, nq):
        for nb in range(0, nq1):
            for nc in range(0, nq2):
                for nd in range(0, nq3):
                    for ne in range(0, nq4):
                        gab = [na, nb, nc, nd, ne]
                        if sum(gab) != nq:
                            continue
                        # else:
                        # gab_std = gab/nq
                        gab_std = [x / nq for x in gab]
                        std = numpy.std(gab_std)

                        if std > 0.06:
                            continue
                        sgab = list(gab)
                        sgab.sort()
                        key = str(sgab)
                        if key in alternativas:
                            if alt_dict[key] != std:
                                print key, ", ", std

                        mink = min(gab)
                        maxk = max(gab)
                        mindif = abs(mediaalter - mink)
                        maxdif = abs(mediaalter - maxk)
                        difkey = 0
                        if (maxdif > mindif):
                            difkey = maxdif
                        else:
                            difkey = mindif

                        sdifkey = str(eliminadas)+"," + str(difkey)
                        #print "", std, ";", gab, ",", eliminadas
                        for L in range(eliminadas, 4):
                            for subset in itertools.combinations(alternativas, L):
                                # print "\t",(subset)
                                gab2 = []
                                for el in range(0, 5):
                                    if el not in subset:
                                        gab2.append(gab[el])

                                for r in range(0, len(gab2)):
                                    gab3 = list(gab2)
                                    gab3[r] -= 1
                                    indice = gab3.index(min(gab3))
                                    ncombinacoes += 1
                                    if sdifkey in alt_dict:
                                        values = alt_dict[sdifkey]
                                    else:
                                        values = [0,0]
                                        alt_dict.update({sdifkey: values})

                                    if indice == r:
                                        sucesso += 1
                                        values[0] += 1
                                    else:
                                        insucesso += 1
                                        values[1] += 1


                                    # extkey = str(eliminadas)+","+ str(difkey) +","+key
                                    # alt_dict.update({extkey:[std,sucesso/(sucesso+insucesso)]})

                                    # sucesso = 0
                                    # insucesso = 0

matrix = numpy.zeros((4, 20))
for key in alt_dict.keys():
    lkey = key.split(',')
    matrix[int(lkey[0])][int(lkey[1])] = alt_dict[key][0]/(alt_dict[key][0]+alt_dict[key][1])

print matrix

