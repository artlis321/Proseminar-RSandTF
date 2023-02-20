from manim import *
from manim_slides import Slide
import numpy as np
from scipy.spatial.transform import Rotation as R

class TestSlide(Slide):
    def torus_func(self,u,v):
        p = np.array(
            [
                (3+np.sin(v))*np.cos(u),
                (3+np.sin(v))*np.sin(u),
                np.cos(v)
            ]
        )

        r = R.from_rotvec(np.pi/2 * np.array([1, 1, 1]))
        r = np.array(r.as_matrix())

        return np.matmul(r,p)
     

    def construct(self):
        surface = Surface(
            lambda u,v : self.torus_func(u,v),
            u_range=[-PI,PI],
            v_range=[-PI,PI],
            resolution=16
        )
        self.play( Create(surface) )
        self.pause()