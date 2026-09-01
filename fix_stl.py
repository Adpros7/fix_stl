import argparse
from datetime import datetime
from zoneinfo import ZoneInfo
import os
import pymeshfix
import trimesh

parser = argparse.ArgumentParser()
parser.add_argument("path")
path = parser.parse_args().path

mesh = trimesh.load_mesh(path)

meshfix = pymeshfix.MeshFix(mesh.vertices, mesh.faces)
meshfix.repair(
    joincomp=True,
    remove_smallest_components=False,
)
meshfix.clean(max_iters=10, inner_loops=3)

mesh = trimesh.Trimesh(
    meshfix.points,
    meshfix.faces,
    process=True,
)

mesh.remove_infinite_values()
mesh.update_faces(mesh.unique_faces())
mesh.update_faces(mesh.nondegenerate_faces())
mesh.remove_unreferenced_vertices()
mesh.merge_vertices()

trimesh.repair.fill_holes(mesh)
trimesh.repair.fix_winding(mesh)
trimesh.repair.fix_normals(mesh, multibody=True)
trimesh.repair.fix_inversion(mesh, multibody=True)

meshfix = pymeshfix.MeshFix(mesh.vertices, mesh.faces)
meshfix.repair(
    joincomp=True,
    remove_smallest_components=False,
)

mesh = trimesh.Trimesh(
    meshfix.points,
    meshfix.faces,
    process=True,
)


timestamp = datetime.now(
    ZoneInfo("America/New_York")
).strftime("%Y-%m-%d_%H-%M-%S")

os.remove(path)

mesh.export(
    f"{path.removesuffix('.stl')}"
)