tcad_sim
============

Analysis tools for TCAD Sentaurus outputs
- converting to csv files
- plotting with matplotlib

# Initialization
Dependent on..
- python3

Clone the git repository:
~~~
git clone https://github.com/CoralieNeubueser/tcad_sim.git .
~~~

# Prepare TCAD outputs
1. define parameter that you want to study, here example for 2 (important!! keep type, float or int), and add them to python/run.py ll 15/16.
2. make sure that the TCAD output files feature parameters "_@par@_" to command files of CV/IV measurements
- see line 24/25 of DB/ARCADIA25um_surfaceDamage/sdevice_des.cmd
- see line 77 of DB/ARCADIA25um_surfaceDamage/sdevice1_des.cmd
Run the simulation using the workbench: 
~~~
swb&
~~~

# Run analysis
use run.py scipt in python/

~~~
python3 python/run.py --project ARCADIA25um_surfaceDamage -m 'cv' --writeCSV
~~~

- possible choices for measurements are: 'cv', 'iv', or 'iv_b'.
- adjust the parameters in python/run.py.
- when you have run once with flag --writeCSV, you can leave it out the next time you want to plot only.

-> csv and pdf files are stored in DB/<--project-->/tmp/
