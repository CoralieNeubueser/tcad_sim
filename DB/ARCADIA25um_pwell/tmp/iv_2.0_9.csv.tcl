load_file /home/cneubueser/tcad_sim/DB/ARCADIA25um_pwell/iv_2.0_9.plt
create_plot -1d
select_plots {Plot_1}
#-> Plot_1
create_curve -plot Plot_1 -dataset {iv_2.0_9} -axisX {Pbot OuterVoltage} -axisY {Ntop TotalCurrent}
#-> Curve_1
export_curves {Curve_1} -plot Plot_1 -filename /home/cneubueser/tcad_sim/DB/ARCADIA25um_pwell/tmp/iv_2.0_9.csv -format csv -overwrite
