from manim import *
from manim_slides import Slide,ThreeDSlide

class TitleTextSlide(Slide):
    def __init__(self):
        Slide.__init__(self)
        self.last_text = None

    def set_slide_count(self,current,total):
        self.current_slide = current
        self.total_slides = total
        
        self.slide_count = Text(f"{current}/{total}",font="Arial").to_edge(DR)
        self.add(self.slide_count.scale(0.5))

    def increment(self):
        self.current_slide += 1

        self.remove(self.slide_count)
        self.slide_count = Text(f"{self.current_slide}/{self.total_slides}",font="Arial").to_edge(DR)
        self.add(self.slide_count.scale(0.5))

    def add_title(self,title):
        self.title = Text(title,weight=BOLD,font="Arial").to_edge(UL)
        self.add(self.title)

    def left_text(self,tex_object):
        if self.last_text == None:
            text = tex_object.align_to(self.title.get_bottom(),UP).align_to(self.title,LEFT).shift([0,-0.2,0])
            text.scale(0.9)
            self.play( FadeIn(text) )
            self.last_text = text
        else:
            text = tex_object.align_to(self.last_text.get_bottom(),UP).align_to(self.title,LEFT).shift([0,-0.2,0])
            text.scale(0.9)
            self.play( FadeIn(text) )
            self.last_text = text

    def middle_text(self,tex_object):
        if self.last_text == None:
            text_object = tex_object.align_to(self.title.get_bottom(),UP).shift([0,-0.2,0])
            text_object.scale(0.9)
            self.play( FadeIn(text_object) )
            self.last_text = text_object
        else:
            text_object = tex_object.align_to(self.last_text.get_bottom(),UP).shift([0,-0.2,0])
            text_object.scale(0.9)
            self.play( FadeIn(text_object) )
            self.last_text = text_object

class TitleText3DSlide(ThreeDSlide):
    def set_slide_count(self,current,total):
        self.current_slide = current
        self.total_slides = total
        
        self.slide_count = Text(f"{current}/{total}",font="Arial").to_edge(DR)
        self.add_fixed_in_frame_mobjects(self.slide_count.scale(0.5))

    def increment(self):
        self.current_slide += 1

        self.remove(self.slide_count)
        self.slide_count = Text(f"{self.current_slide}/{self.total_slides}",font="Arial").to_edge(DR)
        self.add_fixed_in_frame_mobjects(self.slide_count.scale(0.5))

    def add_title(self,title):
        self.title = Text(title,weight=BOLD,font="Arial").to_edge(UL)
        self.add_fixed_in_frame_mobjects(self.title)