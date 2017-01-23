from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.uix.slider import Slider
from kivy.uix.scatter import Scatter
from kivy.graphics import Color, Point

import time
from sandpiles import Sandpile

SAND_0 = [x / 255.0 for x in (204, 142, 116, 255)]
SAND_1 = [x / 255.0 for x in (116, 204, 181, 255)]
SAND_2 = [x / 255.0 for x in (101, 102, 153, 255)]
SAND_3 = [x / 255.0 for x in (171, 252, 255, 255)]


Builder.load_string('''
<Body@FloatLayout>:
    FractalCanvas:
        id: fcanvas
        do_translation: False
        do_scale: False
        auto_bring_to_front: False

    Controls:
        id: controls

<FractalCanvas>:

<Controls@BoxLayout>:
    size_hint_y: None
    height: 60
    pos_hint: {'y': 0}

    Slider:
        on_value: app.root.ids.fcanvas.scale = self.value
        value: 4
        min: 1
        max: 50

    BoxLayout:
        Label:
            text: 'Custom:'

        CheckBox:
            id: custom
            active: False
            disabled: True

        BoxLayout:
            orientation: 'vertical'
            Label:
                text: 'single'

            TextInput:
                id: single
                text: '0'
                input_filter: 'int'

        BoxLayout:
            orientation: 'vertical'

            Label:
                text: 'times'

            TextInput:
                id: times
                text: '1'
                input_filter: 'int'

        Button:
            text: 'Draw'
            on_release: app.root.ids.fcanvas.draw()

        Button:
            text: 'Draw++'
            on_release: app.root.ids.fcanvas.drawpp()

        Button:
            text: 'Clear'
            on_release: app.root.ids.fcanvas.canvas.clear()

        Label:
            id: time
''')


class FractalCanvas(Scatter):
    def __init__(self, **kwargs):
        super(FractalCanvas, self).__init__(**kwargs)
        Clock.schedule_once(self.post_init, 0)

    def post_init(self, *_):
        self.app = App.get_running_app()
        self.controls = self.app.root.ids.controls

    def build_grid(self, custom, single, times):
        start = time.time()
        #
        sand = Sandpile(
            custom=custom.active,
            single=int(single.text),
            times=int(times.text),
            grid=[]  # grid is shared(!!!) across instances for more speed
        )
        #
        end = time.time()

        self.controls.ids.time.text = str(round(end - start, 5)) + 's'
        self.grid_size = sand.size
        return sand.grid

    def get_points(self, grid):
        points_0 = []
        points_1 = []
        points_2 = []
        points_3 = []
        offset_x = self.center[0] - int(self.grid_size / 2.0)
        offset_y = self.center[1] - int(self.grid_size / 2.0)

        for y, row in enumerate(grid):
            for x, col in enumerate(row):
                if col == 0:
                    points_0.extend([
                        offset_x + x,
                        offset_y + y
                    ])
                elif col == 1:
                    points_1.extend([
                        offset_x + x,
                        offset_y + y
                    ])
                elif col == 2:
                    points_2.extend([
                        offset_x + x,
                        offset_y + y
                    ])
                elif col == 3:
                    points_3.extend([
                        offset_x + x,
                        offset_y + y
                    ])
        return (
            points_0,
            points_1,
            points_2,
            points_3
        )

    def drawpp(self):
        self.controls.ids.times.text = str(
            int(self.controls.ids.times.text) + 1
        )
        self.draw()

    def draw(self):
        self.canvas.clear()
        grid = self.build_grid(
            custom=self.controls.ids.custom,
            single=self.controls.ids.single,
            times=self.controls.ids.times
        )
        points = self.get_points(grid)

        # points collected, let's draw
        instr_limit = 2 ** 15 - 2
        with self.canvas:
            Color(*SAND_0)
            sublists_0 = (
                points[0][
                    x:x + instr_limit
                ] for x in range(
                    0, len(points[0]),
                    instr_limit
                )
            )
            for sub in sublists_0:
                Point(points=sub, pointsize=0.5)
            Color(*SAND_1)
            sublists_1 = (
                points[1][
                    x:x + instr_limit
                ] for x in range(
                    0, len(points[1]),
                    instr_limit
                )
            )
            for sub in sublists_1:
                Point(points=sub, pointsize=0.5)
            Color(*SAND_2)
            sublists_2 = (
                points[2][
                    x:x + instr_limit
                ] for x in range(
                    0, len(points[2]),
                    instr_limit
                )
            )
            for sub in sublists_2:
                Point(points=sub, pointsize=0.5)
            Color(*SAND_3)
            sublists_3 = (
                points[3][
                    x:x + instr_limit
                ] for x in range(
                    0, len(points[3]),
                    instr_limit
                )
            )
            for sub in sublists_3:
                Point(points=sub, pointsize=0.5)

    def _reverse(self, grid):
        return list(reversed(grid))


class SandpileFractal(App):
    def build(self):
        return Factory.Body()


if __name__ == '__main__':
    SandpileFractal().run()
