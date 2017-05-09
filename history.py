from xml.dom.minidom import *
import objects


class Writer:
    def __init__(self):
        self.doc = Document()

        self.root = self.doc.createElement("Gra")
        self.doc.appendChild(self.root)

    def zapis_stanu(self, bots):
        nowy_stan = self.doc.createElement("stan")
        for i in range(len(bots)):
            stan_bota = self.doc.createElement("bot")
            stan_bota.setAttribute("index", i)
            wspX = self.doc.createElement("X")
            wspY = self.doc.createElement("Y")
            X = bots[i].get_x()
            Y = bots[i].get_y()
            X = str(X)
            Y = str(Y)
            wspX.appendChild(X)
            wspY.appendChild(Y)
            stan_bota.appendChild(wspX)
            stan_bota.appendChild(wspY)
            nowy_stan.appendChild(stan_bota)
        self.root.appendChild(nowy_stan)
