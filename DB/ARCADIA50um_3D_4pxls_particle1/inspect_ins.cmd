set N     @node@

proj_load  tran_@plot@ PLT($N)
cv_create ITcurve "PLT($N) NO_NODE time" "PLT($N) Ntop TotalCurrent" y
load_library extend
set XMIN [cv_getXmin ITcurve]
set XMAX [cv_getXmax ITcurve]
set QN [cv_integrate "<ITcurve>/1.6e-19" $XMIN $XMAX trapez]
ft_scalar Qpix $QN

