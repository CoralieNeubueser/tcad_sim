Title ""

Controls {
}

IOControls {
	EnableSections
}

Definitions {
	Constant "ProfSub" {
		Species = "PhosphorusActiveConcentration"
		Value = 2.5e+12
	}
	Constant "ProfEpi" {
		Species = "PhosphorusActiveConcentration"
		Value = 1e+14
	}
	AnalyticalProfile "ProfPwell" {
		Function = SubMesh1d(datafile = "./pwell.txt", scale = 1, range = line[ (0), (1.5) ])
		LateralFunction = Gauss(Factor = 0)
	}
	AnalyticalProfile "ProfNwell" {
		Function = SubMesh1d(datafile = "./nwell.txt", scale = 1, range = line[ (0), (1.8) ])
		LateralFunction = Gauss(Factor = 0)
	}
	AnalyticalProfile "ProfDPwell" {
		Function = SubMesh1d(datafile = "./dpwell.txt", scale = 1, range = line[ (0), (10) ])
		LateralFunction = Gauss(Factor = 0)
	}
	AnalyticalProfile "ProfPbot" {
		Species = "BoronActiveConcentration"
		Function = Gauss(PeakPos = 0, PeakVal = 1e+19, ValueAtDepth = 2.5e+12, Depth = 0.1)
		LateralFunction = Gauss(Factor = 0.8)
	}
	Refinement "RefDefGlobal" {
		MaxElementSize = ( 5 2 0 )
		MinElementSize = ( 0.2 0.2 0 )
		RefineFunction = MaxTransDiff(Variable = "DopingConcentration",Value = 1)
	}
	Refinement "RefDefSurf" {
		MaxElementSize = ( 0.3 0.3 0 )
		MinElementSize = ( 0.05 0.05 0 )
		RefineFunction = MaxTransDiff(Variable = "DopingConcentration",Value = 1)
	}
	Refinement "RefDefBot" {
		MaxElementSize = ( 10 0.5 0 )
		MinElementSize = ( 1 0.02 0 )
		RefineFunction = MaxTransDiff(Variable = "DopingConcentration",Value = 1)
	}
}

Placements {
	Constant "PlacSub" {
		Reference = "ProfSub"
		EvaluateWindow {
			Element = region ["substrate"]
		}
	}
	Constant "PlacEpi" {
		Reference = "ProfEpi"
		Replace
		EvaluateWindow {
			Element = Rectangle [(-1 -1) (26 7)]
			DecayLength = 0.3
		}
	}
	AnalyticalProfile "PlacPwell1" {
		Reference = "ProfPwell"
		ReferenceElement {
			Element = Line [(0 0) (10.75 0)]
		}
	}
	AnalyticalProfile "PlacPwell2" {
		Reference = "ProfPwell"
		ReferenceElement {
			Element = Line [(14.25 0) (25 0)]
		}
	}
	AnalyticalProfile "PlacDPwell1" {
		Reference = "ProfDPwell"
		ReferenceElement {
			Element = Line [(0 0) (10 0)]
		}
	}
	AnalyticalProfile "PlacDPwell2" {
		Reference = "ProfDPwell"
		ReferenceElement {
			Element = Line [(15 0) (25 0)]
		}
	}
	AnalyticalProfile "PlacNwell" {
		Reference = "ProfNwell"
		ReferenceElement {
			Element = Line [(11.25 0) (13.75 0)]
		}
	}
	AnalyticalProfile "PlacPbot" {
		Reference = "ProfPbot"
		ReferenceElement {
			Element = Line [(0 50) (25 50)]
		}
	}
	Refinement "RefPlacGlobal" {
		Reference = "RefDefGlobal"
		RefineWindow = Rectangle [(-1 -1) (26 51)]
	}
	Refinement "RefPlacSurf" {
		Reference = "RefDefSurf"
		RefineWindow = Rectangle [(0 0) (25 10)]
	}
	Refinement "RefPlacBot" {
		Reference = "RefDefBot"
		RefineWindow = Rectangle [(0 48) (25 50)]
	}
}

