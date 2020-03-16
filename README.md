tcad_sim
============

Analysis tools for TCAD Sentaurus outputs
- converting to csv files
- plotting with matplotlib

# Initialization
Depends on..
- python3
- a TCAD Sentaurus installation (uses svisual) 

Clone the git repository:
~~~
git clone https://github.com/CoralieNeubueser/tcad_sim.git .
~~~

# Prepare TCAD outputs
1. define parameter that you want to study. You will be able to parse them through the command line when running python/run.py, like e.g. 
~~~
python python/run.py -p1 0.0 -p1 0.5 -p1 2.0 -p1 4.25 -p1Name 'gap [$\mu$m]' -p2 100 -p2Name 'S0 [cm/s]' ...
~~~
- ATTENTION! It is always assumed the you are testing all p2s for each p1 ect.

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
python3 python/run.py --project ARCADIA25um_surfaceDamage -m 'cv' -p1 0.0 -p1 0.5 -p1 2.0 -p1 4.25 -p1Name 'gap [$\mu$m]' -p2 100 -p2Name 'S0 [cm/s]' --writeCSV
~~~

- when you have run once with flag --writeCSV, you can leave it out the next time if you want to plot only.

- possible choices for measurements are: 'cv', 'iv', 'cv_b', 'iv_b', 'iv_p', 'tran', 'charge' and 'tran_4'. The measurements are defined in [*here*](python/writeTcl.py#L95).

## 'cv' and 'iv' measurements

- measurements are by default the capacitance and current measurements at the n+ electrode. Adding '_b' or '_p' means, the values belong to the back side or top pwell contacts.

- add ```--fit``` flag to fit the curves for determining the depletion and punch-through voltage. The methods are defines in *python/utils.py*

- add ```--free``` flag to keep the y-axis range adjusting autmatically, otherwise the range is fixe to [*link*](python/run.py#48).

## 'tran' 'charge' 'tran_4' measurements

- these are measurements of the current signals at the front side n+ electrode over time
- usually, you will define an induced signal charge, using e.g. the **HeavyIonModel** defining the induced charges as pC/&mu;m in the LET value. An examplaratory project is given in 'DB/ARCADIA50um_3D_particle1'.
- the measurements output the current signal over time, and the estimated Charge Collection Efficiency (CCE) as a function of time. This value is determined as ![CCE=\frac{\int{I}}{LET}](https://latex.codecogs.com/gif.latex?CCE=\frac{\int{I}}{LET}).
- !!ATTENTION!! the LET value is given as pC/&mu;m, thus needs the information of the thickness of your device under test. By defalut the thickness is assumed to be 100&mu;m. Use e.g. ```--thickness 50``` to set the value to 50&mu;.  

## Output

- the output csv files and plots are stored in:
```
_workingDir_/tcad/DB/_projectName_/tmp/
```
as:
```
_measurement_parameters.csv
_measurement_option_all.pdf
```
if you are testing e.g. one specific parameter, add ```--out _nwell_10um_``` and this is included in output string as *option*.

