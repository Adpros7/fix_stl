#!/usr/bin/env/ python3


import argparse
from datetime import datetime
from zoneinfo import ZoneInfo
import pymeshfix
import pymeshlab
import trimesh
from trimesh.exchange.load import mesh_formats

parser = argparse.ArgumentParser()
parser.add_argument("path")

path = str(parser.parse_args()._get_kwargs()[0][1])

mesh = trimesh.load(path)
v, f = mesh.vertices, mesh.faces  # ty:ignore[unresolved-attribute]  # pyright: ignore[reportAttributeAccessIssue]

meshfix = pymeshfix.MeshFix(v, f)
meshfix.repair()

v, f = meshfix.mesh.points, meshfix.mesh.faces.reshape(-1, 4)[:, 1:]  # pyright: ignore[reportAttributeAccessIssue]

meshfix.clean()
meshfix.save(
    f"{path.removesuffix('.stl')}_fixed__{str(datetime.now(ZoneInfo('America/New_York'))).replace(' ', '')}.stl"
)
