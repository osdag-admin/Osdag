import math
class Unsymmetrical_I_Section_Properties:
        """
        Parameters:
        D       : Total depth of the section
        B_top   : Width of the top flange
        B_bot   : Width of the bottom flange
        t_w     : Thickness of the web
        t_f_top : Thickness of the top flange
        t_f_bot : Thickness of the bottom flange

        """


        def calc_mass(self, D, B_top, B_bot, t_w, t_f_top, t_f_bot):
                A = Unsymmetrical_I_Section_Properties.calc_area(self,D, B_top, B_bot, t_w, t_f_top, t_f_bot)
                M = (7850 * A) / 10000
                return round(M, 2)


        def calc_area(self, D, B_top, B_bot, t_w, t_f_top, t_f_bot):
                A = (B_top * t_f_top + B_bot * t_f_bot + (D - t_f_top - t_f_bot) * t_w) / 100
                return round(A, 2)


        def calc_centroid(self, D, B_top, B_bot, t_w, t_f_top, t_f_bot):
                A_top = B_top * t_f_top
                A_bot = B_bot * t_f_bot
                A_web = (D - t_f_top - t_f_bot) * t_w

                y_top = D - t_f_top / 2
                y_bot = t_f_bot / 2
                y_web = t_f_bot + (D - t_f_top - t_f_bot) / 2

                y_neutral = (A_top * y_top + A_bot * y_bot + A_web * y_web) / (A_top + A_bot + A_web)
                return y_neutral


        def calc_MomentOfAreaZ(self, D, B_top, B_bot, t_w, t_f_top, t_f_bot):
                y_neutral = Unsymmetrical_I_Section_Properties.calc_centroid(self,D, B_top, B_bot, t_w, t_f_top, t_f_bot)

                I_top = (B_top * t_f_top ** 3) / 12 + B_top * t_f_top * (D - t_f_top / 2 - y_neutral) ** 2
                I_bot = (B_bot * t_f_bot ** 3) / 12 + B_bot * t_f_bot * (y_neutral - t_f_bot / 2) ** 2
                I_web = (t_w * (D - t_f_top - t_f_bot) ** 3) / 12 + t_w * (D - t_f_top - t_f_bot) * (
                            y_neutral - (t_f_bot + (D - t_f_top - t_f_bot) / 2)) ** 2

                I_zz = (I_top + I_bot + I_web) / 10000
                return round(I_zz, 2)


        def calc_MomentOfAreaY(self, D, B_top, B_bot, t_w, t_f_top, t_f_bot):
                I_top = (t_f_top * B_top ** 3) / 12
                I_bot = (t_f_bot * B_bot ** 3) / 12
                I_web = ((D - t_f_top - t_f_bot) * t_w ** 3) / 12

                I_yy = (I_top + I_bot + I_web) / 10000
                return round(I_yy, 2)


        def calc_ElasticModulusZz(self, D, B_top, B_bot, t_w, t_f_top, t_f_bot):
                I_zz = Unsymmetrical_I_Section_Properties.calc_MomentOfAreaZ(self,D, B_top, B_bot, t_w, t_f_top, t_f_bot)
                y_neutral = Unsymmetrical_I_Section_Properties.calc_centroid(self,D, B_top, B_bot, t_w, t_f_top, t_f_bot)
                Z_ez_top = I_zz * 10 / (D - y_neutral)
                Z_ez_bot = I_zz * 10 / y_neutral
                return round(min(Z_ez_top, Z_ez_bot), 2)


        def calc_ElasticModulusZy(self, D, B_top, B_bot, t_w, t_f_top, t_f_bot):
                I_yy = Unsymmetrical_I_Section_Properties.calc_MomentOfAreaY(self,D, B_top, B_bot, t_w, t_f_top, t_f_bot)
                B_max = max(B_top, B_bot)
                Z_ey = (I_yy * 2 * 10) / B_max
                return round(Z_ey, 2)


        def calc_PlasticModulusZ(self, D, B_top, B_bot, t_w, t_f_top, t_f_bot):
                y_neutral = Unsymmetrical_I_Section_Properties.calc_centroid(self,D, B_top, B_bot, t_w, t_f_top, t_f_bot)
                A_top = B_top * t_f_top
                A_bot = B_bot * t_f_bot
                A_web_top = t_w * (D - y_neutral - t_f_top)
                A_web_bot = t_w * (y_neutral - t_f_bot)

                Zpz = (A_top * (D - y_neutral - t_f_top / 2) + A_web_top * (
                            D - y_neutral - t_f_top - (D - y_neutral - t_f_top) / 2) +
                       A_bot * (y_neutral - t_f_bot / 2) + A_web_bot * ((y_neutral - t_f_bot) / 2)) / 1000

                return round(Zpz, 2)


        def calc_PlasticModulusY(self, D, B_top, B_bot, t_w, t_f_top, t_f_bot):
                Zpy = (t_f_top * B_top ** 2 / 4 + t_f_bot * B_bot ** 2 / 4 + (D - t_f_top - t_f_bot) * t_w ** 2 / 4) / 1000
                return round(Zpy, 2)

        def calc_TorsionConstantIt(self, D, B_top, B_bot, t_w, t_f_top, t_f_bot):
                    h = D - (t_f_top + t_f_bot)
                    It = (1 / 3) * (t_f_top * B_top ** 3 + t_f_bot * B_bot ** 3 + t_w ** 3 * h)
                    return round(It, 2)

        def calc_WarpingConstantIw(self, D, B_top, B_bot, t_w, t_f_top, t_f_bot):
                    h = D - (t_f_top + t_f_bot)
                    numerator_Iw = (h ** 2) * t_f_top * t_f_bot * (B_top ** 3) * (B_bot ** 3)
                    denominator_Iw = 12 * (t_f_top * B_top ** 3 + t_f_bot * B_bot ** 3)
                    Iw = numerator_Iw / denominator_Iw
                    return round(Iw, 2)
        
        def calc_RadiusOfGyrationZ(self, D, B_top, B_bot, t_w, t_f_top, t_f_bot):
                """
                Radius of gyration about z-axis (major axis)
                """
                I_zz = self.calc_MomentOfAreaZ(D, B_top, B_bot, t_w, t_f_top, t_f_bot) * 10000  # convert to mm⁴
                A = self.calc_area(D, B_top, B_bot, t_w, t_f_top, t_f_bot) * 100  # convert to mm²
                r_z = math.sqrt(I_zz / A)
                return round(r_z, 2)

        def calc_RadiusOfGyrationY(self, D, B_top, B_bot, t_w, t_f_top, t_f_bot):
                """
                Radius of gyration about y-axis (minor axis)
                """
                I_yy = self.calc_MomentOfAreaY(D, B_top, B_bot, t_w, t_f_top, t_f_bot) * 10000  # convert to mm⁴
                A = self.calc_area(D, B_top, B_bot, t_w, t_f_top, t_f_bot) * 100  # convert to mm²
                r_y = math.sqrt(I_yy / A)
                return round(r_y, 2)