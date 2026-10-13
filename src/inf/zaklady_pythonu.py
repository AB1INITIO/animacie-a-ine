# 1)

from manim import *

# Resolution/FPS come from the Makefile (Q=k → 4K60 by default); fixed bg color
config.background_color = '#1C1C1C'

ACCENT = "#1A3C94"

IN_START = [-5.2, 0.45, 0]
IN_END = [-2.4, 0.45, 0]
OUT_START = [3.0, 0.45, 0]
OUT_END = [4.4, 0.45, 0]

# Seconds a value, packet or DB record takes to travel along a wire
TRAVEL = 1.0

WEB_POS = [0, 2.75, 0]
WEB_R = 0.65
DB_POS = [0, -2.75, 0]
ROWS_TOP = [1.85, -2.2, 0]


def web_icon():
    """Globe: the web/server P* talks to."""
    r = WEB_R
    w = r * np.sqrt(3) / 2  # half-width of the parallels at y = ±r/2
    return VGroup(
        Circle(radius=r),
        Ellipse(width=r, height=2 * r),
        Line([-r, 0, 0], [r, 0, 0]),
        Line([-w, r / 2, 0], [w, r / 2, 0]),
        Line([-w, -r / 2, 0], [w, -r / 2, 0]),
    ).set_stroke(WHITE, 4).move_to(WEB_POS)


def db_icon(width=1.3, height=1.2, ry=0.18):
    """Cylinder split into three disks."""
    w, h = width / 2, height / 2

    def rim(y):  # front (lower) half of the ellipse at height y
        return (
            Arc(start_angle=PI, angle=PI)
            .stretch(w, 0, about_point=ORIGIN)
            .stretch(ry, 1, about_point=ORIGIN)
            .shift(y * UP)
        )

    return VGroup(
        Ellipse(width=width, height=2 * ry).shift(h * UP),
        Line([-w, h, 0], [-w, -h, 0]),
        Line([w, h, 0], [w, -h, 0]),
        *[rim(y) for y in (h / 3, -h / 3, -h)],
    ).set_stroke(WHITE, 4).move_to(DB_POS)


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
            self.play(vi.animate.move_to(IN_END), run_time=TRAVEL, rate_func=linear)
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
            self.play(vo.animate.move_to(OUT_END), run_time=TRAVEL, rate_func=linear)
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
        flow("3", "7", True, r"f(3)=7")

        title_p = Tex(r"$P=$ f``Ahoj, \{\text{meno}\}!''").to_edge(UP, buff=0.8)
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
        flow(r"``Julka''", r"``Ahoj, Julka!''", False)
        flow(r"``user\#123''", r"``Ahoj, user\#123''", False)

        label_ps = MathTex("P^*", font_size=96).move_to(box)
        strikes = VGroup(*[
            Line(lab.get_left() + 0.1 * LEFT, lab.get_right() + 0.1 * RIGHT, stroke_width=4)
            for lab in (lab_in, lab_out)
        ])

        def on_globe(x):  # point on the globe's lower edge above x
            return [x, WEB_POS[1] - np.sqrt(WEB_R**2 - x**2), 0]

        web = web_icon()
        db = db_icon()
        req_wire = Line([-0.3, 1, 0], on_globe(-0.3), stroke_width=4, color=WHITE)
        res_wire = Line([0.3, 1, 0], on_globe(0.3), stroke_width=4, color=WHITE)
        db_wire = Line([0, -1, 0], db.get_top(), stroke_width=4, color=WHITE)
        side_nodes = VGroup(*[
            Dot(p, radius=0.09, color=ACCENT) for p in ([-0.3, 1, 0], [0.3, 1, 0], [0, -1, 0])
        ])

        self.play(
            FadeOut(title_p),
            ReplacementTransform(label_p, label_ps),
            VGroup(in_wire, out_wire, in_node, out_node).animate.set_opacity(0.2),
            VGroup(lab_in, lab_out).animate.set_opacity(0.4),
            Create(strikes),
            run_time=0.9,
        )
        self.play(
            Create(web),
            Create(db),
            Create(req_wire),
            Create(res_wire),
            Create(db_wire),
            FadeIn(side_nodes),
            run_time=0.9,
        )

        def packet(start, end):
            d = Dot(start, radius=0.08, color=ACCENT)
            return Succession(
                FadeIn(d, run_time=0.15),
                d.animate(run_time=TRAVEL, rate_func=linear).move_to(end),
                FadeOut(d, run_time=0.15),
            )

        def call(n):
            # requests go up the left wire, responses come down the right one
            traffic = LaggedStart(
                *[
                    packet(req_wire.get_start(), req_wire.get_end()) if i % 2 == 0
                    else packet(res_wire.get_end(), res_wire.get_start())
                    for i in range(8)
                ],
                lag_ratio=0.35,
            )

            row = RoundedRectangle(
                corner_radius=0.06, width=1.4, height=0.36, stroke_width=2,
                color=WHITE, fill_color=ACCENT, fill_opacity=1,
            ).move_to(ROWS_TOP).shift(0.45 * n * DOWN)
            tag = MathTex(rf"\#{n + 1}", font_size=30).move_to(row)
            entry = row.copy().scale(0.3).move_to(db_wire.get_start())
            store = Succession(
                FadeIn(entry, run_time=0.15),
                entry.animate(run_time=TRAVEL, rate_func=linear).move_to(db),
                AnimationGroup(
                    ReplacementTransform(entry, row),
                    FadeIn(tag),
                    Indicate(db, scale_factor=1.05, color=ACCENT),
                    run_time=0.6,
                ),
            )

            self.play(Indicate(box, scale_factor=1.05, color=ACCENT), run_time=0.5)
            # the record is stored halfway through the traffic
            self.play(LaggedStart(traffic, store, lag_ratio=0.5))

        for n in range(3):
            call(n)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
