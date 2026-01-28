from manim import *
import numpy as np

# CONFIG: Dark Mode, Neon Colors
BACKGROUND_COLOR = "#000000"
ATTACKER_COLOR = "#A855F7" # Purple
VICTIM_COLOR = "#3B82F6"   # Blue
DANGER_COLOR = "#EF4444"   # Red
TEXT_FONT = "Montserrat"

class PhishingFlow(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR

        # 1. CREATE NODES (Aligned via code)
        # Using shift to mimic positioning relative to center or other objects
        attacker = self.create_node("Attacker", ATTACKER_COLOR, LEFT * 5)
        # Email icon made of shapes
        email_icon = RoundedRectangle(corner_radius=0.2, height=0.8, width=1.2, color=WHITE).move_to(LEFT * 2.5)
        
        victim = self.create_node("Target", VICTIM_COLOR, RIGHT * 0)
        fake_site = self.create_node("Fake Site", DANGER_COLOR, RIGHT * 4 + UP * 2)
        hacker_db = self.create_node("Hacker DB", ATTACKER_COLOR, RIGHT * 4 + DOWN * 2)

        # 2. ANIMATE: Email Sent
        arrow1 = Arrow(attacker.get_right(), victim.get_left(), color=WHITE)
        self.play(FadeIn(attacker), FadeIn(victim))
        self.play(GrowArrow(arrow1))
        self.play(Create(email_icon), run_time=1)
        self.play(email_icon.animate.move_to(victim.get_center()), run_time=1.5)
        self.play(FadeOut(email_icon), Flash(victim, color=DANGER_COLOR))

        # 3. ANIMATE: Redirect to Fake Site
        arrow2 = Arrow(victim.get_top(), fake_site.get_left(), color=DANGER_COLOR)
        self.play(FadeIn(fake_site), GrowArrow(arrow2))

        # 4. ANIMATE: Data Theft (Dashed Line)
        # Manim handles the dashed alignment perfectly
        theft_line = DashedLine(fake_site.get_bottom(), hacker_db.get_top(), color=DANGER_COLOR)
        self.play(FadeIn(hacker_db), Create(theft_line))
        self.wait(2)

    def create_node(self, text, color, pos):
        box = RoundedRectangle(corner_radius=0.2, height=1.2, width=2.5, color=color, fill_opacity=0.2, fill_color=color)
        label = Text(text, font=TEXT_FONT, font_size=24, color=WHITE)
        group = VGroup(box, label).move_to(pos)
        return group

class PhishingTypes(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        
        # Center Icon
        center_circle = Circle(radius=1.5, color=WHITE, fill_opacity=0.1)
        center_text = Text("Phishing\\nVectors", font=TEXT_FONT, font_size=36).move_to(center_circle.get_center())
        self.play(Create(center_circle), Write(center_text))

        # Orbiting Types
        types = ["Spear Phishing", "Whaling", "Smishing", "Vishing", "Pharming", "Evil Twin"]
        
        for i, text in enumerate(types):
            # Mathematical positioning (Polar coordinates)
            angle = i * (2 * PI / len(types))
            # Adjust radius to fit screen - 4 might be too wide for standard config, using 3.5
            pos = 3.5 * np.array([np.cos(angle), np.sin(angle), 0])
            
            dot = Dot(color=DANGER_COLOR).move_to(pos)
            # Position text specifically to avoid overlapping the dot, moving it outwards
            label = Text(text, font=TEXT_FONT, font_size=24).next_to(dot, direction=pos)
            
            line = Line(center_circle.get_center(), dot.get_center(), color=GRAY, stroke_opacity=0.5)
            
            self.play(Create(line), FadeIn(dot), Write(label), run_time=0.5)
        
        self.wait(2)
