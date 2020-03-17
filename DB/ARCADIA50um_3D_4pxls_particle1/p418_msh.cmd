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
		MinElementSize = ( 4 4 4 )
		RefineFunction = MaxTransDiff(Variable = "DopingConcentration",Value = 1)
	}
	Refinement "RefDefSurf" {
		MaxElementSize = ( 2.5 2.5 2.5 )
		MinElementSize = ( 0.5 0.5 0.5 )
		RefineFunction = MaxTransDiff(Variable = "DopingConcentration",Value = 1)
	}
	Refinement "RefDefBot" {
		MaxElementSize = ( 10 2 10 )
		MinElementSize = ( 4 1 4 )
		RefineFunction = MaxTransDiff(Variable = "DopingConcentration",Value = 1)
	}
	Refinement "RefDefPart" {
		MaxElementSize = ( 0.4 5 0.4 )
		MinElementSize = ( 0.15 0.25 0.15 )
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
			Element = Cuboid [(-1 -1 -1) (51 7 51)]
			DecayLength = 0.3
		}
	}
	AnalyticalProfile "PlacPwell1" {
		Reference = "ProfPwell"
		ReferenceElement {
			Element = Polygon [ (0 0 0) (0 0 50) (15 0 50) (15 0 0)]
		}
	}
	AnalyticalProfile "PlacPwell2" {
		Reference = "ProfPwell"
		ReferenceElement {
			Element = Polygon [ (35 0 0) (35 0 50) (50 0 50) (50 0 0)]
		}
	}
	AnalyticalProfile "PlacPwell3" {
		Reference = "ProfPwell"
		ReferenceElement {
			Element = Polygon [ (15 0 0) (15 0 15) (35 0 15) (35 0 0)]
		}
	}
	AnalyticalProfile "PlacPwell4" {
		Reference = "ProfPwell"
		ReferenceElement {
			Element = Polygon [ (15 0 35) (15 0 50) (35 0 50) (35 0 35)]
		}
	}
	AnalyticalProfile "PlacDPwell1" {
		Reference = "ProfDPwell"
		ReferenceElement {
			Element = Polygon [ (0 0 0) (0 0 50) (15 0 50) (15 0 0)]
		}
	}
	AnalyticalProfile "PlacDPwell2" {
		Reference = "ProfDPwell"
		ReferenceElement {
			Element = Polygon [ (35 0 0) (35 0 50) (50 0 50) (50 0 0)]
		}
	}
	AnalyticalProfile "PlacDPwell3" {
		Reference = "ProfDPwell"
		ReferenceElement {
			Element = Polygon [ (15 0 0) (15 0 15) (35 0 15) (35 0 0)]
		}
	}
	AnalyticalProfile "PlacDPwell4" {
		Reference = "ProfDPwell"
		ReferenceElement {
			Element = Polygon [ (15 0 35) (15 0 50) (35 0 50) (35 0 35)]
		}
	}
	AnalyticalProfile "PlacNwell" {
		Reference = "ProfNwell"
		ReferenceElement {
			Element = Polygon [ (20 0 20) (20 0 30) (30 0 30) (30 0 20)]
		}
	}
	AnalyticalProfile "PlacPbot" {
		Reference = "ProfPbot"
		ReferenceElement {
			Element = Polygon [ (0 50 0) (0 50 50) (50 50 50) (50 50 0)]
		}
	}
	Refinement "RefPlacGlobal" {
		Reference = "RefDefGlobal"
		RefineWindow = Cuboid [(-1 -1 -1) (51 51 51)]
	}
	Refinement "RefPlacSurf" {
		Reference = "RefDefSurf"
		RefineWindow = Cuboid [(0 0 0) (50 10 50)]
	}
	Refinement "RefPlacBot" {
		Reference = "RefDefBot"
		RefineWindow = Cuboid [(0 48 0) (50 50 50)]
	}
	Refinement "RefPlacPart" {
		Reference = "RefDefPart"
		RefineWindow = Cuboid [(23 0 10.5) (27 50 14.5)]
	}
}

