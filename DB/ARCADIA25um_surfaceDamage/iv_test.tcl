#!/usr/bin/tclsh

set arg1 0.
set arg2 0.

puts $argc

if { $argc!=2 }{
    puts "This scrips requires 2 arguments."
    puts "Please try again."
} else {
    puts [expr [lindex $argv 0] + [lindex $argv 1]]
    set arg1 [lindex $argv 0]
    set arg2 [lindex $argv 1]
}

load_file "/home/cneubueser/synopsys/DB/Pixel25um/ARCADIA25um_surfaceDamage/iv_${arg1}_${arg2}.plt"

create_plot -1d
select_plots {Plot_1}
#-> Plot_1
#-> Plot_1
#-> cv_n274_ac_des
create_curve -plot Plot_1 -dataset {"iv_${arg1}_${arg2}"} -axisX v(Pbot) -axisY c(Ntop,Ntop)
#-> Curve_1
export_curves {Curve_1} -plot Plot_1 -filename /home/cneubueser/synopsys/DB/Pixel25um/ARCADIA25um_surfaceDamage/tmp/iv_${arg1}_${arg2}.csv -format csv -overwrite

#export_curves {Curve_1} -plot Plot_1 -filename /home/cneubueser/synopsys/DB/Pixel25um/ARCADIA25um_epi4_surfaceDamage/tmp/cv_4.25_100.csv -format csv
#-> /home/cneubueser/synopsys/DB/Pixel25um/ARCADIA25um_pwell/cv_test.csv

