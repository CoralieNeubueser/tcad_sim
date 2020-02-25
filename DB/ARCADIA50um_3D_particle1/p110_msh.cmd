Title ""

Controls {
}

Definitions {
	Constant "ProfSub" {
		Species = "PhosphorusActiveConcentration"
		Value = 2.5e+12
	}
	Constant "ProfEpi" {
		Species = "PhosphorusActiveConcentration"
		Value = 2e+14
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
		MaxElementSize = ( 20 5 0 )
		MinElementSize = ( 0.2 0.2 0 )
		RefineFunction = MaxTransDiff(Variable = "DopingConcentration",Value = 1)
	}
	Refinement "RefDefSurf" {
		MaxElementSize = ( 2 1 0 )
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
		EvaluateWindow {
			Element = Rectangle [(0 0) (100 6.5)]
			DecayLength = 0.3
		}
	}
	AnalyticalProfile "PlacPwell1" {
		Reference = "ProfPwell"
		ReferenceElement {
			Element = Line [(0 0) (25 0)]
		}
	}
	AnalyticalProfile "PlacPwell2" {
		Reference = "ProfPwell"
		ReferenceElement {
			Element = Line [(75 0) (100 0)]
		}
	}
	AnalyticalProfile "PlacDPwell1" {
		Reference = "ProfDPwell"
		ReferenceElement {
			Element = Line [(0 0) (25 0)]
		}
	}
	AnalyticalProfile "PlacDPwell2" {
		Reference = "ProfDPwell"
		ReferenceElement {
			Element = Line [(75 0) (100 0)]
		}
	}
	AnalyticalProfile "PlacNwell" {
		Reference = "ProfNwell"
		ReferenceElement {
			Element = Line [(30 0) (70 0)]
		}
	}
	AnalyticalProfile "PlacPbot" {
		Reference = "ProfPbot"
		ReferenceElement {
			Element = Line [(0 300) (100 300)]
		}
	}
	Refinement "RefPlacGlobal" {
		Reference = "RefDefGlobal"
		RefineWindow = Rectangle [(-1 -1) (101 301)]
	}
	Refinement "RefPlacSurf" {
		Reference = "RefDefSurf"
		RefineWindow = Rectangle [(0 0) (100 10)]
	}
	Refinement "RefPlacBot" {
		Reference = "RefDefBot"
		RefineWindow = Rectangle [(0 298) (100 300)]
	}
}

