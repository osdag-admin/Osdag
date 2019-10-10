.. Help_Design_Examples documentation master file, created by
   sphinx-quickstart on Mon Jun 12 15:06:32 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. image::   website_header.png
	:target: http://osdag.fossee.in/
	
	

Welcome to Osdag help!
================================================

Osdag is a cross-platform free and open-source software for the design and detailing of steel structures, following relevant Indian Standards. Osdag is primarily built upon Python and other Python-based FOSS tools, such as, PyQt, OpenCascade, PythonOCC, SQLite, etc. It is developed by the Osdag team at IIT Bombay. 
 
This beta version of Osdag contains four shear connection modules.

The example OSI files can be loaded using the ``File -> Load input`` option of the appropriate connection module.

**************************
Osdag Homepage_.
**************************

***********************
1.  Connections
***********************
1.1. Shear Connection
#######################
1.1.1. Fin Plate Connection
****************************
1.1.1.1 Column Flange-Beam Web (CFBW) connectivity

    	*Sample problem 1*

		Design a fin plate connection between a beam MB 500 and a column UC 305 x 305 x 97 for transferring a vertical (factored) shear force of 140 kN. Use M24 Friction grip bolts of property class 8.8. Try 12mm thick fin plate with weld thickness of 12mm. Take Fe410 grade steel (f\ :sub:`y` \  = 250 MPa,  f\ :sub:`u` = 410 MPa). Assume bolt hole type as standard, weld type as shop weld and type of edge as hand flame cut.

   	 **Download:**

   	 DesignReport_1.1.1.1.1.pdf_. 
	
   	 Example_1.1.1.1.1.osi_.
 
    	*Sample problem 2*

		Design a fin plate connection between a beam MB 350 and a column SC 200 for transferring a vertical (factored) shear force of 150 kN. Use M20 bearing bolts of property class 4.6. Try 12mm thick fin plate with weld thickness of 8mm. Take Fe410 grade steel (f\ :sub:`y` \  = 250 MPa,  f\ :sub:`u` = 410 MPa). Assume weld type as shop weld and type of edge as machine flame cut.

   	 **Download:**

    	DesignReport_1.1.1.1.2.pdf_. 

    	Example_1.1.1.1.2.osi_.
 
1.1.1.2. Column Web-Beam Web (CWBW) connectivity

    	*Sample problem 1*

		Design a fin plate connection between a beam UB 356 x 171 x 45 and a column PBP 300 x 180 for transferring a vertical (factored) shear force of 120 kN. Use M16 Friction grip bolts of property class 8.8. Try 8mm thick fin plate with weld thickness of 8mm. Take Fe410 grade steel (f\ :sub:`y` \  = 250 MPa,  f\ :sub:`u` = 410 MPa). Assume bolt hole type as standard, slip factor of 0.25, type of weld as field weld and edge as hand flame cut.

    	**Download:**

   	 DesignReport_1.1.1.2.1.pdf_.

   	 Example_1.1.1.2.1.osi_.

    	*Sample problem 2*

		Design a fin plate connection between a beam LB 300 and a column SC 250 for transferring a vertical (factored) shear force of 135 kN. Use M24 bearing bolts of property class 4.8. Try 10mm thick fin plate with weld thickness of 8mm. Take Fe410 grade steel f\ :sub:`y` \  = 250 MPa,  f\ :sub:`u` = 410 MPa). Assume bolt hole type as standard, type of weld as shop weld and edge as hand flame cut and environment as corrosive.

    	**Download:**

   	DesignReport_1.1.1.2.2.pdf_.

    	Example_1.1.1.2.2.osi_.

1.1.1.3. Beam-Beam (BB) connectivity

	*Sample problem 1*
    
		Design a fin plate connection between a primary beam MB 350 and a secondary beam NPB 270 x 135 x 36.1 for transferring a vertical (factored) shear force of 110 kN. Use M20 Friction grip bolts of property class 10.9. Try 10mm thick fin plate with weld thickness of 8mm. Take Fe410 grade steel (f\ :sub:`y` \  = 250 MPa,  f\ :sub:`u` = 410 MPa). Assume slip factor of 0.52, bolt hole type oversized and type of edge as machine flame cut.

   	 **Download:**

    	DesignReport_1.1.1.3.1.pdf_.
	
    	Example_1.1.1.3.1.osi_.

   	 *Sample problem 2*

		Design a fin plate connection between a primary beam WPB 450 x 300 x 99.7 and a secondary beam UB 356 x 171 x 67 for transferring a vertical (factored) shear force of 220 kN. Use M24 Friction grip bolts of property class 10.9. Try 14mm thick fin plate with weld thickness of 12mm. Take Fe410 grade steel (f\ :sub:`y` \  = 250 MPa,  f\ :sub:`u` = 410 MPa). Assume slip factor of 0.48, bolt hole type standard, weld type as shop weld and type of edge as machine flame cut.

    	**Download:**

   	DesignReport_1.1.1.3.2.pdf_.

    	Example_1.1.1.3.2.osi_.
 
 
1.1.2. End Plate Connection
****************************

1.1.2.1. Column Flange-Beam Web (CFBW) connectivity

    	*Sample problem 1*

		Design an end plate connection between a beam MB 350 and a column SC 250 for transferring a vertical (factored) shear force of 140 kN. Use M20 bearing bolts of property class 4.6. Try 10mm thick end plate with weld thickness of 6mm. Take Fe410 grade steel (f\ :sub:`y` \  = 250 MPa,  f\ :sub:`u` = 410 MPa). Assume bolt hole type as standard, weld type shop weld and type of edge as hand flame cut.

    	**Download:**

    	DesignReport_1.1.2.1.1.pdf_.

    	Example_1.1.2.1.1.osi_. 
    
    	*Sample problem 2*

		Design an end plate connection between a beam MB 300 and a column UC 254 x254 x 107 for transferring a vertical (factored) shear force of 195 kN. Use M16 Friction grip bolts of property class 8.8. Try 12mm thick end plate with weld thickness of 10mm. Take Fe410 grade steel (f\ :sub:`y` \  = 250 MPa,  f\ :sub:`u` = 410 MPa). Assume bolt hole type as standard, weld type shop weld and type of edge as machine flame cut.

    	**Download:**

    	DesignReport_1.1.2.1.2.pdf_. 

    	Example_1.1.2.1.2.osi_. 
 
1.1.2.2. Column Web-Beam Web (CWBW) connectivity

    	*Sample problem 1*

		Design an end plate connection between a beam UB 356 x 171 x 45 and a column PBP 300 x 180 for transferring a vertical (factored) shear force of 120 kN. Use M16 Friction grip bolts of property class 10.9. Try 12mm thick end plate with weld thickness of 6mm. Take Fe410 grade steel (f\ :sub:`y` \  = 250 MPa,  f\ :sub:`u` = 410 MPa). Assume bolt hole type as standard, slip factor of 0.25, type of weld as field weld and edge type as hand flame cut.
	
    	**Download:**

    	DesignReport_1.1.2.2.1.pdf_. 

    	Example_1.1.2.2.1.osi_. 
    
   	 *Sample problem 2*

		Design an end plate connection between a beam LB 300 and a column SC 250 for transferring a vertical (factored) shear force of 135 kN. Use M12 bearing bolts of property class 4.8. Try 10mm thick end plate with weld thickness of 10mm. Take Fe410 grade steel (f\ :sub:`y` \  = 250 MPa,  f\ :sub:`u` = 410 MPa). Assume bolt hole type as standard, type of weld as shop weld and edge type as hand flame cut.

    	**Download:**

    	DesignReport_1.1.2.2.2.pdf_.

    	Example_1.1.2.2.2.osi_.
 
1.1.2.3. Beam-Beam (BB) connectivity

    	*Sample problem 1*

		Design an end plate connection between a primary beam MB 500 and a secondary beam MB 400 for transferring a vertical (factored) shear force of 160 kN. Use M20 Friction grip bolts of property class 8.8. Try 16mm thick end plate with weld thickness of 8mm. Take Fe410 grade steel (f\ :sub:`y` \  = 250 MPa,  f\ :sub:`u` = 410 MPa). Assume slip factor of 0.2, bolt hole type as oversized, weld type shop weld and type of edge as machine flame cut.

   	**Download:**

   	DesignReport_1.1.2.3.1.pdf_.

    	Example_1.1.2.3.1.osi_. 

    	*Sample problem 2*

		Design an end plate connection between a primary beam WPB 450 x 300 x 99.7 and a secondary beam UB 356 x 171 x 67 for transferring a vertical (factored) shear force of 220 kN. Use M24 Friction grip bolts of property class 10.9. Try 14mm thick end plate with weld thickness of 12mm. Take Fe410 grade steel (f\ :sub:`y` \  = 250 MPa,  f\ :sub:`u` = 410 MPa). Assume slip factor of 0.48, bolt hole type as standard, weld type shop weld and type of edge as machine flame cut.

    	**Download:**

    	DesignReport_1.1.2.3.2.pdf_. 

    	Example_1.1.2.3.2.osi_. 

 
1.1.3. Cleat Angle Connection
*******************************

1.1.3.1. Column Flange-Beam Web (CFBW) connectivity

    	*Sample problem 1*

		Design a cleat angle connection between a beam MB 400 and a column SC 250 for transferring a vertical (factored) shear force of 140 kN. Use M20 Friction grip bolts of property class 8.8. Try cleat angle of size 90 x 90 x 12. Take Fe410 grade steel (f\ :sub:`y` \  = 250 MPa,  f\ :sub:`u` = 410 MPa). Assume slip factor of 0.48, bolt hole type as standard and type of edge as hand flame cut.

   	**Download:**

    	DesignReport_1.1.3.1.1.pdf_.

    	Example_1.1.3.1.1.osi_.
 
    	*Sample problem 2*

		Design a cleat angle connection between a beam MB 350 and a column HB 300 for transferring a vertical (factored) shear force of 170 kN. Use M16 bearing bolts of property class 4.6. Try cleat angle of size 100 x 100 x 12. Take Fe410 grade steel (f\ :sub:`y` \  = 250 MPa,  f\ :sub:`u` = 410 MPa). Assume bolt hole type as standard, type of edge as machine flame cut and environment as corrosive.
 
    	**Download:**

    	DesignReport_1.1.3.1.2.pdf_.

    	Example_1.1.3.1.2.osi_. 
 
1.1.3.2. Column Web-Beam Web (CWBW) connectivity

    	*Sample problem 1*

		Design a cleat angle connection between a beam MB 350 and a column UC 305 x 305 x 97 for transferring a vertical (factored) shear force of 120.5 kN. Use M20 Friction grip bolts of property class 8.8. Try cleat angle of size 110 x 110 x 16. Take Fe410 grade steel (f\ :sub:`y` \  = 250 MPa,  f\ :sub:`u` = 410 MPa). Assume bolt hole type as standard, slip factor of 0.2, type of edge as hand flame cut and gap between column and beam as 5mm.
 
    	**Download:**

    	DesignReport_1.1.3.2.1.pdf_.

    	Example_1.1.3.2.1.osi_. 
 
    	*Sample problem 2*

	Design a cleat angle connection between a beam MB 200 and a column UC 305 x 305 x 118 for transferring a vertical (factored) shear force of 80 kN. Use M12 bearing bolts of property class 6.8. Try cleat angle of size 110 x 110 x 16. Take Fe410 grade steel (f\ :sub:`y` \  = 250 MPa,  f\ :sub:`u` = 410 MPa). Assume bolt hole type as standard, type of edge as hand flame cut and environment as corrosive.
 
    	**Download:**

    	DesignReport_1.1.3.2.2.pdf_.

    	Example_1.1.3.2.2.osi_. 
 
1.1.3.3. Beam-Beam (BB) connectivity

    	*Sample problem 1*
    
		Design a cleat angle connection between a primary beam WB 450 and a secondary beam MB 400 for transferring a vertical (factored) shear force of 145 kN. Use M24 bearing bolts of property class 4.6. Try cleat angle of size 100 100 x 10. Take Fe410 grade steel (f\ :sub:`y` \  = 250 MPa,  f\ :sub:`u` = 410 MPa). Assume bolt hole type as standard and type of edge as hand flame cut.
	 
    	**Download:**

    	DesignReport_1.1.3.3.1.pdf_. 

    	Example_1.1.3.3.1.osi_. 
 
    	*Sample problem 2*
        
		Design a cleat angle connection between a primary beam WPB 280x280x61.2 and a secondary beam NPB 220x110x29.4 for transferring a vertical (factored) shear force of 100 kN. Use M20 Friction grip bolts of property class 10.9. Try cleat angle of size 100 100 x 8. Take Fe410 grade steel (f\ :sub:`y` \  = 250 MPa,  f\ :sub:`u` = 410 MPa). Assume bolt hole type as oversized, slip factor of 0.52, type of edge as machine flame cut and gap between column and beam as 15mm.
 
    	**Download:**

    	DesignReport_1.1.3.3.2.pdf_. 

    	Example_1.1.3.3.2.osi_.

1.1.4. Seated Angle Connection
*******************************
1.1.4.1. Column Flange-Beam Flange (CFBF) connectivity

    	*Sample problem 1*

		Design a seated angle connection between a beam MB 300 and a column UC 203 x 203 x 86 for transferring a vertical (factored) shear force of 100 kN. Use M20 Friction grip bolts of property class 10.9. Try a top angle of size 150 150 x 10 and seated angle of size 150 150 x 15. Take Fe410 grade steel (f\ :sub:`y` \  = 250 MPa,  f\ :sub:`u` = 410 MPa). Assume slip factor of 0.55, bolt fu = 940 MPa and type of edge as hand flame cut.
 
    	**Download:**

    	DesignReport_1.1.4.1.1.pdf_. 

    	Example_1.1.4.1.1.osi_.

 
    	*Sample problem 2*
	
		Design a seated angle connection between a beam MB 200 and a column SC 140 for transferring a vertical (factored) shear force of 140 kN. Use M12 bearing bolts of property class 6.8. Try a top angle of size 90 90 x 8 and seated angle of size 110 110 x 16. Take Fe410 grade steel (f\ :sub:`y` \  = 250 MPa,  f\ :sub:`u` = 410 MPa). Assume type of edge as hand flame cut and environment as corrosive.
 
    	**Download:**

    	DesignReport_1.1.4.1.2.pdf_. 

    	Example_1.1.4.1.2.osi_. 
 
1.1.4.2. Column Web-Beam Flange (CWBF) connectivity

   	 *Sample problem 1*

		Design a seated angle connection between a beam NPB 250x150x39.8 and a column PBP 300x180 for transferring a vertical (factored) shear force of 80 kN. Use M16 bearing bolts of property class 5.8. Try a top angle of size 90 90 x 10 and seated angle of size 150 150 x 15. Take Fe410 grade steel (f\ :sub:`y` \  = 250 MPa,  f\ :sub:`u` = 410 MPa). Assume type of edge as machine flame cut.
 
    	**Download:**

    	DesignReport_1.1.4.2.1.pdf_. 

    	Example_1.1.4.2.1.osi_.
 
	*Sample problem 2*

		Design a seated angle connection between a beam WPB 140x140x24.7 and a column HB 200 for transferring a vertical (factored) shear force of 140 kN. Use M12 bearing bolts of property class 5.8. Try a top angle of size 90 90 x 10 and seated angle of size 150 150 x 15. Take Fe410 grade steel (f\ :sub:`y` \  = 250 MPa,  f\ :sub:`u` = 410 MPa). Assume bolt hole type as Oversized, type of edge as machine flame cut and gap between column and beam as 5mm.
 
    	**Download:**

    	DesignReport_1.1.4.2.2.pdf_. 

    	Example_1.1.4.2.2.osi_. 

	
1.2. Moment Connection
#######################
1.2.1. Beam-Beam
*******************
1.2.1.1. Cover Plate Connection
---------------------------------
1.2.1.1.1 Bolted connectivity
	
	
	*Sample problem 1*

		Design a bolted cover plate splice connection for beam UB 457x191x82 to transfer a factored external moment of 175kNm, factored shear of 115kN and factored axial force of 100kN. Use M20 Friction grip bolts of property class 8.8. Try 16mm thick flange splice plate and 10mm thick web splice plate. Take Fe410 grade steel (f\ :sub:`y` \  = 250 MPa,  f\ :sub:`u` = 410 MPa). Assume bolt hole type as standard, edge as hand flame cut, gap between the beams as 5mm and surface of the metal to be treated with sand blast.
	
 	DesignReport_1.2.1.1.1.1.pdf_.
	
	Example_1.2.1.1.1.1.osi_.


	*Sample problem 2 *
	
		Design a bolted cover plate splice connection for beam UB 406x178x67 to transfer a factored external moment of 150kNm, factored shear of 100kN and factored axial force of 75kN. Use M20 Friction grip bolts of property class 10.9. Try 14mm thick flange splice plate and 6mm thick web splice plate. Take Fe410 grade steel (f\ :sub:`y` \  = 250 MPa,  f\ :sub:`u` = 410 MPa). Assume bolt hole type as standard, edge as hand flame cut, gap between the beams as 5mm and surface of the metal to be treated with sand blast.
	
	**Download:**
	
	DesignReport_1.2.1.1.1.2.pdf_.
	
	Example_1.2.1.1.1.2.osi_.

	
	
1.2.1.2. End Plate Connection
--------------------------------
1.2.1.2.1 Extended Both Ways

	*Sample problem 1*
	
		 Design a bolted extended (both way) end plate spliced moment connection for a beam NPB 350x170x50.2, for transferring a factored reversible moment and shear force of 200 kNm and 150 kN. Use M20 bearing bolts of property class 9.8. Try an end plate 20 mm thick and groove weld (CJP). Take Fe410 grade steel (f\ :sub:`y` \  = 230 MPa,  f\ :sub:`u` = 450 MPa). The bolt hole type is standard. The type of weld is shop weld and the end plate is prepared by machine-flame cut.
		 				 
	**Download:**
	
	DesignReport_1.2.1.2.1.1.pdf_.
	
	Example_1.2.1.2.1.1.osi_.
	
	*Sample problem 2*
	
		Design a bolted extended (both way) end plate spliced moment connection for a beam UB 406 x 178 x 74, for transferring a factored reversible moment, shear force and axial force of 350 kNm, 120 kN and 50 kN, respectively. Use M16 friction grip bolts of property class 8.8. Try an end plate 20 mm thick and use groove weld. Take Fe410 grade steel (f\ :sub:`y` \  = 250 MPa,  f\ :sub:`u` = 410 MPa). Assume the bolts to be pre-tensioned, bolt hole type is standard and the slip factor is 0.48. The type of weld is shop weld and the edge type is sheared or hand flame cut.
				
	**Download:**
	
	DesignReport_1.2.1.2.1.2.pdf_.
	
	Example_1.2.1.2.1.2.osi_.

1.2.1.2.2 Extended One Way

	*Sample problem 1*
	
		Design a bolted extended One Way end plate spliced connection for a beam MB 400, to transfer a vertical factored shear force of 12kN, factored bending moment of 75kNm. Use M30 bearing bolts of property class  3.6. Try 16mm thick end plate with groove weld for flange and web. Take Fe410 grade steel (f\ :sub:`y` \  = 250 MPa,  f\ :sub:`u` = 410 MPa). The bearing bolt is non-pretensioned and the bolt hole type is oversized. The type of weld is shop weld and the edge type is sheared or hand flame cut.

	**Download:**
	
	DesignReport_1.2.1.2.2.1.pdf_.
	
	Example_1.2.1.2.2.1.osi_.

 	*Sample problem 2*
	
		Design a bolted extended One Way end plate spliced connection for a beam MB 400, to transfer a vertical factored shear force of 12kN and factored bending moment of 75kNm. Use M20 bearing bolts of grade 3.6. Try 14mm thick end plate with groove weld for flange and web . Take Fe410 grade steel (f\ :sub:`y` \  = 250 MPa,  f\ :sub:`u` = 410 MPa). The bearing bolt is non-pretensioned and the bolt hole type is oversized. The type of weld is shop weld and the edge type is sheared or hand flame cut.

	**Download:**
	
	DesignReport_1.2.1.2.2.2.pdf_.
	
	Example_1.2.1.2.2.2.osi_.


1.2.1.2.3 Flush Plate

	*Sample problem 1*

		Design a Flush end plate spliced connection for a beam MB 300, to transfer a vertical factored shear force of 25 kN and factored bending moment of 50kNm. Use M24 friction grip bolts of property class 8.8. Try 22mm thick end plate with 6mm fillet weld for flange and 6mm for web. Take Fe410 grade steel (f\ :sub:`y` \  = 250 MPa,  f\ :sub:`u` = 410 MPa). The friction grip bolts is non-pretensioned and the bolt hole type is oversized. The type of weld is shop weld and the edge type is sheared or hand flame cut.


	**Download:**
	
	DesignReport_1.2.1.2.3.1.pdf_.
	
	Example_1.2.1.2.3.1.osi_.

	*Sample problem 2*

		Design a Flush end plate spliced connection for a beam MB 300, to transfer a vertical factored shear force of 25kN and factored bending moment of 50kNm. Use M20 friction girp bolts of property class 8.8. Try 20mm thick end plate with 6mm fillet weld for flange and 5mm for web. Take Fe410 grade steel (f\ :sub:`y` \  = 250 MPa,  f\ :sub:`u` = 410 MPa). The bearing bolts is non-pretensioned and the bolt hole type is oversized. The type of weld is shop weld and the edge type is sheared or hand flame cut.


	**Download:**
	
	DesignReport_1.2.1.2.3.2.pdf_.
	
	Example_1.2.1.2.3.2.osi_.


1.2.2. Beam-Column
*******************
1.2.2.1. End Plate Connection
-------------------------------

1.2.2.1.1. Extended Both Ways

1.2.2.1.1.1 Column Flange-Beam Web (CFBW) connectivity


	*Sample problem 1*

		Design a bolted extented both ways end plate connection between a beam WPB 300x300x96.8 and a column UC 305 x 305 x 137 to transfer a vertical factored shear force of 35 kN, factored bending moment of 25kNm and factored axial force 12kN. Use M30 bearing bolts of property class 12.9. Try 26mm thick end plate with 10mm fillet weld for flange and 6mm fillet weld for web. Take Fe410 grade steel (f\ :sub:`y` \  = 250 MPa,  f\ :sub:`u` = 410 MPa). Assume bolt hole type as standard, weld type shop weld and type of edge as hand flame cut.
	
	**Download:**
	
	DesignReport_1.2.2.1.1.1.1.pdf_.
	
	Example_1.2.2.1.1.1.1.osi_.
	
	*Sample problem 2*
	
		Design a bolted extented both ways end plate connection between a beam WPB 300x300x96.8 and a column UC 305 x 305 x 137 to transfer a vertical factored shear force of 35 kN, factored bending moment of 25kNm and factored axial force 120kN. Use M30 bearing bolts of property class 12.9. Try 26mm thick end plate with 8mm fillet weld for flange and 6mm fillet weld for web. Take Fe410 grade steel (f\ :sub:`y` \  = 250 MPa,  f\ :sub:`u` = 410 MPa). Assume bolt hole type as standard, weld type shop weld and type of edge as hand flame cut.

	**Download:**
	
	DesignReport_1.2.2.1.1.1.2.pdf_.
	
	Example_1.2.2.1.1.1.2.osi_.

1.2.2.1.1.2 Column Web-Beam Web (CWBW) connectivity

	*Sample problem 1*
		
		Design a bolted extented both ways end plate connection between a beam WPB 240x240x60.3 and a column UC 305 x 305 x 137 to transfer a vertical factored shear force of 150 kN, factored bending moment of 12kNm and factored axial force 50kN. Use M30 friction grip bolts of property class 10.9. Try 26mm thick end plate with 10mm fillet weld for flange and 6mm for web. Take Fe410 grade steel (f\ :sub:`y` \  = 250 MPa,  f\ :sub:`u` = 410 MPa). Assume bolt hole type as standard, weld type shop weld and type of edge as hand flame cut.

	**Download:**
	
	DesignReport_1.2.2.1.1.2.1.pdf_.
	
	Example_1.2.2.1.1.2.1.osi_.


	*Sample problem 2*

		Design a bolted extended both ways end plate connection between a beam WPB 240x240x60.3 and a column UC 305 x 305 x 137 to transfer a vertical factored shear force of 150 kN, factored bending moment of 12kNm and factored axial force 50kN. Use M20 friction grip bolts of property class 10.9. Try 26mm thick end plate with 10mm fillet weld for flange and 6mm for web. Take Fe410 grade steel (f\ :sub:`y` \  = 250 MPa,  f\ :sub:`u` = 410 MPa). Assume bolt hole type as standard, weld type shop weld and type of edge as hand flame cut.

	**Download:**
	
	DesignReport_1.2.2.1.1.2.2.pdf_.
	
	Example_1.2.2.1.1.2.2.osi_.


1.2.2.1.2. Extended One Way.

1.2.2.1.2.1 Column Flange-Beam Web (CFBW) connectivity

	*Sample problem 1*

		Design a bolted extended one way end plate connection between a beam WPB 300x300x96.8 and a column UC 305 x 305 x 137 to transfer a vertical factored shear force of 35 kN, factored bending moment of 25kNm and factored axial force 12kN. Use M24 bearing bolts of property class 10.9. Try 26mm thick end plate with 10mm fillet weld for flange and 6mm for web. Take Fe410 grade steel (f\ :sub:`y` \  = 250 MPa,  f\ :sub:`u` = 410 MPa). Assume bolt hole type as standard, weld type shop weld and type of edge as hand flame cut.

	**Download:**
	
	DesignReport_1.2.2.1.2.1.1.pdf_.
	
	Example_1.2.2.1.2.1.1.osi_.
	
	*Sample problem 2*

		Design a bolted extented one way end plate connection between a beam WPB 300x300x96.8 and a column UC 305 x 305 x 137 to transfer a vertical factored shear force of 35kN, factored bending moment of 25kNm and factored axial force 120kN. Use M24 bearing bolts of property class 10.9. Try 26mm thick end plate with 10mm fillet weld for flange and 6mm for web. Take Fe410 grade steel (f\ :sub:`y` \  = 250 MPa,  f\ :sub:`u` = 410 MPa). Assume bolt hole type as standard, weld type shop weld and type of edge as hand flame cut.	

	**Download:**
	
	DesignReport_1.2.2.1.2.1.2.pdf_.
	
	Example_1.2.2.1.2.1.2.osi_.

1.2.2.1.2.2 Column Web-Beam Web (CWBW) connectivity
	
	*Sample problem 1*

		Design a bolted extented one way end plate connection between a beam WPB 240x240x60.3 and a column UC 305 x 305 x 137 to transfer a vertical factored shear force of 150 kN, factored bending moment of 12kNm and factored axial force 50kN. Use M24 friction grip bolts of property class 10.9. Try 24mm thick end plate with 8mm fillet weld for flange and 6mm for web. Take Fe410 grade steel (f\ :sub:`y` \  = 250 MPa,  f\ :sub:`u` = 410 MPa). Assume bolt hole type as standard, weld type shop weld and type of edge as hand flame cut.
	
	**Download:**
	
	DesignReport_1.2.2.1.2.2.1.pdf_.
	
	Example_1.2.2.1.2.2.1.osi_.

	*Sample problem 2*

		Design a bolted extended one way end plate connection between a beam WPB 240x240x60.3 and a column UC 305 x 305 x 137 to transfer a vertical factored shear force of 150 kN, factored bending moment of 12kNm and factored axial force 50kN. Use M20 friction grip bolts of property class 10.9. Try 24mm thick end plate with 8mm fillet weld for flange and 6mm for web. Take Fe410 grade steel (f\ :sub:`y` \  = 250 MPa,  f\ :sub:`u` = 410 MPa). Assume bolt hole type as standard, weld type shop weld and type of edge as hand flame cut.

	**Download:**
	
	DesignReport_1.2.2.1.2.2.2.pdf_.
	
	Example_1.2.2.1.2.2.2.osi_.


1.2.2.1.3. Flush Plate.

1.2.2.1.3.1 Column Flange-Beam Web (CFBW) connectivity


	*Sample problem 1*

		Design a bolted flush end plate connection between a beam WPB 300x300x96.8 and a column UC 305 x 305 x 137 to transfer a vertical factored shear force of 35 kN, factored bending moment of 25kNm and factored axial force 12kN. Use M30 bearing bolts of property class 12.9. Try 24mm thick end plate with 10mm fillet weld for flange and 6mm for web. Take Fe410 grade steel (f\ :sub:`y` \  = 250 MPa,  f\ :sub:`u` = 410 MPa). Assume bolt hole type as standard, weld type shop weld and type of edge as hand flame cut.

	**Download:**

	DesignReport_1.2.2.1.3.1.1.pdf_.
	
	Example_1.2.2.1.3.1.1.osi_.

	*Sample problem 2*

		Design a bolted flush end plate connection between a beam WPB 300x300x96.8 and a column UC 305 x 305 x 137 to transfer a vertical factored shear force of 35 kN, factored bending moment of 25kNm and factored axial force 12kN. Use M20 bearing bolts of property class 10.9. Try 24mm thick end plate with 10mm fillet weld for web and 6mm for flange. Take Fe410 grade steel (f\ :sub:`y` \  = 250 MPa,  f\ :sub:`u` = 410 MPa). Assume bolt hole type as standard, weld type shop weld and type of edge as hand flame cut.

	**Download:**

	DesignReport_1.2.2.1.3.1.2.pdf_.
	
	Example_1.2.2.1.3.1.2.osi_.

1.2.2.1.3.2 Column Web-Beam Web (CWBW) connectivity

	*Sample problem 1*

		Design a bolted flush end plate connection between a beam NPB 160x80x15.8 and a column UC 305 x 305 x 97 to transfer a vertical factored shear force of 20kN, factored bending moment of 15kNm and factored axial force 15kN. Use M16 bearing bolts of property class 8.8. Try 20mm thick end plate with groove weld for flange and web. Take Fe410 grade steel (f\ :sub:`y` \  = 250 MPa,  f\ :sub:`u` = 410 MPa). Assume bolt hole type as standard, weld type shop weld and type of edge as hand flame cut.

	**Download:**

	DesignReport_1.2.2.1.3.2.1.pdf_.
	
	Example_1.2.2.1.3.2.1.osi_.

	*Sample problem 2*

		Design a bolted flush end plate connection between a beam WPB 240x240x60.3 and a column UC 305 x 305 x 137 to transfer a vertical factored shear force of 50 kN, factored bending moment of 75kNm and factored axial force 25kN. Use M20 friction grip bolts of property class 10.9. Try 24mm thick end plate with 6mm fillet weld for flange and 6mm for web. Take Fe410 grade steel (f\ :sub:`y` \  = 250 MPa,  f\ :sub:`u` = 410 MPa). Assume bolt hole type as standard, weld type shop weld and type of edge as hand flame cut.
	
	**Download:**

	DesignReport_1.2.2.1.3.2.2.pdf_.
	
	Example_1.2.2.1.3.2.2.osi_.
















	

1.3. Truss Connection
#######################


Comments, questions, suggestions? See the Feedback_. page to contact Osdag. Copyright © 2017 Osdag. All rights reserved.


.. _Homepage: http://osdag.fossee.in
 
.. _Feedback: http://osdag.fossee.in/forums

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

.. _DesignReport_1.1.4.2.3.pdf: \DesignReport_1.1.4.2.3.pdf
.. _Example_1.1.4.2.3.osi: \Example_1.1.4.2.3.osi

.. _DesignReport_1.2.1.1.1.1.pdf: \DesignReport_1.2.1.1.1.1.pdf 
.. _Example_1.2.1.1.1.1.osi: \Example_1.2.1.1.1.1.osi

.. _DesignReport_1.2.1.1.1.2.pdf: \DesignReport_1.2.1.1.1.2.pdf 
.. _Example_1.2.1.1.1.2.osi: \Example_1.2.1.1.1.2.osi


.. _DesignReport_1.2.1.2.1.1.pdf: \DesignReport_1.2.1.2.1.1.pdf
.. _Example_1.2.1.2.1.1.osi: \Example_1.2.1.2.1.1.osi


.. _DesignReport_1.2.1.2.1.2.pdf: \DesignReport_1.2.1.2.1.2.pdf
.. _Example_1.2.1.2.1.2.osi: \Example_1.2.1.2.1.2.osi

.. _DesignReport_1.2.1.2.2.1.pdf: \DesignReport_1.2.1.2.2.1.pdf
.. _Example_1.2.1.2.2.1.osi: \Example_1.2.1.2.2.1.osi

.. _DesignReport_1.2.1.2.2.2.pdf: \DesignReport_1.2.1.2.2.2.pdf
.. _Example_1.2.1.2.2.2.osi: \Example_1.2.1.2.2.2.osi


.. _DesignReport_1.2.1.2.3.1.pdf: \DesignReport_1.2.1.2.3.1.pdf
.. _Example_1.2.1.2.3.1.osi: \Example_1.2.1.2.3.1.osi

.. _DesignReport_1.2.1.2.3.2.pdf: \DesignReport_1.2.1.2.3.2.pdf
.. _Example_1.2.1.2.3.2.osi: \Example_1.2.1.2.3.2.osi



.. _DesignReport_1.2.2.1.1.1.1.pdf: \DesignReport_1.2.2.1.1.1.1.pdf
.. _Example_1.2.2.1.1.1.1.osi: \Example_1.2.2.1.1.1.1.osi


.. _DesignReport_1.2.2.1.1.1.2.pdf: \DesignReport_1.2.2.1.1.1.2.pdf
.. _Example_1.2.2.1.1.1.2.osi: \Example_1.2.2.1.1.1.2.osi


.. _DesignReport_1.2.2.1.1.2.1.pdf: \DesignReport_1.2.2.1.1.2.1.pdf 
.. _Example_1.2.2.1.1.2.1.osi: \Example_1.2.2.1.1.2.1.osi


.. _DesignReport_1.2.2.1.1.2.2.pdf: \DesignReport_1.2.2.1.1.2.2.pdf
	
.. _Example_1.2.2.1.1.2.2.osi: \Example_1.2.2.1.1.2.2.osi


.. _DesignReport_1.2.2.1.2.1.1.pdf: \DesignReport_1.2.2.1.2.1.1.pdf
	
.. _Example_1.2.2.1.2.1.1.osi: \Example_1.2.2.1.2.1.1.osi


.. _DesignReport_1.2.2.1.2.1.2.pdf: \DesignReport_1.2.2.1.2.1.2.pdf
	
.. _Example_1.2.2.1.2.1.2.osi: \Example_1.2.2.1.2.1.2.osi


.. _DesignReport_1.2.2.1.2.2.1.pdf: \DesignReport_1.2.2.1.2.2.1.pdf
	
.. _Example_1.2.2.1.2.2.1.osi: \Example_1.2.2.1.2.2.1.osi


.. _DesignReport_1.2.2.1.2.2.2.pdf: \DesignReport_1.2.2.1.2.2.2.pdf
	
.. _Example_1.2.2.1.2.2.2.osi: \Example_1.2.2.1.2.2.2.osi


.. _DesignReport_1.2.2.1.3.1.1.pdf: \DesignReport_1.2.2.1.3.1.1.pdf
	
.. _Example_1.2.2.1.3.1.1.osi: \Example_1.2.2.1.3.1.1.osi


.. _DesignReport_1.2.2.1.3.1.2.pdf: \DesignReport_1.2.2.1.3.1.2.pdf
	
.. _Example_1.2.2.1.3.1.2.osi: \Example_1.2.2.1.3.1.2.osi


.. _DesignReport_1.2.2.1.3.2.1.pdf: \DesignReport_1.2.2.1.3.2.1.pdf
	
.. _Example_1.2.2.1.3.2.1.osi: \Example_1.2.2.1.3.2.1.osi


.. _DesignReport_1.2.2.1.3.2.2.pdf: \DesignReport_1.2.2.1.3.2.2.pdf
	
.. _Example_1.2.2.1.3.2.2.osi: \Example_1.2.2.1.3.2.2.osi




.. toctree::
   :maxdepth: 2
   :caption: Contents:

   
   
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

