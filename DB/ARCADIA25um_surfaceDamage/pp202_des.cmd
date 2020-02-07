


	
Electrode {
	{ Name="Ntop" Voltage=0.0}
	{ Name="Ptop" Voltage=0.0 }
	{ Name="Pbot" Voltage=0.0 }
}


File 	{
	Grid  = "n198_msh.tdr"
     	lifetime = "n198_msh.tdr"
     	param   = "pp202_des.par"
     	current = "iv_2.0_100.plt"   
     	plot    = "iv_2.0_100.tdr"
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
		
Physics (MaterialInterface="Silicon/SiO2") {
	Recombination(surfaceSRH)
	Traps(Conc=3e12 FixedCharge)


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
	BreakCriteria{ Current(Contact="Pbot" AbsVal=1e-4) }    
}



Solve {
	Coupled(Iterations=100){ Poisson }
	Coupled{ Poisson Electron Hole }
	Quasistationary(
        		InitialStep=0.1 Increment=1.41 
           		MinStep=1e-6 MaxStep=0.1
           		Goal{ Name="Ntop" Voltage=0.8 }
	) { Coupled { Poisson Electron Hole} }
	Quasistationary(
        		InitialStep=0.01 Increment=1.41 
           		MinStep=1e-8 MaxStep=0.01
           		Goal{ Name="Pbot" Voltage=-50 }
		Plot{Range=(0 1) intervals=10}
	) { Coupled { Poisson Electron Hole} }
}



