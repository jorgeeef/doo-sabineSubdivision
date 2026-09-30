#Doo-Sabin subdivision surfaces

A small, dependency-light implementation of Doo-Sabin subdivision (Doo & Sabin, 1978),
with an interactive Open3D viewer - subdivide a mesh live, right in the 3D window.



#1  Set up a virtual environment
Linux:
python3 -m venv doosabin-env
source doosabin-env/bin/activate

Windows:
python -m venv doosabin-env
doosabin-env\Scripts\Activate.ps1


#2  Install everything
pip install -r requirements.txt


#3  Run the doo-sabin subdivision
python3 visualize_o3d.py

#3  Run the doo-sabin subdivision + noise
python3 interactive_rocky.py
