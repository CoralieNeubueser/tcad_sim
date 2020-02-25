
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
(sdedr:define-refeval-window "WinDPtop1" "Polygon" (list (position 0 0 0) (position 0 0 50) (position 16 0 50) (position 16 0 0)))
(sdedr:define-refeval-window "WinDPtop2" "Polygon" (list (position 34 0 0) (position 34 0 50) (position 50 0 50) (position 50 0 0)))
(sdedr:define-refeval-window "WinDPtop3" "Polygon" (list (position 16 0 0) (position 16 0 16) (position 34 0 16) (position 34 0 0)))
(sdedr:define-refeval-window "WinDPtop4" "Polygon" (list (position 16 0 34) (position 16 0 50) (position 34 0 50) (position 34 0 34)))
(sdedr:define-refeval-window "WinPbot" "Polygon" (list (position 0 100 0) (position 0 100 50) (position 50 100 50) (position 50 100 0)))
(sdedr:define-refeval-window "RefWinGlobal" "Cuboid" (position -1 -1 -1) (position 51 101 51))
(sdedr:define-refeval-window "RefWinSurf" "Cuboid" (position 0 0 0) (position 50 10 50))
(sdedr:define-refeval-window "RefWinBot" "Cuboid" (position 0 98 0) (position 50 100 50))
(sdedr:define-refeval-window "RefWinPart" "Cuboid" (position 23 0 23) (position 27 100 27))
