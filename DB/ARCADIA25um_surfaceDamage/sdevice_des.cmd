#----------------------------------------------------------------
#
#  Author: Lucio Pancheri
#  Date created: 17/2/2015
#  Last modified: 10/5/2019
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
     	current = "iv_@gap@_@S0@.plt"   
     	plot    = "iv_@gap@_@S0@.tdr"
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
#    		Avalanche( ElectricField )   # Avalanche breakdown model not needed
  	)
	Fermi
}
		
Physics (MaterialInterface="Silicon/SiO2") {
	Recombination(surfaceSRH)
	Traps(Conc=3e12 FixedCharge)

##	#follwoing PoS(RD09)019 1GGy of 12keV photons	
##	Traps(
##    	Acceptor Conc=4e12 Gaussian fromCondBand EnergyMid=0.35 EnergySig=0.05
##  	)
##	Traps(
##    	Acceptor Conc=4e13 Gaussian fromCondBand EnergyMid=0.6 EnergySig=0.05
##  	)

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
        		InitialStep=0.1 Increment=1.41 
           		MinStep=1e-6 MaxStep=0.1
           		Goal{ Name="Ntop" Voltage=@vn@ }
	) { Coupled { Poisson Electron Hole} }
	Quasistationary(
        		InitialStep=0.01 Increment=1.41 
           		MinStep=1e-8 MaxStep=0.01
           		Goal{ Name="Pbot" Voltage=@vbot@ }
		Plot{Range=(0 1) intervals=10}
	) { Coupled { Poisson Electron Hole} }
}


