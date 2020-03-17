


	
Electrode {
	{ Name="Ntop_0_0" Voltage=0.0}
	{ Name="Ntop_0_1" Voltage=0.0}
	{ Name="Ntop_1_0" Voltage=0.0}
	{ Name="Ntop_1_1" Voltage=0.0}
	{ Name="Ptop" Voltage=0.0 }
	{ Name="Pbot" Voltage=0.0 }
}


File 	{
	Grid  = "n333_msh.tdr"
     	lifetime = "n333_msh.tdr"
     	param   = "pp443_des.par"
     	current = "n443_des.plt"   
     	plot    = "n443_des.tdr"  
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
	BreakCriteria{ Current(Contact="Pbot" AbsVal=1e-3) }    
}



Solve {
	Coupled(Iterations=100){ Poisson }
	Coupled{ Poisson Electron Hole }
	Quasistationary(
        		InitialStep=0.1 Increment=1.41 
           		MinStep=1e-6 MaxStep=0.1
           		Goal{ Name="Ntop_0_0" Voltage=0.8}
			Goal{ Name="Ntop_0_1" Voltage=0.8}
			Goal{ Name="Ntop_1_0" Voltage=0.8}
			Goal{ Name="Ntop_1_1" Voltage=0.8}
	) { Coupled { Poisson Electron Hole} }
	Quasistationary(
        		InitialStep=0.1 Increment=1.41 
           		MinStep=1e-8 MaxStep=0.1
           		Goal{ Name="Pbot" Voltage=-20 }
		Plot{Range=(0 1) intervals=1}
	) { Coupled { Poisson Electron Hole} }
}



