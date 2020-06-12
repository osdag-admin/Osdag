<<<<<<< HEAD
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

<a href= "http://osdag.fossee.in/resources/downloads">Download the latest release version 2020.08.a.e2dd</a>
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
        

#### Basic User:
 
    Installation steps:
    ===================
    # If you have already installed the  previous version of Osdag in your system then Unistall it first and just run the new downloaded Osdag_windows_setup.exe.
	  Run Osdag_windows_setup.exe
        # Follow on-screen instructions AND select the following options in the Setup:
		i)Just after starting the setup their is two options 1.Osdag and 2.Miktex, if you already have latex install in your system ,untick option 2.miktex and click next.
		ii)Click next, then install.
		iii)Select the install location and click install.
		iv)After process ends, click the finish botton.
    
    Running Osdag:
    ==============
    After the installation is complete, you may run Osdag by one of the following methods:
        i) double-clicking on the Desktop shortcut or
        ii) double-clicking on the Start Menu shortcut or
        iii) navigating to the installation-directory and double-clicking on the Osdag shortcut
    

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
Anyone and everyone is welcome to contribute. It's through your contributions that Osdag will continue to improve. Please take a moment to review the <a href= "https://github.com/osdag-admin/Osdag/blob/master/CONTRIBUTING.md">guidelines for contributing</a>.

   * Bug reports
   * Feature requests
   * Pull requests

## <a id="user-content-bugs" class="anchor" href="#bugs" aria-hidden="true"></a> Bugs and known issues
Have a bug or a feature request? Please first read the <a href= "https://github.com/osdag-admin/Osdag/blob/master/CONTRIBUTING.md#using-the-issue-tracker">issue guidelines</a> and search for existing and closed issues. If your problem or idea is not addressed yet, please <a href= "https://github.com/osdag-admin/Osdag/issues/new">open a new issue</a> or at <a href= "http://osdag.fossee.in/forums"> Osdag forum</a>.

## <a id="user-content-version" class="anchor" href="#version" aria-hidden="true"></a> Versioning
This beta version of Osdag contains only the shear connection modules. Starting with version of Osdag 2017.06.a.874e. The latest version of Osdag 2017.08.a.e2dd is available with bugs fixed.

## <a id="user-content-license" class="anchor" href="#license" aria-hidden="true"></a> Copyright and license
(c) Copyright Osdag contributors 2020.<br>
This program comes with ABSOLUTELY NO WARRANTY. This is free software, and you are welcome to redistribute it under certain conditions. See the <a href="https://github.com/osdag-admin/Osdag/files/1207162/License.txt">License.txt</a> file for details regarding the license.
The beta version of Osdag is released under the terms and conditions of the GNU LESSER GENERAL PUBLIC LICENSE (LGPL) Version 3.
=======
# Osdag_refactored
>>>>>>> restructuring
