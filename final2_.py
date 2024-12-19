import pyxel
import random

# プレイヤークラス
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        # 左右のキー入力で移動
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= 2
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += 2
        # 画面外に出ないように調整
        self.x = max(0, min(self.x, pyxel.width - 8))

    def draw(self):
        # プレイヤーの描画
        pyxel.rect(self.x, self.y, 8, 8, 11)

# ブロッククラス
class Block:
    def __init__(self, x, y, speed, size, color, h_speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.size = size
        self.color = color
        self.h_speed = h_speed

    def update(self):
        # ブロックの落下と横移動
        self.y += self.speed
        self.x += self.h_speed
        # 画面端で反転
        if self.x < 0 or self.x > pyxel.width - self.size:
            self.h_speed *= -1

    def draw(self):
        # ブロックの描画
        pyxel.rect(self.x, self.y, self.size, self.size, self.color)

    def is_off_screen(self):
        # 画面外に出たかどうか
        return self.y > pyxel.height

# メインゲームクラス
class App:
    def __init__(self):
        pyxel.init(160, 120)
        pyxel.caption = "ブロック落下回避ゲーム"
        self.reset_game()
        pyxel.run(self.update, self.draw)

    def reset_game(self):
        self.player = Player(76, 112)
        self.blocks = []
        self.score = 0
        self.game_over = False
        self.block_spawn_timer = 0
        # ゲームバランス調整用の変数
        self.block_spawn_interval = 30
        self.block_min_speed = 1
        self.block_max_speed = 3
        self.block_min_size = 8
        self.block_max_size = 16
        self.block_colors = [8, 9, 10, 11, 12, 13, 14]

    def update(self):
        if not self.game_over:
            self.player.update()
            self.update_blocks()
            self.check_collisions()
            self.score += 1
            # 難易度の上昇
            if self.score % 500 == 0 and self.block_spawn_interval > 10:
                self.block_spawn_interval -= 2
        else:
            # スペースキーでリスタート
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.reset_game()
            # エスケープキーで終了
            if pyxel.btnp(pyxel.KEY_ESCAPE):
                pyxel.quit()

    def update_blocks(self):
        self.block_spawn_timer += 1
        if self.block_spawn_timer > self.block_spawn_interval:
            self.block_spawn_timer = 0
            size = random.randint(self.block_min_size, self.block_max_size)
            x = random.randint(0, pyxel.width - size)
            speed = random.uniform(self.block_min_speed, self.block_max_speed)
            color = random.choice(self.block_colors)
            h_speed = random.uniform(-1, 1)
            new_block = Block(x, 0, speed, size, color, h_speed)
            self.blocks.append(new_block)
        for block in self.blocks:
            block.update()
        # 画面外のブロックを削除
        self.blocks = [block for block in self.blocks if not block.is_off_screen()]

    def check_collisions(self):
        for block in self.blocks:
            if (self.player.x < block.x + block.size and
                self.player.x + 8 > block.x and
                self.player.y < block.y + block.size and
                self.player.y + 8 > block.y):
                self.game_over = True

    def draw(self):
        pyxel.cls(0)
        if not self.game_over:
            self.player.draw()
            for block in self.blocks:
                block.draw()
            pyxel.text(5, 4, f"Score: {self.score}", 7)
        else:
            pyxel.text(68, 50, "Gameover", pyxel.frame_count % 16)
            pyxel.text(35, 70, "スペースキーでリスタート", 7)
            pyxel.text(40, 80, "エスケープキーで終了", 7)

App()
