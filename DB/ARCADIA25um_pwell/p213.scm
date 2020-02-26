
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
(sdedr:define-refeval-window "WinEpi" "Rectangle" (position -1 -1 0) (position 26 7 0))
(sdedr:define-refeval-window "WinNtop" "Line" (position 11.25 0 0) (position 13.75 0 0))
(sdedr:define-refeval-window "WinPtop1" "Line" (position 0 0 0) (position 9.25 0 0))
(sdedr:define-refeval-window "WinPtop2" "Line" (position 15.75 0 0) (position 25 0 0))
(sdedr:define-refeval-window "WinDPtop1" "Line" (position 0 0 0) (position 9 0 0))
(sdedr:define-refeval-window "WinDPtop2" "Line" (position 16 0 0) (position 25 0 0))
(sdedr:define-refeval-window "WinPbot" "Line" (position 0 50 0) (position 25 50 0))
(sdedr:define-refeval-window "RefWinGlobal" "Rectangle" (position -1 -1 0) (position 26 51 0))
(sdedr:define-refeval-window "RefWinSurf" "Rectangle" (position 0 0 0) (position 25 10 0))
(sdedr:define-refeval-window "RefWinBot" "Rectangle" (position 0 48 0) (position 25 50 0))
