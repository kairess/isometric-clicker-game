from ursina import *

app = Ursina()

window.fps_counter.disable()
window.exit_button.disable()
Text.default_font = '/System/Library/Fonts/AppleSDGothicNeo.ttc'

camera.orthographic = True
camera.position = (55, 40, -50)
camera.rotation = (30, -45, 0)
camera.fov = 20

total_gold = 0
gold_text = Text(parent=camera.ui, text=str(total_gold), y=0.45, origin=(0, 0), scale=1.5)

class Building(Button):
    def __init__(self, position=(0, 0, 0), texture='brick', earn=0, earn_interval=1, earn_duration=60):
        super().__init__(
            parent=scene,
            position=position + Vec3(0.7, 1.5, -0.7),
            rotation=(30, -45, 0),
            model='quad',
            texture=texture,
            color=color.white,
            scale=1.3,
            collider='quad'
        )

        self.earn = earn
        self.earn_interval = earn_interval
        self.earn_duration = earn_duration

        self.is_earning = True
        self.earn_end_time = time.time() + earn_duration

        self.earn_gold()

    def earn_gold(self):
        if time.time() >= self.earn_end_time:
            self.is_earning = False
            self.color = color._20
            return False

        global total_gold
        total_gold += self.earn
        invoke(self.earn_gold, delay=self.earn_interval)

    def input(self, key):
        if self.hovered and key == 'left mouse down':
            if not self.is_earning:
                self.is_earning = True
                self.earn_end_time = time.time() + self.earn_duration
                self.color = color.white
                self.earn_gold()


class Menu(Entity):
    def __init__(self):
        super().__init__(parent=camera.ui)

        self.menu = Entity(parent=self, enabled=False)

        ButtonList(button_dict={
            '뒤로': Func(self.menu.disable),
            '운동': Func(
                self.build,
                texture='assets/fitness.png',
                earn=1,
                earn_interval=1,
                earn_duration=10,
            ),
            '인스타그램': Func(
                self.build,
                texture='assets/instagram.png',
                earn=10,
                earn_interval=1,
                earn_duration=2,
            ),
            '공부': Func(
                self.build,
                texture='assets/school.png',
                earn=5,
                earn_interval=2,
                earn_duration=60,
            ),
            'TV 보기': Func(
                self.build,
                texture='assets/tv.png',
                earn=1,
                earn_interval=3,
                earn_duration=120,
            )
        }, y=0.2, parent=self.menu)

    def build(self, *args, **kwargs):
        b = Building(position=self.ground.position, **kwargs)
        self.menu.disable()

    def open(self, ground):
        self.ground = ground
        self.menu.enable()

menu = Menu()

class Ground(Button):
    def __init__(self, position=(0, 0, 0)):
        super().__init__(
            parent=scene,
            position=position,
            model='assets/cube',
            texture='assets/grass.png',
            color=color.color(0, 0, random.uniform(0.9, 1.0)),
            scale=1,
            collider='box'
        )

    def input(self, key):
        if self.hovered and key == 'left mouse down':
            menu.open(self)

for z in range(20):
    for x in range(20):
        ground = Ground(position=(x, 0, z))

def update():
    if held_keys['d']:
        camera.position += Vec3(7 * time.dt, 0, 7 * time.dt)
    elif held_keys['a']:
        camera.position -= Vec3(7 * time.dt, 0, 7 * time.dt)

    if held_keys['w']:
        camera.position += Vec3(0, 7 * time.dt, 0)
    elif held_keys['s']:
        camera.position -= Vec3(0, 7 * time.dt, 0)

    gold_text.text = '♥%s' % (total_gold,)

def input(key):
    if key == 'scroll down':
        camera.fov += 1
    elif key == 'scroll up':
        camera.fov -= 1

app.run()
