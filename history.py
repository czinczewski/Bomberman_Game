from xml.dom.minidom import *
import objects


class Writer:
    def __init__(self):
        self.doc = Document()
        self.root = self.doc.createElement("Game")
        self.doc.appendChild(self.root)

    def auto_save(self, bots, bombs):
        nowy_stan = self.doc.createElement("stan")

        for i in range(len(bots)):
            # print("stan bota")
            stan_bota = self.doc.createElement("bot")
            stan_bota.setAttribute("index", str(i))

            wspX = self.doc.createElement("X")
            wspY = self.doc.createElement("Y")

            X = str(bots[i].get_x())
            Y = str(bots[i].get_y())

            wspX.appendChild(self.doc.createTextNode(X))
            wspY.appendChild(self.doc.createTextNode(Y))

            stan_bota.appendChild(wspX)
            stan_bota.appendChild(wspY)
            nowy_stan.appendChild(stan_bota)

        for i in range(bombs.counter):
            # print("stan bomby")
            stan_bomby = self.doc.createElement("bomb")
            stan_bomby.setAttribute("index", str(i))

            wspX = self.doc.createElement("X")
            wspY = self.doc.createElement("Y")
            zasieg = self.doc.createElement("zasieg")

            X = str(bombs.get_x(i))
            Y = str(bombs.get_y(i))
            Z = str(bombs.get_field(i))

            wspX.appendChild(self.doc.createTextNode(X))
            wspY.appendChild(self.doc.createTextNode(Y))
            zasieg.appendChild(self.doc.createTextNode(Z))

            stan_bomby.appendChild(wspX)
            stan_bomby.appendChild(wspY)
            stan_bomby.appendChild(zasieg)

            nowy_stan.appendChild(stan_bomby)

        self.root.appendChild(nowy_stan)

    def save(self):
        self.doc.writexml(open('data.xml', 'w'), indent="  ", addindent="  ", newl='\n')
        self.doc.unlink()

