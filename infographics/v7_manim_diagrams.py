from manim import *
import numpy as np

# CONFIG: Clean Professional Theme
BACKGROUND_COLOR = "#0F172A"  # Dark Slate
ATTACKER_COLOR = "#F87171"    # Soft Red
VICTIM_COLOR = "#60A5FA"      # Soft Blue
DANGER_COLOR = "#F87171"      # Soft Red
SAFE_COLOR = "#34D399"        # Soft Emerald
TEXT_COLOR = "#F1F5F9"        # Slate 100
TEXT_FONT = "Montserrat"

class PhishingFlow(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR

        # 1. CREATE NODES (Global Scale Reduction built-in via scale(0.7))
        # Initial positions - we keep logic relative but will scale the final group
        
        # Professional Icons
        attacker = self.create_pro_icon("Attacker", ATTACKER_COLOR, "hacker", LEFT * 3.5)
        victim = self.create_pro_icon("Target", VICTIM_COLOR, "user", RIGHT * 0)
        
        fake_site = self.create_pro_icon("Fake Site", DANGER_COLOR, "browser", RIGHT * 2.8 + UP * 1.5)
        hacker_db = self.create_pro_icon("Hacker DB", ATTACKER_COLOR, "database", RIGHT * 2.8 + DOWN * 1.5)

        # Scale everything down centrally to ensure it fits and looks reduced (30% reduction)
        root_group = VGroup(attacker, victim, fake_site, hacker_db).scale(0.7)
        # Re-center after scaling to ensure visual balance
        root_group.move_to(ORIGIN)
        
        # We need to access individual elements again for animations, so we "unpack" after scaling
        # Note: scaling a Group scales its children, so their positions are updated.
        
        # 2. ANIMATE: Email Sent
        # Clean straight arrow
        arrow1 = Arrow(attacker.get_right(), victim.get_left(), color=TEXT_COLOR, buff=0.1, stroke_width=2, tip_length=0.2)
        
        self.play(FadeIn(root_group))
        
        # Clean Email Envelope Icon
        email_icon = VGroup(
            RoundedRectangle(corner_radius=0.05, height=0.3, width=0.5, color=TEXT_COLOR, stroke_width=1.5),
            Line(LEFT*0.25 + UP*0.15, ORIGIN, color=TEXT_COLOR, stroke_width=1.5),
            Line(RIGHT*0.25 + UP*0.15, ORIGIN, color=TEXT_COLOR, stroke_width=1.5),
        ).move_to(attacker.get_right())
        
        self.play(GrowArrow(arrow1))
        self.play(Create(email_icon), run_time=0.5)
        self.play(email_icon.animate.move_to(victim.get_center()), run_time=1.2)
        self.play(FadeOut(email_icon), Flash(victim, color=DANGER_COLOR, flash_radius=0.5, line_length=0.2))

        # 3. ANIMATE: Redirect to Fake Site
        arrow2 = Arrow(victim.get_top(), fake_site.get_left(), color=DANGER_COLOR, buff=0.1, stroke_width=2)
        self.play(GrowArrow(arrow2))

        # 4. ANIMATE: Data Theft (Clean Dashed Line)
        theft_line = DashedLine(fake_site.get_bottom(), hacker_db.get_top(), color=DANGER_COLOR, dashed_ratio=0.6)
        self.play(Create(theft_line))
        
        # Data packet animation (Simple dot)
        packet = Dot(color=DANGER_COLOR, radius=0.06).move_to(fake_site.get_bottom())
        self.play(packet.animate.move_to(hacker_db.get_top()), run_time=0.8)
        self.play(FadeOut(packet))
        
        self.wait(2)

    def create_pro_icon(self, text, color, icon_type, pos):
        """Creates a professional, clean 'Lucide-style' line-art icon"""
        
        stroke_width = 2.5 # Slightly bolder for professional look
        
        if icon_type == "database":
            # Cylinder with layers - Clean line art
            w, h = 0.8, 1.0
            
            # Top ellipse
            top = Ellipse(width=w, height=0.25, color=color, stroke_width=stroke_width)
            
            # Sides
            left_line = Line(top.get_left(), top.get_left() + DOWN*h, color=color, stroke_width=stroke_width)
            right_line = Line(top.get_right(), top.get_right() + DOWN*h, color=color, stroke_width=stroke_width)
            
            # Bottom arc
            bottom_arc = ArcBetweenPoints(left_line.get_end(), right_line.get_end(), angle=-PI, color=color, stroke_width=stroke_width)
            
            # Middle arc (layer separator)
            mid_arc = ArcBetweenPoints(left_line.get_center(), right_line.get_center(), angle=-PI, color=color, stroke_width=stroke_width)
            
            shape = VGroup(top, left_line, right_line, bottom_arc, mid_arc).move_to(ORIGIN)
            
        elif icon_type == "browser":
            # Browser window with address bar
            w, h = 1.2, 0.9
            
            frame = RoundedRectangle(corner_radius=0.1, height=h, width=w, color=color, stroke_width=stroke_width)
            
            # Header line
            header_y = h/2 - 0.25
            header_line = Line(LEFT*w/2 + UP*header_y, RIGHT*w/2 + UP*header_y, color=color, stroke_width=stroke_width/2) # Thinner separator
            
            # Address bar buttons
            btn_y = h/2 - 0.125
            btn1 = Dot(radius=0.04, color=color).move_to(LEFT*(w/2 - 0.15) + UP*btn_y)
            btn2 = Dot(radius=0.04, color=color).move_to(LEFT*(w/2 - 0.30) + UP*btn_y)
            
            shape = VGroup(frame, header_line, btn1, btn2).move_to(ORIGIN)

        elif icon_type == "user":
            # Minimalist user silhouette
            head_radius = 0.2
            body_radius = 0.35
            
            head = Circle(radius=head_radius, color=color, stroke_width=stroke_width)
            
            # Shoulders (Arc)
            shoulders = Arc(radius=body_radius, start_angle=0, angle=PI, color=color, stroke_width=stroke_width)
            # Close the bottom of shoulders? No, open look is cleaner for icons
            # But let's rotate it properly
            shoulders.rotate(PI) # Now it's an arch downwards
            
            shoulders.next_to(head, DOWN, buff=0.1)
            
            shape = VGroup(head, shoulders).move_to(ORIGIN)
            
        elif icon_type == "hacker":
            # Hooded figure (Mysterious)
            
            # Hood outline
            hood_points = [
                UL*0.4 + DOWN*0.2, # Left shoulder
                UP*0.5,            # Top of hood
                UR*0.4 + DOWN*0.2  # Right shoulder
            ]
            hood = VMobject(color=color, stroke_width=stroke_width)
            hood.set_points_smoothly([*hood_points])
            
            # Face mask / Dark void
            eye_l = Line(LEFT*0.15, LEFT*0.05, color=color, stroke_width=stroke_width).shift(UP*0.1)
            eye_r = Line(RIGHT*0.05, RIGHT*0.15, color=color, stroke_width=stroke_width).shift(UP*0.1)
            
            shape = VGroup(hood, eye_l, eye_r).move_to(ORIGIN)
            
        else: 
            shape = RoundedRectangle(corner_radius=0.1, height=0.8, width=0.8, color=color, stroke_width=stroke_width)

        # Label with clear typography
        label = Text(text, font=TEXT_FONT, font_size=20, color=TEXT_COLOR).next_to(shape, DOWN, buff=0.2)
        
        group = VGroup(shape, label).move_to(pos)
        return group


class PhishingTypes(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        
        # Center Icon - Scaled 0.7
        center_circle = Circle(radius=1.0, color=TEXT_COLOR, stroke_width=1.5)
        
        # Center Label
        center_text = Text("Phishing\nVectors", font=TEXT_FONT, font_size=24, line_spacing=1.0, color=TEXT_COLOR).move_to(center_circle.get_center())
        
        center_group = VGroup(center_circle, center_text).scale(0.7)
        self.play(Create(center_circle), Write(center_text))

        # Orbiting Types
        types = ["Spear Phishing", "Whaling", "Smishing", "Vishing", "Pharming", "Evil Twin"]
        
        # Radius for orbit (Scaled down from 2.0 to 1.5 effective visual thanks to group scaling potential, but here we calculate pos directly)
        radius = 1.8 
        
        nodes_group = VGroup()
        
        for i, text in enumerate(types):
            angle = i * (2 * PI / len(types))
            pos = radius * np.array([np.cos(angle), np.sin(angle), 0])
            
            # Simple clean node
            dot = Circle(radius=0.08, color=DANGER_COLOR, fill_opacity=1, fill_color=DANGER_COLOR).move_to(pos)
            
            # Label position optimized
            # Determine direction from center for smart label placement
            direction = pos / np.linalg.norm(pos)
            label = Text(text, font=TEXT_FONT, font_size=18, color=TEXT_COLOR).next_to(dot, direction=direction, buff=0.2)
            
            line = Line(center_circle.get_center(), dot.get_center(), color=TEXT_COLOR, stroke_opacity=0.3, stroke_width=1)
            
            anim_group = VGroup(line, dot, label)
            nodes_group.add(anim_group)
            
            self.play(Create(line), FadeIn(dot, scale=0.5), Write(label), run_time=0.4)
            
        # Final subtle rotation
        self.play(Rotate(nodes_group, angle=PI/6, about_point=ORIGIN), run_time=2, rate_func=smooth)
        
        self.wait(2)
