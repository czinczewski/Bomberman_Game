#bomberman na kwadratach - nie wolno używać pygame
#1. Mechanika -
    # implementacja planszy(zniszczalne i niezniszczalne elementy),
    # przeciwnicy(bez inteligencji(pion/poziom)), nie ma bomb
    # agent(bomby o roznym zakresie 1 - 5 pól)
    # rozgrywaka na konsoli
    # obsluga klawiatury
    # generowanie mapy
#2. GUI - Qt
#3. XML (plansza, zapis i odtworzenie historii) - przyzwoita jakość
#4. AI (silnik przechodzący gre)
# import skfuzzy as fuzzy
#5. TCP/IP (działanie synchorniczne)

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import objects
import sys
import random
import history


class Bomberman(QMainWindow):
    def __init__(self):
        super(Bomberman, self).__init__()

        self.speed = 1000
        self.board = objects.Board()
        self.bots = []

        self.bots.append(objects.PlayerSI(2, 2, 1))
        self.bots.append(objects.PlayerSI(2, 36, 1))
        self.bots.append(objects.PlayerSI(36, 2, 1))
        self.bots.append(objects.PlayerSI(36, 36, 1))

        self.board.set_cell(self.bots[0].get_x(), self.bots[0].get_y(), 5)
        for i in range(1, 4):
            self.board.set_cell(self.bots[i].get_x(), self.bots[i].get_y(), 4)

        self.timer = QBasicTimer()
        self.bomb = objects.Bomb(self)

        self.margin = 0
        self.drawer = objects.DrawBorad(self.height(), self.width(), self, self.margin, self.board.get_all())
        self.saver = history.Writer()
        self.initUi()

    def initUi(self):
        self.setGeometry(50, 50, 585, 585)
        self.resize(585 + 3 * self.margin, 585 + 3 * self.margin)
        self.setWindowTitle('Bomberman v3.0')
        self.start()
        self.show()

    def start(self):
        self.timer.start(self.speed, self)

    def explosion(self):
        x = self.bomb.get_x(0)
        y = self.bomb.get_y(0)
        for k in range(4):
            for i in range(self.bomb.get_field(0) + 1):
                x_vec = [x - i, x + i, x, x]
                y_vec = [y, y, y - i, y + i]
                val = self.board.get_cell(x_vec[k], y_vec[k])
                if val == 1:
                    break
                elif val == 2:
                    self.board.set_cell(x_vec[k], y_vec[k], 0)
                elif val == 4:
                    for j in range(len(self.bots)):
                        if self.bots[j].get_x() == x_vec[k] and self.bots[j].get_y() == y_vec[k]:
                            if j != len(self.bots) - 1:
                                new_bots = self.bots[:j] + self.bots[j + 1:]
                            else:
                                new_bots = self.bots[:j]
                            self.bots = new_bots
                            self.board.set_cell(x_vec[k], y_vec[k], 0)
                            break
                elif val == 5:
                    self.saver.save()
                    exit()
                    break

    def bot_direction(self):
        for i in range(1, len(self.bots)):
            direction = random.randint(1, 15)
            x = self.bots[i].get_x()
            y = self.bots[i].get_y()
            if self.board.get_cell(x + 1, y) == 0 and direction == 1:
                self.bots[i].set_move(direction)
            elif self.board.get_cell(x - 1, y) == 0 and direction == 2:
                self.bots[i].set_move(direction)
            elif self.board.get_cell(x, y + 1) == 0 and direction == 3:
                self.bots[i].set_move(direction)
            elif self.board.get_cell(x, y - 1) == 0 and direction == 4:
                self.bots[i].set_move(direction)

    def Move(self, i):
        x = self.bots[i].get_x()
        y = self.bots[i].get_y()
        move = self.bots[i].get_move()
        moved = False

        if i == 0:
            mark = 5
        else:
            mark = 4

        if move == 1:
            if self.board.get_cell(x + 1, y) == 0:
                self.board.set_cell(x, y, 0)
                self.board.set_cell(x + 1, y, mark)
                self.bots[i].set_x(x + 1)
                moved = True
            elif self.board.get_cell(x - 1, y) == 0:
                self.bots[i].set_move(2)
        elif move == 2:
            if self.board.get_cell(x - 1, y) == 0:
                self.board.set_cell(x, y, 0)
                self.board.set_cell(x - 1, y, mark)
                self.bots[i].set_x(x - 1)
                moved = True
            elif self.board.get_cell(x + 1, y) == 0:
                self.bots[i].set_move(1)
        elif move == 3:
            if self.board.get_cell(x, y + 1) == 0:
                self.board.set_cell(x, y, 0)
                self.board.set_cell(x, y + 1, mark)
                self.bots[i].set_y(y + 1)
                moved = True
            elif self.board.get_cell(x, y - 1) == 0:
                self.bots[i].set_move(4)
        elif move == 4:
            if self.board.get_cell(x, y - 1) == 0:
                self.board.set_cell(x, y, 0)
                self.board.set_cell(x, y - 1, mark)
                self.bots[i].set_y(y - 1)
                moved = True
            elif self.board.get_cell(x, y + 1) == 0:
                self.bots[i].set_move(3)

        if self.bomb.new_bomb and i == 0 and moved:
            self.board.set_cell(self.bomb.get_x(-1), self.bomb.get_y(-1), 3)
            self.bomb.new_bomb = False
            self.repaint()

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Left:
            self.bots[0].set_move(4)
            self.Move(0)
            self.repaint()
        elif key == Qt.Key_Right:
            self.bots[0].set_move(3)
            self.Move(0)
            self.repaint()
        elif key == Qt.Key_Down:
            self.bots[0].set_move(1)
            self.Move(0)
            self.repaint()
        elif key == Qt.Key_Up:
            self.bots[0].set_move(2)
            self.Move(0)
            self.repaint()
        elif key == Qt.Key_1:
            x_b = self.bots[0].get_x()
            y_b = self.bots[0].get_y()
            self.bomb.add_bomb(x_b, y_b, 1)
            self.board.set_cell(x_b, y_b, 3)
            self.bomb.counter += 1
            self.bomb.new_bomb = True
            self.repaint()
        elif key == Qt.Key_2:
            x_b = self.bots[0].get_x()
            y_b = self.bots[0].get_y()
            self.bomb.add_bomb(x_b, y_b, 2)
            self.board.set_cell(x_b, y_b, 3)
            self.bomb.counter += 1
            self.bomb.new_bomb = True
            self.repaint()
        elif key == Qt.Key_3:
            x_b = self.bots[0].get_x()
            y_b = self.bots[0].get_y()
            self.bomb.add_bomb(x_b, y_b, 3)
            self.board.set_cell(x_b, y_b, 3)
            self.bomb.counter += 1
            self.bomb.new_bomb = True
            self.repaint()
        elif key == Qt.Key_4:
            x_b = self.bots[0].get_x()
            y_b = self.bots[0].get_y()
            self.bomb.add_bomb(x_b, y_b, 4)
            self.board.set_cell(x_b, y_b, 3)
            self.bomb.counter += 1
            self.bomb.new_bomb = True
            self.repaint()
        elif key == Qt.Key_5:
            x_b = self.bots[0].get_x()
            y_b = self.bots[0].get_y()
            self.bomb.add_bomb(x_b, y_b, 5)
            self.board.set_cell(x_b, y_b, 3)
            self.bomb.counter += 1
            self.bomb.new_bomb = True
            self.repaint()
        elif key == Qt.Key_A: #tryb auto

            self.repaint()
        elif key == Qt.Key_S:  # odtwórz

            self.repaint()
        else:
            super(Bomberman, self).keyPressEvent(event)

    def timerEvent(self, event):
        self.saver.auto_save(self.bots, self.bomb)
        if self.bomb.counter > 0:
            if event.timerId() == self.bomb.bombs_timer_tab[0].timerId():
                self.board.set_cell(self.bomb.get_x(0), self.bomb.get_y(0), 6)
                self.repaint()
                self.board.set_cell(self.bomb.get_x(0), self.bomb.get_y(0), 0)
                self.explosion()
                self.bomb.counter -= 1
                self.bomb.explosion()

        if event.timerId() == self.timer.timerId():
            for i in range(1, len(self.bots)):
                self.bot_direction()
                self.Move(i)
            self.repaint()
        else:
            super(Bomberman, self).timerEvent(event)

    def paintEvent(self, event):
        self.drawer.draw()


# ----------------------------------------------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    bomberman = Bomberman()
    sys.exit(app.exec_())
