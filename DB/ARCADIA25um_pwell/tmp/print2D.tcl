#/home/cneubueser/synopsys/DB/Pixel25um/ARCADIA25um_epi4_pwell/tmp/print2D.tcl
#MAKO: Output from Tcl commands history.
load_file /home/cneubueser/synopsys/DB/Pixel25um/ARCADIA25um_epi4_pwell/n178_000010_des.tdr
create_plot -dataset n178_000010_des
select_plots {Plot_n178_000010_des}
#-> Plot_n178_000010_des
#-> Plot_n178_000010_des
#-> n178_000010_des
set_field_prop -plot Plot_n178_000010_des -geom n178_000010_des ElectricField-X -show_bands
#-> 0
set_field_prop -plot Plot_n178_000010_des -geom n178_000010_des Abs(ElectricField-V) -show_bands
#-> 0
set_plot_prop -plot {Plot_n178_000010_des} -not_axes_interchanged
#-> 0
zoom_plot -plot Plot_n178_000010_des -window {27.3589 -1.03527 -2.5166 7.8444}
create_streamline -plot Plot_n178_000010_des -field ElectricField-V -p1 {0 50} -p2 {25 0} -direction both -nofpoints 2 -integ_initial_step 0.25 -integ_max_steps 120000 -integ_terminal_speed 0.318431 -integ_max_propagation 30000
#!-> Error: create_streamline: Creation of Streamline(s) couldn't be done.
create_streamline -plot Plot_n178_000010_des -field ElectricField-V -p1 {0 50} -p2 {25 0} -direction both -nofpoints 10 -integ_initial_step 0.25 -integ_max_steps 120000 -integ_terminal_speed 0.318431 -integ_max_propagation 30000
#-> Streamline_4 Streamline_5 Streamline_6 Streamline_7 Streamline_8 Streamline_9 Streamline_10 Streamline_11
zoom_plot -plot Plot_n178_000010_des -factor 0.909091
zoom_plot -plot Plot_n178_000010_des -factor 0.909091
zoom_plot -plot Plot_n178_000010_des -factor 0.909091
zoom_plot -plot Plot_n178_000010_des -factor 0.909091
zoom_plot -plot Plot_n178_000010_des -factor 0.909091
zoom_plot -plot Plot_n178_000010_des -factor 0.909091
zoom_plot -plot Plot_n178_000010_des -factor 0.909091
zoom_plot -plot Plot_n178_000010_des -factor 0.909091
zoom_plot -plot Plot_n178_000010_des -factor 0.909091
zoom_plot -plot Plot_n178_000010_des -factor 0.909091
zoom_plot -plot Plot_n178_000010_des -factor 0.909091
zoom_plot -plot Plot_n178_000010_des -factor 0.909091
zoom_plot -plot Plot_n178_000010_des -factor 0.909091
zoom_plot -plot Plot_n178_000010_des -factor 0.909091
zoom_plot -plot Plot_n178_000010_des -factor 1.1
zoom_plot -plot Plot_n178_000010_des -factor 1.1
zoom_plot -plot Plot_n178_000010_des -factor 1.1
zoom_plot -plot Plot_n178_000010_des -factor 1.1
zoom_plot -plot Plot_n178_000010_des -factor 1.1
zoom_plot -plot Plot_n178_000010_des -factor 1.1
zoom_plot -plot Plot_n178_000010_des -factor 1.1
zoom_plot -plot Plot_n178_000010_des -factor 1.1
zoom_plot -plot Plot_n178_000010_des -factor 1.1
zoom_plot -plot Plot_n178_000010_des -factor 1.1
zoom_plot -plot Plot_n178_000010_des -factor 1.1
zoom_plot -plot Plot_n178_000010_des -factor 1.1
zoom_plot -plot Plot_n178_000010_des -factor 1.1
zoom_plot -plot Plot_n178_000010_des -factor 1.1
zoom_plot -plot Plot_n178_000010_des -factor 1.1
zoom_plot -plot Plot_n178_000010_des -factor 1.1
zoom_plot -plot Plot_n178_000010_des -factor 1.1
zoom_plot -plot Plot_n178_000010_des -factor 1.1
set_field_prop -plot Plot_n178_000010_des -geom n178_000010_des ElectricField-X -show_bands
#-> 0
set_field_prop -plot Plot_n178_000010_des -geom n178_000010_des ElectricField-Y -show_bands
#-> 0
set_field_prop -plot Plot_n178_000010_des -geom n178_000010_des ElectricField-X -show_bands
#-> 0
set_field_prop -plot Plot_n178_000010_des -geom n178_000010_des DopingConcentration -show_bands
#-> 0
set_field_prop -plot Plot_n178_000010_des -geom n178_000010_des Abs(ElectricField-V) -show_bands
#-> 0
zoom_plot -plot Plot_n178_000010_des -window {26.0321 -1.30118 -1.18977 14.3648}
export_view /home/cneubueser/synopsys/DB/Pixel25um/ARCADIA25um_epi4_pwell/elFieldLines_zoom.pdf -plots {Plot_n178_000010_des} -format pdf -overwrite
#-> 0
set_field_prop -plot Plot_n178_000010_des -geom n178_000010_des DopingConcentration -show_bands
#-> 0
export_view /home/cneubueser/synopsys/DB/Pixel25um/ARCADIA25um_epi4_pwell/doping_zoom.pdf -plots {Plot_n178_000010_des} -format pdf -overwrite
#-> 0

