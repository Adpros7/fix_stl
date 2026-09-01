import argparse
from datetime import datetime
from zoneinfo import ZoneInfo
import pymeshfix
import trimesh
import manifold3d

parser = argparse.ArgumentParser()
parser.add_argument("path")

path = str(parser.parse_args()._get_kwargs()[0][1])

mesh = trimesh.load(path)

v, f = mesh.vertices, mesh.faces  # ty:ignore[unresolved-attribute]  # pyright: ignore[reportAttributeAccessIssue]

meshfix = pymeshfix.MeshFix(v, f)
meshfix.repair()
meshfix.clean()

v, f = meshfix.mesh.points, meshfix.mesh.faces.reshape(-1, 4)[:, 1:]  # pyright: ignore[reportAttributeAccessIssue]

fixer = trimesh.Trimesh(v, f)
fixer.fill_holes()
fixer.fix_normals()

v, f = fixer.vertices, fixer.faces

m3d = manifold3d.Mesh(v, f)
m3d.merge()

v, f = m3d.vert_properties, m3d.tri_verts



fixer.export(f"{path.removesuffix('.stl')}_fixed__{str(datetime.now(ZoneInfo('America/New_York'))).replace(' ', '')}.stl")