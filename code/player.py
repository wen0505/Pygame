from pathlib import Path
from typing import Union
import pygame
from pygame.surface import Surface, SurfaceType
from gobject import GameObject
import math


# 玩家類別
class Player(GameObject):
    # 初始化，playground為必要參數
    def __init__(self, playground, xy=None, sensitivity=1):
        GameObject.__init__(self, playground)
        self._moveScale = 0.5 * sensitivity
        __parent_path = Path(__file__).parents[1]
        # 一個類別設定一個圖片
        self.__player_path = __parent_path / 'res' / 'airforce.png'
        self._image = pygame.image.load(self.__player_path)
        # 算出x,y的中心點位置，type 為 tuple
        self._center = self._x + self._image.get_rect().w / 2, self._y + self._image.get_rect().h / 2
        # 碰撞半徑，0.3為自己設定的碰撞偵測半徑，看起來比較逼真
        self._radius = 0.3 * math.hypot(self._image.get_rect().w, self._image.get_rect().h)
        if xy is None:
            self._x = (self._playground[0] - self._image.get_rect().w) / 2
            self._y = 3 * self._playground[1] / 4
        else:
            self._x = xy[0]  # 貼圖位置
            self._y = xy[1]  #
        # 左, 右, 上, 下，objectBound為飛機的移動範圍objectBound，保留10個pixels當邊界
        self._objectBound = (10, self._playground[0] - (self._image.get_rect().w + 10),
                             10, self._playground[1] - (self._image.get_rect().h + 10))
        self._hp = 3

    # 傳統getter撰寫方式，只是做為示範，實際上不使用
    def get_image(self) -> Union[Surface, SurfaceType]:
        return self._image

    def update(self):
        GameObject.update(self)
        self._center = self._x + self._image.get_rect().w / 2, self._y + self._image.get_rect().h / 2

    # 和敵人碰撞的情形，enemies(複數)是指所有的敵人
    def collision_detect(self, enemies):
        # m為敵人
        for m in enemies:
            if self._collided_(m):
                self._hp -= 1
                # 碰撞設為true
                self._collided = True
                if self._hp <= 0:
                    self._collided = True
                    self._available = False
                m.hp = -1
                m.collided = True
                m.available = False
