


	
	
Electrode {
	{ Name="Ntop_0_0" Voltage=0.8}
	{ Name="Ntop_0_1" Voltage=0.8}
	{ Name="Ntop_1_0" Voltage=0.8}
	{ Name="Ntop_1_1" Voltage=0.8}
	{ Name="Ptop" Voltage=0 }
	{ Name="Pbot" Voltage=-17 }
}


File 	{
	Grid  = "n362_msh.tdr"
     	lifetime = "n362_msh.tdr"
     	param   = "pp367_des.par"
     	current = "50_0_0_-17_1.28e-5.plt"  
     	plot    = "50_0_0_-17_1.28e-5.tdr"  
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
        HeavyIon (
               	Direction =(0,1,0)
               	Location =(0,0,0)
               	Time=1e-11
               	Length=50
               	wt_hi=0.5
               	LET_f=1.28e-5
               	Gaussian
               	PicoCoulomb
        )

}


Plot	{
	eDensity hDensity
	TotalCurrent/Vector eCurrent/Vector hCurrent/Vector
	ElectricField/Vector Potential SpaceCharge
	Doping 
	SRH  Auger
	eLifetime hLifetime 
	HeavyIonChargeDensity  
}



Math 	{
	Number_of_Threads = 12
	Number_of_Solver_Threads = 12
	Digits=7
	Extrapolate
	Iterations=30
	Notdamped =100
	RelErrControl
	BreakCriteria{ Current(Contact="Pbot" AbsVal=1e-4) } 
	RecBoxIntegr (1e-2 10 1000)
}


Solve {
    load(Fileprefix="n365_000001")

    NewCurrentFile="tran_"
    Transient(
	InitialTime=0.0
	FinalTime=1e-7
	InitialStep=5e-13
	MaxStep=5e-9
	MinStep=1e-15
	Increment=1.5
	)
    { Coupled { Poisson Electron Hole} }


  
}



