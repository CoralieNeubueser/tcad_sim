
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
(sdedr:define-refeval-window "WinEpi" "Rectangle" (position 0 0 0) (position 100 4.2 0))
(sdedr:define-refeval-window "WinNtop" "Line" (position 30 0 0) (position 70 0 0))
(sdedr:define-refeval-window "WinPtop1" "Line" (position 0 0 0) (position 25 0 0))
(sdedr:define-refeval-window "WinPtop2" "Line" (position 75 0 0) (position 100 0 0))
(sdedr:define-refeval-window "WinPbot" "Line" (position 0 300 0) (position 100 300 0))
(sdedr:define-refeval-window "RefWinGlobal" "Rectangle" (position -1 -1 0) (position 101 301 0))
(sdedr:define-refeval-window "RefWinSurf" "Rectangle" (position 0 0 0) (position 100 10 0))
(sdedr:define-refeval-window "RefWinBot" "Rectangle" (position 0 298 0) (position 100 300 0))
