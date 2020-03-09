# bash
#python python/run.py --project ARCADIA50um_surfaceDamage -m cv -p1 50 -p1Name 'd [$\mu$m]' -p2 5 -p2 10 -p2 15 -p2Name 'nwell [$\mu$m]' -p3 0 -p3 2.75 -p3 5 -p3 7.5 -p3Name 'gap [$\mu$m]' -p4 100 -p4Name 'S0 [cm/s]' --parameters 4 --out '_50um_'

#python python/run.py --project ARCADIA50um_surfaceDamage -m cv -p1 50 -p1Name 'd [$\mu$m]' -p2 5 -p2Name 'nwell [$\mu$m]' -p3 0 -p3 2.75 -p3 5 -p3 7.5 -p3Name 'gap [$\mu$m]' -p4 100 -p4Name 'S0 [cm/s]' --parameters 4 --out '_50um_nwell_5um_' --fit --fit_minX 5 --fit_maxX 60 --log 

python python/run.py --project ARCADIA50um_surfaceDamage -m iv -p1 50 -p1Name 'd [$\mu$m]' -p2 5 -p2Name 'nwell [$\mu$m]' -p3 0 -p3 2.75 -p3 5 -p3 7.5 -p3Name 'gap [$\mu$m]' -p4 100 -p4Name 'S0 [cm/s]' --parameters 4 --out '_50um_nwell_5um_' --log

python python/run.py --project ARCADIA50um_surfaceDamage -m iv -p1 50 -p1Name 'd [$\mu$m]' -p2 10 -p2Name 'nwell [$\mu$m]' -p3 0 -p3 2.75 -p3 5 -p3 7.5 -p3Name 'gap [$\mu$m]' -p4 100 -p4Name 'S0 [cm/s]' --parameters 4 --out '_50um_nwell_10um_' --log

python python/run.py --project ARCADIA50um_surfaceDamage -m iv -p1 50 -p1Name 'd [$\mu$m]' -p2 15 -p2Name 'nwell [$\mu$m]' -p3 0 -p3 2.75 -p3 5 -p3 7.5 -p3Name 'gap [$\mu$m]' -p4 100 -p4Name 'S0 [cm/s]' --parameters 4 --out '_50um_nwell_15um_' --log

#python python/run.py --project ARCADIA50um_surfaceDamage -m cv -p1 100 -p1Name 'd [$\mu$m]' -p2 5 -p2 10 -p2 15 -p2Name 'nwell [$\mu$m]' -p3 0 -p3 2.75 -p3 5 -p3 7.5 -p3Name 'gap [$\mu$m]' -p4 100 -p4Name 'S0 [cm/s]' --parameters 4 --out '_100um_'

#python python/run.py --project ARCADIA50um_surfaceDamage -m cv -p1 50 -p1Name 'd [$\mu$m]' -p2 5 -p2 10 -p2 15 -p2Name 'nwell [$\mu$m]' -p3 0 -p3Name 'gap [$\mu$m]' -p4 100 -p4Name 'S0 [cm/s]' --parameters 4 --out '_50um_gap_0um_'

#python python/run.py --project ARCADIA50um_surfaceDamage -m cv -p1 100 -p1Name 'd [$\mu$m]' -p2 5 -p2 10 -p2 15 -p2Name 'nwell [$\mu$m]' -p3 0 -p3Name 'gap [$\mu$m]' -p4 100 -p4Name 'S0 [cm/s]' --parameters 4 --out '_100um_gap_0um_'
