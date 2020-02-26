#/home/cneubueser/synopsys/DB/Pixel25um/ARCADIA25um_epi4_pwell/tmp/print4.tcl
#MAKO: Output from Tcl commands history.
#load_file /home/cneubueser/synopsys/DB/Pixel25um/ARCADIA25um_epi4_pwell/n170_msh.tdr
create_plot -dataset n170_msh
select_plots {Plot_n170_msh}
#-> Plot_n170_msh
#-> Plot_n170_msh
#-> n170_msh
set_plot_prop -plot {Plot_n170_msh} -not_axes_interchanged
#-> 0
set_material_prop {Silicon} -plot Plot_n170_msh -geom n170_msh -show_mesh
#-> 0
set_material_prop {Silicon} -plot Plot_n170_msh -geom n170_msh -hide_mesh
#-> 0
set_legend_prop -plot Plot_n170_msh -position {0.8 0.5} -size {0.250596 0.3}
#-> 0
set_legend_prop -plot Plot_n170_msh -position {0.239353 0.497253} -size {0.250596 0.3}
#-> 0
set_legend_prop -plot Plot_n170_msh -position {0.312129 0.523004} -size {0.250596 0.3}
#-> 0
# export_view /home/cneubueser/synopsys/DB/Pixel25um/ARCADIA25um_epi4_pwell/print4.pdf -plots {Plot_n170_msh} -format pdf
#-> 0

