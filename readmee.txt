#Doo-Sabin subdivision surfaces

Step 1 - open cmd in the folder where you need keep the project and clode the repo:
git clone  https://github.com/jorgeeef/doo-sabineSubdivision.git

Step 2 - enter the project folder
cd doo-sabineSubdivision

Step 3 - open it in vscode
code .

sudo apt update 
sudo apt install python3.12-venv
python3 -m venv venv



Step 4 - recreate environment
python3 -m venv venv

Step 5 - activate the environment
source venv/bin/activate

Step 6 - install dependencies
pip install -r requirements.txt



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
