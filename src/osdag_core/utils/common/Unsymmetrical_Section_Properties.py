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

        @staticmethod
        def calc_mass(D, B_top, B_bot, t_w, t_f_top, t_f_bot):
                A = Unsymmetrical_I_Section_Properties.calc_area(D, B_top, B_bot, t_w, t_f_top, t_f_bot)
                M = (7850 * A) / 1000000  # Convert to kg from mm^2
                return round(M, 2)

        @staticmethod
        def calc_area(D, B_top, B_bot, t_w, t_f_top, t_f_bot):
                A = (B_top * t_f_top + B_bot * t_f_bot + (D - t_f_top - t_f_bot) * t_w)
                return round(A, 2)

        @staticmethod
        def calc_centroid(D, B_top, B_bot, t_w, t_f_top, t_f_bot):
                A_top = B_top * t_f_top
                A_bot = B_bot * t_f_bot
                A_web = (D - t_f_top - t_f_bot) * t_w

                y_top = D - t_f_top / 2
                y_bot = t_f_bot / 2
                y_web = t_f_bot + (D - t_f_top - t_f_bot) / 2

                y_neutral = (A_top * y_top + A_bot * y_bot + A_web * y_web) / (A_top + A_bot + A_web)
                return y_neutral

        @staticmethod
        def calc_MomentOfAreaZ(D, B_top, B_bot, t_w, t_f_top, t_f_bot):
                y_neutral = Unsymmetrical_I_Section_Properties.calc_centroid(D, B_top, B_bot, t_w, t_f_top, t_f_bot)

                I_top = (B_top * t_f_top ** 3) / 12 + B_top * t_f_top * (D - t_f_top / 2 - y_neutral) ** 2
                I_bot = (B_bot * t_f_bot ** 3) / 12 + B_bot * t_f_bot * (y_neutral - t_f_bot / 2) ** 2
                I_web = (t_w * (D - t_f_top - t_f_bot) ** 3) / 12 + t_w * (D - t_f_top - t_f_bot) * (
                            y_neutral - (t_f_bot + (D - t_f_top - t_f_bot) / 2)) ** 2

                I_zz = (I_top + I_bot + I_web)
                return round(I_zz, 2)

        @staticmethod
        def calc_MomentOfAreaY(D, B_top, B_bot, t_w, t_f_top, t_f_bot):
                I_top = (t_f_top * B_top ** 3) / 12
                I_bot = (t_f_bot * B_bot ** 3) / 12
                I_web = ((D - t_f_top - t_f_bot) * t_w ** 3) / 12

                I_yy = (I_top + I_bot + I_web)
                return round(I_yy, 2)

        @staticmethod
        def calc_ElasticModulusZz( D, B_top, B_bot, t_w, t_f_top, t_f_bot):
                I_zz = Unsymmetrical_I_Section_Properties.calc_MomentOfAreaZ(D, B_top, B_bot, t_w, t_f_top, t_f_bot)
                y_neutral = Unsymmetrical_I_Section_Properties.calc_centroid(D, B_top, B_bot, t_w, t_f_top, t_f_bot)
                Z_ez_top = I_zz  / (D - y_neutral)
                Z_ez_bot = I_zz  / y_neutral
                return round(min(Z_ez_top, Z_ez_bot), 2)

        @staticmethod
        def calc_ElasticModulusZy( D, B_top, B_bot, t_w, t_f_top, t_f_bot):
                I_yy = Unsymmetrical_I_Section_Properties.calc_MomentOfAreaY(D, B_top, B_bot, t_w, t_f_top, t_f_bot)
                B_max = max(B_top, B_bot)
                Z_ey = (I_yy * 2 ) / B_max
                return round(Z_ey, 2)

        @staticmethod
        def calc_PlasticModulusZ( D, bf_top, bf_bot, tw, tf_top, tf_bot, eps=1.0):
            """
            Plastic section modulus Zp about strong axis for unsymmetrical I-sections.
            
            For plastic modulus, we find the plastic neutral axis (PNA) which divides
            the cross-section into two equal areas. Then Zp = sum of (Ai × yi) where
            yi is the distance from PNA to centroid of each element.

            D       : total section depth between outer flange faces (mm)
            bf_top  : top flange width (mm)
            bf_bot  : bottom flange width (mm)
            tw      : web thickness (mm)
            tf_top  : top flange thickness (mm)
            tf_bot  : bottom flange thickness (mm)
            eps     : epsilon factor (not used directly for Zp, kept for API compatibility)
            """
            # Web clear height between flanges
            h_w = D - tf_top - tf_bot
            
            # Calculate areas
            A_top = bf_top * tf_top
            A_bot = bf_bot * tf_bot
            A_web = h_w * tw
            A_total = A_top + A_bot + A_web
            half_area = A_total / 2.0
            
            # Find plastic neutral axis location (from bottom of section)
            # PNA divides the section into two equal areas
            if A_bot >= half_area:
                # PNA is in bottom flange
                y_pna = half_area / bf_bot
            elif A_bot + A_web >= half_area:
                # PNA is in web
                y_pna = tf_bot + (half_area - A_bot) / tw
            else:
                # PNA is in top flange
                y_pna = D - (A_total - half_area) / bf_top
            
            # Calculate plastic section modulus Zp
            # Zp = sum of (area × distance from PNA to centroid of that area)
            # Using the formula: Zp = (bf_bot*y_pna² - (bf_bot-tw)*(y_pna-tf_bot)² + 
            #                         bf_top*(D-y_pna)² - (bf_top-tw)*(D-tf_top-y_pna)²) / 2
            
            # This formula works when PNA is in the web
            if y_pna >= tf_bot and y_pna <= D - tf_top:
                Zp = (
                    bf_bot * y_pna**2 - 
                    (bf_bot - tw) * max(0, y_pna - tf_bot)**2 + 
                    bf_top * (D - y_pna)**2 - 
                    (bf_top - tw) * max(0, D - tf_top - y_pna)**2
                ) / 2.0
            else:
                # PNA is in a flange - use component method
                Zp = 0.0
                # Bottom flange contribution
                if y_pna > 0:
                    if y_pna <= tf_bot:
                        # PNA is in bottom flange
                        Zp += bf_bot * y_pna * (y_pna / 2)  # area below PNA
                        Zp += bf_bot * (tf_bot - y_pna) * ((tf_bot - y_pna) / 2 + y_pna - tf_bot)  # area above
                    else:
                        Zp += A_bot * abs(y_pna - tf_bot / 2)  # whole bottom flange
                
                # Web contribution
                if y_pna > tf_bot and y_pna < D - tf_top:
                    web_below = (y_pna - tf_bot) * tw
                    web_above = (D - tf_top - y_pna) * tw
                    Zp += web_below * (y_pna - tf_bot) / 2
                    Zp += web_above * (D - tf_top - y_pna) / 2
                elif y_pna <= tf_bot:
                    Zp += A_web * (tf_bot + h_w / 2 - y_pna)
                else:  # y_pna >= D - tf_top
                    Zp += A_web * (y_pna - tf_bot - h_w / 2)
                
                # Top flange contribution
                if y_pna >= D - tf_top:
                    # PNA is in top flange
                    above_pna = D - y_pna
                    below_pna = y_pna - (D - tf_top)
                    Zp += bf_top * above_pna * (above_pna / 2)
                    Zp += bf_top * below_pna * (below_pna / 2)
                else:
                    Zp += A_top * abs(D - tf_top / 2 - y_pna)
            
            return round(Zp, 2)

        @staticmethod
        def calc_PlasticModulusY( D, B_top, B_bot, t_w, t_f_top, t_f_bot):
                Zpy = (t_f_top * B_top ** 2 / 4 + t_f_bot * B_bot ** 2 / 4 + (D - t_f_top - t_f_bot) * t_w ** 2 / 4)
                return round(Zpy, 2)

        @staticmethod
        def calc_TorsionConstantIt( D, B_top, B_bot, t_w, t_f_top, t_f_bot):
                    h = D - ((t_f_top + t_f_bot)/2)
                    It = (1 / 3) * ( B_top * t_f_top  ** 3 +  B_bot * t_f_bot ** 3 +  h * t_w ** 3 )
                    return round(It, 2)

        @staticmethod
        def calc_WarpingConstantIw( D, B_top, B_bot, t_w, t_f_top, t_f_bot):
                    h = D - ((t_f_top + t_f_bot)/2)
                    numerator_Iw = (h ** 2) * t_f_top * t_f_bot * (B_top ** 3) * (B_bot ** 3)
                    denominator_Iw = 12 * (t_f_top * B_top ** 3 + t_f_bot * B_bot ** 3)
                    Iw = numerator_Iw / denominator_Iw
                    return round(Iw, 2)
        
        @staticmethod
        def calc_RadiusOfGyrationZ( D, B_top, B_bot, t_w, t_f_top, t_f_bot):
                """
                Radius of gyration about z-axis (major axis)
                """
                I_zz = Unsymmetrical_I_Section_Properties.calc_MomentOfAreaZ(D, B_top, B_bot, t_w, t_f_top, t_f_bot)
                A = Unsymmetrical_I_Section_Properties.calc_area(D, B_top, B_bot, t_w, t_f_top, t_f_bot)
                r_z = math.sqrt(I_zz / A)
                return round(r_z, 2)

        @staticmethod
        def calc_RadiusOfGyrationY( D, B_top, B_bot, t_w, t_f_top, t_f_bot):
                """
                Radius of gyration about y-axis (minor axis)
                """
                I_yy = Unsymmetrical_I_Section_Properties.calc_MomentOfAreaY(D, B_top, B_bot, t_w, t_f_top, t_f_bot)
                A = Unsymmetrical_I_Section_Properties.calc_area(D, B_top, B_bot, t_w, t_f_top, t_f_bot)
                r_y = math.sqrt(I_yy / A)
                return round(r_y, 2)