from math import sqrt
from ocp_vscode import show, show_object, reset_show, set_port, set_defaults, get_defaults
set_port(3939)
from build123d import *

ts_inner_dia = 75.0
ts_outer_dia = 85.0
handle_support_offset = 9.0
ts_height = 79.0
ear_width = 28.0
ear_nut_depth = 0.0
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
    with BuildSketch() as hs_sk:
        r = 10.0 # handle_support_offset / 2
        x = ts_outer_dia/2 + handle_support_offset - r
        y = handle_dia/2
        oc = Circle(ts_outer_dia/2)
        with Locations((x, -y), (x, +y)):
            Circle(radius=r)
        make_hull(hs_sk.edges())
        Circle(ts_inner_dia / 2, mode=Mode.SUBTRACT)
    extrude(amount=ts_height)


    # portafilter wings
    if (ear_nut_depth > 0.0):
        with BuildSketch(ts.faces().sort_by(Axis.Z)[-1]):
            Rectangle(ear_width, ts_outer_dia)
        extrude(amount=-ear_nut_depth, mode=Mode.SUBTRACT)

    # chamfer the handle support
    with BuildSketch(Plane.XZ) as hs2_sk:
        with BuildLine():
            top_w = 13.0
            len = 15.0
            l1 = Line((ts_outer_dia/2, ts_height), (ts_outer_dia/2, ts_height-top_w))
            l1b = JernArc(l1@1, l1%1, r, arc_size=45)
            l2 = PolarLine(l1b@1, len, -45.0)
            l3 = Line(l2 @ 1, ((l2 @ 1).X, ts_height))
            l4 = Line(l3@1, l1@0)
        make_face()
    revolve(axis=Axis.Z, mode=Mode.SUBTRACT)

    # slot for the handle
    if True:
        with BuildSketch(Plane.YZ):
            with Locations((0,handle_center_height)):
                Circle(handle_dia/2)
                Rectangle(handle_dia, ts_height, align=(Align.CENTER, Align.MIN))
        extrude(amount=ts_outer_dia, mode=Mode.SUBTRACT)

    sel = ts.edges().filter_by(GeomType.HYPERBOLA) + ts.edges().filter_by(GeomType.BSPLINE)
    sel1 = sel.filter_by_position(Axis.Y, minimum=-ts_inner_dia/2, maximum=-handle_dia/2-1.0) + sel.filter_by_position(Axis.Y, minimum=handle_dia/2+.1, maximum=ts_inner_dia/2)


    sel2 = ts.edges().filter_by_position(Axis.Y,
                                         minimum=-handle_dia/2,
                                         maximum=handle_dia/2
                                         ).filter_by_position(Axis.Z,
                                                              minimum=ts_height/2,
                                                              maximum=ts_height
                                                              ) 
    fillet(sel1, radius=5.5)
    fillet(sel2, radius=0.6)

show(ts)

ts.part.export_step("tamping-station.step")