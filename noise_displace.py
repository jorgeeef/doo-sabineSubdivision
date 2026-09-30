"""
Turns a smooth Doo-Sabin mesh into a rough / rocky one by pushing every
vertex in or out along its normal, by an amount taken from a 3D coherent
noise field (OpenSimplex). Because the noise is evaluated at each vertex's
actual (x, y, z) position - not per-face - shared vertices get the exact
same displacement from every face that uses them, so no cracks or seams
appear between faces.
"""

import numpy as np
import opensimplex

from doo_sabin import Mesh, build_vertex_faces


def face_normal(mesh, face):
    """Newell's method: a robust normal for any planar-ish n-gon, even
    slightly non-planar ones (which Doo-Sabin faces sometimes are)."""
    n = np.zeros(3)
    verts = [mesh.vertices[i] for i in face]
    k = len(verts)
    for i in range(k):
        v1, v2 = verts[i], verts[(i + 1) % k]
        n[0] += (v1[1] - v2[1]) * (v1[2] + v2[2])
        n[1] += (v1[2] - v2[2]) * (v1[0] + v2[0])
        n[2] += (v1[0] - v2[0]) * (v1[1] + v2[1])
    norm = np.linalg.norm(n)
    return n / norm if norm > 1e-12 else n


def compute_vertex_normals(mesh):
    """Average of the normals of every face touching each vertex."""
    vertex_faces = build_vertex_faces(mesh)
    face_normals = [face_normal(mesh, f) for f in mesh.faces]

    normals = []
    for v in range(len(mesh.vertices)):
        acc = np.zeros(3)
        for fid in vertex_faces.get(v, []):
            acc += face_normals[fid]
        norm = np.linalg.norm(acc)
        normals.append(acc / norm if norm > 1e-12 else np.array([0.0, 0.0, 1.0]))
    return normals


def add_noise_displacement(mesh, amplitude=0.15, frequency=1.5, octaves=2,
                            lacunarity=2.0, persistence=0.5, seed=0):
    """
    Displace every vertex along its normal by a fractal-noise amount.

    amplitude    - how far vertices can move (in the same units as the mesh)
    frequency    - how fine the bumps are; higher = smaller/tighter bumps
    octaves      - how many noise layers are stacked (more = more fine detail
                   on top of the coarse shape, like the fractal terrain look)
    lacunarity   - how much the frequency grows each octave (usually ~2.0)
    persistence  - how much the amplitude shrinks each octave (usually ~0.5)
    seed         - changes which random-looking bumps you get
    """
    opensimplex.seed(seed)
    normals = compute_vertex_normals(mesh)

    new_vertices = []
    for v, n in zip(mesh.vertices, normals):
        freq = frequency
        amp = amplitude
        total = 0.0
        for _ in range(octaves):
            total += amp * opensimplex.noise3(v[0] * freq, v[1] * freq, v[2] * freq)
            freq *= lacunarity
            amp *= persistence
        new_vertices.append(np.array(v) + n * total)

    return Mesh(new_vertices, mesh.faces)