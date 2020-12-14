import math
from utils.common.component import Angle, Column,Beam,Channel
from abc import ABC, abstractmethod


class Section_Properties(ABC):

    @abstractmethod
    def calc_Mass(self,param1,param2,param3,param4):
        pass

    @abstractmethod
    def calc_Area(self,param1,param2,param3,param4):
        pass

    @abstractmethod
    def calc_MomentOfAreaZ(self,param1,param2,param3,param4):
        pass

    @abstractmethod
    def calc_MomentOfAreaY(self,param1,param2,param3,param4):
        pass

    @abstractmethod
    def calc_RogZ(self,param1,param2,param3,param4):
        pass

    @abstractmethod
    def calc_RogY(self,param1,param2,param3,param4):
        pass

    @abstractmethod
    def calc_ElasticModulusZz(self,param1,param2,param3,param4):
        pass

    @abstractmethod
    def calc_ElasticModulusZy(self,param1,param2,param3,param4):
        pass

    @abstractmethod
    def calc_PlasticModulusZpz(self,param1,param2,param3,param4):
        pass

    @abstractmethod
    def calc_PlasticModulusZpy(self,param1,param2,param3,param4):
        pass

    @abstractmethod
    def calc_TorsionConstantIt(self,param1,param2,param3,param4):
        pass

    @abstractmethod
    def calc_WarpingConstantIw(self,param1,param2,param3,param4):
        pass


class I_sectional_Properties(Section_Properties):

    def calc_Mass(self, D, B, t_w, t_f, alpha=90, r_1=0, r_2=0):
        self.A = ((2 * B * t_f) + ((D - 2 * t_f) * t_w)) / 100
        self.M = 7850 * self.A / 10000
        return round(self.M, 2)

    def calc_Area(self, D, B, t_w, t_f, alpha=90, r_1=0, r_2=0):
        self.A = ((2 * B * t_f) + ((D - 2 * t_f) * t_w)) / 100
        return round(self.A, 2)

    def calc_MomentOfAreaZ(self, D, B, t_w, t_f, alpha=90, r_1=0, r_2=0):
        self.I_zz = ((D - 2 * t_f) ** 3 * t_w / 12 + (B * t_f ** 3) / 6 + (B / 2 * t_f * (D - t_f) ** 2)) / 10000
        return round(self.I_zz, 2)

    def calc_MomentOfAreaY(self, D, B, t_w, t_f, alpha=90, r_1=0, r_2=0):
        self.I_yy = ((D - 2 * t_f) * t_w ** 3 / 12 + B ** 3 * t_f / 6) / 10000
        return round(self.I_yy, 2)

    def calc_RogZ(self, D, B, t_w, t_f, alpha=90, r_1=0, r_2=0):
        self.A = ((2 * B * t_f) + ((D - 2 * t_f) * t_w)) / 100
        self.I_zz = ((D - 2 * t_f) ** 3 * t_w / 12 + (B * t_f ** 3) / 6 + (B / 2 * t_f * (D - t_f) ** 2)) / 10000
        self.r_z = math.sqrt(self.I_zz / self.A)
        return round(self.r_z, 2)

    def calc_RogY(self, D, B, t_w, t_f, alpha=90, r_1=0, r_2=0):
        self.A = ((2 * B * t_f) + ((D - 2 * t_f) * t_w)) / 100
        self.I_yy = ((D - 2 * t_f) * t_w ** 3 / 12 + B ** 3 * t_f / 6) / 10000
        self.r_y = math.sqrt(self.I_yy / self.A)

        return round(self.r_y, 2)

    def calc_ElasticModulusZz(self, D, B, t_w, t_f, alpha=90, r_1=0, r_2=0):
        self.I_zz = ((D - 2 * t_f) ** 3 * t_w / 12 + (B * t_f ** 3) / 6 + (B / 2 * t_f * (D - t_f) ** 2)) / 10000
        self.Z_ez = (self.I_zz * 2 * 10) / (D)
        return round(self.Z_ez, 2)

    def calc_ElasticModulusZy(self, D, B, t_w, t_f, alpha=90, r_1=0, r_2=0):
        self.I_yy = ((D - 2 * t_f) * t_w ** 3 / 12 + B ** 3 * t_f / 6) / 10000
        self.Z_ey = (self.I_yy * 2 * 10) / (B)
        return round(self.Z_ey, 2)

    def calc_PlasticModulusZpz(self, D, B, t_w, t_f, alpha=90, r_1=0, r_2=0):
        self.A = ((2 * B * t_f) + ((D - 2 * t_f) * t_w)) / 100
        self.y_p = (((D - 2 * t_f) ** 2 * t_w / 8 + B * t_f * (D - t_f) / 2) / ((D - t_f) / 2 * t_w + B * t_f)) / 10
        self.Z_pz = (2 * (self.A / 2 * self.y_p))
        return round(self.Z_pz, 2)

    def calc_PlasticModulusZpy(self, D, B, t_w, t_f, alpha=90, r_1=0, r_2=0):
        self.A = ((2 * B * t_f) + ((D - 2 * t_f) * t_w)) / 100
        self.z_p = ((((D - 2 * t_f) * t_w ** 2) / 8 + (B * t_f * B) / 4) / ((D - 2 * t_f) * t_w / 2 + (B * t_f)))
        self.Z_py = 2 * (self.A / 2 * self.z_p)
        return round(self.Z_py, 2)

    # TODO:add formula
    def calc_TorsionConstantIt(self, D, B, t_w, t_f, alpha=90, r_1=0, r_2=0):
        self.It = 2 * ((B * t_f ** 3) / 3) + ((D - (2 * t_f)) * t_w ** 3) / 3
        return round(self.It / 10000, 2)

    def calc_WarpingConstantIw(self, D, B, t_w, t_f, alpha=90, r_1=0, r_2=0):
        return 0.0


class Single_Angle_Properties(Section_Properties):
    "return in cm "

    def calc_Mass(self, a, b, t, l):
        self.A = t * (a + b - t)
        self.M = 7850 * self.A / 1000000
        return round(self.M, 2)

    def calc_Area(self, a, b, t, l):
        self.A = t * (a + b - t)
        return round(self.A / 100, 2)

    def calc_Cz(self, a, b, t, l):
        self.A = t * (a + b - t)
        self.Cz = ((0.5 * (b * a ** 2)) - (0.5 * (b - t) * (a ** 2 - t ** 2))) / self.A
        return round(self.Cz / 10, 2)

    def calc_Cy(self, a, b, t, l):
        self.A = t * (a + b - t)
        self.Cy = ((0.5 * (b ** 2) * a) - (0.5 * (b ** 2 - t ** 2) * (a - t))) / self.A
        return round(self.Cy / 10, 2)

    def calc_MomentOfAreaZ(self, a, b, t, l):
        Cza = self.calc_Cz(a, b, t, l) * 10
        self.I_zz = (a ** 3 * b) / 12 - ((b - t) * (a - t) ** 3) / 12 + (a * b * (a / 2 - Cza) ** 2) - (
                (a - t) * (b - t) * ((a + t) / 2 - Cza) ** 2)
        return round(self.I_zz / 10000, 2)

    def calc_MomentOfAreaY(self, a, b, t, l):
        Cya = self.calc_Cy(a, b, t, l) * 10
        self.I_yy = (b ** 3 * a) / 12 - ((a - t) * (b - t) ** 3) / 12 + (a * b * (b / 2 - Cya) ** 2) - (
                (a - t) * (b - t) * ((b + t) / 2 - Cya) ** 2)
        return round(self.I_yy / 10000, 2)

    def calc_MomentOfAreaYZ(self, a, b, t, l):
        Cya = self.calc_Cy(a, b, t, l) * 10
        Cza = self.calc_Cz(a, b, t, l) * 10
        self.I_yz = a * b * (a / 2 - Cza) * (b / 2 - Cya) - (
                (a - t) * (b - t) * (0.5 * (a + t) - Cza) * (0.5 * (b + t) - Cya))
        # self.I_yz = 1.000
        print(self.I_yz)
        return round(self.I_yz / 10000, 2)

    def calc_MomentOfAreaU(self, a, b, t, l):
        I_zza = self.calc_MomentOfAreaZ(a, b, t, l)
        I_yya = self.calc_MomentOfAreaY(a, b, t, l)
        I_yza = self.calc_MomentOfAreaYZ(a, b, t, l)
        self.I_u = 0.5 * (I_zza + I_yya) + math.sqrt(0.25 * (I_zza - I_yya) ** 2 + I_yza ** 2)
        return round(self.I_u, 2)

    def calc_MomentOfAreaV(self, a, b, t, l):
        I_zza = self.calc_MomentOfAreaZ(a, b, t, l)
        I_yya = self.calc_MomentOfAreaY(a, b, t, l)
        I_yza = self.calc_MomentOfAreaYZ(a, b, t, l)
        self.I_v = 0.5 * (I_zza + I_yya) - math.sqrt(0.25 * (I_zza - I_yya) ** 2 + I_yza ** 2)
        return round(self.I_v, 2)

    def calc_RogZ(self, a, b, t, l):
        I_zza = self.calc_MomentOfAreaZ(a, b, t, l)
        Aa = self.calc_Area(a, b, t, l)
        self.r_z = math.sqrt(I_zza / Aa)

        return round(self.r_z, 2)

    def calc_RogY(self, a, b, t, l):
        I_yya = self.calc_MomentOfAreaY(a, b, t, l)
        Aa = self.calc_Area(a, b, t, l)
        self.r_y = math.sqrt(I_yya / Aa)

        return round(self.r_y, 2)

    def calc_RogU(self, a, b, t, l):
        I_ua = self.calc_MomentOfAreaU(a, b, t, l)
        Aa = self.calc_Area(a, b, t, l)
        self.r_u = math.sqrt(I_ua / Aa)

        return round(self.r_u, 2)

    def calc_RogV(self, a, b, t, l):
        I_va = self.calc_MomentOfAreaV(a, b, t, l)
        Aa = self.calc_Area(a, b, t, l)
        self.r_v = math.sqrt(I_va / Aa)

        return round(self.r_v, 2)

    def calc_ElasticModulusZz(self, a, b, t, l):
        I_zza = self.calc_MomentOfAreaZ(a, b, t, l)
        Cza = self.calc_Cz(a, b, t, l)
        self.Z_zz = I_zza / (a / 10 - Cza)
        return round(self.Z_zz, 2)

    def calc_ElasticModulusZy(self, a, b, t, l):
        I_yya = self.calc_MomentOfAreaY(a, b, t, l)
        Cya = self.calc_Cy(a, b, t, l)
        self.Z_yy = I_yya / (b / 10 - Cya)
        return round(self.Z_yy, 2)

    def calc_PlasticModulusZpz(self, a, b, t, l):
        # Aa = self.calc_Area(a, b, t,l)*100
        # self.Z_pz = t * (b-t) * (a- (0.5* Aa/t)-0.5*t) + 0.5* t*(a**2 + (Aa/t)**2 - a*(Aa/t))
        # # self.Z_pz = t * (b-t) * (a- 0.5* Aa/t-0.5*t)
        #
        # # self.Z_pz = 1.000
        # return round(self.Z_pz/1000, 2)
        A_leg_a = (a - t) * t
        A_leg_b = b * t
        if A_leg_a > A_leg_b:
            x = a - (A_leg_a + A_leg_b) / (2 * t)
            A_1 = (a - x) * t
            A_2 = (x - t) * t
            A_3 = b * t
            y_1 = (a - x) / 2
            y_2 = (x - t) / 2
            y_3 = (x - t) + (t / 2)
            print("Leg A area is more than Leg B area")
        else:
            x = (A_leg_a + A_leg_b) / (2 * t)
            A_1 = (a - t) * t
            A_2 = (t - x) * t
            A_3 = x * t
            y_1 = (t - x) + (a - t) / 2
            y_2 = (t - x) / 2
            y_3 = x / 2
            print("Leg B area is more than Leg A area")

        Z_pz = A_1 * y_1 + A_2 * y_2 + A_3 * y_3
        return round(Z_pz / 1000, 2)

    def calc_PlasticModulusZpy(self, a, b, t, l):
        A_leg_a = a * t
        A_leg_b = (b - t) * t
        if A_leg_a > A_leg_b:
            x = (A_leg_a + A_leg_b) / (2 * a)
            A_1 = a * t
            A_2 = (t - x) * a
            A_3 = (b - t) * t
            y_1 = x / 2
            y_2 = (t - x) / 2
            y_3 = (t - x) + (b - t) / 2
            print("Leg A area is more than Leg B area")
        else:
            x = b - (A_leg_a + A_leg_b) / (2 * t)
            A_1 = a * t
            A_2 = (x - t) * t
            A_3 = (b - x) * t
            y_1 = (x - t) + (t / 2)
            y_2 = (x - t) / 2
            y_3 = (b - x) / 2
            print("Leg B area is more than Leg A area")

        Z_py = A_1 * y_1 + A_2 * y_2 + A_3 * y_3
        return round(Z_py / 1000, 2)

    def calc_TorsionConstantIt(self, a, b, t, l):
        self.I_t = ((b * (t ** 3)) / 3) + ((a - t) * (t ** 3) / 3)
        return round(self.I_t / 10000, 2)

    def calc_WarpingConstantIw(self,param1,param2,param3,param4):
        pass


class BBAngle_Properties(Section_Properties):
    "return in cm "

    def __init__(self):
        self.db = False

    def data(self, designation, material_grade=""):
        self.Angle_attributes = Angle(designation, material_grade)
        self.db = True

    def calc_Mass(self, a=0.0, b=0.0, t=0.0, l='Long Leg'):
        self.A = self.calc_Area(a, b, t, l)
        self.M = 7850 * self.A / 10000
        return round(self.M, 2)

    def calc_Area(self, a=0.0, b=0.0, t=0.0, l='Long Leg'):
        if self.db == False:
            self.A = 2 * t * (a + b - t)
        else:
            self.A = 2 * self.Angle_attributes.area
        return round(self.A / 100, 2)

    def calc_Cz(self, a=0.0, b=0.0, t=0.0, l='Long Leg'):
        if self.db == False:
            if l == "Long Leg":
                self.A = t * (a + b - t)
                self.Cz = ((0.5 * (b * a ** 2)) - (0.5 * (b - t) * (a ** 2 - t ** 2))) / self.A
            else:
                self.A = t * (a + b - t)
                self.Cz = ((0.5 * (b ** 2) * a) - (0.5 * (b ** 2 - t ** 2) * (a - t))) / self.A
        else:
            if l == "Long Leg":
                self.Cz = self.Angle_attributes.Cz
            else:
                self.Cz = self.Angle_attributes.Cy
        return round(self.Cz / 10, 2)

    def calc_Cy(self, a=0.0, b=0.0, t=0.0, l='Long Leg'):
        if self.db == False:
            if l == "Long Leg":
                self.A = t * (a + b - t)
                self.Cy = ((0.5 * (b ** 2) * a) - (0.5 * (b ** 2 - t ** 2) * (a - t))) / self.A
            else:
                self.A = t * (a + b - t)
                self.Cy = ((0.5 * (b * a ** 2)) - (0.5 * (b - t) * (a ** 2 - t ** 2))) / self.A
        else:
            if l == "Long Leg":
                self.Cy = self.Angle_attributes.Cy
            else:
                self.Cy = self.Angle_attributes.Cz
        return round(self.Cy / 10, 2)

    def calc_MomentOfAreaZ(self, a=0.0, b=0.0, t=0.0, l='Long Leg', thickness=0.0):
        if self.db == False:
            if l == "Long Leg":
                self.I_zz = 2 * Single_Angle_Properties().calc_MomentOfAreaZ(a, b, t, l) * 10000
            else:
                self.I_zz = 2 * Single_Angle_Properties().calc_MomentOfAreaY(a, b, t, l) * 10000

        else:
            if l == "Long Leg":
                self.I_zz = 2 * self.Angle_attributes.mom_inertia_z
            else:
                self.I_zz = 2 * self.Angle_attributes.mom_inertia_y

        return round(self.I_zz / 10000, 2)

    def calc_MomentOfAreaY(self, a=0.0, b=0.0, t=0.0, l='Long Leg', thickness=0.0):
        if self.db == False:
            if l == "Long Leg":
                mom_inertia_y = Single_Angle_Properties().calc_MomentOfAreaY(a, b, t, l) * 10000
                area = Single_Angle_Properties().calc_Area(a, b, t, l) * 100
                Cg_1 = Single_Angle_Properties().calc_Cy(a, b, t, l) * 10
                self.I_yy = (mom_inertia_y + (area * (Cg_1 + thickness/2) * (Cg_1 + thickness/2))) * 2
            else:
                mom_inertia_y = Single_Angle_Properties().calc_MomentOfAreaZ(a, b, t, l) * 10000
                area = Single_Angle_Properties().calc_Area(a, b, t, l) * 100
                Cg_1 = Single_Angle_Properties().calc_Cz(a, b, t, l) * 10
                self.I_yy = (mom_inertia_y + (area * (Cg_1 + thickness / 2) * (Cg_1 + thickness / 2))) * 2

        else:
            if l == "Long Leg":
                mom_inertia_y = self.Angle_attributes.mom_inertia_y
                area = self.Angle_attributes.area
                Cg_1 = self.Angle_attributes.Cy
                self.I_yy = (mom_inertia_y + (area * (Cg_1 + thickness / 2) * (Cg_1 + thickness / 2))) * 2
            else:
                mom_inertia_y = self.Angle_attributes.mom_inertia_z
                area = self.Angle_attributes.area
                Cg_1 = self.Angle_attributes.Cz
                self.I_yy = (mom_inertia_y + (area * (Cg_1 + thickness / 2) * (Cg_1 + thickness / 2))) * 2

        return round(self.I_yy / 10000, 2)

    def calc_RogZ(self, a=0.0, b=0.0, t=0.0, l='Long Leg', thickness=0.0):

        mom_inertia_z = self.calc_MomentOfAreaZ(a, b, t, l, thickness)
        area = self.calc_Area(a, b, t, l)
        self.r_z = math.sqrt(mom_inertia_z / area)

        return round(self.r_z, 2)

    def calc_RogY(self, a=0.0, b=0.0, t=0.0, l='Long Leg', thickness=0.0):
        mom_inertia_y = self.calc_MomentOfAreaY(a, b, t, l, thickness)
        area = self.calc_Area(a, b, t, l)
        self.r_y = math.sqrt(mom_inertia_y / area)

        return round(self.r_y, 2)

    def calc_ElasticModulusZz(self, a=0.0, b=0.0, t=0.0, l='Long Leg', thickness=0.0):
        mom_inertia_z = self.calc_MomentOfAreaZ(a, b, t, l, thickness)
        Cz = self.calc_Cz(a, b, t, l)*10
        if self.db == False:
            if l == "Long Leg":
                self.Z_zz = mom_inertia_z / ((a - Cz) / 10)
            else:
                self.Z_zz = mom_inertia_z / ((b - Cz) / 10)
        else:
            a = self.Angle_attributes.a
            b = self.Angle_attributes.b
            if l == "Long Leg":
                self.Z_zz = mom_inertia_z / ((a - Cz) / 10)
            else:
                self.Z_zz = mom_inertia_z / ((b - Cz) / 10)
        return round(self.Z_zz, 2)

    def calc_ElasticModulusZy(self, a=0.0, b=0.0, t=0.0, l='Long Leg', thickness=0.0):
        mom_inertia_y = self.calc_MomentOfAreaY(a, b, t, l, thickness)
        if self.db == False:
            if l == "Long Leg":
                self.Z_yy = mom_inertia_y / ((b + thickness / 2) / 10)
            else:
                self.Z_yy = mom_inertia_y / ((a + thickness / 2) / 10)
        else:
            a = self.Angle_attributes.a
            b= self.Angle_attributes.b
            if l == "Long Leg":
                self.Z_yy = mom_inertia_y / ((b + thickness / 2) / 10)
            else:
                self.Z_yy = mom_inertia_y / ((a + thickness / 2) / 10)

        return round(self.Z_yy, 2)

    def calc_PlasticModulusZpz(self, a=0.0, b=0.0, t=0.0, l='Long Leg', thickness=0):
        if self.db == False:
            if l == "Long Leg":
                self.Z_pz = 2 * Single_Angle_Properties().calc_PlasticModulusZpz(a, b, t, l)
            else:
                self.Z_pz = 2 * Single_Angle_Properties().calc_PlasticModulusZpy(a, b, t, l)
        else:
            if l == "Long Leg":
                self.Z_pz = 2 * self.Angle_attributes.plast_sec_mod_z / 1000
            else:
                self.Z_pz = 2 * self.Angle_attributes.plast_sec_mod_y / 1000
        return round(self.Z_pz, 2)

    def calc_PlasticModulusZpy(self, a=0.0, b=0.0, t=0.0, l='Long Leg', thickness=0):
        A = self.calc_Area(a, b, t, l)
        if l == "Long Leg":
            Cy =  Single_Angle_Properties().calc_Cy(a, b, t, l)
            self.Z_py = A * (Cy + Cy + thickness/10) / 2
        else:
            Cz =  Single_Angle_Properties().calc_Cz(a, b, t, l)
            self.Z_py = A * (Cz + Cz + thickness/10) / 2

        return round(self.Z_py, 2)

    def calc_TorsionConstantIt(self, a=0.0, b=0.0, t=0.0, l='Long Leg'):
        if self.db == False:
            self.I_t = 2 * (((b * (t ** 3)) / 3) + ((a - t) * (t ** 3) / 3))
        else:
            self.I_t = self.Angle_attributes.It * 2

        return round(self.I_t / 10000, 2)

    def calc_WarpingConstantIw(self,param1,param2,param3,param4):
        pass



class SAngle_Properties(Section_Properties):
    def __init__(self):
        self.db = False

    def data(self, designation, material_grade):
        self.Angle_attributes = Angle(designation, material_grade)
        self.db = True

    def calc_Mass(self, a, b, t, l):
        self.A = self.calc_Area(a, b, t, l)
        self.M = 7850 * self.A / 10000
        return round(self.M, 2)

    def calc_Area(self, a, b, t, l):
        if self.db == False:
            self.A = 2 * t * (a + b - t)
        else:
            self.A = 2 * self.Angle_attributes.area
        return round(self.A / 100, 2)

    def calc_Cz(self, a=0.0, b=0.0, t=0.0, l='Long Leg'):
        if self.db == False:
            if l == "Long Leg":
                self.A = t * (a + b - t)
                self.Cz = ((0.5 * (b * a ** 2)) - (0.5 * (b - t) * (a ** 2 - t ** 2))) / self.A
            else:
                self.A = t * (a + b - t)
                self.Cz = ((0.5 * (b ** 2) * a) - (0.5 * (b ** 2 - t ** 2) * (a - t))) / self.A
        else:
            if l == "Long Leg":
                self.Cz = self.Angle_attributes.Cz
            else:
                self.Cz = self.Angle_attributes.Cy
        return round(self.Cz / 10, 2)

    def calc_Cy(self, a=0.0, b=0.0, t=0.0, l='Long Leg'):
        if self.db == False:
            if l == "Long Leg":
                self.A = t * (a + b - t)
                self.Cy = ((0.5 * (b ** 2) * a) - (0.5 * (b ** 2 - t ** 2) * (a - t))) / self.A
            else:
                self.A = t * (a + b - t)
                self.Cy = ((0.5 * (b * a ** 2)) - (0.5 * (b - t) * (a ** 2 - t ** 2))) / self.A
        else:
            if l == "Long Leg":
                self.Cy = self.Angle_attributes.Cy
            else:
                self.Cy = self.Angle_attributes.Cz
        return round(self.Cy / 10, 2)

    def calc_MomentOfAreaZ(self, a, b, t, l, thickness=0.0):
        if self.db == False:
            if l == "Long Leg":
                mom_inertia_z = Single_Angle_Properties().calc_MomentOfAreaZ(a, b, t, l) * 10000
                area = Single_Angle_Properties().calc_Area(a, b, t, l) * 100
                Cg_1 = Single_Angle_Properties().calc_Cz(a, b, t, l) * 10
                self.I_zz = (mom_inertia_z + (area * (Cg_1) * (Cg_1))) * 2
            else:
                mom_inertia_y = Single_Angle_Properties().calc_MomentOfAreaY(a, b, t, l) * 10000
                area = Single_Angle_Properties().calc_Area(a, b, t, l) * 100
                Cg_1 = Single_Angle_Properties().calc_Cy(a, b, t, l) * 10
                self.I_zz = (mom_inertia_y + (area * (Cg_1) * (Cg_1))) * 2
        else:
            if l == "Long Leg":
                mom_inertia_z = self.Angle_attributes.mom_inertia_z
                area = self.Angle_attributes.area
                Cg_1 = self.Angle_attributes.Cz
                self.I_zz = (mom_inertia_z + (area * (Cg_1) * (Cg_1))) * 2
            else:
                mom_inertia_y = self.Angle_attributes.mom_inertia_y
                area = self.Angle_attributes.area
                Cg_1 = self.Angle_attributes.Cy
                self.I_zz = (mom_inertia_y + (area * (Cg_1) * (Cg_1))) * 2

        return round(self.I_zz / 10000, 2)

    def calc_MomentOfAreaY(self, a, b, t, l, thickness=0.0):
        if self.db == False:
            if l == "Long Leg":
                mom_inertia_y = Single_Angle_Properties().calc_MomentOfAreaY(a, b, t, l) * 10000
                area = Single_Angle_Properties().calc_Area(a, b, t, l) * 100
                Cg_1 = Single_Angle_Properties().calc_Cy(a, b, t, l) * 10
                self.I_yy = (mom_inertia_y + (area * (Cg_1 + thickness / 2) * (Cg_1 + thickness / 2))) * 2
            else:
                mom_inertia_z = Single_Angle_Properties().calc_MomentOfAreaZ(a, b, t, l) * 10000
                area = Single_Angle_Properties().calc_Area(a, b, t, l) * 100
                Cg_1 = Single_Angle_Properties().calc_Cz(a, b, t, l) * 10
                self.I_yy = (mom_inertia_z + (area * (Cg_1 + thickness / 2) * (Cg_1 + thickness / 2))) * 2
        else:
            if l == "Long Leg":
                mom_inertia_y = self.Angle_attributes.mom_inertia_y
                area = self.Angle_attributes.area
                Cg_1 = self.Angle_attributes.Cy
                self.I_yy = (mom_inertia_y + (area * (Cg_1 + thickness / 2) * (Cg_1 + thickness / 2))) * 2
            else:
                mom_inertia_z = self.Angle_attributes.mom_inertia_z
                area = self.Angle_attributes.area
                Cg_1 = self.Angle_attributes.Cz
                self.I_yy = (mom_inertia_z + (area * (Cg_1 + thickness / 2) * (Cg_1 + thickness / 2))) * 2

        return round(self.I_yy / 10000, 2)

    # def calc_MomentOfAreaYZ(self, a, b, t, l):
    #     Cza = self.calc_Cz(a, b, t, l) * 10
    #     Cya = self.calc_Cy(a, b, t, l) * 10
    #     self.I_yz = a * b * (a / 2 - Cya) * (b / 2 - Cza) - (
    #             (a - t) * (b - t) * (0.5 * (a + t) - Cya) * (0.5 * (b + t) - Cza))
    #     # self.I_yz = 1.000
    #     return round(self.I_yz / 10000, 2)
    def calc_MomentofAreaYZ(self, a, b, t, l, T = 0.0):
        if l == "Long Leg":
            x1 = ((b / 2) + (T / 2))
            y1 = a / 2
            A1 = a * b
            x2 = ((b + t) / 2) + T / 2
            y2 = (a + t) / 2
            A2 = (a - t) * (b - t)
            Iyz1 = x1 * y1 * A1
            Iyz2 = x2 * y2 * A2
        else:
            x1 = ((a / 2) + (T / 2))
            y1 = b / 2
            A1 = a * b
            x2 = ((a + t) / 2) + T / 2
            y2 = (b + t) / 2
            A2 = (b - t) * (a - t)
            Iyz1 = x1 * y1 * A1
            Iyz2 = x2 * y2 * A2

        I_yz = 2 * (Iyz1 - Iyz2)
        return round(I_yz/10000, 2)


    # def calc_MomentOfAreaV(self, a, b, t, l, thickness=0.0):
    #     "min MI will always have subscript v"
    #     if self.db == False:
    #         if a == b:
    #             self.I_vv = 2 * Single_Angle_Properties().calc_MomentOfAreaU(a, b, t, l) * 10000
    #
    #         else:
    #             if l == 'Long Leg':
    #                 mom_inertia_u = Single_Angle_Properties().calc_MomentOfAreaU(a, b, t, l) * 10000
    #                 area = Single_Angle_Properties().calc_Area(a, b, t, l) * 100
    #                 Cg1 = Single_Angle_Properties().calc_Cy(a, b, t, l) * 10
    #                 Cg2 = Single_Angle_Properties().calc_Cz(a, b, t, l) * 10
    #                 diag_cg = math.sqrt(Cg1 ** 2 + Cg2 ** 2)
    #                 value = Cg2 / diag_cg
    #                 angle1 = math.asin(value)
    #                 angle2 = math.pi - (2 * angle1)
    #                 Cg = diag_cg * math.cos(angle2)
    #                 angle3 = math.pi - (math.pi / 2 + angle2)
    #                 angle4 = angle1 - angle3
    #                 thk = thickness / 2 * math.sin(angle4)
    #                 self.I_vv = (mom_inertia_u + (area * (Cg + thk) * (Cg + thk))) * 2
    #             else:
    #                 mom_inertia_u = Single_Angle_Properties().calc_MomentOfAreaU(a, b, t, l) * 10000
    #                 area = Single_Angle_Properties().calc_Area(a, b, t, l) * 100
    #                 Cg1 = Single_Angle_Properties().calc_Cy(a, b, t, l) * 10
    #                 Cg2 = Single_Angle_Properties().calc_Cz(a, b, t, l) * 10
    #                 diag_cg = math.sqrt(Cg1 ** 2 + Cg2 ** 2)
    #                 value = Cg2 / diag_cg
    #                 angle1 = math.asin(value)
    #                 angle2 = math.pi - (2 * angle1)
    #                 Cg = diag_cg * math.cos(angle2)
    #                 angle3 = math.pi - (math.pi / 2 + angle2)
    #                 angle4 = angle3 + angle2/2
    #                 thk = thickness / 2 * math.sin(angle4)
    #                 self.I_vv = (mom_inertia_u + (area * (Cg + thk) * (Cg + thk))) * 2
    #
    #     else:
    #         if a == b:
    #             self.I_vv = 2 * self.Angle_attributes.mom_inertia_u
    #         else:
    #             if l == 'Long Leg':
    #                 mom_inertia_u = self.Angle_attributes.mom_inertia_u
    #                 area = self.Angle_attributes.area
    #                 Cg1 = self.Angle_attributes.Cy
    #                 Cg2 = self.Angle_attributes.Cz
    #                 diag_cg = math.sqrt(Cg1 ** 2 + Cg2 ** 2)
    #                 value = Cg2 / diag_cg
    #                 angle1 = math.asin(value)
    #                 angle2 = math.pi - (2 * angle1)
    #                 Cg = diag_cg * math.cos(angle2)
    #                 angle3 = math.pi - (math.pi / 2 + angle2)
    #                 angle4 = angle1 - angle3
    #                 thk = thickness / 2 * math.sin(angle4)
    #                 self.I_vv = (mom_inertia_u + (area * (Cg + thk) * (Cg + thk))) * 2
    #             else:
    #                 mom_inertia_u = self.Angle_attributes.mom_inertia_u
    #                 area = self.Angle_attributes.area
    #                 Cg1 = self.Angle_attributes.Cy
    #                 Cg2 = self.Angle_attributes.Cz
    #                 diag_cg = math.sqrt(Cg1 ** 2 + Cg2 ** 2)
    #                 value = Cg2 / diag_cg
    #                 angle1 = math.asin(value)
    #                 angle2 = math.pi - (2 * angle1)
    #                 Cg = diag_cg * math.cos(angle2)
    #                 angle3 = math.pi - (math.pi / 2 + angle2)
    #                 angle4 = angle3 + angle2/2
    #                 thk = thickness / 2 * math.sin(angle4)
    #                 self.I_vv = (mom_inertia_u + (area * (Cg + thk) * (Cg + thk))) * 2
    #
    #     return round(self.I_vv / 10000, 2)

    def calc_MomentOfAreaV(self, a, b, t, l, thickness=0.0):
        "min MI will always have subscript v"

        Izz = self.calc_MomentOfAreaZ(a,b,t,l,thickness)
        Iyy = self.calc_MomentOfAreaY(a,b,t,l,thickness)
        Iyz = self.calc_MomentofAreaYZ(a,b,t,l,thickness)
        self.I_vv = ((Izz + Iyy) / 2) - (((Izz - Iyy) / 2) ** 2 + Iyz ** 2) ** (1 / 2)

        return round(self.I_vv,2)

    def calc_MomentOfAreaU(self, a, b, t, l, thickness=0.0):
        "min MI will always have subscript v"

        Izz = self.calc_MomentOfAreaZ(a, b, t, l, thickness)
        Iyy = self.calc_MomentOfAreaY(a, b, t, l, thickness)
        Iyz = self.calc_MomentofAreaYZ(a, b, t, l, thickness)
        self.I_uu = ((Izz + Iyy) / 2 ) +  (((Izz - Iyy)/2)**2 + Iyz**2)**(1/2)

        return round(self.I_uu,2)


    # def calc_MomentOfAreaU(self, a, b, t, l, thickness=0.0):
    #     if self.db == False:
    #         if a == b:
    #             mom_inertia_v = Single_Angle_Properties().calc_MomentOfAreaV(a, b, t, l) * 10000
    #             area = Single_Angle_Properties().calc_Area(a, b, t, l) * 100
    #             Cg_1 = Single_Angle_Properties().calc_Cy(a, b, t, l) * 10
    #             a = math.sqrt(2)
    #             self.I_uu = (mom_inertia_v + (
    #                         area * (a * Cg_1 + a * thickness / 2) * (a * Cg_1 + a * thickness / 2))) * 2
    #         else:
    #             if l == "Long Leg":
    #                 mom_inertia_v = Single_Angle_Properties().calc_MomentOfAreaV(a, b, t, l) * 10000
    #                 area = Single_Angle_Properties().calc_Area(a, b, t, l) * 100
    #                 Cg1 = Single_Angle_Properties().calc_Cy(a, b, t, l) * 10
    #                 Cg2 = Single_Angle_Properties().calc_Cz(a, b, t, l) * 10
    #                 diag_cg = math.sqrt(Cg1 ** 2 + Cg2 ** 2)
    #                 value = Cg2 / diag_cg
    #                 angle1 = math.asin(value)
    #                 angle2 = math.pi - (2 * angle1)
    #                 Cg = diag_cg * math.sin(angle2)
    #                 angle3 = math.pi - (math.pi / 2 + angle2)
    #                 angle4 = angle1 - angle3
    #                 thk = thickness / 2 * math.cos(angle4)
    #                 self.I_uu= (mom_inertia_v + (area * (Cg + thk) * (Cg + thk))) * 2
    #             else:
    #                 mom_inertia_v = Single_Angle_Properties().calc_MomentOfAreaV(a, b, t, l) * 10000
    #                 area = Single_Angle_Properties().calc_Area(a, b, t, l) * 100
    #                 Cg1 = Single_Angle_Properties().calc_Cy(a, b, t, l) * 10
    #                 Cg2 = Single_Angle_Properties().calc_Cz(a, b, t, l) * 10
    #                 diag_cg = math.sqrt(Cg1 ** 2 + Cg2 ** 2)
    #                 value = Cg2 / diag_cg
    #                 angle1 = math.asin(value)
    #                 angle2 = math.pi - (2 * angle1)
    #                 Cg = diag_cg * math.sin(angle2)
    #                 angle3 = math.pi - (math.pi / 2 + angle2)
    #                 angle4 = angle3 + angle2 / 2
    #                 thk = thickness / 2 * math.cos(angle4)
    #                 self.I_uu = (mom_inertia_v + (area * (Cg + thk) * (Cg + thk))) * 2
    #
    #     else:
    #         if a == b:
    #             mom_inertia_v = self.Angle_attributes.mom_inertia_v
    #             area = self.Angle_attributes.area
    #             Cg_1 = self.Angle_attributes.Cy
    #             a = math.sqrt(2)
    #             self.I_uu = (mom_inertia_v + (
    #                         area * (a * Cg_1 + a * thickness / 2) * (a * Cg_1 + a * thickness / 2))) * 2
    #
    #
    #         else:
    #             if l == "Long Leg":
    #                 mom_inertia_v = self.Angle_attributes.mom_inertia_v
    #                 area = self.Angle_attributes.area
    #                 Cg1 = self.Angle_attributes.Cy
    #                 Cg2 = self.Angle_attributes.Cz
    #                 diag_cg = math.sqrt(Cg1 ** 2 + Cg2 ** 2)
    #                 value = Cg2 / diag_cg
    #                 angle1 = math.asin(value)
    #                 angle2 = math.pi - (2 * angle1)
    #                 Cg = diag_cg * math.sin(angle2)
    #                 angle3 = math.pi - (math.pi / 2 + angle2)
    #                 angle4 = angle1 - angle3
    #                 thk = thickness / 2 * math.cos(angle4)
    #                 self.I_uu = (mom_inertia_v + (area * (Cg + thk) * (Cg + thk))) * 2
    #             else:
    #                 mom_inertia_v = self.Angle_attributes.mom_inertia_v
    #                 area = self.Angle_attributes.area
    #                 Cg1 = self.Angle_attributes.Cy
    #                 Cg2 = self.Angle_attributes.Cz
    #                 diag_cg = math.sqrt(Cg1 ** 2 + Cg2 ** 2)
    #                 value = Cg2 / diag_cg
    #                 angle1 = math.asin(value)
    #                 angle2 = math.pi - (2 * angle1)
    #                 Cg = diag_cg * math.sin(angle2)
    #                 angle3 = math.pi - (math.pi / 2 + angle2)
    #                 angle4 = angle3 + angle2 / 2
    #                 thk = thickness / 2 * math.cos(angle4)
    #                 self.I_uu = (mom_inertia_v + (area * (Cg + thk) * (Cg + thk))) * 2
    #
    #
    #     return round(self.I_uu / 10000, 2)

    def calc_RogZ(self, a, b, t, l, thickness=0.0):
        mom_inertia_z = self.calc_MomentOfAreaZ(a, b, t, l, thickness)
        area = self.calc_Area(a, b, t, l)
        self.r_z = math.sqrt(mom_inertia_z / area)

        return round(self.r_z, 2)

    def calc_RogY(self, a, b, t, l, thickness=0.0):
        mom_inertia_y = self.calc_MomentOfAreaY(a, b, t, l, thickness)
        area = self.calc_Area(a, b, t, l)
        self.r_y = math.sqrt(mom_inertia_y / area)

        return round(self.r_y, 2)

    def calc_RogV(self, a, b, t, l, thickness=0.0):
        mom_inertia_v = self.calc_MomentOfAreaV(a, b, t, l, thickness)
        area = self.calc_Area(a, b, t, l)
        self.r_v = math.sqrt(mom_inertia_v / area)

        return round(self.r_v, 2)

    def calc_RogU(self, a, b, t, l, thickness=0.0):
        mom_inertia_u = self.calc_MomentOfAreaU(a, b, t, l, thickness)
        area = self.calc_Area(a, b, t, l)
        self.r_u = math.sqrt(mom_inertia_u / area)

        return round(self.r_u, 2)

    def calc_ElasticModulusZz(self, a, b, t, l, thickness=0):
        mom_inertia_z = self.calc_MomentOfAreaZ(a, b, t, l, thickness)
        if l == "Long Leg":
            self.Z_zz = mom_inertia_z / (a / 10)
        else:
            self.Z_zz = mom_inertia_z / (b / 10)
        return round(self.Z_zz, 2)

    def calc_ElasticModulusZy(self, a, b, t, l, thickness=0):
        mom_inertia_y = self.calc_MomentOfAreaY(a, b, t, l, thickness)
        if l == "Long Leg":
            self.Z_yy = mom_inertia_y / ((b + thickness / 2) / 10)
        else:
            self.Z_yy = mom_inertia_y / ((a + thickness / 2) / 10)
        return round(self.Z_yy, 2)

    def calc_PlasticModulusZpz(self, a, b, t, l, thickness=0):
        if self.db == False:
            A = self.calc_Area(a, b, t, l) * 100
            if l == "Long Leg":
                Cz = Single_Angle_Properties().calc_Cz(a, b, t, l) * 10
                self.Z_pz = A * (Cz + Cz) / 2
            else:
                Cy = Single_Angle_Properties().calc_Cy(a, b, t, l) * 10
                self.Z_pz = A * (Cy + Cy) / 2
        else:
            A = self.Angle_attributes.area * 2
            if l == "Long Leg":
                Cz = self.Angle_attributes.Cz
                self.Z_pz = A * (Cz + Cz) / 2
            else:
                Cy = self.Angle_attributes.Cy
                self.Z_pz = A * (Cy + Cy) / 2

        return round(self.Z_pz / 1000, 2)

    def calc_PlasticModulusZpy(self, a, b, t, l, thickness=0):
        if self.db == False:
            A = self.calc_Area(a, b, t, l) * 100
            if l == "Long Leg":
                Cy = Single_Angle_Properties().calc_Cy(a, b, t, l) * 10
                self.Z_py = A * (Cy + Cy + thickness) / 2
            else:
                Cz = Single_Angle_Properties().calc_Cz(a, b, t, l) * 10
                self.Z_py = A * (Cz + Cz + thickness) / 2
        else:
            A = self.Angle_attributes.area * 2
            if l == "Long Leg":
                Cy = self.Angle_attributes.Cy
                self.Z_py = A * (Cy + Cy + thickness) / 2
            else:
                Cz = self.Angle_attributes.Cz
                self.Z_py = A * (Cz + Cz + thickness) / 2
        return round(self.Z_py / 1000, 2)

    def calc_TorsionConstantIt(self, a, b, t, l, thickness=0):
        if self.db == False:
            self.I_t = 2 * (((b * (t ** 3)) / 3) + ((a - t) * (t ** 3) / 3))
        else:
            self.I_t = self.Angle_attributes.It * 2
        return round(self.I_t / 10000, 2)

    def calc_WarpingConstantIw(self,param1,param2,param3,param4):
        pass


class Single_Channel_Properties(Section_Properties):

    def calc_Mass(self, f_w, f_t, w_h, w_t):
        print(f_w, f_t, w_h, w_t)
        Ac = self.calc_Area(f_w, f_t, w_h, w_t)
        self.M = 7850 * Ac / 10000
        return round(self.M, 2)

    def calc_Area(self, f_w, f_t, w_h, w_t):
        self.A = f_w * w_h - (w_h - 2 * f_t) * (f_w - w_t)
        return round(self.A / 100, 2)

    def calc_C_y(self, f_w, f_t, w_h, w_t):
        Ac = self.calc_Area(f_w, f_t, w_h, w_t) * 100
        # self.Cy = ((f_w * (w_h**2)/2) - ((f_w - w_t)**2 * (w_h - (2 * f_t))/2))/Ac
        self.Cy = ((w_h * (f_w ** 2) / 2) - (f_w - w_t) * (w_h - (2 * f_t)) * (w_t + (f_w - w_t) / 2)) / Ac
        return round(self.Cy / 10, 2)

    def calc_MomentOfAreaZ(self, f_w, f_t, w_h, w_t):
        self.I_zz = (f_w * w_h ** 3) / 12 - ((f_w - w_t) * (w_h - 2 * f_t) ** 3) / 12
        print(self.I_zz, "duvbdf")
        return round(self.I_zz / 10000, 2)

    def calc_MomentOfAreaY(self, f_w, f_t, w_h, w_t):
        Cyc = self.calc_C_y(f_w, f_t, w_h, w_t) * 10
        # Cyc = 13.2
        # self.I_yy = (w_h * (f_w**3)/12) + (f_w * w_h * (Cyc - (f_w/2))**2) - (((w_h - (2 * f_t)) * ((f_w - w_t)**3)/12) - ((w_h - (2 * f_t)) * (f_w - w_t) * (Cyc - ((f_w+w_t)/2))**2))
        self.I_yy = ((w_h * f_w ** 3) / 12) + w_h * f_w * (Cyc - (f_w / 2)) ** 2 - (
                ((w_h - 2 * f_t) * (f_w - w_t) ** 3) / 12) - (
                            w_h - 2 * f_t) * (f_w - w_t) * (Cyc - ((f_w + w_t) / 2)) ** 2
        return round(self.I_yy / 10000, 2)

    def calc_RogZ(self, f_w, f_t, w_h, w_t):
        Ac = self.calc_Area(f_w, f_t, w_h, w_t)
        I_zzc = self.calc_MomentOfAreaZ(f_w, f_t, w_h, w_t)
        self.R_zz = math.sqrt(I_zzc / Ac)
        return round(self.R_zz, 2)

    def calc_RogY(self, f_w, f_t, w_h, w_t):
        Ac = self.calc_Area(f_w, f_t, w_h, w_t)
        I_yyc = self.calc_MomentOfAreaY(f_w, f_t, w_h, w_t)
        self.R_yy = math.sqrt(I_yyc / Ac)
        return round(self.R_yy, 2)

    def calc_ElasticModulusZz(self, f_w, f_t, w_h, w_t):
        I_zzc = self.calc_MomentOfAreaZ(f_w, f_t, w_h, w_t)
        self.Z_zz = I_zzc / (0.5 * (w_h / 10))
        return round(self.Z_zz, 2)

    def calc_ElasticModulusZy(self, f_w, f_t, w_h, w_t):
        Cyc = self.calc_C_y(f_w, f_t, w_h, w_t)
        I_yyc = self.calc_MomentOfAreaY(f_w, f_t, w_h, w_t)
        self.Z_yy = I_yyc / ((f_w / 10) - Cyc)
        return round(self.Z_yy, 2)

    def calc_PlasticModulusZpz(self, f_w, f_t, w_h, w_t):
        self.Z_pz = f_w * (w_h ** 2) / 4 - (f_w - w_t) * ((w_h - 2 * f_t) ** 2) / 4
        return round(self.Z_pz / 1000, 2)

    def calc_PlasticModulusZpy(self, f_w, f_t, w_h, w_t):
        A_w = w_h * w_t
        A_f = 2 * (f_w - w_t) * f_t
        if A_w > A_f:
            x = (A_w + A_f) / (2 * w_h)
            A_1 = w_h * x
            A_2 = w_h * (w_t - x)
            A_3 = 2 * (f_w - w_t) * f_t
            y_1 = x / 2
            y_2 = (w_t - x) / 2
            y_3 = (w_t - x) + (f_w - w_t) / 2

            print("Web area is more than flange area")
        else:
            x = f_w - (A_w + A_f) / (4 * f_t)
            A_1 = w_h * w_t
            A_2 = 2 * (x - w_t) * f_t
            A_3 = 2 * (f_w - x) * f_t
            y_1 = (x - w_t) + (w_t / 2)
            y_2 = (x - w_t) / 2
            y_3 = (f_w - x) / 2
            print("Flange area is more than web area")

        self.Z_py = A_1 * y_1 + A_2 * y_2 + A_3 * y_3
        return round(self.Z_py / 1000, 2)

    def calc_TorsionConstantIt(self, f_w, f_t, w_h, w_t):
        self.It = 2 * ((f_w * f_t ** 3) / 3) + (w_h * w_t ** 3) / 3
        return round(self.It / 10000, 2)

    def calc_WarpingConstantIw(self,param1,param2,param3,param4):
        a = 0.0
        return a


class BBChannel_Properties(Section_Properties):

    def __init__(self):
        self.db = False

    def data(self, designation, material_grade):
        self.Channel_attributes = Channel(designation, material_grade)
        self.db = True

    def calc_Mass(self, f_w, f_t, w_h, w_t):
        self.A = self.calc_Area(f_w, f_t, w_h, w_t)
        self.M = 7850 * self.A / 10000
        return round(self.M, 2)

    def calc_Area(self, f_w, f_t, w_h, w_t):
        if self.db == False:
            self.A = 2 * (f_w * w_h - (w_h - 2 * f_t) * (f_w - w_t))
        else:
            self.A = 2 * self.Channel_attributes.area
        return round(self.A / 100, 2)

    #
    def calc_C_y(self, f_w, f_t, w_h, w_t):
        if self.db == False:
            Ac = Single_Channel_Properties().calc_Area(f_w, f_t, w_h, w_t) * 100
            self.Cy = ((w_h * (f_w ** 2) / 2) - (f_w - w_t) * (w_h - (2 * f_t)) * (w_t + (f_w - w_t) / 2)) / Ac
        else:
            self.Cy = self.Channel_attributes.Cy
        return round(self.Cy / 10, 2)

    def calc_MomentOfAreaZ(self, f_w, f_t, w_h, w_t, thickness=0.0):
        if self.db == False:
            self.I_zz = 2 * Single_Channel_Properties().calc_MomentOfAreaZ(f_w, f_t, w_h, w_t) * 10000
        else:
            self.I_zz = 2 * self.Channel_attributes.mom_inertia_z

        return round(self.I_zz / 10000, 2)

    def calc_MomentOfAreaY(self, f_w, f_t, w_h, w_t, thickness=0.0):
        if self.db == False:
            mom_inertia_y = Single_Channel_Properties().calc_MomentOfAreaY(f_w, f_t, w_h, w_t)*10000
            area = Single_Channel_Properties().calc_Area(f_w, f_t, w_h, w_t)*100
            Cg_1 = Single_Channel_Properties().calc_C_y(f_w, f_t, w_h, w_t)*10
            self.I_yy = (mom_inertia_y + (area * (Cg_1 + thickness / 2) * (Cg_1 + thickness / 2))) * 2
        else:
            mom_inertia_y = self.Channel_attributes.mom_inertia_y
            area = self.Channel_attributes.area
            Cg_1 = self.Channel_attributes.Cy
            self.I_yy = (mom_inertia_y + (area * (Cg_1 + thickness / 2) * (Cg_1 + thickness / 2))) * 2

        return round(self.I_yy/10000, 2)

    def calc_RogZ(self, f_w, f_t, w_h, w_t, thickness=0.0):
        mom_inertia_z = self.calc_MomentOfAreaZ(f_w, f_t, w_h, w_t, thickness)
        area = self.calc_Area(f_w, f_t, w_h, w_t)
        self.r_z = math.sqrt(mom_inertia_z / area)

        return round(self.r_z, 2)

    def calc_RogY(self, f_w, f_t, w_h, w_t, thickness=0.0):
        mom_inertia_y = self.calc_MomentOfAreaY(f_w, f_t, w_h, w_t, thickness)
        area = self.calc_Area(f_w, f_t, w_h, w_t)
        self.r_y = math.sqrt(mom_inertia_y / area)

        return round(self.r_y, 2)

    def calc_ElasticModulusZz(self, f_w, f_t, w_h, w_t, thickness=0.0):
        I_zzc = self.calc_MomentOfAreaZ(f_w, f_t, w_h, w_t, thickness)
        self.Z_zz = I_zzc / (0.5 * (w_h / 10))
        return round(self.Z_zz, 2)

    def calc_ElasticModulusZy(self, f_w, f_t, w_h, w_t, thickness=0.0):
        I_yyc = self.calc_MomentOfAreaY(f_w, f_t, w_h, w_t, thickness)
        self.Z_yy = I_yyc / ((f_w + thickness / 2) / 10)
        return round(self.Z_yy, 2)

    def calc_PlasticModulusZpz(self, f_w, f_t, w_h, w_t, thickness=0.0):
        # A = self.calc_Area(f_w, f_t, w_h, w_t)*100
        self.Z_pz = 2 * f_w * (w_h ** 2) / 4 - 2 * ((f_w - w_t) * ((w_h - 2 * f_t) ** 2) / 4)
        # self.Z_pz = A * (w_h/4 + w_h/4)/2
        return round(self.Z_pz / 1000, 2)

    def calc_PlasticModulusZpy(self, f_w, f_t, w_h, w_t, thickness=0.0):
        A = self.calc_Area(f_w, f_t, w_h, w_t)*100
        Cg_1 = Single_Channel_Properties().calc_C_y(f_w, f_t, w_h, w_t)*10
        # self.Z_py = 2 * w_h * ((f_w) ** 2) / 4 - 2 * ((w_h - 2 * f_t) * ((f_w - w_t) ** 2) / 4)
        self.Z_py = A * (Cg_1+Cg_1+thickness)/2
        return round(self.Z_py / 1000, 2)

    def calc_TorsionConstantIt(self, f_w, f_t, w_h, w_t):
        if self.db == False:
            self.It = (2 * ((f_w * f_t ** 3) / 3) + (w_h * w_t ** 3) / 3) * 2
        else:
            self.It = self.Channel_attributes.It * 2
        return round(self.It / 10000, 2)

    def calc_WarpingConstantIw(self, f_w, f_t, w_h, w_t):
        a = 0.0
        return a


class SHS_RHS_Properties(Section_Properties):
    """ """

    def calc_Mass(self, D, B, t, t_f, alpha=90, r_1=0, r_2=0):
        self.A = 2 * t * ((B - (4 * t)) + (D - (4 * t)) + ((3 / 2) * math.pi * t))  # cm2
        self.M = 0.785 * self.A  # kg/m

        return round(self.M * 1e-2, 2)

    def calc_Area(self, D, B, t, t_f, alpha=90, r_1=0, r_2=0):
        self.A = 2 * t * ((B - (4 * t)) + (D - (4 * t)) + ((3 / 2) * math.pi * t))  # cm2

        return round(self.A * 1e-2, 2)

    def calc_MomentOfAreaZ(self, D, B, t, t_f, alpha=90, r_1=0, r_2=0):
        self.I_zz = (t * ((D - (4 * t)) ** 3 / 6)) + (0.5 * ((((B - (4 * t)) * t ** 3) / 3) + ((B - (4 * t)) * ((D - t) ** 2) * t))) + \
                    (((math.pi * t ** 4) / 108) * (405 - (3136 / math.pi ** 2))) + \
                    ((3 * math.pi * t ** 2) * (((9 * math.pi * (D - (4 * t))) + (56 * t)) / (18 * math.pi)) ** 2)  # cm4

        return round(self.I_zz * 1e-4, 2)

    def calc_MomentOfAreaY(self, D, B, t, t_f, alpha=90, r_1=0, r_2=0):
        self.I_yy = (t * ((B - (4 * t)) ** 3 / 6)) + (0.5 * ((((D - (4 * t)) * t ** 3) / 3) + ((D - (4 * t)) * ((B - t) ** 2) * t))) + \
                    (((math.pi * t ** 4) / 108) * (405 - (3136 / math.pi ** 2))) + \
                    ((3 * math.pi * t ** 2) * (((9 * math.pi * (B - (4 * t))) + (56 * t)) / (18 * math.pi)) ** 2)  # cm4

        return round(self.I_yy * 1e-4, 2)

    def calc_RogZ(self, D, B, t, t_f, alpha=90, r_1=0, r_2=0):
        self.A = 2 * t * ((B - (4 * t)) + (D - (4 * t)) + ((3 / 2) * math.pi * t))  # cm2
        self.I_zz = (t * ((D - (4 * t)) ** 3 / 6)) + (0.5 * ((((B - (4 * t)) * t ** 3) / 3) + ((B - (4 * t)) * ((D - t) ** 2) * t))) + \
                    (((math.pi * t ** 4) / 108) * (405 - (3136 / math.pi ** 2))) + \
                    ((3 * math.pi * t ** 2) * (((9 * math.pi * (D - (4 * t))) + (56 * t)) / (18 * math.pi)) ** 2)  # cm4
        self.r_z = math.sqrt(self.I_zz / self.A)  # cm

        return round(self.r_z * 1e-1, 2)

    def calc_RogY(self, D, B, t, t_f, alpha=90, r_1=0, r_2=0):
        self.A = 2 * t * ((B - (4 * t)) + (D - (4 * t)) + ((3 / 2) * math.pi * t))  # cm2
        self.I_yy = (t * ((B - (4 * t)) ** 3 / 6)) + (0.5 * ((((D - (4 * t)) * t ** 3) / 3) + ((D - (4 * t)) * ((B - t) ** 2) * t))) + \
                    (((math.pi * t ** 4) / 108) * (405 - (3136 / math.pi ** 2))) + \
                    ((3 * math.pi * t ** 2) * (((9 * math.pi * (B - (4 * t))) + (56 * t)) / (18 * math.pi)) ** 2)  # cm4
        self.r_y = math.sqrt(self.I_yy / self.A)  # cm

        return round(self.r_y * 1e-1, 2)

    def calc_ElasticModulusZz(self, D, B, t, t_f, alpha=90, r_1=0, r_2=0):
        self.I_zz = (t * ((D - (4 * t)) ** 3 / 6)) + (0.5 * ((((B - (4 * t)) * t ** 3) / 3) + ((B - (4 * t)) * ((D - t) ** 2) * t))) + \
                    (((math.pi * t ** 4) / 108) * (405 - (3136 / math.pi ** 2))) + \
                    ((3 * math.pi * t ** 2) * (((9 * math.pi * (D - (4 * t))) + (56 * t)) / (18 * math.pi)) ** 2)  # cm4
        self.Z_ez = (2 * self.I_zz) / D  # cm3

        return round(self.Z_ez * 1e-3, 2)

    def calc_ElasticModulusZy(self, D, B, t, t_f, alpha=90, r_1=0, r_2=0):
        self.I_yy = (t * ((B - (4 * t)) ** 3 / 6)) + (0.5 * ((((D - (4 * t)) * t ** 3) / 3) + ((D - (4 * t)) * ((B - t) ** 2) * t))) + \
                    (((math.pi * t ** 4) / 108) * (405 - (3136 / math.pi ** 2))) + \
                    ((3 * math.pi * t ** 2) * (((9 * math.pi * (B - (4 * t))) + (56 * t)) / (18 * math.pi)) ** 2)  # cm4

        self.Z_ey = (2 * self.I_yy) / B  # cm3

        return round(self.Z_ey * 1e-3, 2)

    def calc_PlasticModulusZpz(self, D, B, t, t_f, alpha=90, r_1=0, r_2=0):
        self.Z_pz = (((t / 2) * (D - (4 * t)) ** 2) + (t * (B - (4 * t)) * (D - t)) + ((t ** 2 / 6) *
                                                                                       ((9 * math.pi * (D - (4 * t))) + (56 * t))))  # cm3

        return round(self.Z_pz * 1e-3, 2)

    def calc_PlasticModulusZpy(self, D, B, t, t_f, alpha=90, r_1=0, r_2=0):
        self.Z_py = (((t / 2) * (B - (4 * t)) ** 2) + (t * (D - (4 * t)) * (B - t)) + ((t ** 2 / 6) *
                                                                                       ((9 * math.pi * (B - (4 * t))) + (56 * t))))  # cm3

        return round(self.Z_py * 1e-3, 2)

    def calc_TorsionConstantIt(self, D, B, t_w, t_f, alpha=90, r_1=0, r_2=0):
        return 0.0

    def calc_WarpingConstantIw(self, D, B, t_w, t_f, alpha=90, r_1=0, r_2=0):
        return 0.0


class CHS_Properties(Section_Properties):
    """ """

    def calc_Mass(self, D, B, t, t_f, alpha=90, r_1=0, r_2=0):
        self.A = (math.pi / 4) * (D ** 2 - (D - (2 * t)) ** 2)
        self.M = 0.785 * self.A  # kg/m

        return round(self.M * 1e-2, 2)

    def calc_Area(self, D, B, t, t_f, alpha=90, r_1=0, r_2=0):
        self.A = (math.pi / 4) * (D ** 2 - (D - (2 * t)) ** 2)

        return round(self.A * 1e-2, 2)

    def calc_MomentOfAreaZ(self, D, B, t, t_f, alpha=90, r_1=0, r_2=0):
        self.I_zz = (math.pi / 64) * (D ** 4 - (D - (2 * t)) ** 4)  # cm4

        return round(self.I_zz * 1e-4, 2)

    def calc_MomentOfAreaY(self, D, B, t, t_f, alpha=90, r_1=0, r_2=0):
        self.I_yy = (math.pi / 64) * (D ** 4 - (D - (2 * t)) ** 4)  # cm4

        return round(self.I_yy * 1e-4, 2)

    def calc_RogZ(self, D, B, t, t_f, alpha=90, r_1=0, r_2=0):
        self.A = (math.pi / 4) * (D ** 2 - (D - (2 * t)) ** 2)  # cm2
        self.I = (math.pi / 64) * (D ** 4 - (D - (2 * t)) ** 4)  # cm4
        self.r = math.sqrt(self.I_zz / self.A)  # cm

        return round(self.r, 1)

    def calc_RogY(self, D, B, t, t_f, alpha=90, r_1=0, r_2=0):
        self.A = (math.pi / 4) * (D ** 2 - (D - (2 * t)) ** 2)  # cm2
        self.I = (math.pi / 64) * (D ** 4 - (D - (2 * t)) ** 4)  # cm4
        self.r = math.sqrt(self.I_zz / self.A)  # cm

        return round(self.r, 1)

    def calc_ElasticModulusZz(self, D, B, t, t_f, alpha=90, r_1=0, r_2=0):
        self.I_zz = (math.pi / 64) * (D ** 4 - (D - (2 * t)) ** 4)  # cm4
        self.Z_ez = (2 * self.I_zz) / D  # cm3

        return round(self.Z_ez * 1e-3, 2)

    def calc_ElasticModulusZy(self, D, B, t, t_f, alpha=90, r_1=0, r_2=0):
        self.I_yy = (math.pi / 64) * (D ** 4 - (D - (2 * t)) ** 4)  # cm4
        self.Z_ey = (2 * self.I_yy) / D  # cm3

        return round(self.Z_ey * 1e-3, 2)

    def calc_PlasticModulusZpz(self, D, B, t, t_f, alpha=90, r_1=0, r_2=0):
        self.Z_pz = (((t / 2) * (D - (4 * t)) ** 2) + (t * (B - (4 * t)) * (D - t)) + ((t ** 2 / 6) *
                                                                                       ((9 * math.pi * (D - (4 * t))) + (56 * t))))  # cm3

        return round(self.Z_pz * 1e-3, 2)

    def calc_PlasticModulusZpy(self, D, B, t, t_f, alpha=90, r_1=0, r_2=0):
        self.Z_pz = (((t / 2) * (D - (4 * t)) ** 2) + (t * (B - (4 * t)) * (D - t)) + ((t ** 2 / 6) *
                                                                                       ((9 * math.pi * (D - (4 * t))) + (56 * t))))  # cm3

        return round(self.Z_pz * 1e-3, 2)

    def calc_InternalVolume(self):
        return 0.0

    def calc_TorsionConstantIt(self, D, B, t_w, t_f, alpha=90, r_1=0, r_2=0):
        return 0.0

    def calc_WarpingConstantIw(self, D, B, t_w, t_f, alpha=90, r_1=0, r_2=0):
        return 0.0
