# Doo-Sabin subdivision surfaces
import numpy as np



class Mesh:
   # stores self.vertices and self.faces as arrays
   def __init__(self, vertices, faces):
       self.vertices = [np.array(v, dtype=float) for v in vertices]
       self.faces = [list(f) for f in faces]
   def __repr__(self):
       return f"Mesh({len(self.vertices)} verts, {len(self.faces)} faces)"


# Cette fonction associe chaque arête aux faces qui la partagent
def build_edge_faces(mesh): 
   edge_faces = {}
   for fid, face in enumerate(mesh.faces):
       n = len(face)
       for i in range(n):
           a, b = face[i], face[(i + 1) % n]
           key = frozenset((a, b))
           edge_faces.setdefault(key, []).append((fid, a, b))
   return edge_faces


# Cette fonction cherche toutes les faces qui contiennent un sommet donné
def build_vertex_faces(mesh):
   vertex_faces = {}
   for fid, face in enumerate(mesh.faces):
       for v in face:
           vertex_faces.setdefault(v, []).append(fid)
   return vertex_faces


# Cette fonction organise les faces autour d'un sommet dans un ordre circulaire
def faces_around_vertex(mesh, v, vertex_faces, edge_faces):
   faces = vertex_faces[v]
   if not faces:
       return []
   start = faces[0]
   ordered = [start]
   current = start
   face_verts = mesh.faces[current]
   idx = face_verts.index(v)
   u = face_verts[idx - 1]  

   for _ in range(len(faces)):
       candidates = edge_faces[frozenset((u, v))]
       nxt = None
       for (fid, a, b) in candidates:
           if fid != current:
               nxt = fid
               break
       if nxt is None or nxt == start:
           break
       ordered.append(nxt)
       current = nxt
       face_verts = mesh.faces[current]
       idx = face_verts.index(v)
       u = face_verts[idx - 1]
   return ordered




# Cette fonction calcule les coefficients utilisés pour créer les nouveaux sommets
# Nouveau point = somme (poids × anciens sommets)
def doo_sabin_weights(n):
   """
     j = 0        -> the vertex itself
     j = 1, n-1   -> its two edge-adjacent neighbors
     otherwise    -> every other vertex of the face
   """
   w = np.zeros(n)
   for j in range(n):
       if j == 0:
           w[j] = 0.5 + 1.0 / (4 * n)
       elif j == 1 or j == n - 1:
           w[j] = 0.125 + 1.0 / (4 * n)
       else:
           w[j] = 1.0 / (4 * n)
   return w




# Une stepe subdivision
# Cette fonction réalise une étape complète de subdivision.
def doo_sabin_subdivide(mesh):
   edge_faces = build_edge_faces(mesh)
   vertex_faces = build_vertex_faces(mesh)

   new_vertices = []
   point_index = {}  # (face_id, original_vertex_id) -> index into new_vertices

   # Step 1: Pour chaque coin de chaque face, on crée un nouveau sommet.
   for fid, face in enumerate(mesh.faces):
       n = len(face)
       weights = doo_sabin_weights(n)
       for i in range(n):
           acc = np.zeros(3)
           for j in range(n):
               offset = (j - i) % n
               acc += weights[offset] * mesh.vertices[face[j]]
           point_index[(fid, face[i])] = len(new_vertices)
           new_vertices.append(acc)


   new_faces = []


   # Step 2: F-faces - Chaque ancienne face devient une nouvelle face plus petite
   for fid, face in enumerate(mesh.faces):
       new_faces.append([point_index[(fid, v)] for v in face])


   # Step 3: E-faces - Chaque ancienne arête produit une nouvelle face quadrilatérale entre deux F-faces 
   seen = set()
   for key, entries in edge_faces.items():
       if key in seen:
           continue
       seen.add(key)
       if len(entries) < 2:
           continue  
       (f1, a, b), (f2, _, _) = entries[0], entries[1]
       e_face = [point_index[(f1, a)], point_index[(f2, a)],
                 point_index[(f2, b)], point_index[(f1, b)]]
       new_faces.append(e_face)


   # Step 4: V-faces - Chaque ancien sommet devient le centre d'une nouvelle face
   for v, faces in vertex_faces.items():
       ordered = faces_around_vertex(mesh, v, vertex_faces, edge_faces)
       if len(ordered) < 3:
           continue  # boundary vertex - skipped for the same reason as above
       new_faces.append([point_index[(fid, v)] for fid in ordered])


   return Mesh(new_vertices, new_faces)




def subdivide_n_times(mesh, n):
   result = mesh
   for _ in range(n):
       result = doo_sabin_subdivide(result)
   return result

