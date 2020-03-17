load_file /home/neubuser/tcad_sim/DB/ARCADIA50um_3D_4pxls_particle1/tran_50_0_0_-7_1.28e-5.plt
create_plot -1d
select_plots {Plot_1}
#-> Plot_1
create_curve -plot Plot_1 -dataset {tran_50_0_0_-7_1.28e-5} -axisX time -axisY {Ntop_0_0 TotalCurrent}
create_curve -plot Plot_1 -dataset {tran_50_0_0_-7_1.28e-5} -axisX time -axisY {Ntop_0_1 TotalCurrent}
create_curve -plot Plot_1 -dataset {tran_50_0_0_-7_1.28e-5} -axisX time -axisY {Ntop_1_0 TotalCurrent}
create_curve -plot Plot_1 -dataset {tran_50_0_0_-7_1.28e-5} -axisX time -axisY {Ntop_1_1 TotalCurrent}
#-> Curve_1
export_curves {Curve_1 Curve_2 Curve_3 Curve_4} -plot Plot_1 -filename /home/neubuser/tcad_sim/DB/ARCADIA50um_3D_4pxls_particle1/tmp/tran_4_50_0_0_-7_1.28e-5.csv -format csv -overwrite
