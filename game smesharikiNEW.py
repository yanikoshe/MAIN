import arcade
#настройки
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
SCREEN_TITLE = "Wolf"

PLAYER_MOVEMENT_SPEED = 10
GRAVITY = 1
PLAYER_JUMP_SPEED = 20

LEFT_VIEWPORT_MARGIN = 250
RIGHT_VIEWPORT_MARGIN = 250
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 100

class MyGame(arcade.Window):

    def __init__(self):
        #конструктора для инициализации атрибутов класса

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.wall_list = None
        self.player_sprite = None
        self.player_list = None

        #звук собирания звезд
        self.coin_list = None
        self.collect_coin_sound = arcade.load_sound("E:\УНИК\программирование\игра\zvezda.wav")
        arcade.set_background_color(arcade.color.COOL_BLACK)

        self.view_bottom = 0
        self.view_left = 0

        self.score = 0


#тут добавляю спрайты, где они стоят, через сколько пикселей и т.д.
    def setup(self):
        self.player_list = arcade.SpriteList()
        image_source = "E:\УНИК\программирование\игра\спрайты\перс-стоит.png"
        self.wall_list = arcade.SpriteList(use_spatial_hash=True) #тут для удобства делаем хэширование, чтобы как-то "уменьшить" объем данных
        self.coin_list = arcade.SpriteList(use_spatial_hash=True)

        self.player_sprite = arcade.Sprite(image_source)
        self.player_sprite.center_x = 300
        self.player_sprite.center_y = 350
        self.player_list.append(self.player_sprite)
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, GRAVITY)

#пол, по которому бегает персонаж
        for x in range(0, 10000, 900):
            wall = arcade.Sprite("E:\УНИК\программирование\игра\спрайты\пол.png")
            wall.center_x = x
            wall.center_y = -200
            self.wall_list.append(wall)
#добавляю пеньки
        coordinate_list = [[800, 350], [2900, 350], [3800, 350], [5300, 350], [7100, 350], [9900, 350]]
        for coordinate in coordinate_list:
            wall = arcade.Sprite("E:\УНИК\программирование\игра\спрайты\пень.png")
            wall.position = coordinate
            self.wall_list.append(wall)


#добавляю звезды, которые будет собирать персонаж
        for x in range(600, 10000, 900):
            coin = arcade.Sprite("E:\УНИК\программирование\игра\спрайты\звезда.png")
            coin.center_x = x
            coin.center_y = 350
            self.coin_list.append(coin)
#теперь всё это "рисуем"
    def on_draw(self):


        arcade.start_render()

        self.player_list.draw()
        self.wall_list.draw()
        self.coin_list.draw()

        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 5 + self.view_right, 10 + self.view_top,
                         arcade.csscolor.WHITE, 30)


#прописываю кнопочки при нажатии, скорость
    def on_key_press(self, key, modifiers):

        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

# прописываю кнопочки при их отпускании
    def on_key_release(self, key, modifiers):

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0
#прописываю обновление состояния игры и всех объектов в ней, чтобы звездоки пропадали
    def on_update(self, delta_time):

        self.physics_engine.update()

        coin_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.coin_list
        )
        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            arcade.play_sound(self.collect_coin_sound)
            self.score +=1

        changed = False

        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True

        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True

        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            changed = True

        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed - True

        if changed:
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)

#само окошко
def main():
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
