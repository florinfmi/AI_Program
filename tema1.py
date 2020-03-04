import copy
import os
# import psutil
import time


class NodParcurgere:
    def __init__(self, id, info, parinte):
        self.id = id  # este indicele din vectorul de noduri
        self.info = info
        self.parinte = parinte  # parintele din arborele de parcurgere

    def obtineDrum(self):
        l = [self.info]
        nod = self
        while nod.parinte is not None:
            l.insert(0, nod.parinte.info)
            nod = nod.parinte
        return l

    def afisDrum(self):
        l = self.obtineDrum()
        str=""+("->").join(l)
        return str

    def contineInDrum(self, infoNodNou):
        nodDrum = self
        while nodDrum is not None:
            if (infoNodNou == nodDrum.info):
                return True
            nodDrum = nodDrum.parinte
        return False

    def inScopuri(self):
        curent = self.info
        cuv = curent.split()
        if cuv[0][1] == scopuri[0] and cuv[1][0] == scopuri[1]:
            return True
        else:
            return False

    def __repr__(self):
        sir = ""
        sir += self.info + "("
        sir += "id = {}, ".format(self.id)
        sir += "drum="
        drum = self.obtineDrum()
        sir += ("->").join(drum)
        sir += ")"
        return (sir)


class Graph:  # graful problemei
    def __init__(self, noduri, matrice, start, scopuri):
        self.noduri = noduri
        self.matrice = matrice
        self.nrNoduri = len(matrice)
        self.start = start
        self.scopuri = scopuri

    def indiceNod(self, n):
        return self.noduri.index(n)

    # va genera succesorii sub forma de noduri in arborele de parcurgere
    def genereazaSuccesori(self, nodCurent):
        listaSuccesori = []
        # for i in range(self.nrNoduri):
        #     if self.matrice[nodCurent.id][i] == 1 and not nodCurent.contineInDrum(self.noduri[i]):
        #         nodNou = NodParcurgere(i, self.noduri[i], nodCurent)
        #         listaSuccesori.append(nodNou)
        # return listaSuccesori
        for i in self.matrice[nodCurent.id]:
            if not nodCurent.contineInDrum(i):
                nodNou = NodParcurgere(self.noduri.index(i),i,nodCurent)
                stari[self.noduri.index(i)] = stari[self.noduri.index(i)]-1;
                listaSuccesori.append(nodNou)
        return listaSuccesori


    def __repr__(self):
        sir = ""
        for (k, v) in self.__dict__.items():
            sir += "{} = {}\n".format(k, v)
        return (sir)


##############################################################################################
#                                 Initializare problema                                      #
##############################################################################################

# pozitia i din vectorul de noduri da si numarul liniei/coloanei corespunzatoare din matricea de adiacenta
# noduri = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
#
# m = [
#     [0, 1, 0, 1, 1, 0, 0, 0, 0, 0],
#     [1, 0, 1, 0, 0, 1, 0, 0, 0, 0],
#     [0, 1, 0, 0, 0, 1, 0, 1, 0, 0],
#     [1, 0, 0, 0, 0, 0, 1, 0, 0, 0],
#     [1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
#     [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
#     [0, 0, 1, 0, 1, 0, 0, 0, 1, 1],
#     [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
# ]
#citire date
inp = open("inp1","r")
outp = open("outp1","w")

scopuri = []

linie = inp.readline()
ls = linie.split()

for i in range (0,len(ls)-2):
    scopuri.append(ls[i])

start = ls[2] + " " +ls[3]

print(start, " si ", scopuri)

stari =[]
noduri = []
matrice = []


while linie:
    linie = inp.readline()
    if linie:
        ls = linie.split()
        if ls[2] == 'liber':
            stari.append(1)
        elif ls[2] =='ocupat':
            stari.append(2)
        else:
            stari.append(3)
        noduri.append(ls[0] +' ' + ls[1])
        le = [ls[x] + ' ' + ls[x+1] for x in range(3, len(ls) - 1, 2)]
        matrice.append(le)

stari[0]=stari[0]-1

print(stari, '\n')

gr = Graph(noduri, matrice, start, scopuri)


#### algoritm BF
# presupunem ca vrem mai multe solutii (un numar fix)
# daca vrem doar o solutie, renuntam la variabila nrSolutiiCautate
# si doar oprim algoritsmul la afisarea primei solutii
nrSolutiiCautate = 4
continua=True
maxMem=0

# def calcMaxMem():
# 	global maxMem
# 	process = psutil.Process(os.getpid())
# 	#memCurenta=process.memory_percent()
# 	memCurenta=process.memory_info()[0]
# 	if maxMem<memCurenta:
# 		maxMem=memCurenta


def breadth_first(gr):
    global nrSolutiiCautate  # punem global ca sa putem sa folosim variabile globale
    # putem sa folosim var globale fara global daca nu o modificam
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    c = [NodParcurgere(gr.noduri.index(gr.start), gr.start, None)]
    continua = True  # variabila pe care o setez la false cand consider ca s-au afisat suficiente solutii
    while (len(c) > 0 and continua):
        nodCurent = c.pop(0)

        if nodCurent.inScopuri() is True:
            outp.write(nodCurent.afisDrum()+'\n')

            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                continua = False
        if stari[nodCurent.id] > 0:
            continue

        lSuccesori = gr.genereazaSuccesori(nodCurent)
        c.extend(lSuccesori)

outp.write('BREADTH FIRST:'+'\n')
t1=time.time()
breadth_first(gr)

outp.write('\n')

t2=time.time()
milis=round(1000*(t2-t1))
print("Memorie maxim folosita: {}. Timp: {}".format(maxMem, milis))





def depth_first_iterative_deepening(gr, adancimeMax):
    # vom simula o stiva prin relatia de parinte a nodului curent
    for i in range(1, adancimeMax):
        dfi(i, NodParcurgere(gr.noduri.index(start), start, None))


# e exact ca functia df din laboratorul anterior doar ca impunem si o lungime maxima a drumului

def dfi(adMaxCurenta, nodCurent):
    global nrSolutiiCautate, continua
    # descrestem adMaxCurenta pana la 0
    if adMaxCurenta <= 0 or not continua:  # ar trebui adMaxCurenta sa nu ajunga niciodata < 0
        return
    adMaxCurenta -= 1

    if nodCurent.inScopuri() is True:
        outp.write(nodCurent.afisDrum()+'\n')
        nrSolutiiCautate -= 1
        if nrSolutiiCautate == 0:
            continua = False
    lSuccesori = gr.genereazaSuccesori(nodCurent)
    for sc in lSuccesori:
        dfi(adMaxCurenta, sc)


adancimeMaxima = 5
t1=time.time()
outp.write('DEPTH FIRST ITERATIVE:'+'\n')
depth_first_iterative_deepening(gr, adancimeMaxima)
t2=time.time()
milis=round(1000*(t2-t1))

outp.write('\n')
print("Memorie maxim folosita: {}. Timp: {}".format(maxMem, milis))


def depth_first(gr):
    # vom simula o stiva prin relatia de parinte a nodului curent
    df(NodParcurgere(gr.noduri.index(start), start, None))


def df(nodCurent):
    global nrSolutiiCautate, continua
    if not continua:
        return
    if nodCurent.inScopuri() is True:
        outp.write(nodCurent.afisDrum() + '\n')
        nrSolutiiCautate -= 1
        if nrSolutiiCautate == 0:
            continua = False
    lSuccesori = gr.genereazaSuccesori(nodCurent)
    for sc in lSuccesori:
        df(sc)

t1=time.time()
outp.write('DEPTH FIRST:'+'\n')
depth_first(gr)
t2=time.time()
milis=round(1000*(t2-t1))

print("Memorie maxim folosita: {}. Timp: {}".format(maxMem, milis))


