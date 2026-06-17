"""Manim CE animation: Feynman's differentiation-under-the-integral trick.

Render with:
    manim -pqh feynman_sine_integral.py FeynmanSineIntegral
"""

from manim import *
import numpy as np


class FeynmanSineIntegral(Scene):
    """A short 3Blue1Brown-inspired explainer for ∫₀∞ sin(x)/x dx."""

    def construct(self):
        # ------------------------------------------------------------------
        # Color palette used consistently throughout the animation.
        # ------------------------------------------------------------------
        original_color = BLUE_C
        parameter_color = YELLOW
        damping_color = GREEN_C
        derivative_color = ORANGE
        final_color = GOLD

        # ------------------------------------------------------------------
        # Part 1: Hook — present the integral and the main idea.
        # ------------------------------------------------------------------
        title = Tex("Feynman's Integration Trick", font_size=46).to_edge(UP)
        original = MathTex(
            r"\int_0^\infty {\sin x \over x}\,dx",
            font_size=74,
            color=original_color,
        )
        subtitle = Tex(
            "A hard integral made easier by introducing a parameter.",
            font_size=30,
        ).next_to(original, DOWN, buff=0.55)
        difficult = Tex("Direct antiderivatives do not help much.", font_size=28, color=GRAY_B)
        difficult.next_to(subtitle, DOWN, buff=0.35)

        self.play(Write(title), run_time=1.0)
        self.play(Write(original), run_time=1.2)
        self.play(FadeIn(subtitle, shift=UP * 0.2), FadeIn(difficult, shift=UP * 0.2))
        self.wait(1.1)

        # ------------------------------------------------------------------
        # Part 2: Introduce the parameter and highlight the damping factor.
        # ------------------------------------------------------------------
        parameter_eq = MathTex(
            r"I(",
            r"a",
            r")=\int_0^\infty",
            r"e^{-ax}",
            r"{\sin x \over x}\,dx,\quad",
            r"a>0",
            font_size=48,
        )
        parameter_eq.set_color_by_tex("a", parameter_color)
        parameter_eq.set_color_by_tex(r"e^{-ax}", damping_color)
        parameter_eq.move_to(UP * 0.35)

        damping_label = Tex("damping factor", font_size=28, color=damping_color)
        damping_label.next_to(parameter_eq[3], DOWN, buff=0.35)
        damping_arrow = Arrow(
            damping_label.get_top(),
            parameter_eq[3].get_bottom(),
            buff=0.08,
            color=damping_color,
            stroke_width=4,
        )
        parameter_note = Tex(
            "For $a>0$, oscillations are gently suppressed.",
            font_size=28,
            color=GRAY_A,
        ).next_to(damping_label, DOWN, buff=0.35)

        self.play(FadeOut(difficult), Transform(original, parameter_eq), FadeOut(subtitle))
        self.play(GrowArrow(damping_arrow), FadeIn(damping_label), FadeIn(parameter_note))
        self.wait(1.2)
        self.play(FadeOut(original), FadeOut(damping_arrow), FadeOut(damping_label), FadeOut(parameter_note))

        # ------------------------------------------------------------------
        # Part 3: Dynamic graph of exp(-a x) sin(x)/x as a changes.
        # ------------------------------------------------------------------
        graph_title = Tex(r"Watch $e^{-ax}\,\sin(x)/x$ relax toward $\sin(x)/x$", font_size=32)
        graph_title.to_edge(UP, buff=0.75)
        axes = Axes(
            x_range=[0, 16, 2],
            y_range=[-0.35, 1.15, 0.25],
            x_length=10.5,
            y_length=4.6,
            tips=False,
            axis_config={"color": GRAY_B},
        ).to_edge(DOWN, buff=0.8)
        axes_labels = axes.get_axis_labels(MathTex("x"), MathTex("y"))

        a_tracker = ValueTracker(1.5)

        def damped_sinc(x):
            # Handle the removable singularity: lim_{x→0} sin(x)/x = 1.
            if abs(x) < 1e-6:
                return 1.0
            return np.exp(-a_tracker.get_value() * x) * np.sin(x) / x

        curve = always_redraw(
            lambda: axes.plot(
                damped_sinc,
                x_range=[0, 16, 0.02],
                color=original_color,
                stroke_width=4,
                use_smoothing=True,
            )
        )
        a_display = always_redraw(
            lambda: VGroup(
                MathTex("a=", font_size=34, color=parameter_color),
                DecimalNumber(a_tracker.get_value(), num_decimal_places=2, font_size=34, color=parameter_color),
            ).arrange(RIGHT, buff=0.08).to_corner(UR).shift(DOWN * 0.65)
        )
        graph_caption = Tex(
            r"As $a\to 0^+$, the damping disappears.",
            font_size=30,
            color=damping_color,
        ).next_to(axes, UP, buff=0.25)

        self.play(FadeIn(graph_title), Create(axes), FadeIn(axes_labels), Create(curve), FadeIn(a_display))
        self.play(FadeIn(graph_caption, shift=UP * 0.2))
        self.play(a_tracker.animate.set_value(0.05), run_time=5.0, rate_func=smooth)
        self.wait(0.8)
        self.play(FadeOut(VGroup(graph_title, axes, axes_labels, curve, a_display, graph_caption)))

        # ------------------------------------------------------------------
        # Part 4: Differentiate under the integral sign.
        # ------------------------------------------------------------------
        step_title = Tex("Differentiate under the integral sign", font_size=38).to_edge(UP)
        d1 = MathTex(
            r"I'(a)=\int_0^\infty {\partial\over\partial a}"
            r"\left(e^{-ax}{\sin x\over x}\right)\,dx",
            font_size=44,
        )
        d1.set_color_by_tex(r"\partial", derivative_color)
        d1.set_color_by_tex(r"e^{-ax}", damping_color)
        d2 = MathTex(
            r"I'(a)=\int_0^\infty \left(-x e^{-ax}\right){\sin x\over x}\,dx",
            font_size=44,
        ).next_to(d1, DOWN, buff=0.65)
        d2.set_color_by_tex("-x", derivative_color)
        d2.set_color_by_tex(r"e^{-ax}", damping_color)
        d3 = MathTex(
            r"I'(a)=-\int_0^\infty e^{-ax}\sin x\,dx",
            font_size=48,
        ).next_to(d2, DOWN, buff=0.65)
        d3.set_color_by_tex(r"-", derivative_color)
        cancel_note = Tex("The $x$ cancels.", font_size=28, color=derivative_color).next_to(d2, RIGHT, buff=0.45)

        self.play(Transform(title, step_title))
        self.play(Write(d1))
        self.play(TransformFromCopy(d1, d2), FadeIn(cancel_note))
        self.play(TransformFromCopy(d2, d3))
        self.wait(1.0)

        # ------------------------------------------------------------------
        # Part 5: Evaluate I'(a) using the standard Laplace-transform integral.
        # ------------------------------------------------------------------
        eval_eq = MathTex(
            r"I'(a)=-\int_0^\infty e^{-ax}\sin x\,dx=-{1\over a^2+1}",
            font_size=48,
        ).move_to(ORIGIN)
        eval_note = Tex("A standard Laplace transform result.", font_size=28, color=GRAY_A)
        eval_note.next_to(eval_eq, DOWN, buff=0.45)
        self.play(FadeOut(VGroup(d1, d2, d3, cancel_note)))
        self.play(Write(eval_eq), FadeIn(eval_note))
        self.wait(1.2)

        # ------------------------------------------------------------------
        # Part 6: Integrate back with respect to a.
        # ------------------------------------------------------------------
        integrate_title = Tex("Integrate back in $a$", font_size=38).to_edge(UP)
        i1 = MathTex(r"I'(a)=-{1\over a^2+1}", font_size=48)
        i2 = MathTex(r"I(a)=-\tan^{-1}(a)+C", font_size=54, color=parameter_color)
        VGroup(i1, i2).arrange(DOWN, buff=0.8).move_to(ORIGIN)
        self.play(Transform(title, integrate_title), FadeOut(eval_note), Transform(eval_eq, i1))
        self.play(TransformFromCopy(eval_eq, i2))
        self.wait(1.1)

        # ------------------------------------------------------------------
        # Part 7: Boundary condition as a → ∞ determines C.
        # ------------------------------------------------------------------
        boundary_title = Tex("Use the boundary condition", font_size=38).to_edge(UP)
        b1 = MathTex(r"a\to\infty \quad\Longrightarrow\quad e^{-ax}\text{ kills the integrand}", font_size=40)
        b1.set_color_by_tex(r"e^{-ax}", damping_color)
        b2 = MathTex(r"\lim_{a\to\infty} I(a)=0", font_size=46)
        b3 = MathTex(r"0=-{\pi\over2}+C\quad\Longrightarrow\quad C={\pi\over2}", font_size=46)
        VGroup(b1, b2, b3).arrange(DOWN, buff=0.55).move_to(ORIGIN)
        self.play(Transform(title, boundary_title), FadeOut(eval_eq), FadeOut(i2))
        self.play(Write(b1))
        self.play(Write(b2))
        self.play(Write(b3))
        self.wait(1.2)

        # ------------------------------------------------------------------
        # Part 8: Final substitution and the limit a → 0+.
        # ------------------------------------------------------------------
        final_title = Tex("Let the damping vanish", font_size=38).to_edge(UP)
        f1 = MathTex(r"I(a)={\pi\over2}-\tan^{-1}(a)", font_size=52)
        f2 = MathTex(r"I(0)=\int_0^\infty {\sin x\over x}\,dx={\pi\over2}", font_size=54)
        box = SurroundingRectangle(f2, color=final_color, buff=0.28, corner_radius=0.12)
        final_group = VGroup(f1, f2, box).arrange(DOWN, buff=0.8).move_to(ORIGIN)
        final_label = Tex("Feynman's trick turns the hard integral into a simple derivative.", font_size=28)
        final_label.next_to(final_group, DOWN, buff=0.45)

        self.play(Transform(title, final_title), FadeOut(VGroup(b1, b2, b3)))
        self.play(Write(f1))
        self.play(TransformFromCopy(f1, f2))
        self.play(Create(box), f2.animate.set_color(final_color))
        self.play(FadeIn(final_label, shift=UP * 0.2))
        self.wait(2.0)


if __name__ == "__main__":
    # Allows quick syntax checks with `python feynman_sine_integral.py`.
    print("Render with: manim -pqh feynman_sine_integral.py FeynmanSineIntegral")
