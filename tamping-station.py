from ocp_vscode import show, show_object, reset_show, set_port, set_defaults, get_defaults
set_port(3939)
from build123d import *

ts_inner_dia = 75.0
ts_outer_dia = 85.0
ts_height = 75.0
handle_dia = 18.0
handle_z_offset = 33.0

with BuildPart() as ts:
    # handle support
    with BuildSketch() as hs_sk:
        x = ts_outer_dia / 2 - 2.0
        y = handle_dia / 2
        Circle(ts_outer_dia / 2)
        with Locations((x, -y), (x, +y)):
            Circle(10.0)
        make_hull(hs_sk.edges())
        Circle(ts_inner_dia / 2, mode=Mode.SUBTRACT)
    extrude(amount=ts_height)

    # chamfer the handle support
    with BuildSketch(Plane.XZ) as hsc_sk:
        with BuildLine():
            l1 = Line((ts_outer_dia / 2, ts_height), 
                      (ts_outer_dia / 2, ts_height - 13.0))
            l2 = JernArc(l1 @ 1, l1 % 1, 10.0, arc_size=45)
            l3 = PolarLine(l2 @ 1, 15.0, -45.0)
            l4 = Line(l3 @ 1, ((l3 @ 1).X, ts_height))
            l5 = Line(l4 @ 1, l1 @ 0)
        make_face()
    revolve(axis=Axis.Z, mode=Mode.SUBTRACT)

    # slot for the handle
    with BuildSketch(Plane.YZ):
        with Locations((0, ts_height - handle_z_offset + handle_dia / 2)):
            Circle(handle_dia / 2)
            Rectangle(handle_dia, 
                      ts_height, 
                      align=(Align.CENTER, Align.MIN))
    extrude(amount=ts_outer_dia, mode=Mode.SUBTRACT)

    sel = (ts.edges().filter_by(GeomType.HYPERBOLA) +
           ts.edges().filter_by(GeomType.BSPLINE))

    sel1 = sel.filter_by_position(Axis.Y,
                                  minimum=-ts_inner_dia / 2,
                                  maximum=-handle_dia / 2 - 1.0)
    
    sel2 = sel.filter_by_position(Axis.Y,
                                  minimum=handle_dia / 2 + 1.0,
                                  maximum=ts_inner_dia / 2)
    fillet(sel1, radius=5.4)
#    fillet(sel2, radius=5.0)

show(ts, sel2)
