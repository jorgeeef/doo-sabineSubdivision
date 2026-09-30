"""
Minimal Wavefront .obj exporter for our Mesh class.
 
OBJ natively supports polygons with any number of vertices, so we write
each face exactly as it is (triangle, quad, pentagon, ...) instead of
triangulating - the saved file matches the topology you see in the
Open3D viewer.
"""
 
def save_obj(mesh, filepath):
    """Write mesh.vertices / mesh.faces to filepath as a Wavefront .obj file."""
    with open(filepath, "w") as f:
        f.write("# Doo-Sabin rocky mesh\n")
        f.write(f"# {len(mesh.vertices)} vertices, {len(mesh.faces)} faces\n")
 
        for v in mesh.vertices:
            f.write(f"v {v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n")
 
        # OBJ face indices are 1-based
        for face in mesh.faces:
            indices = " ".join(str(i + 1) for i in face)
            f.write(f"f {indices}\n")
 
    print(f"-> Maillage sauvegarde : {filepath} "
          f"({len(mesh.vertices)} sommets, {len(mesh.faces)} faces)") 