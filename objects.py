import numpy as np
import math
from PyQt5.QtCore import *
from PyQt5.QtGui import *


# -----------------------------------------------
class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y


# -----------------------------------------------
class PlayerSI(Position):
    def __init__(self, x, y, move):
        super().__init__(x, y)
        self.move = move

    def set_move(self, move):
        self.move = move

    def get_move(self):
        return self.move


# -----------------------------------------------
class Bomb:
    def __init__(self, q_window):
        self.q_window = q_window
        self.new_bomb = False
        self.x = []
        self.y = []
        self.field = []
        self.explode_time = 4
        self.bomb_speed = 1000 * self.explode_time
        self.bombs_timer_tab = []
        self.counter = 0

    def b_timer(self):
        new_timer = QBasicTimer()
        new_timer.start(self.bomb_speed, self.q_window)
        self.bombs_timer_tab.append(new_timer)

    def add_bomb(self, x, y, field):
        self.field.append(field)
        self.y.append(y)
        self.x.append(x)
        self.b_timer()

    def get_x(self, i):
        return self.x[i]

    def get_y(self, i):
        return self.y[i]

    def get_field(self, i):
        return self.field[i]

    def get_time(self, i):
        return self.bombs_timer_tab[i].isActive()

    def explosion(self):
        self.x = self.x[1:]
        self.y = self.y[1:]
        self.field = self.field[1:]
        self.bombs_timer_tab = self.bombs_timer_tab[1:]


# -----------------------------------------------
class Board:
    def __init__(self):
        map = 2 * np.ones((39, 39))  # puste pole
        y = 0
        while y < 39:
            x = 0
            while x < 39:
                if x == 0 or y == 0 or x == 38 or y == 38:
                    map[x, y] = 1  # niezniszczalna sciana

                if 0 < x < 4 and 0 < y < 4:  # puste pole
                    map[x, y] = 0

                if 0 < x < 4 and 34 < y < 38:  # puste pole
                    map[x, y] = 0

                if 34 < x < 38 and 0 < y < 4:  # puste pole
                    map[x, y] = 0

                if 34 < x < 38 and 34 < y < 38:  # puste pole
                    map[x, y] = 0

                if x%2 == 0 and y%2 == 0 and (3 < x < 35 or 3 < y < 35) and x != 38 and y != 38:
                    map[x, y] = 1

                x = x + 1
            y = y + 1
        self.board = map

    def get_cell(self, x, y):
        return self.board[x, y]

    def get_all(self):
        return self.board

    def set_cell(self, x, y, value):
        self.board[x, y] = value
        # 0 - puste pole
        # 1 - niezniszczalna sciana
        # 2 - zniszczalna sciana
        # 3 - bomba
        # 4 - pc
        # 5 - gracz
        # 6 - wybuch


# -----------------------------------------------
class DrawBorad:
    def __init__(self, height, width, q_window, margin, board):
        self.height = height
        self.width = width
        self.d_QWindow = q_window
        self.margin = margin
        self.x = 0
        self.y = 0
        self.board = board

    def draw(self):
        paint = QPainter()
        paint.begin(self.d_QWindow)
        paint.setRenderHint(QPainter.Antialiasing)

        paint.setBrush(Qt.white)
        clip_rect = QRect(0, 0, 585, 585)
        paint.drawRect(clip_rect)

        for i in range(39):
            for j in range(39):
                if self.board[j, i] == 1:
                    paint.setPen(Qt.white)
                    paint.setBrush(Qt.black)
                    paint.drawRect(self.x + 15 * i, self.y + 15 * j, self.x + 15, self.y + 15)
                elif self.board[j, i] == 2:
                    paint.setPen(Qt.white)
                    paint.setBrush(Qt.darkGray)
                    paint.drawRect(self.x + 15 * i, self.y + 15 * j, self.x + 15, self.y + 15)
                elif self.board[j, i] == 3:
                    paint.setPen(Qt.magenta)
                    paint.setBrush(Qt.magenta)
                    paint.drawRect(self.x + 15 * i, self.y + 15 * j, self.x + 15, self.y + 15)
                elif self.board[j, i] == 4:
                    paint.setPen(Qt.red)
                    paint.setBrush(Qt.darkRed)
                    paint.drawRect(self.x + 15 * i, self.y + 15 * j, self.x + 15, self.y + 15)
                elif self.board[j, i] == 4:
                    paint.setPen(Qt.black)
                    paint.setBrush(Qt.darkCyan)
                    paint.drawRect(self.x + 15 * i, self.y + 15 * j, self.x + 15, self.y + 15)
                elif self.board[j, i] == 5:
                    paint.setPen(Qt.white)
                    paint.setBrush(Qt.darkYellow)
                    paint.drawRect(self.x + 15 * i, self.y + 15 * j, self.x + 15, self.y + 15)
                elif self.board[j, i] == 6:
                    paint.setPen(Qt.red)
                    paint.setBrush(Qt.yellow)
                    paint.drawRect(self.x + 15 * i, self.y + 15 * j, self.x + 15, self.y + 15)
        paint.end()


class AutoPlayer:
    def sterowanie(self, bots, board, bomb):
        x = bots[0].get_x()
        y = bots[0].get_y()
        # print("SI, x:", x, "y:", y)

        x_min_distance = 40
        y_min_distance = 40
        min_distance = math.sqrt((40**2) + (40**2))
        target = 0

        #szukam najbliższego
        for i in range(1, 3):
            distance_x = abs(bots[i].get_x() - x)
            distance_y = abs(bots[i].get_y() - y)
            if min_distance > math.sqrt((distance_x**2) + (distance_y**2)):
                min_distance = math.sqrt((distance_x**2) + (distance_y**2))
                x_min_distance = distance_x
                y_min_distance = distance_y
                target = i

        # print("B: ", target, "X:", x, "Xb", bots[target].get_x(), "Y:", y, "Yb", bots[target].get_y(),
        #       "x(min): ", x_min_distance, " y(min): ", y_min_distance, "vec(min): ", min_distance)

        if bomb.counter > 0:  # uciekanie od postawionej bomby
            if board.get_cell(x - 1, y) == 3:
                print("Bomba w gore - Uciekam z x:", x, "y:", y)
                if board.get_cell(x + 1, y) == 0:
                    bots[0].set_move(1)
                    print("Ide w dol")
                elif board.get_cell(x, y - 1) == 0:
                    bots[0].set_move(4)
                    print("Ide w lewo")
                elif board.get_cell(x, y + 1) == 0:
                    bots[0].set_move(3)
                    print("Ide w prawo")
            elif board.get_cell(x + 1, y) == 3:
                print("Bomba w dol - Uciekam z x:", x, "y:", y)
                if board.get_cell(x - 1, y) == 0:
                    bots[0].set_move(2)
                    print("Ide w gore")
                elif board.get_cell(x, y - 1) == 0:
                    bots[0].set_move(4)
                    print("Ide w lewo")
                elif board.get_cell(x, y + 1) == 0:
                    bots[0].set_move(3)
                    print("Ide w prawo")
            elif board.get_cell(x, y - 1) == 3:
                print("Bomba na lewo - Uciekam z x:", x, "y:", y)
                if board.get_cell(x + 1, y) == 0:
                    bots[0].set_move(1)
                    print("Ide w dol")
                elif board.get_cell(x - 1, y) == 0:
                    bots[0].set_move(2)
                    print("Ide w gore")
                elif board.get_cell(x, y + 1) == 0:
                    bots[0].set_move(3)
                    print("Ide w prawo")
            elif board.get_cell(x, y + 1) == 3:
                print("Bomba na prawo - Uciekam z x:", x, "y:", y)
                if board.get_cell(x + 1, y) == 0:
                    bots[0].set_move(1)
                    print("Ide w dol")
                elif board.get_cell(x, y - 1) == 0:
                    bots[0].set_move(4)
                    print("Ide w lewo")
                elif board.get_cell(x - 1, y) == 0:
                    bots[0].set_move(2)
                    print("Ide w gore")
            else:
                print("Czekam na pozycji: x:", x, "y:", y)
        elif bomb.counter == 0:
            if x_min_distance <= y_min_distance:    #cel blizej w pionie
                print("Cel blizej w pionie")
                if y <= bots[target].get_y():
                    print("Cel na prawo")
                    if board.get_cell(x, y + 1) == 0:
                        bots[0].set_move(3)
                    elif board.get_cell(x, y + 1) == 1:
                        if x <= bots[target].get_x():   # dol
                            print("Gora")
                            if board.get_cell(x + 1, y) == 0:
                                bots[0].set_move(1)
                            elif board.get_cell(x + 1, y) == 2 or board.get_cell(x + 1, y) == 4:
                                bomb.add_bomb(x, y, 1)
                                board.set_cell(x, y, 3)
                                bomb.counter += 1
                                bomb.new_bomb = True
                        else:                           # gora
                            print("Dol")
                            if board.get_cell(x - 1, y) == 0:
                                bots[0].set_move(1)
                            elif board.get_cell(x - 1, y) == 2 or board.get_cell(x - 1, y) == 4:
                                bomb.add_bomb(x, y, 1)
                                board.set_cell(x, y, 3)
                                bomb.counter += 1
                                bomb.new_bomb = True
                    elif board.get_cell(x, y + 1) == 2 or board.get_cell(x, y + 1) == 4:
                        bomb.add_bomb(x, y, 1)
                        board.set_cell(x, y, 3)
                        bomb.counter += 1
                        bomb.new_bomb = True
                elif y > bots[target].get_y():
                    print("Cel na lewo")
                    if board.get_cell(x, y - 1) == 0:
                        bots[0].set_move(4)
                    elif board.get_cell(x, y - 1) == 1:
                        if x <= bots[target].get_x():   # dol
                            print("Dol")
                            if board.get_cell(x + 1, y) == 0:
                                bots[0].set_move(1)
                            elif board.get_cell(x + 1, y) == 2 or board.get_cell(x + 1, y) == 4:
                                bomb.add_bomb(x, y, 1)
                                board.set_cell(x, y, 3)
                                bomb.counter += 1
                                bomb.new_bomb = True
                        else:                           # gora
                            print("Gora")
                            if board.get_cell(x - 1, y) == 0:
                                bots[0].set_move(1)
                            elif board.get_cell(x - 1, y) == 2 or board.get_cell(x - 1, y) == 4:
                                bomb.add_bomb(x, y, 1)
                                board.set_cell(x, y, 3)
                                bomb.counter += 1
                                bomb.new_bomb = True
                    elif board.get_cell(x, y - 1) == 2 or board.get_cell(x, y - 1) == 4:
                        bomb.add_bomb(x, y, 1)
                        board.set_cell(x, y, 3)
                        bomb.counter += 1
                        bomb.new_bomb = True
            elif x_min_distance > y_min_distance:
                print("Cel blizej w poziomie")
                if x <= bots[target].get_x():
                    print("Cel w dol")
                    if board.get_cell(x + 1, y) == 0:
                        bots[0].set_move(1)
                    elif board.get_cell(x + 1, y) == 1:
                        if y <= bots[target].get_y():   # prawo
                            print("Prawo")
                            if board.get_cell(x, y + 1) == 0:
                                bots[0].set_move(3)
                            elif board.get_cell(x, y + 1) == 2 or board.get_cell(x, y + 1) == 4:
                                bomb.add_bomb(x, y, 1)
                                board.set_cell(x, y, 3)
                                bomb.counter += 1
                                bomb.new_bomb = True
                        else:                           # lewo
                            print("Lewo")
                            if board.get_cell(x, y - 1) == 0:
                                bots[0].set_move(4)
                            elif board.get_cell(x, y - 1) == 2 or board.get_cell(x, y - 1) == 4:
                                bomb.add_bomb(x, y, 1)
                                board.set_cell(x, y, 3)
                                bomb.counter += 1
                                bomb.new_bomb = True
                    elif board.get_cell(x + 1, y) == 2 or board.get_cell(x + 1, y) == 4:
                        bomb.add_bomb(x, y, 1)
                        board.set_cell(x, y, 3)
                        bomb.counter += 1
                        bomb.new_bomb = True
                elif x > bots[target].get_x():
                    print("Cel w gore")
                    if board.get_cell(x - 1, y) == 0:
                        bots[0].set_move(2)
                    elif board.get_cell(x - 1, y) == 1:
                        if y <= bots[target].get_y():  # prawo
                            print("Prawo")
                            if board.get_cell(x, y + 1) == 0:
                                bots[0].set_move(3)
                            elif board.get_cell(x, y + 1) == 2 or board.get_cell(x, y + 1) == 4:
                                bomb.add_bomb(x, y, 1)
                                board.set_cell(x, y, 3)
                                bomb.counter += 1
                                bomb.new_bomb = True
                        else:  # lewo
                            print("Lewo")
                            if board.get_cell(x, y - 1) == 0:
                                bots[0].set_move(4)
                            elif board.get_cell(x, y - 1) == 2 or board.get_cell(x, y - 1) == 4:
                                bomb.add_bomb(x, y, 1)
                                board.set_cell(x, y, 3)
                                bomb.counter += 1
                                bomb.new_bomb = True
                    elif board.get_cell(x - 1, y) == 2 or board.get_cell(x - 1, y) == 4:
                        bomb.add_bomb(x, y, 1)
                        board.set_cell(x, y, 3)
                        bomb.counter += 1
                        bomb.new_bomb = True

        return bots, board, bomb
