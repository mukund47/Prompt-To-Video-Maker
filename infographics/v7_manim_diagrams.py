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
            hood_points = [UL*0.4 + DOWN*0.2, UP*0.5, UR*0.4 + DOWN*0.2]
            hood = VMobject(color=color, stroke_width=stroke_width)
            hood.set_points_smoothly([*hood_points])
            eye_l = Line(LEFT*0.15, LEFT*0.05, color=color, stroke_width=stroke_width).shift(UP*0.1)
            eye_r = Line(RIGHT*0.05, RIGHT*0.15, color=color, stroke_width=stroke_width).shift(UP*0.1)
            shape = VGroup(hood, eye_l, eye_r).move_to(ORIGIN)
            
        elif icon_type == "cloud":
            # Cloud silhouette
            c1 = Circle(radius=0.3, color=color, stroke_width=stroke_width).shift(LEFT*0.4)
            c2 = Circle(radius=0.45, color=color, stroke_width=stroke_width).shift(UP*0.1)
            c3 = Circle(radius=0.3, color=color, stroke_width=stroke_width).shift(RIGHT*0.4)
            base = Line(LEFT*0.5+DOWN*0.2, RIGHT*0.5+DOWN*0.2, color=color, stroke_width=stroke_width)
            shape = VGroup(c1, c2, c3, base).move_to(ORIGIN)

        elif icon_type == "shield":
            # Shield shape
            shield_pts = [UP*0.5, UP*0.5+RIGHT*0.4, DOWN*0.3+RIGHT*0.4, DOWN*0.6, DOWN*0.3+LEFT*0.4, UP*0.5+LEFT*0.4, UP*0.5]
            shape = VMobject(color=color, stroke_width=stroke_width).set_points_as_corners(shield_pts).move_to(ORIGIN)

        elif icon_type == "lock":
            # Padlock
            body = RoundedRectangle(corner_radius=0.1, height=0.5, width=0.6, color=color, stroke_width=stroke_width)
            shackle = Arc(radius=0.2, start_angle=0, angle=PI, color=color, stroke_width=stroke_width).next_to(body, UP, buff=0)
            shape = VGroup(body, shackle).move_to(ORIGIN)

        elif icon_type == "server":
            # Server rack
            frame = Rectangle(height=0.8, width=0.7, color=color, stroke_width=stroke_width)
            lines = VGroup(*[Line(LEFT*0.25, RIGHT*0.25, color=color, stroke_width=1.5).shift(UP*(0.2 - 0.2*i)) for i in range(3)])
            dots = VGroup(*[Dot(radius=0.03, color=color).shift(LEFT*0.28 + UP*(0.2 - 0.2*i)) for i in range(3)])
            shape = VGroup(frame, lines, dots).move_to(ORIGIN)

        elif icon_type == "globe":
            # Globe with grid
            circle = Circle(radius=0.5, color=color, stroke_width=stroke_width)
            h_line = Line(LEFT*0.5, RIGHT*0.5, color=color, stroke_width=1)
            v_line = Line(UP*0.5, DOWN*0.5, color=color, stroke_width=1)
            ellipse = Ellipse(width=0.4, height=1.0, color=color, stroke_width=1)
            shape = VGroup(circle, h_line, v_line, ellipse).move_to(ORIGIN)

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

class PhishingSimulation(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        
        # 1. SETUP: Split Screen (Email on Left, Terminal on Right)
        # Email Client Window
        email_window = RoundedRectangle(corner_radius=0.1, height=4, width=5, color=TEXT_COLOR, stroke_width=2).shift(LEFT * 3)
        # Re-doing window properly
        # Re-doing window properly - increasing header spacing
        email_header_line = Line(LEFT*5.3, LEFT*0.7, color=TEXT_COLOR).shift(UP*1.0)
        
        # Wrapped text for sender/subject/body to ensure it stays in box
        # Using Paragraph for better control or just scaling down
        email_sender = Text("From: HR Department\n<hr-update@fake-corp.com>", font=TEXT_FONT, font_size=14, color=ATTACKER_COLOR, line_spacing=1.2).next_to(email_header_line, DOWN, buff=0.15, aligned_edge=LEFT).shift(LEFT*0.1)
        
        email_subject = Text("Subject: URGENT:\nPayroll Action Required", font=TEXT_FONT, font_size=16, weight="BOLD", color=TEXT_COLOR, line_spacing=1.2).next_to(email_sender, DOWN, buff=0.15, aligned_edge=LEFT)
        
        email_body = Paragraph("Please confirm your details immediately", "to avoid payroll suspension.", font=TEXT_FONT, font_size=12, color=TEXT_COLOR).next_to(email_subject, DOWN, buff=0.2, aligned_edge=LEFT)
        
        link_text = Text("CLICK HERE TO VERIFY", font=TEXT_FONT, font_size=14, color=VICTIM_COLOR).next_to(email_body, DOWN, buff=0.3)
        underline = Line(link_text.get_left(), link_text.get_right(), color=VICTIM_COLOR).next_to(link_text, DOWN, buff=0.05)
        link_group = VGroup(link_text, underline)
        
        email_group = VGroup(email_window, email_header_line, email_sender, email_subject, email_body, link_group)
        
        # Terminal Window (Attacker)
        term_window = RoundedRectangle(corner_radius=0.1, height=4, width=5, color=SAFE_COLOR, stroke_width=2).shift(RIGHT * 3)
        term_label = Text("ATTACKER CONSOLE", font="Consolas", font_size=14, color=SAFE_COLOR).next_to(term_window, UP, buff=0.1)
        term_content = VGroup()
        
        self.play(Create(email_group), Create(term_window), Write(term_label))
        
        # 2. ANIMATION: Cursor movement
        cursor = Arrow(ORIGIN, UL, color=WHITE, stroke_width=4, max_tip_length_to_length_ratio=0.5).scale(0.3)
        cursor.move_to(email_window.get_bottom() + RIGHT*2)
        self.play(FadeIn(cursor))
        
        # Move to link
        self.play(cursor.animate.move_to(link_group.get_center() + DR*0.2), run_time=1.5)
        
        # Click effect
        self.play(cursor.animate.scale(0.8), link_group.animate.set_color(DANGER_COLOR), run_time=0.2)
        self.play(cursor.animate.scale(1.25), run_time=0.2)
        
        # 3. ANIMATION: Terminal Hacking Effect
        lines = [
            "Listening on port 80...",
            "GET /login.php HTTP/1.1",
            "Cookie: session_id=XYZ123",
            "[+] CREDENTIALS CAPTURED!",
            "Username: jdoe@corp.com",
            "Password: *********"
        ]
        
        prev_line = term_window.get_top() + LEFT*2.3 + DOWN*0.5
        
        for i, line in enumerate(lines):
            color = SAFE_COLOR if "[+]" not in line else DANGER_COLOR
            txt = Text(line, font="Consolas", font_size=12, color=color).next_to(prev_line, DOWN, buff=0.15, aligned_edge=LEFT)
            if i == 0:
                txt.move_to(term_window.get_top() + LEFT*2.3 + DOWN*0.5, aligned_edge=LEFT)
            
            term_content.add(txt)
            self.play(AddTextLetterByLetter(txt), run_time=0.5)
            # Need to explicitly update prev_line if it was used for relative placement
            prev_line = txt
            
            if "[+]" in line:
                 self.play(Flash(term_window, color=DANGER_COLOR, flash_radius=1.0))

        self.wait(2)

# --- EXPANSION SCENES ---

class CloudSecurityArchitecture(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        title = Text("Cloud Security Architecture", font=TEXT_FONT, font_size=32).to_edge(UP)
        
        internet = PhishingFlow.create_pro_icon(self, "Internet", TEXT_COLOR, "globe", LEFT*4.5)
        waf = PhishingFlow.create_pro_icon(self, "WAF", DANGER_COLOR, "shield", LEFT*2)
        lb = PhishingFlow.create_pro_icon(self, "Load Balancer", VICTIM_COLOR, "browser", ORIGIN)
        app = PhishingFlow.create_pro_icon(self, "App Instance", SAFE_COLOR, "server", RIGHT*2 + UP*1.2)
        db = PhishingFlow.create_pro_icon(self, "Secure DB", SAFE_COLOR, "database", RIGHT*2 + DOWN*1.2)
        
        root = VGroup(internet, waf, lb, app, db).scale(0.75).move_to(ORIGIN + DOWN*0.5)
        
        self.play(Write(title))
        self.play(FadeIn(internet), FadeIn(waf))
        self.play(Create(Arrow(internet.get_right(), waf.get_left(), color=TEXT_COLOR)))
        
        self.play(FadeIn(lb))
        self.play(Create(Arrow(waf.get_right(), lb.get_left(), color=DANGER_COLOR)))
        
        self.play(FadeIn(app), FadeIn(db))
        self.play(Create(Arrow(lb.get_right(), app.get_left(), color=TEXT_COLOR)))
        self.play(Create(Arrow(lb.get_right(), db.get_left(), color=TEXT_COLOR)))
        self.wait(2)

class HackerKillChain(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        title = Text("Hacker Kill Chain", font=TEXT_FONT, font_size=32).to_edge(UP)
        
        stages = ["Recon", "Delivery", "Exploit", "C2", "Exfil"]
        icons = ["globe", "browser", "hacker", "cloud", "database"]
        colors = [TEXT_COLOR, VICTIM_COLOR, DANGER_COLOR, ATTACKER_COLOR, SAFE_COLOR]
        
        nodes = VGroup()
        for i, (s, ic, col) in enumerate(zip(stages, icons, colors)):
            node = PhishingFlow.create_pro_icon(self, s, col, ic, ORIGIN)
            nodes.add(node)
        
        nodes.arrange(RIGHT, buff=0.8).scale(0.7)
        self.play(Write(title))
        
        for i, node in enumerate(nodes):
            self.play(FadeIn(node, shift=UP*0.5))
            if i > 0:
                self.play(Create(Line(nodes[i-1].get_right(), node.get_left(), color=colors[i], stroke_width=2)), run_time=0.3)
        
        self.wait(2)

class MalwareSpread(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        
        center = PhishingFlow.create_pro_icon(self, "Infected Host", DANGER_COLOR, "server", ORIGIN).scale(0.8)
        others = VGroup(*[
            PhishingFlow.create_pro_icon(self, f"Host {i+1}", SAFE_COLOR, "user", 2.5 * np.array([np.cos(i*TAU/6), np.sin(i*TAU/6), 0]))
            for i in range(6)
        ]).scale(0.6)
        
        self.play(FadeIn(center))
        self.play(LaggedStart(*[FadeIn(h) for h in others], lag_ratio=0.1))
        
        for h in others:
            line = Line(center.get_center(), h.get_center(), color=DANGER_COLOR, stroke_width=1, stroke_opacity=0.4)
            self.play(Create(line), run_time=0.2)
            packet = Dot(color=DANGER_COLOR, radius=0.05).move_to(center.get_center())
            self.play(packet.animate.move_to(h.get_center()), run_time=0.5)
            self.play(h.animate.set_color(DANGER_COLOR), Flash(h, color=DANGER_COLOR, flash_radius=0.3), run_time=0.3)
        
        self.wait(2)

class DataBreachSunburst(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        core = Circle(radius=1, color=DANGER_COLOR, fill_opacity=0.2, stroke_width=2)
        label = Text("DATA BREACH", font=TEXT_FONT, font_size=24, color=DANGER_COLOR)
        
        categories = ["PII", "Financial", "Corporate", "Passwords"]
        colors = [VICTIM_COLOR, SAFE_COLOR, YELLOW, ATTACKER_COLOR]
        
        sectors = VGroup()
        for i, (cat, col) in enumerate(zip(categories, colors)):
            sector = AnnularSector(inner_radius=1.1, outer_radius=2.2, angle=TAU/4, start_angle=i*TAU/4, color=col, fill_opacity=0.6)
            txt = Text(cat, font=TEXT_FONT, font_size=18, color=TEXT_COLOR).move_to(sector.get_center())
            sectors.add(VGroup(sector, txt))
            
        self.play(Create(core), Write(label))
        self.play(LaggedStart(*[FadeIn(s, shift=s[0].get_start_angle()*RIGHT) for s in sectors], lag_ratio=0.3))
        self.wait(2)

class ZeroTrustComparison(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        
        # Traditional
        trad_box = RoundedRectangle(height=4, width=3.5, color=GREY, stroke_width=2).shift(LEFT*3)
        trad_title = Text("Traditional (Perimeter)", font=TEXT_FONT, font_size=18).next_to(trad_box, UP)
        user = PhishingFlow.create_pro_icon(self, "User", VICTIM_COLOR, "user", trad_box.get_center())
        lock = PhishingFlow.create_pro_icon(self, "Firewall", SAFE_COLOR, "shield", trad_box.get_left() + LEFT*0.5)
        
        # Zero Trust
        zt_box = RoundedRectangle(height=4, width=3.5, color=SAFE_COLOR, stroke_width=2).shift(RIGHT*3)
        zt_title = Text("Zero Trust (Identity)", font=TEXT_FONT, font_size=18, color=SAFE_COLOR).next_to(zt_box, UP)
        user_zt = PhishingFlow.create_pro_icon(self, "Verify", VICTIM_COLOR, "user", zt_box.get_center() + LEFT*0.8)
        lock_zt = PhishingFlow.create_pro_icon(self, "Auth", DANGER_COLOR, "lock", zt_box.get_center() + RIGHT*0.8)
        
        self.play(Create(trad_box), Write(trad_title), FadeIn(user), FadeIn(lock))
        self.play(Create(zt_box), Write(zt_title), FadeIn(user_zt), FadeIn(lock_zt))
        
        # Traditional Trust
        self.play(Line(user.get_center(), trad_box.get_right(), color=SAFE_COLOR).animate)
        
        # Zero Trust Check
        self.play(Indicate(user_zt), Indicate(lock_zt), color=SAFE_COLOR)
        self.wait(2)

class VulnerabilityLifecycle(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        stages = ["Discovery", "Analysis", "Patching", "Deployment"]
        colors = [YELLOW, ORANGE, SAFE_COLOR, VICTIM_COLOR]
        
        circle = Circle(radius=2.2, color=GREY, stroke_opacity=0.2)
        nodes = VGroup()
        
        for i, (s, col) in enumerate(zip(stages, colors)):
            angle = i * -TAU/4 + PI/2
            pos = 2.2 * np.array([np.cos(angle), np.sin(angle), 0])
            node = PhishingFlow.create_pro_icon(self, s, col, "lock" if "Patch" in s else "shield", pos).scale(0.8)
            nodes.add(node)
            
        self.play(Create(circle))
        for i, node in enumerate(nodes):
            self.play(FadeIn(node))
            if i > 0:
                self.play(ArcBetweenPoints(nodes[i-1].get_center(), node.get_center(), radius=2.2, color=colors[i]).animate)
        
        # Close loop
        self.play(ArcBetweenPoints(nodes[-1].get_center(), nodes[0].get_center(), radius=2.2, color=colors[0]).animate)
        self.wait(2)

class SIEMCorrelationTree(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        
        root = PhishingFlow.create_pro_icon(self, "SIEM Engine", VICTIM_COLOR, "server", UP*2)
        l1 = PhishingFlow.create_pro_icon(self, "Log A", TEXT_COLOR, "browser", LEFT*2).scale(0.7)
        l2 = PhishingFlow.create_pro_icon(self, "Log B", TEXT_COLOR, "browser", RIGHT*2).scale(0.7)
        alert = PhishingFlow.create_pro_icon(self, "Alert", DANGER_COLOR, "shield", DOWN*2)
        
        self.play(FadeIn(root))
        self.play(FadeIn(l1), FadeIn(l2))
        self.play(Create(Line(l1.get_top(), root.get_bottom())), Create(Line(l2.get_top(), root.get_bottom())))
        
        # Correlation
        packet1 = Dot(color=VICTIM_COLOR).move_to(l1.get_center())
        packet2 = Dot(color=VICTIM_COLOR).move_to(l2.get_center())
        self.play(packet1.animate.move_to(root.get_center()), packet2.animate.move_to(root.get_center()))
        
        self.play(Indicate(root, color=DANGER_COLOR))
        self.play(FadeIn(alert, shift=DOWN))
        self.play(Create(Line(root.get_bottom(), alert.get_top(), color=DANGER_COLOR)))
        self.wait(2)
