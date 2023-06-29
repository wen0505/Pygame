# 遊戲物件類別
import math


class GameObject:
    # 初始化
    def __init__(self, playground=None):
        if playground is None:
            self._playground = [1000, 760]
        else:
            self._playground = playground

        # 移動範圍(左、右、上、下)
        self._objectBound = (0, self._playground[0], 0, self._playground[1])
        self._changeX = 0  # 座標改變量
        self._changeY = 0
        self._x = 0  # 貼圖位置(從視窗的左上角開始算，不是從中心點開始算)
        self._y = 0
        self._moveScale = 1  # 移動計量值
        self._hp = 1  # HP
        self._image = None
        self._available = True  # 有效物件
        self._center = None
        self._radius = None  # 碰撞半徑
        self._collided = False  # 是否產生碰撞

    # 解構子，目前沒用
    def __del__(self):      # 當物件要被砍掉之前，需要做的動作
        # 使用類別變數的時候，會用__class__這個變量來顯示class
        print(self.__class__.__name__, "is being automatically destroyed. Goodbye!")

    # Python提供的getter
    @property       # 因為有這行的前置處理所以def xy可以同名
    def xy(self):
        return [self._x, self._y]

    # 因為介面安全性的問題，只要會被外界使用到，都需要加setter和getter，setter和getter屬於對外的街口
    # Python提供的setter，setter前面都要加名字，這是python的規定
    # 一開始會執行try的程式碼，如果try的程式碼有錯誤，執行except，可以有很多的except，如果try的程式碼沒有錯誤，就會執行else
    @xy.setter
    def xy(self, xy):
        try:
            self._x, self._y = xy
            if self._x > self._objectBound[1]:
                self._x = self._objectBound[1]
            if self._x < self._objectBound[0]:
                self._x = self._objectBound[0]
            if self._y > self._objectBound[3]:
                self._y = self._objectBound[3]
            if self._y < self._objectBound[2]:
                self._y = self._objectBound[2]
        except ValueError:
            raise ValueError("Pass an iterable with two items")
        else:
            """ This will run only if no exception was raised """
            pass

    # Python提供的getter，getter對應property，這是python的規定
    @property
    def x(self):
        return self._x

    # Python提供的setter
    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = value

    def to_the_left(self):
        self._changeX = -self._moveScale

    def to_the_right(self):
        self._changeX = self._moveScale

    def to_the_bottom(self):
        self._changeY = self._moveScale

    def to_the_top(self):
        self._changeY = -self._moveScale

    def stop_x(self):
        self._changeX = 0

    def stop_y(self):
        self._changeY = 0

    def update(self):
        self._x += self._changeX
        self._y += self._changeY
        if self._x > self._objectBound[1]:
            self._x = self._objectBound[1]
        if self._x < self._objectBound[0]:
            self._x = self._objectBound[0]
        if self._y > self._objectBound[3]:
            self._y = self._objectBound[3]
        if self._y < self._objectBound[2]:
            self._y = self._objectBound[2]

    @property
    def image(self):
        return self._image

    @property
    def available(self):
        return self._available

    @available.setter
    def available(self, value):
        self._available = value

    @property
    def collided(self):
        return self._collided

    @collided.setter
    def collided(self, value):
        self._collided = value

    @property
    def center(self):
        return self._center

    @property
    def radius(self):
        return self._radius

    # 碰撞偵測的API
    def _collided_(self, enemy):
        distance = math.hypot(self._center[0] - enemy.center[0], self.center[1] - enemy.center[1])
        if distance < self._radius + enemy.radius:
            return True
        else:
            return False
