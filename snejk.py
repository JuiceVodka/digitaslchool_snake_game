#Python snake game z uporabo numpy

#imamo razred "Polje", ki hrani 2D numpy matriko
#imamo razred "Kaca", ki hrani koordinate vseh polij na katerih kaca je in smer v katero kaca gleda


#najdi nacin, da neprestano spremljas kaj uporabnik pise v konzolo in ce vnese w, a, s, d, 
#kaco obrni v pravo smer

#Razred Polje:

#Razred polje je glavni razred v katerem se igrica igra
#hrani razred kača, trenuten rezultat, 2d numpy matriko in koordinato polja, na katerem je hrana
#razred polje je tudi razred, ki spremlja kaj uporabnik piše v konzolo
#razred polje hrani igralno polje kot 2d numpy matriko; vse kordinate so koordinate v tej matriki
#razred polje skrbi za izris igralnega polja

#Razred Kača
#razred kača hrani vse koordinate na kateriih kača je, smer v katero kača gleda, in boolean ali je kača živa ali mrtva
#razred ima funkcijo, ki prejme smer in ko se funkcija izvede, kačo obrne v to smer (če jo lahko)
#razred ima tudi funkcijo, ki preveri, ali je kača pojedla samo sebe in ali se je kača zabila v steno
#razded ima funkcijo, ki celo kačo premakne za 1 polje v smer katero gleda -> POMEMBNO NARIŠI SI
#razred ima funkcijo, ki kačo podaljša za 1 polje če ta poje hrano (to ali poje hrano se lahko spremlja iz razreda polje)

#osveževanje zaslova;
#vse igrice imajo neko frekvenco osveževanja zaslona (FPS)
#sami določite frekvenco osveževanja, in med vsako osvežitvijo izvedite komando "cls" -> import os
#|_> za to obstajajo tudi druge opcije, če najdeš katero, jo lahko tudi uporabiš
#frekvenco osveževanje določimo s time.sleep() -> za to ne pozabi import time



#Kako se take stvari lotit?
#1. začnemo z razredom polje
#   -> najprej napišemo konstruktor (__init__) in določimo katere vse podatke bo razred potreboval (kaca, 2d numpy matrika itd)
#   -> napišemo funkcijo za izris (__str__) -> ne pozabi da je treba izrisati tudi kačo in hrano
#   -> dopolnimo funkcijo za izris, da kombiniramo s time.sleep in cls
#   -> najdemo način, da lahko sproti spremljamo vse kar uporabnik vnese v konzolo (kaj se piše na tipkovnici)

#2. nadaljujemo z razredom kača
#   -> najprej naredimo konstruktor
#   -> naredimo funkcijo, ki preveri čeje kača živa ali mrtva
#   -> naredimo funkcijo, ki prejme smer in kačo obrne v to smer, če je možno
#   -> naredimo funkcijo, ki kačo premakne za 1 polje v smer gledanja
#   -> naredimo funkcijo ki kačo podaljša za 1 polje -> to je v laho v isti funckiji kot premik, samo da ne zradiramo repa

#Dodatna naloga:
#naredi powerup. Powerup se pojavi na polju tako kot hrana, ampak ne vsakič 
#(vsakič ko se pojavi hrana, je neka šansa da se pojavi tudi powerup)
#powerup kači omogoča da se premika skozi stene


import numpy as np
import time
import os
from pynput import keyboard
import random


lst = np.zeros((20, 20))
#print(lst)

class Kaca:
    def __init__(self):
        self.koordinate = [(1, 1), (1, 2), (2, 2), (2, 3), (2, 4)]
        self.smer = "s"
        self.mrtva = False

    def obrni(self, smer):
        if smer not in "wasd":
            return

        if (smer == "w" and self.smer != "s") or (smer == "a" and self.smer != "d") or (smer == "s" and self.smer != "w") or (smer == "d" and self.smer != "a") :
            self.smer = smer
            

    def preveri_stanje(self):
        if self.koordinate[0][0] < 0 or self.koordinate[0][1] < 0 or self.koordinate[0][0] >= 15 or self.koordinate[0][1] >= 15:
            self.mrtva = True

        if self.koordinate[0] in self.koordinate[1:]:
            self.mrtva = True

    def premakni(self, hrana):
        nova_glava = (0, 0)
        if self.smer == "w":
            nova_glava = (self.koordinate[0][0]-1, self.koordinate[0][1])

        elif self.smer == "a":
            nova_glava = (self.koordinate[0][0], self.koordinate[0][1]-1)

        elif self.smer == "s":
            nova_glava = (self.koordinate[0][0]+1, self.koordinate[0][1])

        elif self.smer == "d":
            nova_glava = (self.koordinate[0][0], self.koordinate[0][1]+1)

        self.koordinate.insert(0, nova_glava)

        if nova_glava == hrana:
            while hrana in self.koordinate:
                hranax = random.randint(0, 14)
                hranay = random.randint(0, 14)
                hrana = (hranax, hranay)


        else:
            self.koordinate.pop(-1)

        return hrana




class Polje:
    def __init__(self):
        self.kaca = Kaca()
        self.igralno_polje = np.zeros((15, 15))
        self.hrana = (7, 7)

    def __str__(self):
        izris = ""
        kacina_polja = self.kaca.koordinate

        izris += (self.igralno_polje.shape[1]*2 +2) * "-" + "\n"
        for i in range(self.igralno_polje.shape[0]):
            izris += "|"
            for j in range(self.igralno_polje.shape[1]):
                trenutna_koordinata = (i, j)

                if trenutna_koordinata == self.hrana:
                    izris += "x "

                elif trenutna_koordinata in kacina_polja:
                    if trenutna_koordinata == kacina_polja[0]:
                        izris += "# "
                    else:
                        izris += "o "

                else:
                    izris += "  "
            izris += "|\n"
        izris += (self.igralno_polje.shape[1]*2 +2) * "-"
        #izris += f"    {self.kaca.smer}"
        izris += f"\n Current score: {len(kacina_polja)-5}"
        return izris

    def game_loop(self):
        while True:
            os.system("cls")
            print(self)

            self.kaca.preveri_stanje()
            if self.kaca.mrtva:
                break

            self.hrana = self.kaca.premakni(self.hrana)
            time.sleep(0.25)
        print("GAME OVER")

def zahec():
    print("ABCD")
    print("DEF")
    a = 5
    return a


polje = Polje()
#print(polje)

def on_press(key):
    #print("TEST")
    try:
        polje.kaca.obrni(key.char)
    except:
        pass

    #print(key.char)

listener = keyboard.Listener(on_press=on_press)
listener.start()
#listener.join()

polje.game_loop()

#dodaten komentar

#pygame + github