
;; Defined Parameters:

;; Contact Sets:
(sdegeo:define-contact-set "Ptop_0_0" 4 (color:rgb 1 0 0 )"##" )
(sdegeo:define-contact-set "Ntop_0_0" 4 (color:rgb 0 1 0 )"##" )
(sdegeo:define-contact-set "Ptop_0_1" 4 (color:rgb 1 0 0 )"##" )
(sdegeo:define-contact-set "Ntop_0_1" 4 (color:rgb 0 1 0 )"##" )
(sdegeo:define-contact-set "Ptop_1_0" 4 (color:rgb 1 0 0 )"##" )
(sdegeo:define-contact-set "Ntop_1_0" 4 (color:rgb 0 1 0 )"##" )
(sdegeo:define-contact-set "Ptop_1_1" 4 (color:rgb 1 0 0 )"##" )
(sdegeo:define-contact-set "Ntop_1_1" 4 (color:rgb 0 1 0 )"##" )
(sdegeo:define-contact-set "Ptop" 4 (color:rgb 1 0 0 )"##" )
(sdegeo:define-contact-set "Pbot" 4 (color:rgb 1 0 0 )"##" )

;; Work Planes:
(sde:workplanes-init-scm-binding)

;; Defined ACIS Refinements:
(sde:refinement-init-scm-binding)

;; Reference/Evaluation Windows:
(sdedr:define-refeval-window "WinEpi" "Cuboid" (position -1 -1 -1) (position 101 7 101))
(sdedr:define-refeval-window "WinPbot" "Polygon" (list (position 0 100 0) (position 0 100 100) (position 100 100 100) (position 100 100 0)))
(sdedr:define-refeval-window "WinNtop_0_0" "Polygon" (list (position 20 0 20) (position 20 0 30) (position 30 0 30) (position 30 0 20)))
(sdedr:define-refeval-window "WinPtop1_0_0" "Polygon" (list (position 0 0 0) (position 0 0 50) (position 15 0 50) (position 15 0 0)))
(sdedr:define-refeval-window "WinPtop2_0_0" "Polygon" (list (position 35 0 0) (position 35 0 50) (position 50 0 50) (position 50 0 0)))
(sdedr:define-refeval-window "WinPtop3_0_0" "Polygon" (list (position 15 0 0) (position 15 0 15) (position 35 0 15) (position 35 0 0)))
(sdedr:define-refeval-window "WinPtop4_0_0" "Polygon" (list (position 15 0 35) (position 15 0 50) (position 35 0 50) (position 35 0 35)))
(sdedr:define-refeval-window "WinDPtop1_0_0" "Polygon" (list (position 0 0 0) (position 0 0 50) (position 15 0 50) (position 15 0 0)))
(sdedr:define-refeval-window "WinDPtop2_0_0" "Polygon" (list (position 35 0 0) (position 35 0 50) (position 50 0 50) (position 50 0 0)))
(sdedr:define-refeval-window "WinDPtop3_0_0" "Polygon" (list (position 15 0 0) (position 15 0 15) (position 35 0 15) (position 35 0 0)))
(sdedr:define-refeval-window "WinDPtop4_0_0" "Polygon" (list (position 15 0 35) (position 15 0 50) (position 35 0 50) (position 35 0 35)))
(sdedr:define-refeval-window "WinNtop_0_1" "Polygon" (list (position 20 0 70) (position 20 0 80) (position 30 0 80) (position 30 0 70)))
(sdedr:define-refeval-window "WinPtop1_0_1" "Polygon" (list (position 0 0 50) (position 0 0 100) (position 15 0 100) (position 15 0 50)))
(sdedr:define-refeval-window "WinPtop2_0_1" "Polygon" (list (position 35 0 50) (position 35 0 100) (position 50 0 100) (position 50 0 50)))
(sdedr:define-refeval-window "WinPtop3_0_1" "Polygon" (list (position 15 0 50) (position 15 0 65) (position 35 0 65) (position 35 0 50)))
(sdedr:define-refeval-window "WinPtop4_0_1" "Polygon" (list (position 15 0 85) (position 15 0 100) (position 35 0 100) (position 35 0 85)))
(sdedr:define-refeval-window "WinDPtop1_0_1" "Polygon" (list (position 0 0 50) (position 0 0 100) (position 15 0 100) (position 15 0 50)))
(sdedr:define-refeval-window "WinDPtop2_0_1" "Polygon" (list (position 35 0 50) (position 35 0 100) (position 50 0 100) (position 50 0 50)))
(sdedr:define-refeval-window "WinDPtop3_0_1" "Polygon" (list (position 15 0 50) (position 15 0 65) (position 35 0 65) (position 35 0 50)))
(sdedr:define-refeval-window "WinDPtop4_0_1" "Polygon" (list (position 15 0 85) (position 15 0 100) (position 35 0 100) (position 35 0 85)))
(sdedr:define-refeval-window "WinNtop_1_0" "Polygon" (list (position 70 0 20) (position 70 0 30) (position 80 0 30) (position 80 0 20)))
(sdedr:define-refeval-window "WinPtop1_1_0" "Polygon" (list (position 50 0 0) (position 50 0 50) (position 65 0 50) (position 65 0 0)))
(sdedr:define-refeval-window "WinPtop2_1_0" "Polygon" (list (position 85 0 0) (position 85 0 50) (position 100 0 50) (position 100 0 0)))
(sdedr:define-refeval-window "WinPtop3_1_0" "Polygon" (list (position 65 0 0) (position 65 0 15) (position 85 0 15) (position 85 0 0)))
(sdedr:define-refeval-window "WinPtop4_1_0" "Polygon" (list (position 65 0 35) (position 65 0 50) (position 85 0 50) (position 85 0 35)))
(sdedr:define-refeval-window "WinDPtop1_1_0" "Polygon" (list (position 50 0 0) (position 50 0 50) (position 65 0 50) (position 65 0 0)))
(sdedr:define-refeval-window "WinDPtop2_1_0" "Polygon" (list (position 85 0 0) (position 85 0 50) (position 100 0 50) (position 100 0 0)))
(sdedr:define-refeval-window "WinDPtop3_1_0" "Polygon" (list (position 65 0 0) (position 65 0 15) (position 85 0 15) (position 85 0 0)))
(sdedr:define-refeval-window "WinDPtop4_1_0" "Polygon" (list (position 65 0 35) (position 65 0 50) (position 85 0 50) (position 85 0 35)))
(sdedr:define-refeval-window "WinNtop_1_1" "Polygon" (list (position 70 0 70) (position 70 0 80) (position 80 0 80) (position 80 0 70)))
(sdedr:define-refeval-window "WinPtop1_1_1" "Polygon" (list (position 50 0 50) (position 50 0 100) (position 65 0 100) (position 65 0 50)))
(sdedr:define-refeval-window "WinPtop2_1_1" "Polygon" (list (position 85 0 50) (position 85 0 100) (position 100 0 100) (position 100 0 50)))
(sdedr:define-refeval-window "WinPtop3_1_1" "Polygon" (list (position 65 0 50) (position 65 0 65) (position 85 0 65) (position 85 0 50)))
(sdedr:define-refeval-window "WinPtop4_1_1" "Polygon" (list (position 65 0 85) (position 65 0 100) (position 85 0 100) (position 85 0 85)))
(sdedr:define-refeval-window "WinDPtop1_1_1" "Polygon" (list (position 50 0 50) (position 50 0 100) (position 65 0 100) (position 65 0 50)))
(sdedr:define-refeval-window "WinDPtop2_1_1" "Polygon" (list (position 85 0 50) (position 85 0 100) (position 100 0 100) (position 100 0 50)))
(sdedr:define-refeval-window "WinDPtop3_1_1" "Polygon" (list (position 65 0 50) (position 65 0 65) (position 85 0 65) (position 85 0 50)))
(sdedr:define-refeval-window "WinDPtop4_1_1" "Polygon" (list (position 65 0 85) (position 65 0 100) (position 85 0 100) (position 85 0 85)))
(sdedr:define-refeval-window "RefWinGlobal" "Cuboid" (position -1 -1 -1) (position 101 101 101))
(sdedr:define-refeval-window "RefWinSurf" "Cuboid" (position 0 0 0) (position 100 10 100))
(sdedr:define-refeval-window "RefWinBot" "Cuboid" (position 0 98 0) (position 100 100 100))
(sdedr:define-refeval-window "RefWinPart" "Cuboid" (position -2 0 -2) (position 2 100 2))
