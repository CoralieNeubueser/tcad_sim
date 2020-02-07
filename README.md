tcad_sim
============

Analysis tools for TCAD Sentaurus outputs
- converting to csv files
- plotting with matplotlib

# Initialization
- python3

# Prepare TCAD outputs:
1. define parameter that you want to study, here example for 2.
2. make sure that the output files feature parameters "_@par@_" to command files of CV/IV measurements
- see line 24/25 of sdevice_des.cmd

# Run analysis
use run.py scipt in python/

~~~
python3 python/run.py --project ARCADIA25um_surfaceDamage -m cv --writeCSV
~~~