from ocp_vscode import show, show_object, reset_show, set_port, set_defaults, get_defaults
set_port(3939)
from build123d import *

ts_inner_dia = 75.0
ts_outer_dia = 85.0
ts_handle_support_offset = ts_outer_dia - ts_inner_dia
ts_height = 79.0
ear_width = 28.0
ear_nut_depth = 7.5
handle_dia = 18.0
handle_z_offset = 31.0

handle_center_height = ts_height - ear_nut_depth - handle_z_offset + handle_dia/2

with BuildPart() as ts:
    # main body
    with BuildSketch() as sk1:
        Circle(ts_outer_dia / 2)
        Circle(ts_inner_dia / 2, mode=Mode.SUBTRACT)
    extrude(amount=ts_height)
    # handle support
    with BuildSketch() as sk1:
        Rectangle(ts_outer_dia / 2 + ts_handle_support_offset, 
                  handle_dia + ts_handle_support_offset, 
                  align=(Align.MIN, Align.CENTER))
        Circle(ts_inner_dia / 2, mode=Mode.SUBTRACT)
    extrude(amount=handle_center_height)
    # portafilter wings
    with BuildSketch(ts.faces().sort_by(Axis.Z)[-1]):
        Rectangle(ear_width, ts_outer_dia)
    extrude(amount=-ear_nut_depth, mode=Mode.SUBTRACT)
    # slot for the handle
    with BuildSketch(Plane.YZ):
        with Locations((0,handle_center_height)):
            Circle(handle_dia/2)
            Rectangle(handle_dia, ts_height, align=(Align.CENTER, Align.MIN))
    extrude(amount=ts_outer_dia, mode=Mode.SUBTRACT)
    fillet(ts.edges().filter_by_position(Axis.Z,minimum=ts_height - ear_nut_depth, maximum=ts_height), radius=1)

show(ts)

ts.part.export_step("tamping-station.step")