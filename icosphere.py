import numpy as np
from doo_sabin import Mesh


def icosahedron(radius=1.0):
    """A regular icosahedron: 12 vertices, 20 triangular faces, projected
    onto a sphere of the given radius. A much better starting point than a
    cube for rounded, rock/asteroid-like shapes, since all faces and all
    vertices start out equivalent (no flat faces to hide seams in)."""
    phi = (1.0 + np.sqrt(5.0)) / 2.0

    raw = [
        (-1, phi, 0), (1, phi, 0), (-1, -phi, 0), (1, -phi, 0),
        (0, -1, phi), (0, 1, phi), (0, -1, -phi), (0, 1, -phi),
        (phi, 0, -1), (phi, 0, 1), (-phi, 0, -1), (-phi, 0, 1),
    ]
    vertices = [tuple(radius * np.array(v) / np.linalg.norm(v)) for v in raw]

    faces = [
        [0, 11, 5], [0, 5, 1], [0, 1, 7], [0, 7, 10], [0, 10, 11],
        [1, 5, 9], [5, 11, 4], [11, 10, 2], [10, 7, 6], [7, 1, 8],
        [3, 9, 4], [3, 4, 2], [3, 2, 6], [3, 6, 8], [3, 8, 9],
        [4, 9, 5], [2, 4, 11], [6, 2, 10], [8, 6, 7], [9, 8, 1],
    ]
    return Mesh(vertices, faces)