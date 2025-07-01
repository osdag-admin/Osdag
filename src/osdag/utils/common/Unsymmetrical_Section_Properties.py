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
                M = (7850 * A) / 1000000  # Convert to kg from mm^2
                return round(M, 2)


        def calc_area(self, D, B_top, B_bot, t_w, t_f_top, t_f_bot):
                A = (B_top * t_f_top + B_bot * t_f_bot + (D - t_f_top - t_f_bot) * t_w)
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

                I_zz = (I_top + I_bot + I_web)
                return round(I_zz, 2)


        def calc_MomentOfAreaY(self, D, B_top, B_bot, t_w, t_f_top, t_f_bot):
                I_top = (t_f_top * B_top ** 3) / 12
                I_bot = (t_f_bot * B_bot ** 3) / 12
                I_web = ((D - t_f_top - t_f_bot) * t_w ** 3) / 12

                I_yy = (I_top + I_bot + I_web)
                return round(I_yy, 2)


        def calc_ElasticModulusZz(self, D, B_top, B_bot, t_w, t_f_top, t_f_bot):
                I_zz = Unsymmetrical_I_Section_Properties.calc_MomentOfAreaZ(self,D, B_top, B_bot, t_w, t_f_top, t_f_bot)
                y_neutral = Unsymmetrical_I_Section_Properties.calc_centroid(self,D, B_top, B_bot, t_w, t_f_top, t_f_bot)
                Z_ez_top = I_zz  / (D - y_neutral)
                Z_ez_bot = I_zz  / y_neutral
                return round(min(Z_ez_top, Z_ez_bot), 2)


        def calc_ElasticModulusZy(self, D, B_top, B_bot, t_w, t_f_top, t_f_bot):
                I_yy = Unsymmetrical_I_Section_Properties.calc_MomentOfAreaY(self,D, B_top, B_bot, t_w, t_f_top, t_f_bot)
                B_max = max(B_top, B_bot)
                Z_ey = (I_yy * 2 ) / B_max
                return round(Z_ey, 2)


        def calc_PlasticModulusZ(self, D, bf_top, bf_bot, tw, tf_top, tf_bot, eps):
            """
                    Plastic section modulus Zp about strong axis for unequal flanges:

                    D       : total section depth between outer flange faces (mm)
                    bf_top  : top flange width (mm)
                    bf_bot  : bottom flange width (mm)
                    tw      : web thickness (mm)
                    tf_top  : top flange thickness (mm)
                    tf_bot  : bottom flange thickness (mm)
                    """
            # clear web height between flange faces
            h_w = D - tf_top - tf_bot
            # thin-web check
            if h_w/tw > 67 * eps:
                print("Thin web condition, using rectangular section properties", h_w/tw)
                A_top = bf_top * tf_top
                A_bot = bf_bot * tf_bot
                A = A_top + A_bot

                # Centroid location from top fiber
                # top rectangle centroid at tf_top/2, bottom at D - tf_bot/2
                c = (A_top * (tf_top / 2) + A_bot * (D - tf_bot / 2)) / A
                c1 = D - c

                # Distances from each rectangle's centroid to the composite centroid
                y_top_centroid = abs((tf_top / 2) - c)
                y_bot_centroid = abs((D - tf_bot / 2) - c)

                # Second moment of area of each rectangle about its own centroid
                I_top = (bf_top * tf_top ** 3) / 12.0
                I_bot = (bf_bot * tf_bot ** 3) / 12.0

                # Parallel-axis theorem
                I = I_top + A_top * y_top_centroid ** 2 + I_bot + A_bot * y_bot_centroid ** 2

                # Section moduli
                Zp = I / c
                return round(Zp, 2)
                    
            else:

                A_u = bf_top * tf_top
                A_d = bf_bot * tf_bot
                A_w = h_w * tw
                A = A_u + A_d + A_w
                if h_w / tw <= 67.0 * eps:
                        y = (A_u * tf_top/2 + A_d * (D - tf_bot/2))/(A_u + A_d)
                        y1 = D - y

                # centroids measured from bottom face
                y_d = tf_bot / 2.0
                y_w = tf_bot + h_w / 2.0
                y_u = tf_bot + h_w + tf_top / 2.0
                # plastic neutral axis from bottom face
                if A_d < A / 2.0 and A_u < A / 2.0:
                        y_pna = tf_bot + (A - 2 * A_d) / (2 * tw)
                elif A_d >= A / 2.0:
                        y_pna = A / (2 * bf_bot)
                else:
                        y_pna = D - A / (2 * bf_top)
                # compute Zp as sum of Ai * distance from plastic axis
                Zp = (
                                (bf_bot * y_pna ** 2 - (bf_bot - tw) * (y_pna - tf_bot) ** 2)
                                + (bf_top * (D - y_pna) ** 2 - (bf_top - tw) * (D - tf_top - y_pna) ** 2)
                        ) / 2.0
                return round(Zp, 2)

        def calc_PlasticModulusY(self, D, B_top, B_bot, t_w, t_f_top, t_f_bot):
                Zpy = (t_f_top * B_top ** 2 / 4 + t_f_bot * B_bot ** 2 / 4 + (D - t_f_top - t_f_bot) * t_w ** 2 / 4)
                return round(Zpy, 2)

        def calc_TorsionConstantIt(self, D, B_top, B_bot, t_w, t_f_top, t_f_bot):
                    h = D - ((t_f_top + t_f_bot)/2)
                    It = (1 / 3) * ( B_top * t_f_top  ** 3 +  B_bot * t_f_bot ** 3 +  h * t_w ** 3 )
                    return round(It, 2)

        def calc_WarpingConstantIw(self, D, B_top, B_bot, t_w, t_f_top, t_f_bot):
                    h = D - ((t_f_top + t_f_bot)/2)
                    numerator_Iw = (h ** 2) * t_f_top * t_f_bot * (B_top ** 3) * (B_bot ** 3)
                    denominator_Iw = 12 * (t_f_top * B_top ** 3 + t_f_bot * B_bot ** 3)
                    Iw = numerator_Iw / denominator_Iw
                    return round(Iw, 2)
        
        def calc_RadiusOfGyrationZ(self, D, B_top, B_bot, t_w, t_f_top, t_f_bot):
                """
                Radius of gyration about z-axis (major axis)
                """
                I_zz = self.calc_MomentOfAreaZ(D, B_top, B_bot, t_w, t_f_top, t_f_bot)
                A = self.calc_area(D, B_top, B_bot, t_w, t_f_top, t_f_bot)
                r_z = math.sqrt(I_zz / A)
                return round(r_z, 2)

        def calc_RadiusOfGyrationY(self, D, B_top, B_bot, t_w, t_f_top, t_f_bot):
                """
                Radius of gyration about y-axis (minor axis)
                """
                I_yy = self.calc_MomentOfAreaY(D, B_top, B_bot, t_w, t_f_top, t_f_bot)
                A = self.calc_area(D, B_top, B_bot, t_w, t_f_top, t_f_bot)
                r_y = math.sqrt(I_yy / A)
                return round(r_y, 2)