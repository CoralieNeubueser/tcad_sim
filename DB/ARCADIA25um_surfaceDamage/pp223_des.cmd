



Device MAPD {
	
	
Electrode {
	{ Name="Ntop" Voltage=0.0}
	{ Name="Ptop" Voltage=0.0 }
	{ Name="Pbot" Voltage=0.0 }
}


File 	{
	Grid  = "n170_msh.tdr"
     	lifetime = "n170_msh.tdr"
     	param   = "pp223_des.par"
     	current = "4.25_1000.plt"  
     	plot    = "4.25_1000.tdr"  
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

				
} # device	


File {
	Output = "n223_des.log"
	ACExtract = "ac_4.25_1000"
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



