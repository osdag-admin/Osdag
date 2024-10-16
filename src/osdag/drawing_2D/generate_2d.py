import os

from OCC.Core.gp import gp_Dir
from OCC.src.Display.WebGl.jupyter_renderer import JupyterRenderer
from OCC.src.Extend.DataExchange import read_step_file, export_shape_to_svg




my_renderer = JupyterRenderer()
robot_shp = read_step_file(os.path.join('..', '..','..', 'workspace', 'untitled.stp'))
my_renderer.DisplayShapeAsSVG(robot_shp, direction=gp_Dir(1, 1, 0.1),
                              export_hidden_edges=False,
                              line_width=1.5)