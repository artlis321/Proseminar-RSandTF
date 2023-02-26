from manim import *
from manim_slides import Slide,ThreeDSlide
import numpy as np
from scipy.spatial.transform import Rotation as R

class TestSlide(ThreeDSlide):
    def torus_func(self,u,v,rot):
        p = np.array(
            [
                (3+np.sin(v))*np.cos(u),
                (3+np.sin(v))*np.sin(u),
                np.cos(v)
            ]
        )

        r = R.from_rotvec(rot)
        r = np.array(r.as_matrix())

        out = np.matmul(r,p)
        #print(out)

        return out
     

    def construct(self):
        axes = ThreeDAxes(x_range=[-4,4], x_length=8)
        rot = np.pi/2*np.array([0,0,0])

        self.set_camera_orientation(phi=PI/4)

        torus = Surface(
            lambda u,v : self.torus_func(u,v,rot),
            u_range=[0,TAU],
            v_range=[0,TAU],
            resolution=16,
            checkerboard_colors = [GRAY_D,GRAY_C]
        )
        self.play( Create(torus) )
        
        self.wait(2/60)
        self.pause()

        curve_a = ParametricFunction(
            lambda t : self.torus_func(0,t,rot), color=RED, t_range=[0,TAU]
        )
        self.play( Create(curve_a) )

        self.wait(2/60)
        self.pause()

        curve_b = ParametricFunction(
            lambda t : self.torus_func(t,0,rot), color=BLUE, t_range=[0,TAU]
        )
        self.play( Create(curve_b) )

        self.wait(2/60)
        self.pause()

        self.move_camera(frame_center=[6,0,0], zoom=0.6)

        self.wait(2/60)
        self.pause()

        torus_copy = torus.copy()
        curve_a1_copy = curve_a.copy()
        curve_a2_copy = curve_a.copy()
        curve_b1_copy = curve_b.copy()
        curve_b2_copy = curve_b.copy()

        flat_func = lambda u,v: np.array([12+PI-v,0+PI-u,0])

        flattened = Surface(
            lambda u,v : flat_func(u,v),
            u_range=[0,TAU],
            v_range=[0,TAU],
            resolution=16,
            checkerboard_colors = [GRAY_D,GRAY_C]
        )

        curve_a1_dest = ParametricFunction(
            lambda t : flat_func(0,t), color=RED, t_range=[0,TAU]
        )

        curve_a2_dest = ParametricFunction(
            lambda t : flat_func(TAU,t), color=RED, t_range=[0,TAU]
        )

        curve_b1_dest = ParametricFunction(
            lambda t : flat_func(t,0), color=BLUE, t_range=[0,TAU]
        )

        curve_b2_dest = ParametricFunction(
            lambda t : flat_func(t,TAU), color=BLUE, t_range=[0,TAU]
        )

        self.play(
            Transform(torus_copy,flattened,run_time=3),
            Transform(curve_a1_copy,curve_a1_dest,run_time=3),
            Transform(curve_a2_copy,curve_a2_dest,run_time=3),
            Transform(curve_b1_copy,curve_b1_dest,run_time=3),
            Transform(curve_b2_copy,curve_b2_dest,run_time=3)
        )

        self.wait(2/60)
        self.pause()

        text = Tex('$\longleftrightarrow$')
        text.set_x(6)

        self.play( Write(text) )

        self.wait(2/60)
        self.pause()

        
        