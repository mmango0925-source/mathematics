"""Vertical Instagram Reel: the first Sophomore's Dream.

Quick test:
    manim -ql sophomores_dream_reel.py SophomoresDreamReel

Full-quality vertical render:
    manim -qh --fps 30 sophomores_dream_reel.py SophomoresDreamReel
"""

from manim import *

# Instagram Reel / phone-first frame.
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16
config.frame_rate = 30

# Asymmetric mobile safe area: extra room on the right for Reel buttons.
SAFE_LEFT = -3.4
SAFE_RIGHT = 2.8
SAFE_TOP = 5.6
SAFE_BOTTOM = -5.6

TITLE_Y = 4.6
UPPER_Y = 2.8
CENTER_Y = 0.2
LOWER_Y = -2.6
BOTTOM_Y = -4.8

DEBUG_LAYOUT = False


def fit_to_safe_width(mobject, max_width=6.0):
    """Keep equations large, but never wider than the mobile safe width."""
    if mobject.width > max_width:
        mobject.scale_to_fit_width(max_width)
    return mobject


def fit_to_safe_height(mobject, max_height=4.8):
    """Keep tall groups inside the central safe area."""
    if mobject.height > max_height:
        mobject.scale_to_fit_height(max_height)
    return mobject


def stack_vertical(*mobjects, buff=0.65):
    """Consistent vertical layout for Reel-safe equation groups."""
    return VGroup(*mobjects).arrange(DOWN, buff=buff)


def keep_inside_safe_area(mobject):
    """Shift a positioned object back into the asymmetric safe rectangle."""
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


def objects_overlap(a, b, padding=0.15):
    """Axis-aligned bounding-box overlap check for final object positions."""
    a_left = a.get_left()[0] - padding
    a_right = a.get_right()[0] + padding
    a_bottom = a.get_bottom()[1] - padding
    a_top = a.get_top()[1] + padding

    b_left = b.get_left()[0] - padding
    b_right = b.get_right()[0] + padding
    b_bottom = b.get_bottom()[1] - padding
    b_top = b.get_top()[1] + padding

    horizontal_overlap = a_left < b_right and a_right > b_left
    vertical_overlap = a_bottom < b_top and a_top > b_bottom
    return horizontal_overlap and vertical_overlap


class SophomoresDreamReel(Scene):
    """A clear 20–24 second vertical animation for the first Sophomore's Dream."""

    def construct(self):
        self.camera.background_color = "#080A12"

        # Restrained palette: math first, accents only for structure.
        main = WHITE
        muted = GRAY_B
        x_color = BLUE_C
        exp_color = TEAL_C
        sigma_color = YELLOW_C
        sub_color = PURPLE_B
        gamma_color = ORANGE
        final_color = GOLD
        fill_color = BLUE_E

        visible_objects = VGroup()

        def caption(text, color=WHITE, size=34):
            mob = Tex(rf"\textbf{{{text}}}", font_size=size, color=color)
            mob.set_z_index(6)
            return keep_inside_safe_area(fit_to_safe_width(mob, 5.8))

        def prep_equation(mob, max_width=6.0, max_height=4.8, z=5):
            mob.set_z_index(z)
            return keep_inside_safe_area(fit_to_safe_height(fit_to_safe_width(mob, max_width), max_height))

        def set_visible(*mobjects):
            nonlocal visible_objects
            visible_objects = VGroup(*mobjects)

        def clear_visible(run_time=0.3):
            nonlocal visible_objects
            if len(visible_objects) == 0:
                return
            self.play(FadeOut(visible_objects), run_time=run_time)
            visible_objects = VGroup()

        def x_to_minus_x(x):
            # Graph only starts at x=0.01, but this keeps the helper safe.
            if x <= 0:
                return 1
            return x ** (-x)

        if DEBUG_LAYOUT:
            safe_width = SAFE_RIGHT - SAFE_LEFT
            safe_height = SAFE_TOP - SAFE_BOTTOM
            safe_center_x = (SAFE_LEFT + SAFE_RIGHT) / 2
            safe_center_y = (SAFE_TOP + SAFE_BOTTOM) / 2
            safe_rect = Rectangle(width=safe_width, height=safe_height, color=RED_C)
            safe_rect.move_to([safe_center_x, safe_center_y, 0]).set_stroke(opacity=0.45)
            zone_labels = VGroup(
                Tex("TITLE", font_size=18).move_to([SAFE_LEFT + 0.5, TITLE_Y, 0]),
                Tex("UPPER", font_size=18).move_to([SAFE_LEFT + 0.55, UPPER_Y, 0]),
                Tex("CENTER", font_size=18).move_to([SAFE_LEFT + 0.65, CENTER_Y, 0]),
                Tex("LOWER", font_size=18).move_to([SAFE_LEFT + 0.55, LOWER_Y, 0]),
                Tex("BOTTOM", font_size=18).move_to([SAFE_LEFT + 0.65, BOTTOM_Y, 0]),
            ).set_color(RED_C)
            self.add(safe_rect, zone_labels)

        # ------------------------------------------------------------------
        # 0–2 seconds: hook.
        # Running total ≈ 1.9s
        # ------------------------------------------------------------------
        hook_eq = prep_equation(
            MathTex(
                r"I=\int_0^1 x^{-x}\,dx",
                font_size=68,
                color=main,
                substrings_to_isolate=[r"x^{-x}"],
            ),
            5.8,
        )
        hook_eq.set_color_by_tex(r"x^{-x}", x_color)
        hook_eq.move_to([0, UPPER_Y, 0])
        hook_caption = caption("This integral becomes a series.", sigma_color, 32)
        hook_group = stack_vertical(hook_eq, hook_caption, buff=0.45).move_to([0, 2.65, 0])
        keep_inside_safe_area(hook_group)

        axes = Axes(
            x_range=[0, 1.05, 0.25],
            y_range=[0, 1.5, 0.5],
            x_length=5.2,
            y_length=2.55,
            tips=False,
            axis_config={"color": muted, "stroke_width": 2},
        )
        curve = axes.plot(x_to_minus_x, x_range=[0.01, 1, 0.01], color=x_color, stroke_width=4)
        area = axes.get_area(curve, x_range=[0.01, 1], color=fill_color, opacity=0.38)
        axis_labels = axes.get_axis_labels(MathTex("x", font_size=24), MathTex("y", font_size=24))
        area.set_z_index(1)
        axes.set_z_index(2)
        axis_labels.set_z_index(2)
        curve.set_z_index(3)
        graph_group = VGroup(axes, area, curve, axis_labels).move_to([0, LOWER_Y, 0])
        keep_inside_safe_area(graph_group)
        assert not objects_overlap(hook_group, graph_group)

        teaser = prep_equation(
            MathTex(r"?\ \longrightarrow\ 1+\frac{1}{2^2}+\frac{1}{3^3}+\cdots", font_size=42, color=final_color),
            5.9,
        ).move_to([0, BOTTOM_Y, 0])
        keep_inside_safe_area(teaser)
        assert not objects_overlap(teaser, graph_group, padding=0.05)

        self.play(FadeIn(hook_eq, scale=1.04), FadeIn(hook_caption), run_time=0.45)
        self.play(Create(axes), FadeIn(area), Create(curve), FadeIn(axis_labels), run_time=0.55)
        self.play(FadeIn(teaser, shift=UP * 0.12), run_time=0.45)
        self.play(FadeOut(teaser), run_time=0.25)
        set_visible(hook_group, graph_group)

        # ------------------------------------------------------------------
        # 2–5 seconds: exponential form.
        # Running total ≈ 4.9s
        # ------------------------------------------------------------------
        integrand_caption = caption("Expose the exponential.", exp_color, 34)
        integrand = prep_equation(
            MathTex(
                r"x^{-x}\ \longrightarrow\ e^{-x\ln x}",
                font_size=62,
                color=main,
                substrings_to_isolate=[r"x^{-x}", r"-x\ln x"],
            ),
            5.8,
        )
        integrand.set_color_by_tex(r"x^{-x}", x_color)
        integrand.set_color_by_tex(r"-x\ln x", exp_color)
        integrand_group = stack_vertical(integrand_caption, integrand, buff=0.55).move_to([0, CENTER_Y, 0])
        keep_inside_safe_area(integrand_group)
        assert not objects_overlap(integrand_caption, integrand)

        integral_exp = prep_equation(
            MathTex(
                r"I=\int_0^1 e^{-x\ln x}\,dx",
                font_size=56,
                color=main,
                substrings_to_isolate=[r"-x\ln x"],
            ),
            5.8,
        )
        integral_exp.set_color_by_tex(r"-x\ln x", exp_color)
        integral_exp.move_to([0, CENTER_Y, 0])
        focus_exp = SurroundingRectangle(integral_exp, color=exp_color, buff=0.18, corner_radius=0.08).set_z_index(7)

        self.play(FadeOut(graph_group), FadeTransform(hook_group, integrand_group), run_time=0.60)
        self.play(Circumscribe(integrand, color=exp_color), run_time=0.45)
        self.play(FadeTransform(integrand, integral_exp), FadeOut(integrand_caption), run_time=0.60)
        self.play(Create(focus_exp), run_time=0.35)
        self.play(FadeOut(focus_exp), run_time=0.25)
        set_visible(integral_exp)

        # ------------------------------------------------------------------
        # 5–8 seconds: Taylor expansion.
        # Running total ≈ 7.9s
        # ------------------------------------------------------------------
        taylor_caption = caption("One function becomes infinitely many.", sigma_color, 31)
        taylor_1 = prep_equation(MathTex(r"e^z=1+z+\frac{z^2}{2!}+\cdots", font_size=54, color=main), 5.9)
        taylor_2 = prep_equation(
            MathTex(r"e^{-x\ln x}=1+(-x\ln x)+\frac{(-x\ln x)^2}{2!}+\cdots", font_size=46, color=main),
            6.0,
        )
        sigma_line_1 = MathTex(
            r"e^{-x\ln x}",
            font_size=54,
            color=main,
            substrings_to_isolate=[r"-x\ln x"],
        )
        sigma_line_2 = MathTex(
            r"=\sum_{n=0}^{\infty}\frac{x^n(-\ln x)^n}{n!}",
            font_size=50,
            color=main,
            substrings_to_isolate=[r"\sum_{n=0}^{\infty}", r"-\ln x"],
        )
        sigma_line_1.set_color_by_tex(r"-x\ln x", exp_color)
        sigma_line_2.set_color_by_tex(r"\sum_{n=0}^{\infty}", sigma_color)
        sigma_line_2.set_color_by_tex(r"-\ln x", exp_color)
        sigma_group = prep_equation(stack_vertical(sigma_line_1, sigma_line_2, buff=0.32), 5.95)

        taylor_group_1 = stack_vertical(taylor_caption, taylor_1, buff=0.60).move_to([0, CENTER_Y, 0])
        taylor_group_2 = stack_vertical(taylor_caption.copy(), taylor_2, buff=0.60).move_to([0, CENTER_Y, 0])
        sigma_full_group = stack_vertical(taylor_caption.copy(), sigma_group, buff=0.55).move_to([0, CENTER_Y, 0])
        keep_inside_safe_area(taylor_group_1)
        keep_inside_safe_area(taylor_group_2)
        keep_inside_safe_area(sigma_full_group)

        self.play(FadeTransform(integral_exp, taylor_group_1), run_time=0.60)
        self.play(FadeTransform(taylor_group_1, taylor_group_2), run_time=0.60)
        self.play(FadeTransform(taylor_group_2, sigma_full_group), run_time=0.70)
        self.play(Circumscribe(sigma_group, color=sigma_color), run_time=0.55)
        self.play(FadeOut(sigma_full_group[0]), run_time=0.20)
        set_visible(sigma_group)

        # ------------------------------------------------------------------
        # 8–11 seconds: move the sum outside the integral.
        # Running total ≈ 10.8s
        # ------------------------------------------------------------------
        inside_line_1 = MathTex(r"I=\int_0^1", r"\sum_{n=0}^{\infty}", font_size=54, color=main, substrings_to_isolate=[r"\sum_{n=0}^{\infty}"])
        inside_line_2 = MathTex(r"\frac{x^n(-\ln x)^n}{n!}\,dx", font_size=50, color=main)
        inside_group = prep_equation(stack_vertical(inside_line_1, inside_line_2, buff=0.30), 5.9).move_to([0, CENTER_Y + 0.4, 0])
        inside_line_1.set_color_by_tex(r"\sum_{n=0}^{\infty}", sigma_color)

        outside_line_1 = MathTex(r"I=\sum_{n=0}^{\infty}\frac{1}{n!}", font_size=54, color=main, substrings_to_isolate=[r"\sum_{n=0}^{\infty}"])
        outside_line_2 = MathTex(r"\int_0^1x^n(-\ln x)^n\,dx", font_size=50, color=main)
        outside_group = prep_equation(stack_vertical(outside_line_1, outside_line_2, buff=0.35), 5.9).move_to([0, CENTER_Y + 0.35, 0])
        outside_line_1.set_color_by_tex(r"\sum_{n=0}^{\infty}", sigma_color)

        note = caption("Termwise integration is valid here.", muted, 23).move_to([0, -2.2, 0])
        keep_inside_safe_area(note)
        assert not objects_overlap(outside_group, note)

        self.play(FadeTransform(sigma_group, inside_group), run_time=0.55)
        self.play(FadeTransform(inside_group, outside_group), FadeIn(note), run_time=0.70)
        self.play(Indicate(outside_group[0], color=sigma_color, scale_factor=1.02), run_time=0.45)
        self.play(FadeOut(note), run_time=0.20)
        set_visible(outside_group)

        # ------------------------------------------------------------------
        # 11–14 seconds: logarithmic substitution.
        # Running total ≈ 13.9s
        # ------------------------------------------------------------------
        sub_caption = caption("The logarithm disappears.", sub_color, 34)
        sub_eq = prep_equation(MathTex(r"x=e^{-t}", font_size=66, color=sub_color), 5.6)
        sub_group = stack_vertical(sub_caption, sub_eq, buff=0.55).move_to([0, CENTER_Y, 0])
        keep_inside_safe_area(sub_group)

        interval_line_raw = MathTex(
            r"x:0\to1\quad\Rightarrow\quad",
            r"t",
            r":\infty\to0",
            font_size=48,
            color=main,
        )
        interval_line_raw[0].set_color(x_color)
        interval_line_raw[1].set_color(sub_color)
        interval_line = prep_equation(interval_line_raw, 5.9)
        log_line_raw = MathTex(
            r"-\ln x\longrightarrow",
            r"t",
            font_size=50,
            color=exp_color,
        )
        log_line_raw[1].set_color(sub_color)
        log_line = prep_equation(log_line_raw, 5.5)
        interval_group = stack_vertical(interval_line, log_line, buff=0.8).move_to([0, CENTER_Y, 0])
        keep_inside_safe_area(interval_group)
        assert not objects_overlap(interval_line, log_line)

        old_int = prep_equation(MathTex(r"\int_0^1x^n(-\ln x)^n\,dx", font_size=48, color=main), 5.8)
        new_int_raw = MathTex(
            r"\int_0^\infty",
            r"t^n",
            r"e^{-(n+1)t}",
            r"\,dt",
            font_size=50,
            color=main,
        )
        new_int_raw[1].set_color(sub_color)
        new_int_raw[2].set_color(sub_color)
        new_int = prep_equation(new_int_raw, 5.8)
        transformed_group = stack_vertical(old_int, new_int, buff=0.75).move_to([0, CENTER_Y, 0])
        keep_inside_safe_area(transformed_group)
        assert not objects_overlap(old_int, new_int)

        self.play(FadeOut(outside_group), FadeIn(sub_group), run_time=0.55)
        self.play(Circumscribe(sub_eq, color=sub_color), run_time=0.45)
        self.play(FadeOut(sub_group), FadeIn(interval_group), run_time=0.55)
        self.play(Flash(log_line, color=exp_color), run_time=0.45)
        self.play(FadeOut(interval_group), FadeIn(transformed_group), run_time=0.70)
        self.play(Circumscribe(new_int, color=sub_color), run_time=0.45)
        set_visible(transformed_group)

        # ------------------------------------------------------------------
        # 14–17 seconds: Gamma integral transformation.
        # Running total ≈ 16.9s
        # ------------------------------------------------------------------
        u_eq = prep_equation(MathTex(r"u=(n+1)t", font_size=60, color=sub_color), 5.4).move_to([0, CENTER_Y, 0])
        scaled_line_1 = MathTex(r"\frac{1}{(n+1)^{n+1}}", font_size=52, color=main)
        scaled_line_2 = MathTex(
            r"\int_0^\infty",
            r"u^n",
            r"e^{-u}",
            r"\,du",
            font_size=52,
            color=main,
        )
        scaled_line_2[1].set_color(sub_color)
        scaled_line_2[2].set_color(sub_color)
        scaled_group = prep_equation(stack_vertical(scaled_line_1, scaled_line_2, buff=0.22), 5.6)
        scaled_group.move_to([0, CENTER_Y, 0])

        gamma_label = caption("Gamma integral", gamma_color, 34)
        gamma_eq = prep_equation(
            MathTex(
                r"\int_0^\infty u^ne^{-u}\,du=n!",
                font_size=52,
                color=main,
                substrings_to_isolate=["n!"],
            ),
            5.8,
        )
        gamma_eq.set_color_by_tex("n!", gamma_color)
        gamma_group = stack_vertical(gamma_label, gamma_eq, buff=0.45).move_to([0, CENTER_Y, 0])
        keep_inside_safe_area(gamma_group)
        assert not objects_overlap(gamma_label, gamma_eq)

        result_line_1 = MathTex(r"\int_0^1x^n(-\ln x)^n\,dx", font_size=43, color=main)
        result_line_2 = MathTex(r"=\frac{n!}{(n+1)^{n+1}}", font_size=56, color=gamma_color)
        result_group = prep_equation(stack_vertical(result_line_1, result_line_2, buff=0.35), 5.8).move_to([0, CENTER_Y, 0])

        self.play(FadeOut(transformed_group), FadeIn(u_eq), run_time=0.45)
        self.play(FadeTransform(u_eq, scaled_group), run_time=0.65)
        self.play(FadeOut(scaled_group), FadeIn(gamma_group), run_time=0.55)
        self.play(Flash(gamma_eq, color=gamma_color), Indicate(gamma_eq, color=gamma_color, scale_factor=1.03), run_time=0.60)
        self.play(FadeTransform(gamma_group, result_group), run_time=0.55)
        set_visible(result_group)

        # ------------------------------------------------------------------
        # 17–20 seconds: perfect cancellation.
        # Running total ≈ 19.9s
        # ------------------------------------------------------------------
        cancel_eq_line_1 = MathTex(r"I=\sum_{n=0}^{\infty}", font_size=54, color=main)
        cancel_eq_line_2 = MathTex(
            r"\frac{1}{n!}\,\frac{n!}{(n+1)^{n+1}}",
            font_size=54,
            color=main,
            substrings_to_isolate=["n!"],
        )
        cancel_eq_line_2.set_color_by_tex("n!", gamma_color)
        cancel_eq = prep_equation(stack_vertical(cancel_eq_line_1, cancel_eq_line_2, buff=0.24), 5.8)
        cancel_caption = caption("Everything cancels perfectly.", final_color, 31)
        cancel_group = stack_vertical(cancel_eq, cancel_caption, buff=0.60).move_to([0, CENTER_Y, 0])
        keep_inside_safe_area(cancel_group)
        assert not objects_overlap(cancel_eq, cancel_caption)

        cancel_marks = VGroup(
            Line([-0.72, -0.04, 0], [-0.30, -0.43, 0], color=gamma_color, stroke_width=7),
            Line([0.08, -0.04, 0], [0.50, -0.43, 0], color=gamma_color, stroke_width=7),
        ).set_z_index(7)

        simplified_line_1 = MathTex(
            r"I=\sum_{n=0}^{\infty}",
            font_size=56,
            color=main,
            substrings_to_isolate=[r"\sum_{n=0}^{\infty}"],
        )
        simplified_line_1.set_color_by_tex(r"\sum_{n=0}^{\infty}", sigma_color)
        simplified_line_2 = MathTex(r"\frac{1}{(n+1)^{n+1}}", font_size=58, color=main)
        simplified_group = prep_equation(stack_vertical(simplified_line_1, simplified_line_2, buff=0.28), 5.6)
        simplified_group.move_to([0, CENTER_Y, 0])

        self.play(FadeTransform(result_group, cancel_group), run_time=0.60)
        self.play(Create(cancel_marks), run_time=0.35)
        self.play(Flash(cancel_eq, color=gamma_color), run_time=0.40)
        self.play(FadeOut(cancel_marks), FadeOut(cancel_caption), FadeTransform(cancel_eq, simplified_group), run_time=0.65)
        self.play(Circumscribe(simplified_group, color=final_color), run_time=0.45)
        set_visible(simplified_group)

        # ------------------------------------------------------------------
        # 20–23 seconds: re-index and final identity.
        # Running total ≈ 23.2s including final hold and clean loop ending.
        # ------------------------------------------------------------------
        k_eq = prep_equation(MathTex(r"k=n+1", font_size=54, color=sub_color), 5.3).move_to([0, UPPER_Y, 0])
        reindexed = prep_equation(MathTex(r"\sum_{k=1}^{\infty}\frac{1}{k^k}", font_size=64, color=final_color), 5.3).move_to([0, CENTER_Y, 0])
        reindex_group = stack_vertical(k_eq, reindexed, buff=0.65).move_to([0, CENTER_Y + 0.2, 0])
        keep_inside_safe_area(reindex_group)
        assert not objects_overlap(k_eq, reindexed)

        expanded = prep_equation(MathTex(r"1+\frac{1}{2^2}+\frac{1}{3^3}+\cdots", font_size=50, color=final_color), 5.8).move_to([0, CENTER_Y, 0])

        final_integral = MathTex(r"\int_0^1x^{-x}\,dx", font_size=66, color=main)
        final_equals = MathTex(r"=", font_size=58, color=main)
        final_series = MathTex(r"\sum_{k=1}^{\infty}\frac{1}{k^k}", font_size=66, color=final_color)
        final_group = prep_equation(stack_vertical(final_integral, final_equals, final_series, buff=0.30), 5.8, 4.8).move_to([0, CENTER_Y, 0])
        final_box = SurroundingRectangle(final_group, color=final_color, buff=0.30, corner_radius=0.14).set_z_index(7)
        numeric_value = Tex(r"$\approx 1.291285997\ldots$", font_size=30, color=muted).set_z_index(6)
        numeric_value.next_to(final_box, DOWN, buff=0.25)
        keep_inside_safe_area(VGroup(final_box, numeric_value))
        assert not objects_overlap(final_group, numeric_value, padding=0.05)

        faint_graph = graph_group.copy().set_opacity(0.10).move_to([0, BOTTOM_Y + 0.3, 0]).set_z_index(0)
        opening_echo = prep_equation(MathTex(r"\int_0^1x^{-x}\,dx", font_size=72, color=main), 5.8).move_to([0, CENTER_Y, 0])

        self.play(FadeTransform(simplified_group, reindex_group), run_time=0.65)
        self.play(FadeOut(k_eq), FadeTransform(reindexed, expanded), run_time=0.55)
        self.play(FadeOut(expanded), FadeIn(faint_graph), FadeIn(final_group), run_time=0.65)
        self.play(Create(final_box), FadeIn(numeric_value), Circumscribe(final_group, color=final_color), run_time=0.80)
        # Optional sound: reveal impact
        self.play(Flash(final_group, color=final_color), run_time=0.45)
        self.wait(1.10)

        # Clean loop ending: remove final identity first, then restore the opener.
        self.play(FadeOut(VGroup(final_group, final_box, numeric_value, faint_graph)), run_time=0.45)
        self.play(FadeIn(opening_echo, scale=1.03), run_time=0.45)
        # Optional sound: soft loop transition
        self.wait(0.10)


if __name__ == "__main__":
    print("Quick test: manim -ql sophomores_dream_reel.py SophomoresDreamReel")
    print("Full-quality vertical render: manim -qh --fps 30 sophomores_dream_reel.py SophomoresDreamReel")
