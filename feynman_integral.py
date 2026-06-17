"""Fast Manim CE explainer for Feynman's integration trick.

Render with:
    manim -qh feynman_integral.py FeynmanSineIntegral
"""

from manim import *
import numpy as np


class FeynmanSineIntegral(Scene):
    """A ~20 second animation for ∫₀∞ sin(x)/x dx = π/2."""

    def construct(self):
        # Consistent colors for the few ideas that appear on screen.
        original_color = BLUE_C
        parameter_color = YELLOW
        damping_color = GREEN_C
        derivative_color = ORANGE
        final_color = GOLD

        # ------------------------------------------------------------------
        # 0–3 seconds: Introduction.
        # ------------------------------------------------------------------
        title = Tex("Feynman's Trick", font_size=42).to_edge(UP)
        original = MathTex(
            r"\int_0^\infty {\sin x\over x}\,dx",
            font_size=78,
            color=original_color,
        )
        caption = Tex("Use a parameter.", font_size=32).next_to(original, DOWN, buff=0.45)

        self.play(Write(title), run_time=0.55)
        self.play(Write(original), FadeIn(caption, shift=UP * 0.15), run_time=0.9)
        self.play(original.animate.scale(0.72).to_edge(UP, buff=1.15), FadeOut(caption), run_time=0.7)

        # ------------------------------------------------------------------
        # 3–7 seconds: Introduce I(a), highlight damping, and animate a graph.
        # ------------------------------------------------------------------
        parameter_eq = MathTex(
            r"I(",
            r"a",
            r")=\int_0^\infty ",
            r"e^{-ax}",
            r"{\sin x\over x}\,dx",
            font_size=44,
        ).next_to(title, DOWN, buff=0.25)
        parameter_eq.set_color_by_tex("a", parameter_color)
        parameter_eq.set_color_by_tex(r"e^{-ax}", damping_color)

        damping_label = Tex("damping factor", font_size=26, color=damping_color)
        damping_label.next_to(parameter_eq[3], DOWN, buff=0.18)
        damping_box = SurroundingRectangle(parameter_eq[3], color=damping_color, buff=0.08)

        axes = Axes(
            x_range=[0, 14, 2],
            y_range=[-0.35, 1.15, 0.5],
            x_length=9.6,
            y_length=3.45,
            tips=False,
            axis_config={"color": GRAY_B, "stroke_width": 2},
        ).to_edge(DOWN, buff=0.45)
        axes_labels = axes.get_axis_labels(MathTex("x", font_size=24), MathTex("y", font_size=24))
        a_tracker = ValueTracker(1.4)

        def damped_sinc(x):
            # Removable singularity: lim_{x→0} sin(x)/x = 1.
            if abs(x) < 1e-6:
                return 1.0
            return np.exp(-a_tracker.get_value() * x) * np.sin(x) / x

        curve = always_redraw(
            lambda: axes.plot(
                damped_sinc,
                x_range=[0, 14, 0.03],
                color=original_color,
                stroke_width=4,
                use_smoothing=True,
            )
        )
        a_value = always_redraw(
            lambda: VGroup(
                MathTex("a=", font_size=30, color=parameter_color),
                DecimalNumber(a_tracker.get_value(), num_decimal_places=2, font_size=30, color=parameter_color),
            ).arrange(RIGHT, buff=0.06).next_to(axes, UP, buff=0.1).to_edge(RIGHT, buff=0.75)
        )

        self.play(TransformMatchingTex(original, parameter_eq), run_time=0.85)
        self.play(Create(damping_box), FadeIn(damping_label, shift=UP * 0.1), run_time=0.55)
        self.play(Create(axes), FadeIn(axes_labels), Create(curve), FadeIn(a_value), run_time=0.75)
        self.play(a_tracker.animate.set_value(0.04), run_time=1.65, rate_func=smooth)
        self.play(FadeOut(damping_box), FadeOut(damping_label), run_time=0.25)

        # ------------------------------------------------------------------
        # 7–12 seconds: Differentiate under the integral sign.
        # ------------------------------------------------------------------
        derivative_eq = MathTex(
            r"I'(a)=-\int_0^\infty e^{-ax}\sin x\,dx=-{1\over 1+a^2}",
            font_size=46,
            color=derivative_color,
        ).next_to(title, DOWN, buff=0.55)
        quick_note = Tex("Differentiate under the integral sign.", font_size=28, color=GRAY_A)
        quick_note.next_to(derivative_eq, DOWN, buff=0.25)

        self.play(FadeOut(axes), FadeOut(axes_labels), FadeOut(curve), FadeOut(a_value), run_time=0.55)
        self.play(TransformMatchingTex(parameter_eq, derivative_eq), FadeIn(quick_note), run_time=1.0)
        self.play(Indicate(derivative_eq[-6:], color=final_color, scale_factor=1.05), run_time=0.8)
        self.play(FadeOut(quick_note), run_time=0.35)

        # ------------------------------------------------------------------
        # 12–16 seconds: Integrate back and apply I(∞)=0.
        # ------------------------------------------------------------------
        integral_back = MathTex(
            r"I(a)={\pi\over2}-\tan^{-1}(a)",
            font_size=58,
            color=parameter_color,
        ).next_to(title, DOWN, buff=0.75)
        boundary = Tex(r"$I(\infty)=0$", font_size=32, color=GRAY_A)
        boundary.next_to(integral_back, DOWN, buff=0.32)

        self.play(TransformMatchingTex(derivative_eq, integral_back), run_time=0.95)
        self.play(FadeIn(boundary, shift=UP * 0.1), run_time=0.45)
        self.play(Indicate(boundary, color=damping_color), run_time=0.65)

        # ------------------------------------------------------------------
        # 16–20 seconds: Let a → 0+ and reveal the final result.
        # ------------------------------------------------------------------
        limit_note = Tex(r"Let $a\to0^+$.", font_size=34, color=parameter_color)
        limit_note.next_to(integral_back, DOWN, buff=0.32)
        final_eq = MathTex(
            r"\int_0^\infty {\sin x\over x}\,dx={\pi\over2}",
            font_size=70,
            color=final_color,
        ).move_to(ORIGIN)
        final_box = SurroundingRectangle(final_eq, color=final_color, buff=0.24, corner_radius=0.12)

        self.play(Transform(boundary, limit_note), run_time=0.45)
        self.play(TransformMatchingTex(integral_back, final_eq), FadeOut(boundary), run_time=0.95)
        self.play(Create(final_box), run_time=0.45)
        self.play(final_eq.animate.scale(1.04), final_box.animate.scale(1.04), run_time=0.45)


if __name__ == "__main__":
    print("Render with: manim -qh feynman_integral.py FeynmanSineIntegral")
