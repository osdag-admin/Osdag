<p align="center"> 
  <img src = "https://user-images.githubusercontent.com/19147922/27816506-9f15355a-60a9-11e7-98cc-585312264801.png"><br>
  Open Steel Design and Graphics <br><br>
  <a href="http://osdag.fossee.in/">Osdag</a><br><br>
  Osdag is a cross-platform free/libre and open-source software for the design (and detailing) of steel structures, following the Indian Standard IS 800:2007. It allows the user to design steel connections, members and systems using a graphical user interface. The interactive GUI provides a 3D visualisation of the designed component and an option to export the CAD model to any drafting software for the creation of construction/fabrication drawings. The design is typically optimised following industry best practices.
  Starting with version 2017.06.a.e2dd, the beta version of Osdag is released under the terms and conditions of the GNU LESSER GENERAL PUBLIC LICENSE (LGPL) Version 3.

</p>

## Table of contents
* <a href="#quick-start">Quick start</a>
* <a href="#contribute">Contributing</a>
* <a href="#bugs">Bugs and known issues</a>
* <a href="#version">Versioning</a>
* <a href="#license">Copyright and license</a>

## <a id="user-content-quick-start" class="anchor" href="#quick-start" aria-hidden="true"></a> Quick start

<a href= "http://osdag.fossee.in/resources/downloads">Download the latest version of Osdag</a>

### 1. Windows Installation

#### System Requirements:
    Supported Operating Systems:
        Windows Vista
        Windows 7,
        Windows 8,
        Windows 8.1,
        Windows 10
    Supported Architecture:
             64-bit
    RAM and Storage Space:
        Minimum 2 Gb RAM recommended
        Minimum 1 Gb free storage space recommended
        
	
    Installation steps:
    ===================
    
    Uninstalling Earlier Version of Osdag: If you have a previous version of Osdag installed then it is mandatory to uninstall the same.
    
    		i) Go to the location where Osdag was installed and run "Uninstall.exe".
   
    # Note: If you have an active Antivirus package installed on your system please disable it during the installation of Osdag. Since, Osdag is not registered with the Microsoft store, the antivirus might block installation/running of Osdag. Osdag does not install any harmful package on your system.
    
    To install Osdag, Run Osdag_windows_setup.exe
    
    # Follow on-screen instructions AND select the following options in the Setup:
    
        	i)    Double click on the Osdag_windows_installer.exe to start the start the installation process. 
		ii)   Click Next.
		iii)  Read the License and click 'I Agree' to proceed.
		iv)   Select the installation directory after checking the space requirement and click Next.
		v)    Click Install.
		vi)   Wait for the installation process to get over (this might take several minutes).
		vii)  Accept the MiKTeX license and click Next.
		Viii) Choose the MiKTeX installation scope and click Next.
		ix)   Select the installation directory and click Next.
		x)    Keep the MiKTeX setting to default and click Next.
		xi)   Click start to install MiKTeX.
		xii)  Click Next.
		Xiii) (optional) You can check for MiKTeX package updates.
		xiv)  Click Close to exit the MiKTeX setup wizard.
		xv)   The installation process will continue. After the process ends, click the Finish button.
	
	Osdag will be successfully installed!
    
    Running Osdag:
    ==============
    After the installation is complete, you may run Osdag by one of the following methods:
    
    		i)   Double-clicking on the Desktop shortcut or
		ii)  Press the Windows key and search Osdag 
		iii) Navigating to the installation-directory and double-clicking on the Osdag shortcut

    

### 2. Ubuntu Installation

#### System Requirements:
    Operating System: 
        Ubuntu 14.04 (LTS) and later; 64-bit
    Hardware Requirements:
        Minimum 4 Gb RAM
        Minimum of 1 Gb of free disk space
 
    This setup script is for machines running Ubuntu that do not have Miniconda3.  
    If you have Miniconda3 already installed on your computer, please skip Step/Command 1 and proceed to Step/Command 2.
 

    Installation steps:
    ===================
      Extract the downloaded installer using the Archive Manager/File-Roller, or using the following command on the bash prompt: tar -xvf Osdag_ubuntu_installer.tar.gz

      # If you have already installed the  previous version of Osdag in your system then skip Step/Command 1) and just run the new 2-install-osdag.sh.

		In bash, navigate to the extracted installation folder containing the shell 
		scripts (the folder that contains this README file) and a folder named Osdag, 
		and enter Command 1 , Command 2 and Command 3 given below.  
		 
			Note: After entering Command 1, while installing Miniconda3, you will be asked  
		whether you wish to set the system default python to Miniconda3. You need to agree  
		to this.After that you have to run command 2 in order for the 3rd command to work.
		After that execute the 3rd steps. After 3rd step completed run the command 4.Please be sure 
		to have internet connection as it's required to download some files.
			Step/Command 1:
				bash 1-install-Miniconda3-latest-Linux-x86_64.sh
			 Step/Command 2:
			bash 2-init-conda_base.sh
			Step/Command 3:
				bash 3-install-osdag.sh
			Step/Command 4:
			bash 4-install-texlive.sh


    Running Osdag:
    =============
      After the installation is complete, you may copy/move the extracted Osdag folder to a location of your choice (say, directly under your home folder). 
      You can run Osdag in two ways
      1) Using the Osdag Launcher:
          To run Osdag, navigate to the Osdag folder, double click on the file named Osdag (without any extension). 
          This file is different from Osdag_icon.ico (although both will show the Osdag logo in the grid icon view mode).
          If you are using the Unity desktop, you may also pin this launcher to the launcher sidebar.

      2) Using the Command:
          In the bash prompt, navigate to the Osdag directory and enter the following command python osdagMainPage.py

      Note that, Step/Command 2 will work only if the system default python is the one installed through Miniconda2.
      Alternatively, you may specify the (installed) python you wish to use, in Command 2.

## <a id="user-content-contribute" class="anchor" href="#bugs" aria-hidden="true"></a> Contributing
Osdag invites enthusiasts with similar interest(s) to contribute to Osdag development. Your contributions can go a long way in improving the software.
Please take a moment to review the <a href= "https://github.com/osdag-admin/Osdag/blob/master/CONTRIBUTING.md">guidelines for contributing</a>.

   * Bug reports
   * Feature requests
   * Pull requests

## <a id="user-content-bugs" class="anchor" href="#bugs" aria-hidden="true"></a> Bugs and known issues
Have a bug or a feature request? Please first read the <a href= "https://github.com/osdag-admin/Osdag/blob/master/CONTRIBUTING.md#using-the-issue-tracker">issue guidelines</a> and search for existing and closed issues. If your problem or idea has not been addressed yet, please <a href= "https://github.com/osdag-admin/Osdag/issues/new">open a new issue</a> or post a query <a href= "https://osdag.fossee.in/forum"> on the Osdags discussion forum</a>.

## <a id="user-content-version" class="anchor" href="#version" aria-hidden="true"></a> Versioning
The latest version of Osdag can perform design for two scenarios;

Scenario 1: Users can obtain the optimum design for a given scenario, from a suite of available options in terms of steel sections (e.g., different channel sizes and plate thicknesses) and connectors (e.g., bolts of different grades and diameters). The optimum design is selected based on the total volume of material and this design solution is detailed in the output dock and design report.

Scenario 2: Perform a design check with a specific set of single inputs/selections in the 'Customized' option. In this case, Osdag will inform if the design checks are satisfied and suggest changes otherwise. 

The Design Report has been reformatted using the LaTeX software system through the PyLaTeX package. The report is much more detailed and shows step-by-step calculation(s) for a better user experience.

The Shear and Moment connections available with the previous versions have been modified in terms of structure at the backend, GUI and calculations. Any know bug(s) have been fixed. 

The latest version of Osdag contains the following modules (in addition to the ones available with the previous versions):

    Beam-Beam Splice Connection

        Beam-Beam Cover Plate Bolted
        Beam-Beam End Plate
        Beam-Beam Cover Plate Welded

    Beam-Column Connection
        
        Beam-Column End Plate

    Column-Column Splice Connection

        Column-Column Cover Plate Bolted
        Column-Column Cover Plate Welded
        Column-Column End Plate

    Base Plate Connection 
    
    Tension Member

        Tension Member Bolted
        Tension Member Welded

Previous Releases

Version 2017.08.a.874e

    Bugs fixed

Version 2017.06.a.e2dd

    This beta version of Osdag contains only the shear connection modules.

===============================================
The contributors of the latest version are:

Osdag development team (2019 - Present)

===============================

Project Investigator - Osdag

Professor Siddhartha Ghosh

===============================

Research Associates/Assistants - Technical and Development Team

Mr. Danish Ansari

Mr. Ajmal Babu MS

Mr. N Dharma Teja

Ms. Thushara Pushkaran

Mr. Yash Lokhande

Mr. Anand Swaroop

Mr. Darshan Divesan

Mr. Anjali Jatav

Mr. Sourabh Das

Ms. Deepthi Reddy

===============================

Project Interns

Mr. Ansari Mohammad Umair 

Mr. Amir Chappalwala

Mr. Zunzunia Arsil

Mr. Mohammad Azhar U Din Mir

Mr. Satyam Singh Niranjan

Mr. Anshul Kumar Singh

Mr. Mosam Patel

Mr. Shahadad PP

Ms. Priti Kumari

===============================

Project Management

Ms. Usha Viswanathan

Ms. Vineeta Parmar

Mr. Sunil Shetye

===============================

Web, Graphics, Promotions and System Administrators Team

Ms. Sashi Rekha B M K

Mr. Lee Thomas Stephen

Mr. Rohan Mhatre

Mr. Khushal Singh Rajput

Mr. Yash Vohra

===============================

Office Staff

Ms.Komal Solanki

Mr.Vishal Birare

Mr. Sushant Bammkanti

===============================

Acknowledgements:

Ministry of Education (MoE), Govt. of India

FOSSEE

Professor Kannan Moudgalya

Professor Prabhu Ramachandran

Mr. Sunil Shetye

## <a id="user-content-license" class="anchor" href="#license" aria-hidden="true"></a> Copyright and license
(c) Copyright Osdag contributors 2020.<br>
This program comes with ABSOLUTELY NO WARRANTY. This is free software, and you are welcome to redistribute it under certain conditions. See the <a href="https://github.com/osdag-admin/Osdag/files/1207162/License.txt">License.txt</a> file for details regarding the license.
The beta version of Osdag is released under the terms and conditions of the GNU LESSER GENERAL PUBLIC LICENSE (LGPL) Version 3.

=============================== End of File ===============================
