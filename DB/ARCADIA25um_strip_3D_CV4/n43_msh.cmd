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
		MaxElementSize = ( 20 5 20 )
		MinElementSize = ( 2 2 2 )
		RefineFunction = MaxTransDiff(Variable = "DopingConcentration",Value = 1)
	}
	Refinement "RefDefSurf" {
		MaxElementSize = ( 2 2 2 )
		MinElementSize = ( 0.5 0.5 0.5 )
		RefineFunction = MaxTransDiff(Variable = "DopingConcentration",Value = 1)
	}
	Refinement "RefDefBot" {
		MaxElementSize = ( 4 1 4 )
		MinElementSize = ( 2 0.5 2 )
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
			Element = Cuboid [(-1 -1 -1) (26 7 26)]
			DecayLength = 0.3
		}
	}
	AnalyticalProfile "PlacPwell1" {
		Reference = "ProfPwell"
		ReferenceElement {
			Element = Polygon [ (0 0 0) (0 0 25) (7 0 25) (7 0 0)]
		}
	}
	AnalyticalProfile "PlacPwell2" {
		Reference = "ProfPwell"
		ReferenceElement {
			Element = Polygon [ (18 0 0) (18 0 25) (25 0 25) (25 0 0)]
		}
	}
	AnalyticalProfile "PlacDPwell1" {
		Reference = "ProfDPwell"
		ReferenceElement {
			Element = Polygon [ (0 0 0) (0 0 25) (7 0 25) (7 0 0)]
		}
	}
	AnalyticalProfile "PlacDPwell2" {
		Reference = "ProfDPwell"
		ReferenceElement {
			Element = Polygon [ (18 0 0) (18 0 25) (25 0 25) (25 0 0)]
		}
	}
	AnalyticalProfile "PlacNwell" {
		Reference = "ProfNwell"
		ReferenceElement {
			Element = Polygon [ (11.25 0 0) (11.25 0 25) (13.75 0 25) (13.75 0 0)]
		}
	}
	AnalyticalProfile "PlacPbot" {
		Reference = "ProfPbot"
		ReferenceElement {
			Element = Polygon [ (0 50 0) (0 50 25) (25 50 25) (25 50 0)]
		}
	}
	Refinement "RefPlacGlobal" {
		Reference = "RefDefGlobal"
		RefineWindow = Cuboid [(-1 -1 -1) (26 51 26)]
	}
	Refinement "RefPlacSurf" {
		Reference = "RefDefSurf"
		RefineWindow = Cuboid [(0 0 0) (25 10 25)]
	}
	Refinement "RefPlacBot" {
		Reference = "RefDefBot"
		RefineWindow = Cuboid [(0 48 0) (25 50 25)]
	}
}

