import NemAll_Python_Geometry as ge
import NemAll_Python_BaseElements as b
import NemAll_Python_BasisElements as bs
import NemAll_Python_Utility as u
import GeometryValidate as val
from HandleDirection import HandleDirection
from HandleProperties import HandleProperties

def parametres(build_ele):
        wid = build_ele.wid.value
        len = build_ele.len.value
        hei = build_ele.hei.value
        cenw = build_ele.cenw.value
        cenh = build_ele.cenh.value
        cutt = build_ele.cutt.value
        rad = build_ele.rad.value
        widt = build_ele.widt.value
        tot = build_ele.tot.value
        plas = build_ele.plas.value
        plah = build_ele.plah.value
        Color4 = build_ele.Color4.value
        cuttb = build_ele.cuttb.value
        return [wid, len, hei, cenw, cenh, cutt, rad, widt, tot, plas, plah, Color4, cuttb]

def cut_edges(cub, c_h, cw, cb):
    if cw > 0:
            ed = u.VecSizeTList()
            ed.append(1)
            ed.append(3)
            e, cub = ge.ChamferCalculus.Calculate(cub, ed, cw, False)
            
            if not val.polyhedron(e):
                return

    if cb > 0:
        ed2 = u.VecSizeTList()
        ed2.append(8)
        ed2.append(10)
        e, c_h = ge.ChamferCalculus.Calculate(c_h, ed2, cb, False)
        
        if not val.polyhedron(e):
           return

    e, f = ge.MakeIntersection(cub, c_h)
    return f