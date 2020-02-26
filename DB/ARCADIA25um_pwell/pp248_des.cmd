



Device MAPD {
	
	
Electrode {
	{ Name="Ntop" Voltage=0.0}
	{ Name="Ptop" Voltage=0.0 }
	{ Name="Pbot" Voltage=0.0 }
}


File 	{
	Grid  = "n244_msh.tdr"
     	lifetime = "n244_msh.tdr"
     	param   = "pp248_des.par"
     	current = "0.5_9.plt"  
     	plot    = "0.5_9.tdr"  
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

				
} # device	


File {
	Output = "n248_des.log"
	ACExtract = "ac_0.5_9"
}

Math 	{
	Digits=5
	Extrapolate
	Iterations=30
	Notdamped =100
	RelErrControl
	BreakCriteria{ Current(Contact="Pbot" AbsVal=1e-4) }    
}

System {
 	MAPD diode (Ntop Ptop Pbot)
  	Vsource_pset  vnt (Ntop  0) {dc=0}
 	Vsource_pset  vpt (Ptop  0) {dc=0}
 	Vsource_pset  vpb (Pbot  0) {dc=0}
 }


Solve {
	Coupled(Iterations=100){ Poisson }
	Coupled{ Poisson Electron Hole }
	Quasistationary(
        		InitialStep=1e-2 Increment=1.41 
           		MinStep=1e-6 MaxStep=0.1
		Goal { Parameter=vnt.dc Voltage=0.8 }
	) { Coupled { Poisson Electron Hole} }
	
	newcurrentprefix = "cv_"
  	
   	Quasistationary (
		InitialStep=0.001 MaxStep=0.01 MinStep=1.e-5
		Goal { Parameter=vpb.dc Voltage=-50 }
	) { ACCoupled (
		StartFrequency=10e3 EndFrequency=10e3
		NumberOfPoints=1 Decade
		Node(Ntop Ptop Pbot) Exclude(vnt vpt vpb)
	) { Poisson Electron Hole }
	}
	
}



