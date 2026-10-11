# 1)

from manim import *

# Resolution/FPS come from the Makefile (Q=k → 4K60 by default); fixed bg color
config.background_color = '#1C1C1C'

ACCENT = "#1A3C94"

IN_START = [-5.2, 0.45, 0]
IN_END = [-2.4, 0.45, 0]
OUT_START = [3.0, 0.45, 0]
OUT_END = [4.4, 0.45, 0]


class FunctionsAsPrograms(Scene):
    def construct(self):
        title = MathTex(
            r"f:\mathbb{N}\to\mathbb{N},\quad f(x)=2x+1"
        ).to_edge(UP, buff=0.8)

        box = RoundedRectangle(
            corner_radius=0.2, width=3, height=2, stroke_width=5, color=WHITE
        )
        label = MathTex("f", font_size=96).move_to(box)

        in_wire = Line([-5.5, 0, 0], [-1.5, 0, 0], stroke_width=4, color=WHITE)
        out_wire = Line([1.5, 0, 0], [5.5, 0, 0], stroke_width=4, color=WHITE)
        in_node = Dot([-1.5, 0, 0], radius=0.09, color=ACCENT)
        out_node = Dot([1.5, 0, 0], radius=0.09, color=ACCENT)

        def val(s, math):
            return MathTex(s, color=ACCENT) if math else Tex(s, color=ACCENT)

        def flow(s_in, s_out, math, caption=None):
            vi = val(s_in, math).move_to(IN_START)
            vo = val(s_out, math).move_to(OUT_START)
            cap = MathTex(caption).move_to([0, -1.8, 0]) if caption else None

            self.play(FadeIn(vi), run_time=0.3)
            self.play(vi.animate.move_to(IN_END), run_time=0.5, rate_func=linear)
            self.play(
                FadeOut(vi),
                Indicate(box, scale_factor=1.05, color=ACCENT),
                run_time=0.5,
            )
            self.play(
                FadeIn(vo),
                *([Write(cap)] if cap else []),
                run_time=0.5,
            )
            self.play(vo.animate.move_to(OUT_END), run_time=0.5, rate_func=linear)
            self.play(
                FadeOut(vo),
                *([FadeOut(cap)] if cap else []),
                run_time=0.5,
            )

        self.play(
            Write(title),
            Create(box),
            FadeIn(label),
            Create(in_wire),
            Create(out_wire),
            FadeIn(in_node),
            FadeIn(out_node),
            run_time=0.9,
        )
        flow("1", "3", True, r"f(1)=3")
        flow("2", "5", True, r"f(2)=5")

        title_p = Tex(r"$P=$ ``\textless Ahoj, \{\text{meno}\}!\textgreater{}''").to_edge(UP, buff=0.8)
        label_p = MathTex("P", font_size=96).move_to(box)
        lab_in = Tex(r"input", font_size=40).move_to([-3.5, -0.5, 0])
        lab_out = Tex(r"output", font_size=40).move_to([3.5, -0.5, 0])

        self.play(
            ReplacementTransform(title, title_p),
            ReplacementTransform(label, label_p),
            FadeIn(lab_in),
            FadeIn(lab_out),
            run_time=0.9,
        )

        flow(r"``Michal''", r"``Ahoj, Michal!''", False)
        flow(r"``Andrej''", r"``Ahoj, Andrej!''", False)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
