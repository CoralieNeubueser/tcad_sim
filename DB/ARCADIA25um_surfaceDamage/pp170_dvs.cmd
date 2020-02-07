;;--------------------------------------------------------------------
;;  MAPS simulation in LF process - structure definition
;;  Created by L. Pancheri
;;  Creation date: 17/2/2015
;;  Last modified: 10/5/2019
;;--------------------------------------------------------------------


;; Macros
;;--------------------------------------------------------------------

(define TSi 50)	; Silicon thickness
(define WSi 25)	; Silicon Width
(define nwW 2.5)	; nwell Width
(define pwW (- (/ (- WSi nwW) 2) 4.25))	; pwell Width
(define dpwW 8)	; deep pwell Width
(define nwSTART (- (/ WSi 2) (/ nwW 2) ) )	; nwell start x
(define nwSTOP (+ (/ WSi 2) (/ nwW 2) ) )	; nwell stop x
(define TEpi 7)	; Silicon Width
(define oxideW WSi ); oxide width
(define oxideT -0.2) ; oxide depth

;; Substrate definition
;;--------------------------------------------------------------------

(sdegeo:create-rectangle (position 0 0 0 )  (position WSi TSi 0 ) "Silicon" "substrate" )
(sdegeo:create-rectangle (position 0 0 0 )  (position oxideW oxideT 0 ) "SiO2" "oxide" )
(sdegeo:insert-vertex (position  3 0 0))
(sdegeo:insert-vertex (position  (- (/ WSi 2) 0.5) 0 0))
(sdegeo:insert-vertex (position  (+ (/ WSi 2) 0.5) 0 0))
(sdegeo:insert-vertex (position  (- WSi 3) 0 0))

;; Contacts definition
;;--------------------------------------------------------------------

(sdegeo:define-contact-set "Ptop" 4  (color:rgb 1 0 0 ) "##" )
(sdegeo:define-contact-set "Ntop" 4  (color:rgb 0 1 0 ) "##" )
(sdegeo:define-contact-set "Pbot" 4  (color:rgb 0 1 0 ) "##" )

(sdegeo:set-current-contact-set "Ntop")
(sdegeo:set-contact-edges (list (car (find-edge-id (position (/ WSi 2) 0 0)))) "Ntop")
(sdegeo:set-current-contact-set "Ptop")
(sdegeo:set-contact-edges (list (car (find-edge-id (position 0.5 0 0)))) "Ptop")
(sdegeo:set-contact-edges (list (car (find-edge-id (position (- WSi 0.5) 0 0)))) "Ptop")
(sdegeo:set-current-contact-set "Pbot")
(sdegeo:set-contact-edges (list (car (find-edge-id (position 0.5 TSi 0)))) "Pbot")


;; Doping profiles
;;--------------------------------------------------------------------

(sdedr:define-refeval-window "WinEpi"   "Rectangle"  (position -1 -1 0) (position (+ WSi 1) TEpi 0)) 	      ;epi doping
(sdedr:define-refeval-window "WinNtop"   "Line"  (position nwSTART 0 0) (position nwSTOP 0 0)) 	      ;line to start Ntop doping
(sdedr:define-refeval-window "WinPtop1" "Line"  (position 0 0 0) (position pwW 0 0)) 	        ;line to start Ptop region 1 doping
(sdedr:define-refeval-window "WinPtop2" "Line"  (position (- WSi pwW) 0 0) (position WSi 0 0)) 	    ;line to start Ptop region 2 doping
(sdedr:define-refeval-window "WinDPtop1" "Line"  (position 0 0 0) (position dpwW 0 0)) 	        ;line to start Ptop region 1 doping
(sdedr:define-refeval-window "WinDPtop2" "Line"  (position (- WSi dpwW) 0 0) (position WSi 0 0)) 	    ;line to start Ptop region 2 doping
(sdedr:define-refeval-window "WinPbot"   "Line"  (position 0 TSi 0) (position WSi TSi 0)) 	  ;line to start Pbot doping
;;(sdedr:define-refeval-window "WinDDNwell"   "Line"  (position 0 0 0) (position WSi 0 0)) 	  ;line to start DDNwelldoping

(sdedr:define-constant-profile "ProfSub" "PhosphorusActiveConcentration" 2.5e12)   ;bulk doping, costant
(sdedr:define-constant-profile "ProfEpi" "PhosphorusActiveConcentration" 1e14)   ;epitaxial doping, costant
(sdedr:define-1d-external-profile "ProfPwell" "./pwell.txt" "Scale" 1 "Range" 0 1.5 "Gauss"  "Factor" 0) 
(sdedr:define-1d-external-profile "ProfNwell" "./nwell.txt" "Scale" 1 "Range" 0 1.8 "Gauss"  "Factor" 0) 
(sdedr:define-1d-external-profile "ProfDPwell" "./dpwell.txt" "Scale" 1 "Range" 0 10 "Gauss"  "Factor" 0) 
;;(sdedr:define-1d-external-profile "ProfDDNwell" "./ddnwellld.txt" "Scale" 1 "Range" 0 10 "Gauss"  "Factor" 0) 
(sdedr:define-gaussian-profile "ProfPbot" "BoronActiveConcentration" "PeakPos" 0  "PeakVal" 1e+19 "ValueAtDepth" 2.5e+12 "Depth" 0.1 "Gauss"  "Factor" 0.8)  

(sdedr:define-constant-profile-region "PlacSub" "ProfSub" "substrate")
(sdedr:define-constant-profile-placement "PlacEpi" "ProfEpi" "WinEpi" 0.3 "Replace")
(sdedr:define-analytical-profile-placement "PlacPwell1" "ProfPwell" "WinPtop1" "Both" "NoReplace" "Eval")
(sdedr:define-analytical-profile-placement "PlacPwell2" "ProfPwell" "WinPtop2" "Both" "NoReplace" "Eval")
(sdedr:define-analytical-profile-placement "PlacDPwell1" "ProfDPwell" "WinDPtop1" "Both" "NoReplace" "Eval")
(sdedr:define-analytical-profile-placement "PlacDPwell2" "ProfDPwell" "WinDPtop2" "Both" "NoReplace" "Eval")
(sdedr:define-analytical-profile-placement "PlacNwell" "ProfNwell" "WinNtop" "Both" "NoReplace" "Eval")
;;(sdedr:define-analytical-profile-placement "PlacDDNwell" "ProfDDNwell" "WinDDNwell" "Both" "NoReplace" "Eval")
(sdedr:define-analytical-profile-placement "PlacPbot" "ProfPbot" "WinPbot" "Both" "NoReplace" "Eval")


;; Refinements
;;--------------------------------------------------------------------

(sdedr:define-refeval-window "RefWinGlobal" "Rectangle"  (position -1 -1 0) (position (+ WSi 1) (+ TSi 1) 0)) 	;global mesh
;global mesh options
(sdedr:define-refinement-size "RefDefGlobal" 5 2 0 0.2 0.2 0 ) ;; maxDeltaX, maxDeltaY, maxDeltaZ, min...
(sdedr:define-refinement-placement "RefPlacGlobal" "RefDefGlobal" "RefWinGlobal" )
(sdedr:define-refinement-function "RefDefGlobal" "DopingConcentration" "MaxTransDiff" 1)

; surface mesh
(sdedr:define-refeval-window "RefWinSurf" "Rectangle"  (position 0 oxideT 0) (position WSi 10 0)) 	
(sdedr:define-refinement-size "RefDefSurf" 0.2 0.2 0 0.025 0.025 0 )
(sdedr:define-refinement-placement "RefPlacSurf" "RefDefSurf" "RefWinSurf" )
(sdedr:define-refinement-function "RefDefSurf" "DopingConcentration" "MaxTransDiff" 1)

; bottom mesh
(sdedr:define-refeval-window "RefWinBot" "Rectangle"  (position 0 (- TSi 2) 0) (position WSi TSi 0)) 	
(sdedr:define-refinement-size "RefDefBot" 10 0.5 0 1 0.02 0 )
(sdedr:define-refinement-placement "RefPlacBot" "RefDefBot" "RefWinBot" )
(sdedr:define-refinement-function "RefDefBot" "DopingConcentration" "MaxTransDiff" 1)


;saving and meshing 
(sde:save-model "p170")
(sde:build-mesh "snmesh" "-a -c boxmethod" "n170")





