"""Vertical Instagram Reel: inversion symmetry for a quartic integral.

Quick vertical test:
    manim -ql quartic_integral_reel.py QuarticIntegralReel

Full-quality Instagram Reel render:
    manim -qh --fps 30 quartic_integral_reel.py QuarticIntegralReel

Optional Instagram-friendly H.264 MP4:
    ffmpeg -i media/videos/quartic_integral_reel/1080p30/QuarticIntegralReel.mp4 \
    -c:v libx264 -profile:v high -level 4.1 -pix_fmt yuv420p \
    -movflags +faststart -an quartic_integral_instagram.mp4
"""

from manim import *
import numpy as np

# Instagram Reel / phone-first frame.
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16
config.frame_rate = 30


class QuarticIntegralReel(Scene):
    """A fast, vertical Manim CE Reel for ∫₀∞ 1/(1+x⁴) dx = π/(2√2)."""

    def construct(self):
        self.camera.background_color = "#080A12"

        # High-contrast but restrained palette.
        white = WHITE
        muted = GRAY_B
        x_color = BLUE_C
        inv_color = TEAL_C
        u_color = PURPLE_B
        add_color = YELLOW_C
        final_color = GOLD
        area_color = BLUE_E

        def cap(text, color=WHITE, size=36):
            """Short bold caption sized for mobile."""
            return Tex(rf"\textbf{{{text}}}", font_size=size, color=color)

        def safe_center(mob, y=0):
            """Place key content away from Reel UI edges."""
            return mob.move_to([0, y, 0])

        # ------------------------------------------------------------------
        # 0–2 seconds: Immediate hook.
        # ------------------------------------------------------------------
        hook = MathTex(r"\int_0^\infty {1\over 1+x^4}\,dx", font_size=68, color=white)
        hook.move_to([0, 2.65, 0])
        impossible = cap("Looks impossible.", color=RED_B, size=38).next_to(hook, DOWN, buff=0.28)
        symmetry = cap("But it hides a symmetry.", color=add_color, size=36).next_to(hook, DOWN, buff=0.28)

        axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 1.15, 0.5],
            x_length=5.6,
            y_length=2.5,
            tips=False,
            axis_config={"color": muted, "stroke_width": 2},
        ).move_to([0, -2.85, 0])
        curve = axes.plot(lambda x: 1 / (1 + x**4), x_range=[0, 4, 0.02], color=x_color, stroke_width=4)
        area = axes.get_area(curve, x_range=[0, 4], color=area_color, opacity=0.45)

        self.play(FadeIn(hook, scale=1.08), run_time=0.45)
        self.play(FadeIn(impossible, shift=UP * 0.12), run_time=0.35)
        self.play(ReplacementTransform(impossible, symmetry), run_time=0.35)
        self.play(Create(axes), FadeIn(area), Create(curve), run_time=0.7)
        self.play(FadeOut(symmetry), run_time=0.15)

        # ------------------------------------------------------------------
        # 2–5 seconds: Invert the variable, x ↦ 1/x.
        # ------------------------------------------------------------------
        invert = MathTex(r"x\longmapsto {1\over x}", font_size=64)
        invert.set_color_by_tex("x", x_color)
        invert.set_color_by_tex(r"1\over x", inv_color)
        invert.move_to([0, 3.1, 0])

        line = NumberLine(x_range=[0, 2.4, 0.5], length=5.4, include_numbers=False, color=muted)
        line.move_to([0, 0.35, 0])
        dot_half = Dot(line.n2p(0.5), color=inv_color, radius=0.09)
        dot_one = Dot(line.n2p(1), color=final_color, radius=0.08)
        dot_two = Dot(line.n2p(2), color=x_color, radius=0.09)
        lab_half = MathTex(r"\frac12", font_size=34, color=inv_color).next_to(dot_half, DOWN, buff=0.16)
        lab_one = MathTex("1", font_size=34, color=final_color).next_to(dot_one, UP, buff=0.16)
        lab_two = MathTex("2", font_size=34, color=x_color).next_to(dot_two, DOWN, buff=0.16)
        swap = MathTex(r"2\leftrightarrow {1\over2}", font_size=44, color=white).move_to([0, -0.95, 0])
        fixed = MathTex(r"1\longmapsto1", font_size=42, color=final_color).move_to([0, -1.72, 0])

        i_plain = MathTex(r"I=\int_0^\infty {1\over 1+x^4}\,dx", font_size=52, color=white)
        i_plain.move_to([0, -3.0, 0])
        i_inverted = MathTex(r"I=\int_0^\infty {x^2\over 1+x^4}\,dx", font_size=52, color=white)
        i_inverted.move_to(i_plain)

        self.play(FadeOut(axes), FadeOut(area), FadeOut(curve), TransformMatchingTex(hook, i_plain), FadeIn(invert), run_time=0.75)
        self.play(Create(line), FadeIn(dot_half, dot_one, dot_two), FadeIn(lab_half, lab_one, lab_two), FadeIn(swap), run_time=0.55)
        self.play(dot_two.animate.move_to(line.n2p(0.5)), dot_half.animate.move_to(line.n2p(2)), Flash(dot_one, color=final_color), FadeIn(fixed), run_time=0.65)
        self.play(TransformMatchingTex(i_plain, i_inverted), run_time=0.65)
        self.play(FadeOut(VGroup(invert, line, dot_half, dot_one, dot_two, lab_half, lab_one, lab_two, swap, fixed)), run_time=0.25)

        # ------------------------------------------------------------------
        # 5–8 seconds: Add the two symmetric forms.
        # ------------------------------------------------------------------
        twin_caption = cap("Add the twins.", color=add_color, size=36).move_to([0, 3.35, 0])
        form1 = MathTex(r"I=\int_0^\infty {1\over 1+x^4}\,dx", font_size=48, color=white)
        form2 = MathTex(r"I=\int_0^\infty {x^2\over 1+x^4}\,dx", font_size=48, color=white)
        VGroup(form1, form2).arrange(DOWN, buff=0.42).move_to([0, 0.55, 0])
        combined = MathTex(r"2I=\int_0^\infty {1+x^2\over 1+x^4}\,dx", font_size=54, color=white)
        combined.move_to([0, 0.35, 0])
        combined.set_color_by_tex("1+x^2", add_color)

        self.play(ReplacementTransform(i_inverted, form2), FadeIn(form1, shift=DOWN * 0.15), FadeIn(twin_caption), run_time=0.7)
        self.play(LaggedStart(form1.animate.shift(DOWN * 0.1), form2.animate.shift(UP * 0.1), lag_ratio=0.15), run_time=0.35)
        self.play(TransformMatchingTex(VGroup(form1, form2), combined), run_time=0.75)
        self.play(Circumscribe(combined, color=add_color), run_time=0.6)
        self.play(FadeOut(twin_caption), run_time=0.2)

        # ------------------------------------------------------------------
        # 8–13 seconds: The clever substitution u = x - 1/x.
        # ------------------------------------------------------------------
        u_sub = MathTex(r"u=x-{1\over x}", font_size=66, color=u_color).move_to([0, 2.85, 0])
        map_top = MathTex(r"0^+\to-\infty", font_size=40, color=white)
        map_mid = MathTex(r"1\to0", font_size=40, color=final_color)
        map_bot = MathTex(r"\infty\to\infty", font_size=40, color=white)
        maps = VGroup(map_top, map_mid, map_bot).arrange(DOWN, buff=0.25).move_to([0, 0.85, 0])
        du = MathTex(r"du={1+x^2\over x^2}\,dx", font_size=48, color=add_color).move_to([0, -1.4, 0])
        usq = MathTex(r"u^2+2={x^4+1\over x^2}", font_size=48, color=u_color).move_to([0, -2.55, 0])
        u_integral = MathTex(r"2I=\int_{-\infty}^{\infty}{1\over u^2+2}\,du", font_size=52, color=white)
        u_integral.set_color_by_tex("u", u_color)
        u_integral.move_to([0, 0.15, 0])
        arctan_caption = cap("Now it is an arctangent.", color=add_color, size=34).next_to(u_integral, DOWN, buff=0.35)

        self.play(FadeIn(u_sub, scale=1.08), combined.animate.move_to([0, -3.45, 0]).scale(0.86), run_time=0.65)
        self.play(LaggedStart(FadeIn(map_top), FadeIn(map_mid), FadeIn(map_bot), lag_ratio=0.18), run_time=0.65)
        self.play(FadeIn(du, shift=UP * 0.1), FadeIn(usq, shift=UP * 0.1), run_time=0.55)
        self.play(FadeOut(maps), FadeOut(du), FadeOut(usq), TransformMatchingTex(combined, u_integral), run_time=0.85)
        self.play(FadeIn(arctan_caption), Circumscribe(u_integral, color=u_color), run_time=0.75)
        self.play(FadeOut(u_sub), FadeOut(arctan_caption), run_time=0.3)

        # ------------------------------------------------------------------
        # 13–17 seconds: Evaluate with arctangent endpoints.
        # ------------------------------------------------------------------
        eval_line1 = MathTex(r"2I={1\over\sqrt2}", font_size=54, color=white)
        eval_line2 = MathTex(r"\left[\tan^{-1}\!\left({u\over\sqrt2}\right)\right]_{-\infty}^{\infty}", font_size=48, color=white)
        eval_group = VGroup(eval_line1, eval_line2).arrange(DOWN, buff=0.18).move_to([0, 1.0, 0])
        left_end = MathTex(r"-\frac{\pi}{2}", font_size=44, color=inv_color).move_to([-1.85, -1.75, 0])
        right_end = MathTex(r"\frac{\pi}{2}", font_size=44, color=final_color).move_to([1.85, -1.75, 0])
        mini_axis = NumberLine(x_range=[-3, 3, 1], length=4.7, include_numbers=False, color=muted).move_to([0, -1.1, 0])
        mini_curve = ParametricFunction(
            lambda t: np.array([t, 0.45 * np.arctan(t), 0]),
            t_range=[-3, 3, 0.05],
            color=PURPLE_A,
            stroke_width=4,
        ).scale(0.7).move_to([0, -1.1, 0])
        two_i_answer = MathTex(r"2I={\pi\over\sqrt2}", font_size=66, color=final_color).move_to([0, 0.45, 0])

        self.play(TransformMatchingTex(u_integral, eval_group), run_time=0.85)
        self.play(Create(mini_axis), Create(mini_curve), FadeIn(left_end), FadeIn(right_end), run_time=0.7)
        self.play(Flash(left_end, color=inv_color), Flash(right_end, color=final_color), run_time=0.6)
        self.play(TransformMatchingTex(eval_group, two_i_answer), FadeOut(mini_axis), FadeOut(mini_curve), FadeOut(left_end), FadeOut(right_end), run_time=0.8)

        # ------------------------------------------------------------------
        # 17–21 seconds: Final reveal and loop-friendly ending.
        # ------------------------------------------------------------------
        final_i = MathTex(r"I={\pi\over2\sqrt2}", font_size=72, color=final_color).move_to([0, 1.35, 0])
        final_line1 = MathTex(r"\int_0^\infty", font_size=66, color=white)
        final_line2 = MathTex(r"{1\over1+x^4}\,dx", font_size=66, color=white)
        final_line3 = MathTex(r"={\pi\over2\sqrt2}", font_size=72, color=final_color)
        final_result = VGroup(final_line1, final_line2, final_line3).arrange(DOWN, buff=0.12).move_to([0, 0.1, 0])
        final_box = SurroundingRectangle(final_result, color=final_color, buff=0.26, corner_radius=0.16)
        faint_axes = axes.copy().set_opacity(0.22).move_to([0, -3.0, 0])
        faint_curve = curve.copy().set_opacity(0.28).move_to(faint_axes.get_center())
        opening_echo = MathTex(r"\int_0^\infty {1\over 1+x^4}\,dx", font_size=56, color=white).move_to([0, 2.65, 0])

        self.play(TransformMatchingTex(two_i_answer, final_i), run_time=0.7)
        self.play(ReplacementTransform(final_i, final_result), FadeIn(faint_axes), FadeIn(faint_curve), run_time=0.85)
        self.play(Create(final_box), Circumscribe(final_result, color=final_color), run_time=0.9)
        # Optional sound: reveal impact
        self.play(Flash(final_result, color=final_color), final_result.animate.scale(1.035), final_box.animate.scale(1.035), run_time=0.55)
        self.wait(0.3)
        self.play(final_result.animate.scale(0.82).move_to([0, -0.55, 0]), final_box.animate.scale(0.82).move_to([0, -0.55, 0]), FadeIn(opening_echo), run_time=0.7)
        # Optional sound: soft transition
        self.wait(0.25)


if __name__ == "__main__":
    print("Quick vertical test: manim -ql quartic_integral_reel.py QuarticIntegralReel")
    print("Full-quality Instagram Reel render: manim -qh --fps 30 quartic_integral_reel.py QuarticIntegralReel")
