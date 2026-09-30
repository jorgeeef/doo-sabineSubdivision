



from doo_sabin import Mesh




def cube():
   vertices = [
       (-1, -1, -1),  # 0
       (1, -1, -1),   # 1
       (1, 1, -1),    # 2
       (-1, 1, -1),   # 3
       (-1, -1, 1),   # 4
       (1, -1, 1),    # 5
       (1, 1, 1),     # 6
       (-1, 1, 1),    # 7
   ]
   faces = [
       [0, 1, 2, 3],  # bottom
       [4, 7, 6, 5],  # top
       [0, 4, 5, 1],  # front
       [1, 5, 6, 2],  # right
       [2, 6, 7, 3],  # back
       [3, 7, 4, 0],  # left
   ]
   return Mesh(vertices, faces)





