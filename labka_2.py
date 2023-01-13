import NemAll_Python_Geometry as ge
import NemAll_Python_BaseElements as b
import NemAll_Python_BasisElements as bs
import NemAll_Python_Utility as u
import GeometryValidate as val
from HandleDirection import HandleDirection
from HandleProperties import HandleProperties
from labka_2_help import parametres, cut_edges


class labka_2:

    def __init__(self, doc):
        self.model_ele_list = []
        self.handle_list = []
        self.document = doc

    def create(self, build_ele):
        self.top(build_ele)
        self.handles(build_ele)
        return (self.model_ele_list, self.handle_list)

    def bottom(self, build_ele):
        params = parametres(build_ele)
        cub = ge.BRep3D.CreateCuboid(ge.AxisPlacement3D(ge.Point3D(0, 0, 0), ge.Vector3D(1, 0, 0), ge.Vector3D(0, 0, 1)), params[0], params[1], params[2])
        c_h = ge.BRep3D.CreateCuboid(ge.AxisPlacement3D(ge.Point3D(0, 0, 0), ge.Vector3D(1, 0, 0), ge.Vector3D(0, 0, 1)), params[0], params[1], params[2])
        cw = build_ele.cutt.value
        cb = build_ele.cutb.value

        f = cut_edges(cub, c_h, cw, cb)
        return f

    def middle(self, build_ele):
        params = parametres(build_ele)
        cub = ge.BRep3D.CreateCuboid(ge.AxisPlacement3D(ge.Point3D(params[0] / 2 - params[3] / 2, 0, params[2]), ge.Vector3D(1, 0, 0), ge.Vector3D(0, 0, 1)), params[3], params[1], params[4])
        cylinder = ge.BRep3D.CreateCylinder(ge.AxisPlacement3D(ge.Point3D(params[5], params[1] / 8, params[2] + params[4] / 2), ge.Vector3D(0, 0, 1), ge.Vector3D(1, 0, 0)), params[6], params[3])
        cylinder1 = ge.BRep3D.CreateCylinder(ge.AxisPlacement3D(ge.Point3D(params[5], params[1] - params[1] / 8, params[2] + params[4] / 2), ge.Vector3D(0, 0, 1), ge.Vector3D(1, 0, 0)), params[6], params[3])
        trouble, cub = ge.MakeSubtraction(cub, cylinder)
        trouble, cub = ge.MakeSubtraction(cub, cylinder1)
        trouble, f = ge.MakeUnion(
            cub, self.bottom(build_ele))
        return f

    def top(self, build_ele):
        params = parametres(build_ele)
        cub = ge.BRep3D.CreateCuboid(ge.AxisPlacement3D(ge.Point3D(0 - (params[7] - params[0]) / 2, 0, params[2] + params[4]), ge.Vector3D(1, 0, 0), ge.Vector3D(0, 0, 1)), params[7], params[1], params[8])
        plate = ge.BRep3D.CreateCuboid(ge.AxisPlacement3D(ge.Point3D(params[9] - (params[7] - params[0]) / 2, 0, params[2] + params[4] + params[8]), ge.Vector3D(1, 0, 0), ge.Vector3D(0, 0, 1)), params[7] - params[9]*2, params[1], params[10])
        com_prop = b.CommonProperties()
        com_prop.GetGlobalProperties()
        com_prop.Pen = 1
        com_prop.Color = params[11]
        chamfer_width_top = params[12]

        if chamfer_width_top > 0:
            ed2 = u.VecSizeTList()
            ed2.append(8)
            ed2.append(10)
            trouble, cub = ge.ChamferCalculus.Calculate(cub, ed2, chamfer_width_top, False)

            if not val.polyhedron(trouble):
                return

        trouble, f = ge.MakeUnion(cub, self.middle(build_ele))
        trouble, f = ge.MakeUnion(f, plate)
        self.model_ele_list.append(bs.ModelElement3D(com_prop, f))

    def handles(self, build_ele):
        params = parametres(build_ele)
        d = ge.Point3D(params[0] / 2, params[1], params[4] + params[2])
        d2 = ge.Point3D(params[0] / 2, 0, params[2] / 2)
        d3 = ge.Point3D(0, params[1], (params[2] - params[5]) / 2)
        d4 = ge.Point3D(0 - (params[7] - params[0]) / 2, params[1], params[4] + params[2] + params[12])
        d5 = ge.Point3D(params[0] / 2, params[1], params[4] + params[2] - params[2] / 4)
        d6 = ge.Point3D(params[0] / 2, params[1], params[4] + params[2] + params[8])
        d7 = ge.Point3D(params[0] / 2, params[1], 0)
        d8 = ge.Point3D(params[0] / 2 - params[3] / 2, params[1], params[4] / 2 + params[2])

        self.handle_list.append(HandleProperties("cenh", ge.Point3D(d.X, d.Y, d.Z), ge.Point3D(d.X, d.Y, d.Z - params[4]), [("cenh", HandleDirection.z_dir)], HandleDirection.z_dir, False))
        self.handle_list.append(HandleProperties("len", ge.Point3D(d2.X, d2.Y + params[1], d2.Z), ge.Point3D(d2.X, d2.Y, d2.Z), [("len", HandleDirection.y_dir)], HandleDirection.y_dir, False))
        self.handle_list.append(HandleProperties("wid", ge.Point3D(d3.X + params[0], d3.Y, d3.Z), ge.Point3D(d3.X, d3.Y, d3.Z), [("wid", HandleDirection.x_dir)], HandleDirection.x_dir, False))
        self.handle_list.append(HandleProperties("widt", ge.Point3D(d4.X + params[7], d4.Y, d4.Z), ge.Point3D(d4.X, d4.Y, d4.Z), [("widt", HandleDirection.x_dir)], HandleDirection.x_dir, False))
        self.handle_list.append(HandleProperties("tot", ge.Point3D(d5.X, d5.Y, d5.Z + params[8]), ge.Point3D(d5.X, d5.Y, d5.Z), [("tot", HandleDirection.z_dir)], HandleDirection.z_dir, False))
        self.handle_list.append(HandleProperties("plah", ge.Point3D(d6.X, d6.Y, d6.Z + params[10]), ge.Point3D(d6.X, d6.Y, d6.Z), [("plah", HandleDirection.z_dir)], HandleDirection.z_dir, False))
        self.handle_list.append(HandleProperties("hei", ge.Point3D(d7.X, d7.Y, d7.Z + params[2]), ge.Point3D(d7.X, d7.Y, d7.Z), [("hei", HandleDirection.z_dir)], HandleDirection.z_dir, False))
        self.handle_list.append(HandleProperties("cenw", ge.Point3D(d8.X + params[3], d8.Y, d8.Z), ge.Point3D(d8.X, d8.Y, d8.Z), [("cenw", HandleDirection.x_dir)], HandleDirection.x_dir, False))


def check_allplan_version(build_ele, version):
    del build_ele
    del version
    return True


def create_element(build_ele, doc):
    element = labka_2(doc)
    return element.create(build_ele)


def move_handle(build_ele, handle_prop, input_pnt, doc):
    build_ele.change_property(handle_prop, input_pnt)
    return create_element(build_ele, doc)