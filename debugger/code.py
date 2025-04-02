import pytch
import random

score = 0
lives = 3

game_over = False

class Alien(pytch.Sprite):
    Costumes = ["friendly-alien.png", "enemy-alien.png"]
    Sounds = ["explosion.mp3", "scream.mp3"]

    @pytch.when_I_receive("make-clones")
    def make_clones(self):
        for i in range(5):
            self.go_to_xy(-150 + i * 60, 180)
            pytch.create_clone_of(self)
        self.go_to_xy(150, 180)

    @pytch.when_I_receive("play-game")
    def drift_down_screen(self):
        while not game_over:
            self.set_y(180)
            self.show()
            glide_time = random.uniform(3.0, 5.0)
            self.glide_to_xy(self.x_position, -180, glide_time)
            self.switch_costume(random.choice([0, 1]))

    @pytch.when_this_sprite_clicked
    def handle_hit(self):
        if self.costume_number == 1:
            self.start_sound("explosion")
            global score
            score += 10
        else:
            self.start_sound("scream")
            global lives
            lives -= 1
            if lives == 0:
                game_over = True
                pytch.broadcast("game-over")
        self.hide()

class Galaxy(pytch.Stage):
    Backdrops = ["starry-sky.jpg"]
    Sounds = ["fizz.mp3"]

    @pytch.when_green_flag_clicked
    def run(self):
        pytch.show_variable(None, "score")
        pytch.show_variable(None, "lives", right=236)
        pytch.broadcast_and_wait("make-clones")
        pytch.broadcast("play-game")

    @pytch.when_stage_clicked
    def make_miss_sound(self):
        self.start_sound("fizz")
