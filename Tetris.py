import pygame
from pygame import mixer

import datetime
import random


pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Tetris")


# --------------------------------------- 変数 ------------------------------------------

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

# テトリミノを構成するブロック
class Block:

    WIDTH = 36.1
    HEIGHT = 36.1

    def __init__(self, x, y):
        self.img = pygame.image.load("Images/Block.png")
        self.img = pygame.transform.scale(self.img, (Block.WIDTH, Block.HEIGHT))
        self.x = x
        self.y = y
    
    def display(self):
        screen.blit(self.img, (self.x, self.y))
    
    def move_down(self):
        self.y += Block.HEIGHT
    
    def move_left(self):
        self.x -= Block.WIDTH

    def move_right(self):
        self.x += Block.HEIGHT
    
    # 引数にブロックを渡し、対象のブロックが下側において引数に渡したブロックと衝突しているかどうかを判定
    def is_collision_bottom(self, block):   
        if self.x == block.x and self.y + Block.HEIGHT == block.y:
            return True
        else:
            return False
    
    # 引数にブロックを渡し、対象のブロックが左側において引数に渡したブロックと衝突しているかどうかを判定
    def is_collision_left(self, block):
        if self.x == block.x + Block.WIDTH and self.y == block.y:
            return True
        else:
            return False

    # 引数にブロックを渡し、対象のブロックが右側において引数に渡したブロックと衝突しているかどうかを判定
    def is_collision_right(self, block):
        if self.x + Block.WIDTH == block.x and self.y == block.y:
            return True
        else:
            return False
    
    # ブロックが床に衝突しているかどうかを判定
    def is_at_bottom(self):
        if self.y >= BOTTOM:
            return True
        else:
            return False
    
    # ブロックが左側の壁に衝突しているかどうかを判定
    def is_on_left(self):
        if self.x <= LEFT:
            return True
        else:
            return False
    
    # ブロックが右側の壁に衝突しているかどうかを判定
    def is_on_right(self):
        if self.x + Block.WIDTH >= RIGHT:
            return True
        else:
            return False

class TetriminoManager:
    def __init__(self):
        self.cycle_timer = Timer() # サイクルを管理するタイマー
        self.cycle_timer.start()
        self.cycle_time = 1 # 1サイクルの時間
        self.tetrimino_list = []
        self.number_of_moving_down = 0 # サイクル内においてテトリミノが下へ移動した回数
    
    def display(self):
        for tetrimino in self.tetrimino_list:
            tetrimino.display()
    
    def manage_cycle_timer(self):
        if self.cycle_timer.measure(self.cycle_time):
            self.cycle_timer.start()
            self.number_of_moving_down = 0
    
    # ランダムに1種類のテトリミノを生成する
    # 最後に生成したテトリミノが固定状態かつ、そのサイクルにおいて0.2秒以上時間が経過していなければ、新しいテトリミノを生成できる
    def generate_tetrimino(self):

        if (len(self.tetrimino_list) == 0 or self.tetrimino_list[-1].is_fixed) and not self.cycle_timer.measure(self.cycle_time - 0.8):

            number = random.randint(0, 6)

            if number == 0:
                self.tetrimino_list.append(ITetrimino())
            elif number == 1:
                self.tetrimino_list.append(OTetrimino())
            elif number == 2:
                self.tetrimino_list.append(TTetrimino())
            elif number == 3:
                self.tetrimino_list.append(JTetrimino())
            elif number == 4:
                self.tetrimino_list.append(LTetrimino())
            elif number == 5:
                self.tetrimino_list.append(STetrimino())
            elif number == 6:
                self.tetrimino_list.append(ZTetrimino())
    
    # サイクル内において一度もテトリミノを下に移動させていなければ、下に移動させることができる
    def move_down_tetrimino(self):

        if self.number_of_moving_down == 0:

            for tetrimino in self.tetrimino_list:
                tetrimino.move_down(self.tetrimino_list)
            
            self.number_of_moving_down += 1
    
    def move_left_tetrimino(self):
        self.tetrimino_list[-1].move_left(self.tetrimino_list)
    
    def move_right_tetrimino(self):
        self.tetrimino_list[-1].move_right(self.tetrimino_list)
    
    # 現在操作しているテトリミノが下側において衝突し、かつサイクルの残り時間が0.2秒以下であれば、そのテトリミノを固定状態にする
    def fix_tetrimino(self):
        if self.cycle_timer.measure(self.cycle_time - 0.2) and not self.tetrimino_list[-1].is_fixed:

            collision = False
            for tetrimino in self.tetrimino_list:
                
                if self.tetrimino_list[-1].is_collision_bottom(tetrimino):
                    collision = True
            
            if self.tetrimino_list[-1].is_at_bottom():
                collision = True
            
            if collision:
                self.tetrimino_list[-1].is_fixed = True
    



class ITetrimino:
    def __init__(self):
        self.block_list = [Block(LEFT+Block.WIDTH*4, TOP), Block(LEFT+Block.WIDTH*4, TOP+Block.HEIGHT), Block(LEFT+Block.WIDTH*4, TOP+Block.HEIGHT*2), Block(LEFT+Block.WIDTH*4, TOP+Block.HEIGHT*3)]
        self.is_fixed = False # テトリミノが固定状態になったかどうかを示す。テトリミノが床または他のテトリミノに衝突したら、
                              # テトリミノは固定状態になる。固定状態になると、横方向へは動けなくなる。

    def display(self):
        for block in self.block_list:
            block.display()
    
    def move_down(self, tetrimino_list):
        collision = False
        for tetrimino in tetrimino_list:
            if self.is_collision_bottom(tetrimino):
                collision = True
        
        if self.is_at_bottom():
            collision = True
        
        if not collision:
            for block in self.block_list:
                block.move_down()
    
    def move_left(self, tetrimino_list):
        collision = False
        for tetrimino in tetrimino_list:
            if self.is_collision_left(tetrimino):
                collision = True
        
        if self.is_on_left():
            collision = True
        
        if not collision and not self.is_fixed:
            for block in self.block_list:
                block.move_left()
    
    def move_right(self, tetrimino_list):
        collision = False
        for tetrimino in tetrimino_list:
            if self.is_collision_right(tetrimino):
                collision = True
        
        if self.is_on_right:
            collision = True
        
        if not collision and not self.is_fixed:
            for block in self.block_list:
                block.move_right()
    
    # 引数にテトリミノを渡す。対象のテトリミノの一番下のブロックが下側において、引数に渡したテトリミノのブロックと衝突しているかどうかを判定
    def is_collision_bottom(self, tetrimino):
        collision = False
        for block in tetrimino.block_list:
            if self.block_list[3].is_collision_bottom(block):
                collision = True
        
        return collision
    
    # 引数にテトリミノを渡す。対象のテトリミノのブロックが左側において、引数に渡したテトリミノのブロックと衝突しているかどうかを判定
    def is_collision_left(self, tetrimino):
        collision = False
        for block in self.block_list:
            for another_block in tetrimino.block_list:

                if block.is_collision_left(another_block):
                    collision = True
        
        return collision
    
    # 引数にテトリミノを渡す。対象のテトリミノのブロックが右側において、引数に渡したテトリミノのブロックと衝突しているかどうかを判定
    def is_collision_right(self, tetrimino):
        collision = False
        for block in self.block_list:
            for another_block in tetrimino.block_list:

                if block.is_collision_right(another_block):
                    collision = True
        
        return collision
    
    # ブロックが床に衝突しているかどうかを判定
    def is_at_bottom(self):
        return self.block_list[3].is_at_bottom()
    
    # テトリミノのブロックが左側の壁に衝突しているかどうかを判定
    def is_on_left(self):
        collision = False
        for block in self.block_list:
            if block.is_on_left():
                collision = True
        
        return collision
    
    # テトリミノのブロックが右側の壁に衝突しているかどうかを判定
    def is_on_right(self):
        collision = False
        for block in self.block_list:
            if block.is_on_right():
                collision = True
        
        return collision

class OTetrimino:
    def __init__(self):
        self.block_list = [Block(LEFT+Block.WIDTH*4, TOP), Block(LEFT+Block.WIDTH*5, TOP), Block(LEFT+Block.WIDTH*4, TOP+Block.HEIGHT), Block(LEFT+Block.WIDTH*5, TOP+Block.HEIGHT)]
        self.is_fixed = False # テトリミノが固定状態になったかどうかを示す。テトリミノが床または他のテトリミノに衝突したら、
                              # テトリミノは固定状態になる。固定状態になると、横方向へは動けなくなる。

    def display(self):
        for block in self.block_list:
            block.display()
    
    def move_down(self, tetrimino_list):
        collision = False
        for tetrimino in tetrimino_list:
            if self.is_collision_bottom(tetrimino):
                collision = True
        
        if self.is_at_bottom():
            collision = True
        
        if not collision:
            for block in self.block_list:
                block.move_down()
    
    def move_left(self, tetrimino_list):
        collision = False
        for tetrimino in tetrimino_list:
            if self.is_collision_left(tetrimino):
                collision = True
        
        if self.is_on_left():
            collision = True
        
        if not collision and not self.is_fixed:
            for block in self.block_list:
                block.move_left()
    
    def move_right(self, tetrimino_list):
        collision = False
        for tetrimino in tetrimino_list:
            if self.is_collision_right(tetrimino):
                collision = True
        
        if self.is_on_right:
            collision = True
        
        if not collision and not self.is_fixed:
            for block in self.block_list:
                block.move_right()
    
    # 引数にテトリミノを渡す。対象のテトリミノの一番下のブロックが下側において、引数に渡したテトリミノのブロックと衝突しているかどうかを判定
    def is_collision_bottom(self, tetrimino):
        collision = False
        for block in tetrimino.block_list:
            if self.block_list[2].is_collision_bottom(block) or self.block_list[3].is_collision_bottom(block):
                collision = True
        
        return collision
    
    # 引数にテトリミノを渡す。対象のテトリミノのブロックが左側において、引数に渡したテトリミノのブロックと衝突しているかどうかを判定
    def is_collision_left(self, tetrimino):
        collision = False
        for block in tetrimino.block_list:

            if self.block_list[0].is_collision_left(block) or self.block_list[2].is_collision_left(block):
                collision = True
        
        return collision
    
    # 引数にテトリミノを渡す。対象のテトリミノのブロックが右側において、引数に渡したテトリミノのブロックと衝突しているかどうかを判定
    def is_collision_right(self, tetrimino):
        collision = False
        for block in tetrimino.block_list:

            if self.block_list[1].is_collision_right(block) or self.block_list[3].is_collision_right(block):
                collision = True
        
        return collision
    
    # ブロックが床に衝突しているかどうかを判定
    def is_at_bottom(self):
        return self.block_list[3].is_at_bottom()
    
    # テトリミノのブロックが左側の壁に衝突しているかどうかを判定
    def is_on_left(self):
        collision = False
        for block in self.block_list:
            if block.is_on_left():
                collision = True
        
        return collision
    
    # テトリミノのブロックが右側の壁に衝突しているかどうかを判定
    def is_on_right(self):
        collision = False
        for block in self.block_list:
            if block.is_on_right():
                collision = True
        
        return collision

class TTetrimino:

    def __init__(self):
        self.block_list = [Block(LEFT+Block.WIDTH*4, TOP), Block(LEFT+Block.WIDTH*4, TOP+Block.HEIGHT), Block(LEFT+Block.WIDTH*4, TOP+Block.HEIGHT*2), Block(LEFT+Block.WIDTH*5, TOP+Block.HEIGHT)]
        self.is_fixed = False # テトリミノが固定状態になったかどうかを示す。テトリミノが床または他のテトリミノに衝突したら、
                              # テトリミノは固定状態になる。固定状態になると、横方向へは動けなくなる。

    def display(self):
        for block in self.block_list:
            block.display()
    
    def move_down(self, tetrimino_list):
        collision = False
        for tetrimino in tetrimino_list:
            if self.is_collision_bottom(tetrimino):
                collision = True
        
        if self.is_at_bottom():
            collision = True
        
        if not collision:
            for block in self.block_list:
                block.move_down()
    
    def move_left(self, tetrimino_list):
        collision = False
        for tetrimino in tetrimino_list:
            if self.is_collision_left(tetrimino):
                collision = True
        
        if self.is_on_left():
            collision = True
        
        if not collision and not self.is_fixed:
            for block in self.block_list:
                block.move_left()
    
    def move_right(self, tetrimino_list):
        collision = False
        for tetrimino in tetrimino_list:
            if self.is_collision_right(tetrimino):
                collision = True
        
        if self.is_on_right:
            collision = True
        
        if not collision and not self.is_fixed:
            for block in self.block_list:
                block.move_right()
    
    # 引数にテトリミノを渡す。対象のテトリミノの一番下のブロックが下側において、引数に渡したテトリミノのブロックと衝突しているかどうかを判定
    def is_collision_bottom(self, tetrimino):
        collision = False
        for block in tetrimino.block_list:
            if self.block_list[2].is_collision_bottom(block) or self.block_list[3].is_collision_bottom(block):
                collision = True
        
        return collision
    
    # 引数にテトリミノを渡す。対象のテトリミノのブロックが左側において、引数に渡したテトリミノのブロックと衝突しているかどうかを判定
    def is_collision_left(self, tetrimino):
        collision = False
        for block in tetrimino.block_list:

            if self.block_list[0].is_collision_left(block) or self.block_list[1].is_collision_left(block) or self.block_list[2].is_collision_left(block):
                collision = True
        
        return collision
    
    # 引数にテトリミノを渡す。対象のテトリミノのブロックが右側において、引数に渡したテトリミノのブロックと衝突しているかどうかを判定
    def is_collision_right(self, tetrimino):
        collision = False
        for block in tetrimino.block_list:

            if self.block_list[0].is_collision_right(block) or self.block_list[2].is_collision_right(block) or self.block_list[3].is_collision_right(block):
                collision = True
        
        return collision
    
    # ブロックが床に衝突しているかどうかを判定
    def is_at_bottom(self):
        return self.block_list[2].is_at_bottom()
    
    # テトリミノのブロックが左側の壁に衝突しているかどうかを判定
    def is_on_left(self):
        collision = False
        for block in self.block_list:
            if block.is_on_left():
                collision = True
        
        return collision
    
    # テトリミノのブロックが右側の壁に衝突しているかどうかを判定
    def is_on_right(self):
        collision = False
        for block in self.block_list:
            if block.is_on_right():
                collision = True
        
        return collision

class JTetrimino:

    def __init__(self):
        self.block_list = [Block(LEFT+Block.WIDTH*3, TOP), Block(LEFT+Block.WIDTH*3, TOP+Block.HEIGHT), Block(LEFT+Block.WIDTH*4, TOP+Block.HEIGHT), Block(LEFT+Block.WIDTH*5, TOP+Block.HEIGHT)]
        self.is_fixed = False # テトリミノが固定状態になったかどうかを示す。テトリミノが床または他のテトリミノに衝突したら、
                              # テトリミノは固定状態になる。固定状態になると、横方向へは動けなくなる。

    def display(self):
        for block in self.block_list:
            block.display()
    
    def move_down(self, tetrimino_list):
        collision = False
        for tetrimino in tetrimino_list:
            if self.is_collision_bottom(tetrimino):
                collision = True
        
        if self.is_at_bottom():
            collision = True
        
        if not collision:
            for block in self.block_list:
                block.move_down()
    
    def move_left(self, tetrimino_list):
        collision = False
        for tetrimino in tetrimino_list:
            if self.is_collision_left(tetrimino):
                collision = True
        
        if self.is_on_left():
            collision = True
        
        if not collision and not self.is_fixed:
            for block in self.block_list:
                block.move_left()
    
    def move_right(self, tetrimino_list):
        collision = False
        for tetrimino in tetrimino_list:
            if self.is_collision_right(tetrimino):
                collision = True
        
        if self.is_on_right:
            collision = True
        
        if not collision and not self.is_fixed:
            for block in self.block_list:
                block.move_right()
    
    # 引数にテトリミノを渡す。対象のテトリミノの一番下のブロックが下側において、引数に渡したテトリミノのブロックと衝突しているかどうかを判定
    def is_collision_bottom(self, tetrimino):
        collision = False
        for block in tetrimino.block_list:
            if self.block_list[1].is_collision_bottom(block) or self.block_list[2].is_collision_bottom(block) or self.block_list[3].is_collision_bottom(block):
                collision = True
        
        return collision
    
    # 引数にテトリミノを渡す。対象のテトリミノのブロックが左側において、引数に渡したテトリミノのブロックと衝突しているかどうかを判定
    def is_collision_left(self, tetrimino):
        collision = False
        for block in tetrimino.block_list:

            if self.block_list[0].is_collision_left(block) or self.block_list[1].is_collision_left(block):
                collision = True
        
        return collision
    
    # 引数にテトリミノを渡す。対象のテトリミノのブロックが右側において、引数に渡したテトリミノのブロックと衝突しているかどうかを判定
    def is_collision_right(self, tetrimino):
        collision = False
        for block in tetrimino.block_list:

            if self.block_list[0].is_collision_right(block) or self.block_list[3].is_collision_right(block):
                collision = True
        
        return collision
    
    # ブロックが床に衝突しているかどうかを判定
    def is_at_bottom(self):
        return self.block_list[3].is_at_bottom()
    
    # テトリミノのブロックが左側の壁に衝突しているかどうかを判定
    def is_on_left(self):
        collision = False
        for block in self.block_list:
            if block.is_on_left():
                collision = True
        
        return collision
    
    # テトリミノのブロックが右側の壁に衝突しているかどうかを判定
    def is_on_right(self):
        collision = False
        for block in self.block_list:
            if block.is_on_right():
                collision = True
        
        return collision

class LTetrimino:

    def __init__(self):
        self.block_list = [Block(LEFT+Block.WIDTH*4, TOP), Block(LEFT+Block.WIDTH*4, TOP+Block.HEIGHT), Block(LEFT+Block.WIDTH*4, TOP+Block.HEIGHT*2), Block(LEFT+Block.WIDTH*5, TOP+Block.HEIGHT*2)]
        self.is_fixed = False # テトリミノが固定状態になったかどうかを示す。テトリミノが床または他のテトリミノに衝突したら、
                              # テトリミノは固定状態になる。固定状態になると、横方向へは動けなくなる。

    def display(self):
        for block in self.block_list:
            block.display()
    
    def move_down(self, tetrimino_list):
        collision = False
        for tetrimino in tetrimino_list:
            if self.is_collision_bottom(tetrimino):
                collision = True
        
        if self.is_at_bottom():
            collision = True
        
        if not collision:
            for block in self.block_list:
                block.move_down()
    
    def move_left(self, tetrimino_list):
        collision = False
        for tetrimino in tetrimino_list:
            if self.is_collision_left(tetrimino):
                collision = True
        
        if self.is_on_left():
            collision = True
        
        if not collision and not self.is_fixed:
            for block in self.block_list:
                block.move_left()
    
    def move_right(self, tetrimino_list):
        collision = False
        for tetrimino in tetrimino_list:
            if self.is_collision_right(tetrimino):
                collision = True
        
        if self.is_on_right:
            collision = True
        
        if not collision and not self.is_fixed:
            for block in self.block_list:
                block.move_right()
    
    # 引数にテトリミノを渡す。対象のテトリミノの一番下のブロックが下側において、引数に渡したテトリミノのブロックと衝突しているかどうかを判定
    def is_collision_bottom(self, tetrimino):
        collision = False
        for block in tetrimino.block_list:
            if self.block_list[2].is_collision_bottom(block) or self.block_list[3].is_collision_bottom(block):
                collision = True
        
        return collision
    
    # 引数にテトリミノを渡す。対象のテトリミノのブロックが左側において、引数に渡したテトリミノのブロックと衝突しているかどうかを判定
    def is_collision_left(self, tetrimino):
        collision = False
        for block in tetrimino.block_list:

            if self.block_list[0].is_collision_left(block) or self.block_list[1].is_collision_left(block) or self.block_list[2].is_collision_left(block):
                collision = True
        
        return collision
    
    # 引数にテトリミノを渡す。対象のテトリミノのブロックが右側において、引数に渡したテトリミノのブロックと衝突しているかどうかを判定
    def is_collision_right(self, tetrimino):
        collision = False
        for block in tetrimino.block_list:

            if self.block_list[0].is_collision_right(block) or self.block_list[1].is_collision_right(block) or self.block_list[3].is_collision_right(block):
                collision = True
        
        return collision
    
    # ブロックが床に衝突しているかどうかを判定
    def is_at_bottom(self):
        return self.block_list[3].is_at_bottom()
    
    # テトリミノのブロックが左側の壁に衝突しているかどうかを判定
    def is_on_left(self):
        collision = False
        for block in self.block_list:
            if block.is_on_left():
                collision = True
        
        return collision
    
    # テトリミノのブロックが右側の壁に衝突しているかどうかを判定
    def is_on_right(self):
        collision = False
        for block in self.block_list:
            if block.is_on_right():
                collision = True
        
        return collision

class STetrimino:

    def __init__(self):
        self.block_list = [Block(LEFT+Block.WIDTH*4, TOP), Block(LEFT+Block.WIDTH*5, TOP), Block(LEFT+Block.WIDTH*3, TOP+Block.HEIGHT), Block(LEFT+Block.WIDTH*4, TOP+Block.HEIGHT)]
        self.is_fixed = False # テトリミノが固定状態になったかどうかを示す。テトリミノが床または他のテトリミノに衝突したら、
                              # テトリミノは固定状態になる。固定状態になると、横方向へは動けなくなる。

    def display(self):
        for block in self.block_list:
            block.display()
    
    def move_down(self, tetrimino_list):
        collision = False
        for tetrimino in tetrimino_list:
            if self.is_collision_bottom(tetrimino):
                collision = True
        
        if self.is_at_bottom():
            collision = True
        
        if not collision:
            for block in self.block_list:
                block.move_down()
    
    def move_left(self, tetrimino_list):
        collision = False
        for tetrimino in tetrimino_list:
            if self.is_collision_left(tetrimino):
                collision = True
        
        if self.is_on_left():
            collision = True
        
        if not collision and not self.is_fixed:
            for block in self.block_list:
                block.move_left()
    
    def move_right(self, tetrimino_list):
        collision = False
        for tetrimino in tetrimino_list:
            if self.is_collision_right(tetrimino):
                collision = True
        
        if self.is_on_right:
            collision = True
        
        if not collision and not self.is_fixed:
            for block in self.block_list:
                block.move_right()
    
    # 引数にテトリミノを渡す。対象のテトリミノの一番下のブロックが下側において、引数に渡したテトリミノのブロックと衝突しているかどうかを判定
    def is_collision_bottom(self, tetrimino):
        collision = False
        for block in tetrimino.block_list:
            if self.block_list[1].is_collision_bottom(block) or self.block_list[2].is_collision_bottom(block) or self.block_list[3].is_collision_bottom(block):
                collision = True
        
        return collision
    
    # 引数にテトリミノを渡す。対象のテトリミノのブロックが左側において、引数に渡したテトリミノのブロックと衝突しているかどうかを判定
    def is_collision_left(self, tetrimino):
        collision = False
        for block in tetrimino.block_list:

            if self.block_list[0].is_collision_left(block) or self.block_list[2].is_collision_left(block):
                collision = True
        
        return collision
    
    # 引数にテトリミノを渡す。対象のテトリミノのブロックが右側において、引数に渡したテトリミノのブロックと衝突しているかどうかを判定
    def is_collision_right(self, tetrimino):
        collision = False
        for block in tetrimino.block_list:

            if self.block_list[1].is_collision_right(block) or self.block_list[3].is_collision_right(block):
                collision = True
        
        return collision
    
    # ブロックが床に衝突しているかどうかを判定
    def is_at_bottom(self):
        return self.block_list[3].is_at_bottom()
    
    # テトリミノのブロックが左側の壁に衝突しているかどうかを判定
    def is_on_left(self):
        collision = False
        for block in self.block_list:
            if block.is_on_left():
                collision = True
        
        return collision
    
    # テトリミノのブロックが右側の壁に衝突しているかどうかを判定
    def is_on_right(self):
        collision = False
        for block in self.block_list:
            if block.is_on_right():
                collision = True
        
        return collision

class ZTetrimino:

    def __init__(self):
        self.block_list = [Block(LEFT+Block.WIDTH*4, TOP+Block.HEIGHT), Block(LEFT+Block.WIDTH*4, TOP+Block.HEIGHT*2), Block(LEFT+Block.WIDTH*5, TOP), Block(LEFT+Block.WIDTH*5, TOP+Block.HEIGHT)]
        self.is_fixed = False # テトリミノが固定状態になったかどうかを示す。テトリミノが床または他のテトリミノに衝突したら、
                              # テトリミノは固定状態になる。固定状態になると、横方向へは動けなくなる。

    def display(self):
        for block in self.block_list:
            block.display()
    
    def move_down(self, tetrimino_list):
        collision = False
        for tetrimino in tetrimino_list:
            if self.is_collision_bottom(tetrimino):
                collision = True
        
        if self.is_at_bottom():
            collision = True
        
        if not collision:
            for block in self.block_list:
                block.move_down()
    
    def move_left(self, tetrimino_list):
        collision = False
        for tetrimino in tetrimino_list:
            if self.is_collision_left(tetrimino):
                collision = True
        
        if self.is_on_left():
            collision = True
        
        if not collision and not self.is_fixed:
            for block in self.block_list:
                block.move_left()
    
    def move_right(self, tetrimino_list):
        collision = False
        for tetrimino in tetrimino_list:
            if self.is_collision_right(tetrimino):
                collision = True
        
        if self.is_on_right:
            collision = True
        
        if not collision and not self.is_fixed:
            for block in self.block_list:
                block.move_right()
    
    # 引数にテトリミノを渡す。対象のテトリミノの一番下のブロックが下側において、引数に渡したテトリミノのブロックと衝突しているかどうかを判定
    def is_collision_bottom(self, tetrimino):
        collision = False
        for block in tetrimino.block_list:
            if self.block_list[1].is_collision_bottom(block) or self.block_list[3].is_collision_bottom(block):
                collision = True
        
        return collision
    
    # 引数にテトリミノを渡す。対象のテトリミノのブロックが左側において、引数に渡したテトリミノのブロックと衝突しているかどうかを判定
    def is_collision_left(self, tetrimino):
        collision = False
        for block in tetrimino.block_list:

            if self.block_list[0].is_collision_left(block) or self.block_list[1].is_collision_left(block) or self.block_list[2].is_collision_left(block):
                collision = True
        
        return collision
    
    # 引数にテトリミノを渡す。対象のテトリミノのブロックが右側において、引数に渡したテトリミノのブロックと衝突しているかどうかを判定
    def is_collision_right(self, tetrimino):
        collision = False
        for block in tetrimino.block_list:

            if self.block_list[1].is_collision_right(block) or self.block_list[2].is_collision_right(block) or self.block_list[3].is_collision_right(block):
                collision = True
        
        return collision
    
    # ブロックが床に衝突しているかどうかを判定
    def is_at_bottom(self):
        return self.block_list[1].is_at_bottom()
    
    # テトリミノのブロックが左側の壁に衝突しているかどうかを判定
    def is_on_left(self):
        collision = False
        for block in self.block_list:
            if block.is_on_left():
                collision = True
        
        return collision
    
    # テトリミノのブロックが右側の壁に衝突しているかどうかを判定
    def is_on_right(self):
        collision = False
        for block in self.block_list:
            if block.is_on_right():
                collision = True
        
        return collision


# ------------------------------------ 関数 -----------------------------------------



# --------------------------------------- 処理の定義 -----------------------------------------

game_scene = "playing_scene"
running = True
while running:
    
    # プレイシーン
    if game_scene == "playing_scene":
        
        background = Background()
        tetrimino_manager = TetriminoManager()


        playing_scene = True
        while playing_scene:

            background.display()

            tetrimino_manager.manage_cycle_timer()

            tetrimino_manager.generate_tetrimino()
            tetrimino_manager.move_down_tetrimino()
            
            # 左矢印キー、右矢印キーが押されたら、テトリミノを左右へ移動させる
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_LEFT:
                        tetrimino_manager.move_left_tetrimino()
                    
                    elif event.key == pygame.K_RIGHT:
                        tetrimino_manager.move_right_tetrimino()
            
            tetrimino_manager.fix_tetrimino()
            
            tetrimino_manager.display()

            pygame.display.update()

            screen.fill((255, 255, 255))
