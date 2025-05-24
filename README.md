<div align="center">
  <img src="https://user-images.githubusercontent.com/19147922/27816506-9f15355a-60a9-11e7-98cc-585312264801.png" alt="Osdag Logo">
  <h1>Osdag - Open Steel Design and Graphics</h1>
  <p><a href="http://osdag.fossee.in/">Official Website</a></p>
  <p>
    Osdag is a cross-platform free/libre and open-source software for the design (and detailing) of steel structures, following the Indian Standard IS 800:2007. It allows the user to design steel connections, members and systems using a graphical user interface. The interactive GUI provides a 3D visualisation of the designed component and an option to export the CAD model to any drafting software for the creation of construction/fabrication drawings. The design is typically optimised following industry best practices.
  </p>
  <p>
    <i>Starting with version 2017.06.a.e2dd, the beta version of Osdag is released under the terms and conditions of the GNU LESSER GENERAL PUBLIC LICENSE (LGPL) Version 3.</i>
  </p>
</div>

## Table of Contents

* [Quick Start](#quick-start)
* [Building from Source](#building-from-source)
* [Contributing](#contribute)
* [Bugs and Known Issues](#bugs)
* [Versioning](#version)
* [Copyright and License](#license)

## <a id="quick-start"></a>Quick Start

**[Download the latest version of Osdag](http://osdag.fossee.in/resources/downloads)**

### 1. Windows Installation

#### System Requirements

* **Supported Operating Systems:**
  * Windows Vista
  * Windows 7
  * Windows 8
  * Windows 8.1
  * Windows 10
* **Supported Architecture:**
  * 64-bit
* **RAM and Storage Space:**
  * Minimum 2 Gb RAM recommended
  * Minimum 1 Gb free storage space recommended

#### Installation Steps

**Before Installation:**

* If you have a previous version of Osdag installed, it is mandatory to uninstall it first.
  * Go to the location where Osdag was installed and run "Uninstall.exe".
* **Note:** If you have an active Antivirus package installed on your system, please disable it during the installation. Since Osdag is not registered with the Microsoft store, the antivirus might block installation/running of Osdag. Osdag does not install any harmful packages on your system.

**Installation Process:**

1. Double click on the Osdag_windows_installer.exe to start the installation process
2. Click Next
3. Read the License and click 'I Agree' to proceed
4. Select the installation directory after checking the space requirement and click Next
5. Click Install
6. Wait for the installation process to complete (this might take several minutes)
7. Accept the MiKTeX license and click Next
8. Choose the MiKTeX installation scope and click Next
9. Select the installation directory and click Next
10. Keep the MiKTeX setting to default and click Next
11. Click start to install MiKTeX
12. Click Next
13. (optional) You can check for MiKTeX package updates
14. Click Close to exit the MiKTeX setup wizard
15. The installation process will continue. After the process ends, click the Finish button

Osdag will be successfully installed!

#### Running Osdag

After the installation is complete, you may run Osdag by one of the following methods:

1. Double-clicking on the Desktop shortcut
2. Press the Windows key and search Osdag
3. Navigating to the installation-directory and double-clicking on the Osdag shortcut

### 2. Ubuntu Installation

#### System Requirements

* **Operating System:**
  * Ubuntu 14.04 (LTS) and later; 64-bit
* **Hardware Requirements:**
  * Minimum 4 Gb RAM
  * Minimum of 1 Gb of free disk space

> This setup script is for machines running Ubuntu that do not have Miniconda3.  
> If you have Miniconda3 already installed on your computer, please skip Step/Command 1 and proceed to Step/Command 2.

#### Installation Steps

1. Extract the downloaded installer using the Archive Manager/File-Roller, or using the following command on the bash prompt:

   ```
   tar -xvf Osdag_ubuntu_installer.tar.gz
   ```

2. If you have already installed the previous version of Osdag in your system, skip Step/Command 1 and just run the new 2-install-osdag.sh.

3. In bash, navigate to the extracted installation folder containing the shell scripts (the folder that contains this README file) and a folder named Osdag, and enter the following commands:

   > **Note:** After entering Command 1, while installing Miniconda3, you will be asked whether you wish to set the system default python to Miniconda3. You need to agree to this. After that, run command 2 in order for the 3rd command to work. Then execute the 3rd step. After the 3rd step is completed, run command 4. Please ensure you have an internet connection as it's required to download some files.

   **Step/Command 1:**

   ```
   bash 1-install-Miniconda3-latest-Linux-x86_64.sh
   ```

   **Step/Command 2:**

   ```
   bash 2-init-conda_base.sh
   ```

   **Step/Command 3:**

   ```
   bash 3-install-osdag.sh
   ```

   **Step/Command 4:**

   ```
   bash 4-install-texlive.sh
   ```

#### Running Osdag

After the installation is complete, you may copy/move the extracted Osdag folder to a location of your choice (say, directly under your home folder).

You can run Osdag in two ways:

1. **Using the Osdag Launcher:**
   * Navigate to the Osdag folder, double click on the file named Osdag (without any extension)
   * This file is different from Osdag_icon.ico (although both will show the Osdag logo in the grid icon view mode)
   * If you are using the Unity desktop, you may also pin this launcher to the launcher sidebar

2. **Using the Command:**
   * In the bash prompt, navigate to the Osdag directory and enter the following command:

     ```
     python osdagMainPage.py
     ```

> Note that Step/Command 2 will work only if the system default python is the one installed through Miniconda2. Alternatively, you may specify the (installed) python you wish to use, in Command 2.

## <a id="building-from-source"></a>Building from Source

These instructions are for users who want to build Osdag from the latest source code. This might be for development purposes, to access the very latest changes, or for operating system distributions where pre-built Osdag packages are not yet available.

### General Prerequisites

* **Git:** Required for cloning the Osdag repository
* **Python:** Python 3.8 or newer is recommended. We suggest using Python 3.9 for best compatibility with dependencies
* **Miniconda or Anaconda:** Highly recommended for managing Python dependencies, especially for complex packages like PyQt5 and OpenCASCADE (python-occ-core). You can download Miniconda from [here](https://docs.conda.io/en/latest/miniconda.html)

### Generic Build/Setup Steps

1. **Clone the Repository:**  
   Open your terminal or command prompt and run the following commands:

   ```
   git clone https://github.com/osdag-admin/Osdag.git
   cd Osdag
   ```

2. **Create and Activate Conda Environment:**  
   We recommend creating a dedicated Conda environment for Osdag to avoid conflicts with other Python projects.

   ```
   # We recommend Python 3.9, but 3.8, 3.10, 3.11 should also work. 
   # Python 3.12+ might have issues with some dependencies at the time of writing.
   conda create -n osdag_dev python=3.9 -y
   conda activate osdag_dev
   ```

3. **Install Core Dependencies (PyQt5, OpenCASCADE, and others via Conda):**  
   Conda is preferred for installing PyQt5 and python-occ-core as it handles their complex binary dependencies effectively.

   ```
   # For OpenCASCADE (python-occ-core) and PyQt
   conda install -c conda-forge python-occ-core=7.7 pyqt=5 -y 
   # For other Python packages
   conda install -c anaconda numpy pyyaml requests pynput -y
   # Note: pynput might be optional depending on the features you need.
   ```

4. **Install Remaining Python Dependencies (using pip):**  
   Some dependencies are listed in `requirements.txt` and can be installed using pip. If packages like `numpy` or `pyyaml` were already installed by Conda, pip will recognize them.

   ```
   pip install -r requirements.txt
   ```

### Install TeXLive (for PDF Report Generation)

A comprehensive TeXLive installation is required for Osdag to generate PDF design reports.

* **Ubuntu/Debian-based Systems:**

  ```
  sudo apt-get update
  sudo apt-get install texlive-full -y 
  # Alternatively, for a more targeted installation, you can refer to the packages
  # listed in the script src/osdag/texlive/texlive_install.sh and install their
  # equivalents using your package manager.
  ```

* **Fedora/RHEL-based Systems:**

  ```
  sudo dnf install texlive-scheme-full -y 
  # For older versions, you might need to use 'yum' instead of 'dnf'.
  ```

* **Arch Linux:**

  ```
  sudo pacman -S texlive-most --noconfirm
  ```

* **Windows:**  
  It is recommended to install MiKTeX (which is typically included with the Osdag Windows installer) or a full TeX Live distribution (see [TeX Live net-install](https://www.tug.org/texlive/acquire-netinstall.html)). Ensure that `pdflatex` and all necessary TeX packages are accessible from your system's PATH environment variable.

* **macOS:**  
  Install MacTeX, which provides a full TeX Live distribution. You can find it at [MacTeX website](https://www.tug.org/mactex/).

### Running Osdag from Source

Once all prerequisites and dependencies are installed, and your Conda environment (`osdag_dev`) is activated, you can run Osdag using:

```
python src/osdag/osdagMainPage.py
```

### Troubleshooting Notes

* **Conda Environment:** Always ensure your Conda environment (`osdag_dev`) is activated before attempting to run Osdag or install packages
* **Graphics Issues:** If you encounter problems with the 3D graphics rendering, make sure your system's graphics drivers are up to date
* **OpenCASCADE/PyQt5 Installation:** If you face issues installing `python-occ-core` or `PyQt5`, the `conda-forge` channel is generally the most reliable source for pre-compiled packages that work across different platforms
* **PDF Report Failures:** If Osdag fails to generate PDF reports, it usually indicates an incomplete TeXLive installation. Ensure your TeXLive distribution is comprehensive. The script `src/osdag/texlive/texlive_install.sh` provides a list of many required TeX packages; ensure their equivalents are installed in your TeX distribution

## <a id="contribute"></a>Contributing

Osdag invites enthusiasts with similar interest(s) to contribute to Osdag development. Your contributions can go a long way in improving the software.
Please take a moment to review the [guidelines for contributing](https://github.com/osdag-admin/Osdag/blob/master/CONTRIBUTING.md).

* Bug reports
* Feature requests
* Pull requests

## <a id="bugs"></a>Bugs and Known Issues

Have a bug or a feature request? Please first read the [issue guidelines](https://github.com/osdag-admin/Osdag/blob/master/CONTRIBUTING.md#using-the-issue-tracker) and search for existing and closed issues. If your problem or idea has not been addressed yet, please [open a new issue](https://github.com/osdag-admin/Osdag/issues/new) or post a query [on the Osdag discussion forum](https://osdag.fossee.in/forum).

## <a id="version"></a>Versioning

The latest version of Osdag can perform design for two scenarios:

**Scenario 1:** Users can obtain the optimum design for a given scenario, from a suite of available options in terms of steel sections (e.g., different channel sizes and plate thicknesses) and connectors (e.g., bolts of different grades and diameters). The optimum design is selected based on the total volume of material and this design solution is detailed in the output dock and design report.

**Scenario 2:** Perform a design check with a specific set of single inputs/selections in the 'Customized' option. In this case, Osdag will inform if the design checks are satisfied and suggest changes otherwise.

The Design Report has been reformatted using the LaTeX software system through the PyLaTeX package. The report is much more detailed and shows step-by-step calculation(s) for a better user experience.

The Shear and Moment connections available with the previous versions have been modified in terms of structure at the backend, GUI and calculations. Any known bug(s) have been fixed.

### The Latest Version of Osdag Contains the Following Modules

* **Beam-Beam Splice Connection**
  * Beam-Beam Cover Plate Bolted
  * Beam-Beam End Plate
  * Beam-Beam Cover Plate Welded

* **Beam-Column Connection**
  * Beam-Column End Plate

* **Column-Column Splice Connection**
  * Column-Column Cover Plate Bolted
  * Column-Column Cover Plate Welded
  * Column-Column End Plate

* **Base Plate Connection**

* **Tension Member**
  * Tension Member Bolted
  * Tension Member Welded

### Previous Releases

**Version 2017.08.a.874e**

* Bugs fixed

**Version 2017.06.a.e2dd**

* This beta version of Osdag contained only the shear connection modules

### Contributors

The contributors of the latest version are:

**Osdag Development Team (2019 - Present)**

#### Project Investigator - Osdag

* Professor Siddhartha Ghosh

#### Research Associates/Assistants - Technical and Development Team

* Mr. Danish Ansari
* Mr. Ajmal Babu MS
* Mr. N Dharma Teja
* Ms. Thushara Pushkaran
* Mr. Yash Lokhande
* Mr. Anand Swaroop
* Mr. Darshan Divesan
* Mr. Anjali Jatav
* Mr. Sourabh Das
* Ms. Deepthi Reddy

#### Project Interns

* Mr. Ansari Mohammad Umair
* Mr. Amir Chappalwala
* Mr. Zunzunia Arsil
* Mr. Mohammad Azhar U Din Mir
* Mr. Satyam Singh Niranjan
* Mr. Anshul Kumar Singh
* Mr. Mosam Patel
* Mr. Shahadad PP
* Ms. Priti Kumari

#### Project Management

* Ms. Usha Viswanathan
* Ms. Vineeta Parmar
* Mr. Sunil Shetye

#### Web, Graphics, Promotions and System Administrators Team

* Ms. Sashi Rekha B M K
* Mr. Lee Thomas Stephen
* Mr. Rohan Mhatre
* Mr. Khushal Singh Rajput
* Mr. Yash Vohra

#### Office Staff

* Ms. Komal Solanki
* Mr. Vishal Birare
* Mr. Sushant Bammkanti

#### Acknowledgements

* Ministry of Education (MoE), Govt. of India
* FOSSEE
* Professor Kannan Moudgalya
* Professor Prabhu Ramachandran
* Mr. Sunil Shetye

## <a id="license"></a>Copyright and License

(c) Copyright Osdag contributors 2020.

This program comes with ABSOLUTELY NO WARRANTY. This is free software, and you are welcome to redistribute it under certain conditions. See the [License.txt](https://github.com/osdag-admin/Osdag/files/1207162/License.txt) file for details regarding the license.

The beta version of Osdag is released under the terms and conditions of the GNU LESSER GENERAL PUBLIC LICENSE (LGPL) Version 3.
