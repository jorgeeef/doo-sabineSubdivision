"""
Rocher Doo-Sabin interactif, en partant d'un cube.

Les parametres (amplitude, frequence, octaves, graine, subdivisions par
iteration)

  N  ->  applique UNE iteration de plus (subdivision + bruit)
  R  ->  reinitialise a la forme de depart
  W  ->  affiche/masque le fil de fer
  Echap -> quitter

Des que le nombre d'iterations demande est atteint, le maillage est
automatiquement sauvegarde dans un fichier .obj.
"""

import os
import open3d as o3d

from doo_sabin import doo_sabin_subdivide
from sample_meshes import cube
from noise_displace import add_noise_displacement
from visualize_o3d import to_o3d_triangle_mesh, to_o3d_wireframe
from obj_export import save_obj


def ask_float(prompt, default):
    raw = input(f"{prompt} [{default}]: ").strip()
    return float(raw) if raw else default


def ask_int(prompt, default):
    raw = input(f"{prompt} [{default}]: ").strip()
    return int(raw) if raw else default


class InteractiveRockyCube:
    def __init__(self, subdiv_per_step, amplitude, frequency, octaves, seed,
                 max_iterations=8, output_dir="."):
        self.base = cube()
        self.subdiv_per_step = subdiv_per_step
        self.amplitude = amplitude
        self.frequency = frequency
        self.octaves = octaves
        self.seed = seed
        self.max_iterations = max_iterations
        self.output_dir = output_dir
        self.iteration = 0
        self.show_wire = True
        self.saved = False  # so we only auto-save once per run
        self._cache = {0: self.base}  # iteration number -> mesh, so R/N never recompute needlessly

        self.vis = o3d.visualization.VisualizerWithKeyCallback()
        self.vis.create_window(
            window_name="Rocher Doo-Sabin (cube)  [N: iteration, R: reset, W: fil de fer]",
            width=1000, height=800,
        )
        self._rebuild_geometry()

        self.vis.register_key_callback(ord("N"), self._on_next)
        self.vis.register_key_callback(ord("R"), self._on_reset)
        self.vis.register_key_callback(ord("W"), self._on_toggle_wire)

    def _compute_iteration(self, n):
        """Maillage apres n iterations (subdivision + bruit), toujours a
        partir du cube de base, toujours avec LES MEMES parametres."""
        if n in self._cache:
            return self._cache[n]
        mesh = self._compute_iteration(n - 1)
        for _ in range(self.subdiv_per_step):
            mesh = doo_sabin_subdivide(mesh)
        mesh = add_noise_displacement(
            mesh, amplitude=self.amplitude, frequency=self.frequency,
            octaves=self.octaves, seed=self.seed,
        )
        self._cache[n] = mesh
        return mesh

    def _rebuild_geometry(self):
        mesh = self._compute_iteration(self.iteration)
        self.vis.clear_geometries()
        self.vis.add_geometry(to_o3d_triangle_mesh(mesh), reset_bounding_box=(self.iteration == 0))
        if self.show_wire:
            self.vis.add_geometry(to_o3d_wireframe(mesh), reset_bounding_box=False)
        print(f"iteration {self.iteration} : {len(mesh.vertices)} sommets, {len(mesh.faces)} faces")

    def _export_current_mesh(self):
        mesh = self._compute_iteration(self.iteration)
        filename = (
            f"rock_iter{self.iteration}_amp{self.amplitude}_"
            f"freq{self.frequency}_oct{self.octaves}_seed{self.seed}.obj"
        )
        obj_dir = os.path.join(self.output_dir, "obj")
        os.makedirs(obj_dir, exist_ok=True)

        filepath = os.path.join(obj_dir, filename)
        save_obj(mesh, filepath)


    def _on_next(self, vis):
        if self.iteration < self.max_iterations:
            self.iteration += 1
            self._rebuild_geometry()
            if self.iteration == self.max_iterations and not self.saved:
                self._export_current_mesh()
                self.saved = True
                print(f"-> Nombre d'iterations maximum ({self.max_iterations}) atteint : "
                      f"la touche N est desormais desactivee. Utilisez R (reset) ou Echap (quitter).")
        else:
            print(f"N desactivee : vous avez deja fait les {self.max_iterations} iterations demandees. "
                  f"Appuyez sur R pour reinitialiser, ou Echap pour quitter.")
        return False

    def _on_reset(self, vis):
        self.iteration = 0
        self._rebuild_geometry()
        print(f"-> Reinitialise. Vous pouvez de nouveau appuyer sur N (jusqu'a {self.max_iterations} fois).")
        return False

    def _on_toggle_wire(self, vis):
        self.show_wire = not self.show_wire
        self._rebuild_geometry()
        return False

    def run(self):
        self.vis.run()
        self.vis.destroy_window()
        # Filet de securite : si la fenetre est fermee avant d'avoir
        # atteint le nombre d'iterations demande, on sauvegarde quand
        # meme l'etat courant.
        if not self.saved:
            self._export_current_mesh()
            self.saved = True


def main():
    print("=== Generateur de rocher Doo-Sabin (depart : cube) ===")
    print("Les parametres ne sont demandes qu'une fois : chaque N applique la meme regle.\n")

    n_iterations = ask_int("Nombre d'iterations souhaitees (nombre de fois qu'on pourra appuyer sur N)", 3)
    subdiv_per_step = 1  # une subdivision Doo-Sabin par iteration
    amplitude = ask_float("Amplitude du bruit (hauteur des bosses)", 0.15)
    frequency = ask_float("Frequence du bruit (finesse des bosses)", 1.5)
    octaves = ask_int("Nombre d'octaves (couches de detail)", 2)
    seed = ask_int("Graine aleatoire (change le motif obtenu)", 1)

    print(f"\nFenetre Open3D : N = iteration suivante (jusqu'a {n_iterations} fois), "
          f"R = retour au cube, W = fil de fer, Echap = quitter.")
    print(f"Des que vous aurez appuye {n_iterations} fois sur N, le maillage sera "
          f"automatiquement sauvegarde en .obj dans le dossier courant.\n")

    InteractiveRockyCube(
        subdiv_per_step, amplitude, frequency, octaves, seed,
        max_iterations=n_iterations,
    ).run()


if __name__ == "__main__":
    main()