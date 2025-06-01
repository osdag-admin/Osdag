from .plate import Plate
from .filletweld import FilletWeld
import math
import numpy

# OCC Imports
from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Trsf, gp_Ax1, gp_Dir
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakePolygon, BRepBuilderAPI_MakeFace, BRepBuilderAPI_Transform, BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire
from OCC.Core.BRepPrimAPI import  BRepPrimAPI_MakePrism
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse, BRepAlgoAPI_Cut
from OCC.Core.AIS import AIS_Shape
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Core.Graphic3d import Graphic3d_NOM_ALUMINIUM, Graphic3d_MaterialAspect
from OCC.Display.SimpleGui import init_display






class PlateGirder:

    def __init__(self,D,tw,length,gap,T_ft,T_fb,B_ft,B_fb):
        super(PlateGirder, self).__init__()
        self.D =D
        self.tw =tw
        self.length =length
        self.gap =gap 
        self.T_ft =T_ft
        self.T_fb =T_fb
        self.B_ft =B_ft
        self.B_fb =B_fb
        
    def createPlateGirder(self):
        #central plate
        #self.D = self.total_depth # total depth
        #self.tw = self.web_thickness #web thickness
        # length = self.length #length along Y axis or length of the section

        # gap = self.c #space between each stiffner plate
        chamfer_length = 20 #traingular chamfer length hard coding the value


        L_top = self.length #length of top plate of I section
        L_bottom = self.length #length of bottom plate of I section

        bottom_outstand = 30 #bottom outstand
        top_outstand = 50 #top outstand


        stiffener_weld_height = None
        web_flange_weld_height = 5 #height of weld for web flange hard coding the value


        # #top and bottom flange
        # T_ft = self.top_flange_thickness #top flange thickness
        # T_fb = self.bottom_flange_thickness #bottom flange thickness
        # B_ft = self.top_flange_width #breadth or width of top flange
        # B_fb = self.bottom_flange_width #breadth or width of bottom flange



        # stiffener's dimensions
        L = (min(self.B_ft, self.B_fb)-self.tw)/2 -10 #horizontal length
        T_is = 5 #thickness of stiffener # need to check this
        W = self.D - (self.T_fb+self.T_ft) #vertical height

        #weld dimensions
        b = 5
        h = 5
        h=b
        l = L - chamfer_length


        # Define the colors using Quantity_Color
        center_plate_color = Quantity_Color(5/255, 5/255, 255/255, Quantity_TOC_RGB) 
        top_bottom_plate_color = Quantity_Color(137/255, 95/255, 16/255, Quantity_TOC_RGB) 

        def plate_model_with_color(origin, l, b, h, color):
            plate_origin = origin
            plate_uDir = numpy.array([0.,0.,1.])
            plate_wDir = numpy.array([0.,1.,0.])
            plate = Plate(l, b, h)
            _place = plate.place(plate_origin, plate_uDir, plate_wDir)
            plate_point = plate.compute_params()
            plate_shape = plate.create_model()

            # Apply the color to the plate shape using AIS_Shape
            ais_shape = AIS_Shape(plate_shape)
            ais_shape.SetColor(color)
            display.Context.Display(ais_shape, True)

            return plate_shape



        print("model generating......")



        start_gap = end_gap = self.gap # gap at front and back 


        #initialisation of the display method to display the 3D model
        display, start_display, add_menu, add_function_to_menu = init_display()
        display.set_bg_gradient_color([51, 51, 102], [150, 150, 170]) 



        center_plate = plate_model_with_color(numpy.array([0., 0., 0.]) ,self.tw, self.length,self.D, center_plate_color)
        top_plate = plate_model_with_color(numpy.array([0, 0, (self.D + self.T_ft) // 2]) , self.B_ft, L_top, self.T_ft, top_bottom_plate_color)
        bottom_plate = plate_model_with_color(numpy.array([0, 0, -(self.D+self.T_fb) // 2]) , self.B_fb, L_bottom, self.T_fb, top_bottom_plate_color)


        ISection_model = BRepAlgoAPI_Fuse(bottom_plate, top_plate).Shape()
        #ISection_model = BRepAlgoAPI_Fuse(ISection_model, bottom_plate).Shape()

        def translation_movement(x,y,z, model):
            trsf = gp_Trsf()
            translation_vector = gp_Vec(x, y, z)
            trsf.SetTranslation(translation_vector)
            model = BRepBuilderAPI_Transform(model, trsf).Shape()
            return model

        def translation_rotation(angle,axis, model):
            trsf = gp_Trsf()
            trsf.SetRotation(axis, math.radians(angle))
            model = BRepBuilderAPI_Transform(model, trsf).Shape()
            return model

        def triangle_model(p1,p2,p3, thickness):
            
            polygon = BRepBuilderAPI_MakePolygon()
            polygon.Add(p1)
            polygon.Add(p2)
            polygon.Add(p3)
            polygon.Close() 
            face = BRepBuilderAPI_MakeFace(polygon.Shape()).Face()
            direction = gp_Vec(0, 3*thickness, 0)
            extrusion = BRepPrimAPI_MakePrism(face, direction)
            triangle_3d = extrusion.Shape()
            ais_shape = AIS_Shape(triangle_3d)

            return ais_shape.Shape()


        def create_weld_model(thickness, width, position, direction):
            origin = position
            
            if direction=='y':
                uDir = numpy.array([0., 0., 1.])
                shaftDir = numpy.array([0., 1., 0.])

            elif direction=='x':
                uDir = numpy.array([0., 0., 1.])
                shaftDir = numpy.array([1., 0., 0.])

            elif direction=='z':
                uDir = numpy.array([1., 0., 0.])
                shaftDir = numpy.array([0., 0., 1.])

            FWeld = FilletWeld(thickness, thickness, width)
            _place = FWeld.place(origin, uDir, shaftDir)
            point = FWeld.compute_params()
            prism = FWeld.create_model(0)

            return prism


        def create_corner_cutout(model, coordinates, thickness, side):

            x = coordinates[0]
            y = coordinates[1]
            z = coordinates[2]
            # extra_gap = chamfer_length+4
            if side=="right":
                #top triangle cutout
                t_p1 = gp_Pnt(self.tw//2, y-thickness,self.D//2)  
                t_p2 = gp_Pnt(self.tw//2, y-thickness, (self.D//2)-chamfer_length) 
                t_p3 = gp_Pnt((self.tw//2)+chamfer_length, y-thickness,self.D//2) 

                top_triangle = triangle_model(t_p1,t_p2,t_p3, thickness)
                model = BRepAlgoAPI_Cut(model, top_triangle).Shape()


                #bottom triangle cutout
                b_p1 = gp_Pnt(self.tw//2, y-thickness, -self.D//2)  
                b_p2 = gp_Pnt(self.tw//2, y-thickness, -(self.D//2)+chamfer_length) 
                b_p3 = gp_Pnt((self.tw//2)+chamfer_length, y-thickness, -self.D//2) 

                bottom_triangle= triangle_model(b_p1,b_p2,b_p3, thickness)
                final_model = BRepAlgoAPI_Cut(model, bottom_triangle).Shape()
                

            if side=="left":
                #top triangle cutout
                t_p1 = gp_Pnt(-self.tw//2, y-thickness,self.D//2)  
                t_p2 = gp_Pnt(-self.tw//2, y-thickness, (self.D//2)-chamfer_length) 
                t_p3 = gp_Pnt(-(self.tw//2)-chamfer_length, y-thickness,self.D//2) 

                top_triangle = triangle_model(t_p1,t_p2,t_p3, thickness)
                model = BRepAlgoAPI_Cut(model, top_triangle).Shape()


                #bottom triangle cutout
                b_p1 = gp_Pnt(-self.tw//2, y-thickness, -(self.D//2))     
                b_p2 = gp_Pnt(-self.tw//2, y-thickness, -(self.D//2)+chamfer_length)   
                b_p3 = gp_Pnt(-(self.tw//2)-chamfer_length, y-thickness, -(self.D//2)) 

                bottom_triangle= triangle_model(b_p1,b_p2,b_p3, thickness)
                final_model = BRepAlgoAPI_Cut(model, bottom_triangle).Shape()
                

            return final_model


        def stiffner_plate(position, L,D, T_is, direction):
            '''
            this function returns stiffner plate with corner cutout, hence this function can be called multiple times inside for loop
            '''
            
            #creating stiffner plate model 

            #plate_origin = numpy.array([-L//2-self.tw//2,remaining_gap,-D//2])
            plate_origin = position
            plate_uDir = numpy.array([0.,1.,0.])
            plate_wDir = numpy.array([0.,0.,1.])
            plate = Plate(L,self.D, T_is)
            _place = plate.place(plate_origin, plate_uDir, plate_wDir)
            point = plate.compute_params()
            stiffner_plate_model = plate.create_model()
            
            #punching cutouts in the stiffner plate
            stiffner_plate_model = create_corner_cutout(stiffner_plate_model, plate_origin, T_is, direction)

            return stiffner_plate_model


        def vertical_weld(weld_height, length):
            '''
            this function creates vertical weld between stiffner plate and the vertical plate of the I section plate
            '''
            p1 = gp_Pnt(0, 0, 0)
            p2 = gp_Pnt(weld_height, 0, 0)
            p3 = gp_Pnt(0, -weld_height, 0)
            edge1 = BRepBuilderAPI_MakeEdge(p1, p2).Edge()
            edge2 = BRepBuilderAPI_MakeEdge(p2, p3).Edge()
            edge3 = BRepBuilderAPI_MakeEdge(p3, p1).Edge()
            wire = BRepBuilderAPI_MakeWire(edge1, edge2, edge3).Wire()
            face = BRepBuilderAPI_MakeFace(wire).Face()
            extrude_vec = gp_Vec(0, 0, length)
            solid = BRepPrimAPI_MakePrism(face, extrude_vec).Shape()
            return solid


        def filletWeld_model(b, h, l, y, position, T_is):
            origin = numpy.array([0., 0., 0.])
            uDir = numpy.array([0., 0., 1.])
            shaftDir = numpy.array([1., 0., 0.])
            FWeld = FilletWeld(b, h, l)
            _place = FWeld.place(origin, uDir, shaftDir)
            point = FWeld.compute_params()
            prism = FWeld.create_model(0)
            angle = 0
            axis = gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(1, 0, 0))
            x=0
            '''
            position if statement for right and left weld   
            '''
            if position=="right":
                x=self.tw//2+chamfer_length
            
            if position=="left":
                x=(-self.tw//2)-l-chamfer_length
            

            #formation of front weld

            
            #down
            trsf = gp_Trsf()
            angle = 0
            trsf.SetRotation(axis, math.radians(angle))
            prism_down = BRepBuilderAPI_Transform(prism, trsf).Shape()

            #up
            trsf = gp_Trsf()
            angle = 90
            trsf.SetRotation(axis, math.radians(angle))
            prism_up = BRepBuilderAPI_Transform(prism, trsf).Shape()
            
            #translation
            prism_up = translation_movement(x, y-T_is//2,self.D//2, prism_up)

            prism_down = translation_movement( x, y-T_is//2, -(self.D//2), prism_down)


            weld_fused_forward= BRepAlgoAPI_Fuse(prism_up, prism_down).Shape()

            #for behind weld

            #down
            trsf = gp_Trsf()
            angle = 270
            trsf.SetRotation(axis, math.radians(angle))
            prism_down = BRepBuilderAPI_Transform(prism, trsf).Shape()

            #up
            trsf = gp_Trsf()
            angle = 180
            trsf.SetRotation(axis, math.radians(angle))
            prism_up = BRepBuilderAPI_Transform(prism, trsf).Shape()
            
            #translation
            prism_up = translation_movement( x, y+T_is//2,self.D//2, prism_up)

            prism_down = translation_movement( x, y+T_is//2, -self.D//2, prism_down)

            weld_fused_behind= BRepAlgoAPI_Fuse(prism_up, prism_down)
            if weld_fused_behind.IsDone():
                weld_fused_behind = weld_fused_behind.Shape()

            weld_fused = BRepAlgoAPI_Fuse(weld_fused_forward,weld_fused_behind)
            if weld_fused.IsDone():
                weld_fused = weld_fused.Shape()

            return weld_fused

        #bottom weld across longitudinal direction
        right_bottom_weld = create_weld_model(0.5*chamfer_length, self.length, numpy.array([self.tw//2, 0.,(-self.D//2)]), "y")
        left_bottom_weld = create_weld_model(0.5*chamfer_length, self.length, numpy.array([-self.tw//2, 0.,(-self.D//2)]),"y")
        axis = gp_Ax1(gp_Pnt(-self.tw//2, 0.,(-self.D//2)), gp_Dir(0, 1, 0))
        trsf = gp_Trsf()
        angle = -90
        trsf.SetRotation(axis, math.radians(angle))
        left_bottom_weld = BRepBuilderAPI_Transform(left_bottom_weld, trsf).Shape()

        #top weld across longitudinal direction
        right_top_weld = create_weld_model(0.5*chamfer_length, self.length, numpy.array([self.tw//2, 0.,(self.D//2)]), "y")
        axis = gp_Ax1(gp_Pnt(self.tw//2, 0.,(self.D//2)), gp_Dir(0, 1, 0))
        trsf = gp_Trsf()
        angle = 90
        trsf.SetRotation(axis, math.radians(angle))
        right_top_weld = BRepBuilderAPI_Transform(right_top_weld, trsf).Shape()

        left_top_weld = create_weld_model(0.5*chamfer_length, self.length, numpy.array([-self.tw//2, 0.,(self.D//2)]),"y")
        axis = gp_Ax1(gp_Pnt(-self.tw//2, 0.,(self.D//2)), gp_Dir(0, 1, 0))
        trsf = gp_Trsf()
        angle = 180
        trsf.SetRotation(axis, math.radians(angle))
        left_top_weld = BRepBuilderAPI_Transform(left_top_weld, trsf).Shape()

        longitudinal_weld = BRepAlgoAPI_Fuse(right_bottom_weld, left_bottom_weld).Shape()
        longitudinal_weld = BRepAlgoAPI_Fuse(longitudinal_weld, right_top_weld).Shape()
        longitudinal_weld = BRepAlgoAPI_Fuse(longitudinal_weld, left_top_weld).Shape()

        #vertical weld test
        vertical_weld_height = 0.5*chamfer_length #vertical weld height is fixed as 0.5*chamfer_length
        stiffner_vertical_weld = vertical_weld(vertical_weld_height,self.D-(2*chamfer_length))


        for y in range(self.gap, self.length, self.gap):

            right_stiffner_plate = stiffner_plate(numpy.array([(L/2)+self.tw/2,y,-self.D/2]), L,self.D, T_is, "right") 
            left_stiffner_plate = stiffner_plate(numpy.array([-L/2-self.tw/2,y,-self.D/2]), L,self.D, T_is, "left")
            
            right_horizontal_stiffner_weld = filletWeld_model(b,h,l,y,"right", T_is)
            left_horizontal_stiffner_weld = filletWeld_model(b,h,l,y,"left", T_is)

            right_vertical_front_weld = translation_movement(self.tw/2 ,y , (-self.D/2) + chamfer_length, stiffner_vertical_weld)
            right_vertical_rear_weld = translation_rotation(180, gp_Ax1(gp_Pnt(0., 0., 0.), gp_Dir(0, 0, 1)), stiffner_vertical_weld)
            right_vertical_rear_weld = translation_movement((self.tw/2)+vertical_weld_height ,y+(T_is/2) , (-self.D/2) + chamfer_length , right_vertical_rear_weld)
            
            left_vertical_front_weld = translation_rotation(-90, gp_Ax1(gp_Pnt(0., 0., 0.), gp_Dir(0, 0, 1)), stiffner_vertical_weld)
            left_vertical_front_weld = translation_movement(-self.tw/2 ,y , (-self.D/2) + chamfer_length, left_vertical_front_weld)
            left_vertical_rear_weld = translation_rotation(-180, gp_Ax1(gp_Pnt(0., 0., 0.), gp_Dir(0, 0, 1)), stiffner_vertical_weld)
            left_vertical_rear_weld = translation_movement((-self.tw/2) ,y+(T_is/2) , (-self.D/2) + chamfer_length , left_vertical_rear_weld)
            

            if y==self.gap:
                stiffner_plate_model = BRepAlgoAPI_Fuse(right_stiffner_plate, left_stiffner_plate).Shape()
                stiffner_horizontal_weld = BRepAlgoAPI_Fuse(right_horizontal_stiffner_weld, left_horizontal_stiffner_weld).Shape()
                right_vertical_weld = BRepAlgoAPI_Fuse(right_vertical_front_weld, right_vertical_rear_weld).Shape()
                left_vertical_weld = BRepAlgoAPI_Fuse(left_vertical_front_weld, left_vertical_rear_weld).Shape()

            else:
                stiffner_plate_model = BRepAlgoAPI_Fuse(stiffner_plate_model, right_stiffner_plate).Shape()
                stiffner_plate_model = BRepAlgoAPI_Fuse(stiffner_plate_model, left_stiffner_plate).Shape()
                stiffner_horizontal_weld = BRepAlgoAPI_Fuse(stiffner_horizontal_weld, right_horizontal_stiffner_weld).Shape()
                stiffner_horizontal_weld = BRepAlgoAPI_Fuse(stiffner_horizontal_weld, left_horizontal_stiffner_weld).Shape()
                right_vertical_weld = BRepAlgoAPI_Fuse(right_vertical_weld, right_vertical_rear_weld).Shape()
                right_vertical_weld = BRepAlgoAPI_Fuse(right_vertical_weld, right_vertical_front_weld).Shape()
                left_vertical_weld = BRepAlgoAPI_Fuse(left_vertical_weld, left_vertical_front_weld).Shape()
                left_vertical_weld = BRepAlgoAPI_Fuse(left_vertical_weld, left_vertical_rear_weld).Shape()


        # #displaying the model
        # display.DisplayShape(ISection_model, update=True)
        # display.DisplayShape(center_plate, update=True)
        # display.DisplayShape(stiffner_plate_model,material=Graphic3d_NOM_ALUMINIUM, update=True)
        # display.DisplayShape(longitudinal_weld,color="red", update=True)
        # display.DisplayShape(right_vertical_weld,color="red", update=True)
        # display.DisplayShape(left_vertical_weld,color="red", update=True)
        # display.DisplayShape(stiffner_horizontal_weld,color="red", update=True)

        # start_display()


        #fusing only weld
        weld = BRepAlgoAPI_Fuse(longitudinal_weld, right_vertical_weld)
        weld = BRepAlgoAPI_Fuse(weld, left_vertical_weld)
        weld = BRepAlgoAPI_Fuse(weld, stiffner_horizontal_weld)

        weld_color = Quantity_Color(255/255, 0/255, 0/255, Quantity_TOC_RGB)

        ais_weld_shape = AIS_Shape(weld)
        ais_weld_shape.SetColor(weld_color)
        display.Context.Display(ais_weld_shape, True)


        #fusing only the I girder
        girder = BRepAlgoAPI_Fuse(ISection_model, center_plate)

        #stiffener plates
        ais_box = AIS_Shape(stiffner_plate_model)
        ais_box.SetMaterial(Graphic3d_NOM_ALUMINIUM)
        display.Context.Display(ais_box, True)

        plate_girder_model = BRepAlgoAPI_Fuse(weld, girder)
        plate_girder_model = BRepAlgoAPI_Fuse(plate_girder_model, stiffner_plate_model)

        return plate_girder_model
    