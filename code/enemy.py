from pathlib import Path
import random
import pygame
import math
from gobject import GameObject


# 敵機類別，用player的做模板
class Enemy(GameObject):

    # 建構式
    def __init__(self, xy=None, playground=None, sensitivity=1):
        GameObject.__init__(self, playground)
        if xy is None:
            self._y = -100
            self._x = random.randint(10, playground[0] - 100)
        else:
            self._x = xy[0]  # 座標屬性
            self._y = xy[1]  #

        # 設定邊界
        self._objectBound = (10, self._playground[0] - 100, -100, self._playground[1])  # 右, 左, 上, 下
        self._moveScale = 0.1 * sensitivity
        if random.random() > 0.5:
            self._slop = 0.5    # 飛機是斜斜的移動，所以要設定斜率
        else:
            self._slop = -0.5
        self._moveScaleY = math.cos(self._slop * math.pi / 2) * self._moveScale
        self._moveScaleX = math.sin(self._slop * math.pi / 2) * self._moveScale

        __parent_path = Path(__file__).parents[1]
        self.__enemy_path = __parent_path / 'res' / 'ufo.png'
        self._image = pygame.image.load(self.__enemy_path)
        self._center = self._x + self._image.get_rect().w / 2, self._y + self._image.get_rect().h / 2
        self._radius = 0.3 * math.hypot(self._image.get_rect().w, self._image.get_rect().h)

        self.to_the_bottom()

    def to_the_bottom(self):
        self._changeY = self._moveScaleY
        self._changeX = self._moveScaleX

    def update(self):
        self._x += self._changeX
        self._y += self._changeY

        if random.random() < 0.001:
            self._slop = -self._slop
            self._changeX = math.sin(self._slop * math.pi / 2) * self._moveScale
        if self._x > self._objectBound[1]:
            self._x = self._objectBound[1]
            self._slop = -self._slop
            self._changeX = math.sin(self._slop * math.pi / 2) * self._moveScale
        if self._x < self._objectBound[0]:
            self._x = self._objectBound[0]
            self._slop = -self._slop
            self._changeX = math.sin(self._slop * math.pi / 2) * self._moveScale
        if self._y > self._objectBound[3]:
            self._y = self._objectBound[3]
            # 超過螢幕範圍，標記為失效
            self._available = False
        if self._y < self._objectBound[2]:
            self._y = self._objectBound[2]

        self._center = self._x + self._image.get_rect().w / 2, self._y + self._image.get_rect().h / 2
