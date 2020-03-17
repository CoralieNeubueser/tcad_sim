;;--------------------------------------------------------------------
;;  MAPS simulation in LF process - structure definition
;;  Created by L. Pancheri
;;  Creation date: 31/10/2019
;;  Last modified: 31/10/2019
;;--------------------------------------------------------------------


;; Macros
;;--------------------------------------------------------------------

(define TSi 50)	; Silicon thickness
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
(define TEpi 7)	; epi thickness



;; Substrate definition
;;--------------------------------------------------------------------

(sdegeo:create-cuboid (position 0 0 0 )  (position (* WSi 2) TSi (* DSi 2) ) "Silicon" "substrate" )
(sdegeo:imprint-rectangular-wire (position  0 0 0) (position  (* 2 WSi) 0 (* 2 DSi)) )

(do ( (l 0 (+ l 1) ) )
    ( (= l 2) )
    (begin
	(do ( (k 0 (+ k 1) ) )
    	( (= k 2) )
	(begin
		(display "The value of l is ") (display l) (newline)
		(display "The value of k is ") (display k) (newline)
                (display "The value of l is ") (display (* l WSi)) (newline)
                (display "The value of k is ") (display (* k DSi)) (newline)

	    	(sdegeo:imprint-rectangular-wire (position  (+ (+ nwSTART (* l WSi)) 0.5) 0 (+ (+ nwSTART (* k DSi)) 0.5) ) (position  (- (+ nwSTOP (* l WSi)) 0.5) 0 (- (+ nwSTOP (* k DSi)) 0.5) ) )
	    	(sdegeo:imprint-rectangular-wire (position  (+ (- pwW 3) (* l WSi)) 0 (+ (- pwD 3) (* k DSi))) (position  (+ (+ (- WSi pwW ) 3) (* l WSi)) 0 (+ (+ (- DSi pwD) 3) (* k DSi)))) 
		
		;;(sdegeo:imprint-rectangular-wire (position  (+ 5 (* l WSi)) 0 (+ 5 (* k DSi)) ) (position  (+ 10 (* l WSi)) 0 (+ (- DSi 5) (* k DSi)) ) )
	    	;;(sdegeo:imprint-rectangular-wire (position  (+ 10 (* l WSi)) 0 (+ 10 (* k DSi)) ) (position  (+ (- WSi 10) (* l WSi)) 0 (+ 5 (* k DSi)) ) )
	    	;;(sdegeo:imprint-rectangular-wire (position  (+ (- WSi 10) (* l WSi)) 0 (+ 5 (* k DSi))) (position  (+ (- WSi 5) (* l WSi)) 0 (+ (- DSi 5) (* k DSi)) ) )
	    	;;(sdegeo:imprint-rectangular-wire (position  (+ 10 (* l WSi)) 0 (+ (- DSi 10) (* k DSi))) (position  (+ (- WSi 10) (* l WSi)) 0 (+ (- DSi 5) (* k DSi)) ) )
))))

;; Contacts definition
;;--------------------------------------------------------------------
(define NAMES (list "0_0" "0_1" "1_0" "1_1"))
(define LS (list 0 0 1 1))
(define KS (list 0 1 0 1))
(for-each
	(lambda (NAME L K)
       		(begin
			(define NTOP (string-append "Ntop_" NAME))
       			(define PTOP (string-append "Ptop_" NAME))

       			(sdegeo:define-contact-set PTOP 4  (color:rgb 1 0 0 ) "##" )
       			(sdegeo:define-contact-set NTOP 4  (color:rgb 0 1 0 ) "##" )
       			
			(sdegeo:set-current-contact-set NTOP)
       			(sdegeo:define-3d-contact (find-face-id (position (+ (/ WSi 2) (* L WSi)) 0 (+ (/ DSi 2) (* K DSi)) )) NTOP)
       			
			;;(sdegeo:set-current-contact-set PTOP)
       			;;(sdegeo:define-3d-contact (find-face-id (position (+ 10 (* L WSi)) 0 (+ 7.5 (* K DSi)))) PTOP)
       			;;(sdegeo:define-3d-contact (find-face-id (position (+ 7.5 (* L WSi)) 0 (+ 7.5 (* K DSi)))) PTOP)
       			;;(sdegeo:define-3d-contact (find-face-id (position (- (+ WSi (* L WSi)) 7.5) 0 (+ 7.5 (* K DSi)))) PTOP)
       			;;(sdegeo:define-3d-contact (find-face-id (position (+ 10 (* L WSi)) 0 (- (+ DSi (* K DSi)) 7.5))) PTOP)
       			)
	) NAMES LS KS
)
(sdegeo:set-current-contact-set "Ptop")
(sdegeo:set-contact-faces (list (car (find-face-id (position (+ 10 WSi) 0 (+ 7.5 DSi))))) "Ptop")

(sdegeo:set-current-contact-set "Pbot")
(sdegeo:set-contact-faces (list (car (find-face-id (position 0.5 TSi 0.5)))) "Pbot")

;; Doping profiles
;;--------------------------------------------------------------------



(sdedr:define-refeval-window "WinEpi"   "Cuboid"  (position -1 -1 -1) (position (+ (* 2 WSi) 1) TEpi (+ (* 2 DSi) 1))) 	      ;epi doping
(sdedr:define-refeval-window "WinPbot"   "Rectangle"  (position 0 TSi 0) (position (* 2 WSi) TSi (* 2 DSi) ) )                 ;line to start Pbot doping

(sdedr:define-constant-profile "ProfSub" "PhosphorusActiveConcentration" 2.5e12)   ;bulk doping, costant
(sdedr:define-constant-profile "ProfEpi" "PhosphorusActiveConcentration" 1e14)   ;epitaxial doping, costant
(sdedr:define-gaussian-profile "ProfPbot" "BoronActiveConcentration" "PeakPos" 0  "PeakVal" 1e+19 "ValueAtDepth" 2.5e+12 "Depth" 0.1 "Gauss"  "Factor" 0.8)
(sdedr:define-1d-external-profile "ProfPwell" "./pwell.txt" "Scale" 1 "Range" 0 1.5 "Gauss"  "Factor" 0)
(sdedr:define-1d-external-profile "ProfNwell" "./nwell.txt" "Scale" 1 "Range" 0 1.8 "Gauss"  "Factor" 0)
(sdedr:define-1d-external-profile "ProfDPwell" "./dpwell.txt" "Scale" 1 "Range" 0 10 "Gauss"  "Factor" 0)

(sdedr:define-constant-profile-region "PlacSub" "ProfSub" "substrate")
(sdedr:define-constant-profile-placement "PlacEpi" "ProfEpi" "WinEpi" 0.3 "Replace")
(sdedr:define-analytical-profile-placement "PlacPbot" "ProfPbot" "WinPbot" "Both" "NoReplace" "Eval")
 
(define NAMES (list "0_0" "0_1" "1_0" "1_1"))
(define LS (list 0 0 1 1))
(define KS (list 0 1 0 1))
(for-each
        (lambda (NAME L K)
                (begin
	
	                (display "The value of L is ") (display L) (newline)
        		(display "The value of K is ") (display K) (newline)
			(define L1 (+ L 1))
                        (define K1 (+ K 1))

			(define WINNTOP (string-append "WinNtop_" NAME ))
	                (define WINPTOP1 (string-append "WinPtop1_" NAME))
	                (define WINPTOP2 (string-append "WinPtop2_" NAME))
	                (define WINPTOP3 (string-append "WinPtop3_" NAME))
	                (define WINPTOP4 (string-append "WinPtop4_" NAME))
			(define WINDPTOP1 (string-append "WinDPtop1_" NAME))
	                (define WINDPTOP2 (string-append "WinDPtop2_" NAME))
	                (define WINDPTOP3 (string-append "WinDPtop3_" NAME))
	                (define WINDPTOP4 (string-append "WinDPtop4_" NAME))
	
	                (define PLACNTOP (string-append "PlacNtop_" NAME ))
	                (define PLACPTOP1 (string-append "PlacPtop1_" NAME))
	                (define PLACPTOP2 (string-append "PlacPtop2_" NAME))
	                (define PLACPTOP3 (string-append "PlacPtop3_" NAME))
	                (define PLACPTOP4 (string-append "PlacPtop4_" NAME))
	                (define PLACDPTOP1 (string-append "PlacDPtop1_" NAME))
	                (define PLACDPTOP2 (string-append "PlacDPtop2_" NAME))
	                (define PLACDPTOP3 (string-append "PlacDPtop3_" NAME))
	                (define PLACDPTOP4 (string-append "PlacDPtop4_" NAME))
	
			(sdedr:define-refeval-window WINNTOP   "Rectangle"  (position (+ nwSTART (* L WSi)) 0 (+ nwSTART (* K DSi))) (position (+ nwSTOP (* L WSi)) 0 (+ nwSTOP (* K DSi))) )  	      ;line to start Ntop doping
			(sdedr:define-refeval-window WINPTOP1  "Rectangle"  (position (* L WSi) 0 (* K DSi)) (position (+ pwW (* L WSi)) 0 (+ DSi (* K DSi))) )	             	      	      ;line to start Ptop region 1 doping
			(sdedr:define-refeval-window WINPTOP2  "Rectangle"  (position (- (* L1 WSi) pwW) 0 (* K DSi)) (position (* L1 WSi) 0 (* K1 DSi)) )		   		      ;line to start Ptop region 2 doping
			(sdedr:define-refeval-window WINPTOP3  "Rectangle"  (position (+ pwW (* L WSi)) 0 (* K DSi)) (position (- (* L1 WSi) pwW) 0 (+ pwD (* K DSi))) )    		      ;line to start Ptop region 3 doping
			(sdedr:define-refeval-window WINPTOP4  "Rectangle"  (position (+ pwW (* L WSi)) 0 (- (* K1 DSi) pwD)) (position (- (* L1 WSi) pwW) 0 (+ DSi (* K DSi))) )	      ;line to start Ptop region 4 doping
			(sdedr:define-refeval-window WINDPTOP1 "Rectangle"  (position (* L WSi) 0 (* K DSi)) (position (+ dpwW (* L WSi)) 0 (+ DSi (* K DSi))))	     	              		      ;line to start Ptop region 1 doping
			(sdedr:define-refeval-window WINDPTOP2 "Rectangle"  (position (- (* L1 WSi) dpwW) 0 (* K DSi)) (position (+ WSi (* L WSi)) 0 (+ DSi (* K DSi))))			      ;line to start Ptop region 2 doping
			(sdedr:define-refeval-window WINDPTOP3 "Rectangle"  (position (+ dpwW (* L WSi)) 0 (* K DSi)) (position  (- (* L1 WSi) dpwW) 0 (+ dpwD (* K DSi))))   		      ;line to start Ptop region 3 doping
			(sdedr:define-refeval-window WINDPTOP4 "Rectangle"  (position (+ dpwW (* L WSi)) 0 (- (* K1 DSi) dpwD)) (position (- (* L1 WSi) dpwW) 0 (+ DSi (* K DSi))))     ;line to start Ptop region 4 doping
		
			(sdedr:define-analytical-profile-placement PLACPTOP1 "ProfPwell" WINPTOP1 "Both" "NoReplace" "Eval")
			(sdedr:define-analytical-profile-placement PLACPTOP2 "ProfPwell" WINPTOP2 "Both" "NoReplace" "Eval")
			(sdedr:define-analytical-profile-placement PLACPTOP3 "ProfPwell" WINPTOP3 "Both" "NoReplace" "Eval")
			(sdedr:define-analytical-profile-placement PLACPTOP4 "ProfPwell" WINPTOP4 "Both" "NoReplace" "Eval")
			(sdedr:define-analytical-profile-placement PLACDPTOP1 "ProfDPwell" WINDPTOP1 "Both" "NoReplace" "Eval")
			(sdedr:define-analytical-profile-placement PLACDPTOP2 "ProfDPwell" WINDPTOP2 "Both" "NoReplace" "Eval")
			(sdedr:define-analytical-profile-placement PLACDPTOP3 "ProfDPwell" WINDPTOP3 "Both" "NoReplace" "Eval")
			(sdedr:define-analytical-profile-placement PLACDPTOP4 "ProfDPwell" WINDPTOP4 "Both" "NoReplace" "Eval")
			(sdedr:define-analytical-profile-placement PLACNTOP "ProfNwell" WINNTOP "Both" "NoReplace" "Eval")
		)
        ) NAMES LS KS
)


;; Refinements
;;--------------------------------------------------------------------

(sdedr:define-refeval-window "RefWinGlobal" "Cuboid"  (position -1 -1 -1) (position (+ (* 2 WSi) 1) (+ TSi 1) (+ (* 2 DSi) 1))) 	;global mesh
;global mesh options
(sdedr:define-refinement-size "RefDefGlobal" 20 5 20 4 4 4 )
(sdedr:define-refinement-placement "RefPlacGlobal" "RefDefGlobal" "RefWinGlobal" )
(sdedr:define-refinement-function "RefDefGlobal" "DopingConcentration" "MaxTransDiff" 1)

; surface mesh
(sdedr:define-refeval-window "RefWinSurf" "Cuboid"  (position 0 0 0) (position (* 2 WSi) 10 (* 2 DSi))) 	
(sdedr:define-refinement-size "RefDefSurf" 2.5 2.5 2.5 0.5 0.5 0.5 )
(sdedr:define-refinement-placement "RefPlacSurf" "RefDefSurf" "RefWinSurf" )
(sdedr:define-refinement-function "RefDefSurf" "DopingConcentration" "MaxTransDiff" 1)

; bottom mesh
(sdedr:define-refeval-window "RefWinBot" "Cuboid"  (position 0 (- TSi 2) 0) (position (* 2 WSi) TSi (* 2 DSi))) 	
(sdedr:define-refinement-size "RefDefBot" 10 2 10 4 1 4 )
(sdedr:define-refinement-placement "RefPlacBot" "RefDefBot" "RefWinBot" )
(sdedr:define-refinement-function "RefDefBot" "DopingConcentration" "MaxTransDiff" 1)

; particle
(sdedr:define-refeval-window "RefWinPart" "Cuboid"  (position (- 0 2) 0 (- 0 2)) (position (+ 0 2) TSi (+ 0 2))) 	
(sdedr:define-refinement-size "RefDefPart" 0.4 5 0.4 0.15 0.25 0.15 )
(sdedr:define-refinement-placement "RefPlacPart" "RefDefPart" "RefWinPart" )


;saving and meshing 
(sde:save-model "p362")
(sde:build-mesh "snmesh" "-a -c boxmethod" "n362")







