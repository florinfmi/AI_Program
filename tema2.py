# import numpy as np
# import psutil da eroare
import copy

def costNou(m_zone, indice, m_culori):
    #####calcul cost mutare
    culoare=-2
    nr_p_curent=0
    for i in range(0,len(m_zone)):
        for j in range(0,len(m_zone[i])):
            if m_zone[i][j] == indice:
                nr_p_curent+=1
                culoare = m_culori[i][j]
    if culoare>=0:
        cm = 1+(nr_placute[culori.index(culoare)]- nr_p_curent)/nr_placute[culori.index(culoare)]
    else:
        cm = 0
    return cm

class NodParcurgere:
    graf = None  # static
    def __init__(self, m_culori evidentaZone, cost ,parinte):
        self.m_culori=m_culori
        self.evidentaZone=evidentaZone
        self.m_zone = m_zone
        self.cost=cost
        # self.g=g
        # self.h = self.calculeaza_h()
        # self.f = self.g + self.h
        self.parinte=parinte  # parintele din arborele de parcurgere

    # def calculeaza_h(self):
    #     return NodParcurgere.graf.lista_h[0]

    def actualizareEvidentaZone(self, evidentaZone, deSters):
        # scoate indicele zonei din evidenta
        x=deSters
        for i in range(0, len(evidentaZone)):
            for j in range(0, len(evidentaZone[i])):
                if evidentaZone[i][j] == x:
                    evidentaZone[i].pop(j)
        return evidentaZone


    def identificareZone(self, m_culori):
        m_indici = []
        index = 0
        for i in range(0, len(m_culori)):
            m_indici.append([])
            for j in range(0, len(m_culori[i])):
                if m_culori[i][j] == '#':
                    m_indici[i].append(-1)
                else:
                    m_indici[i].append(index)

                    if j < len(m_culori[i]) - 1:
                        if m_culori[i][j + 1] != m_culori[i][j]:
                            index += 1
                    else:
                        if i < len(m_culori) - 1:#daca e ultimul element de pe linie
                            if m_culori[i + 1][0] != m_culori[i][j]:
                                index += 1
        for i in range(1, len(m_culori)):
            for j in range(0, len(m_culori[i])):
                if m_indici[i][j] != -1:
                    if m_culori[i - 1][j] == m_culori[i][j] and m_indici[i - 1][j] != m_indici[i][j]:
                        m_indici[i][j] = m_indici[i - 1][j]
                        while (True):
                            if i == len(m_culori) - 1 and j == len(m_culori[i]) - 1: break
                            if j < len(m_culori[i]) - 1:
                                if m_culori[i][j + 1] == m_culori[i][j]:
                                    m_indici[i][j + 1] = m_indici[i][j]
                                    j += 1
                                else:
                                    break
                            else:
                                if i < len(m_culori) - 1:
                                    if m_culori[i + 1][0] == m_culori[i][j]:
                                        m_indici[i + 1][0] = m_indici[i][j]
                                        i += 1
                                        j = 0
                                    else:
                                        break

        #verific daca toate zonele au fost unite
        # zone = []
        # for i in range(0, len(culori)):
        #     zone.append([])
        # for i in range(0, len(zone)):
        #     zone[i].append(culori[i])
        # for i in range(0, len(m_indici)):
        #     for j in range(0, len(m_indici[i])):
        #         if m_indici[i][j] != -1:
        #             if m_indici[i][j] not in zone[culori.index(self.m_culori[i][j])]:
        #                 zone[culori.index(self.m_culori[i][j])].append(m_indici[i][j])
        #
        # for i in range(0,len(zone)):
        #     while len(zone[i]) > 2:
        #         for j in range(0,len(m_indici)):
        #             for k in range(0,len(m_indici[j])):
        #                 if m_indici[j][k] != -1:
        #                     if m_indici[j][k] != zone[i][1] and self.m_culori[j][k] == zone[i][0]:
        #                        if m_indici[j][k] in zone[i]:
        #                           zone[i].pop(zone[i].index(m_indici[j][k]))
        #                        m_indici[j][k]=zone[i][1]


        return m_indici

    def stergere( self, m_c, m_z, zonaDeSters):
        x = zonaDeSters
        #sterge toate placutele din zona aleasa
        for i in range(0, len(m_z)):
            for j in range(0, len(m_z[i])):
                if m_z[i][j] == x:
                    m_c[i][j] = '#'
        #muta jos
        for i in range(len(m_c) - 1, -1, -1):
            for j in range(0, len(m_c[i])):
                if m_c[i][j] != '#':
                    k = i + 1
                    while k != len(m_c) and m_c[k][j] == '#':
                        k += 1
                    if k - 1 != i:
                        m_c[k - 1][j] = m_c[i][j]
                        m_c[i][j] = '#'
        #muta la stanga
        for i in range(len(m_c) - 1, -1, -1):
            for j in range(0, len(m_c[i])):
                if m_c[i][j] != '#':
                    k = j - 1
                    while k >= 0 and m_c[i][k] == '#':
                        k -= 1
                    if k + 1 != j:
                        m_c[i][k + 1] = m_c[i][j]
                        m_c[i][j] = '#'
        return m_c


    def obtineDrum(self):
        l=[self.m_culori];
        nod=self
        while nod.parinte is not None:
            l.insert(0, nod.parinte.m_culori)
            nod=nod.parinte
        return l

    # def afisDrum(self):  # returneaza si lungimea drumului
    #     l=self.obtineDrum()
    #     print(("->").join(l))
    #     return len(l)


    def contineInDrum(self, infoNodNou):
        nodDrum=self
        while nodDrum is not None:
            if(infoNodNou == nodDrum.m_culori):
                return True
            nodDrum=nodDrum.parinte

        return False

    def __repr__(self):
        sir = ""
        l=[]
        l=self.obtineDrum()
        for k in l:
            for i in k:
                sir+='\n'
                for j in i:
                    sir+=' {}'.format(j)
        # sir += self.info + "("
        # sir += "id = {}, ".format(self.id)
        # sir += "drum="
        # drum = self.obtineDrum()
        # sir += ("->").join(drum)
        # sir += " cost:{})".format(self.cost)
        return (sir)


class Graph:  #  graful problemei
    def __init__(self, culori,scop):
        self.culori=culori
        self.scop=scop
        # self.lista_h = lista_h


    def indiceNod(self, n):
        return self.culori.index(n)

    # va genera succesorii sub forma de noduri in arborele de parcurgere
    def genereazaSuccesori(self, nodCurent):
        nodTemp=copy.deepcopy(nodCurent)
        listaSuccesori=[]
        for i in nodCurent.evidentaZone:
            for j in range(1, len(i)):
                #am facut incat functia de stergere returneaza matricea cu placute noua
                #iar __init__ apeleaza indentificareZone pt m_zone
                m_culori_noua=nodTemp.stergere(nodTemp.m_culori,nodTemp.m_zone,j)
                m_zone_noua=nodTemp.identificareZone(m_culori_noua)
                nodNou = NodParcurgere(m_culori_noua, m_zone_noua,nodTemp.actualizareEvidentaZone(nodTemp.evidentaZone,j),
                                       nodTemp.cost + costNou(m_zone_noua, j, m_culori_noua),nodCurent)
                if not nodCurent.contineInDrum(nodNou.m_culori):
                    listaSuccesori.append(nodNou)
        return listaSuccesori

    def __repr__(self):
        sir=""
        for (k,v) in self.__dict__.items() :
            sir+='{}  = {}\n'.format(k,v)
        return(sir )


##############################################################################################
#                                 Initializare problema                                      #
##############################################################################################


#creare m_init initiala
m_init=[]
inp=open('input1','r')
out=open('output','w')
linie = inp.readline()
l=[]
for i in range(0,len(linie)-1):
    l.append(linie[i])
m_init.append(l)
while linie:
    l=[]
    linie = inp.readline()
    if linie:
        for i in range(0, len(linie)):
          if linie[i] != '\n':
            l.append(linie[i])
        m_init.append(l)

print('m_init:')
for i in m_init:
    print(i)

#indexez fiecare culoare in vectorul de culori
culori=[]#vector cu indicii fiecarei culori ex: [a,b,c]
for i in m_init:
    for j in i:
        if j not in culori:
            culori.append(j)

#nr total placute
nr_placute=[]
while len(nr_placute) < len(culori):
    nr_placute.append(0)
for i in range (0,len(m_init)):
        for j in range (0,len(m_init[i])):
             nr_placute[culori.index(m_init[i][j])]+=1

#Verificare conditie incheiere rapida
for i in nr_placute:
    if i<3:
        print('Grila invalida')#de gasit cum sa opresc programul
        exit()


#indentificare zone matrice initiala
grila_init=[]
nod=NodParcurgere(m_init,None,None,0,None)
grila_init=nod.identificareZone(m_init)
print('MATRICE ZONE:')
for i in grila_init:
    print(i)

evidentaZone=[]#matrice cu indicii zonelor fiecarei culori
#creez matrice cu litera culorii ca primul element al liniei
#in functie de indicele din vectorul de culori
#si zonele sale dupa
for i in range(0,len(culori)):
    evidentaZone.append([])
for i in range(0,len(evidentaZone)):
    evidentaZone[i].append(culori[i])
for i in range(0,len(grila_init)):
    for j in range (0,len(grila_init[i])):
        if grila_init[i][j] not in evidentaZone[culori.index(m_init[i][j])]:
            evidentaZone[culori.index(m_init[i][j])].append(grila_init[i][j])

print(evidentaZone)

# cost_mutari=[] #cost pentru fiecare zona
#sunt 0 la inceput deoarece n-a fost realizata nicio mutare
# for i in evidentaZone:
#     for j in range(1,len(i)):
#         cost_mutari.append(0)


#creare scop
scop=[]
for i in m_init:
    le = [ '#' for i in range(0,len(i))]
    scop.append(le)
print()
for i in scop:
    print(i)
print()

# mat = [
#     ['#','#','#','b'],
#     ['a','a','#','b'],
#     ['a','b','b','b'],
#     ['a','b','b','b']
# ]
# for i in mat:
#     print(i)
# print()


# vect_h=[1,1,1,1,1,1,1,1,1,0]
gr=Graph(culori,scop)

#### algoritm Uniform Cost Search
# presupunem ca vrem mai multe solutii (un numar fix)
# daca vrem doar o solutie, renuntam la variabila nrSolutiiCautate
# si doar oprim algoritmul la afisarea primei solutii
nrSolutiiCautate=1

def uniform_cost(gr):
    global nrSolutiiCautate
    c=[NodParcurgere(m_init, grila_init, evidentaZone,0, None)]
    continua=True # variabila pe care o setez la false cand consider ca s-au afisat suficiente solutii
    while(len(c)>0 and continua):
        nodCurent=c.pop(0)

        if nodCurent.m_culori == gr.scop:
            nodCurent.afisDrum()
            nrSolutiiCautate-=1
            if nrSolutiiCautate==0:
                continua=False
        lSuccesori=gr.genereazaSuccesori(nodCurent)
        for s in lSuccesori:
            i=0
            for i in range(len(c)):
                if c[i].cost>=s.cost:
                    break;
            c.insert(i,s)

uniform_cost(gr)

def cautare_drum(gr):
    global nrSolutiiCautate
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    c = [NodParcurgere(m_init,evidentaZone,0, None)]
    continua = True  # variabila pe care o setez la false cand consider ca s-au afisat suficiente solutii
    while (len(c) > 0 and continua):
        nodCurent = c.pop(0)

        if nodCurent.info in scop:
            out.write(nodCurent.obtineDrum())
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                continua = False
        lSuccesori = gr.genereazaSuccesori(nodCurent)
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(c)):
                # diferenta e ca ordonez dupa f
                if c[i].f >= s.f:
                    gasit_loc = True
                    break;
            if gasit_loc:
                c.insert(i, s)
            else:
                c.append(s)


#cautare_drum(gr)