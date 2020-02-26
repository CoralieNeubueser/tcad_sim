;;--------------------------------------------------------------------
;;  MAPS simulation in LF process - structure definition
;;  Created by L. Pancheri
;;  Creation date: 31/10/2019
;;  Last modified: 31/10/2019
;;--------------------------------------------------------------------


;; Macros
;;--------------------------------------------------------------------

(define TSi @tsi@)	; Silicon thickness
(define WSi 50)	; Silicon Width
(define DSi 50) ;Silicon Depth
(define pwW 15)	; pwell Width
(define pwD 15)	; pwell Depth
(define dpwW 15) ; deep pwell Width
(define dpwD 15) ; deep pwell Depth
(define nwW 10)	; nwell Width
(define nwD 10)	; nwell Depth
(define nwSTART (- (/ WSi 2) (/ nwW 2) ) )	; nwell start x
(define nwSTOP (+ (/ WSi 2) (/ nwW 2) ) )	; nwell stop x
(define TEpi @tepi@)	; epi thickness



;; Substrate definition
;;--------------------------------------------------------------------

(sdegeo:create-cuboid (position 0 0 0 )  (position WSi TSi DSi ) "Silicon" "substrate" )
(sdegeo:imprint-rectangular-wire (position  (+ nwSTART 0.5) 0 (+ nwSTART 0.5)) (position  (- nwSTOP 0.5) 0 (- nwSTOP 0.5)))
(sdegeo:imprint-rectangular-wire (position  0 0 0) (position  5 0 DSi))
(sdegeo:imprint-rectangular-wire (position  5 0 0) (position  WSi 0 5))
(sdegeo:imprint-rectangular-wire (position  (- WSi 5) 0 5) (position  WSi 0 DSi))
(sdegeo:imprint-rectangular-wire (position  (- WSi 5) 0 (- DSi 5)) (position  5 0 DSi))
;;(sdegeo:insert-vertex (position  5 0 5))
;;(sdegeo:insert-vertex (position  5 0 (- DSi 5)))
;;(sdegeo:insert-vertex (position  (- WSi 5) 0 5))
;;(sdegeo:insert-vertex (position  (- WSi 5) 0 (- DSi 5)))
;;(sdegeo:insert-vertex (position  (+ nwSTART 0.5) 0 (+ nwSTART 0.5)))
;;(sdegeo:insert-vertex (position  (+ nwSTART 0.5) 0 (- nwSTOP 0.5)))
;;(sdegeo:insert-vertex (position  (- nwSTOP 0.5) 0 (+ nwSTART 0.5)))
;;(sdegeo:insert-vertex (position  (- nwSTOP 0.5) 0 (- nwSTOP 0.5)))
;;(sdegeo:insert-vertex (position  (- WSi 5) 0 0))
;;(sdegeo:insert-vertex (position  (- WSi 5) 0 DSi))

;; Contacts definition
;;--------------------------------------------------------------------

(sdegeo:define-contact-set "Ptop" 4  (color:rgb 1 0 0 ) "##" )
(sdegeo:define-contact-set "Ntop" 4  (color:rgb 0 1 0 ) "##" )
(sdegeo:define-contact-set "Pbot" 4  (color:rgb 0 1 0 ) "##" )
(sdegeo:set-current-contact-set "Ntop")
(sdegeo:define-3d-contact (find-face-id (position (/ WSi 2) 0 (/ DSi 2))) "Ntop")
;;(sdegeo:set-contact-faces (list (car (find-edge-id (position (/ WSi 2) 0 (/ DSi 2))))) "Ntop")
(sdegeo:set-current-contact-set "Ptop")
(sdegeo:define-3d-contact (find-face-id (position 2.5 0 2.5)) "Ptop")
(sdegeo:define-3d-contact (find-face-id (position 10 0 2.5)) "Ptop")
(sdegeo:define-3d-contact (find-face-id (position (- WSi 2.5) 0 10)) "Ptop")
(sdegeo:define-3d-contact (find-face-id (position 10 0 (- DSi 2.5))) "Ptop")
;;(sdegeo:set-contact-faces (list (car (find-face-id (position 0.5 0 0.5)))) "Ptop")
;;(sdegeo:set-contact-edges (list (car (find-edge-id (position (- WSi 0.5) 0 0)))) "Ptop")
(sdegeo:set-current-contact-set "Pbot")
(sdegeo:set-contact-faces (list (car (find-face-id (position 0.5 TSi 0.5)))) "Pbot")


;; Doping profiles
;;--------------------------------------------------------------------

(sdedr:define-refeval-window "WinEpi"   "Cuboid"  (position -1 -1 -1) (position (+ WSi 1) TEpi (+ DSi 1))) 	      ;epi doping
(sdedr:define-refeval-window "WinNtop"   "Rectangle"  (position nwSTART 0 nwSTART) (position nwSTOP 0 nwSTOP)) 	      ;line to start Ntop doping
(sdedr:define-refeval-window "WinPtop1" "Rectangle"  (position 0 0 0) (position pwW 0 DSi)) 	        ;line to start Ptop region 1 doping
(sdedr:define-refeval-window "WinPtop2" "Rectangle"  (position (- WSi pwW) 0 0) (position WSi 0 DSi)) 	    ;line to start Ptop region 2 doping
(sdedr:define-refeval-window "WinPtop3" "Rectangle"  (position pwW 0 0) (position (- WSi pwW) 0 pwD)) 	    ;line to start Ptop region 3 doping
(sdedr:define-refeval-window "WinPtop4" "Rectangle"  (position pwW 0 (- DSi pwD)) (position (- WSi pwW) 0 DSi)) 	    ;line to start Ptop region 4 doping
(sdedr:define-refeval-window "WinDPtop1" "Rectangle"  (position 0 0 0) (position dpwW 0 DSi)) 	        ;line to start Ptop region 1 doping
(sdedr:define-refeval-window "WinDPtop2" "Rectangle"  (position (- WSi dpwW) 0 0) (position WSi 0 DSi)) 	    ;line to start Ptop region 2 doping
(sdedr:define-refeval-window "WinDPtop3" "Rectangle"  (position dpwW 0 0) (position (- WSi dpwW) 0 dpwD)) 	    ;line to start Ptop region 3 doping
(sdedr:define-refeval-window "WinDPtop4" "Rectangle"  (position dpwW 0 (- DSi dpwD)) (position (- WSi dpwW) 0 DSi)) 	    ;line to start Ptop region 4 doping
(sdedr:define-refeval-window "WinPbot"   "Rectangle"  (position 0 TSi 0) (position WSi TSi DSi)) 	  ;line to start Pbot doping
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
(sdedr:define-analytical-profile-placement "PlacPwell3" "ProfPwell" "WinPtop3" "Both" "NoReplace" "Eval")
(sdedr:define-analytical-profile-placement "PlacPwell4" "ProfPwell" "WinPtop4" "Both" "NoReplace" "Eval")
(sdedr:define-analytical-profile-placement "PlacDPwell1" "ProfDPwell" "WinDPtop1" "Both" "NoReplace" "Eval")
(sdedr:define-analytical-profile-placement "PlacDPwell2" "ProfDPwell" "WinDPtop2" "Both" "NoReplace" "Eval")
(sdedr:define-analytical-profile-placement "PlacDPwell3" "ProfDPwell" "WinDPtop3" "Both" "NoReplace" "Eval")
(sdedr:define-analytical-profile-placement "PlacDPwell4" "ProfDPwell" "WinDPtop4" "Both" "NoReplace" "Eval")
(sdedr:define-analytical-profile-placement "PlacNwell" "ProfNwell" "WinNtop" "Both" "NoReplace" "Eval")
;;(sdedr:define-analytical-profile-placement "PlacDDNwell" "ProfDDNwell" "WinDDNwell" "Both" "NoReplace" "Eval")
(sdedr:define-analytical-profile-placement "PlacPbot" "ProfPbot" "WinPbot" "Both" "NoReplace" "Eval")


;; Refinements
;;--------------------------------------------------------------------

(sdedr:define-refeval-window "RefWinGlobal" "Cuboid"  (position -1 -1 -1) (position (+ WSi 1) (+ TSi 1) (+ DSi 1))) 	;global mesh
;global mesh options
(sdedr:define-refinement-size "RefDefGlobal" 20 5 20 4 4 4 )
(sdedr:define-refinement-placement "RefPlacGlobal" "RefDefGlobal" "RefWinGlobal" )
(sdedr:define-refinement-function "RefDefGlobal" "DopingConcentration" "MaxTransDiff" 1)

; surface mesh
(sdedr:define-refeval-window "RefWinSurf" "Cuboid"  (position 0 0 0) (position WSi 10 DSi)) 	
(sdedr:define-refinement-size "RefDefSurf" 2.5 2.5 2.5 0.5 0.5 0.5 )
(sdedr:define-refinement-placement "RefPlacSurf" "RefDefSurf" "RefWinSurf" )
(sdedr:define-refinement-function "RefDefSurf" "DopingConcentration" "MaxTransDiff" 1)

; bottom mesh
(sdedr:define-refeval-window "RefWinBot" "Cuboid"  (position 0 (- TSi 2) 0) (position WSi TSi DSi)) 	
(sdedr:define-refinement-size "RefDefBot" 10 2 10 4 1 4 )
(sdedr:define-refinement-placement "RefPlacBot" "RefDefBot" "RefWinBot" )
(sdedr:define-refinement-function "RefDefBot" "DopingConcentration" "MaxTransDiff" 1)

; particle
(sdedr:define-refeval-window "RefWinPart" "Cuboid"  (position (- @xpart@ 2) 0 (- @zpart@ 2)) (position (+ @xpart@ 2) TSi (+ @zpart@ 2))) 	
(sdedr:define-refinement-size "RefDefPart" 0.4 5 0.4 0.15 0.25 0.15 )
(sdedr:define-refinement-placement "RefPlacPart" "RefDefPart" "RefWinPart" )


;saving and meshing 
(sde:save-model "p@node@")
(sde:build-mesh "snmesh" "-a -c boxmethod" "n@node@")






