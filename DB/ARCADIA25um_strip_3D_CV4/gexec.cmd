# project name
name ARCADIA25um_strip_3D_CV4
# execution graph
job 47 -d "43"  -post { extract_vars "$wdir" n47_des.out 47 }  -o n47_des "sdevice pp47_des.cmd"
job 46 -d "43"  -post { extract_vars "$wdir" n46_des.out 46 }  -o n46_des "sdevice pp46_des.cmd"
job 43   -post { extract_vars "$wdir" n43_dvs.out 43 }  -o n43_dvs "sde -e -l n43_dvs.cmd"
check sde_dvs.cmd 1581345072
check sdevice_des.cmd 1579711406
check sdevice.par 1579711403
check sdevice1_des.cmd 1582709470
check global_tooldb 1556860855
check gtree.dat 1581342114
# included files
