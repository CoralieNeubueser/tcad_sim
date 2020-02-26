
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
(sdedr:define-refeval-window "WinNtop" "Polygon" (list (position 11.25 0 0) (position 11.25 0 25) (position 13.75 0 25) (position 13.75 0 0)))
(sdedr:define-refeval-window "WinPtop1" "Polygon" (list (position 0 0 0) (position 0 0 25) (position 7 0 25) (position 7 0 0)))
(sdedr:define-refeval-window "WinPtop2" "Polygon" (list (position 18 0 0) (position 18 0 25) (position 25 0 25) (position 25 0 0)))
(sdedr:define-refeval-window "WinDPtop1" "Polygon" (list (position 0 0 0) (position 0 0 25) (position 7 0 25) (position 7 0 0)))
(sdedr:define-refeval-window "WinDPtop2" "Polygon" (list (position 18 0 0) (position 18 0 25) (position 25 0 25) (position 25 0 0)))
(sdedr:define-refeval-window "WinPbot" "Polygon" (list (position 0 50 0) (position 0 50 25) (position 25 50 25) (position 25 50 0)))
(sdedr:define-refeval-window "RefWinGlobal" "Cuboid" (position -1 -1 -1) (position 26 51 26))
(sdedr:define-refeval-window "RefWinSurf" "Cuboid" (position 0 0 0) (position 25 10 25))
(sdedr:define-refeval-window "RefWinBot" "Cuboid" (position 0 48 0) (position 25 50 25))
