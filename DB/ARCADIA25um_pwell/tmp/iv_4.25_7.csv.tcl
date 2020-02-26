load_file /home/cneubueser/tcad_sim/DB/ARCADIA25um_pwell/iv_4.25_7.plt
create_plot -1d
select_plots {Plot_1}
#-> Plot_1
create_curve -plot Plot_1 -dataset {iv_4.25_7} -axisX {Pbot OuterVoltage} -axisY {Ntop TotalCurrent}
#-> Curve_1
export_curves {Curve_1} -plot Plot_1 -filename /home/cneubueser/tcad_sim/DB/ARCADIA25um_pwell/tmp/iv_4.25_7.csv -format csv -overwrite
