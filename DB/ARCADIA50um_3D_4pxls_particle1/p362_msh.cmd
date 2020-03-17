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
	AnalyticalProfile "ProfPbot" {
		Species = "BoronActiveConcentration"
		Function = Gauss(PeakPos = 0, PeakVal = 1e+19, ValueAtDepth = 2.5e+12, Depth = 0.1)
		LateralFunction = Gauss(Factor = 0.8)
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
			Element = Cuboid [(-1 -1 -1) (101 7 101)]
			DecayLength = 0.3
		}
	}
	AnalyticalProfile "PlacPbot" {
		Reference = "ProfPbot"
		ReferenceElement {
			Element = Polygon [ (0 50 0) (0 50 100) (100 50 100) (100 50 0)]
		}
	}
	AnalyticalProfile "PlacPtop1_0_0" {
		Reference = "ProfPwell"
		ReferenceElement {
			Element = Polygon [ (0 0 0) (0 0 50) (15 0 50) (15 0 0)]
		}
	}
	AnalyticalProfile "PlacPtop2_0_0" {
		Reference = "ProfPwell"
		ReferenceElement {
			Element = Polygon [ (35 0 0) (35 0 50) (50 0 50) (50 0 0)]
		}
	}
	AnalyticalProfile "PlacPtop3_0_0" {
		Reference = "ProfPwell"
		ReferenceElement {
			Element = Polygon [ (15 0 0) (15 0 15) (35 0 15) (35 0 0)]
		}
	}
	AnalyticalProfile "PlacPtop4_0_0" {
		Reference = "ProfPwell"
		ReferenceElement {
			Element = Polygon [ (15 0 35) (15 0 50) (35 0 50) (35 0 35)]
		}
	}
	AnalyticalProfile "PlacDPtop1_0_0" {
		Reference = "ProfDPwell"
		ReferenceElement {
			Element = Polygon [ (0 0 0) (0 0 50) (15 0 50) (15 0 0)]
		}
	}
	AnalyticalProfile "PlacDPtop2_0_0" {
		Reference = "ProfDPwell"
		ReferenceElement {
			Element = Polygon [ (35 0 0) (35 0 50) (50 0 50) (50 0 0)]
		}
	}
	AnalyticalProfile "PlacDPtop3_0_0" {
		Reference = "ProfDPwell"
		ReferenceElement {
			Element = Polygon [ (15 0 0) (15 0 15) (35 0 15) (35 0 0)]
		}
	}
	AnalyticalProfile "PlacDPtop4_0_0" {
		Reference = "ProfDPwell"
		ReferenceElement {
			Element = Polygon [ (15 0 35) (15 0 50) (35 0 50) (35 0 35)]
		}
	}
	AnalyticalProfile "PlacNtop_0_0" {
		Reference = "ProfNwell"
		ReferenceElement {
			Element = Polygon [ (20 0 20) (20 0 30) (30 0 30) (30 0 20)]
		}
	}
	AnalyticalProfile "PlacPtop1_0_1" {
		Reference = "ProfPwell"
		ReferenceElement {
			Element = Polygon [ (0 0 50) (0 0 100) (15 0 100) (15 0 50)]
		}
	}
	AnalyticalProfile "PlacPtop2_0_1" {
		Reference = "ProfPwell"
		ReferenceElement {
			Element = Polygon [ (35 0 50) (35 0 100) (50 0 100) (50 0 50)]
		}
	}
	AnalyticalProfile "PlacPtop3_0_1" {
		Reference = "ProfPwell"
		ReferenceElement {
			Element = Polygon [ (15 0 50) (15 0 65) (35 0 65) (35 0 50)]
		}
	}
	AnalyticalProfile "PlacPtop4_0_1" {
		Reference = "ProfPwell"
		ReferenceElement {
			Element = Polygon [ (15 0 85) (15 0 100) (35 0 100) (35 0 85)]
		}
	}
	AnalyticalProfile "PlacDPtop1_0_1" {
		Reference = "ProfDPwell"
		ReferenceElement {
			Element = Polygon [ (0 0 50) (0 0 100) (15 0 100) (15 0 50)]
		}
	}
	AnalyticalProfile "PlacDPtop2_0_1" {
		Reference = "ProfDPwell"
		ReferenceElement {
			Element = Polygon [ (35 0 50) (35 0 100) (50 0 100) (50 0 50)]
		}
	}
	AnalyticalProfile "PlacDPtop3_0_1" {
		Reference = "ProfDPwell"
		ReferenceElement {
			Element = Polygon [ (15 0 50) (15 0 65) (35 0 65) (35 0 50)]
		}
	}
	AnalyticalProfile "PlacDPtop4_0_1" {
		Reference = "ProfDPwell"
		ReferenceElement {
			Element = Polygon [ (15 0 85) (15 0 100) (35 0 100) (35 0 85)]
		}
	}
	AnalyticalProfile "PlacNtop_0_1" {
		Reference = "ProfNwell"
		ReferenceElement {
			Element = Polygon [ (20 0 70) (20 0 80) (30 0 80) (30 0 70)]
		}
	}
	AnalyticalProfile "PlacPtop1_1_0" {
		Reference = "ProfPwell"
		ReferenceElement {
			Element = Polygon [ (50 0 0) (50 0 50) (65 0 50) (65 0 0)]
		}
	}
	AnalyticalProfile "PlacPtop2_1_0" {
		Reference = "ProfPwell"
		ReferenceElement {
			Element = Polygon [ (85 0 0) (85 0 50) (100 0 50) (100 0 0)]
		}
	}
	AnalyticalProfile "PlacPtop3_1_0" {
		Reference = "ProfPwell"
		ReferenceElement {
			Element = Polygon [ (65 0 0) (65 0 15) (85 0 15) (85 0 0)]
		}
	}
	AnalyticalProfile "PlacPtop4_1_0" {
		Reference = "ProfPwell"
		ReferenceElement {
			Element = Polygon [ (65 0 35) (65 0 50) (85 0 50) (85 0 35)]
		}
	}
	AnalyticalProfile "PlacDPtop1_1_0" {
		Reference = "ProfDPwell"
		ReferenceElement {
			Element = Polygon [ (50 0 0) (50 0 50) (65 0 50) (65 0 0)]
		}
	}
	AnalyticalProfile "PlacDPtop2_1_0" {
		Reference = "ProfDPwell"
		ReferenceElement {
			Element = Polygon [ (85 0 0) (85 0 50) (100 0 50) (100 0 0)]
		}
	}
	AnalyticalProfile "PlacDPtop3_1_0" {
		Reference = "ProfDPwell"
		ReferenceElement {
			Element = Polygon [ (65 0 0) (65 0 15) (85 0 15) (85 0 0)]
		}
	}
	AnalyticalProfile "PlacDPtop4_1_0" {
		Reference = "ProfDPwell"
		ReferenceElement {
			Element = Polygon [ (65 0 35) (65 0 50) (85 0 50) (85 0 35)]
		}
	}
	AnalyticalProfile "PlacNtop_1_0" {
		Reference = "ProfNwell"
		ReferenceElement {
			Element = Polygon [ (70 0 20) (70 0 30) (80 0 30) (80 0 20)]
		}
	}
	AnalyticalProfile "PlacPtop1_1_1" {
		Reference = "ProfPwell"
		ReferenceElement {
			Element = Polygon [ (50 0 50) (50 0 100) (65 0 100) (65 0 50)]
		}
	}
	AnalyticalProfile "PlacPtop2_1_1" {
		Reference = "ProfPwell"
		ReferenceElement {
			Element = Polygon [ (85 0 50) (85 0 100) (100 0 100) (100 0 50)]
		}
	}
	AnalyticalProfile "PlacPtop3_1_1" {
		Reference = "ProfPwell"
		ReferenceElement {
			Element = Polygon [ (65 0 50) (65 0 65) (85 0 65) (85 0 50)]
		}
	}
	AnalyticalProfile "PlacPtop4_1_1" {
		Reference = "ProfPwell"
		ReferenceElement {
			Element = Polygon [ (65 0 85) (65 0 100) (85 0 100) (85 0 85)]
		}
	}
	AnalyticalProfile "PlacDPtop1_1_1" {
		Reference = "ProfDPwell"
		ReferenceElement {
			Element = Polygon [ (50 0 50) (50 0 100) (65 0 100) (65 0 50)]
		}
	}
	AnalyticalProfile "PlacDPtop2_1_1" {
		Reference = "ProfDPwell"
		ReferenceElement {
			Element = Polygon [ (85 0 50) (85 0 100) (100 0 100) (100 0 50)]
		}
	}
	AnalyticalProfile "PlacDPtop3_1_1" {
		Reference = "ProfDPwell"
		ReferenceElement {
			Element = Polygon [ (65 0 50) (65 0 65) (85 0 65) (85 0 50)]
		}
	}
	AnalyticalProfile "PlacDPtop4_1_1" {
		Reference = "ProfDPwell"
		ReferenceElement {
			Element = Polygon [ (65 0 85) (65 0 100) (85 0 100) (85 0 85)]
		}
	}
	AnalyticalProfile "PlacNtop_1_1" {
		Reference = "ProfNwell"
		ReferenceElement {
			Element = Polygon [ (70 0 70) (70 0 80) (80 0 80) (80 0 70)]
		}
	}
	Refinement "RefPlacGlobal" {
		Reference = "RefDefGlobal"
		RefineWindow = Cuboid [(-1 -1 -1) (101 51 101)]
	}
	Refinement "RefPlacSurf" {
		Reference = "RefDefSurf"
		RefineWindow = Cuboid [(0 0 0) (100 10 100)]
	}
	Refinement "RefPlacBot" {
		Reference = "RefDefBot"
		RefineWindow = Cuboid [(0 48 0) (100 50 100)]
	}
	Refinement "RefPlacPart" {
		Reference = "RefDefPart"
		RefineWindow = Cuboid [(-2 0 -2) (2 50 2)]
	}
}

