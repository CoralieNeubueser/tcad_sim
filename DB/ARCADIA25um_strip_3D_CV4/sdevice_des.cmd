#----------------------------------------------------------------
#
#  Author: Lucio Pancheri
#  Date created: 17/2/2015
#  Last modified: 17/2/2015
#
#----------------------------------------------------------------


#define _Idmax_ 1e-4

	
Electrode {
	{ Name="Ntop" Voltage=0.0}
	{ Name="Ptop" Voltage=0.0 }
	{ Name="Pbot" Voltage=0.0 }
}


File 	{
	Grid  = "@tdr@"
     	lifetime = "@tdr@"
     	param   = "@parameter@"
     	current = "@plot@"   # .plt inspect
     	save	= "n@node@_initial_condition"
     	plot    = "@tdrdat@"   # .dat  tecplot_sv
}

		
Physics{
	Temperature = 300	
	EffectiveIntrinsicDensity( OldSlotboom )     
	Mobility(
  	 	DopingDep
    		HighFieldsaturation( GradQuasiFermi )
    		Enormal
  	)
  	Recombination(
    		SRH( DopingDep )
    		Band2Band(E2)
#    		Avalanche( ElectricField )
  	)
	Fermi
}
		
		
Plot	{
	eDensity hDensity
	TotalCurrent/Vector eCurrent/Vector hCurrent/Vector
	ElectricField/Vector Potential SpaceCharge
	Doping 
	SRH  Auger
	eLifetime hLifetime   
}


Math 	{
	Digits=5
	Extrapolate
	Iterations=30
	Notdamped =100
	RelErrControl
	BreakCriteria{ Current(Contact="Pbot" AbsVal=_Idmax_) }    
}



Solve {
	Coupled(Iterations=100){ Poisson }
	Coupled{ Poisson Electron Hole }
	Quasistationary(
        		InitialStep=1e-2 Increment=1.41 
           		MinStep=1e-6 MaxStep=0.1
           		Goal{ Name="Ntop" Voltage=@vn@ }
	) { Coupled { Poisson Electron Hole} }
	Quasistationary(
        		InitialStep=1e-3 Increment=1.41 
           		MinStep=1e-8 MaxStep=0.01
           		Goal{ Name="Pbot" Voltage=@vbot@ }
		Plot{Range=(0 1) intervals=1}
	) { Coupled { Poisson Electron Hole} }
}

