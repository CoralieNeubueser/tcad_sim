#/home/cneubueser/synopsys/DB/Pixel25um/ARCADIA25um_pwell/cv_test.tcl
#MAKO: Output from Tcl commands history.
load_file /home/cneubueser/synopsys/DB/Pixel25um/ARCADIA25um_surfaceDamage/cv_ac_4.25_100_ac_des.plt
#/home/cneubueser/synopsys/DB/Pixel25um/ARCADIA25um_surfaceDamage/cv_diode_cv_4.25_100.tdr
create_plot -1d
select_plots {Plot_1}
#-> Plot_1
#-> Plot_1
#-> cv_n274_ac_des
create_curve -plot Plot_1 -dataset {cv_ac_4.25_100_ac_des} -axisX v(Pbot) -axisY c(Ntop,Ntop)
#-> Curve_1
export_curves {Curve_1} -plot Plot_1 -filename /home/cneubueser/synopsys/DB/Pixel25um/ARCADIA25um_surfaceDamage/tmp/cv_425_100.csv -format csv -overwrite

#export_curves {Curve_1} -plot Plot_1 -filename /home/cneubueser/synopsys/DB/Pixel25um/ARCADIA25um_epi4_surfaceDamage/tmp/cv_4.25_100.csv -format csv
#-> /home/cneubueser/synopsys/DB/Pixel25um/ARCADIA25um_pwell/cv_test.csv

