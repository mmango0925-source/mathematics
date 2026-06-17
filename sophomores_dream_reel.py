"""Vertical Instagram Reel: the first Sophomore's Dream.

Quick test:
    manim -ql sophomores_dream_reel.py SophomoresDreamReel

Full-quality vertical render:
    manim -qh --fps 30 sophomores_dream_reel.py SophomoresDreamReel

Optional Instagram-friendly H.264 conversion:
    ffmpeg \
    -i media/videos/sophomores_dream_reel/1080p30/SophomoresDreamReel.mp4 \
    -c:v libx264 \
    -profile:v high \
    -level 4.1 \
    -pix_fmt yuv420p \
    -movflags +faststart \
    -an \
    sophomores_dream_instagram.mp4
"""

from manim import *

# Instagram Reel / phone-first frame.
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16
config.frame_rate = 30


class SophomoresDreamReel(Scene):
    """A 20–24 second vertical animation for ∫₀¹ x^{-x} dx = Σ 1/nⁿ."""

    def construct(self):
        self.camera.background_color = "#080A12"

        # Limited, consistent palette for a clean mobile look.
        main_color = WHITE
        subtle = GRAY_B
        x_color = BLUE_C
        exp_color = TEAL_C
        sigma_color = YELLOW_C
        sub_color = PURPLE_B
        gamma_color = ORANGE
        final_color = GOLD
        area_color = BLUE_E

        def caption(text, color=WHITE, size=34):
            """Bold, short captions that remain readable on a phone."""
            return Tex(rf"\textbf{{{text}}}", font_size=size, color=color)

        def x_to_minus_x(x):
            """Safe graphing helper: avoid evaluating the endpoint x=0."""
            if x <= 0:
                return 1
            return x ** (-x)

        # ------------------------------------------------------------------
        # 0–2 seconds: hook.
        # Running total ≈ 2.0s
        # ------------------------------------------------------------------
        hook = MathTex(r"\int_0^1 x^{-x}\,dx", font_size=74, color=main_color)
        hook.move_to([0, 3.05, 0])
        hook.set_color_by_tex(r"x^{-x}", x_color)
        hook_caption = caption("This integral becomes a series.", sigma_color, 34)
        hook_caption.next_to(hook, DOWN, buff=0.28)

        axes = Axes(
            x_range=[0, 1.05, 0.25],
            y_range=[0, 1.5, 0.5],
            x_length=5.4,
            y_length=2.75,
            tips=False,
            axis_config={"color": subtle, "stroke_width": 2},
        ).move_to([0, -2.35, 0])
        graph = axes.plot(x_to_minus_x, x_range=[0.01, 1, 0.01], color=x_color, stroke_width=4)
        area = axes.get_area(graph, x_range=[0.01, 1], color=area_color, opacity=0.45)
        teaser = MathTex(
            r"?\quad\longrightarrow\quad 1+{1\over2^2}+{1\over3^3}+\cdots",
            font_size=42,
            color=final_color,
        ).move_to([0, -4.55, 0])

        self.play(FadeIn(hook, scale=1.08), Create(axes), run_time=0.45)
        self.play(Create(graph), FadeIn(area), FadeIn(hook_caption, shift=UP * 0.1), run_time=0.55)
        self.play(FadeIn(teaser, shift=UP * 0.15), run_time=0.55)
        self.play(FadeOut(teaser), FadeOut(hook_caption), run_time=0.30)
        # ------------------------------------------------------------------
        # 2–5 seconds: exponential form.
        # Running total ≈ 5.0s
        # ------------------------------------------------------------------
        base = MathTex(r"x^{-x}", font_size=66, color=x_color).move_to([0, 2.35, 0])
        exp_form = MathTex(r"e^{-x\ln x}", font_size=66, color=exp_color).move_to(base)
        integral_exp = MathTex(r"I=\int_0^1 e^{-x\ln x}\,dx", font_size=56, color=main_color)
        integral_exp.move_to([0, 0.65, 0])
        integral_exp.set_color_by_tex(r"-x\ln x", exp_color)
        exp_caption = caption("Expose the exponential.", exp_color, 34).move_to([0, -1.05, 0])
        exp_focus = SurroundingRectangle(exp_form, color=exp_color, buff=0.16, corner_radius=0.08)

        self.play(FadeOut(axes), FadeOut(area), FadeOut(graph), ReplacementTransform(hook, base), run_time=0.55)
        self.play(TransformMatchingTex(base, exp_form), FadeIn(exp_caption), run_time=0.65)
        self.play(Create(exp_focus), run_time=0.35)
        self.play(ReplacementTransform(exp_form.copy(), integral_exp), FadeOut(exp_focus), run_time=0.60)
        self.play(Circumscribe(integral_exp, color=exp_color), run_time=0.40)
        self.play(FadeOut(exp_caption), run_time=0.20)

        # ------------------------------------------------------------------
        # 5–8 seconds: Taylor expansion.
        # Running total ≈ 8.0s
        # ------------------------------------------------------------------
        series_caption = caption("One function becomes infinitely many.", sigma_color, 32).move_to([0, 3.45, 0])
        ez = MathTex(r"e^z=1+z+{z^2\over2!}+{z^3\over3!}+\cdots", font_size=50, color=main_color)
        ez.move_to([0, 1.6, 0])
        terms = VGroup(
            MathTex("1", font_size=44, color=main_color),
            MathTex(r"x(-\ln x)", font_size=44, color=exp_color),
            MathTex(r"{x^2(-\ln x)^2\over2!}", font_size=44, color=sigma_color),
            MathTex(r"\cdots", font_size=50, color=main_color),
        ).arrange(DOWN, buff=0.18).move_to([0, -0.7, 0])
        sigma_exp = MathTex(
            r"e^{-x\ln x}=\sum_{n=0}^{\infty}{x^n(-\ln x)^n\over n!}",
            font_size=50,
            color=main_color,
        ).move_to([0, 0.35, 0])
        sigma_exp.set_color_by_tex(r"\sum", sigma_color)
        sigma_exp.set_color_by_tex(r"-\ln x", exp_color)

        self.play(FadeOut(integral_exp), FadeIn(series_caption), FadeIn(ez, scale=1.03), run_time=0.60)
        self.play(LaggedStart(*[FadeIn(term, shift=UP * 0.12) for term in terms], lag_ratio=0.14), run_time=0.60)
        self.play(ReplacementTransform(ez, sigma_exp), FadeOut(terms), run_time=0.60)
        self.play(Circumscribe(sigma_exp, color=sigma_color), run_time=0.55)
        self.play(FadeOut(series_caption), run_time=0.20)
        # ------------------------------------------------------------------
        # 8–11 seconds: move the sum outside the integral.
        # Running total ≈ 11.0s
        # ------------------------------------------------------------------
        inside = MathTex(
            r"I=\int_0^1 \sum_{n=0}^{\infty}{x^n(-\ln x)^n\over n!}\,dx",
            font_size=47,
            color=main_color,
        ).move_to([0, 1.15, 0])
        outside = MathTex(
            r"I=\sum_{n=0}^{\infty}{1\over n!}\int_0^1 x^n(-\ln x)^n\,dx",
            font_size=47,
            color=main_color,
        ).move_to([0, 0.65, 0])
        inside.set_color_by_tex(r"\sum", sigma_color)
        outside.set_color_by_tex(r"\sum", sigma_color)
        sigma_symbol = MathTex(r"\sum", font_size=78, color=sigma_color).move_to([-0.15, 1.0, 0])
        footnote = Tex("Termwise integration is valid here.", font_size=23, color=subtle)
        footnote.move_to([0, -2.15, 0])

        self.play(ReplacementTransform(sigma_exp, inside), run_time=0.60)
        self.play(FadeIn(sigma_symbol, scale=1.2), sigma_symbol.animate.move_to([-1.65, 0.66, 0]), run_time=0.55)
        self.play(ReplacementTransform(inside, outside), FadeOut(sigma_symbol), FadeIn(footnote), run_time=0.75)
        self.play(Indicate(outside, color=sigma_color, scale_factor=1.02), run_time=0.45)
        self.play(FadeOut(footnote), run_time=0.20)
        # ------------------------------------------------------------------
        # 11–14 seconds: logarithmic substitution.
        # Running total ≈ 14.0s
        # ------------------------------------------------------------------
        sub_caption = caption("The logarithm disappears.", sub_color, 34).move_to([0, 3.4, 0])
        x_sub = MathTex(r"x=e^{-t}", font_size=66, color=sub_color).move_to([0, 2.35, 0])
        interval_x = MathTex(r"x:0\to1", font_size=42, color=x_color).move_to([-1.45, 0.8, 0])
        interval_t = MathTex(r"t:\infty\to0", font_size=42, color=sub_color).move_to([1.45, 0.8, 0])
        arrow = Arrow(interval_x.get_right(), interval_t.get_left(), buff=0.15, color=subtle)
        log_to_t = MathTex(r"-\ln x\longrightarrow t", font_size=46, color=exp_color).move_to([0, -0.25, 0])
        log_integral = MathTex(
            r"\int_0^1 x^n(-\ln x)^n\,dx",
            font_size=46,
            color=main_color,
        ).move_to([0, -1.55, 0])
        gamma_seed = MathTex(
            r"\int_0^\infty t^n e^{-(n+1)t}\,dt",
            font_size=48,
            color=main_color,
        ).move_to(log_integral)
        gamma_seed.set_color_by_tex("t", sub_color)

        self.play(FadeOut(outside), FadeIn(sub_caption), GrowFromCenter(x_sub), run_time=0.65)
        self.play(FadeIn(interval_x), GrowArrow(arrow), FadeIn(interval_t), run_time=0.55)
        self.play(FadeIn(log_to_t, shift=UP * 0.1), run_time=0.45)
        self.play(FadeIn(log_integral), run_time=0.45)
        self.play(ReplacementTransform(log_integral, gamma_seed), Flash(log_to_t, color=exp_color), run_time=0.60)
        self.play(FadeOut(VGroup(sub_caption, x_sub, interval_x, interval_t, arrow, log_to_t)), run_time=0.35)

        # ------------------------------------------------------------------
        # 14–17 seconds: reveal the Gamma integral.
        # Running total ≈ 17.0s
        # ------------------------------------------------------------------
        u_sub = MathTex(r"u=(n+1)t", font_size=60, color=sub_color).move_to([0, 2.6, 0])
        scaled = MathTex(
            r"{1\over (n+1)^{n+1}}\int_0^\infty u^n e^{-u}\,du",
            font_size=48,
            color=main_color,
        ).move_to([0, 0.75, 0])
        scaled.set_color_by_tex("u", sub_color)
        gamma_eq = MathTex(r"\int_0^\infty u^n e^{-u}\,du=n!", font_size=52, color=main_color)
        gamma_eq.move_to([0, -1.35, 0])
        gamma_eq.set_color_by_tex("n!", gamma_color)
        gamma_label = caption("Gamma integral", gamma_color, 34).next_to(gamma_eq, DOWN, buff=0.28)

        self.play(FadeIn(u_sub, scale=1.05), run_time=0.45)
        self.play(ReplacementTransform(gamma_seed, scaled), run_time=0.60)
        self.play(FadeIn(gamma_eq, shift=UP * 0.1), FadeIn(gamma_label), run_time=0.65)
        self.play(Flash(gamma_eq, color=gamma_color), Indicate(gamma_eq, color=gamma_color, scale_factor=1.04), run_time=0.60)
        self.play(FadeOut(VGroup(u_sub, scaled, gamma_label)), run_time=0.35)

        # ------------------------------------------------------------------
        # 17–20 seconds: perfect cancellation.
        # Running total ≈ 20.0s
        # ------------------------------------------------------------------
        cancel_caption = caption("Everything cancels perfectly.", final_color, 32).move_to([0, 3.2, 0])
        cancel_eq = MathTex(
            r"I=\sum_{n=0}^{\infty}{1\over n!}\,{n!\over (n+1)^{n+1}}",
            font_size=48,
            color=main_color,
        ).move_to([0, 0.95, 0])
        cancel_eq.set_color_by_tex("n!", gamma_color)
        line1 = Line([-0.55, 1.12, 0], [0.05, 0.58, 0], color=gamma_color, stroke_width=7)
        line2 = Line([0.68, 1.12, 0], [1.2, 0.58, 0], color=gamma_color, stroke_width=7)
        simplified = MathTex(
            r"I=\sum_{n=0}^{\infty}{1\over (n+1)^{n+1}}",
            font_size=54,
            color=main_color,
        ).move_to([0, 0.65, 0])
        simplified.set_color_by_tex(r"\sum", sigma_color)

        self.play(ReplacementTransform(gamma_eq, cancel_eq), FadeIn(cancel_caption), run_time=0.70)
        self.play(Create(line1), Create(line2), run_time=0.35)
        self.play(Flash(cancel_eq, color=gamma_color), run_time=0.45)
        self.play(ReplacementTransform(cancel_eq, simplified), FadeOut(line1), FadeOut(line2), run_time=0.60)
        self.play(Circumscribe(simplified, color=final_color), run_time=0.45)
        self.play(FadeOut(cancel_caption), run_time=0.20)

        # ------------------------------------------------------------------
        # 20–23 seconds: final identity and loop-friendly ending.
        # Running total ≈ 23.0s including the final hold.
        # ------------------------------------------------------------------
        reindex = MathTex(r"k=n+1", font_size=50, color=sub_color).move_to([0, 2.7, 0])
        final_sum = MathTex(r"\sum_{k=1}^{\infty}{1\over k^k}", font_size=62, color=final_color).move_to([0, 0.65, 0])
        terms_final = MathTex(
            r"1+{1\over2^2}+{1\over3^3}+{1\over4^4}+\cdots",
            font_size=45,
            color=final_color,
        ).move_to([0, -1.05, 0])
        final_top = MathTex(r"\int_0^1 x^{-x}\,dx", font_size=64, color=main_color)
        final_bottom = MathTex(r"\sum_{k=1}^{\infty}{1\over k^k}", font_size=64, color=final_color)
        final_equals = MathTex("=", font_size=58, color=main_color)
        final_group = VGroup(final_top, final_equals, final_bottom).arrange(DOWN, buff=0.12).move_to([0, 0.25, 0])
        final_box = SurroundingRectangle(final_group, color=final_color, buff=0.22, corner_radius=0.14)
        numeric_value = Tex(r"$\approx 1.291285997\ldots$", font_size=30, color=subtle)
        numeric_value.next_to(final_box, DOWN, buff=0.22)
        faint_axes = axes.copy().set_opacity(0.18).move_to([0, -3.0, 0])
        faint_graph = graph.copy().set_opacity(0.25).move_to(faint_axes.get_center())
        faint_area = area.copy().set_opacity(0.16).move_to(faint_axes.get_center())
        opening_echo = MathTex(r"\int_0^1 x^{-x}\,dx", font_size=72, color=main_color).move_to([0, 0.25, 0])

        self.play(FadeIn(reindex, shift=DOWN * 0.12), run_time=0.35)
        self.play(ReplacementTransform(simplified, final_sum), run_time=0.50)
        self.play(FadeIn(terms_final, shift=UP * 0.1), run_time=0.35)
        self.play(ReplacementTransform(VGroup(final_sum, terms_final, reindex), final_group), FadeIn(faint_axes), FadeIn(faint_area), FadeIn(faint_graph), run_time=0.70)
        self.play(Create(final_box), Circumscribe(final_group, color=final_color), FadeIn(numeric_value), run_time=0.65)
        # Optional sound: reveal impact
        self.play(Flash(final_group, color=final_color), final_group.animate.scale(1.03), final_box.animate.scale(1.03), run_time=0.45)
        self.wait(1.00)
        self.play(final_group.animate.set_opacity(0.18), final_box.animate.set_opacity(0.12), numeric_value.animate.set_opacity(0.12), FadeIn(opening_echo, scale=1.02), run_time=0.45)
        # Optional sound: soft loop transition
        self.wait(0.10)


if __name__ == "__main__":
    print("Quick test: manim -ql sophomores_dream_reel.py SophomoresDreamReel")
    print("Full-quality vertical render: manim -qh --fps 30 sophomores_dream_reel.py SophomoresDreamReel")
    print("Optional H.264: ffmpeg -i media/videos/sophomores_dream_reel/1080p30/SophomoresDreamReel.mp4 -c:v libx264 -profile:v high -level 4.1 -pix_fmt yuv420p -movflags +faststart -an sophomores_dream_instagram.mp4")
