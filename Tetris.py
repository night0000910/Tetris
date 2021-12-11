import pygame
from pygame import mixer

import datetime
import random


pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Tetris")


# --------------------------------------- 変数 ------------------------------------------

BLOCK_WIDTH = 36.1 # 一つのブロックの幅
BLOCK_HEIGHT = 36.1 # 一つのブロックの高さ
TOP = 28.5 # 画面の上側の座標
BOTTOM = 570 # 画面の下側の座標
LEFT = 222 # 画面の左側の座標
RIGHT = 583 # 画面の右側の座標



# ------------------------------------ オブジェクト -----------------------------------------

class Timer:
    def __init__(self):
        self.first_time = datetime.datetime.now().timestamp()
        self.second_time = datetime.datetime.now().timestamp()
        self.time_interval = self.second_time - self.first_time
    
    def start(self):
        self.first_time = datetime.datetime.now().timestamp()
        self.second_time = datetime.datetime.now().timestamp()
    
    def measure(self, standard_time):
        self.second_time = datetime.datetime.now().timestamp()
        self.time_interval = self.second_time - self.first_time

        if self.time_interval >= standard_time:
            return True
        else:
            return False
    
    def tell_time(self):
        self.second_time = datetime.datetime.now().timestamp()
        self.time_interval = self.second_time - self.first_time
        return self.time_interval

class Background:
    def __init__(self):
        self.img = pygame.image.load("Images/Background.png")
        self.img = pygame.transform.scale(self.img, (424, 601))
        self.x = 190
        self.y = 0

    def display(self):
        screen.blit(self.img, (self.x, self.y))

class ITetrimino:
    
    WIDTH = BLOCK_WIDTH * 4
    HEIGHT = BLOCK_HEIGHT * 1

    def __init__(self, number_of_cycles, cycle_timer):
        self.img = pygame.image.load("Images/ITetrimino.png")
        self.img = pygame.transform.scale(self.img, (ITetrimino.WIDTH, ITetrimino.HEIGHT))
        self.x = LEFT + BLOCK_WIDTH * 3
        self.y = TOP
        self.cycle_timer = cycle_timer
        self.number_of_cycles = number_of_cycles 
        self.number_of_moving_down = 0 # サイクル内において、下に移動した回数
        self.is_fixed = False # テトリミノが固定されているかどうかを示す。一度テトリミノが下まで降りてきたら、テトリミノは固定される。

    # サイクル内において既に下に移動したならば、そのサイクル内では下に移動することはできない
    # 衝突していなければ、下へ移動することができる
    # 一度テトリミノが固定されても、下にテトリミノが存在しなければ下へ移動することができる
    # テトリミノの下側において衝突し、かつサイクルが残り0.2秒以下であれば、テトリミノは固定される
    def move_down(self, number_of_cycles, tetrimino_list):
        self.manage_number_of_moving_down(number_of_cycles)
        
        if self.number_of_moving_down == 0:

            collision = False
            for tetrimino in tetrimino_list:

                if self.is_collision_bottom(tetrimino.y):
                    collision = True
            
            if collision:
                if self.cycle_timer.measure(CYCLE_TIME - 0.2):
                    self.is_fixed = True

            else:
                self.y += BLOCK_HEIGHT
                self.number_of_moving_down += 1

    
    # 衝突していなければ、右へ移動することができる
    # 一度テトリミノが固定されてしまったら、右へ移動することはできなくなる
    def move_right(self, tetrimino_list):
        if not self.is_fixed:

            collision = False
            for tetrimino in tetrimino_list:

                if self.is_collision_right(tetrimino.x):
                    collision = True
            
            if not collision:
                self.x += BLOCK_WIDTH
    
    # 衝突していなければ、左へ移動することができる
    # 一度テトリミノが固定されてしまったら、左へ移動することはできなくなる
    def move_left(self, tetrimino_list):
        if not self.is_fixed:

            collision = False
            for tetrimino in tetrimino_list:

                if self.is_collision_left(tetrimino.x):
                    collision = True
            
            if not collision:
                self.x -= BLOCK_WIDTH
    
    def rotate_right(self):
        self.img = pygame.transform.rotate(self.img, -90)
    
    def rotate_left(self):
        self.img = pygame.transform.rotate(self.img, 90)
    
    def display(self):
        screen.blit(self.img, (self.x, self.y))
    
    # サイクルが変われば、number_of_moving_downの数を0にリセットする
    def manage_number_of_moving_down(self, number_of_cycles):
        if self.number_of_cycles != number_of_cycles:
            self.number_of_moving_down = 0
            self.number_of_cycles = number_of_cycles
    
    def is_collision_left(self, x):
        if self.x == x + BLOCK_WIDTH:
            return True
        elif self.x <= LEFT:
            return True
        else:
            return False

    def is_collision_right(self, x):
        if self.x + BLOCK_WIDTH == x:
            return True
        elif self.x + ITetrimino.WIDTH >= RIGHT:
            return True
        else:
            return False

    def is_collision_bottom(self, y):
        if self.y + BLOCK_HEIGHT == y:
            return True
        elif self.y + ITetrimino.HEIGHT >= BOTTOM:
            return True
        else:
            return False

class OTetrimino:

    WIDTH = BLOCK_WIDTH * 2
    HEIGHT = BLOCK_HEIGHT * 2

    def __init__(self, number_of_cycles, cycle_timer):
        self.img = pygame.image.load("Images/OTetrimino.png")
        self.img = pygame.transform.scale(self.img, (OTetrimino.WIDTH, OTetrimino.HEIGHT))
        self.x = LEFT + BLOCK_WIDTH * 4
        self.y = TOP
        self.cycle_timer = cycle_timer
        self.number_of_cycles = number_of_cycles 
        self.number_of_moving_down = 0 # サイクル内において、下に移動した回数
        self.is_fixed = False # テトリミノが固定されているかどうかを示す。一度テトリミノが下まで降りてきたら、テトリミノは固定される。

    # サイクル内において既に下に移動したならば、そのサイクル内では下に移動することはできない
    # 衝突していなければ、下へ移動することができる
    # 一度テトリミノが固定されても、下にテトリミノが存在しなければ下へ移動することができる
    # テトリミノの下側において衝突し、かつサイクルが残り0.2秒以下であれば、テトリミノは固定される
    def move_down(self, number_of_cycles, tetrimino_list):
        self.manage_number_of_moving_down(number_of_cycles)
        
        if self.number_of_moving_down == 0:

            collision = False
            for tetrimino in tetrimino_list:

                if self.is_collision_bottom(tetrimino.y):
                    collision = True
            
            if collision:
                if self.cycle_timer.measure(CYCLE_TIME - 0.2):
                    self.is_fixed = True

            else:
                self.y += BLOCK_HEIGHT
                self.number_of_moving_down += 1

    
    # 衝突していなければ、右へ移動することができる
    # 一度テトリミノが固定されてしまったら、右へ移動することはできなくなる
    def move_right(self, tetrimino_list):
        if not self.is_fixed:

            collision = False
            for tetrimino in tetrimino_list:

                if self.is_collision_right(tetrimino.x):
                    collision = True
            
            if not collision:
                self.x += BLOCK_WIDTH
    
    # 衝突していなければ、左へ移動することができる
    # 一度テトリミノが固定されてしまったら、左へ移動することはできなくなる
    def move_left(self, tetrimino_list):
        if not self.is_fixed:

            collision = False
            for tetrimino in tetrimino_list:

                if self.is_collision_left(tetrimino.x):
                    collision = True
            
            if not collision:
                self.x -= BLOCK_WIDTH
    
    def rotate_right(self):
        self.img = pygame.transform.rotate(self.img, -90)
    
    def rotate_left(self):
        self.img = pygame.transform.rotate(self.img, 90)
    
    def display(self):
        screen.blit(self.img, (self.x, self.y))
    
    # サイクルが変われば、number_of_moving_downの数を0にリセットする
    def manage_number_of_moving_down(self, number_of_cycles):
        if self.number_of_cycles != number_of_cycles:
            self.number_of_moving_down = 0
            self.number_of_cycles = number_of_cycles
    
    def is_collision_left(self, x):
        if self.x == x + BLOCK_WIDTH:
            return True
        elif self.x <= LEFT:
            return True
        else:
            return False

    def is_collision_right(self, x):
        if self.x + BLOCK_WIDTH == x:
            return True
        elif self.x + OTetrimino.WIDTH >= RIGHT:
            return True
        else:
            return False

    def is_collision_bottom(self, y):
        if self.y + BLOCK_HEIGHT == y:
            return True
        elif self.y + OTetrimino.HEIGHT >= BOTTOM:
            return True
        else:
            return False

class TTetrimino:

    WIDTH = BLOCK_WIDTH * 3
    HEIGHT = BLOCK_HEIGHT * 2

    def __init__(self, number_of_cycles, cycle_timer):
        self.img = pygame.image.load("Images/TTetrimino.png")
        self.img = pygame.transform.scale(self.img, (TTetrimino.WIDTH, TTetrimino.HEIGHT))
        self.x = LEFT + BLOCK_WIDTH * 3
        self.y = TOP
        self.cycle_timer = cycle_timer
        self.number_of_cycles = number_of_cycles 
        self.number_of_moving_down = 0 # サイクル内において、下に移動した回数
        self.is_fixed = False # テトリミノが固定されているかどうかを示す。一度テトリミノが下まで降りてきたら、テトリミノは固定される。

    # サイクル内において既に下に移動したならば、そのサイクル内では下に移動することはできない
    # 衝突していなければ、下へ移動することができる
    # 一度テトリミノが固定されても、下にテトリミノが存在しなければ下へ移動することができる
    # テトリミノの下側において衝突し、かつサイクルが残り0.2秒以下であれば、テトリミノは固定される
    def move_down(self, number_of_cycles, tetrimino_list):
        self.manage_number_of_moving_down(number_of_cycles)
        
        if self.number_of_moving_down == 0:

            collision = False
            for tetrimino in tetrimino_list:

                if self.is_collision_bottom(tetrimino.y):
                    collision = True
            
            if collision:
                if self.cycle_timer.measure(CYCLE_TIME - 0.2):
                    self.is_fixed = True

            else:
                self.y += BLOCK_HEIGHT
                self.number_of_moving_down += 1

    
    # 衝突していなければ、右へ移動することができる
    # 一度テトリミノが固定されてしまったら、右へ移動することはできなくなる
    def move_right(self, tetrimino_list):
        if not self.is_fixed:

            collision = False
            for tetrimino in tetrimino_list:

                if self.is_collision_right(tetrimino.x):
                    collision = True
            
            if not collision:
                self.x += BLOCK_WIDTH
    
    # 衝突していなければ、左へ移動することができる
    # 一度テトリミノが固定されてしまったら、左へ移動することはできなくなる
    def move_left(self, tetrimino_list):
        if not self.is_fixed:

            collision = False
            for tetrimino in tetrimino_list:

                if self.is_collision_left(tetrimino.x):
                    collision = True
            
            if not collision:
                self.x -= BLOCK_WIDTH
    
    def rotate_right(self):
        self.img = pygame.transform.rotate(self.img, -90)
    
    def rotate_left(self):
        self.img = pygame.transform.rotate(self.img, 90)
    
    def display(self):
        screen.blit(self.img, (self.x, self.y))
    
    # サイクルが変われば、number_of_moving_downの数を0にリセットする
    def manage_number_of_moving_down(self, number_of_cycles):
        if self.number_of_cycles != number_of_cycles:
            self.number_of_moving_down = 0
            self.number_of_cycles = number_of_cycles
    
    def is_collision_left(self, x):
        if self.x == x + BLOCK_WIDTH:
            return True
        elif self.x <= LEFT:
            return True
        else:
            return False

    def is_collision_right(self, x):
        if self.x + BLOCK_WIDTH == x:
            return True
        elif self.x + TTetrimino.WIDTH >= RIGHT:
            return True
        else:
            return False

    def is_collision_bottom(self, y):
        if self.y + BLOCK_HEIGHT == y:
            return True
        elif self.y + TTetrimino.HEIGHT >= BOTTOM:
            return True
        else:
            return False

class JTetrimino:

    WIDTH = BLOCK_WIDTH * 3
    HEIGHT = BLOCK_HEIGHT * 2

    def __init__(self, number_of_cycles, cycle_timer):
        self.img = pygame.image.load("Images/JTetrimino.png")
        self.img = pygame.transform.scale(self.img, (JTetrimino.WIDTH, JTetrimino.HEIGHT))
        self.x = LEFT + BLOCK_WIDTH * 3
        self.y = TOP
        self.cycle_timer = cycle_timer
        self.number_of_cycles = number_of_cycles 
        self.number_of_moving_down = 0 # サイクル内において、下に移動した回数
        self.is_fixed = False # テトリミノが固定されているかどうかを示す。一度テトリミノが下まで降りてきたら、テトリミノは固定される。

    # サイクル内において既に下に移動したならば、そのサイクル内では下に移動することはできない
    # 衝突していなければ、下へ移動することができる
    # 一度テトリミノが固定されても、下にテトリミノが存在しなければ下へ移動することができる
    # テトリミノの下側において衝突し、かつサイクルが残り0.2秒以下であれば、テトリミノは固定される
    def move_down(self, number_of_cycles, tetrimino_list):
        self.manage_number_of_moving_down(number_of_cycles)
        
        if self.number_of_moving_down == 0:

            collision = False
            for tetrimino in tetrimino_list:

                if self.is_collision_bottom(tetrimino.y):
                    collision = True
            
            if collision:
                if self.cycle_timer.measure(CYCLE_TIME - 0.2):
                    self.is_fixed = True

            else:
                self.y += BLOCK_HEIGHT
                self.number_of_moving_down += 1

    
    # 衝突していなければ、右へ移動することができる
    # 一度テトリミノが固定されてしまったら、右へ移動することはできなくなる
    def move_right(self, tetrimino_list):
        if not self.is_fixed:

            collision = False
            for tetrimino in tetrimino_list:

                if self.is_collision_right(tetrimino.x):
                    collision = True
            
            if not collision:
                self.x += BLOCK_WIDTH
    
    # 衝突していなければ、左へ移動することができる
    # 一度テトリミノが固定されてしまったら、左へ移動することはできなくなる
    def move_left(self, tetrimino_list):
        if not self.is_fixed:

            collision = False
            for tetrimino in tetrimino_list:

                if self.is_collision_left(tetrimino.x):
                    collision = True
            
            if not collision:
                self.x -= BLOCK_WIDTH
    
    def rotate_right(self):
        self.img = pygame.transform.rotate(self.img, -90)
    
    def rotate_left(self):
        self.img = pygame.transform.rotate(self.img, 90)
    
    def display(self):
        screen.blit(self.img, (self.x, self.y))
    
    # サイクルが変われば、number_of_moving_downの数を0にリセットする
    def manage_number_of_moving_down(self, number_of_cycles):
        if self.number_of_cycles != number_of_cycles:
            self.number_of_moving_down = 0
            self.number_of_cycles = number_of_cycles
    
    def is_collision_left(self, x):
        if self.x == x + BLOCK_WIDTH:
            return True
        elif self.x <= LEFT:
            return True
        else:
            return False

    def is_collision_right(self, x):
        if self.x + BLOCK_WIDTH == x:
            return True
        elif self.x + JTetrimino.WIDTH >= RIGHT:
            return True
        else:
            return False

    def is_collision_bottom(self, y):
        if self.y + BLOCK_HEIGHT == y:
            return True
        elif self.y + JTetrimino.HEIGHT >= BOTTOM:
            return True
        else:
            return False

class LTetrimino:

    WIDTH = BLOCK_WIDTH * 3
    HEIGHT = BLOCK_HEIGHT * 2

    def __init__(self, number_of_cycles, cycle_timer):
        self.img = pygame.image.load("Images/LTetrimino.png")
        self.img = pygame.transform.scale(self.img, (LTetrimino.WIDTH, LTetrimino.HEIGHT))
        self.x = LEFT + BLOCK_WIDTH * 3
        self.y = TOP
        self.cycle_timer = cycle_timer
        self.number_of_cycles = number_of_cycles 
        self.number_of_moving_down = 0 # サイクル内において、下に移動した回数
        self.is_fixed = False # テトリミノが固定されているかどうかを示す。一度テトリミノが下まで降りてきたら、テトリミノは固定される。

    # サイクル内において既に下に移動したならば、そのサイクル内では下に移動することはできない
    # 衝突していなければ、下へ移動することができる
    # 一度テトリミノが固定されても、下にテトリミノが存在しなければ下へ移動することができる
    # テトリミノの下側において衝突し、かつサイクルが残り0.2秒以下であれば、テトリミノは固定される
    def move_down(self, number_of_cycles, tetrimino_list):
        self.manage_number_of_moving_down(number_of_cycles)
        
        if self.number_of_moving_down == 0:

            collision = False
            for tetrimino in tetrimino_list:

                if self.is_collision_bottom(tetrimino.y):
                    collision = True
            
            if collision:
                if self.cycle_timer.measure(CYCLE_TIME - 0.2):
                    self.is_fixed = True

            else:
                self.y += BLOCK_HEIGHT
                self.number_of_moving_down += 1

    
    # 衝突していなければ、右へ移動することができる
    # 一度テトリミノが固定されてしまったら、右へ移動することはできなくなる
    def move_right(self, tetrimino_list):
        if not self.is_fixed:

            collision = False
            for tetrimino in tetrimino_list:

                if self.is_collision_right(tetrimino.x):
                    collision = True
            
            if not collision:
                self.x += BLOCK_WIDTH
    
    # 衝突していなければ、左へ移動することができる
    # 一度テトリミノが固定されてしまったら、左へ移動することはできなくなる
    def move_left(self, tetrimino_list):
        if not self.is_fixed:

            collision = False
            for tetrimino in tetrimino_list:

                if self.is_collision_left(tetrimino.x):
                    collision = True
            
            if not collision:
                self.x -= BLOCK_WIDTH
    
    def rotate_right(self):
        self.img = pygame.transform.rotate(self.img, -90)
    
    def rotate_left(self):
        self.img = pygame.transform.rotate(self.img, 90)
    
    def display(self):
        screen.blit(self.img, (self.x, self.y))
    
    # サイクルが変われば、number_of_moving_downの数を0にリセットする
    def manage_number_of_moving_down(self, number_of_cycles):
        if self.number_of_cycles != number_of_cycles:
            self.number_of_moving_down = 0
            self.number_of_cycles = number_of_cycles
    
    def is_collision_left(self, x):
        if self.x == x + BLOCK_WIDTH:
            return True
        elif self.x <= LEFT:
            return True
        else:
            return False

    def is_collision_right(self, x):
        if self.x + BLOCK_WIDTH == x:
            return True
        elif self.x + LTetrimino.WIDTH >= RIGHT:
            return True
        else:
            return False

    def is_collision_bottom(self, y):
        if self.y + BLOCK_HEIGHT == y:
            return True
        elif self.y + LTetrimino.HEIGHT >= BOTTOM:
            return True
        else:
            return False

class STetrimino:

    WIDTH = BLOCK_WIDTH * 3
    HEIGHT = BLOCK_HEIGHT * 2

    def __init__(self, number_of_cycles, cycle_timer):
        self.img = pygame.image.load("Images/STetrimino.png")
        self.img = pygame.transfrom.scale(self.img, (STetrimino.WIDTH, STetrimino.HEIGHT))
        self.x = LEFT + BLOCK_WIDTH * 3
        self.y = TOP
        self.cycle_timer = cycle_timer
        self.number_of_cycles = number_of_cycles 
        self.number_of_moving_down = 0 # サイクル内において、下に移動した回数
        self.is_fixed = False # テトリミノが固定されているかどうかを示す。一度テトリミノが下まで降りてきたら、テトリミノは固定される。

    # サイクル内において既に下に移動したならば、そのサイクル内では下に移動することはできない
    # 衝突していなければ、下へ移動することができる
    # 一度テトリミノが固定されても、下にテトリミノが存在しなければ下へ移動することができる
    # テトリミノの下側において衝突し、かつサイクルが残り0.2秒以下であれば、テトリミノは固定される
    def move_down(self, number_of_cycles, tetrimino_list):
        self.manage_number_of_moving_down(number_of_cycles)
        
        if self.number_of_moving_down == 0:

            collision = False
            for tetrimino in tetrimino_list:

                if self.is_collision_bottom(tetrimino.y):
                    collision = True
            
            if collision:
                if self.cycle_timer.measure(CYCLE_TIME - 0.2):
                    self.is_fixed = True

            else:
                self.y += BLOCK_HEIGHT
                self.number_of_moving_down += 1

    
    # 衝突していなければ、右へ移動することができる
    # 一度テトリミノが固定されてしまったら、右へ移動することはできなくなる
    def move_right(self, tetrimino_list):
        if not self.is_fixed:

            collision = False
            for tetrimino in tetrimino_list:

                if self.is_collision_right(tetrimino.x):
                    collision = True
            
            if not collision:
                self.x += BLOCK_WIDTH
    
    # 衝突していなければ、左へ移動することができる
    # 一度テトリミノが固定されてしまったら、左へ移動することはできなくなる
    def move_left(self, tetrimino_list):
        if not self.is_fixed:

            collision = False
            for tetrimino in tetrimino_list:

                if self.is_collision_left(tetrimino.x):
                    collision = True
            
            if not collision:
                self.x -= BLOCK_WIDTH
    
    def rotate_right(self):
        self.img = pygame.transform.rotate(self.img, -90)
    
    def rotate_left(self):
        self.img = pygame.transform.rotate(self.img, 90)
    
    def display(self):
        screen.blit(self.img, (self.x, self.y))
    
    # サイクルが変われば、number_of_moving_downの数を0にリセットする
    def manage_number_of_moving_down(self, number_of_cycles):
        if self.number_of_cycles != number_of_cycles:
            self.number_of_moving_down = 0
            self.number_of_cycles = number_of_cycles
    
    def is_collision_left(self, x):
        if self.x == x + BLOCK_WIDTH:
            return True
        elif self.x <= LEFT:
            return True
        else:
            return False

    def is_collision_right(self, x):
        if self.x + BLOCK_WIDTH == x:
            return True
        elif self.x + STetrimino.WIDTH >= RIGHT:
            return True
        else:
            return False

    def is_collision_bottom(self, y):
        if self.y + BLOCK_HEIGHT == y:
            return True
        elif self.y + STetrimino.HEIGHT >= BOTTOM:
            return True
        else:
            return False

class ZTetrimino:

    WIDTH = BLOCK_WIDTH * 3
    HEIGHT = BLOCK_HEIGHT * 2

    def __init__(self, number_of_cycles, cycle_timer):
        self.img = pygame.image.load("Images/ZTetrimino.png")
        self.img = pygame.transform.scale(self.img, (ZTetrimino.WIDTH, ZTetrimino.HEIGHT))
        self.x = LEFT + BLOCK_WIDTH * 3
        self.y = TOP
        self.cycle_timer = cycle_timer
        self.number_of_cycles = number_of_cycles 
        self.number_of_moving_down = 0 # サイクル内において、下に移動した回数
        self.is_fixed = False # テトリミノが固定されているかどうかを示す。一度テトリミノが下まで降りてきたら、テトリミノは固定される。

    # サイクル内において既に下に移動したならば、そのサイクル内では下に移動することはできない
    # 衝突していなければ、下へ移動することができる
    # 一度テトリミノが固定されても、下にテトリミノが存在しなければ下へ移動することができる
    # テトリミノの下側において衝突し、かつサイクルが残り0.2秒以下であれば、テトリミノは固定される
    def move_down(self, number_of_cycles, tetrimino_list):
        self.manage_number_of_moving_down(number_of_cycles)
        
        if self.number_of_moving_down == 0:

            collision = False
            for tetrimino in tetrimino_list:

                if self.is_collision_bottom(tetrimino.y):
                    collision = True
            
            if collision:
                if self.cycle_timer.measure(CYCLE_TIME - 0.2):
                    self.is_fixed = True

            else:
                self.y += BLOCK_HEIGHT
                self.number_of_moving_down += 1

    
    # 衝突していなければ、右へ移動することができる
    # 一度テトリミノが固定されてしまったら、右へ移動することはできなくなる
    def move_right(self, tetrimino_list):
        if not self.is_fixed:

            collision = False
            for tetrimino in tetrimino_list:

                if self.is_collision_right(tetrimino.x):
                    collision = True
            
            if not collision:
                self.x += BLOCK_WIDTH
    
    # 衝突していなければ、左へ移動することができる
    # 一度テトリミノが固定されてしまったら、左へ移動することはできなくなる
    def move_left(self, tetrimino_list):
        if not self.is_fixed:

            collision = False
            for tetrimino in tetrimino_list:

                if self.is_collision_left(tetrimino.x):
                    collision = True
            
            if not collision:
                self.x -= BLOCK_WIDTH
    
    def rotate_right(self):
        self.img = pygame.transform.rotate(self.img, -90)
    
    def rotate_left(self):
        self.img = pygame.transform.rotate(self.img, 90)
    
    def display(self):
        screen.blit(self.img, (self.x, self.y))
    
    # サイクルが変われば、number_of_moving_downの数を0にリセットする
    def manage_number_of_moving_down(self, number_of_cycles):
        if self.number_of_cycles != number_of_cycles:
            self.number_of_moving_down = 0
            self.number_of_cycles = number_of_cycles
    
    def is_collision_left(self, x):
        if self.x == x + BLOCK_WIDTH:
            return True
        elif self.x <= LEFT:
            return True
        else:
            return False

    def is_collision_right(self, x):
        if self.x + BLOCK_WIDTH == x:
            return True
        elif self.x + ZTetrimino.WIDTH >= RIGHT:
            return True
        else:
            return False

    def is_collision_bottom(self, y):
        if self.y + BLOCK_HEIGHT == y:
            return True
        elif self.y + ZTetrimino.HEIGHT >= BOTTOM:
            return True
        else:
            return False


# ------------------------------------ 関数 -----------------------------------------

# テトリミノを生成する関数
# テトリミノの種類はランダムに選ばれる
def generate_tetrimino(number_of_cycles, cycle_timer):
    number = random.randint(0, 6)

    if number == 0:
        i_tetrimino = ITetrimino(number_of_cycles, cycle_timer)
        return i_tetrimino
    elif number == 1:
        o_tetrimino = OTetrimino(number_of_cycles, cycle_timer)
        return o_tetrimino
    elif number == 2:
        t_tetrimino = TTetrimino(number_of_cycles, cycle_timer)
        return t_tetrimino
    elif number == 3:
        j_tetrimino = JTetrimino(number_of_cycles, cycle_timer)
        return j_tetrimino
    elif number == 4:
        l_tetrimino = LTetrimino(number_of_cycles, cycle_timer)
        return l_tetrimino
    elif number == 5:
        s_tetrimino = STetrimino(number_of_cycles, cycle_timer)
        return s_tetrimino
    elif number == 6:
        z_tetrimino = ZTetrimino(number_of_cycles, cycle_timer)


game_scene = "playing_scene"
running = True
while running:
    
    # プレイシーン
    if game_scene == "playing_scene":
        
        background = Background()

        CYCLE_TIMER = Timer() # 周期1秒のサイクルを管理するためのタイマー
        CYCLE_TIMER.start()
        CYCLE_TIME = 1 # 1サイクルの時間
        number_of_cycles = 0 # サイクルの回数

        tetrimino_list = [generate_tetrimino(number_of_cycles, CYCLE_TIMER)]

        playing_scene = True
        while playing_scene:

            background.display()

            # サイクルを管理する
            # 1秒が経過したら、新しいサイクルが始まる
            # 全てのテトリミノが固定されている場合、新しいテトリミノを生成する
            if CYCLE_TIMER.measure(CYCLE_TIME):
                CYCLE_TIMER.start()
                number_of_cycles += 1

                is_fixed = False
                for tetrimino in tetrimino_list:

                    if tetrimino.is_fixed:
                        is_fixed = True
                
                if is_fixed:
                    tetrimino_list.append(generate_tetrimino(number_of_cycles, CYCLE_TIMER))

            
            # テトリミノを下に動かす
            for tetrimino in tetrimino_list:
                tetrimino.move_down(number_of_cycles, tetrimino_list)
            
            # 左矢印キー、右矢印キーが押されたら、テトリミノを左右へ移動させる
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_LEFT:
                        tetrimino.move_left(tetrimino_list)
                    
                    elif event.key == pygame.K_RIGHT:
                        tetrimino.move_right(tetrimino_list)
            
            # テトリミノを画面に表示させる
            for tetrimino in tetrimino_list:
                tetrimino.display()

            pygame.display.update()

            screen.fill((255, 255, 255))
