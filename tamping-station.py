from ocp_vscode import show, show_object, reset_show, set_port, set_defaults, get_defaults
set_port(3939)
from build123d import *

ts_inner_dia = 75.0
ts_outer_dia = 85.0
ts_height = 79.0
wing_width = 28.0
wing_nut_depth = 7.5
handle_dia = 18.0
handle_z_offset = 31.0

with BuildPart() as ts:
    with BuildSketch() as sk1:
        Circle(ts_outer_dia / 2)
        Circle(ts_inner_dia / 2, mode=Mode.SUBTRACT)
    extrude(amount=ts_height)
    with BuildSketch(ts.faces().sort_by(Axis.Z)[-1]):
        Rectangle(ts_outer_dia, wing_width)
    extrude(amount=-wing_nut_depth, mode=Mode.SUBTRACT)
    with BuildSketch(Plane.XZ):
        with Locations((0,ts_height - wing_nut_depth - handle_z_offset)):
            Circle(handle_dia/2, align=(Align.CENTER, Align.MIN))
        with Locations((0,ts_height - wing_nut_depth - handle_z_offset + handle_dia/2)):
            Rectangle(handle_dia, ts_height, align=(Align.CENTER, Align.MIN))
    extrude(amount=ts_outer_dia, mode=Mode.SUBTRACT)


show(ts)
