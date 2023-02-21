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
        rot = np.pi/2*np.array([1,1,1])

        surface = Surface(
            lambda u,v : axes.c2p(*self.torus_func(u,v,rot)),
            u_range=[-PI,PI],
            v_range=[-PI,PI],
            resolution=16
        )
        self.play( Create(surface) )
        self.pause()

        text = Text("THE TORUS WORKS :)")
        self.add_fixed_in_frame_mobjects(text)
        self.remove(text)

        self.move_camera(phi=PI/2,theta=PI/2,run_time=2)
        self.pause()

        self.play( Write(text,run_time=1) )

        self.pause()
        