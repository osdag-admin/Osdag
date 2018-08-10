<p align="center"> 
  <img src = "https://user-images.githubusercontent.com/19147922/27816506-9f15355a-60a9-11e7-98cc-585312264801.png"><br>
  Open steel design and graphics <br><br>
  <a href="http://osdag.fossee.in/">Osdag</a><br><br>
  Osdag is a cross-platform, free, and open-source software for the design and detailing of steel structures.
</p>

## Table of contents
* <a href="#quick-start">Quick start</a>
* <a href="#contribute">Contributing</a>
* <a href="#bugs">Bugs and known issues</a>
* <a href="#version">Versioning</a>
* <a href="#license">Copyright and license</a>

## <a id="user-content-quick-start" class="anchor" href="#quick-start" aria-hidden="true"></a> Quick start

<a href= "http://osdag.fossee.in/resources/downloads">Download the latest release version 2017.08.a.e2dd</a>
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
        Minimum 4 Gb free storage space recommended        
        

#### Basic User:
 
    Installation steps:
    ===================
    # If you have already installed the  previous version of Osdag in your system then skip step 1) & 2) and just run the new downloaded 	Osdag_setup_x86.exe.
    # See Advanced-User section below, before you execute these steps.
    1) Run Miniconda2-latest-Windows-x86.exe
        # Follow on-screen instructions AND select the following options in the Setup:
	NOTE: Installation of Miniconda2-latest-Windows-x86 is mandatory in 'C drive' only.
        a) Install for: [All Users (requires admin privileges)]
        b) Destination Folder: ["C:\Program Files (x86)\Miniconda2"]
				1. After selecting the “Program Files (x86)\” directory, manually type “Miniconda2” (without quotes)
				2. If an error message appears saying, “The installation directory has 2 spaces”, ignore it by clicking OK.
        c) Advanced Options: Check both the options:
            i) Add Anaconda to my PATH environment variable
            ii) Register Anaconda as my default Python 2.7            
    2) Run Osdag_setup_x86.exe    and follow on-screen instructions
        # The default directory to install Osdag is the User’s Desktop.
        You may choose any other location. However, DO NOT choose any of the following locations:
            a) Program Files  
            b) Program Files (x86)
            c) ProgramData
    
    Running Osdag:
    ==============
    After the installation is complete, you may run Osdag by one of the following methods:
        i) double-clicking on the Desktop shortcut or
        ii) double-clicking on the Start Menu shortcut or
        iii) navigating to the installation-directory and double-clicking on the Osdag shortcut
    

#### Advanced User:
    # If you have already installed the  previous version of Osdag in your system then skip step 1) & 2) and just run the new downloaded Osdag_setup_x86.exe.

    Criteria:
    =========
    If you satisfy one of the following two conditions, then you will need to follow a different installation procedure.  
    Condition a) You already use Anaconda/Miniconda
    Condition b) You have already installed a version of python on your computer AND you wish to keep that as the system default instead of the Miniconda(/Anaconda)-python
    
    Installation:
    =============
    1) Run wkhtmltox-0.12.4_msvc2015-win32.exe
        # Follow on-screen instructions AND select the following option in the Setup:
        a) Destination Folder: ["C:\Program Files (x86)\wkhtmltopdf"]
        
    2) Miniconda
        a) If you already are a Miniconda/Anaconda user:-
            i) Navigate to the "dependencies" folder in the installation-directory
            ii) Open the "install_osdag_dependencies.bat" in a text editor and  
            iii) Manually install the missing python packages listed in the .bat file, through conda.            
            iv) In Step 3 ("Run Osdag_setup_x86"), when the installer prompts if you have Miniconda installed, just close the window and let the installer continue.
        b) If you do not have Miniconda installed and are OK with installing it and but do not wish to Register Anaconda as the default Python 2.7:
            i) First install Miniconda2-latest-Windows-x86.exe (same as the basic user) BUT follow the steps in the "Running Osdag" section below, instead of the "Running Osdag" steps of the basic user.
    3) Run Osdag_setup_x86.exe and follow on-screen instructions
        # The default directory to install Osdag is the User Desktop.  
        You may choose any other location. However, DO NOT choose any of the following locations:
            a) Program Files  
            b) Program Files (x86)
            c) ProgramData    
    
    Running Osdag:
    =============
    You need navigate to the Osdag-installation folder, in a command prompt, and use the following command to run Osdag:
        python osdagMainPage.py
        # You need to replace 'python' in the above command with python from the miniconda-package, if you opted not to register it as the system default python
    You may choose to create a batch file that contains the above command and create a shortcut to Run Osdag.

### 2. Ubuntu Installation

#### System Requirements:
    Operating System: 
        Ubuntu 14.04 (LTS) and later; 64-bit
    Hardware Requirements:
        Minimum 4 Gb RAM
        Minimum of 2 Gb of free disk space
 
    This setup script is for machines running Ubuntu that do not have Miniconda2.  
    If you have Miniconda2 already installed on your computer, please skip Step/Command 1 and proceed to Step/Command 2.
 

    Installation steps:
    ===================
      Extract the downloaded installer using the Archive Manager/File-Roller, or using the following command on the bash prompt: tar -xvf Osdag_ubuntu_installer.tar.gz

      # If you have already installed the  previous version of Osdag in your system then skip Step/Command 1) and just run the new 2-install-osdag.sh.

      In bash, navigate to the extracted installation folder containing the shell scripts (the folder that contains this README file)
      and a folder named Osdag, and enter Command 1 and Command 2 given below.  

      Note: After entering Command 1, while installing Miniconda2, you will be asked whether you wish to set the system default python
      to Miniconda2. You need to agree to this, in order for the second command to work. Alternatively, you may manually execute the 
      steps in the script 2-install-osdag.sh, and specify the python version while calling pip to install pdfkit.

      Step/Command 1:
          bash 1-install-Miniconda2-latest-Linux-x86_64.sh
      Step/Command 2:
          bash 2-install-osdag.sh


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
Anyone and everyone is welcome to contribute. It's through your contributions that Osdag will continue to improve. Please take a moment to review the <a href= "https://github.com/osdag-admin/Osdag/blob/master/CONTRIBUTING.md">guidelines for contributing</a>.

   * Bug reports
   * Feature requests
   * Pull requests

## <a id="user-content-bugs" class="anchor" href="#bugs" aria-hidden="true"></a> Bugs and known issues
Have a bug or a feature request? Please first read the <a href= "https://github.com/osdag-admin/Osdag/blob/master/CONTRIBUTING.md#using-the-issue-tracker">issue guidelines</a> and search for existing and closed issues. If your problem or idea is not addressed yet, please <a href= "https://github.com/osdag-admin/Osdag/issues/new">open a new issue</a> or at <a href= "http://osdag.fossee.in/forums"> Osdag forum</a>.

## <a id="user-content-version" class="anchor" href="#version" aria-hidden="true"></a> Versioning
This beta version of Osdag contains only the shear connection modules. Starting with version of Osdag 2017.06.a.874e. The latest version of Osdag 2017.08.a.e2dd is available with bugs fixed.

## <a id="user-content-license" class="anchor" href="#license" aria-hidden="true"></a> Copyright and license
(c) Copyright Osdag contributors 2017.<br>
This program comes with ABSOLUTELY NO WARRANTY. This is free software, and you are welcome to redistribute it under certain conditions. See the <a href="https://github.com/osdag-admin/Osdag/files/1207162/License.txt">License.txt</a> file for details regarding the license.
The beta version of Osdag is released under the terms and conditions of the GNU LESSER GENERAL PUBLIC LICENSE (LGPL) Version 3.
