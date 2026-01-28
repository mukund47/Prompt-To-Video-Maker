from manim import *

class PhishingFlow(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        
        # Colors
        NEON_BLUE = "#3B82F6"
        NEON_PURPLE = "#A855F7"
        NEON_RED = "#EF4444"
        NEON_GREEN = "#22C55E"

        # 1. Title
        title = Text("THE PHISHING ATTACK CHAIN", font="Montserrat", weight=BOLD).scale(0.8).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # 2. Nodes
        hacker = VGroup(Dot(color=NEON_PURPLE), Text("Hacker", font="Montserrat").scale(0.4).next_to(Dot(), DOWN)).shift(LEFT * 4 + UP * 1.5)
        target = VGroup(Dot(color=NEON_BLUE), Text("User", font="Montserrat").scale(0.4).next_to(Dot(), DOWN)).shift(RIGHT * 4 + UP * 1.5)
        phish_site = VGroup(Rectangle(width=2, height=1.2, color=NEON_RED), Text("Phishing Site", font="Montserrat").scale(0.4).move_to(Rectangle())).shift(DOWN * 1.5)
        orig_site = VGroup(Rectangle(width=2, height=1.2, color=NEON_GREEN), Text("Original Site", font="Montserrat").scale(0.4).move_to(Rectangle())).shift(LEFT * 4 + DOWN * 1.5)

        # 3. Animation: Step 1 - Send Email
        mail_icon = SVGMobject("mail") if False else Square(color=NEON_BLUE).scale(0.2) # Fallback to square if no SVG
        mail_text = Text("Email", font="Montserrat").scale(0.3).next_to(mail_icon, UP)
        email = VGroup(mail_icon, mail_text).move_to(hacker.get_center())

        self.play(FadeIn(hacker), FadeIn(target))
        self.play(email.animate.move_to(target.get_center()), run_time=2)
        self.play(Indicate(target, color=NEON_RED))
        
        # 4. Animation: Step 2 - Redirect to Fake Site
        arrow_to_fake = DashedLine(target.get_bottom(), phish_site.get_top(), color=NEON_BLUE)
        self.play(Create(arrow_to_fake), FadeIn(phish_site))
        self.wait(1)

        # 5. Animation: Step 3 - Data Leak to Hacker
        leak_line = DashedLine(phish_site.get_left(), hacker.get_bottom(), color=NEON_RED)
        self.play(Create(leak_line), run_time=2)
        self.play(Flash(hacker, color=NEON_RED, flash_radius=0.5))

        # 6. Animation: Step 4 - Access Original Site
        access_line = Arrow(hacker.get_bottom(), orig_site.get_top(), color=NEON_GREEN)
        self.play(Create(access_line), FadeIn(orig_site))
        self.wait(2)

class PhishingTypes(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        
        # Colors
        NEON_BLUE = "#3B82F6"
        NEON_RED = "#EF4444"
        
        # 1. Central Hook Icon (Simplified)
        center_circle = Circle(radius=1.2, color=WHITE, fill_opacity=0.1)
        hook = Triangle(color=NEON_RED).scale(0.4).rotate(180*DEGREES).move_to(center_circle.get_center())
        hook_label = Text("THE HOOK", font="Montserrat", weight=BOLD).scale(0.5).next_to(center_circle, DOWN)
        self.play(Create(center_circle), DrawBorderThenFill(hook), Write(hook_label))

        # 2. Orbiting Nodes
        labels = ["Spear Phishing", "Whaling", "Smishing", "Vishing", "Pharming", "Evil Twin"]
        nodes = VGroup()
        orbit = Circle(radius=3.2, color=GRAY, stroke_opacity=0.3)
        self.add(orbit)

        for i, label_txt in enumerate(labels):
            angle = i * (TAU / 6)
            pos = 3.2 * np.array([np.cos(angle), np.sin(angle), 0])
            
            node_dot = Dot(color=NEON_BLUE).move_to(pos)
            node_label = Text(label_txt, font="Montserrat").scale(0.4).next_to(node_dot, pos/np.linalg.norm(pos))
            node = VGroup(node_dot, node_label)
            nodes.add(node)
            
            self.play(FadeIn(node), Create(Line(center_circle.get_center(), node_dot.get_center(), color=NEON_BLUE, stroke_opacity=0.2)), run_time=0.5)

        self.wait(3)
