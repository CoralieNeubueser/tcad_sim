
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
(sdedr:define-refeval-window "WinEpi" "Cuboid" (position -1 -1 -1) (position 26 7 26))
(sdedr:define-refeval-window "WinNtop" "Polygon" (list (position 11.25 0 11.25) (position 11.25 0 13.75) (position 13.75 0 13.75) (position 13.75 0 11.25)))
(sdedr:define-refeval-window "WinPtop1" "Polygon" (list (position 0 0 0) (position 0 0 25) (position 7 0 25) (position 7 0 0)))
(sdedr:define-refeval-window "WinPtop2" "Polygon" (list (position 18 0 0) (position 18 0 25) (position 25 0 25) (position 25 0 0)))
(sdedr:define-refeval-window "WinPtop3" "Polygon" (list (position 7 0 0) (position 7 0 7) (position 18 0 7) (position 18 0 0)))
(sdedr:define-refeval-window "WinPtop4" "Polygon" (list (position 7 0 18) (position 7 0 25) (position 18 0 25) (position 18 0 18)))
(sdedr:define-refeval-window "WinDPtop1" "Polygon" (list (position 0 0 0) (position 0 0 25) (position 8 0 25) (position 8 0 0)))
(sdedr:define-refeval-window "WinDPtop2" "Polygon" (list (position 17 0 0) (position 17 0 25) (position 25 0 25) (position 25 0 0)))
(sdedr:define-refeval-window "WinDPtop3" "Polygon" (list (position 8 0 0) (position 8 0 8) (position 17 0 8) (position 17 0 0)))
(sdedr:define-refeval-window "WinDPtop4" "Polygon" (list (position 8 0 17) (position 8 0 25) (position 17 0 25) (position 17 0 17)))
(sdedr:define-refeval-window "WinPbot" "Polygon" (list (position 0 100 0) (position 0 100 25) (position 25 100 25) (position 25 100 0)))
(sdedr:define-refeval-window "RefWinGlobal" "Cuboid" (position -1 -1 -1) (position 26 101 26))
(sdedr:define-refeval-window "RefWinSurf" "Cuboid" (position 0 0 0) (position 25 10 25))
(sdedr:define-refeval-window "RefWinBot" "Cuboid" (position 0 98 0) (position 25 100 25))
