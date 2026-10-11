from manim import *

# Resolution/FPS come from the Makefile (Q=k → 4K60 by default); fixed bg color
config.background_color = '#1C1C1C'

ACCENT = "#1A3C94"


class __SCENE__(Scene):
    def construct(self):
        title = Tex(r"__SCENE__", color=ACCENT)

        self.play(Write(title))
        self.wait()
        self.play(FadeOut(title))
