"""Vertical Instagram Reel: Planck integral via Gamma-zeta identity.

Quick test:
    manim -ql planck_integral_reel.py PlanckIntegralReel

High-quality Reel render:
    manim -qh --fps 30 planck_integral_reel.py PlanckIntegralReel

Optional Instagram-compatible H.264 conversion:
    ffmpeg \
    -i media/videos/planck_integral_reel/1080p30/PlanckIntegralReel.mp4 \
    -c:v libx264 \
    -profile:v high \
    -level 4.1 \
    -pix_fmt yuv420p \
    -movflags +faststart \
    -an \
    planck_integral_instagram.mp4
"""

from manim import *
import numpy as np

config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16
config.frame_rate = 30

SAFE_LEFT = -3.4
SAFE_RIGHT = 2.8
SAFE_TOP = 5.6
SAFE_BOTTOM = -5.6
CENTER_Y = 0.15
UPPER_Y = 2.65
LOWER_Y = -2.65
BOTTOM_Y = -4.7


def fit_to_safe_width(mobject, max_width=6.0):
    if mobject.width > max_width:
        mobject.scale_to_fit_width(max_width)
    return mobject


def fit_to_safe_height(mobject, max_height=5.0):
    if mobject.height > max_height:
        mobject.scale_to_fit_height(max_height)
    return mobject


def keep_inside_safe_area(mobject):
    left = mobject.get_left()[0]
    right = mobject.get_right()[0]
    top = mobject.get_top()[1]
    bottom = mobject.get_bottom()[1]

    if left < SAFE_LEFT:
        mobject.shift((SAFE_LEFT - left) * RIGHT)
    if right > SAFE_RIGHT:
        mobject.shift((SAFE_RIGHT - right) * LEFT)
    if top > SAFE_TOP:
        mobject.shift((top - SAFE_TOP) * DOWN)
    if bottom < SAFE_BOTTOM:
        mobject.shift((SAFE_BOTTOM - bottom) * UP)
    return mobject


def stack_vertical(*mobjects, buff=0.45):
    return VGroup(*mobjects).arrange(DOWN, buff=buff)


def objects_overlap(a, b, padding=0.12):
    a_left = a.get_left()[0] - padding
    a_right = a.get_right()[0] + padding
    a_bottom = a.get_bottom()[1] - padding
    a_top = a.get_top()[1] + padding

    b_left = b.get_left()[0] - padding
    b_right = b.get_right()[0] + padding
    b_bottom = b.get_bottom()[1] - padding
    b_top = b.get_top()[1] + padding

    horizontal = a_left < b_right and a_right > b_left
    vertical = a_bottom < b_top and a_top > b_bottom
    return horizontal and vertical


class PlanckIntegralReel(Scene):
    """A no-caption, notation-only Instagram Reel derivation of the Planck integral."""

    def construct(self):
        self.camera.background_color = "#070914"

        main = WHITE
        exp_color = TEAL_C
        sigma_color = YELLOW_C
        gamma_color = PURPLE_B
        final_color = GOLD
        muted = GRAY_B
        graph_color = BLUE_C

        def prep(mobject, max_width=6.0, max_height=5.2, z=5):
            mobject.set_z_index(z)
            fit_to_safe_height(fit_to_safe_width(mobject, max_width), max_height)
            keep_inside_safe_area(mobject)
            return mobject

        def planck_integrand(x):
            if x <= 0:
                return 0
            return x**3 / (np.exp(x) - 1)

        # ------------------------------------------------------------------
        # 0–2 seconds: opening hook and general integral.
        # Running total ≈ 2.0s
        # ------------------------------------------------------------------
        opening = MathTex(
            r"\int_0^\infty \frac{x^3}{e^x-1}\,dx",
            font_size=68,
            color=main,
            substrings_to_isolate=[r"x^3", r"e^x-1"],
        )
        opening.set_color_by_tex(r"x^3", final_color)
        opening.set_color_by_tex(r"e^x-1", exp_color)
        prep(opening, 5.9).move_to([0, UPPER_Y, 0])

        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 1.6, 0.5],
            x_length=5.2,
            y_length=2.4,
            tips=False,
            axis_config={"color": muted, "stroke_width": 2},
        )
        curve = axes.plot(planck_integrand, x_range=[0.05, 10, 0.05], color=graph_color, stroke_width=4)
        area = axes.get_area(curve, x_range=[0.05, 10], color=graph_color, opacity=0.18)
        area.set_z_index(1)
        axes.set_z_index(2)
        curve.set_z_index(3)
        graph_group = VGroup(axes, area, curve).move_to([0, LOWER_Y, 0])
        keep_inside_safe_area(graph_group)
        assert not objects_overlap(opening, graph_group)

        general_line_1 = MathTex(r"I(s)=\int_0^\infty", font_size=54, color=main)
        general_line_2 = MathTex(
            r"\frac{x^{s-1}}{e^x-1}\,dx",
            font_size=58,
            color=main,
            substrings_to_isolate=[r"x^{s-1}", r"e^x-1"],
        )
        general_line_2.set_color_by_tex(r"x^{s-1}", final_color)
        general_line_2.set_color_by_tex(r"e^x-1", exp_color)
        condition = MathTex(r"\operatorname{Re}(s)>1", font_size=34, color=muted)
        general_group = prep(stack_vertical(general_line_1, general_line_2, condition, buff=0.28), 5.8).move_to([0, CENTER_Y, 0])

        self.play(FadeIn(opening, scale=1.04), Create(axes), FadeIn(area), Create(curve), run_time=0.65)
        self.play(Circumscribe(opening, color=exp_color), run_time=0.45)
        self.play(FadeOut(graph_group), FadeTransform(opening, general_group), run_time=0.70)
        self.play(Indicate(general_line_2, color=final_color, scale_factor=1.02), run_time=0.25)

        # ------------------------------------------------------------------
        # 2–6 seconds: denominator explosion.
        # Running total ≈ 5.8s
        # ------------------------------------------------------------------
        denominator = MathTex(r"\frac{1}{e^x-1}", font_size=70, color=exp_color)
        denom_geom = MathTex(r"\frac{e^{-x}}{1-e^{-x}}", font_size=70, color=exp_color)
        prep(denominator, 5.4).move_to([0, CENTER_Y, 0])
        prep(denom_geom, 5.4).move_to([0, CENTER_Y, 0])

        term_1 = MathTex(r"e^{-x}", font_size=48, color=exp_color)
        term_2 = MathTex(r"e^{-2x}", font_size=48, color=exp_color)
        term_3 = MathTex(r"e^{-3x}", font_size=48, color=exp_color)
        term_4 = MathTex(r"e^{-4x}", font_size=48, color=exp_color)
        term_dots = MathTex(r"\cdots", font_size=52, color=exp_color)
        cascade = VGroup(term_1, term_2, term_3, term_4, term_dots).arrange(DOWN, buff=0.22)
        cascade.move_to([0, CENTER_Y, 0])
        prep(cascade, 4.8, 4.8)
        sigma_exp = MathTex(
            r"\sum_{n=1}^{\infty}e^{-nx}",
            font_size=68,
            color=main,
            substrings_to_isolate=[r"\sum_{n=1}^{\infty}", r"e^{-nx}"],
        )
        sigma_exp.set_color_by_tex(r"\sum_{n=1}^{\infty}", sigma_color)
        sigma_exp.set_color_by_tex(r"e^{-nx}", exp_color)
        prep(sigma_exp, 5.5).move_to([0, CENTER_Y, 0])

        self.play(FadeOut(general_group), FadeIn(denominator, scale=1.06), run_time=0.45)
        self.play(FadeTransform(denominator, denom_geom), run_time=0.55)
        self.play(LaggedStart(*[FadeIn(term, shift=0.25 * UP) for term in cascade], lag_ratio=0.12), FadeOut(denom_geom), run_time=0.95)
        self.play(AnimationGroup(*[term.animate.move_to(sigma_exp.get_center()).set_opacity(0.15) for term in cascade], lag_ratio=0.08), FadeIn(sigma_exp, scale=1.04), run_time=0.65)
        self.play(FadeOut(cascade), Circumscribe(sigma_exp, color=sigma_color), run_time=0.45)
        self.wait(0.10)

        # ------------------------------------------------------------------
        # 6–9 seconds: one integral becomes infinitely many integrals.
        # Running total ≈ 8.8s
        # ------------------------------------------------------------------
        inserted_1 = MathTex(r"I(s)=\int_0^\infty x^{s-1}", font_size=46, color=main)
        inserted_2 = MathTex(
            r"\sum_{n=1}^{\infty}e^{-nx}\,dx",
            font_size=52,
            color=main,
            substrings_to_isolate=[r"\sum_{n=1}^{\infty}", r"e^{-nx}"],
        )
        inserted_2.set_color_by_tex(r"\sum_{n=1}^{\infty}", sigma_color)
        inserted_2.set_color_by_tex(r"e^{-nx}", exp_color)
        inserted_group = prep(stack_vertical(inserted_1, inserted_2, buff=0.22), 5.8).move_to([0, CENTER_Y, 0])

        many_1 = MathTex(r"I(s)=\sum_{n=1}^{\infty}", font_size=52, color=main, substrings_to_isolate=[r"\sum_{n=1}^{\infty}"])
        many_1.set_color_by_tex(r"\sum_{n=1}^{\infty}", sigma_color)
        many_2 = MathTex(r"\int_0^\infty x^{s-1}e^{-nx}\,dx", font_size=50, color=main)
        many_group = prep(stack_vertical(many_1, many_2, buff=0.30), 5.8).move_to([0, CENTER_Y, 0])

        ghost_integrals = VGroup(
            MathTex(r"n=1", font_size=34, color=sigma_color),
            MathTex(r"n=2", font_size=34, color=sigma_color),
            MathTex(r"n=3", font_size=34, color=sigma_color),
        ).arrange(DOWN, buff=0.18).next_to(many_group, DOWN, buff=0.35)
        keep_inside_safe_area(VGroup(many_group, ghost_integrals))

        self.play(FadeTransform(sigma_exp, inserted_group), run_time=0.55)
        self.play(FadeTransform(inserted_group, many_group), run_time=0.65)
        self.play(LaggedStart(*[FadeIn(g, shift=0.15 * DOWN) for g in ghost_integrals], lag_ratio=0.12), run_time=0.40)
        self.play(FadeOut(ghost_integrals), Indicate(many_1, color=sigma_color, scale_factor=1.02), run_time=0.40)

        # ------------------------------------------------------------------
        # 9–12 seconds: scaling substitution.
        # Running total ≈ 11.7s
        # ------------------------------------------------------------------
        u_eq = MathTex(r"u=nx", font_size=72, color=main, substrings_to_isolate=["u", "n"])
        u_eq.set_color_by_tex("u", gamma_color)
        u_eq.set_color_by_tex("n", sigma_color)
        prep(u_eq, 5.0).move_to([0, CENTER_Y, 0])
        x_dx = MathTex(r"x=\frac{u}{n},\qquad dx=\frac{du}{n}", font_size=52, color=main)
        prep(x_dx, 5.8).move_to([0, CENTER_Y, 0])
        scale_left = MathTex(r"\int_0^\infty x^{s-1}e^{-nx}\,dx", font_size=48, color=main)
        scale_right_1 = MathTex(r"\frac{1}{n^s}", font_size=58, color=sigma_color)
        scale_right_2 = MathTex(r"\int_0^\infty u^{s-1}e^{-u}\,du", font_size=50, color=gamma_color)
        scaled_integral = prep(stack_vertical(scale_right_1, scale_right_2, buff=0.18), 5.6).move_to([0, CENTER_Y, 0])
        factor_copies = VGroup(*[MathTex(r"\frac{1}{n^s}", font_size=34, color=sigma_color) for _ in range(4)])
        factor_copies.arrange(RIGHT, buff=0.20).move_to([0, LOWER_Y + 0.7, 0])
        factor_sigma = MathTex(r"\sum_{n=1}^{\infty}\frac{1}{n^s}", font_size=48, color=sigma_color).move_to(factor_copies.get_center())
        prep(factor_sigma, 5.6)

        self.play(FadeOut(many_group), GrowFromCenter(u_eq), run_time=0.45)
        self.play(FadeTransform(u_eq, x_dx), run_time=0.45)
        self.play(FadeTransform(x_dx, scale_left), run_time=0.45)
        self.play(FadeTransform(scale_left, scaled_integral), run_time=0.65)
        self.play(LaggedStart(*[FadeIn(f, shift=0.15 * UP) for f in factor_copies], lag_ratio=0.10), run_time=0.35)
        self.play(FadeTransform(factor_copies, factor_sigma), run_time=0.45)
        self.play(FadeOut(factor_sigma), run_time=0.20)

        # ------------------------------------------------------------------
        # 12–15 seconds: Gamma-zeta reveal.
        # Running total ≈ 14.9s
        # ------------------------------------------------------------------
        product_1 = MathTex(r"I(s)=\sum_{n=1}^{\infty}\frac{1}{n^s}", font_size=48, color=main)
        product_2 = MathTex(r"\int_0^\infty u^{s-1}e^{-u}\,du", font_size=48, color=main)
        product_group = prep(stack_vertical(product_1, product_2, buff=0.30), 5.8).move_to([0, CENTER_Y, 0])

        gamma_part = MathTex(r"\int_0^\infty u^{s-1}e^{-u}\,du", font_size=48, color=gamma_color).move_to([0, UPPER_Y - 0.35, 0])
        zeta_part = MathTex(r"\sum_{n=1}^{\infty}\frac{1}{n^s}", font_size=52, color=sigma_color).move_to([0, LOWER_Y + 0.45, 0])
        parts_group = VGroup(gamma_part, zeta_part)
        prep(parts_group, 5.8, 5.0)
        gamma_symbol = MathTex(r"\Gamma(s)", font_size=70, color=gamma_color).move_to(gamma_part)
        zeta_symbol = MathTex(r"\zeta(s)", font_size=70, color=sigma_color).move_to(zeta_part)
        identity = MathTex(
            r"I(s)=\Gamma(s)\zeta(s)",
            font_size=64,
            color=main,
            substrings_to_isolate=[r"\Gamma(s)", r"\zeta(s)"],
        )
        identity.set_color_by_tex(r"\Gamma(s)", gamma_color)
        identity.set_color_by_tex(r"\zeta(s)", sigma_color)
        prep(identity, 5.8).move_to([0, CENTER_Y, 0])
        identity_box = SurroundingRectangle(identity, color=final_color, buff=0.22, corner_radius=0.12)

        self.play(FadeTransform(scaled_integral, product_group), run_time=0.55)
        self.play(FadeTransform(product_group, parts_group), run_time=0.55)
        self.play(FadeTransform(gamma_part, gamma_symbol), FadeTransform(zeta_part, zeta_symbol), run_time=0.55)
        self.play(FadeTransform(VGroup(gamma_symbol, zeta_symbol), identity), run_time=0.55)
        self.play(Create(identity_box), Flash(identity, color=final_color), run_time=0.55)
        self.play(FadeOut(identity_box), run_time=0.20)

        # ------------------------------------------------------------------
        # 15–19 seconds: s=4 and rapid simplification.
        # Running total ≈ 18.8s
        # ------------------------------------------------------------------
        s4 = MathTex(r"s=4", font_size=72, color=final_color).move_to([0, CENTER_Y, 0])
        special_1 = MathTex(r"\int_0^\infty", font_size=52, color=main)
        special_2 = MathTex(r"\frac{x^3}{e^x-1}\,dx", font_size=58, color=main)
        special_3 = MathTex(r"=\Gamma(4)\zeta(4)", font_size=58, color=main, substrings_to_isolate=[r"\Gamma(4)", r"\zeta(4)"])
        special_3.set_color_by_tex(r"\Gamma(4)", gamma_color)
        special_3.set_color_by_tex(r"\zeta(4)", sigma_color)
        special_group = prep(stack_vertical(special_1, special_2, special_3, buff=0.20), 5.8).move_to([0, CENTER_Y, 0])
        step_a = MathTex(r"\Gamma(4)\zeta(4)", font_size=64, color=main).move_to([0, CENTER_Y, 0])
        step_b = MathTex(r"3!\cdot\frac{\pi^4}{90}", font_size=66, color=main, substrings_to_isolate=[r"3!", r"\pi^4"])
        step_b.set_color_by_tex(r"3!", gamma_color)
        step_b.set_color_by_tex(r"\pi^4", final_color)
        prep(step_b, 5.4).move_to([0, CENTER_Y, 0])
        step_c = MathTex(r"6\cdot\frac{\pi^4}{90}", font_size=66, color=main, substrings_to_isolate=["6", r"\pi^4", "90"])
        step_c.set_color_by_tex("6", gamma_color)
        step_c.set_color_by_tex(r"\pi^4", final_color)
        prep(step_c, 5.4).move_to([0, CENTER_Y, 0])
        step_d = MathTex(r"\frac{\pi^4}{15}", font_size=78, color=final_color).move_to([0, CENTER_Y, 0])

        self.play(FadeTransform(identity, s4), run_time=0.40)
        self.play(FadeTransform(s4, special_group), run_time=0.65)
        self.play(FadeTransform(special_group, step_a), run_time=0.35)
        self.play(FadeTransform(step_a, step_b), run_time=0.45)
        self.play(FadeTransform(step_b, step_c), run_time=0.45)
        self.play(FadeTransform(step_c, step_d), run_time=0.45)
        self.play(Circumscribe(step_d, color=final_color), run_time=0.45)

        # ------------------------------------------------------------------
        # 19–22 seconds: final reveal and loop-friendly ending.
        # Running total ≈ 21.3s
        # ------------------------------------------------------------------
        final_top = MathTex(r"\int_0^\infty", font_size=62, color=main)
        final_mid = MathTex(r"\frac{x^3}{e^x-1}\,dx", font_size=64, color=main)
        final_eq = MathTex(r"=", font_size=58, color=main)
        final_bottom = MathTex(r"\frac{\pi^4}{15}", font_size=78, color=final_color)
        final_group = prep(stack_vertical(final_top, final_mid, final_eq, final_bottom, buff=0.18), 5.8, 5.0).move_to([0, CENTER_Y, 0])
        final_box = SurroundingRectangle(final_group, color=final_color, buff=0.24, corner_radius=0.14)
        final_box.set_z_index(7)
        opening_echo = MathTex(r"\int_0^\infty \frac{x^3}{e^x-1}\,dx", font_size=66, color=main)
        prep(opening_echo, 5.9).move_to([0, CENTER_Y, 0])

        self.play(FadeTransform(step_d, final_group), run_time=0.60)
        self.play(Create(final_box), Circumscribe(final_group, color=final_color), run_time=0.65)
        self.play(Flash(final_group, color=final_color), final_group.animate.scale(1.025), final_box.animate.scale(1.025), run_time=0.45)
        self.wait(1.00)
        self.play(FadeOut(final_box), FadeTransform(final_group, opening_echo), run_time=0.65)
        self.wait(0.10)


if __name__ == "__main__":
    print("manim -ql planck_integral_reel.py PlanckIntegralReel")
    print("manim -qh --fps 30 planck_integral_reel.py PlanckIntegralReel")
