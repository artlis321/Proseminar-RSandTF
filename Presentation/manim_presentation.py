from manim import *
from manim_slides import Slide
import numpy as np
from scipy.spatial.transform import Rotation as R

class TestSlide(Slide):
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

        return np.matmul(r,p)
     

    def construct(self):
        rot = np.pi/2*np.array([1,1,1])

        surface = Surface(
            lambda u,v : self.torus_func(u,v,rot),
            u_range=[-PI,PI],
            v_range=[-PI,PI],
            resolution=16
        )
        self.play( Create(surface) )
        self.pause()

        rot = np.pi/2*np.array([0,0,0])
        surface_rotated = Surface(
            lambda u,v : self.torus_func(u,v,rot),
            u_range=[-PI,PI],
            v_range=[-PI,PI],
            resolution=16
        )

        self.play( Transform(surface,surface_rotated) )
        self.pause()

        text = Text("THE TORUS DOESN'T WORK :(")
        self.play( Write(text) )

        self.pause()
        