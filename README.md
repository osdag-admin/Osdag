<p align="center"> 
  <img src = "https://user-images.githubusercontent.com/19147922/27816506-9f15355a-60a9-11e7-98cc-585312264801.png"><br>
  Open Steel Design and Graphics <br><br>
  <a href="http://osdag.fossee.in/">Osdag</a><br><br>
  Osdag is a cross-platform free/libre and open-source software for the design (and detailing) of steel structures, following the Indian Standard IS 800:2007. It allows the user to design steel connections, members and systems using a graphical user interface. The interactive GUI provides a 3D visualisation of the designed component and an option to export the CAD model to any drafting software for the creation of construction/fabrication drawings. The design is typically optimised following industry best practices.
  Starting with version 2017.06.a.e2dd, the beta version of Osdag is released under the terms and conditions of the GNU LESSER GENERAL PUBLIC LICENSE (LGPL) Version 3.

</p>

---

## Table of Contents

- [Quick Start](#quick-start)
  - [Windows Installation](#1-windows-installation)
  - [Conda Installation](#2-conda-installation)
- [Contributing](#contributing)
- [Bugs and Known Issues](#bugs-and-known-issues)
- [Versioning](#versioning)
- [Copyright and License](#copyright-and-license)

---

## Quick Start

**[Download the latest version of Osdag](http://osdag.fossee.in/resources/downloads)**

### 1. Windows Installation

```
System Requirements:

    Supported Operating Systems:
        Windows Vista
        Windows 7
        Windows 8
        Windows 8.1
        Windows 10
        Windows 11
    
    Supported Architecture:
        64-bit
    
    RAM and Storage Space:
        Minimum 4 GB RAM recommended
        Minimum 3 GB free storage space recommended


Installation Steps:
===================

Uninstalling Earlier Version of Osdag:

    If you have a previous version of Osdag installed then it is mandatory to uninstall the same.
    
        i) Go to the location where Osdag was installed and run "Uninstall.exe".

# Note: If you have an active Antivirus package installed on your system please disable it 
  during the installation of Osdag. Since Osdag is not registered with the Microsoft store, 
  the antivirus might block installation/running of Osdag. Osdag does not install any harmful 
  package on your system.

To install Osdag, Run Osdag_windows_installer.exe

# Follow on-screen instructions AND select the following options in the Setup:

        i)   Double click on the Osdag_windows_installer.exe to start the installation process.
        ii)  Click Next.
        iii) Read the License and click 'I Agree' to proceed.
        iv)  Select the installation directory after checking the space requirement and click Next.
        v)   Click Install.
        vi)  The installation process will continue. After the process ends, click the Finish button.

    Osdag will be successfully installed!


Running Osdag:
==============

After the installation is complete, you may run Osdag by one of the following methods:

        i)   Double-clicking on the Desktop shortcut or
        ii)  Press the Windows key and search Osdag
        iii) Navigating to the installation-directory and double-clicking on the Osdag shortcut
```

---

### 2. Conda Installation

```
System Requirements:

    Hardware Requirements:
        Minimum 4 GB RAM
        Minimum 3 GB free disk space

    Prerequisites:
        This setup script is for machines running Ubuntu, Windows or macOS that do not have 
        Miniconda3. If you have Miniconda3 already installed on your computer, please skip 
        Step 1 and proceed to Step 2.
```

#### Installation Steps

**1. Install Miniconda3**

Install [Miniconda3](https://docs.anaconda.com/miniconda/install/) if not installed already. Select your operating system. Any other installation giving access to the latest conda version (e.g., Anaconda, miniforge, etc.) is also acceptable.

**2. Install LaTeX Distribution**

Install [MikTeX](https://miktex.org/howto/install-miktex) (for Windows) / [TeX Live](http://www.tug.org/texlive) (for Linux or other OS). This will be needed to generate reports.

- **For MikTeX:** Make sure to select "Install for yourself". Once the installation is complete, open MikTeX Console, click on "Check for updates". Click "Update now" if there is any update available.

- **For TeX Live:** The package `texlive-full` may have to be installed to avoid a "missing packages" error (more details below).

**3. Open the Conda-Enabled Shell**

Instructions are available on the Miniconda3 installations page.

- **For Windows:** Open the Anaconda Command Prompt or Anaconda PowerShell Prompt. These should be available from the start menu after installation.

- **For Linux:** Open the terminal (use `Ctrl+Alt+T`)

**4. Create Osdag Environment**

Run this command. This will create a new environment and install Osdag in it. It may take several minutes to get the prompt back.

```bash
conda create -n osdag-env osdag::osdag -c conda-forge
```

**5. Run Osdag**

To run Osdag, from the same shell, run these two commands. This will open the Osdag main page. 

```bash
conda activate osdag-env
osdag
```

> **Note:** Running Osdag will create a folder "ResourceFiles" where this command is run. This folder will be used to store data for use in subsequent runs (for example, input values for various modules).

**6. Verify Installation**

Attempt a sample problem to make sure everything is working.

**7. LaTeX Package Installation**

During the first run, when creating the design report, some LaTeX packages may have to be installed before the report can be compiled. MikTeX will generally attempt to do this right then, but may fail if it was installed as an administrator. TeX Live is generally installed as an administrator (i.e., with sudo), so you may have to install `texlive-full` first.

**8. Future Usage**

To run Osdag in the future, follow Step 5 from the same folder. This will not require an internet connection (except for installing missing packages as described in Step 7).

**9. Update Osdag**

Occasionally, update Osdag as new updates may have been added since the install.

```bash
conda activate osdag-env
conda update osdag
```

#### Alternative Installation (if issues occur)

In case of issues during Steps 3 or 4, i.e., in case Osdag is not installed or does not run, you could try to use the alternative mamba solver:

**1. Activate the environment**

```bash
conda activate osdag-env
```

**2. Install mamba**

```bash
conda install mamba
```

**3. Install Osdag using mamba**

```bash
mamba install osdag::osdag -c conda-forge
```

---

## Contributing

Osdag invites enthusiasts with similar interests to contribute to Osdag development. Your contributions can go a long way in improving the software.

Please take a moment to review the [guidelines for contributing](https://github.com/osdag-admin/Osdag/blob/master/CONTRIBUTING.md).

**Ways to Contribute:**
- Bug reports
- Feature requests
- Pull requests

---

## Bugs and Known Issues

Have a bug or a feature request? Please first read the [issue guidelines](https://github.com/osdag-admin/Osdag/blob/master/CONTRIBUTING.md#using-the-issue-tracker) and search for existing and closed issues.

If your problem or idea has not been addressed yet, please:
- [Open a new issue](https://github.com/osdag-admin/Osdag/issues/new), or
- Post a query [on the Osdag discussion forum](https://osdag.fossee.in/forum)

---

## Versioning

### Current Version Features

The latest version of Osdag can perform design for two scenarios:

**Scenario 1: Optimum Design**

Users can obtain the optimum design for a given scenario from a suite of available options in terms of:
- Steel sections (e.g., different channel sizes and plate thicknesses)
- Connectors (e.g., bolts of different grades and diameters)

The optimum design is selected based on the total volume of material, and this design solution is detailed in the output dock and design report.

**Scenario 2: Design Check**

Perform a design check with a specific set of single inputs/selections in the 'Customized' option. In this case, Osdag will inform if the design checks are satisfied and suggest changes otherwise.

### Key Improvements

- The Design Report has been reformatted using the LaTeX software system through the PyLaTeX package
- The report is much more detailed and shows step-by-step calculations for a better user experience
- Shear and Moment connections, Slab and Gusseted Base Plates, Tension Members, Compression Members, and Flexural Members have been modified in terms of structure at the backend, GUI, and calculations
- Known bugs have been fixed

### Available Modules

The latest version of Osdag contains the following modules (in addition to those available with previous versions):

#### Connections

**Plate(d) Connections:**
- Lap Joint - Bolted
- Lap Joint - Welded
- Butt Joint - Bolted
- Butt Joint - Welded

#### Compression Member

- Strut - Bolted to End Gusset
- Strut - Welded to End Gusset
- Axially Loaded Columns

#### Flexural Member

- Plate Girder

---

### Previous Releases

#### Version 2025_01_a_2

- New modules have been added to Osdag:
  - **Compression Member:** Strut in Trusses
  - **Flexural Member:** Simply Supported Beam, Cantilever Beam
- The process of creating the CAD models has been optimized to reduce the time required
- A more streamlined conda-based installer is available to allow for smoother installation and updating. Once installed, users can update Osdag without the need for reinstallation

#### Version 2017.08.a.874e

- Bugs fixed

#### Version 2017.06.a.e2dd

- This beta version of Osdag contains only the shear connection modules

---

**Contributors**

The contributors of the latest version are acknowledged in [CONTRIBUTORS.md](https://github.com/osdag-admin/Osdag/blob/dev/src/osdag_core/data/doc/CONTRIBUTORS.MD)

---

## Copyright and License

Copyright © Osdag contributors 2020.

This program comes with ABSOLUTELY NO WARRANTY. This is free software, and you are welcome to redistribute it under certain conditions. See the [License.txt](https://github.com/osdag-admin/Osdag/files/1207162/License.txt) file for details regarding the license.

The beta version of Osdag is released under the terms and conditions of the **GNU LESSER GENERAL PUBLIC LICENSE (LGPL) Version 3**.