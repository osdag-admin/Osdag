.. Help_Design_Examples documentation master file, created by
   sphinx-quickstart on Mon Jun 12 15:06:32 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. image::   website_header.png
	:target: http://osdag.fossee.in/
	


Welcome to Osdag help!
================================================

Osdag is a cross-platform free and open-source software for the design and detailing of steel structures, following relevant Indian Standards. Osdag is primarily built upon Python and other Python-based FOSS tools, such as, PyQt, OpenCascade, PythonOCC, SQLite, etc. It is developed by the Osdag team at IIT Bombay.
 |

The OSI file of a sample design can be loaded through the ``File -> Load input`` option of the appropriate module.

.. note:: The examples highlighted inside a box are from the **Release 2018-06-21**  and older versions of Osdag. Please use the examples with the appropriate version of Osdag.
|


**************************
Osdag Homepage_.
**************************

***********************
1.  **Connection**
***********************

1.1. *Shear Connection*
#######################

1.1.1. Fin Plate
****************************

1.1.1.1 Column Flange-Beam Web (CFBW) connectivity

      **Sample Problem 1**

         Design a *Fin Plate* connection for a beam *MB 350* connected to a column *HB 450* to transfer a factored shear force of **180 kN** and an axial force of **50 kN**.
         The grade of the beam and the column material is **E 250 (Fe 410 W)A** respectively.

         Perform an *optimum design* by adopting the following design specifications:

         - **Bolt type:** Friction grip (HSFG); Diameter: 12, 16, 20, 24, 30; Grade: 4.6, 4.8, 5.6, 6.8, 8.8
         - **Plate:** Material E 350 (Fe 490); Thickness (mm): 10, 12, 16, 18, 20
         - Bolt hole type is standard and slip factor is 0.3
         - The plate edges are machine-flame cut
         - Gap between the members is 15 mm

      **Download:**

      DesignReport_1.1.1.1.1.pdf_.
	
      Example_1.1.1.1.1.osi_.

--------------------------------------------------------------------------------------------------------------------------
 
      **Sample Problem 2**

         Design a *Fin Plate* connection for a beam *WB 300* connected to a column *PBP 300 X 88.48* to transfer a factored shear force of **175 kN** and an axial force of **35 kN**.
         The grade of the beam and the column material is **E 300 (Fe 440)** respectively.

         Perform a *design check* by adopting the following design specifications:

         - **Bolt type:** Bearing bolt; Diameter: 20; Grade: 6.8
         - **Plate:** Material E 250 (Fe 410 W)A; Thickness (mm): 14
         - Bolt hole type is standard
         - The plate edges are hand flame cut
         - Gap between the members is 10 mm

      **Download:**

      DesignReport_1.1.1.1.2.pdf_.

      Example_1.1.1.1.2.osi_.

--------------------------------------------------------------------------------------------------------------------------
 
1.1.1.2. Column Web-Beam Web (CWBW) connectivity

      **Sample Problem 1**

         Design a *Fin Plate* connection for a beam *NPB 350 X 250 X 79.18* connected to a column *PBP 400 X 230.9* to transfer a factored shear force of **225 kN** and an axial force of **100 kN**.
         The grade of the beam and the column material is **E 350 (Fe 410 W)A** respectively.

         Perform an *optimum design* by adopting the following design specifications:

         - **Bolt type:** Bearing bolt; Diameter: 12, 16, 20, 24 ; Grade: 4.6, 8.8, 10.9
         - **Plate:** Material E 250 (Fe 410 W)A; Thickness (mm): 12, 14, 16, 18, 20, 22, 25
         - Bolt hole type is over-sized
         - The ultimate strength of the weld material is, f\ :sub:`u` = 510 MPa
         - The plate edges are machine-flame cut
         - Gap between the members is 12 mm

      **Download:**

      DesignReport_1.1.1.2.1.pdf_.

      Example_1.1.1.2.1.osi_.

--------------------------------------------------------------------------------------------------------------------------

      **Sample Problem 2**

         Design a *Fin Plate* connection for a beam *WPB 300 X 300 X 100.85* connected to a column *UC 356 X 368 X 129* to transfer a factored shear force of **140 kN**.
         The grade of the beam and the column material is **E 250 (Fe 410 W)A** respectively.

         Perform a *design check* by adopting the following design specifications:

         - **Bolt type:** Bearing bolt; Diameter: 16; Grade: 4.6
         - **Plate:** Material E 250 (Fe 410 W)A; Thickness (mm): 16
         - Bolt hole type is standard
         - The plate edges are machine-flame cut
         - Gap between the members is 10 mm

      **Download:**

      DesignReport_1.1.1.2.2.pdf_.

      Example_1.1.1.2.2.osi_.

--------------------------------------------------------------------------------------------------------------------------

1.1.1.3. Beam-Beam (BB) connectivity

      **Sample Problem 1**
    
         Design a *Fin Plate* connection for a primary beam *WB 400* connected to a secondary beam *MB 300* to transfer a factored shear force of **160 kN** and an axial force of **20 kN**.
         The grade of the primary and secondary beam material is **E 300 (Fe 440)** respectively.

         Perform an *optimum design* by adopting the following design specifications:

         - **Bolt type:** Friction grip (HSFG); Diameter: 16, 20, 24 ; Grade: 8.8, 10.9
         - **Plate:** Material E 250 (Fe 410 W)A; Thickness (mm): 16, 18, 20, 22
         - Bolt hole type is standard
         - Surface treatment: Sand blast (slip factor = 0.48)
         - The plate edges are machine-flame cut
         - Gap between the members is 5 mm

      **Download:**

      DesignReport_1.1.1.3.1.pdf_.
	
      Example_1.1.1.3.1.osi_.

--------------------------------------------------------------------------------------------------------------------------

      **Sample Problem 2**

         Design a *Fin Plate* connection for a primary beam *UB 305 x 102 x 33* connected to a secondary beam *MB 300* to transfer a factored shear force of **100 kN**.
         The grade of the primary and secondary beam material is **E 250 (Fe 410 W)A** respectively.

         Perform a *design check* by adopting the following design specifications:

         - **Bolt type:** Bearing bolt; Diameter: 16; Grade: 5.8
         - **Plate:** Material E 250 (Fe 410 W)A; Thickness (mm): 14
         - Bolt hole type is over-sized
         - The ultimate strength of the weld material is, f\ :sub:`u` = 450 MPa
         - The plate edges are hand flame cut
         - Gap between the members is 10 mm

      **Download:**

      DesignReport_1.1.1.3.2.pdf_.

      Example_1.1.1.3.2.osi_.

.. note:: Example for **Release 2018-06-21**  and lower versions - Fin Plate

   1.1.1.1 Column Flange-Beam Web (CFBW) connectivity

      **Sample Problem 1**

         Design a fin plate connection between a beam MB 500 and a column UC 305 x 305 x 97 for transferring a vertical (factored) shear force of 140 kN. Use M24 Friction grip bolts of grade 8.8. Try 12mm thick fin plate with weld thickness of 12mm. Take Fe410 grade steel (fy = 250 MPa, fu = 410 MPa). Assume bolt hole type as standard, weld type as shop weld and type of edge as hand flame cut.

      **Download:**

      Design_Report_1.1.1.1.1.pdf_.

      Design_Example_1.1.1.1.1.osi_.


      **Sample Problem 2**

         Design a fin plate connection between a beam MB 350 and a column SC 200 for transferring a vertical (factored) shear force of 150 kN. Use M20 bearing bolts of grade 4.6. Try 12mm thick fin plate with weld thickness of 8mm. Take Fe410 grade steel (fy = 250 MPa, fu = 410 MPa). Assume weld type as shop weld and type of edge as machine flame cut.

      **Download:**

      Design_Report_1.1.1.1.2.pdf_.

      Design_Example_1.1.1.1.2.osi_.

--------------------------------------------------------------------------------------------------------------------------

.. note:: Example for **Release 2018-06-21**  and lower versions - Fin Plate

   1.1.1.2. Column Web-Beam Web (CWBW) connectivity

      **Sample Problem 1**

         Design a fin plate connection between a beam UB 356 x 171 x 45 and a column PBP 300 x 180 for transferring a vertical (factored) shear force of 120 kN. Use M16 Friction grip bolts of grade 8.8. Try 8mm thick fin plate with weld thickness of 8mm. Take Fe410 grade steel (fy = 250 MPa, fu = 410 MPa). Assume bolt hole type as standard, slip factor of 0.25, type of weld as field weld and edge as hand flame cut.

      **Download:**

      Design_Report_1.1.1.2.1.pdf_.

      Design_Example_1.1.1.2.1.osi_.


      **Sample Problem 2**

         Design a fin plate connection between a beam LB 300 and a column SC 250 for transferring a vertical (factored) shear force of 135 kN. Use M24 bearing bolts of grade 4.8. Try 10mm thick fin plate with weld thickness of 8mm. Take Fe410 grade steel fy = 250 MPa, fu = 410 MPa). Assume bolt hole type as standard, type of weld as shop weld and edge as hand flame cut and environment as corrosive.

      **Download:**

      Design_Report_1.1.1.2.2.pdf_.

      Design_Example_1.1.1.2.2.osi_.

--------------------------------------------------------------------------------------------------------------------------

.. note:: Example for **Release 2018-06-21**  and lower versions - Fin Plate

   1.1.1.3. Beam-Beam (BB) connectivity

      *Sample Problem 1*

         Design a fin plate connection between a primary beam MB 350 and a secondary beam NPB 270 x 135 x 36.1 for transferring a vertical (factored) shear force of 110 kN. Use M20 Friction grip bolts of grade 10.9. Try 10mm thick fin plate with weld thickness of 8mm. Take Fe410 grade steel (fy = 250 MPa, fu = 410 MPa). Assume slip factor of 0.52, bolt hole type oversized and type of edge as machine flame cut.

      **Download:**

      Design_Report_1.1.1.3.1.pdf_.

      Design_Example_1.1.1.3.1.osi_.


      **Sample Problem 2**

         Design a fin plate connection between a primary beam WPB 450 x 300 x 99.7 and a secondary beam UB 356 x 171 x 67 for transferring a vertical (factored) shear force of 220 kN. Use M24 Friction grip bolts of grade 10.9. Try 14mm thick fin plate with weld thickness of 12mm. Take Fe410 grade steel (fy = 250 MPa, fu = 410 MPa). Assume slip factor of 0.48, bolt hole type standard, weld type as shop weld and type of edge as machine flame cut.

      **Download:**

      Design_Report_1.1.1.3.2.pdf_.

      Design_Example_1.1.1.3.2.osi_.

1.1.2. End Plate
****************************

1.1.2.1. Column Flange-Beam Web (CFBW) connectivity

      **Sample Problem 1**

         Design an *End Plate* connection for a beam *LB 400* connected to a column *PBP 300 X 109.54* to transfer a factored shear force of **240 kN** and an axial force of **125 kN**.
         The grade of the beam and the column material are **E 250 (Fe 410 W)A** and **E 350 (Fe 490)** respectively.

         Perform an *optimum design* by adopting the following design specifications:

         - **Bolt type:** Bearing bolt; Diameter: 16, 20, 24, 30; Grade: 4.8, 5.6, 6.8, 9.8
         - **Plate:** Material E 250 (Fe 410 W)A; Thickness (mm): 14, 16, 18, 20, 22, 25, 28
         - Bolt hole type is standard
         - The plate edges are machine-flame cut

      **Download:**

      DesignReport_1.1.2.1.1.pdf_.

      Example_1.1.2.1.1.osi_.

--------------------------------------------------------------------------------------------------------------------------

      **Sample Problem 2**

         Design an *End Plate* connection for a beam *UB 356 x 127 x 39* connected to a column *UB 254 x 254 x 89* to transfer a factored shear force of **250 kN** and an axial force of **80 kN**.
         The grade of the beam and the column material is **E 300 (Fe 440)** respectively.

         Perform a *design check* by adopting the following design specifications:

         - **Bolt type:** Friction grip (HSFG); Diameter: 24; Grade: 8.8
         - **Plate:** Material E 250 (Fe 410 W)A; Thickness (mm): 18
         - Bolt hole type is standard and slip factor is 0.25
         - The plate edges are hand flame cut

      **Download:**

      DesignReport_1.1.2.1.2.pdf_.

      Example_1.1.2.1.2.osi_.

--------------------------------------------------------------------------------------------------------------------------

1.1.2.2. Column Web-Beam Web (CWBW) connectivity

      **Sample Problem 1**

         Design an *End Plate* connection for a beam *WB 300* connected to a column *HB 350* to transfer a factored shear force of **220 kN** and an axial force of **30 kN**.
         The grade of the beam and the column material is **E 250 (Fe 410 W)A**.

         Perform an *optimum design* by adopting the following design specifications:

         - **Bolt type:** Bearing bolt; Diameter: 16, 20, 24; Grade: 4.6, 4.8, 5.6, 5.8
         - **Plate:** Material E 250 (Fe 410 W)A; Thickness (mm): 14, 16, 20
         - Bolt hole type is over-sized
         - The ultimate strength of the weld material is, f\ :sub:`u` = 500 MPa
         - The plate edges are machine-flame cut

      **Download:**

      DesignReport_1.1.2.2.1.pdf_.

      Example_1.1.2.2.1.osi_.

--------------------------------------------------------------------------------------------------------------------------

      **Sample Problem 2**

         Design an *End Plate* connection for a beam *MB 400* connected to a column *HB 350* to transfer a factored shear force of **275 kN**.
         The grade of the beam and the column material is **E 300 (Fe 440)** respectively.

         Perform a *design check* by adopting the following design specifications:

         - **Bolt type:** Bearing bolt; Diameter: 20; Grade: 9.8
         - **Plate:** Material E 250 (Fe 410 W)A; Thickness(mm): 20
         - Bolt hole type is standard
         - The plate edges are are machine-flame cut

      **Download:**

      DesignReport_1.1.2.2.2.pdf_.

      Example_1.1.2.2.2.osi_.

--------------------------------------------------------------------------------------------------------------------------

1.1.2.3. Beam-Beam (BB) connectivity

      **Sample Problem 1**

         Design an *End Plate* connection for a primary beam *WB 400* connected to a secondary beam *MB 300* to transfer a factored shear force of **160 kN** and an axial force of **20 kN**.
         The grade of the primary and secondary beam material is **E 300 (Fe 440)** respectively.

         Perform an *optimum design* by adopting the following design specifications:

         - **Bolt type:** Friction grip (HSFG); Diameter: 16, 20, 24 ; Grade: 8.8, 10.9
         - **Plate:** Material E 250 (Fe 410 W)A; Thickness (mm): 16, 18, 20, 22
         - Bolt hole type is standard
         - Surface treatment: Sand blast (slip factor = 0.48)
         - The plate edges are machine-flame cut

      **Download:**

      DesignReport_1.1.2.3.1.pdf_.

      Example_1.1.2.3.1.osi_.

--------------------------------------------------------------------------------------------------------------------------

      **Sample Problem 2**

         Design an *End Plate* connection for a primary beam *UB 305 x 102 x 33* connected to a secondary beam *MB 300* to transfer a factored shear force of **100 kN**.
         The grade of the primary and secondary beam material is **E 250 (Fe 410 W)A** respectively.

         Perform a *design check* by adopting the following design specifications:

         - **Bolt type:** Bearing bolt; Diameter: 16; Grade: 5.8
         - **Plate:** Material E 250 (Fe 410 W)A; Thickness (mm): 14
         - Bolt hole type is over-sized
         - The ultimate strength of the weld material is, f\ :sub:`u` = 450 MPa
         - The plate edges are hand flame cut

      **Download:**

      DesignReport_1.1.2.3.2.pdf_.

      Example_1.1.2.3.2.osi_.

.. note:: Example for **Release 2018-06-21** and lower versions - End Plate

   1.1.2.1. Column Flange-Beam Web (CFBW) connectivity

      **Sample Problem 1**

         Design an end plate connection between a beam MB 350 and a column SC 250 for transferring a vertical (factored) shear force of 140 kN. Use M20 bearing bolts of grade 4.6. Try 10mm thick end plate with weld thickness of 6mm. Take Fe410 grade steel (fy = 250 MPa, fu = 410 MPa). Assume bolt hole type as standard, weld type shop weld and type of edge as hand flame cut.
      **Download:**

      Design_Report_1.1.2.1.1.pdf_.

      Design_Example_1.1.2.1.1.osi_.


      **Sample Problem 2**

         Design an end plate connection between a beam MB 300 and a column UC 254 x254 x 107 for transferring a vertical (factored) shear force of 195 kN. Use M16 Friction grip bolts of grade 8.8. Try 12mm thick end plate with weld thickness of 10mm. Take Fe410 grade steel (fy = 250 MPa, fu = 410 MPa). Assume bolt hole type as standard, weld type shop weld and type of edge as machine flame cut.

      **Download:**

      Design_Report_1.1.2.1.2.pdf_.

      Design_Example_1.1.2.1.2.osi_.

--------------------------------------------------------------------------------------------------------------------------

.. note:: Example for **Release 2018-06-21** and lower versions - End Plate

   1.1.2.2. Column Web-Beam Web (CWBW) connectivity

      **Sample Problem 1**

         Design an end plate connection between a beam UB 356 x 171 x 45 and a column PBP 300 x 180 for transferring a vertical (factored) shear force of 120 kN. Use M16 Friction grip bolts of grade 10.9. Try 12mm thick end plate with weld thickness of 6mm. Take Fe410 grade steel (fy = 250 MPa, fu = 410 MPa). Assume bolt hole type as standard, slip factor of 0.25, type of weld as field weld and edge type as hand flame cut.

      **Download:**

      Design_Report_1.1.2.2.1.pdf_.

      Design_Example_1.1.2.2.1.osi_.


      **Sample Problem 2**

         Design an end plate connection between a beam LB 300 and a column SC 250 for transferring a vertical (factored) shear force of 135 kN. Use M12 bearing bolts of grade 4.8. Try 10mm thick end plate with weld thickness of 10mm. Take Fe410 grade steel (fy = 250 MPa, fu = 410 MPa). Assume bolt hole type as standard, type of weld as shop weld and edge type as hand flame cut.

      **Download:**

      Design_Report_1.1.2.2.2.pdf_.

      Design_Example_1.1.2.2.2.osi_.

--------------------------------------------------------------------------------------------------------------------------

.. note:: Example for **Release 2018-06-21** and lower versions - End Plate

   1.1.2.3. Beam-Beam (BB) connectivity

      **Sample Problem 1**

         Design an end plate connection between a primary beam MB 500 and a secondary beam MB 400 for transferring a vertical (factored) shear force of 160 kN. Use M20 Friction grip bolts of grade 8.8. Try 16mm thick end plate with weld thickness of 8mm. Take Fe410 grade steel (fy = 250 MPa, fu = 410 MPa). Assume slip factor of 0.2, bolt hole type as oversized, weld type shop weld and type of edge as machine flame cut.

      **Download:**

      Design_Report_1.1.2.3.1.pdf_.

      Design_Example_1.1.2.3.1.osi_.


      **Sample Problem 2**

         Design an end plate connection between a primary beam WPB 450 x 300 x 99.7 and a secondary beam UB 356 x 171 x 67 for transferring a vertical (factored) shear force of 220 kN. Use M24 Friction grip bolts of grade 10.9. Try 14mm thick end plate with weld thickness of 12mm. Take Fe410 grade steel (fy = 250 MPa, fu = 410 MPa). Assume slip factor of 0.48, bolt hole type as standard, weld type shop weld and type of edge as machine flame cut.

      **Download:**

      Design_Report_1.1.2.3.2.pdf_.

      Design_Example_1.1.2.3.2.osi_.


1.1.3. Cleat Angle
*******************************

1.1.3.1. Column Flange-Beam Web (CFBW) connectivity

      **Sample Problem 1**

         Design a *Cleat Angle* connection for a beam *MB 300* connected to a column *HB 250* to transfer a factored shear force of **130 kN**.
         The grade of the beam and the column material is **E 250 (Fe 410 W)A** respectively.

         Perform an *optimum design* by adopting the following design specifications:

         - **Bolt type:** Bearing bolt; Diameter: 16, 20; Grade: 4.6, 4.8
         - **Angle:** Material E 250 (Fe 410 W)A; Designation: 90 x 90 x 10, 90 x 90 x 12, 100 x 100 x 6, 100 x 100 x 8
         - Bolt hole type is standard
         - The plate edges are machine-flame cut

      **Download:**

      DesignReport_1.1.3.1.1.pdf_.

      Example_1.1.3.1.1.osi_.

--------------------------------------------------------------------------------------------------------------------------

      **Sample Problem 2**

         Design a *Cleat Angle* connection for a beam *MB 450* connected to a column *UC 305 x 305 x 118* to transfer a factored shear force of **240 kN**.
         The grade of the beam and the column material is **E 300 (Fe 440)** respectively.

         Perform a *design check* by adopting the following design specifications:

         - **Bolt type:** Friction grip (HSFG); Diameter: 20; Grade: 12.9
         - **Cleat Angle:** Material E 250 (Fe 410 W)A; Designation: 120 x 120 x 8
         - Bolt hole type is standard
         - Surface treatment: Clean mill scale (slip factor = 0.33)
         - The plate edges are machine-flame cut

      **Download:**

      DesignReport_1.1.3.1.2.pdf_.

      Example_1.1.3.1.2.osi_.

--------------------------------------------------------------------------------------------------------------------------

1.1.3.2. Column Web-Beam Web (CWBW) connectivity

      **Sample Problem 1**

         Design a *Cleat Angle* connection for a beam *WPB 250 X 250 X 85.4* connected to a column *PBP 300 X 95* to transfer a factored shear force of **170 kN**.
         The grade of the beam and the column material is **E 250 (Fe 410 W)A** respectively.

         Perform an *optimum design* by adopting the following design specifications:

         - **Bolt type:** Bearing bolt; Diameter: 16, 20, 24; Grade: 6.8, 8.8, 98
         - **Angle:** Material E 250 (Fe 410 W)A; Designation: All the sections available with the Osdag database
         - Bolt hole type is standard
         - The plate edges are machine-flame cut

      **Download:**

      DesignReport_1.1.3.2.1.pdf_.

      Example_1.1.3.2.1.osi_.

--------------------------------------------------------------------------------------------------------------------------

      **Sample Problem 2**

         Design a *Cleat Angle* connection for a beam *MB 450* connected to a column *UC 305 x 305 x 118* to transfer a factored shear force of **240 kN**.
         The grade of the beam and the column material is **E 300 (Fe 440)** respectively.

         Perform a *design check* by adopting the following design specifications:

         - **Bolt type:** Friction grip (HSFG); Diameter: 20; Grade: 12.9
         - **Cleat Angle:** Material E 250 (Fe 410 W)A; Designation: 80 x 80 x 8
         - Bolt hole type is standard
         - Surface treatment: Clean mill scale (slip factor = 0.33)
         - The plate edges are machine-flame cut
 
      **Download:**

      DesignReport_1.1.3.2.2.pdf_.

      Example_1.1.3.2.2.osi_.

--------------------------------------------------------------------------------------------------------------------------

1.1.3.3. Beam-Beam (BB) connectivity

      **Sample Problem 1**
    
         Design a *Cleat Angle* connection for a primary beam *WB 400* connected to a secondary beam *MB 300* to transfer a factored shear force of **160 kN**.
         The grade of the primary and secondary beam material is **E 300 (Fe 440)** respectively.

         Perform an *optimum design* by adopting the following design specifications:

         - **Bolt type:** Friction grip (HSFG); Diameter: 16, 20, 24 ; Grade: 8.8, 12.9
         - **Cleat Angle:** Material E 165 (Fe 290); Designation: 80 x 80 x 8, 90 x 90 x 6, 90 x 90 x 8, 90 x 90 x 10, 90 x 90 x 12, 100 x 100 x 8, 100 x 100 x 10, 110 x 110 x 10
         - Bolt hole type is standard
         - Surface treatment: Sand blast (slip factor = 0.48)
         - The plate edges are machine-flame cut
	 
      **Download:**

      DesignReport_1.1.3.3.1.pdf_.

      Example_1.1.3.3.1.osi_.

--------------------------------------------------------------------------------------------------------------------------

      **Sample Problem 2**
        
         Design a *Cleat Angle* connection for a primary beam *UB 305 x 102 x 33* connected to a secondary beam *MB 300* to transfer a factored shear force of **100 kN**.
         The grade of the primary and secondary beam material is **E 250 (Fe 410 W)A** respectively.

         Perform a *design check* by adopting the following design specifications:

         - **Bolt type:** Bearing bolt; Diameter: 16; Grade: 5.8
         - **Cleat Angle:** Material E 250 (Fe 410 W)A; Designation: 130 x 130 x 10
         - Bolt hole type is over-sized
         - The plate edges are hand flame cut

      **Download:**

      DesignReport_1.1.3.3.2.pdf_.

      Example_1.1.3.3.2.osi_.

.. note:: Examples for **Release 2018-06-21** and lower versions - Cleat Angle

   1.1.3.1. Column Flange-Beam Web (CFBW) connectivity

      **Sample Problem 1**

         Design a cleat angle connection between a beam MB 400 and a column SC 250 for transferring a vertical (factored) shear force of 140 kN. Use M20 Friction grip bolts of grade 8.8. Try cleat angle of size 90 x 90 x 12. Take Fe410 grade steel (fy = 250 MPa, fu = 410 MPa). Assume slip factor of 0.48, bolt hole type as standard and type of edge as hand flame cut.
      **Download:**

      Design_Report_1.1.3.1.1.pdf_.

      Design_Example_1.1.3.1.1.osi_.


      **Sample Problem 2**

         Design a cleat angle connection between a beam MB 350 and a column HB 300 for transferring a vertical (factored) shear force of 170 kN. Use M16 bearing bolts of grade 4.6. Try cleat angle of size 100 x 100 x 12. Take Fe410 grade steel (fy = 250 MPa, fu = 410 MPa). Assume bolt hole type as standard, type of edge as machine flame cut and environment as corrosive.

      **Download:**

      Design_Report_1.1.3.1.2.pdf_.

      Design_Example_1.1.3.1.2.osi_.

--------------------------------------------------------------------------------------------------------------------------

.. note:: Examples for **Release 2018-06-21** and lower versions - Cleat Angle

   1.1.3.2. Column Web-Beam Web (CWBW) connectivity

      **Sample Problem 1**

         Design a cleat angle connection between a beam MB 350 and a column UC 305 x 305 x 97 for transferring a vertical (factored) shear force of 120.5 kN. Use M20 Friction grip bolts of grade 8.8. Try cleat angle of size 110 x 110 x 16. Take Fe410 grade steel (fy = 250 MPa, fu = 410 MPa). Assume bolt hole type as standard, slip factor of 0.2, type of edge as hand flame cut and gap between column and beam as 5mm.

      **Download:**

      Design_Report_1.1.3.2.1.pdf_.

      Design_Example_1.1.3.2.1.osi_.


      **Sample Problem 2**

         Design a cleat angle connection between a beam MB 200 and a column UC 305 x 305 x 118 for transferring a vertical (factored) shear force of 80 kN. Use M12 bearing bolts of grade 6.8. Try cleat angle of size 110 x 110 x 16. Take Fe410 grade steel (fy = 250 MPa, fu = 410 MPa). Assume bolt hole type as standard, type of edge as hand flame cut and environment as corrosive.

      **Download:**

      Design_Report_1.1.3.2.2.pdf_.

      Design_Example_1.1.3.2.2.osi_.

--------------------------------------------------------------------------------------------------------------------------

.. note:: Examples for **Release 2018-06-21** and lower versions - Cleat Angle

   1.1.3.3. Beam-Beam (BB) connectivity

      **Sample Problem 1**

         Design a cleat angle connection between a primary beam WB 450 and a secondary beam MB 400 for transferring a vertical (factored) shear force of 145 kN. Use M24 bearing bolts of grade 4.6. Try cleat angle of size 100 100 x 10. Take Fe410 grade steel (fy = 250 MPa, fu = 410 MPa). Assume bolt hole type as standard and type of edge as hand flame cut.

      **Download:**

      Design_Report_1.1.3.3.1.pdf_.

      Design_Example_1.1.3.3.1.osi_.


      **Sample Problem 2**

         Design a cleat angle connection between a primary beam WPB 280x280x61.2 and a secondary beam NPB 220x110x29.4 for transferring a vertical (factored) shear force of 100 kN. Use M20 Friction grip bolts of grade 10.9. Try cleat angle of size 100 100 x 8. Take Fe410 grade steel (fy = 250 MPa, fu = 410 MPa). Assume bolt hole type as oversized, slip factor of 0.52, type of edge as machine flame cut and gap between column and beam as 15mm.

      **Download:**

      Design_Report_1.1.3.3.2.pdf_.

      Design_Example_1.1.3.3.2.osi_.


1.1.4. Seated Angle
*******************************

1.1.4.1. Column Flange-Beam Flange (CFBF) connectivity

      **Sample Problem 1**

         Design a *Seated Angle* connection for a beam *WB 400* connected to a column *PBP 360 X 152.2* to transfer a factored shear force of **210 kN**.
         The grade of the beam and the column material is **E 250 (Fe 410 W)A** respectively.

         Perform an *optimum design* by adopting the following design specifications:

         - **Bolt type:** Bearing bolt; Diameter: 20, 24, 30; Grade: 4.6, 4.8, 5.6, 5.8, 6.8, 8.8, 9.8
         - **Seated Angle:** Material E 300 (Fe 440); Designation: All the sections available with the Osdag database
         - **Top Angle:** Material E 300 (Fe 440); Designation: All the sections available with the Osdag database
         - Bolt hole type is standard
         - The plate edges are machine-flame cut
         - Gap between the members is 10 mm
 
      **Download:**

      DesignReport_1.1.4.1.1.pdf_.

      Example_1.1.4.1.1.osi_.

--------------------------------------------------------------------------------------------------------------------------

      **Sample Problem 2**
	
         Design a *Seated Angle* connection for a beam *MB 500* connected to a column *UC 305 x 305 x 118* to transfer a factored shear force of **185 kN**.
         The grade of the beam and the column material is **E 300 (Fe 440)** respectively.

         Perform a *design check* by adopting the following design specifications:

         - **Bolt type:** Friction grip (HSFG); Diameter: 20; Grade: 12.9
         - **Seated Angle:** Material E 250 (Fe 410 W)A; Designation: 150 x 150 x 10
         - **Top Angle:** Material E 250 (Fe 410 W)A; Designation: 150 x 150 x 10
         - Bolt hole type is standard
         - Surface treatment: Blasted with short or grit, loose rust removed (slip factor = 0.5)
         - The plate edges are machine-flame cut
         - Gap between the members is 10 mm
 
      **Download:**

      DesignReport_1.1.4.1.2.pdf_.

      Example_1.1.4.1.2.osi_.

--------------------------------------------------------------------------------------------------------------------------

1.1.4.2. Column Web-Beam Flange (CWBF) connectivity

      **Sample Problem 1**

         Design a *Seated Angle* connection for a beam *MB 400* connected to a column *HB 450* to transfer a factored shear force of **230 kN**.
         The grade of the beam and the column material is **E 250 (Fe 410 W)A** respectively.

         Perform an *optimum design* by adopting the following design specifications:

         - **Bolt type:** Bearing bolt; Diameter: 20, 24, 30; Grade: 4.6, 4.8, 5.6, 5.8, 6.8, 8.8, 9.8
         - **Seated Angle:** Material E 250 (Fe 410 W)A; Designation: All the sections available with the Osdag database
         - **Top Angle:** Material E 250 (Fe 410 W)A; Designation: All the sections available with the Osdag database
         - Bolt hole type is standard
         - The plate edges are machine-flame cut
         - Gap between the members is 10 mm

      **Download:**

      DesignReport_1.1.4.2.1.pdf_.

      Example_1.1.4.2.1.osi_.

--------------------------------------------------------------------------------------------------------------------------

      **Sample Problem 2**

         Design a *Seated Angle* connection for a beam *LB 325* connected to a column *UC 203 x 203 x 52* to transfer a factored shear force of **90 kN**.
         The grade of the beam and the column material is **E 300 (Fe 440)** respectively.

         Perform a *design check* by adopting the following design specifications:

         - **Bolt type:** Bearing bolt; Diameter: 16; Grade: 8.8
         - **Seated Angle:** Material E 250 (Fe 410 W)A; Designation: 90 x 90 x 10
         - **Top Angle:** Material E 250 (Fe 410 W)A; Designation: 80 x 80 x 10
         - Bolt hole type is standard
         - The plate edges are machine-flame cut
         - Gap between the members is 10 mm

      **Download:**

      DesignReport_1.1.4.2.2.pdf_.

      Example_1.1.4.2.2.osi_.

.. note:: Examples for **Release 2018-06-21** and lower versions - Seated Angle

   1.1.4.1. Column Flange-Beam Flange (CFBF) connectivity

      **Sample Problem 1**

         Design a seated angle connection between a beam MB 300 and a column UC 203 x 203 x 86 for transferring a vertical (factored) shear force of 100 kN. Use M20 Friction grip bolts of grade 10.9. Try a top angle of size 150 150 x 10 and seated angle of size 150 150 x 15. Take Fe410 grade steel (fy = 250 MPa, fu = 410 MPa). Assume slip factor of 0.55, bolt fu = 940 MPa and type of edge as hand flame cut.

      **Download:**

      Design_Report_1.1.4.1.1.pdf_.

      Design_Example_1.1.4.1.1.osi_.


      **Sample Problem 2**

         Design a seated angle connection between a beam MB 200 and a column SC 140 for transferring a vertical (factored) shear force of 140 kN. Use M12 bearing bolts of grade 6.8. Try a top angle of size 90 90 x 8 and seated angle of size 110 110 x 16. Take Fe410 grade steel (fy = 250 MPa, fu = 410 MPa). Assume type of edge as hand flame cut and environment as corrosive.

      **Download:**

      Design_Report_1.1.4.1.2.pdf_.

      Design_Example_1.1.4.1.2.osi_.

--------------------------------------------------------------------------------------------------------------------------

.. note:: Examples for **Release 2018-06-21** and lower versions - Seated Angle

   1.1.4.2. Column Web-Beam Flange (CWBF) connectivity

      **Sample Problem 1**

         Design a seated angle connection between a beam NPB 250x150x39.8 and a column PBP 300x180 for transferring a vertical (factored) shear force of 80 kN. Use M16 bearing bolts of grade 5.8. Try a top angle of size 90 90 x 10 and seated angle of size 150 150 x 15. Take Fe410 grade steel (fy = 250 MPa, fu = 410 MPa). Assume type of edge as machine flame cut.

      **Download:**

      Design_Report_1.1.4.2.1.pdf_.

      Design_Example_1.1.4.2.1.osi_.


      **Sample Problem 2**

         Design a seated angle connection between a beam WPB 140x140x24.7 and a column HB 200 for transferring a vertical (factored) shear force of 140 kN. Use M12 bearing bolts of grade 5.8. Try a top angle of size 90 90 x 10 and seated angle of size 150 150 x 15. Take Fe410 grade steel (fy = 250 MPa, fu = 410 MPa). Assume bolt hole type as Oversized, type of edge as machine flame cut and gap between column and beam as 5mm.

      **Download:**

      Design_Report_1.1.4.2.2.pdf_.

      Design_Example_1.1.4.2.2.osi_.


1.2. *Moment Connection*
#######################
1.2.1. Beam-to-Beam Splice Connection
*******************
1.2.1.1. Cover Plate Bolted
---------------------------------

      **Sample Problem 1**

         Design a *Beam-Beam Cover Plate Splice* connection for a beam *UB 610 x 305 x 179*. The grade of the beam material is **E 300 (Fe 440)**.

         The beam is subjected to the following loading condition;

         - **Bending Moment**: 300 kNm (reversible)

         - **Shear Force**: 160 kN

         - **Axial Force**: 40 kN

         Perform an *optimum design* by adopting the following design specifications:

         - **Bolt type:** Bearing bolt; Diameter: 20, 24, 30, 36; Grade: 6.8, 8.8, 9.8
         - **Flange Splice Plate:** Material E 250 (Fe 410 W)A; Preference: Outside; Thickness (mm): Most optimum from the available thicknesses in the Osdag database
         - **Web Splice Plate:** Material E 250 (Fe 410 W)A; Thickness (mm): Most optimum from the available thicknesses in the Osdag database
         - Bolt hole type is standard
         - The plate edges are machine-flame cut
         - Gap between the members is 0 mm

      **Download:**

      DesignReport_1.2.1.1.1.pdf_.

      Example_1.2.1.1.1.osi_.

--------------------------------------------------------------------------------------------------------------------------
	
      **Sample Problem 2**

         Design a *Beam-Beam Cover Plate Splice* connection for a beam *WPB 900 x 300 x 198.01*. The grade of the beam material is **E 350 (Fe 490)**.

         The beam is subjected to the following loading condition;

         - **Bending Moment**: 395 kNm (reversible)

         - **Shear Force**: 110 kN

         Perform a *design check* by adopting the following design specifications:

         - **Bolt type:** Bearing bolt; Diameter: 24; Grade: 8.8
         - **Flange Splice Plate:** Material E 300 (Fe 440); Preference: Outside + Inside; Thickness (mm): Most optimum from the available thicknesses in the Osdag database
         - **Web Splice Plate:** Material E 300 (Fe 440); Thickness (mm): Most optimum from the available thicknesses in the Osdag database
         - Bolt hole type is over-sized
         - The plate edges are machine-flame cut
         - Gap between the members is 0 mm

      **Download:**

      DesignReport_1.2.1.1.2.pdf_.

      Example_1.2.1.1.2.osi_.

--------------------------------------------------------------------------------------------------------------------------

.. note:: Example for **Release 2018-06-21** and lower versions - Cover Plate Bolted Connection

      **Sample Problem 1**

         Design a bolted cover plate splice connection for beam MB 450 to transfer a factored external moment of 140 kNm, factored shear of 110 kN and factored axial force of 40 kN. Use M20 Friction grip bolts of grade 8.8. Try 20mm thick flange splice plate and 10mm thick web splice plate. Take Fe410 grade steel (fy = 250 MPa, fu = 410 MPa). Assume bolt hole type as standard, edge as hand flame cut, gap between the beams as 5mm and surface of the metal to be treated with sand blast.

      **Download:**

      Design_Report_1.2.1.1.1.1.pdf_.

      Design_Example_1.2.1.1.1.1.osi_.


      **Sample Problem 2**

         Design a bolted cover plate splice connection for beam NPB 350 x 250 x 79.2 to transfer a factored external moment and shear force of 225 kNm ad 55 kN. Use M24 Friction grip bolts of grade 10.9. Try 14mm thick flange splice plate and 6mm thick web splice plate. Take Fe410 grade steel (fy = 250 MPa, fu = 410 MPa). Assume bolt hole type as oversized, edge as machine-flame cut, slip factor as 0.33 and gap between the beams as 3mm.

      **Download:**

      Design_Report_1.2.1.1.1.2.pdf_.

      Design_Example_1.2.1.1.1.2.osi_.

1.2.1.2. End Plate
--------------------------------
1.2.1.2.1. Coplanar Tension-Compression Flange

1.2.1.2.1.1. Flushed - Reversible Moment

      **Sample Problem 1**

         Design a *Beam-Beam End Plate Splice* connection for a beam *WB 500*. The grade of the beam material is **E 250 (Fe 410 W)A**.

         The beam is subjected to the following loading condition;

         - **Bending Moment**: 250 kNm (reversible)

         - **Shear Force**: 120 kN

         - **Axial Force**: 35 kN

         Perform an *optimum design* by adopting the following design specifications:

         - **Bolt type:** Bearing bolt; Diameter: 20, 24, 30; Grade: 6.8, 8.8
         - **End Plate:** Material E 300 (Fe 440); Thickness (mm): 20, 22, 25, 28, 32
         - Bolt hole type is standard
         - The ultimate strength of the weld material is, f\ :sub:`u` = 500 MPa
         - The plate edges are machine-flame cut
         - Gap between the members is 0 mm

      **Download:**
	
      DesignReport_1.2.1.2.1.1.1.pdf_.
	
      Example_1.2.1.2.1.1.1.osi_.

--------------------------------------------------------------------------------------------------------------------------

      **Sample Problem 2**
	
         Design a *Beam-Beam End Plate Splice* connection for a beam *MB 400*. The grade of the beam material is **E 250 (Fe 410 W)A**.

         The beam is subjected to the following loading condition;

         - **Bending Moment**: 100 kNm (reversible)

         - **Shear Force**: 40 kN

         - **Axial Force**: 20 kN

         Perform a *design check* by adopting the following design specifications:

         - **Bolt type:** Friction grip (HSFG); Pre-tensioned; Diameter: 16; Grade: 12.9
         - **End Plate:** Material E 250 (Fe 410 W)A; Thickness (mm): 22
         - Bolt hole type is standard
         - Surface treatment: Sand blast (slip factor = 0.48)
         - The ultimate strength of the weld material is, f\ :sub:`u` = 450 MPa
         - The plate edges are machine-flame cut
         - Gap between the members is 0 mm
         - Members are exposed to marine environment

      **Download:**
	
      DesignReport_1.2.1.2.1.1.2.pdf_.
	
      Example_1.2.1.2.1.1.2.osi_.

--------------------------------------------------------------------------------------------------------------------------

1.2.1.2.1.2. Extended One way - Irreversible Moment

      **Sample Problem 1**
	
         Design a *Beam-Beam End Plate Splice* connection for a beam *UB 610 x 229 x 125*. The grade of the beam material is **E 300 (Fe 440)**.

         The beam is subjected to the following loading condition;

         - **Bending Moment**: 300 kNm (irreversible)

         - **Shear Force**: 140 kN

         - **Axial Force**: 50 kN

         Perform an *optimum design* by adopting the following design specifications:

         - **Bolt type:** Bearing bolt; Diameter: 20, 24, 30; Grade: 8.8, 10.9
         - **End Plate:** Material E 250 (Fe 410 W)A; Thickness (mm): 18, 20, 22
         - Bolt hole type is standard
         - The ultimate strength of the weld material is, f\ :sub:`u` = 410 MPa
         - The plate edges are hand flame cut
         - Gap between the members is 0 mm

      **Download:**
	
      DesignReport_1.2.1.2.1.2.1.pdf_.
	
      Example_1.2.1.2.1.2.1.osi_.

--------------------------------------------------------------------------------------------------------------------------

      **Sample Problem 2**
	
         Design a *Beam-Beam End Plate Splice* connection for a beam *LB 400*. The grade of the beam material is **E 250 (Fe 410 W)A**.

         The beam is subjected to the following loading condition;

         - **Bending Moment**: 110 kNm (irreversible)

         - **Shear Force**: 55 kN

         - **Axial Force**: 15 kN

         Perform a *design check* by adopting the following design specifications:

         - **Bolt type:** Bearing bolt; Diameter: 20; Grade: 5.8
         - **End Plate:** Material E 250 (Fe 410 W)A; Thickness (mm): 12
         - Bolt hole type is standard
         - The ultimate strength of the weld material is, f\ :sub:`u` = 410 MPa
         - The plate edges are machine-flame cut
         - Gap between the members is 0 mm

      **Download:**
	
      DesignReport_1.2.1.2.1.2.2.pdf_.
	
      Example_1.2.1.2.1.2.2.osi_.

--------------------------------------------------------------------------------------------------------------------------

1.2.1.2.1.3. Extended Both Ways - Reversible Moment

      **Sample Problem 1**

         Design a *Beam-Beam End Plate Splice* connection for a beam *WPB 360 X 300 X 91.4*. The grade of the beam material is **E 250 (Fe 410 W)A**.

         The beam is subjected to the following loading condition;

         - **Bending Moment**: 120 kNm (reversible)

         - **Shear Force**: 75 kN

         Perform an *optimum design* by adopting the following design specifications:

         - **Bolt type:** Bearing bolt; Diameter: 20, 24; Grade: 4.6, 4.8, 5.6, 5.8
         - **End Plate:** Material E 250 (Fe 410 W)A; Thickness (mm): 16
         - Bolt hole type is standard
         - The ultimate strength of the weld material is, f\ :sub:`u` = 410 MPa
         - The plate edges are machine-flame cut
         - Gap between the members is 0 mm

      **Download:**
	
      DesignReport_1.2.1.2.1.3.1.pdf_.
	
      Example_1.2.1.2.1.3.1.osi_.

--------------------------------------------------------------------------------------------------------------------------

      **Sample Problem 2**

         Design a *Beam-Beam End Plate Splice* connection for a beam *UB 406 x 140 x 46*. The grade of the beam material is **E 300 (Fe 440)**.

         The beam is subjected to the following loading condition;

         - **Bending Moment**: 85 kNm (reversible)

         - **Shear Force**: 40 kN

         - **Axial Force**: 12 kN

         Perform a *design check* by adopting the following design specifications:

         - **Bolt type:** Friction grip (HSFG); Pre-tensioned; Diameter: 16; Grade: 12.9
         - **End Plate:** Material E 250 (Fe 410 W)A; Thickness (mm): 14
         - Bolt hole type is standard and bot type is Pre-tensioned
         - Surface treatment: Sand blast (slip factor = 0.48)
         - The plate edges are machine-flame cut
         - Gap between the members is 0 mm

      **Download:**
	
      DesignReport_1.2.1.2.1.3.2.pdf_.
	
      Example_1.2.1.2.1.3.2.osi_.

.. note:: Example for **Release 2018-06-21** and lower versions - End Plate Splice Connection (Extended both ways)

      **Sample Problem 1**

         Design a bolted extended (both way) end plate spliced connection for a beam NPB 350x170x50.2, for transferring a factored reversible moment and shear force of 100 kNm and 40 kN. Use M20 bearing bolts of grade 9.8. Try an end plate 20 mm thick and weld of sizes 8 mm and 6 mm at flange and web, respectively. Take Fe410 grade steel (fy = 250 MPa, fu = 410 MPa). The bearing bolt is non-pretensioned and the bolt hole type is oversized. The type of weld is shop weld and the edge type is sheared or hand flame cut.

      **Download:**

      Design_Report_1.2.1.2.1.1.pdf_.

      Design_Example_1.2.1.2.1.1.osi_.


      **Sample Problem 2**

         Design a bolted extended (both way) end plate spliced connection for a beam MB 450, for transferring a factored reversible moment, shear force and axial force of 170 kNm, 100 kN and 40 kN, respectively. Use M20 friction grip bolts of grade 8.8. Try an end plate 12 mm thick. The size of weld at flange and web is 6 mm and 8 mm. Take Fe410 grade steel (fy = 250 MPa, fu = 410 MPa). Assume the bolts to be pre-tensioned, bolt hole type is standard and the slip factor is 0.3. The type of weld is shop weld and the edge type is sheared or hand flame cut.

      **Download:**

      Design_Report_1.2.1.2.1.2.pdf_.

      Design_Example_1.2.1.2.1.2.osi_.

1.2.1.3. Cover Plate Welded
--------------------------------

      **Sample Problem 1**

         Design a *Beam-Beam Cover Plate Splice* connection for a beam *UB 686 x 254 x 140*. The grade of the beam material is **E 300 (Fe 440)**.

         The beam is subjected to the following loading condition;

         - **Bending Moment**: 235 kNm (reversible)

         - **Shear Force**: 150 kN

         - **Axial Force**: 20 kN

         Perform an *optimum design* by adopting the following design specifications:

         - **Flange Splice Plate:** Material E 250 (Fe 410 W)A; Preference: Outside + Inside; Thickness (mm): Most optimum from the available thicknesses in the Osdag database
         - **Web Splice Plate:** Material E 250 (Fe 410 W)A; Thickness (mm): Most optimum from the available thicknesses in the Osdag database
         - Type of weld fabrication: Field weld
         - The ultimate strength of the weld material is, f\ :sub:`u` = 550 MPa
         - Gap between the members is 5 mm
         - Members are exposed to (mild) marine environment

      **Download:**

      DesignReport_1.2.1.3.1.pdf_.

      Example_1.2.1.3.1.osi_.

--------------------------------------------------------------------------------------------------------------------------

      **Sample Problem 2**

         Design a *Beam-Beam Cover Plate Splice* connection for a beam *WB 400*. The grade of the beam material is **E 250 (Fe 410 W)A**.

         The beam is subjected to the following loading condition;

         - **Bending Moment**: 150 kNm (reversible)

         - **Shear Force**: 80 kN

         Perform a *design check* by adopting the following design specifications:

         - **Flange Splice Plate:** Material E 300 (Fe 440); Preference: Outside + Inside; Thickness (mm): 18
         - **Web Splice Plate:** Material E 300 (Fe 440); Thickness (mm): 12
         - Type of weld fabrication: Shop weld
         - The ultimate strength of the weld material is, f\ :sub:`u` = 450 MPa
         - Gap between the members is 8 mm
         - Members are not exposed to marine/corrosive environment

      **Download:**

      DesignReport_1.2.1.3.2.pdf_.

      Example_1.2.1.3.2.osi_.

1.2.2. Beam-to-Column Connection
*******************
1.2.2.1. End Plate
-------------------------------

1.2.2.1.1. Column Flange-Beam Web (CFBW) connectivity

1.2.2.1.1.1. Flushed - Reversible Moment

      **Sample Problem 1**

         Design a *Beam-Column End Plate* connection for a beam *WB 500* connected to a column *PBP 400 X 140.2*. The grade of the beam and the column material is **E 300 (Fe 440)** respectively.

         The load transferred from the beam to the column is as follows;

         - **Bending Moment**: 220 kNm (reversible)

         - **Shear Force**: 95 kN

         - **Axial Force**: 32 kN

         Perform an *optimum design* by adopting the following design specifications:

         - **Bolt type:** Bearing bolt; Diameter: 24, 30; Grade: 10.9, 12.9
         - **End Plate:** Material E 300 (Fe 440); Thickness (mm): 20, 22, 25, 28, 32
         - Bolt hole type is standard
         - Type of weld fabrication: Shop weld
         - The ultimate strength of the weld material is, f\ :sub:`u` = 510 MPa
         - The plate edges are machine-flame cut
         - Gap between the members is 0 mm
         - Members are not exposed to marine/corrosive environment

      **Download:**

      DesignReport_1.2.2.1.1.1.1.pdf_.

      Example_1.2.2.1.1.1.1.osi_.

--------------------------------------------------------------------------------------------------------------------------

      **Sample Problem 2**

         Design a *Beam-Column End Plate* connection for a beam *MB 500* connected to a column *UC 305 x 305 x 118*. The grade of the beam and the column material are **E 250 (Fe 410 W)A** and **E 300 (Fe 440)** respectively.

         The load transferred from the beam to the column is as follows;

         - **Bending Moment**: 150 kNm (reversible)

         - **Shear Force**: 90 kN

         Perform a *design check* by adopting the following design specifications:

         - **Bolt type:** Friction grip (HSFG); Pre-tensioned; Diameter: 20; Grade: 12.9
         - **End Plate:** Material E 250 (Fe 410 W)A; Thickness (mm): 28
         - Bolt hole type is standard
         - Surface treatment: Sand blast (slip factor = 0.48)
         - Type of weld fabrication: Shop weld
         - The ultimate strength of the weld material is, f\ :sub:`u` = 410 MPa
         - The plate edges are machine-flame cut
         - Gap between the members is 0 mm
         - Members are exposed to marine environment

      **Download:**

      DesignReport_1.2.2.1.1.1.2.pdf_.

      Example_1.2.2.1.1.1.2.osi_.

--------------------------------------------------------------------------------------------------------------------------

1.2.2.1.1.2. Extended One way - Irreversible Moment

      **Sample Problem 1**

         Design a *Beam-Column End Plate* connection for a beam *WB 450* connected to a column *HB 450*. The grade of the beam and the column material is **E 250 (Fe 410 W)A** respectively.

         The load transferred from the beam to the column is as follows;

         - **Bending Moment**: 210 kNm (reversible)

         - **Shear Force**: 40 kN

         - **Axial Force**: 15 kN

         Perform an *optimum design* by adopting the following design specifications:

         - **Bolt type:** Bearing bolt; Diameter: 20, 24, 30; Grade: 6.8, 8.8, 9.8
         - **End Plate:** Material E 250 (Fe 410 W)A; Thickness (mm): 16, 18, 20, 22
         - Bolt hole type is standard
         - Type of weld fabrication: Shop weld
         - The ultimate strength of the weld material is, f\ :sub:`u` = 410 MPa
         - The plate edges are hand flame cut
         - Gap between the members is 0 mm
         - Members are not exposed to marine/corrosive environment

      **Download:**

      DesignReport_1.2.2.1.1.2.1.pdf_.

      Example_1.2.2.1.1.2.1.osi_.

--------------------------------------------------------------------------------------------------------------------------

      **Sample Problem 2**

         Design a *Beam-Column End Plate* connection for a beam *LB 450* connected to a column *PBP 300 X 124.2*. The grade of the beam and the column material is **E 250 (Fe 410 W)A** respectively.

         The load transferred from the beam to the column is as follows;

         - **Bending Moment**: 100 kNm (reversible)

         - **Shear Force**: 55 kN

         - **Axial Force**: 12 kN

         Perform a *design check* by adopting the following design specifications:

         - **Bolt type:** Bearing bolt; Diameter: 24; Grade: 10.9
         - **End Plate:** Material E 250 (Fe 410 W)A; Thickness (mm): 16
         - Bolt hole type is standard
         - Type of weld fabrication: Shop weld
         - The ultimate strength of the weld material is, f\ :sub:`u` = 410 MPa
         - The plate edges are machine-flame cut
         - Gap between the members is 0 mm

      **Download:**

      DesignReport_1.2.2.1.1.2.2.pdf_.

      Example_1.2.2.1.1.2.2.osi_.

--------------------------------------------------------------------------------------------------------------------------

1.2.2.1.1.3. Extended Both Ways - Reversible Moment

      **Sample Problem 1**

         Design a *Beam-Column End Plate* connection for a beam *MB 500* connected to a column *PBP 400 X 158.1*. The grade of the beam and the column material are **E 300 (Fe 440)** and **E 350 (Fe 490)** respectively.

         The load transferred from the beam to the column is as follows;

         - **Bending Moment**: 180 kNm (reversible)

         - **Shear Force**: 100 kN

         Perform an *optimum design* by adopting the following design specifications:

         - **Bolt type:** Bearing bolt; Diameter: 20, 24, 30; Grade: 6.8, 8.8, 9.8
         - **End Plate:** Material E 250 (Fe 410 W)A; Thickness (mm): 16, 20, 22
         - Bolt hole type is standard
         - Type of weld fabrication: Shop weld
         - The ultimate strength of the weld material is, f\ :sub:`u` = 590 MPa
         - The plate edges are hand flame cut
         - Gap between the members is 0 mm
         - Members are exposed to marine environment

      **Download:**

      DesignReport_1.2.2.1.1.3.1.pdf_.

      Example_1.2.2.1.1.3.1.osi_.

--------------------------------------------------------------------------------------------------------------------------

      **Sample Problem 2**

         Design a *Beam-Column End Plate* connection for a beam *LB(P) 300* connected to a column *HB 300*. The grade of the beam and the column material is **E 250 (Fe 410 W)A** respectively.

         The load transferred from the beam to the column is as follows;

         - **Bending Moment**: 90 kNm (reversible)

         - **Shear Force**: 45 kN

         - **Axial Force**: 10 kN

         Perform a *design check* by adopting the following design specifications:

         - **Bolt type:** Friction grip (HSFG); Pre-tensioned; Diameter: 16; Grade: 8.8
         - **End Plate:** Material E 250 (Fe 410 W)A; Thickness (mm): 18
         - Bolt hole type is standard and bot type is Pre-tensioned
         - Surface treatment: Clean mill scale (slip factor = 0.33)
         - Type of weld fabrication: Shop weld
         - The plate edges are machine-flame cut
         - Gap between the members is 0 mm

      **Download:**

      DesignReport_1.2.2.1.1.3.2.pdf_.

      Example_1.2.2.1.1.3.2.osi_.

--------------------------------------------------------------------------------------------------------------------------

1.2.2.1.2. Column Web-Beam Web (CWBW) connectivity

1.2.2.1.2.1. Flushed - Reversible Moment

      **Sample Problem 1**

         Design a *Beam-Column End Plate* connection for a beam *WB 300* connected to a column *HB 450*. The grade of the beam and the column material is **E 250 (Fe 410 W)A** respectively.

         The load transferred from the beam to the column is as follows;

         - **Bending Moment**: 75 kNm (reversible)

         - **Shear Force**: 50 kN

         Perform an *optimum design* by adopting the following design specifications:

         - **Bolt type:** Bearing bolt; Diameter: 16, 20, 24, 30; Grade: 8.8, 9.8, 10.9
         - **End Plate:** Material E 300 (Fe 440); Thickness (mm): 14, 16, 18, 20
         - Bolt hole type is standard
         - Type of weld fabrication: Shop weld
         - The ultimate strength of the weld material is, f\ :sub:`u` = 490 MPa
         - The plate edges are machine-flame cut
         - Gap between the members is 0 mm

      **Download:**

      DesignReport_1.2.2.1.2.1.1.pdf_.

      Example_1.2.2.1.2.1.1.osi_.

--------------------------------------------------------------------------------------------------------------------------

      **Sample Problem 2**

         Design a *Beam-Column End Plate* connection for a beam *MB 300* connected to a column *UC 305 x 305 x 118*. The grade of the beam and the column material is **E 250 (Fe 410 W)A** respectively.

         The load transferred from the beam to the column is as follows;

         - **Bending Moment**: 45 kNm (reversible)

         - **Shear Force**: 70 kN

         Perform a *design check* by adopting the following design specifications:

         - **Bolt type:** Bearing bolt; Diameter: 20; Grade: 9.8
         - **End Plate:** Material E 250 (Fe 410 W)A; Thickness (mm): Most optimum from the available thicknesses in the Osdag database
         - Bolt hole type is standard
         - Type of weld fabrication: Shop weld
         - The ultimate strength of the weld material is, f\ :sub:`u` = 435 MPa
         - The plate edges are machine-flame cut
         - Gap between the members is 0 mm
         - Members are exposed to marine environment

      **Download:**

      DesignReport_1.2.2.1.2.1.2.pdf_.

      Example_1.2.2.1.2.1.2.osi_.

--------------------------------------------------------------------------------------------------------------------------

1.2.2.1.2.2. Extended One way - Irreversible Moment

      **Sample Problem 1**

         Design a *Beam-Column End Plate* connection for a beam *NPB 300 x 200 x 59.57* connected to a column *PBP 400 X 122.4*. The grade of the beam and the column material is **E 300 (Fe 440)** respectively.

         The load transferred from the beam to the column is as follows;

         - **Bending Moment**: 73 kNm (irreversible)

         - **Shear Force**: 50 kN

         - **Axial Force**: 15 kN

         Perform an *optimum design* by adopting the following design specifications:

         - **Bolt type:** Bearing bolt; Diameter: 20, 24; Grade: 8.8, 9.8
         - **End Plate:** Material E 250 (Fe 410 W)A; Thickness (mm): 14, 16, 18
         - Bolt hole type is standard
         - Type of weld fabrication: Shop weld
         - The ultimate strength of the weld material is, f\ :sub:`u` = 440 MPa
         - The plate edges are hand flame cut
         - Gap between the members is 0 mm

      **Download:**

      DesignReport_1.2.2.1.2.2.1.pdf_.

      Example_1.2.2.1.2.2.1.osi_.

--------------------------------------------------------------------------------------------------------------------------

      **Sample Problem 2**

         Design a *Beam-Column End Plate* connection for a beam *LB 400* connected to a column *PBP 400 X 122.4*. The grade of the beam and the column material is **E 300 (Fe 440)** respectively.

         The load transferred from the beam to the column is as follows;

         - **Bending Moment**: 110 kNm (irreversible)

         - **Shear Force**: 55 kN

         - **Axial Force**: 15 kN

         Perform a *design check* by adopting the following design specifications:

         - **Bolt type:** Bearing bolt; Diameter: 20; Grade: 4.8
         - **End Plate:** E 300 (Fe 440); Thickness (mm): 16
         - Bolt hole type is standard
         - Type of weld fabrication: Shop weld
         - The ultimate strength of the weld material is, f\ :sub:`u` = 450 MPa
         - The plate edges are machine-flame cut
         - Gap between the members is 0 mm

      **Download:**

      DesignReport_1.2.2.1.2.2.2.pdf_.

      Example_1.2.2.1.2.2.2.osi_.

--------------------------------------------------------------------------------------------------------------------------

1.2.2.1.2.3. Extended Both Ways - Reversible Moment

      **Sample Problem 1**

         Design a *Beam-Column End Plate* connection for a beam *UB 305 x 165 x 40* connected to a column *UC 356 x 406 x 235*. The grade of the beam and the column material are **E 300 (Fe 440)** and **E 350 (Fe 490)** respectively.

         The load transferred from the beam to the column is as follows;

         - **Bending Moment**: 65 kNm (reversible)

         - **Shear Force**: 150 kN

         Perform an *optimum design* by adopting the following design specifications:

         - **Bolt type:** Friction grip (HSFG); Pre-tensioned; Diameter: 24; Grade: 8.8
         - **End Plate:** Material E 250 (Fe 410 W)A; Thickness (mm): 16, 18, 20
         - Bolt hole type is standard and slip factor is 0.3
         - Type of weld fabrication: Shop weld
         - The ultimate strength of the weld material is, f\ :sub:`u` = 450 MPa
         - The plate edges are machine-flame cut
         - Gap between the members is 0 mm

      **Download:**

      DesignReport_1.2.2.1.2.3.1.pdf_.

      Example_1.2.2.1.2.3.1.osi_.

--------------------------------------------------------------------------------------------------------------------------

      **Sample Problem 2**

         Design a *Beam-Column End Plate* connection for a beam *MB 500* connected to a column *PBP 400 X 212.5*. The grade of the beam and the column material is **E 250 (Fe 410 W)A** respectively.

         The load transferred from the beam to the column is as follows;

         - **Bending Moment**: 85 kNm (reversible)

         - **Shear Force**: 120 kN

         - **Axial Force**: 18 kN

         Perform a *design check* by adopting the following design specifications:

         - **Bolt type:** Friction grip (HSFG); Pre-tensioned; Diameter: 20; Grade: 8.8
         - **End Plate:** Material E 300 (Fe 440); Thickness (mm): 20
         - Bolt hole type is standard and bot type is Pre-tensioned
         - Surface treatment: Blasted with short or girt (slip factor = 0.5)
         - Type of weld fabrication: Shop weld
         - The ultimate strength of the weld material is, f\ :sub:`u` = 500 MPa
         - The plate edges are machine-flame cut
         - Gap between the members is 0 mm

      **Download:**

      DesignReport_1.2.2.1.2.3.2.pdf_.

      Example_1.2.2.1.2.3.2.osi_.

1.2.3. Column-to-Column Splice Connection
*******************
1.2.3.1. Cover Plate Bolted
-------------------------------

      **Sample Problem 1**

         Design a *Column-Column Cover Plate* bolted connection for a column *HB 300*. The grade of the column material is **E 300 (Fe 440)**.

         The column is subjected to the following loading condition;

         - **Bending Moment**: 127 kNm (reversible)

         - **Axial Force**: 320 kN

         Perform an *optimum design* by adopting the following design specifications:

         - **Bolt type:** Bearing bolt; Diameter: 20, 24, 30; Grade: 10.9, 12.9
         - **Flange Splice Plate:** Material E 300 (Fe 440); Preference: Outside + Inside; Thickness (mm): Most optimum from the available thicknesses in the Osdag database
         - **Web Splice Plate:** Material E 300 (Fe 440); Thickness (mm): Most optimum from the available thicknesses in the Osdag database
         - Bolt hole type is over-sized
         - The plate edges are machine-flame cut
         - Gap between the members is 0 mm
         - Members are not exposed to marine/corrosive environment

      **Download:**

      DesignReport_1.2.3.1.1.pdf_.

      Example_1.2.3.1.1.osi_.

--------------------------------------------------------------------------------------------------------------------------

      **Sample Problem 2**

         Design a *Column-Column Cover Plate* bolted connection for a column *PBP 400 X 176.1*. The grade of the column material is **E 300 (Fe 440)**.

         The column is subjected to the following loading condition;

         - **Bending Moment**: 60 kNm (reversible)

         - **Shear Force**: 40 kN

         - **Axial Force**: 520 kN

         Perform a *design check* by adopting the following design specifications:

         - **Bolt type:** Friction grip (HSFG); Pre-tensioned; Diameter: 24; Grade: 8.8
         - **Flange Splice Plate:** Material E 300 (Fe 440); Preference: Outside; Thickness (mm): 20
         - **Web Splice Plate:** Material E 300 (Fe 440); Thickness (mm): 16
         - Bolt hole type is standard
         - Surface treatment: Sand blasted (slip factor = 0.52)
         - The plate edges are machine-flame cut
         - Gap between the members is 0 mm
         - Members are exposed to marine environment

      **Download:**

      DesignReport_1.2.3.1.2.pdf_.

      Example_1.2.3.1.2.osi_.

1.2.3.2. Cover Plate Welded
-------------------------------

      **Sample Problem 1**

         Design a *Column-Column Cover Plate* welded connection for a column *PBP 400 X 140.2*. The grade of the column material is **E 300 (Fe 440)**.

         The column is subjected to the following loading condition;

         - **Bending Moment**: 127 kNm (reversible)

         - **Axial Force**: 370 kN

         Perform an *optimum design* by adopting the following design specifications:

         - **Flange Splice Plate:** Material E 300 (Fe 440); Preference: Outside + Inside; Thickness (mm): Most optimum from the available thicknesses in the Osdag database
         - **Web Splice Plate:** Material E 300 (Fe 440); Thickness (mm): Most optimum from the available thicknesses in the Osdag database
         - Type of weld fabrication: Field weld
         - The ultimate strength of the weld material is, f\ :sub:`u` = 540 MPa
         - Gap between the members is 3 mm
         - Members are not exposed to marine/corrosive environment

      **Download:**

      DesignReport_1.2.3.2.1.pdf_.

      Example_1.2.3.2.1.osi_.

--------------------------------------------------------------------------------------------------------------------------

      **Sample Problem 2**

         Design a *Column-Column Cover Plate* welded connection for a column *HB 400*. The grade of the column material is **E 250 (Fe 410 W)A**.

         The column is subjected to the following loading condition;

         - **Bending Moment**: 50 kNm (reversible)

         - **Shear Force**: 30 kN

         - **Axial Force**: 480 kN

         Perform a *design check* by adopting the following design specifications:

         - **Flange Splice Plate:** Material E 250 (Fe 410 W)A; Preference: Outside; Thickness (mm): 18
         - **Web Splice Plate:** Material E 250 (Fe 410 W)A; Thickness (mm): 14
         - Type of weld fabrication: Field weld
         - The ultimate strength of the weld material is, f\ :sub:`u` = 510 MPa
         - Gap between the members is 5 mm
         - Members are exposed to (mild) marine environment

      **Download:**

      DesignReport_1.2.3.2.2.pdf_.

      Example_1.2.3.2.2.osi_.

1.2.3.3. End Plate
-------------------------------

1.2.3.3.1. Flush End Plate

      **Sample Problem 1**

         Design a *Column-Column End Plate* connection for a column *HB 250*. The grade of the column material is **E 250 (Fe 410 W)A**.

         The column is subjected to the following loading condition;

         - **Axial Force**: 350 kN

         Perform an *optimum design* by adopting the following design specifications:

         - **Bolt type:** Bearing bolt; Diameter: 24, 30; Grade: 8.8, 9.8, 10.9, 12.9
         - **End Plate:** Material E 250 (Fe 410 W)A; Thickness (mm): Most optimum from the available thicknesses in the Osdag database
         - Bolt hole type is standard
         - The plate edges are machine-flame cut
         - Gap between the members is 0 mm
         - Members are not exposed to marine/corrosive environment

      **Download:**

      DesignReport_1.2.3.3.1.1.pdf_.

      Example_1.2.3.3.1.1.osi_.

--------------------------------------------------------------------------------------------------------------------------

      **Sample Problem 2**

         Design a *Column-Column End Plate* connection for a column *PBP 300 X 95*. The grade of the column material is **E 300 (Fe 440)**.

         The column is subjected to the following loading condition;

         - **Bending Moment**: 50 kNm (reversible)

         - **Shear Force**: 20 kN

         - **Axial Force**: 250 kN

         Perform a *design check* by adopting the following design specifications:

         - **Bolt type:** Bearing bolt; Diameter: 30; Grade: 9.8
         - **End Plate:** Material E 300 (Fe 440); Thickness (mm): 32
         - Bolt hole type is standard
         - The plate edges are machine-flame cut
         - Gap between the members is 0 mm
         - Members are not exposed to marine/corrosive environment

      **Download:**

      DesignReport_1.2.3.3.1.2.pdf_.

      Example_1.2.3.3.1.2.osi_.

--------------------------------------------------------------------------------------------------------------------------

1.2.3.3.2. Extended Both Ways

      **Sample Problem 1**

         Design a *Column-Column End Plate* connection for a column *HB 250*. The grade of the column material is **E 250 (Fe 410 W)A**.

         The column is subjected to the following loading condition;

         - **Axial Force**: 350 kN

         Perform an *optimum design* by adopting the following design specifications:

         - **Bolt type:** Bearing bolt; Diameter: 24, 30; Grade: 8.8, 9.8, 10.9, 12.9
         - **End Plate:** Material E 250 (Fe 410 W)A; Thickness (mm): Most optimum from the available thicknesses in the Osdag database
         - Bolt hole type is standard
         - The plate edges are machine-flame cut
         - Gap between the members is 0 mm
         - Members are not exposed to marine/corrosive environment

      **Download:**

      DesignReport_1.2.3.3.2.1.pdf_.

      Example_1.2.3.3.2.1.osi_.

--------------------------------------------------------------------------------------------------------------------------

      **Sample Problem 2**

         Design a *Column-Column End Plate* connection for a column *PBP 300 X 95*. The grade of the column material is **E 300 (Fe 440)**.

         The column is subjected to the following loading condition;

         - **Bending Moment**: 50 kNm (reversible)

         - **Shear Force**: 20 kN

         - **Axial Force**: 250 kN

         Perform a *design check* by adopting the following design specifications:

         - **Bolt type:** Friction grip (HSFG); Pre-tensioned; Diameter: 30; Grade: 9.8
         - **End Plate:** Material E 300 (Fe 440); Thickness (mm): 32
         - Bolt hole type is standard
         - The plate edges are machine-flame cut
         - Gap between the members is 0 mm
         - Members are not exposed to marine/corrosive environment

      **Download:**

      DesignReport_1.2.3.3.2.2.pdf_.

      Example_1.2.3.3.2.2.osi_.

1.3. *Base Plate Connection*
#######################

1.3.1. Welded Column Base

      **Sample Problem 1**

         Design a *Base Plate* connection for a column *HB 450* subjected to the following reactions at the base;

         - **Axial Compression**: 1100 kN

         Perform an *optimum design* by adopting the following design specifications:

         - **Column:** Grade of the column material is **E 250 (Fe 410 W)A**.
         - **Anchor Bolt:** Type: End Plate Type; Diameter: M20, M24, M30; Grade: 8.8, 9.8
         - **Footing:** Grade of concrete is M 25
         - **Base Plate:** Material E 250 (Fe 410 W)A
         - Bolt hole type is over-sized and the Anchor bolt is *Galvanized*
         - Type of weld fabrication: Shop weld
         - The ultimate strength of the weld material is, f\ :sub:`u` = 510 MPa
         - The plate edges are machine-flame cut
         - Members are exposed to marine/corrosive environment

      **Download:**

      DesignReport_1.3.1.1.pdf_.

      Example_1.3.1.1.osi_.

--------------------------------------------------------------------------------------------------------------------------

      **Sample Problem 2**

         Design a *Base Plate* connection for a column *PBP 360 X 178.4* subjected to the following reactions at the base;

         - **Axial Compression**: 880 kN
         - **Shear Force (at base)**:
            - Along major (z-z) axis: 25 kN
            - Along minor (y-y) axis: 10 kN

         Perform a *design check* by adopting the following design specifications:

         - **Column:** Grade of the column material is **E 300 (Fe 440)**.
         - **Anchor Bolt:** Type: End Plate Type; Diameter: M20; Grade: 10.9
         - **Footing:** Grade of concrete is M 30
         - **Base Plate:** Material E 250 (Fe 410 W)A
         - **Stiffener/Shear Key:** Material E 250 (Fe 410 W)A
         - Bolt hole type is over-sized and the Anchor bolt is *Galvanized*
         - Type of weld fabrication: Shop weld
         - The ultimate strength of the weld material is, f\ :sub:`u` = 440 MPa
         - The plate edges are machine-flame cut
         - Members are exposed to corrosive environment

      **Download:**

      DesignReport_1.3.1.2.pdf_.

      Example_1.3.1.2.osi_.

--------------------------------------------------------------------------------------------------------------------------

1.3.2. Moment Base Plate

      **Sample Problem 1**

         Design a *Base Plate* connection for a column *PBP 400 X 140.2* subjected to the following reactions at the base;

         - **Axial Compression**: 900 kN
         - **Axial Tension/Uplift**: 27 kN
         - **Shear Force (at base)**:
            - Along major (z-z) axis: 85 kN
            - Along minor (y-y) axis: 12 kN
         - **Bending Moment**:
            - Major (z-z) axis: 123 kN

         Perform an *optimum design* by adopting the following design specifications:

         - **Column:** Grade of the column material is **E 350 (Fe 490)**.
         - **Anchor Bolt - Outside Column Flange:** Type: End Plate Type; Diameter: M24, M30; Grade: 8.8, 12.9
         - **Anchor Bolt - Inside Column Flange:** Type: End Plate Type; Diameter: M20, M24; Grade: 8.8, 9.8
         - **Footing:** Grade of concrete is M 30
         - **Base Plate:** Material E 250 (Fe 410 W)A
         - **Stiffener/Shear Key:** Material E 250 (Fe 410 W)A
         - Bolt hole type is over-sized and the Anchor bolt is *Galvanized* (both, outside and inside flange)
         - Type of weld fabrication: Shop weld
         - The ultimate strength of the weld material is, f\ :sub:`u` = 510 MPa
         - The plate edges are machine-flame cut
         - Members are exposed to marine/corrosive environment

      **Download:**

      DesignReport_1.3.2.1.pdf_.

      Example_1.3.2.1.osi_.

--------------------------------------------------------------------------------------------------------------------------

      **Sample Problem 2**

         Design a *Base Plate* connection for a column *HB 450* subjected to the following reactions at the base;

         - **Axial Compression**: 1600 kN
         - **Shear Force (at base)**:
            - Along major (z-z) axis: 80 kN
            - Along minor (y-y) axis: 23 kN
         - **Bending Moment**:
            - Major (z-z) axis: 180 kN
            - Minor (y-y) axis: 45 kN

         Perform a *design check* by adopting the following design specifications:

         - **Column:** Grade of the column material is **E 300 (Fe 440)**.
         - **Anchor Bolt - Outside Column Flange:** Type: End Plate Type; Diameter: M30; Grade: 10.9
         - **Anchor Bolt - Inside Column Flange:** Type: End Plate Type; Diameter: M20; Grade: 8.8
         - **Footing:** Grade of concrete is M 25
         - **Base Plate:** Material E 300 (Fe 440)
         - **Stiffener/Shear Key:** Material E 300 (Fe 440)
         - Bolt hole type is over-sized and the Anchor bolt is *Galvanized* (both, outside and inside flange)
         - Type of weld fabrication: Shop weld
         - The ultimate strength of the weld material is, f\ :sub:`u` = 600 MPa
         - The plate edges are machine-flame cut
         - Members are not exposed to marine/corrosive environment

      **Download:**

      DesignReport_1.3.2.2.pdf_.

      Example_1.3.2.2.osi_.

--------------------------------------------------------------------------------------------------------------------------

1.3.3. Hollow/Tubular Column Base

      **Sample Problem 1**

         Design a *Base Plate* connection for a square hollow column section *SHS 180 x 180 x 8* subjected to the following reactions at the base;

         - **Axial Compression**: 650 kN

         Perform an *optimum design* by adopting the following design specifications:

         - ** Hollow Column:** Grade of the column material is **E 300 (Fe 440)**
         - **Anchor Bolt:** Type: End Plate Type; Diameter: M20, M24, M30; Grade: 8.8, 10.9
         - **Footing:** Grade of concrete is M 25
         - **Base Plate:** Material E 250 (Fe 410 W)A
         - **Stiffener Plate:** Material E 250 (Fe 410 W)A
         - Bolt hole type is over-sized and the Anchor bolt is *Galvanized*
         - Type of weld fabrication: Shop weld
         - The ultimate strength of the weld material is, f\ :sub:`u` = 510 MPa
         - The plate edges are machine-flame cut
         - Members are not exposed to corrosive environment

      **Download:**

      DesignReport_1.3.3.1.pdf_.

      Example_1.3.3.1.osi_.

--------------------------------------------------------------------------------------------------------------------------

      **Sample Problem 2**

         Design a *Base Plate* connection for a circular hollow column section *CHS 355.6 x 10* subjected to the following reactions at the base;

         - **Axial Compression**: 775 kN
         - **Shear Force (at base)**:
            - Along major (z-z) axis: 45 kN
            - Along minor (y-y) axis: 10 kN

         Perform a *design check* by adopting the following design specifications:

         - **Column:** Grade of the column material is **E 300 (Fe 440)**.
         - **Anchor Bolt:** Type: End Plate Type; Diameter: M20; Grade: 8.8
         - **Footing:** Grade of concrete is M 35
         - **Base Plate:** Material E 250 (Fe 410 W)A
         - **Stiffener/Shear Key:** Material E 250 (Fe 410 W)A
         - Bolt hole type is over-sized and the Anchor bolt is *Galvanized*
         - Type of weld fabrication: Shop weld
         - The ultimate strength of the weld material is, f\ :sub:`u` = 440 MPa
         - The plate edges are machine-flame cut
         - Members are exposed to corrosive environment

      **Download:**

      DesignReport_1.3.3.2.pdf_.

      Example_1.3.3.2.osi_.

***********************
2.  **Tension Member Design**
***********************
2.1. *Tension Member - Bolted to End Gusset*
#######################

      **Sample Problem 1**

         Design a *Tension Member* with a bolted end connection to transfer a factored axial force of **235 kN**.

         Perform an *optimum design* by adopting the following design specifications:

         - **Section:**
            - Profile: Angle
            - Material Grade: E 250 (Fe 410 W)A
            - Connection Location: Longer leg
            - Length: 2560 mm

         - **End Connection:**
            - Connector: Type: Bolted; Bolt type: Bearing bolt; Diameter: 16, 20; Grade: 4.6, 4.8
            - Bolt hole type is standard
         - **Gusset Plate:** Material E 250 (Fe 410 W)A; Thickness (mm): 10, 12, 14, 16
         - The plate edges are machine-flame cut

      **Download:**

      DesignReport_2.1.1.pdf_.

      Example_2.1.1.osi_.

--------------------------------------------------------------------------------------------------------------------------

      **Sample Problem 2**

         Design a *Tension Member* with a bolted end connection to transfer a factored axial force of **330 kN**.

         Perform an *optimum design* by adopting the following design specifications:

         - **Section:**
            - Profile: Back to Back Angles
            - Material Grade: E 250 (Fe 410 W)A
            - Connection Location: Longer leg
            - Length: 2200 mm

         - **End Connection:**
            - Connector: Type: Bolted; Bolt type: Bearing bolt; Diameter: 16, 20, 24; Grade: 6.8, 8.8
            - Bolt hole type is over-sized
         - **Gusset Plate:** Material E 250 (Fe 410 W)A; Thickness (mm): 10, 12, 14, 16, 20
         - The plate edges are machine-flame cut

      **Download:**

      DesignReport_2.1.2.pdf_.

      Example_2.1.2.osi_.

--------------------------------------------------------------------------------------------------------------------------

      **Sample Problem 3**

         Design a *Tension Member* with a bolted end connection to transfer a factored axial force of **180 kN**.

         Perform an *optimum design* by adopting the following design specifications:

         - **Section:**
            - Profile: Star Angles
            - Material Grade: E 165 (Fe 290)
            - Connection Location: Short leg
            - Length: 2500 mm

         - **End Connection:**
            - Connector: Type: Bolted; Bolt type: Bearing bolt; Diameter: 16, 20; Grade: 5.6, 5.8, 6.8
            - Bolt hole type is standard
         - **Gusset Plate:** Material E 250 (Fe 410 W)A; Thickness (mm): 10, 12, 14
         - The plate edges are hand flame cut

      **Download:**

      DesignReport_2.1.3.pdf_.

      Example_2.1.3.osi_.

--------------------------------------------------------------------------------------------------------------------------

      **Sample Problem 4**

         Design a *Tension Member* with a bolted end connection to transfer a factored axial force of **240 kN**.

         Perform a *design check* by adopting the following design specifications:

         - **Section:**
            - Profile: Channel
            - Designation: MC 250
            - Material Grade: E 250 (Fe 410 W)A
            - Connection Location: Web
            - Length: 3200 mm

         - **End Connection:**
            - Connector: Type: Bolted; Bolt type: Friction grip (HSFG); Diameter: 20; Grade: 8.8
            - Bolt hole type is standard and slip factor is 0.3
         - **Gusset Plate:** Material E 250 (Fe 410 W)A; Thickness (mm): 14
         - The plate edges are machine-flame cut

      **Download:**

      DesignReport_2.1.4.pdf_.

      Example_2.1.4.osi_.

--------------------------------------------------------------------------------------------------------------------------

      **Sample Problem 5**

         Design a *Tension Member* with a bolted end connection to transfer a factored axial force of **500 kN**.

         Perform an *optimum design* by adopting the following design specifications:

         - **Section:**
            - Profile: Back to Back Channels
            - Material Grade: E 300 (Fe 440)
            - Connection Location: Web
            - length: 3000 mm

         - **End Connection:**
            - Connector: Type: Bolted; Bolt type: Bearing bolt; Diameter: 20, 24; Grade: 8.8, 9.8, 10.9
            - Bolt hole type is over-sized
         - **Gusset Plate:** Material E 250 (Fe 410 W)A; Thickness (mm): 16, 18, 20
         - The plate edges are machine-flame cut

      **Download:**

      DesignReport_2.1.5.pdf_.

      Example_2.1.5.osi_.

2.2. *Tension Member - Welded to End Gusset*
#######################

      **Sample Problem 1**

         Design a *Tension Member* with a welded end connection to transfer a factored axial force of **235 kN**.

         Perform an *optimum design* by adopting the following design specifications:

         - **Section:**
            - Profile: Angle
            - Material Grade: E 250 (Fe 410 W)A
            - Connection Location: Longer leg
            - Length: 2560 mm

         - **End Connection:**
            - Connector: Type: Welded; Type of weld fabrication: Field weld
            - The ultimate strength of the weld material is, f\ :sub:`u` = 450 MPa
         - **Gusset Plate:** Material E 250 (Fe 410 W)A; Thickness (mm): 10, 12, 14, 16
         - The plate edges are machine-flame cut

      **Download:**

      DesignReport_2.2.1.pdf_.

      Example_2.2.1.osi_.

--------------------------------------------------------------------------------------------------------------------------

      **Sample Problem 2**

         Design a *Tension Member* with bolted end connection to transfer a factored axial force of **330 kN**.

         Perform an *optimum design* by adopting the following design specifications:

         - **Section:**
            - Profile: Back to Back Angles
            - Material Grade: E 250 (Fe 410 W)A
            - Connection Location: Longer leg
            - Length: 2200 mm

         - **End Connection:**
            - Connector: Type: Welded; Type of weld fabrication: Shop weld
            - The ultimate strength of the weld material is, f\ :sub:`u` = 410 MPa
         - **Gusset Plate:** Material E 250 (Fe 410 W)A; Thickness (mm): 10, 12, 14, 16, 20
         - The plate edges are machine-flame cut

      **Download:**

      DesignReport_2.2.2.pdf_.

      Example_2.2.2.osi_.

--------------------------------------------------------------------------------------------------------------------------

      **Sample Problem 3**

         Design a *Tension Member* with bolted end connection to transfer a factored axial force of **180 kN**.

         Perform an *optimum design* by adopting the following design specifications:

         - **Section:**
            - Profile: Star Angles
            - Material Grade: E 165 (Fe 290)
            - Connection Location: Short leg
            - Length: 2500 mm

         - **End Connection:**
            - Connector: Type: Welded; Type of weld fabrication: Field weld
            - The ultimate strength of the weld material is, f\ :sub:`u` = 410 MPa
         - **Gusset Plate:** Material E 250 (Fe 410 W)A; Thickness (mm): 10, 12, 14
         - The plate edges are hand flame cut

      **Download:**

      DesignReport_2.2.3.pdf_.

      Example_2.2.3.osi_.

--------------------------------------------------------------------------------------------------------------------------

      **Sample Problem 4**

         Design a *Tension Member* with bolted end connection to transfer a factored axial force of **240 kN**.

         Perform a *design check* by adopting the following design specifications:

         - **Section:**
            - Profile: Channel
            - Designation: MC 250
            - Material Grade: E 250 (Fe 410 W)A
            - Connection Location: Web
            - Length: 3200 mm

         - **End Connection:**
            - Connector: Type: Welded; Type of weld fabrication: Field weld
            - The ultimate strength of the weld material is, f\ :sub:`u` = 410 MPa
         - **Gusset Plate:** Material E 250 (Fe 410 W)A; Thickness (mm): 14
         - The plate edges are machine-flame cut

      **Download:**

      DesignReport_2.2.4.pdf_.

      Example_2.2.4.osi_.

--------------------------------------------------------------------------------------------------------------------------

      **Sample Problem 5**

         Design a *Tension Member* with bolted end connection to transfer a factored axial force of **500 kN**.

         Perform an *optimum design* by adopting the following design specifications:

         - **Section:**
            - Profile: Back to Back Channels
            - Material Grade: E 300 (Fe 440)
            - Connection Location: Web
            - length: 3000 mm

         - **End Connection:**
            - Connector: Type: Welded; Type of weld fabrication: Shop weld
            - The ultimate strength of the weld material is, f\ :sub:`u` = 440 MPa
         - **Gusset Plate:** Material E 250 (Fe 410 W)A; Thickness (mm): 16, 18, 20
         - The plate edges are machine-flame cut

      **Download:**

      DesignReport_2.2.5.pdf_.

      Example_2.2.5.osi_.

--------------------------------------------------------------------------------------------------------------------------

**Other Resources**

   - How to use Osdag? Learn through Osdag's audio-video Tutorials_

   - We are on YouTube_ as well. Like and Subscribe our channel to keep up-to-date with Osdag

   - Comments, questions, suggestions? Check the forum Discussion_

   - Or, ask us a query directly through the FOSSEE Forum_

--------------------------------------------------------------------------------------------------------------------------

   Copyright © 2017 Osdag. All rights reserved.

.. _Homepage: http://osdag.fossee.in

.. _Tutorials: https://osdag.fossee.in/resources/videos

.. _YouTube: https://www.youtube.com/channel/UCnSZ7EjhDwNi3eCPcSKpgJg
 
.. _Discussion: https://osdag.fossee.in/forum

.. _Forum: https://forums.fossee.in/

.. _DesignReport_1.1.1.1.1.pdf: \DesignReport_1.1.1.1.1.pdf
.. _Example_1.1.1.1.1.osi: \Example_1.1.1.1.1.osi

.. _DesignReport_1.1.1.1.2.pdf: \DesignReport_1.1.1.1.2.pdf
.. _Example_1.1.1.1.2.osi: \Example_1.1.1.1.2.osi

.. _DesignReport_1.1.1.2.1.pdf: \DesignReport_1.1.1.2.1.pdf
.. _Example_1.1.1.2.1.osi: \Example_1.1.1.2.1.osi

.. _DesignReport_1.1.1.2.2.pdf: \DesignReport_1.1.1.2.2.pdf
.. _Example_1.1.1.2.2.osi: \Example_1.1.1.2.2.osi

.. _DesignReport_1.1.1.3.1.pdf: \DesignReport_1.1.1.3.1.pdf
.. _Example_1.1.1.3.1.osi: \Example_1.1.1.3.1.osi

.. _DesignReport_1.1.1.3.2.pdf: \DesignReport_1.1.1.3.2.pdf
.. _Example_1.1.1.3.2.osi: \Example_1.1.1.3.2.osi

.. _DesignReport_1.1.2.1.1.pdf: \DesignReport_1.1.2.1.1.pdf
.. _Example_1.1.2.1.1.osi: \Example_1.1.2.1.1.osi

.. _DesignReport_1.1.2.1.2.pdf: \DesignReport_1.1.2.1.2.pdf
.. _Example_1.1.2.1.2.osi: \Example_1.1.2.1.2.osi

.. _DesignReport_1.1.2.2.1.pdf: \DesignReport_1.1.2.2.1.pdf
.. _Example_1.1.2.2.1.osi: \Example_1.1.2.2.1.osi

.. _DesignReport_1.1.2.2.2.pdf: \DesignReport_1.1.2.2.2.pdf
.. _Example_1.1.2.2.2.osi: \Example_1.1.2.2.2.osi

.. _DesignReport_1.1.2.3.1.pdf: \DesignReport_1.1.2.3.1.pdf
.. _Example_1.1.2.3.1.osi: \Example_1.1.2.3.1.osi

.. _DesignReport_1.1.2.3.2.pdf: \DesignReport_1.1.2.3.2.pdf
.. _Example_1.1.2.3.2.osi: \Example_1.1.2.3.2.osi

.. _DesignReport_1.1.3.1.1.pdf: \DesignReport_1.1.3.1.1.pdf
.. _Example_1.1.3.1.1.osi: \Example_1.1.3.1.1.osi

.. _DesignReport_1.1.3.1.2.pdf: \DesignReport_1.1.3.1.2.pdf
.. _Example_1.1.3.1.2.osi: \Example_1.1.3.1.2.osi

.. _DesignReport_1.1.3.2.1.pdf: \DesignReport_1.1.3.2.1.pdf
.. _Example_1.1.3.2.1.osi: \Example_1.1.3.2.1.osi

.. _DesignReport_1.1.3.2.2.pdf: \DesignReport_1.1.3.2.2.pdf
.. _Example_1.1.3.2.2.osi: \Example_1.1.3.2.2.osi

.. _DesignReport_1.1.3.3.1.pdf: \DesignReport_1.1.3.3.1.pdf
.. _Example_1.1.3.3.1.osi: \Example_1.1.3.3.1.osi

.. _DesignReport_1.1.3.3.2.pdf: \DesignReport_1.1.3.3.2.pdf
.. _Example_1.1.3.3.2.osi: \Example_1.1.3.3.2.osi

.. _DesignReport_1.1.4.1.1.pdf: \DesignReport_1.1.4.1.1.pdf
.. _Example_1.1.4.1.1.osi: \Example_1.1.4.1.1.osi

.. _DesignReport_1.1.4.1.2.pdf: \DesignReport_1.1.4.1.2.pdf
.. _Example_1.1.4.1.2.osi: \Example_1.1.4.1.2.osi

.. _DesignReport_1.1.4.2.1.pdf: \DesignReport_1.1.4.2.1.pdf
.. _Example_1.1.4.2.1.osi: \Example_1.1.4.2.1.osi

.. _DesignReport_1.1.4.2.2.pdf: \DesignReport_1.1.4.2.2.pdf
.. _Example_1.1.4.2.2.osi: \Example_1.1.4.2.2.osi

.. _DesignReport_1.2.1.1.1.pdf: \DesignReport_1.2.1.1.1.pdf
.. _Example_1.2.1.1.1.osi: \Example_1.2.1.1.1.osi

.. _DesignReport_1.2.1.1.2.pdf: \DesignReport_1.2.1.1.2.pdf
.. _Example_1.2.1.1.2.osi: \Example_1.2.1.1.2.osi


.. _DesignReport_1.2.1.2.1.1.1.pdf: \DesignReport_1.2.1.2.1.1.1.pdf
.. _Example_1.2.1.2.1.1.1.osi: \Example_1.2.1.2.1.1.1.osi


.. _DesignReport_1.2.1.2.1.1.2.pdf: \DesignReport_1.2.1.2.1.1.2.pdf
.. _Example_1.2.1.2.1.1.2.osi: \Example_1.2.1.2.1.1.2.osi

.. _DesignReport_1.2.1.2.1.2.1.pdf: \DesignReport_1.2.1.2.1.2.1.pdf
.. _Example_1.2.1.2.1.2.1.osi: \Example_1.2.1.2.1.2.1.osi


.. _DesignReport_1.2.1.2.1.2.2.pdf: \DesignReport_1.2.1.2.1.2.2.pdf
.. _Example_1.2.1.2.1.2.2.osi: \Example_1.2.1.2.1.2.2.osi


.. _DesignReport_1.2.1.2.1.3.1.pdf: \DesignReport_1.2.1.2.1.3.1.pdf
.. _Example_1.2.1.2.1.3.1.osi: \Example_1.2.1.2.1.3.1.osi


.. _DesignReport_1.2.1.2.1.3.2.pdf: \DesignReport_1.2.1.2.1.3.2.pdf
.. _Example_1.2.1.2.1.3.2.osi: \Example_1.2.1.2.1.3.2.osi

.. _Design_Report_1.2.1.2.1.1.pdf: \Design_Report_1.2.1.2.1.1.pdf
.. _Design_Example_1.2.1.2.1.1.osi: \Design_Example_1.2.1.2.1.1.osi

.. _Design_Report_1.2.1.2.1.2.pdf: \Design_Report_1.2.1.2.1.2.pdf
.. _Design_Example_1.2.1.2.1.2.osi: \Design_Example_1.2.1.2.1.2.osi

.. _DesignReport_1.2.1.3.1.pdf: \DesignReport_1.2.1.3.1.pdf
.. _Example_1.2.1.3.1.osi: \Example_1.2.1.3.1.osi


.. _DesignReport_1.2.1.3.2.pdf: \DesignReport_1.2.1.3.2.pdf
.. _Example_1.2.1.3.2.osi: \Example_1.2.1.3.2.osi


.. _DesignReport_1.2.2.1.1.1.1.pdf: \DesignReport_1.2.2.1.1.1.1.pdf
.. _Example_1.2.2.1.1.1.1.osi: \Example_1.2.2.1.1.1.1.osi


.. _DesignReport_1.2.2.1.1.1.2.pdf: \DesignReport_1.2.2.1.1.1.2.pdf
	
.. _Example_1.2.2.1.1.1.2.osi: \Example_1.2.2.1.1.1.2.osi


.. _DesignReport_1.2.2.1.1.2.1.pdf: \DesignReport_1.2.2.1.1.2.1.pdf
	
.. _Example_1.2.2.1.1.2.1.osi: \Example_1.2.2.1.1.2.1.osi


.. _DesignReport_1.2.2.1.1.2.2.pdf: \DesignReport_1.2.2.1.1.2.2.pdf
	
.. _Example_1.2.2.1.1.2.2.osi: \Example_1.2.2.1.1.2.2.osi


.. _DesignReport_1.2.2.1.1.3.1.pdf: \DesignReport_1.2.2.1.1.3.1.pdf
	
.. _Example_1.2.2.1.1.3.1.osi: \Example_1.2.2.1.1.3.1.osi


.. _DesignReport_1.2.2.1.1.3.2.pdf: \DesignReport_1.2.2.1.1.3.2.pdf
	
.. _Example_1.2.2.1.1.3.2.osi: \Example_1.2.2.1.1.3.2.osi


.. _DesignReport_1.2.2.1.2.1.1.pdf: \DesignReport_1.2.2.1.2.1.1.pdf
	
.. _Example_1.2.2.1.2.1.1.osi: \Example_1.2.2.1.2.1.1.osi


.. _DesignReport_1.2.2.1.2.1.2.pdf: \DesignReport_1.2.2.1.2.1.2.pdf
	
.. _Example_1.2.2.1.2.1.2.osi: \Example_1.2.2.1.2.1.2.osi


.. _DesignReport_1.2.2.1.2.2.1.pdf: \DesignReport_1.2.2.1.2.2.1.pdf
	
.. _Example_1.2.2.1.2.2.1.osi: \Example_1.2.2.1.2.2.1.osi


.. _DesignReport_1.2.2.1.2.2.2.pdf: \DesignReport_1.2.2.1.2.2.2.pdf
	
.. _Example_1.2.2.1.2.2.2.osi: \Example_1.2.2.1.2.2.2.osi

.. _DesignReport_1.2.2.1.2.3.1.pdf: \DesignReport_1.2.2.1.2.3.1.pdf

.. _Example_1.2.2.1.2.3.1.osi: \Example_1.2.2.1.2.3.1.osi

.. _DesignReport_1.2.2.1.2.3.2.pdf: \DesignReport_1.2.2.1.2.3.2.pdf

.. _Example_1.2.2.1.2.3.2.osi: \Example_1.2.2.1.2.3.2.osi

.. _DesignReport_1.2.3.1.1.pdf: \DesignReport_1.2.3.1.1.pdf

.. _Example_1.2.3.1.1.osi: \Example_1.2.3.1.1.osi

.. _DesignReport_1.2.3.1.2.pdf: \DesignReport_1.2.3.1.2.pdf

.. _Example_1.2.3.1.2.osi: \Example_1.2.3.1.2.osi

.. _DesignReport_1.2.3.2.1.pdf: \DesignReport_1.2.3.2.1.pdf

.. _Example_1.2.3.2.1.osi: \Example_1.2.3.2.1.osi

.. _DesignReport_1.2.3.2.2.pdf: \DesignReport_1.2.3.2.2.pdf

.. _Example_1.2.3.2.2.osi: \Example_1.2.3.2.2.osi

.. _DesignReport_1.2.3.3.1.1.pdf: \DesignReport_1.2.3.3.1.1.pdf

.. _Example_1.2.3.3.1.1.osi: \Example_1.2.3.3.1.1.osi

.. _DesignReport_1.2.3.3.1.2.pdf: \DesignReport_1.2.3.3.1.2.pdf

.. _Example_1.2.3.3.1.2.osi: \Example_1.2.3.3.1.2.osi

.. _DesignReport_1.2.3.3.2.1.pdf: \DesignReport_1.2.3.3.2.1.pdf

.. _Example_1.2.3.3.2.1.osi: \Example_1.2.3.3.2.1.osi

.. _DesignReport_1.2.3.3.2.2.pdf: \DesignReport_1.2.3.3.2.2.pdf

.. _Example_1.2.3.3.2.2.osi: \Example_1.2.3.3.2.2.osi

.. _DesignReport_1.3.1.1.pdf: \DesignReport_1.3.1.1.pdf

.. _Example_1.3.1.1.osi: \Example_1.3.1.1.osi

.. _DesignReport_1.3.1.2.pdf: \DesignReport_1.3.1.2.pdf

.. _Example_1.3.1.2.osi: \Example_1.3.1.2.osi

.. _DesignReport_1.3.2.1.pdf: \DesignReport_1.3.2.1.pdf

.. _Example_1.3.2.1.osi: \Example_1.3.2.1.osi

.. _DesignReport_1.3.2.2.pdf: \DesignReport_1.3.2.2.pdf

.. _Example_1.3.2.2.osi: \Example_1.3.2.2.osi

.. _DesignReport_1.3.3.1.pdf: \DesignReport_1.3.3.1.pdf

.. _Example_1.3.3.1.osi: \Example_1.3.3.1.osi

.. _DesignReport_1.3.3.2.pdf: \DesignReport_1.3.3.2.pdf

.. _Example_1.3.3.2.osi: \Example_1.3.3.2.osi

.. _DesignReport_2.1.1.pdf: \DesignReport_2.1.1.pdf

.. _Example_2.1.1.osi: \Example_2.1.1.osi

.. _DesignReport_2.1.2.pdf: \DesignReport_2.1.2.pdf

.. _Example_2.1.2.osi: \Example_2.1.2.osi

.. _DesignReport_2.1.3.pdf: \DesignReport_2.1.3.pdf

.. _Example_2.1.3.osi: \Example_2.1.3.osi

.. _DesignReport_2.1.4.pdf: \DesignReport_2.1.4.pdf

.. _Example_2.1.4.osi: \Example_2.1.4.osi

.. _DesignReport_2.1.5.pdf: \DesignReport_2.1.5.pdf

.. _Example_2.1.5.osi: \Example_2.1.5.osi

.. _DesignReport_2.2.1.pdf: \DesignReport_2.2.1.pdf

.. _Example_2.2.1.osi: \Example_2.2.1.osi

.. _DesignReport_2.2.2.pdf: \DesignReport_2.2.2.pdf

.. _Example_2.2.2.osi: \Example_2.2.2.osi

.. _DesignReport_2.2.3.pdf: \DesignReport_2.2.3.pdf

.. _Example_2.2.3.osi: \Example_2.2.3.osi

.. _DesignReport_2.2.4.pdf: \DesignReport_2.2.4.pdf

.. _Example_2.2.4.osi: \Example_2.2.4.osi

.. _DesignReport_2.2.5.pdf: \DesignReport_2.2.5.pdf

.. _Example_2.2.5.osi: \Example_2.2.5.osi

.. _Design_Report_1.2.1.1.1.2.pdf: \Design_Report_1.2.1.1.1.2.pdf

.. _Design_Example_1.2.1.1.1.2.osi: \Design_Example_1.2.1.1.1.2.osi

.. _Design_Report_1.2.1.1.1.1.pdf: \Design_Report_1.2.1.1.1.1.pdf

.. _Design_Example_1.2.1.1.1.1.osi: \Design_Example_1.2.1.1.1.1.osi

.. _Design_Report_1.1.4.1.1.pdf: \Design_Report_1.1.4.1.1.pdf

.. _Design_Example_1.1.4.1.1.osi: \Design_Example_1.1.4.1.1.osi

.. _Design_Report_1.1.4.1.2.pdf: \Design_Report_1.1.4.1.2.pdf

.. _Design_Example_1.1.4.1.2.osi: \Design_Example_1.1.4.1.2.osi

.. _Design_Report_1.1.4.2.1.pdf: \Design_Report_1.1.4.2.1.pdf

.. _Design_Example_1.1.4.2.1.osi: \Design_Example_1.1.4.2.1.osi

.. _Design_Report_1.1.4.2.2.pdf: \Design_Report_1.1.4.2.2.pdf

.. _Design_Example_1.1.4.2.2.osi: \Design_Example_1.1.4.2.2.osi

.. _Design_Report_1.1.3.1.1.pdf: \Design_Report_1.1.3.1.1.pdf

.. _Design_Example_1.1.3.1.1.osi: \Design_Example_1.1.3.1.1.osi

.. _Design_Report_1.1.3.1.2.pdf: \Design_Report_1.1.3.1.2.pdf

.. _Design_Example_1.1.3.1.2.osi: \Design_Example_1.1.3.1.2.osi

.. _Design_Report_1.1.3.2.1.pdf: \Design_Report_1.1.3.2.1.pdf

.. _Design_Example_1.1.3.2.1.osi: \Design_Example_1.1.3.2.1.osi

.. _Design_Report_1.1.3.2.2.pdf: \Design_Report_1.1.3.2.2.pdf

.. _Design_Example_1.1.3.2.2.osi: \Design_Example_1.1.3.2.2.osi

.. _Design_Report_1.1.3.3.1.pdf: \Design_Report_1.1.3.3.1.pdf

.. _Design_Example_1.1.3.3.1.osi: \Design_Example_1.1.3.3.1.osi

.. _Design_Report_1.1.3.3.2.pdf: \Design_Report_1.1.3.3.2.pdf

.. _Design_Example_1.1.3.3.2.osi: \Design_Example_1.1.3.3.2.osi

.. _Design_Report_1.1.1.1.1.pdf: \Design_Report_1.1.1.1.1.pdf

.. _Design_Example_1.1.1.1.1.osi: \Design_Example_1.1.1.1.1.osi

.. _Design_Report_1.1.1.1.2.pdf: \Design_Report_1.1.1.1.2.pdf

.. _Design_Example_1.1.1.1.2.osi: \Design_Example_1.1.1.1.2.osi

.. _Design_Report_1.1.1.2.1.pdf: \Design_Report_1.1.1.2.1.pdf

.. _Design_Example_1.1.1.2.1.osi: \Design_Example_1.1.1.2.1.osi

.. _Design_Report_1.1.1.2.2.pdf: \Design_Report_1.1.1.2.2.pdf

.. _Design_Example_1.1.1.2.2.osi: \Design_Example_1.1.1.2.2.osi

.. _Design_Report_1.1.1.3.1.pdf: \Design_Report_1.1.1.3.1.pdf

.. _Design_Example_1.1.1.3.1.osi: \Design_Example_1.1.1.3.1.osi

.. _Design_Report_1.1.1.3.2.pdf: \Design_Report_1.1.1.3.2.pdf

.. _Design_Example_1.1.1.3.2.osi: \Design_Example_1.1.1.3.2.osi

.. _Design_Report_1.1.2.1.1.pdf: \Design_Report_1.1.2.1.1.pdf

.. _Design_Example_1.1.2.1.1.osi: \Design_Example_1.1.2.1.1.osi

.. _Design_Report_1.1.2.1.2.pdf: \Design_Report_1.1.2.1.2.pdf

.. _Design_Example_1.1.2.1.2.osi: \Design_Example_1.1.2.1.2.osi

.. _Design_Report_1.1.2.2.1.pdf: \Design_Report_1.1.2.2.1.pdf

.. _Design_Example_1.1.2.2.1.osi: \Design_Example_1.1.2.2.1.osi

.. _Design_Report_1.1.2.2.2.pdf: \Design_Report_1.1.2.2.2.pdf

.. _Design_Example_1.1.2.2.2.osi: \Design_Example_1.1.2.2.2.osi

.. _Design_Report_1.1.2.3.1.pdf: \Design_Report_1.1.2.3.1.pdf

.. _Design_Example_1.1.2.3.1.osi: \Design_Example_1.1.2.3.1.osi

.. _Design_Report_1.1.2.3.2.pdf: \Design_Report_1.1.2.3.2.pdf

.. _Design_Example_1.1.2.3.2.osi: \Design_Example_1.1.2.3.2.osi

.. toctree::
   :maxdepth: 2
   :caption: Contents:

