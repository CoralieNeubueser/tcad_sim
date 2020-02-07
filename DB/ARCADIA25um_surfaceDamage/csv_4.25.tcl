#/home/cneubueser/synopsys/DB/Pixel25um/ARCADIA25um_pwell/cv_test.tcl
#MAKO: Output from Tcl commands history.
load_file /home/cneubueser/synopsys/DB/Pixel25um/ARCADIA25um_epi4_surfaceDamage/cv_n174_ac_des.plt
create_plot -1d
select_plots {Plot_1}
#-> Plot_1
#-> Plot_1
#-> cv_n274_ac_des
create_curve -plot Plot_1 -dataset {cv_n174_ac_des} -axisX v(Pbot) -axisY c(Ntop,Ntop)
#-> Curve_1
export_curves {Curve_1} -plot Plot_1 -filename /home/cneubueser/synopsys/DB/Pixel25um/ARCADIA25um_epi4_surfaceDamage/cv_4.25.csv -format csv
#-> /home/cneubueser/synopsys/DB/Pixel25um/ARCADIA25um_pwell/cv_test.csv

