from manim import *
from manim_slides import Slide,ThreeDSlide
from my_slide_classes import TitleTextSlide,TitleText3DSlide
import numpy as np
from scipy.spatial.transform import Rotation as R

class TestSlide(TitleText3DSlide):
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
        self.camera.background_color="#bbbbbb"

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

        
class GenusNTorus(TitleText3DSlide):
    def construct(self):
        #####
        GENUS = 3
        DISPLAY = 3
        POLYGON_RADIUS = 2.5
        POLYGON_Z = -1
        TORUS_HOLE_RADIUS = 1.5
        TORUS_BRANCH_RADIUS = 1

        SURFACE_LEFT_COLORS = [[RED_C,RED_D],[GREEN_C,GREEN_D],[YELLOW_C,YELLOW_D]]
        SURFACE_RIGHT_COLORS = [[BLUE_C,BLUE_D],[PURPLE_C,PURPLE_D],[TEAL_C,TEAL_D]]
        A_CYCLE_COLORS = [RED,GREEN,YELLOW]
        B_CYCLE_COLORS = [BLUE,PURPLE,TEAL]

        self.set_camera_orientation(phi=PI/4,zoom=0.5)
        #####
        N = GENUS

        polygon_angle = PI*(1-1/N)
        polygon_unscaled_radius = 1/np.cos(polygon_angle/2)
        polygon_scaling = POLYGON_RADIUS / polygon_unscaled_radius
        radius_power = 2
        def display_polygon(u,v,index,genus):
            if u <= PI:
                return display_polygon_right(u,v,index,genus)
            else:
                return display_polygon_left(u,v,index,genus)

        def display_polygon_right(u,v,index,genus):
            center_angle = TAU*(index-1/4)/genus
            center_location = np.array([POLYGON_RADIUS*np.cos(center_angle),POLYGON_RADIUS*np.sin(center_angle),-POLYGON_Z])

            point_angle = (PI-u)/PI*polygon_angle

            if point_angle > polygon_angle / 2:
                point_radius = (TAU-v)/TAU * polygon_scaling / np.cos(polygon_angle-point_angle)
            else:
                point_radius = (TAU-v)/TAU * polygon_scaling / np.cos(point_angle)

            relative_angle = point_angle+center_angle-polygon_angle/2
            relative_location = -np.array([point_radius*np.cos(relative_angle),point_radius*np.sin(relative_angle),0])

            cartesian_coords = -(center_location + relative_location)

            return cartesian_coords * np.linalg.norm(cartesian_coords)**(radius_power-1)
        
        def display_polygon_left(u,v,index,genus):
            center_angle = TAU*(index+1/4)/genus
            center_location = np.array([POLYGON_RADIUS*np.cos(center_angle),POLYGON_RADIUS*np.sin(center_angle),-POLYGON_Z])

            point_angle = (u-PI)/PI*polygon_angle

            if point_angle > polygon_angle / 2:
                point_radius = v/TAU * polygon_scaling / np.cos(polygon_angle-point_angle)
            else:
                point_radius = v/TAU * polygon_scaling / np.cos(point_angle)
            
            relative_angle = point_angle+center_angle-polygon_angle/2
            relative_location = -np.array([point_radius*np.cos(relative_angle),point_radius*np.sin(relative_angle),0])

            cartesian_coords = -(center_location + relative_location)

            return cartesian_coords * np.linalg.norm(cartesian_coords)**(radius_power-1)
        
        torus_radius = TORUS_HOLE_RADIUS + TORUS_BRANCH_RADIUS
        def torus_to_cylindrical(angles):
            theta,phi = angles
            # theta goes around internal hole
            # phi goes around external hole
            return ((torus_radius+TORUS_BRANCH_RADIUS*np.sin(theta)), phi, TORUS_BRANCH_RADIUS*np.cos(theta))
        
        def cylindrical_to_cartesian(coords):
            r,phi,z = coords

            return np.array([
                r*np.cos(phi),
                r*np.sin(phi),
                z
            ])
        
        torus_split = 1/N
        def cut_torus(coords,index,genus):
            x,y,z = coords
            x -= torus_radius

            r = np.sqrt(x*x+y*y)
            phi = np.arctan2(y,x)
            if phi < 0:
                phi += TAU
            
            phi = phi*torus_split+(1-torus_split)*PI+TAU/genus*index
            
            cartesian_coords = cylindrical_to_cartesian((r,phi,z))

            return cartesian_coords

        def torus_curve(start_theta,theta_rate,phi):
            return (start_theta+theta_rate*phi,phi)
        
        def torus(u,v):
            if u <= PI:
                return torus_curve(
                    2*u,
                    -u/PI,
                    v
                )
            else:
                return torus_curve(
                    0,
                    -(TAU-u)/PI,
                    v
                )
            
        def display_torus(u,v,index,genus):
            torus_coords = torus(u,v)
            cylindrical_coords = torus_to_cylindrical(torus_coords)
            cartesian_coords = cylindrical_to_cartesian(cylindrical_coords)
            cut_coords = cut_torus(cartesian_coords,index,genus)
            return cut_coords

        RANGE = [0,TAU]

        s_R_torus = [
            Surface(
                lambda u,v : display_torus(u,v,i,N), # display_torus(u,v,i,N),
                u_range = [0,PI],
                v_range = RANGE,
                checkerboard_colors=SURFACE_RIGHT_COLORS[i],
                resolution=8
            )
            for i in range(DISPLAY)
        ]

        s_L_torus = [
            Surface(
                lambda u,v : display_torus(u,v,i,N), # display_torus(u,v,i,N),
                u_range = [PI+1e-9,TAU],
                v_range = RANGE,
                checkerboard_colors=SURFACE_LEFT_COLORS[i],
                resolution=8
            )
            for i in range(DISPLAY)
        ]

        a_L_torus = [
            ParametricFunction(
                lambda t : display_torus(PI,t,i,N), # display_torus(PI,t,i,N),
                t_range = RANGE,
                color=A_CYCLE_COLORS[i]
            )
            for i in range(DISPLAY)
        ]

        a_R_torus = [
            ParametricFunction(
                lambda t : display_torus(PI+1e-9,t,i,N), # display_torus(PI,t,i,N),
                t_range = RANGE,
                color=A_CYCLE_COLORS[i]
            )
            for i in range(DISPLAY)
        ]

        b_L_torus = [
            ParametricFunction(
                lambda t : display_torus(0,t,i,N), # display_torus(0,t,i,N),
                t_range = RANGE,
                color=B_CYCLE_COLORS[i]
            )
            for i in range(DISPLAY)
        ]

        b_R_torus = [
            ParametricFunction(
                lambda t : display_torus(TAU,t,i,N), # display_polygon(TAU,t,i,N),
                t_range = RANGE,
                color=B_CYCLE_COLORS[i]
            )
            for i in range(DISPLAY)
        ]
        
        s_R_polygon = [
            Surface(
                lambda u,v : display_polygon(u,v,i,N), # display_polygon(u,v,i,N),
                u_range = [0,PI],
                v_range = RANGE,
                checkerboard_colors=SURFACE_RIGHT_COLORS[i],
                resolution=8
            )
            for i in range(DISPLAY)
        ]

        s_L_polygon = [
            Surface(
                lambda u,v : display_polygon(u,v,i,N), # display_polygon(u,v,i,N),
                u_range = [PI+1e-9,TAU],
                v_range = RANGE,
                checkerboard_colors=SURFACE_LEFT_COLORS[i],
                resolution=8
            )
            for i in range(DISPLAY)
        ]

        a_L_polygon = [
            ParametricFunction(
                lambda t : display_polygon(PI,t,i,N), # display_polygon(PI,t,i,N),
                t_range = RANGE,
                color=A_CYCLE_COLORS[i]
            )
            for i in range(DISPLAY)
        ]

        a_R_polygon = [
            ParametricFunction(
                lambda t : display_polygon(PI+1e-9,t,i,N), # display_polygon(PI,t,i,N),
                t_range = RANGE,
                color=A_CYCLE_COLORS[i]
            )
            for i in range(DISPLAY)
        ]

        b_L_polygon = [
            ParametricFunction(
                lambda t : display_polygon(0,t,i,N), # display_polygon(0,t,i,N),
                t_range = RANGE,
                color=B_CYCLE_COLORS[i]
            )
            for i in range(DISPLAY)
        ]

        b_R_polygon = [
            ParametricFunction(
                lambda t : display_polygon(TAU,t,i,N), # display_polygon(TAU,t,i,N),
                t_range = RANGE,
                color=B_CYCLE_COLORS[i]
            )
            for i in range(DISPLAY)
        ]

        objects_torus = s_L_torus+s_R_torus+a_L_torus+a_R_torus+b_L_torus+b_R_torus

        objects_polygon = s_L_polygon+s_R_polygon+a_L_polygon+a_R_polygon+b_L_polygon+b_R_polygon

        self.add( *objects_torus )

        self.begin_ambient_camera_rotation(rate=TAU/6)
        self.wait(6)
        self.stop_ambient_camera_rotation()

        self.play( *[Transform(T,P,run_time=12) for (T,P) in zip(objects_torus,objects_polygon)] )

        #self.wait(1)
        