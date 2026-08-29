import os
import shutil
import pytest
import tempfile
import socket
from pylatex import Document, Section, Command, Tabular, Subsection, Tabularx, NewPage, Package, PageStyle, Head, Foot, Tabularx, MultiColumn, StandAloneGraphic, NoEscape
from pylatex.utils import NoEscape
from pylatex.errors import CompilerError
import subprocess
import sys
from importlib.resources import files
from datetime import datetime

# Get texmf-dist root from package
# Absolute path to the texmf-dist folder of osdag-latex-env
LATEX_ENV_PATH = os.path.abspath(os.path.join("ResourceFiles", "osdag-latex-env"))
TEXMF_DIST = os.path.join(LATEX_ENV_PATH, "texmf-dist")
# Set TEXMFHOME to point to our LaTeX environment (optional, for tools like kpsewhich)
os.environ["TEXMFHOME"] = TEXMF_DIST

# Set TEXINPUTS so pdflatex can find the required .cls and .sty files
texinputs_dirs = [
    os.path.join(TEXMF_DIST, "tex", "latex", "base"),
    os.path.join(TEXMF_DIST, "tex", "latex"),
    TEXMF_DIST,
    "",  # fallback to system paths if needed
]
os.environ["TEXINPUTS"] = os.pathsep.join(texinputs_dirs)

LATEX_ENV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'ResourceFiles', 'osdag-latex-env'))
FALLBACK_PDFLATEX_PATH = os.path.join(LATEX_ENV_PATH, 'bin', 'windows', 'pdflatex.exe')
PDFLATEX_PATH = shutil.which("pdflatex") or FALLBACK_PDFLATEX_PATH

REQUIRED_STY_FILES = [
    "lastpage.sty", "parskip.sty", "kvoptions.sty", "ltxcmds.sty", "kvsetkeys.sty",
    "geometry.sty", "needspace.sty", "multirow.sty", "colortbl.sty",
    "fancyhdr.sty", "latexmk.pl", "amsmath.sty", "article.sty", "color.sty",
    "fontenc.sty", "graphicx.sty", "inputenc.sty", "lmodern.sty",
    "longtable.sty", "tabularx.sty", "xcolor.sty"
]

diagnostics_log = []
test_counter = [1]

def is_pdflatex_in_path():
    return shutil.which("pdflatex") is not None

def is_pdflatex_in_osdag_env():
    return os.path.exists(FALLBACK_PDFLATEX_PATH)

def find_sty_file(root_dir, target_file):
    for dirpath, _, filenames in os.walk(root_dir):
        if target_file in filenames:
            return os.path.join(dirpath, target_file)
    return None

# === Test 1: pdflatex availability ===
def test_pdflatex_available():
    in_path = is_pdflatex_in_path()
    in_env = is_pdflatex_in_osdag_env()
    available = in_path or in_env
    diagnostics_log.append(f"Test {test_counter[0]} - pdflatex availability: {'PASSED' if available else 'FAILED'}")
    test_counter[0] += 1
    assert available, "pdflatex is not installed globally or in osdag-latex-env"

# === Test 2: latexmk presence ===
def test_latexmk_present():
    latexmk_path = os.path.join(LATEX_ENV_PATH, 'bin', 'windows', 'latexmk.exe')
    exists = os.path.exists(latexmk_path)
    diagnostics_log.append(f"Test {test_counter[0]} - latexmk presence: {'PASSED' if exists else 'FAILED'}")
    test_counter[0] += 1
    assert exists, "latexmk executable not found in osdag-latex-env"

# === Test 3: Check .sty files ===
@pytest.mark.parametrize("sty_file", REQUIRED_STY_FILES)
def test_required_sty_files_present(sty_file):
    found = find_sty_file(LATEX_ENV_PATH, sty_file) is not None
    diagnostics_log.append(f"Test {test_counter[0]} - {sty_file}: {'PASSED' if found else 'FAILED'}")
    test_counter[0] += 1
    assert found, f"{sty_file} not found in LaTeX environment"


def test_compile_latex_with_pylatex():

    os.environ['TEXMFHOME'] = os.path.abspath("ResourceFiles/osdag-latex-env/texmf-dist")
    os.environ["TEXINPUTS"] = os.path.abspath("ResourceFiles/osdag-latex-env/texmf-dist") + os.pathsep + os.environ.get("TEXINPUTS", "")

    sty_pkgs = os.path.abspath(os.path.join("ResourceFiles", "osdag-latex-env", "texmf-dist"))
    sty_pkgs = sty_pkgs.replace("\\", "/")  # Normalize path for LaTeX on Windows
    pkg_resources = [f'{sty_pkgs}/amsmath', f'{sty_pkgs}/graphics', f'{sty_pkgs}/needspace']
    texinp = os.environ.get('TEXINPUTS', ' ')
    pkg_path = ";".join(pkg_resources)
    os.environ['TEXINPUTS'] = f'{pkg_path};{texinp}'

    geometry_options = {
        "a4paper": True,
        "top": "2cm",
        "bottom": "2cm",
        "left": "2.5cm",
        "right": "2.5cm"
    }

    doc = Document(documentclass="article", geometry_options=geometry_options)

    # Import all packages
    doc.packages.append(Package('inputenc', options='utf8'))
    doc.packages.append(Package('fontenc', options='T1'))
    doc.packages.append(Package('lmodern'))
    doc.packages.append(Package('amsmath'))
    doc.packages.append(Package('graphicx'))
    doc.packages.append(Package('xcolor'))
    doc.packages.append(Package('color'))
    doc.packages.append(Package('fancyhdr'))
    doc.packages.append(Package('geometry'))
    doc.packages.append(Package('lastpage'))
    doc.packages.append(Package('multirow'))
    doc.packages.append(Package('colortbl'))
    doc.packages.append(Package('array'))
    doc.packages.append(Package('longtable'))
    doc.packages.append(Package('tabularx'))
    doc.packages.append(Package('needspace'))
    doc.packages.append(Package('parskip'))
    doc.packages.append(Package('ltxcmds'))
    doc.packages.append(Package('kvoptions'))
    doc.packages.append(Package('kvsetkeys'))

    doc.preamble.append(NoEscape(r'''
            \usepackage{fancyhdr}
            \pagestyle{fancy}
            \renewcommand{\headrulewidth}{0pt}

            \fancyhead[L]{
            \begin{minipage}[t]{0.6\textwidth}
                \vspace{-1em}
                {\Large\bfseries Osdag Diagnostics Report - Test 4} \\[0.5em]
                {\small \today}
            \end{minipage}
        }

        '''))



    doc.append('This document confirms the successful import and basic usage of essential .sty files used by Osdag.\n')

    with doc.create(Subsection('amsmath')):
        doc.append(NoEscape(r'$\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}$'))

    with doc.create(Subsection('xcolor & color')):
        doc.append(NoEscape(r'\definecolor{OsdagGreen}{RGB}{153,169,36}'))
        doc.append(NoEscape(r'\textcolor{OsdagGreen}{This is Osdag Green Colour}'))

    with doc.create(Subsection('multirow, colortbl, array')):
        doc.append(NoEscape(r'''
\begin{tabular}{|c|c|}
\hline
\multirow{2}{*}{A} & Row 1 \\
                   & Row 2 \\
\hline
\end{tabular}
'''))

    with doc.create(Subsection('longtable, tabularx')):
        doc.append(NoEscape(r'''
\rowcolors{2}{gray!10}{white}
\begin{longtable}{|>{\raggedright\arraybackslash}p{4cm}|p{9cm}|}
\hline
Feature & Description \\
\hline
Color Alternating & Tested with colortbl and xcolor \\
Custom Column Align & Tested with array \\
Auto Page-Break Table & longtable allows breaking \\
\hline
\end{longtable}
'''))

    # Export
    doc.generate_pdf('test4_latex_testing_suite', clean=True, compiler=PDFLATEX_PATH, clean_tex=False)
    diagnostics_log.append(f"Test {test_counter[0]} - LaTeX compilation with all .sty files: PASSED")
    test_counter[0] += 1

# === Test 4: Final Compilation Report ===
def test_compile_latex_with_pylatex_report():

    # Set LaTeX environment paths
    os.environ['TEXMFHOME'] = os.path.abspath("ResourceFiles/osdag-latex-env/texmf-dist")
    os.environ["TEXINPUTS"] = os.path.abspath("ResourceFiles/osdag-latex-env/texmf-dist") + os.pathsep + os.environ.get("TEXINPUTS", "")

    sty_pkgs = os.path.abspath(os.path.join("ResourceFiles", "osdag-latex-env", "texmf-dist"))
    sty_pkgs = sty_pkgs.replace("\\", "/")  # Normalize path for LaTeX on Windows
    pkg_resources = [f'{sty_pkgs}/amsmath', f'{sty_pkgs}/graphics', f'{sty_pkgs}/needspace']
    texinp = os.environ.get('TEXINPUTS', ' ')
    pkg_path = ";".join(pkg_resources)
    os.environ['TEXINPUTS'] = f'{pkg_path};{texinp}'
    base_dir = os.path.dirname(os.path.abspath(__file__))
    pkg_images = os.path.join(base_dir, "ResourceFiles", "images")
    geometry_options = {
        "a4paper": True,
        "top": "4cm",
        "hmargin": "2cm",
        "headheight": "100pt",
        "footskip": "100pt",
        "bottom": "2.5cm"
    }
    imgpath_osdagheader = os.path.join(pkg_images, "Osdag_header_report.png").replace("\\", "/")
    doc = Document(documentclass="article", geometry_options=geometry_options)

    doc.packages.append(Package('inputenc', options='utf8'))
    doc.packages.append(Package('graphicx'))
    doc.packages.append(Package('lmodern'))
    doc.preamble.append(NoEscape(r'\renewcommand{\familydefault}{\sfdefault}'))
    doc.packages.append(Package('helvet'))
    doc.packages.append(Package('fancyhdr'))
    doc.packages.append(Package('xcolor'))
    doc.packages.append(Package('array'))
    doc.packages.append(Package('xcolor', options='table'))

    # Add Osdag green color
    doc.preamble.append(NoEscape(r'\definecolor{OsdagGreen}{RGB}{153,169,36}'))

    # Add Osdag header image
    doc.preamble.append(NoEscape(r'''
        \usepackage{fancyhdr}
        \pagestyle{fancy}
        \renewcommand{\headrulewidth}{1pt}

        \fancyhead[L]{
        \begin{minipage}[t]{0.6\textwidth}
            \vspace{-3em}
            {\Large\bfseries Osdag Diagnostics Report} \\[0.5em]
            {\small \today}
        \end{minipage}
    }

        \fancyhead[R]{
            \begin{minipage}[t]{0.3\textwidth}
    '''))

    # Insert the image with StandAloneGraphic
    doc.preamble.append(StandAloneGraphic(image_options="width=4.40cm,height=1.1cm",filename=imgpath_osdagheader))

    doc.preamble.append(NoEscape(r'''
            \end{minipage}
        }
    '''))
    current_time = datetime.now().strftime("%d-%m-%Y | %H:%M:%S")
    # Add metadata table
    with doc.create(Tabular(r'|>{\raggedright\arraybackslash}p{5cm}||>{\raggedright\arraybackslash}p{10cm}|')) as table:

        table.add_hline()
        table.add_row(('Test', 'LaTex Testing Suite'), color='OsdagGreen')
        table.add_hline()
        table.add_row(('Date & Time', current_time), color='OsdagGreen')
        table.add_hline()
        table.add_row(('Computer Name', f'{socket.gethostname()}'), color='OsdagGreen')
        table.add_hline()
        table.add_row(('User', f'{os.getlogin()}'), color='OsdagGreen')
        table.add_hline()

    # Description section
    with doc.create(Section("Checks Done:", numbering=False)):
        doc.append(NoEscape(r'''
            The current LaTeX testing suite checks for the presence of the following dependencies:
            \begin{itemize}
                \item Presence of pdflatex.exe either in system path or present in osdag\_latex\_env/bin/windows
                \item Presence of latexmk.exe
                \item Presence of the essential .sty files. Also includes all .sty files used by any .tex file generated by Osdag currently for any module.
                \item Calls each of the essential .sty files and compiles a sample report where each package is used. If compilation is successful it deletes the .tex file and resultant .pdf, .aux, .log. If compilation is unsuccessful, the test fails i.e either a .sty package is corrupt or it is missing.
            \end{itemize}
        '''))

    diagnostics_log.append(f"Test {test_counter[0]} - Osdag Diagnostics Report compilation: PASSED")
    test_counter[0] += 1

    # Results Table
    with doc.create(Section("Tests", numbering=False)):
        doc.append("Each test conducted is listed below along with its result:")
        doc.append(NoEscape(r'\newline\newline'))

        with doc.create(Tabular('|l|l|')) as table:
            table.add_hline()
            table.add_row(('Check Performed', 'Result'))
            table.add_hline()
            for entry in diagnostics_log:
                if ' - ' in entry:
                    test_name, result = entry.split(":")
                    table.add_row((test_name.strip(), result.strip()))
                    table.add_hline()

    # Compile
    doc.generate_pdf('osdag_diagnostics_report', compiler=PDFLATEX_PATH, clean=True, clean_tex=False)


all_passed = all("PASSED" in entry for entry in diagnostics_log)
if __name__ == "__main__":
    # Run all tests explicitly
    test_pdflatex_available()
    test_latexmk_present()
    for sty_file in REQUIRED_STY_FILES:
        test_required_sty_files_present(sty_file)
    test_compile_latex_with_pylatex()
    test_compile_latex_with_pylatex_report()

    # Check if all tests passed
    all_passed = all("PASSED" in entry for entry in diagnostics_log)
    print(0 if all_passed else 1)



