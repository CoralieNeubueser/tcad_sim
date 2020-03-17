
;; Defined Parameters:

;; Contact Sets:
(sdegeo:define-contact-set "Ptop" 4 (color:rgb 1 0 0 )"##" )
(sdegeo:define-contact-set "Ntop" 4 (color:rgb 0 1 0 )"##" )
(sdegeo:define-contact-set "Pbot" 4 (color:rgb 0 1 0 )"##" )
(sdegeo:define-contact-set "Ngr" 4 (color:rgb 0 1 0 )"##" )

;; Work Planes:
(sde:workplanes-init-scm-binding)

;; Defined ACIS Refinements:
(sde:refinement-init-scm-binding)

;; Reference/Evaluation Windows:
(sdedr:define-refeval-window "WinEpi" "Rectangle" (position -101 -1 0) (position 26 8 0))
(sdedr:define-refeval-window "WinNtop" "Line" (position 11.25 0 0) (position 13.75 0 0))
(sdedr:define-refeval-window "WinNgr" "Line" (position -100 0 0) (position -15 0 0))
(sdedr:define-refeval-window "WinPtop1" "Line" (position -15 0 0) (position 7 0 0))
(sdedr:define-refeval-window "WinPtop2" "Line" (position 18 0 0) (position 25 0 0))
(sdedr:define-refeval-window "WinDPtop1" "Line" (position -15 0 0) (position 8 0 0))
(sdedr:define-refeval-window "WinDPtop2" "Line" (position 17 0 0) (position 25 0 0))
(sdedr:define-refeval-window "WinPbot" "Line" (position -100 100 0) (position 25 100 0))
(sdedr:define-refeval-window "RefWinGlobal" "Rectangle" (position -101 -1 0) (position 26 101 0))
(sdedr:define-refeval-window "RefWinSurf" "Rectangle" (position -100 0 0) (position 25 10 0))
(sdedr:define-refeval-window "RefWinBot" "Rectangle" (position -100 98 0) (position 25 100 0))
(sdedr:define-refeval-window "RefWinPart" "Rectangle" (position -22 0 0) (position -18 100 0))
