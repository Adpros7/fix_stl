from pathlib import Path
import sys

import traceback


def excepthook(exc_type, exc_value, exc_tb):

    with open(Path().home() / "Downloads/fix_stl_error.txt", "w") as f:
        traceback.print_exception(exc_type, exc_value, exc_tb, file=f)


sys.excepthook = excepthook

import argparse
from datetime import datetime
from zoneinfo import ZoneInfo
import pymeshfix
import trimesh
import manifold3d
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("path")

path = str(parser.parse_args().path)

mesh = trimesh.load_mesh(path)

v, f = mesh.vertices, mesh.faces  # pyright: ignore[reportAttributeAccessIssue]

meshfix = pymeshfix.MeshFix(v, f)
meshfix.repair(remove_smallest_components=False)
meshfix.clean()

v, f = meshfix.mesh.points, meshfix.mesh.faces.reshape(-1, 4)[:, 1:]  # pyright: ignore[reportAttributeAccessIssue]

fixer = trimesh.Trimesh(v, f)
fixer.fill_holes()
fixer.fix_normals()

v, f = (
    np.ascontiguousarray(fixer.vertices, dtype=np.float32),
    np.ascontiguousarray(fixer.faces, dtype=np.uint32),
)

m3d = manifold3d.Mesh(v, f)
m3d.merge()

v, f = m3d.vert_properties, m3d.tri_verts

trimesh.Trimesh(v, f).export(
    f"{path.removesuffix('.stl')}_fixed__{str(datetime.now(ZoneInfo('America/New_York'))).replace(' ', '')}.stl"
)
