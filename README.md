

# Osdag
### Open Steel design and graphics

Osdag is a cross-platform free and open-source software for the design (and detailing) of steel structures, following the Indian Standard IS 800:2007.

It allows the user to design steel connections, members and systems using a graphical user interface. The interactive GUI provides a 3D visualisation of the designed component and creates images for construction/fabrication drawings.

The design is typically optimised following industry best practices. In the preliminary stages, Osdag's development focuses mainly on connection designs.

Osdag is primarily built upon Python other Python-based FOSS tools, such as, PyQt, OpenCascade, and PythonOCC. It uses SQLite for managing steel section databases. Osdag is currently under development. An alpha version of Osdag containing a few connection design modules is expected to be released in April, 2017.


-------------------------------------------------------------------
## Downlaod and install dependencies

1) Download [miniconda](https://conda.io/miniconda.html)
then in your terminal window type the following and follow the prompts on the installer screens.
 bash Miniconda3-latest-Linux-x86_64.sh

2) Clone osdag repository:
git clone https://github.com/osdag-admin/Osdag.git

3) Create virtual environment and install dependencies.
conda env create -f environment.yml

4) In your terminal window type the following:
python osdagMainPage.py
