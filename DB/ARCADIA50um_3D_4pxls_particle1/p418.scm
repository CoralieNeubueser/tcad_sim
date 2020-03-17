
;; Defined Parameters:

;; Contact Sets:
(sdegeo:define-contact-set "Ptop" 4 (color:rgb 1 0 0 )"##" )
(sdegeo:define-contact-set "Ntop" 4 (color:rgb 0 1 0 )"##" )
(sdegeo:define-contact-set "Pbot" 4 (color:rgb 0 1 0 )"##" )

;; Work Planes:
(sde:workplanes-init-scm-binding)

;; Defined ACIS Refinements:
(sde:refinement-init-scm-binding)

;; Reference/Evaluation Windows:
(sdedr:define-refeval-window "WinEpi" "Cuboid" (position -1 -1 -1) (position 51 7 51))
(sdedr:define-refeval-window "WinNtop" "Polygon" (list (position 20 0 20) (position 20 0 30) (position 30 0 30) (position 30 0 20)))
(sdedr:define-refeval-window "WinPtop1" "Polygon" (list (position 0 0 0) (position 0 0 50) (position 15 0 50) (position 15 0 0)))
(sdedr:define-refeval-window "WinPtop2" "Polygon" (list (position 35 0 0) (position 35 0 50) (position 50 0 50) (position 50 0 0)))
(sdedr:define-refeval-window "WinPtop3" "Polygon" (list (position 15 0 0) (position 15 0 15) (position 35 0 15) (position 35 0 0)))
(sdedr:define-refeval-window "WinPtop4" "Polygon" (list (position 15 0 35) (position 15 0 50) (position 35 0 50) (position 35 0 35)))
(sdedr:define-refeval-window "WinDPtop1" "Polygon" (list (position 0 0 0) (position 0 0 50) (position 15 0 50) (position 15 0 0)))
(sdedr:define-refeval-window "WinDPtop2" "Polygon" (list (position 35 0 0) (position 35 0 50) (position 50 0 50) (position 50 0 0)))
(sdedr:define-refeval-window "WinDPtop3" "Polygon" (list (position 15 0 0) (position 15 0 15) (position 35 0 15) (position 35 0 0)))
(sdedr:define-refeval-window "WinDPtop4" "Polygon" (list (position 15 0 35) (position 15 0 50) (position 35 0 50) (position 35 0 35)))
(sdedr:define-refeval-window "WinPbot" "Polygon" (list (position 0 50 0) (position 0 50 50) (position 50 50 50) (position 50 50 0)))
(sdedr:define-refeval-window "RefWinGlobal" "Cuboid" (position -1 -1 -1) (position 51 51 51))
(sdedr:define-refeval-window "RefWinSurf" "Cuboid" (position 0 0 0) (position 50 10 50))
(sdedr:define-refeval-window "RefWinBot" "Cuboid" (position 0 48 0) (position 50 50 50))
(sdedr:define-refeval-window "RefWinPart" "Cuboid" (position 23 0 10.5) (position 27 50 14.5))
