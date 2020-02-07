load_file /home/cneubueser/tcad_sim/DB/ARCADIA25um_surfaceDamage/iv_2.0_1000.plt
create_plot -1d
select_plots {Plot_1}
#-> Plot_1
create_curve -plot Plot_1 -dataset {iv_2.0_1000} -axisX {Pbot OuterVoltage} -axisY {Ptop TotalCurrent}
#-> Curve_1
export_curves {Curve_1} -plot Plot_1 -filename /home/cneubueser/tcad_sim/DB/ARCADIA25um_surfaceDamage/tmp/iv_b_2.0_1000.csv -format csv -overwrite
