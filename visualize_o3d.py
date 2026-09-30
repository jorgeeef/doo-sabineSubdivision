



"""
Interactive Doo-Sabin viewer built on Open3D.


Controls (with the window focused):
 N  ->  subdivide one more level
 R  ->  reset to the original (level 0) mesh
 W  ->  toggle the wireframe overlay
 Esc / close window -> quit
"""


import numpy as np
import open3d as o3d


from doo_sabin import subdivide_n_times
from sample_meshes import cube




def fan_triangulate(face):
   """
   Turn an n-gon into (n-2) triangles by fanning out from its first vertex.
   Open3D's TriangleMesh only understands triangles, so every F/E/V-face
   (which can be a triangle, quad, or larger n-gon) needs this before it can
   be handed to Open3D. Good enough for the roughly-planar, roughly-convex
   faces Doo-Sabin produces.
   """
   return [[face[0], face[i], face[i + 1]] for i in range(1, len(face) - 1)]




def to_o3d_triangle_mesh(mesh, color=(0.62, 0.88, 0.80)):
   """Build the shaded surface Open3D renders."""
   triangles = []
   for face in mesh.faces:
       triangles.extend(fan_triangulate(face))


   o3d_mesh = o3d.geometry.TriangleMesh()
   o3d_mesh.vertices = o3d.utility.Vector3dVector(np.array(mesh.vertices))
   o3d_mesh.triangles = o3d.utility.Vector3iVector(np.array(triangles))
   o3d_mesh.compute_vertex_normals()
   o3d_mesh.paint_uniform_color(color)
   return o3d_mesh




def to_o3d_wireframe(mesh, color=(0.06, 0.31, 0.25)):
   """
   Wireframe of the mesh's ACTUAL polygon edges - not the extra diagonal
   lines fan-triangulation introduces (those aren't real mesh edges and
   would be misleading to draw).
   """
   edges = set()
   for face in mesh.faces:
       n = len(face)
       for i in range(n):
           a, b = face[i], face[(i + 1) % n]
           edges.add((min(a, b), max(a, b)))


   lineset = o3d.geometry.LineSet()
   lineset.points = o3d.utility.Vector3dVector(np.array(mesh.vertices))
   lineset.lines = o3d.utility.Vector2iVector(np.array(sorted(edges)))
   lineset.paint_uniform_color(color)
   return lineset




class InteractiveDooSabin:
   def __init__(self, base_mesh, max_level=5):
       self.base_mesh = base_mesh
       self.level = 0
       self.max_level = max_level
       self.show_wire = True
       self._cache = {0: base_mesh}  # avoid recomputing levels you've already visited


       self.vis = o3d.visualization.VisualizerWithKeyCallback()
       self.vis.create_window(
           window_name="Doo-Sabin subdivision  [N: subdivide, R: reset, W: wireframe]",
           width=1000, height=800,
       )
       self._rebuild_geometry()


       self.vis.register_key_callback(ord("N"), self._on_subdivide)
       self.vis.register_key_callback(ord("R"), self._on_reset)
       self.vis.register_key_callback(ord("W"), self._on_toggle_wire)


   def _get_mesh(self, level):
       if level not in self._cache:
           self._cache[level] = subdivide_n_times(self.base_mesh, level)
       return self._cache[level]


   def _rebuild_geometry(self):
       mesh = self._get_mesh(self.level)
       self.vis.clear_geometries()
       self.vis.add_geometry(to_o3d_triangle_mesh(mesh), reset_bounding_box=(self.level == 0))
       if self.show_wire:
           self.vis.add_geometry(to_o3d_wireframe(mesh), reset_bounding_box=False)
       print(f"level {self.level}: {len(mesh.vertices)} verts, {len(mesh.faces)} faces")


   def _on_subdivide(self, vis):
       if self.level < self.max_level:
           self.level += 1
           self._rebuild_geometry()
       return False


   def _on_reset(self, vis):
       self.level = 0
       self._rebuild_geometry()
       return False


   def _on_toggle_wire(self, vis):
       self.show_wire = not self.show_wire
       self._rebuild_geometry()
       return False


   def run(self):
       self.vis.run()
       self.vis.destroy_window()




def main():
   viewer = InteractiveDooSabin(cube(), max_level=5)
   viewer.run()




if __name__ == "__main__":
   main()





