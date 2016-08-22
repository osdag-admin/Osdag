'''
Created on 16-Jul-2015

@author: deepa
'''
'''
Created on 25-May-2015

@author: subhrajit
'''
''' 
Example 5.18 Page 412 N. Subramanium
Design of steel structures
Design of fin-plate:
Design a web side plate connection (welded to the column and site bolted to the beam) for ISMB 400 in Fe 410 grade steel and to carry a reaction of 140 kN due
to factored loads. The connection is to the flange of an ISSC 200 column.

'''
import cmath;
import math
import sys;

from model import *
from PyQt4.Qt import QString
import logging
flag  = 1
logger = None

def module_setup():
    
    global logger
    logger = logging.getLogger("osdag.finPlateCalc")

module_setup()
# def set_designlogger():
#         global logger
#         logger = logging.getLogger("Designlogger")
#         logger.setLevel(logging.DEBUG)
#      
#         # create the logging file handler
#         fh = logging.FileHandler("fin.log", mode="w")
#         
#         #,datefmt='%a, %d %b %Y %H:%M:%S'
#         #formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#         
#         formatter = logging.Formatter('''
#         <div  class="LOG %(levelname)s">
#             <span class="DATE">%(asctime)s</span>
#             <span class="LEVEL">%(levelname)s</span>
#             <span class="MSG">%(message)s</span>
#         </div>''')
#         formatter.datefmt = '%a, %d %b %Y %H:%M:%S'
#         fh.setFormatter(formatter)
#      
#         # add handler to logger object
#         logger.addHandler(fh)
#         
        



#FUNCTION DEFINITIONS---------------
#BOLT: determination of shear capacity = fu * n * A / (root(3) * Y)
def bolt_shear(dia, n, fu):
    A = cmath.pi * dia * dia * 0.25 * 0.78; #threaded area = 0.78 x shank area
    root3 = cmath.sqrt(3);
    Vs = fu * n * A / (root3 * 1.25 * 1000);
    Vs = round(Vs.real,3);
    return Vs
    
#BOLT: determination of bearing capacity = 2.5 * kb * d * t * fu / Y
def bolt_bearing(dia, t, fu):
    #add code to determine kb if pitch, gauge, edge distance known
    kb = 0.5;            #assumption
    Vb = 2.5 * kb * dia * t * fu / (1.25 * 1000);
    Vb = round(Vb.real,3);
    return Vb;

# PLATE: minimum thickness of web plate for eccentricity
def web_min_h(shear, fy, thk):
    min_plate_ht = 5*shear*1000/(fy*thk);
    return min_plate_ht;


def finConn(uiObj):
    global logger
    beam_sec = uiObj['Member']['BeamSection']
    column_sec = uiObj['Member']['ColumSection']
    connectivity = uiObj['Member']['Connectivity']
    beam_fu = uiObj['Member']['fu (MPa)']
    beam_fy = uiObj['Member']['fy (MPa)']
              
    shear_load = uiObj['Load']['ShearForce (kN)']
                  
    bolt_dia = uiObj['Bolt']['Diameter (mm)']
    bolt_type  = uiObj["Bolt"]["Type"]
    bolt_grade = uiObj['Bolt']['Grade']
              
    web_plate_t = uiObj['Plate']['Thickness (mm)']
    web_plate_w = uiObj['Plate']['Width (mm)']
    web_plate_l = uiObj['Plate']['Height (mm)']
    web_plate_fu = uiObj['Member']['fu (MPa)']
    web_plate_fy = uiObj['Member']['fy (MPa)']
              
    weld_t = uiObj["Weld"]['Size (mm)']
    weld_fu = 410

    bolt_planes = 1 
    dictbeamdata  = get_beamdata(beam_sec)
    beam_w_t = float(dictbeamdata[QString("tw")])
    beam_f_t = float(dictbeamdata[QString("T")])
    beam_d = float(dictbeamdata[QString("D")])

    
    # ############### Need to discuss with sir ########################
    # #Bolt grade chosen from drop down list
    # 
    # #Bolt dia chosen from list of standard sizes between 12 and 36
    # 
    # # web_plate_t lies between (5, 63)
    # if web_plate_t < 5 | web_plate_t > 63:
    #     sys.exit();
    # 
    # #weld_fu lies between (410, 610)
    # if weld_fu <= 410 | weld_fu >= 610:
    #     sys.exit();

    ########################################################################
    # INPUT FOR PLATE DIMENSIONS (FOR OPTIONAL INPUTS) AND VALIDATION
    
    # Plate thickness check
    if web_plate_t < beam_w_t:
        web_plate_t = beam_w_t
        #logger.error("The length of the plate is more than the available depth of %2.2f mm " % (plate_len))
        
        logger.error(": Chosen web plate thickness is not sufficient" )
        logger.warning(" : Minimum required thickness %2.2f mm" % (beam_w_t))
    
    # Plate height check
    # Maximum/minimum plate height
    max_plate_height = beam_d - 2 * beam_f_t - 40;
    min_plate_height = web_min_h(shear_load,web_plate_fy,web_plate_t);
    min_plate_height = int(min_plate_height) /10 * 10 +10;
    min_plate_height = round(min_plate_height,3)
    
    # Height input and check
             
    if web_plate_l != 0:
        if web_plate_l > max_plate_height :
            logger.error(": Height of plate is more than the clear depth of the beam")
            logger.warning(": Maximum plate height allowed is %2.2f mm " % (max_plate_height))
            web_plate_l = max_plate_height ; 
              
        elif min_plate_height > max_plate_height:
            logger.error(": Minimum required plate height is more than the clear depth of the beam")
            logger.warning(": Plate height required should be more than  %2.2f mm " % (min_plate_height))
            logger.warning(": Maximum plate height allowed is %2.2f mm " % (max_plate_height))
            logger.info(": Increase the plate thickness")
            web_plate_l = max_plate_height;
            
        elif min_plate_height >= web_plate_l:
            
            logger.error(": Plate height provided is less than the minimum required ")
            logger.warning(": Plate height required should be more than  %2.2f mm " % (min_plate_height))
            
            web_plate_l = min_plate_height 
    else:
        if min_plate_height < max_plate_height:
            web_plate_l = min_plate_height +10
        elif min_plate_height >= max_plate_height:
            web_plate_l = (max_plate_height-10)//10*10 ;
        
    
    ########################################################################
    # Bolt design:
    
    # I: Check for number of bolts -------------------
    bolt_fu = int(bolt_grade) * 100
    bolt_fy = (bolt_grade - int(bolt_grade))*bolt_fu;
    
    t_thinner = min(beam_w_t.real,web_plate_t.real);
    bolt_shear_capacity = bolt_shear(bolt_dia,bolt_planes,bolt_fu).real;
    bolt_bearing_capacity = bolt_bearing(bolt_dia,t_thinner,beam_fu).real;
    
    bolt_capacity = min(bolt_shear_capacity, bolt_bearing_capacity);
    
    bolts_required = int(shear_load/bolt_capacity) + 1; 
    if bolts_required <= 2:
        bolts_required = 3;
    
    bolt_group_capacity = bolts_required * bolt_capacity;
    
    # Spacing of bolts for web plate -------------------
    if bolt_dia == 12 or bolt_dia == 14:
        dia_hole = bolt_dia + 1
    elif bolt_dia == 16 or bolt_dia == 18 or bolt_dia == 20 or bolt_dia == 22 or bolt_dia == 24:
        dia_hole = bolt_dia + 2
    else:
        dia_hole = bolt_dia + 3    

    # Minimum/maximum pitch and gauge
    min_pitch = int(2.5 * bolt_dia);
    min_gauge = int(2.5 * bolt_dia);
    
    if min_pitch%10 != 0 or min_gauge%10 != 0:
        min_pitch = (min_pitch/10)*10 + 10;
        min_gauge = (min_gauge/10)*10 + 10;
    else:
        min_pitch = min_pitch;
        min_gauge = min_gauge;
                            #clause 10.2.2 is800
    max_spacing = int(min(100 + 4 * t_thinner, 200));        #clause 10.2.3.3 is800
    
    min_edge_dist = int(1.5 * (dia_hole)) + 10;    # 10 mm added than min. value
    if min_edge_dist%10 != 0:
        min_edge_dist = (min_edge_dist/10)*10 + 10;
    else:
        min_edge_dist = min_edge_dist;
        
    max_edge_dist = int((12 * t_thinner * cmath.sqrt(250/beam_fy)).real)-1;

    # Determine single or double line of bolts
    
    length_avail = (web_plate_l-2*min_edge_dist);
    pitch = round(length_avail/(bolts_required-1),3);
    
    
    
    ## Calculation of moment demand
    
    M1 = bolt_shear_capacity * (20+min_edge_dist/2);
    # Single line of bolts
    if pitch >= min_pitch:
        bolt_line =1;
        gauge = 0;
        bolts_one_line = bolts_required;
        K = bolts_one_line / 2;
        M2=0;
        if bolts_required % 2 ==0 or bolts_required % 2 !=0:
            for k in range (0,K):
                M2 = M2 + 2*(bolt_shear_capacity * ((length_avail/2 - k * pitch)**2/(length_avail/2 - k * pitch)));
            moment_demand = max(M1,M2);
            moment_demand =  round(moment_demand * 0.001,3)
    
    # Multi-line of bolts
    if pitch < min_pitch:
        bolt_line = 2;
        if bolts_required % 2 == 0:
            bolts_one_line = bolts_required/2;
        else:
            bolts_one_line = (bolts_required/2) + 1;
        
        pitch = round(length_avail/(bolts_one_line-1),3); 
        gauge = min_gauge;        
        M1 = bolt_shear_capacity * (20+ min_edge_dist + gauge/2);
        
        if pitch >= min_pitch:
            K = bolts_one_line / 2;
            M2=0;
            if bolts_required % 2 ==0 or bolts_required % 2 !=0:
                for k in range (0,K):
                    V = length_avail/2 - k * pitch
                    H = gauge/2;
                    d = math.sqrt(V**2 + H**2);
                    M2 = M2 + 2*(bolt_shear_capacity * (d**2/d));
                M2=M2*2;
                moment_demand = max(M1,M2);
                moment_demand =  round(moment_demand * 0.001,3)

    # Needs discussion with Sir
        else:
            logger.error(": Bolt strength is insufficient to carry the shear force")
            logger.warning (": Increase bolt diameter and/or bolt grade")
            moment_demand=0.0
    ####################################################################################
    # Design of plate:
    
    # Width input (optional) and validation
    if web_plate_w != 0:
        if bolt_line == 1:
                web_plate_w_req = 2 * min_edge_dist 
                end_dist = web_plate_w/2
        if bolt_line == 2:
                web_plate_w_req = gauge + 2 * min_edge_dist 
                end_dist = (web_plate_w - gauge)/2
            
    if web_plate_w == 0:   
        if bolt_line == 1:
            web_plate_w_req = 2 * min_edge_dist;
            web_plate_w = web_plate_w_req
            end_dist = web_plate_w /2
        if bolt_line == 2:
            web_plate_w_req = gauge + 2 * min_edge_dist;
            web_plate_w = web_plate_w_req;
            end_dist = (web_plate_w - gauge)/2

            
    # if web_plate_w < web_plate_w_req:
    #     web_plate_w = web_plate_w_req;
    
    # Moment capacity of web plate
    moment_capacity = 1.2 * (web_plate_fy/1.1) * (web_plate_t * web_plate_l * web_plate_l)/6 * 0.001;
    moment_capacity = round(moment_capacity * 0.001,3);
    
    if moment_capacity > moment_demand:
        pass
    else:
        logger.error(": Plate moment capacity is less than the moment demand")
        
        logger.warning(": Re-design with increased plate dimensions")
        
        
    # Plate dimension optimisation 
    
    web_plate_l_req1 = math.sqrt((moment_demand*1000*6*1.1)/(1.2*beam_fy*web_plate_t));
    # Single line of bolts
    if bolt_line == 1:
        web_plate_l_req2 = (bolts_required-1) * min_pitch + 2 * min_edge_dist;
        if web_plate_l == 0 or web_plate_l == min_plate_height or web_plate_l == max_plate_height:
            web_plate_l_req = max(web_plate_l_req1, web_plate_l_req2, web_plate_l);
        else:
            web_plate_l_req = max(web_plate_l_req1, web_plate_l_req2,min_plate_height);

    # Multi line of bolts
    if bolt_line == 2:
        web_plate_l_req2 = (bolts_one_line-1) * min_pitch + 2 * min_edge_dist;
    
        if web_plate_l == 0 or web_plate_l == min_plate_height or web_plate_l == max_plate_height:
            web_plate_l_req = max(web_plate_l_req1, web_plate_l_req2, web_plate_l);
        elif web_plate_l > min_plate_height or web_plate_l < max_plate_height:
            web_plate_l_req = max(web_plate_l_req1, web_plate_l_req2, min_plate_height);
    
    if web_plate_l != min_plate_height +10 or web_plate_l != (max_plate_height-10)//10*10 :
        pass
    else:
        if web_plate_l < web_plate_l_req:
            logger.error(": Plate height provided is less than the minimum required")
            
    if web_plate_w < web_plate_w_req: 
           
        logger.error(": Plate width provided is less than the minimum required")
        logger.warning(": Minimum plate width required is %2.2f mm " %(web_plate_w_req))
        
    ##################################################################################
    ## Weld design
    # V: Weld shear strength -------------------
    weld_l = web_plate_l - weld_t * 2;
    
    #direct shear
    Vy1 = shear_load *1000 /float(2*weld_l);        
    
    #shear due to moment
    xCritical = 0;                    #single line weld
    yCritical = weld_l * 0.5;        #single line weld
    
    Ip = weld_l * weld_l * weld_l / 12;
    
    Vx = moment_demand * yCritical *1000000 / (2 * Ip);
    Vy2 = moment_demand * xCritical * 1000000 / (2 * Ip);
    
    Vr = math.sqrt(Vx ** 2 + (Vy1 + Vy2) ** 2);
    Vr = round(Vr,3);
    
    weld_strength = 0.7 * weld_t * weld_fu / (math.sqrt(3) * 1.25);
    weld_strength = round(weld_strength,3);
    
    weld_t_req = (Vr * (math.sqrt(3) * 1.25))/(0.7 * weld_fu) ;
    
    if weld_t_req != int(weld_t_req):
        weld_t_req = int(weld_t_req) + 1;
    else:
        weld_t_req = weld_t_req;
    
    if weld_t >= weld_t_req:
        pass
    else:
        logger.error(": Weld thickness is not sufficient")
        logger.warning(": Minimum weld thickness is required is %2.2f mm " % (weld_t_req))
    
    # End of calculation
    outputObj = {}
    outputObj['Bolt'] ={}
    outputObj['Bolt']['status'] = True
    outputObj['Bolt']['shearcapacity'] = bolt_shear_capacity
    outputObj['Bolt']['bearingcapacity'] = bolt_bearing_capacity
    outputObj['Bolt']['boltcapacity'] = bolt_capacity
    outputObj['Bolt']['numofbolts'] = bolts_required
    outputObj['Bolt']['boltgrpcapacity'] = bolt_group_capacity
    outputObj['Bolt']['numofrow'] = bolts_one_line
    outputObj['Bolt']['numofcol'] = bolt_line
    outputObj['Bolt']['pitch'] = pitch
    outputObj['Bolt']['enddist'] = float(end_dist)
    outputObj['Bolt']['edge'] = float(min_edge_dist)
    outputObj['Bolt']['gauge'] = float(gauge)
     
    outputObj['Weld'] = {}
    outputObj['Weld']['thickness'] = weld_t_req
    outputObj['Weld']['resultantshear'] = Vr
    outputObj['Weld']['weldstrength'] = weld_strength
     
    outputObj['Plate'] = {}
    outputObj['Plate']['minHeight'] = web_plate_l_req
    outputObj['Plate']['minWidth'] = web_plate_w_req
    outputObj['Plate']['externalmoment'] = moment_demand
    outputObj['Plate']['momentcapacity'] = moment_capacity
    outputObj['Plate']['height'] = float(web_plate_l)
    outputObj['Plate']['width'] = float(web_plate_w)
    
    
    #return outputObj
    
    if web_plate_l == (min_plate_height+10) or web_plate_l == ((max_plate_height-10)//10*10):
        if bolt_line==1:
            if web_plate_l == min_plate_height or web_plate_l == max_plate_height or web_plate_l < web_plate_l_req or web_plate_w < web_plate_w_req or weld_t_req > weld_t:
                for k in outputObj.keys():
                    for key in outputObj[k].keys():
                        outputObj[k][key] = ""
            elif moment_capacity < moment_demand:
                for k in outputObj.keys():
                    for key in outputObj[k].keys():
                        outputObj[k][key] = ""
        
        if bolt_line==2:
            if pitch < min_pitch:
                for k in outputObj.keys():
                    for key in outputObj[k].keys():
                        outputObj[k][key] = ""
            elif web_plate_l == min_plate_height or web_plate_l == max_plate_height or web_plate_l < web_plate_l_req or web_plate_w < web_plate_w_req or weld_t_req > weld_t:
                for k in outputObj.keys():
                    for key in outputObj[k].keys():
                        outputObj[k][key] = ""
            elif moment_capacity < moment_demand:
                for k in outputObj.keys():
                    for key in outputObj[k].keys():
                        outputObj[k][key] = ""
        else:
            
            pass
        
    else:
        if web_plate_l == min_plate_height or web_plate_l == max_plate_height or web_plate_l < web_plate_l_req or web_plate_w < web_plate_w_req or weld_t_req > weld_t:
            for k in outputObj.keys():
                for key in outputObj[k].keys():
                    outputObj[k][key] = ""
        elif moment_capacity < moment_demand:
            for k in outputObj.keys():
                for key in outputObj[k].keys():
                    outputObj[k][key] = ""
        elif bolt_line==2:
            if pitch < min_pitch:
                for k in outputObj.keys():
                    for key in outputObj[k].keys():
                        outputObj[k][key] = ""
                        
#     outputObj = {}
    if  outputObj['Bolt']['status'] == True:
        
        logger.info(": Overall finplate connection design is safe \n")
        logger.debug(" :=========End Of design===========")
        
    else:
        logger.error(": Design is not safe \n ")
        logger.debug(" :=========End Of design===========")
    
    return outputObj
    





