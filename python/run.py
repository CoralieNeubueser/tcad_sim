import os, sys, argparse, re
from utils import *
from drawCCEmap import *
import pandas as pd
import numpy as np
from matplotlib import ticker
parser = argparse.ArgumentParser()

parser.add_argument('--project', type=str, default='ARCADIA25um_surfaceDamage', help='Define patht to project.')
parser.add_argument('--writeCSV', action='store_true', help='Convert tcl to csv, if not already done.')
parser.add_argument('-m', '--measure', action='append', type=str, default=[], help='Define which plots you want to draw.', choices=['cv','iv','iv_p','iv_b','cv_b','tran','tran_3','tran_4','tran_7','tran_8','charge'])
# define read-out electrode
parser.add_argument('-el', '--electrode', type=int, help='Possibility to define read-out electrode. Do not use if simulations has only one!', choices=[1,2,3,4,5])
# set sepletion voltage for leakage current determination
parser.add_argument('-deplV', '--depletion', type=float, help='Give depletion voltage to extract corresponding leakage currents.')
# draw and fit ranges
parser.add_argument('--log', action='store_true', help='Define if y axis on log scale.')
parser.add_argument('--fit', action='store_true', help='Define if cv curve is fitted.')
parser.add_argument('--fit_minX', type=float, default=0., help='Set fit range minimum.')
parser.add_argument('--fit_maxX', type=float, default=100., help='Set fit range maximum.')
parser.add_argument('--fit_maxY', type=float, default=1e-14, help='Limits the fit range for punch through by maximum current.')
parser.add_argument('--free', action='store_true', help='Free y range.')
parser.add_argument('--maxX', type=int, help='Set draw range maximum.')
parser.add_argument('-threeD', '--threeD', action='store_true', help='3D measurement, assumes only particle transient measurement at the moment.')
# options for transient measurements
parser.add_argument('-th', '--thickness', type=int, default=100, help='Define silicon thickness for CCE.', required= 'tran_4' in sys.argv or 'tran' in sys.argv or 'tran_3' in sys.argv or 'tran_7' in sys.argv or 'tran_8' in sys.argv)
parser.add_argument('--LET', type=float, default=1.28, help='Set the LET value for CCE calculation in [e-5pC].', required= 'tran_4' in sys.argv or 'tran_3' in sys.argv or 'tran_7' in sys.argv or 'tran_8' in sys.argv)
parser.add_argument('--scaleLET', type=int, default=1, help='Scaling of the LET for CCE.', required= 'tran_4' in sys.argv or 'tran_3' in sys.argv or 'tran_7' in sys.argv or 'tran_8' in sys.argv)
parser.add_argument('--drawMap', action='store_true', help='Print out CCE per pixel in map.')
parser.add_argument('--pitch', type=int, help='Define pitch for maps.', required='drawMap' in sys.argv)
parser.add_argument('--positionX', type=float, help='Set x position of impinging particle.', required='drawMap' in sys.argv)
parser.add_argument('--positionZ', type=float, help='Set z position of impinging particle.', required='drawMap' in sys.argv)
parser.add_argument('--drawMoreCCE', action='store_true', help='Print out 1-CCE.')
# Tested variables
parser.add_argument('-out', '--output', type=str, default='_', help='Define output file name..')
parser.add_argument('-numP', '--Parameters', type=int, default=2, help='Define how many parameters are tested.')
parser.add_argument('-p1', '--par1', action='append', default=[], help='Fill arrays with parameter value.')
parser.add_argument('-p2', '--par2', action='append', default=[], help='Fill arrays with parameter value.')
parser.add_argument('-p3', '--par3', action='append', default=[], help='Fill arrays with parameter value.')
parser.add_argument('-p4', '--par4', action='append', default=[], help='Fill arrays with parameter value.')
parser.add_argument('-p5', '--par5', action='append', default=[], help='Fill arrays with parameter value.')
parser.add_argument('-p1Name', '--par1Name', type=str, default="par1", help='Set parameter name.')
parser.add_argument('-p2Name', '--par2Name', type=str, default="par2", help='Set parameter name.')
parser.add_argument('-p3Name', '--par3Name', type=str, default="par3", help='Set parameter name.')
parser.add_argument('-p4Name', '--par4Name', type=str, default="par4", help='Set parameter name.')
parser.add_argument('-p5Name', '--par5Name', type=str, default="par5", help='Set parameter name.')

args,_=parser.parse_known_args()

threeDim = args.threeD
xmax = args.maxX
if threeDim:
    print('Running on 3D simulation..')
thickness = args.thickness
numP=args.Parameters
if args.log:
    args.output += 'log_'
if args.depletion:
    vdepletion = args.depletion
    print("Depletion voltage set to: ", vdepletion)

titles = dict([('cv', 'C [F/$\mu$m]'),
               ('iv', 'I [A/$\mu$m]'),
               ('iv_p', '|I$_{ptop}$| [A/$\mu$m]'),
               ('iv_b', '|I$_{back}$| [A/$\mu$m]'),
               ('cv_b', 'C$_{back}$ [F/$\mu$m]'),
               ('tran',  r'I$_{front}$ [$\mu$A] $\times$ '+str(args.scaleLET) ),
               ('tran_3', r'I$_{front}$ [$\mu$A] $\times$ '+str(args.scaleLET)),
               ('tran_4', r'I$_{front}$ [$\mu$A] $\times$ '+str(args.scaleLET)),
               ('tran_7', r'I$_{front}$ [$\mu$A] $\times$ '+str(args.scaleLET)),
               ('tran_8', r'I$_{front}$ [$\mu$A] $\times$ '+str(args.scaleLET)),
               ('charge', 'charge [pC]')
               ])

ranges = dict([('cv', [0, 1.5e-15]),
               ('iv', [-0.3e-13, 1.2e-13]),
               ('iv_p', [1e-20, 1e-5]),
               ('iv_b', [1e-16, 1e-5]),
               ('cv_b', [1e-16, 5e-15]),
               ('tran', [0, 1.2]),
               ('tran_3', [0, 0.2]),
               ('tran_4', [0, 0.2]),
               ('tran_7', [0, 0.2]),
               ('tran_8', [0, 0.2]),
               ('charge', [0, 1.2])
           ])

if threeDim:
    ranges['cv']=[0, 2e-14]
    titles['cv']='C [F]'
    titles['iv']='I$_{front}$ [A]'
    titles['iv_b']='|I$_{back}$| [A]'
    titles['iv_p']='|I$_{ptop}$| [A]'
if args.electrode:
    titles['iv']='I(ntop'+str(args.electrode)+') [A]'

# write parameter permutations..
arrayParPerm=[]
arrayParPermName=[]
arrayParName=[]

legTitle='' #'ARCADIA TCAD simulation\n'
legTitleAll=''
moreThanOne = 0

for i1,p1 in enumerate(args.par1):
    parOption='-pS '+p1
    parPermName=p1
    legTitleAll = args.par1Name
    if len(args.par1)>1:
        parName=p1
        arrayParName.append(parName)
        if i1==0:
            legTitle=args.par1Name
            moreThanOne+=1
    # check of more than 1 par
    if len(args.par2)>0:
        numP=2
        legTitleAll = args.par1Name+'_'+args.par2Name
        for i2,p2 in enumerate(args.par2):
            parOption='-pS '+p1+' -pS '+p2
            parPermName=p1+'_'+p2
            if len(args.par2)>1:
                parName=p2
                arrayParName.append(parName)
                if i2==0:
                    legTitle+='_'+args.par2Name
                    moreThanOne+=1
            if len(args.par3)>0:
                numP=3
                legTitleAll = args.par1Name+'_'+args.par2Name+'_'+args.par3Name
                for i3,p3 in enumerate(args.par3):
                    parOption='-pS '+p1+' -pS '+p2+' -pS '+p3
                    parPermName=p1+'_'+p2+'_'+p3
                    if len(args.par3)>1:
                        parName=p3
                        arrayParName.append(parName)
                        if i3==0:
                            legTitle+='_'+args.par3Name
                            moreThanOne+=1
                    if len(args.par4)>0:
                        numP=4
                        legTitleAll = args.par1Name+'_'+args.par2Name+'_'+args.par3Name+'_'+args.par4Name
                        for i4,p4 in enumerate(args.par4):
                            parOption='-pS '+p1+' -pS '+p2+' -pS '+p3+' -pS '+p4
                            parPermName=p1+'_'+p2+'_'+p3+'_'+p4
                            if len(args.par4)>1:
                                parName=p4
                                arrayParName.append(parName)
                                if i4==0:
                                    legTitle+='_'+args.par4Name
                                    moreThanOne+=1
                            if len(args.par5)>0:
                                numP=5
                                legTitleAll = args.par1Name+'_'+args.par2Name+'_'+args.par3Name+'_'+args.par4Name+'_'+args.par5Name
                                for i5,p5 in enumerate(args.par5):
                                    parOption='-pS '+p1+' -pS '+p2+' -pS '+p3+' -pS '+p4+' -pS '+p5
                                    parPermName=p1+'_'+p2+'_'+p3+'_'+p4+'_'+p5
                                    print(parOption)
                                    arrayParPerm.append(parOption)
                                    arrayParPermName.append(parPermName)
                                    if len(args.par5)>1:
                                        parName = p5
                                        arrayParName.append(parName)
                                        if i5==0:
                                            legTitle+='_'+args.par5Name
                                            moreThanOne+=1
                            else:
                                print(parOption)
                                arrayParPerm.append(parOption)
                                arrayParPermName.append(parPermName)
                    else:
                        print(parOption)
                        arrayParPerm.append(parOption)
                        arrayParPermName.append(parPermName)
            else:
                print(parOption)
                arrayParPerm.append(parOption)
                arrayParPermName.append(parPermName)
    else:
        print(parOption)
        arrayParPerm.append(parOption)
        arrayParPermName.append(parPermName)

if len(arrayParName)==0 or moreThanOne>1:
    arrayParName = arrayParPermName
    legTitle = legTitleAll

# produce csv files
if args.writeCSV:
    for parOption in arrayParPerm:
        print(parOption)
        if len(args.measure)>1:
            for im,m in enumerate(args.measure):
                if m=='cv':
                    # only cv files are re-written in case that muli-measures are taken!
                    # write and run tcl files to store csv files in tmp/ for
                    os.system('python3 python/writeTcl.py --project '+str(args.project)+' --'+str(m)+' '+parOption+' --run')
        else:
            # write and run tcl files to store csv files in tmp/ for
            cmd = 'python python/writeTcl.py --project '+str(args.project)+' --'+str(args.measure[0])+' '+parOption+' --run'
            if args.electrode:
                cmd += ' --electrode '+str(args.electrode)
            os.system(cmd)
            
# prepare for drawing
mark=','
lines=['-','--',':','-.','']

# create canvas
print(len(args.measure))
fig, axs = plt.subplots(len(args.measure),1, sharex=True, sharey=False) #, gridspec_kw={'hspace': 0})
# need two canvas' to include CCE
if args.measure[0]=='tran' or args.measure[0]=='tran_4' or  args.measure[0]=='tran_3' or  args.measure[0]=='tran_7' or  args.measure[0]=='tran_8':
    fig, axs = plt.subplots(2,1, sharex=True, sharey=False)

# pick color map
colormap = plt.cm.nipy_spectral
colors = [colormap(i) for i in np.linspace(0, 0.9,len(arrayParPermName))]

# arrays of Vdpl and Cend
ptVs=np.zeros(len(arrayParPermName), dtype=float)
ptIs=np.zeros(len(arrayParPermName), dtype=float)
deplVs=np.zeros(len(arrayParPermName), dtype=float)
capCs=np.zeros(len(arrayParPermName), dtype=[])
endIs=np.zeros(len(arrayParPermName), dtype=[])
CCEs=[[0 for x in range(len(arrayParPermName))] for y in range(100)]
CCEs1=[[0 for x in range(len(arrayParPermName))] for y in range(100)] 
CCEs2=[[0 for x in range(len(arrayParPermName))] for y in range(100)] 
CCEs3=[[0 for x in range(len(arrayParPermName))] for y in range(100)] 
CCEs4=[[0 for x in range(len(arrayParPermName))] for y in range(100)] 
CCEs5=[[0 for x in range(len(arrayParPermName))] for y in range(100)] 
CCEs6=[[0 for x in range(len(arrayParPermName))] for y in range(100)] 
CCEs7=[[0 for x in range(len(arrayParPermName))] for y in range(100)] 
CCEs8=[[0 for x in range(len(arrayParPermName))] for y in range(100)] 
times=[[0 for x in range(len(arrayParPermName))] for y in range(100)] 

# read csv files and analyse
for i,perm in enumerate(arrayParPermName):

    f1=csvFileName(args.project, args.measure[0], perm)
    if args.electrode:
        f1=csvFileNameElectrode(args.project, args.measure[0], perm, args.electrode)

    print(f1)
    data1 = pd.read_csv(f1, names=["X","Y","X1","Y1","X2","Y2","X3","Y3","X4","Y4","X5","Y5","X6","Y6","X7","Y7"], skiprows=1)
    lab=str(arrayParName[i])

    # if multiple measurements are analysed draw in multiple subplots
    if len(args.measure)>1:
        for im,m in enumerate(args.measure):
            f2=csvFileName(args.project, m, perm)
            if args.electrode:
                f2=csvFileNameElectrode(args.project, m, perm, args.electrode)

            data2 = pd.read_csv(f2, names=["X","Y"], skiprows=1)
            if m=='iv_b' or m=='iv_p':
                drawGraphLines(axs[im],abs(data2.X), abs(data2.Y),colors[i],lines[0],lab)
            else:
                drawGraphLines(axs[im],abs(data2.X), data2.Y,colors[i],lines[0],lab)

            axs[im].set_ylabel(titles[m])
            if not args.free:
                axs[im].set_ylim(ranges[m][0],ranges[m][1])
            if args.log:
                axs[im].set_yscale('log')
            if args.maxX:
                axs[im].set_xlim(-2, xmax)
            
            # if measurement is iv curve, fit and extract the punch through voltage
            if m=='iv_b':
                # set maximum current to be fitted for detemining punch through.. keep low for set-off
                ptV,Ipt=punchThrough(axs[im],abs(data2.X),abs(data2).Y,args.fit_maxY,colors[i])
                print('#############################')
                print( perm )
                print('Punch-through voltage found to be:  {:.1f} V'.format(ptV))
                print('Current at punch through voltage:   {:.4f} uA'.format(Ipt*pow(10,6)))
                print('#############################')
                ptVs[i]=ptV
                ptIs[i]=Ipt

            # if measurement is iv curve, fit and extract the punch through voltage
            elif m=='iv_p':
                # set maximum current to be fitted for detemining punch through.. keep low for set-off
                newDat1x=np.array(abs(data2.X[ abs(data2.X) > float(3) ]))
                newDat1y=np.array(abs(data2.Y[ abs(data2.X) > float(3) ]))
                indMin=np.where(newDat1y == newDat1y.min())
                ptV = newDat1x[int(indMin[0])]
                Ipt = newDat1y[int(indMin[0])]
                drawVoltageLine(axs[im],ptV,colors[i])
                print('#############################')
                print( perm )
                print('Punch-through voltage found to be:  {:.1f} V'.format(ptV))
                print('Current at punch through voltage:   {:.4f} uA'.format(Ipt*pow(10,6)))
                print('#############################')
                ptVs[i]=ptV
                ptIs[i]=Ipt

            # if measurement is cv curve, fit and extract the depletion voltage
            elif m=='cv' and args.fit and not args.depletion and not find_element_in_list('iv_p',args.measure):
                if args.fit_maxX or args.fit_minX:
                    deplV,deplC=deplVoltageRange(axs[im],data2,args.fit_minX, args.fit_maxX, colors[i])
                else:
                    deplV,deplC=deplVoltage(axs[im],data2,colors[i])
                print('#############################')
                print('p1='+str(p1)+', p2='+str(p2))
                print('Depletion voltage found to be:    {:.1f} V'.format(deplV))
                print('Capacitance at depletion voltage: {:.4f} fF'.format(deplC*pow(10,15)))
                print('#############################')
                deplVs[i]=deplV
                capCs[i]=deplC

            # if measurement is iv curve at specific nwell, fit and extract the depletion voltage 
            elif m=='iv' and args.electrode and args.fit and not find_element_in_list('iv_p',args.measure):
                # find minimum above 2V and below 20V
                useMin=2
                useMax=20
                if args.fit_minX:
                    useMin = args.fit_minX
                if args.fit_maxX:
                    useMax = args.fit_maxX
                newDat1x=np.array(data2.X[ (data2.X < float(useMax)) & (data2.X > float(useMin)) ])
                newDat1y=np.array(data2.Y[ (data2.X < float(useMax)) & (data2.X > float(useMin)) ])
                indMin=np.where(newDat1y == newDat1y.min())
                deplVs[i]=newDat1x[int(indMin[0])]
                Ipt = newDat1y[int(indMin[0])]
                ptIs[i]=Ipt
                drawVoltageLine(axs,deplVs[i],colors[i])
                print('#############################')
                print( perm )
                print('Depletion voltage found to be:    {:.1f} V'.format(deplVs[i]))
                print('Current at depletion voltage:     {:.4f} uA'.format(Ipt*pow(10,6)))
                print('#############################')
            
            elif (m=='iv' or m=='cv') and args.depletion:
                xtmp=np.array(abs(data2.X))
                vbin=np.where((xtmp<(vdepletion+0.5)) & (xtmp>(vdepletion-0.5)))
                ytmp=np.array(abs(data2.Y))
                Ileak=float(ytmp[vbin])
                print('#############################')
                print('Leakage current at depletion voltage {}V: {}'.format(vdepletion, Ileak))
                addValuesToPlot(axs[im], vdepletion, Ileak, colors[i], len(arrayParPermName), i ,args.log)
                print('#############################')

            elif m=='cv_b' and args.fit:
                deplV,deplC=deplVoltageRange(axs[im],data2,args.fit_minX,args.fit_maxX,colors[i])
                print('#############################')
                print( perm )
                print('Depletion voltage found to be:    {:.1f} V'.format(deplV))
                print('Capacitance at depletion voltage: {:.4f} fF'.format(deplC*pow(10,15)))
                print('#############################')
                deplVs[i]=deplV
                capCs[i]=deplC
                
        for im,m in enumerate(args.measure):
            f2=csvFileName(args.project, m, perm)
            if args.electrode:
                f2=csvFileNameElectrode(args.project, m, perm, args.electrode)

            data2 = pd.read_csv(f2, names=["X","Y"], skiprows=1)
                
            if m=='cv' and ( find_element_in_list('iv_p',args.measure) or find_element_in_list('iv_b',args.measure) ) and args.fit:
                print('#############################')
                print('Draw line at punch-through voltage.. ', ptVs[i])
                xtmp=np.array(abs(data2.X))
                vbin=0
                for volt in xtmp:
                    if volt < ptVs[i]:
                        vbin+=1
                    else:
                        break
                ytmp=np.array(abs(data2.Y))
                Cend=float(ytmp[vbin])
                print('#############################')
                print('Capacitance at punch-through voltage {}V: {}F'.format(ptVs[i], Cend))
                print('#############################')
                addValuesToPlot(axs[im], ptVs[i], Cend, colors[i], m, len(arrayParPermName), i ,args.log)
                drawVoltageLine(axs[im], ptVs[i], colors[i])
            
            elif m=='iv' and find_element_in_list('iv_p',args.measure) and args.fit:
                print('#############################')
                print('Write leakage current at punch through in plot.. ')
                xtmp=np.array(abs(data2.X))
                vbin=np.where((xtmp<ptVs[i]+0.5) & (xtmp>ptVs[i]-0.5))
                if len(vbin[0])>1:
                    vbin = vbin[0][0]
                ytmp=np.array(abs(data2.Y))
                Ileak=float(ytmp[vbin])
                print('#############################')
                print('Leakage current at punch-thourgh: ', Ileak)
                print('#############################')
                addValuesToPlot(axs[im], ptVs[i], Ileak, colors[i], m, len(arrayParPermName), i ,args.log)
                drawVoltageLine(axs[im], ptVs[i], colors[i])

    # if only one measurement, draw in one canvas
    else:
        if args.measure[0]=='tran' or args.measure[0]=='tran_3' or args.measure[0]=='tran_4' or args.measure[0]=='tran_7' or args.measure[0]=='tran_8':
            if args.measure[0]=='tran':
                drawGraphLines(axs[0],data1.X*pow(10,9), args.scaleLET*(data1.Y*pow(10,6)), colors[i], lines[0],lab)
            # scale the current signals with args.scaleLET to correspond to the CCE
            elif args.measure[0]=='tran_3':
                draw3MultiGraphLines(axs[0],data1.X*pow(10,9), data1.Y*pow(10,6), data1.Y1*pow(10,6), data1.Y2*pow(10,6), args.scaleLET, lines[0])
            elif args.measure[0]=='tran_4':
                if len(arrayParPermName)==1:
                    draw4MultiGraphLines(axs[0],data1.X*pow(10,9), data1.Y*pow(10,6), data1.Y1*pow(10,6), data1.Y2*pow(10,6), data1.Y3*pow(10,6), args.scaleLET)
                else:
                    draw4MultiMultiGraphLines(axs[0],data1.X*pow(10,9), data1.Y*pow(10,6), data1.Y1*pow(10,6), data1.Y2*pow(10,6), data1.Y3*pow(10,6), args.scaleLET, i, colors, lines)
            elif args.measure[0]=='tran_7':
                draw7MultiGraphLines(axs[0],data1.X*pow(10,9), data1.Y*pow(10,6), data1.Y1*pow(10,6), data1.Y2*pow(10,6), data1.Y3*pow(10,6), data1.Y4*pow(10,6), data1.Y5*pow(10,6), data1.Y6*pow(10,6), args.scaleLET, lines[0])
            elif args.measure[0]=='tran_8':
                draw8MultiGraphLines(axs[0],data1.X*pow(10,9), data1.Y*pow(10,6), data1.Y1*pow(10,6), data1.Y2*pow(10,6), data1.Y3*pow(10,6), data1.Y4*pow(10,6), data1.Y5*pow(10,6), data1.Y6*pow(10,6), data1.Y7*pow(10,6), args.scaleLET, lines[0])
                    
            #set x range
            axs[0].set_xlim(-2, axs[0].get_xlim()[1])
            if args.maxX:
                axs[1].set_xlim(-2, xmax)
                axs[0].set_xlim(-2, xmax)

            # fill array with time bins for hit maps
            times[i]=data1.X*pow(10,9)
            datay = data1.Y
            if args.measure[0]=='tran_7':
                datay = data1.Y3

            # integrate current over 200ns
            # C=A*s
            totalCharge=getIntegral(datay,data1.X)* pow(10,12)
            # search for the LET value in string
            # transform from pC/um to pC
            print("Found LET of: ", args.LET)
            final_let=float( args.LET ) * pow(10,-5) * thickness
            # print("Convert to LET*thickness: ", final_let)
            # normalise to 1/4 when running in 4 pixel domain, assumes particle in 0,0
                
            if args.scaleLET != 1:
                final_let = final_let / float(args.scaleLET)
            cce = totalCharge/final_let
            print('#############################')
            print( perm )
            print('Total charge                                 :    {:.4f}x10^-5 pC'.format(totalCharge)) #*pow(10,5)))
            print('LET                                          :    {:.4f}x10^-5 pC'.format(final_let*pow(10,5)))
            print('Charge collection efficiency (single channel):    {:.1f} %'.format(cce*100))
            print('#############################')
            
            # draw CCE over time
            if args.measure[0]=='tran':
                CCEs1[i] = drawCCE(axs[1],data1.X,data1.Y,final_let,colors[i],lines[0],lab)
                axs[1].set_ylabel('CCE')

            # draw CCEs over time and return 3 arrays
            elif args.measure[0]=='tran_3':
                CCEs1[i], CCEs2[i], CCEs3[i] = draw3MultiCCE(axs[1],data1.X,data1.Y,data1.Y1,data1.Y2,final_let,lines[0])
                axs[1].set_ylabel(r'CCE $\times$ '+str(args.scaleLET))
                
            elif args.measure[0]=='tran_4':
                if len(arrayParPermName)==1:
                    times[i], CCEs1[i], CCEs2[i], CCEs3[i], CCEs4[i] = draw4MultiCCE(axs[1],data1.X,data1.Y,data1.Y1,data1.Y2,data1.Y3,final_let)
                else:
                    times[i], CCEs1[i], CCEs2[i], CCEs3[i], CCEs4[i] = draw4MultiMultiCCE(axs[1],data1.X,data1.Y,data1.Y1,data1.Y2,data1.Y3,final_let,i,colors,lines)
                axs[1].set_ylabel(r'CCE $\times$ '+str(args.scaleLET))
                
            # draw CCEs over time and return 7 arrays
            elif args.measure[0]=='tran_7':
                CCEs1[i], CCEs2[i], CCEs3[i], CCEs4[i], CCEs5[i], CCEs6[i], CCEs7[i] = draw7MultiCCE(axs[1],data1.X,data1.Y,data1.Y1,data1.Y2,data1.Y3,data1.Y4,data1.Y5,data1.Y6,final_let,lines[0])
                axs[1].set_ylabel(r'CCE $\times$ '+str(args.scaleLET))

            # draw CCEs over time and return 8 arrays
            elif args.measure[0]=='tran_8':
                CCEs1[i], CCEs2[i], CCEs3[i], CCEs4[i], CCEs5[i], CCEs6[i], CCEs7[i], CCEs8[i] = draw8MultiCCE(axs[1],data1.X,data1.Y,data1.Y1,data1.Y2,data1.Y3,data1.Y4,data1.Y5,data1.Y6,data1.Y7,final_let,lines[0])
                axs[1].set_ylabel(r'CCE $\times$ '+str(args.scaleLET))

            print('#############################')
            print('Total CCE, integrated over all channels.')
            
            channels = int(re.search(r'\d+', args.measure[0]).group())
            for ch in range(1,channels+1):
                #print(i,ch)
                if ch==1:
                    CCEs[i] = eval("CCEs"+str(ch))[i]
                else:
                    CCEs[i] += eval("CCEs"+str(ch))[i]

            time95 = getTime(times[i],CCEs[i],95)
            time99 = getTime(times[i],CCEs[i],99)
                
            print('Time of 95% collection:    {:.1f} ns'.format(time95))
            print('Time of 99% collection:    {:.1f} ns'.format(time99))
            print('#############################')

            axs[1].set_xlabel('time [ns]')
            startY=0.05
            deltaY=0.2*i
            if args.log:
                startY=1E-6
                deltaY=pow(10,-6+i)
            axs[1].text( axs[0].get_xlim()[1]/2., startY+deltaY, '$t_{95}=$'+str("{:.1f}ns").format(time95)+', $t_{99}=$'+str("{:.1f}ns").format(time99), color=colors[i])
            axs[0].set_ylabel(titles['tran'])

            if not args.free:
                axs[1].set_ylim(0,1.2)

            if args.log:
                axs[0].set_yscale('log')
                axs[1].set_yscale('log')

            axs[1].set_xticks(np.arange(0, int(axs[1].get_xlim()[1]),  int(axs[1].get_xlim()[1]/10.) ))
            plt.grid(True)

        elif args.measure[0]=='charge':
            drawGraphLines(axs,data1.X*pow(10,9), data1.Y*pow(10,12),colors[i],lines[0],lab)
            axs.set_xlabel('time [ns]')
            axs.set_xlim(-2,50)
            axs.set_ylabel(titles[args.measure[0]])
            if not args.free:
                axs.set_ylim(ranges[args.measure[0]][0],ranges[args.measure[0]][1])

        else:
            if args.maxX:
                axs.set_xlim(-2, xmax)

            dat1x=abs(data1.X)
            dat1y=data1.Y

            # if measure current at back, determine punch through voltage
            if args.measure[0]=='iv_b' and args.fit:
                drawGraphLines(axs,dat1x,abs(dat1y),colors[i],lines[0],lab)
                dat1y=abs(dat1y)
                # set maximum current to be fitted for detemining punch through.. keep low for set-off
                ptV,Ipt=punchThrough(axs,dat1x,dat1y,args.fit_maxY,colors[i])
                print('#############################')
                print( perm )
                print('Punch-through voltage found to be:  {:.1f} V'.format(ptV))
                print('Current at punch through voltage:   {:.4f} uA'.format(Ipt*pow(10,6)))
                print('#############################')

                # if measure current at p well, determine punch through voltage
            elif args.measure[0]=='iv_p' and args.fit:
                drawGraphLines(axs,dat1x,abs(dat1y),colors[i],lines[0],lab)
                dat1y=abs(dat1y)
                # find minimum above 3V
                newDat1x=np.array(dat1x[ dat1x > float(3) ])
                newDat1y=np.array(dat1y[ dat1x > float(3) ])
                indMin=np.where(newDat1y == newDat1y.min())
                ptV = newDat1x[int(indMin[0])]
                Ipt = newDat1y[int(indMin[0])]
                drawVoltageLine(axs,ptV,colors[i])
                
                print('#############################')
                print( perm )
                print('Punch-through voltage found to be:  {:.1f} V'.format(ptV))
                print('Current at punch through voltage:   {:.4f} uA'.format(Ipt*pow(10,6)))
                print('#############################')
                
            elif args.measure[0]=='iv' and args.fit and args.electrode:
                drawGraphLines(axs,dat1x,dat1y,colors[i],lines[0],lab)
                # find minimum above 2V and below 20V
                useMin=2
                useMax=20
                if args.fit_minX:
                    useMin = args.fit_minX
                if args.fit_maxX:
                    useMax = args.fit_maxX 
                newDat1x=np.array(dat1x[ (dat1x < float(useMax)) & (dat1x > float(useMin)) ])
                newDat1y=np.array(dat1y[ (dat1x < float(useMax)) & (dat1x > float(useMin)) ])
                indMin=np.where(newDat1y == newDat1y.min())
                ptV = newDat1x[int(indMin[0])]
                Ipt = newDat1y[int(indMin[0])]
                drawVoltageLine(axs,ptV,colors[i])
                
                print('#############################')
                print( perm )
                print('Depletion voltage found to be:    {:.1f} V'.format(ptV))
                print('Current at depletion voltage:     {:.4f} uA'.format(Ipt*pow(10,6)))
                print('#############################')
                
            elif (args.measure[0]=='iv' or args.measure[0]=='cv') and args.depletion:
                drawGraphLines(axs,dat1x,dat1y,colors[i],lines[0],lab)
                xtmp=np.array(abs(data1.X))
                #print(xtmp)
                vbin=np.where( (xtmp < (vdepletion+1.5)) & (xtmp > (vdepletion-1.5)) )
                # use value found closest to actual value
                # print(vbin)
                if len(vbin[0])>1:
                    usev=0
                    diff = 10
                    for index in range(0, len(vbin[0])):
                        voltage = xtmp[vbin[0][index]]
                        if abs((voltage - vdepletion)/vdepletion) < diff:
                            usev=index
                    vbin=vbin[0][usev]
                print('Found: ', xtmp[vbin])
                ytmp=np.array(abs(data1.Y))
                Ileak=float(ytmp[vbin])
                print('#############################')
                print('Leakage current/Capacitance at depletion voltage {}V: {}'.format(vdepletion, Ileak))
                print('#############################')
                drawVoltageLine(axs, vdepletion, colors[i])
                addValuesToPlot(axs, vdepletion, Ileak, colors[i], args.measure[0], len(arrayParPermName), i ,args.log)

            else:
                drawGraphLines(axs,abs(data1.X), data1.Y,colors[i],lines[0],lab)
            axs.set_xlabel('|V|')
            axs.set_ylabel(titles[args.measure[0]])
            if not args.free:
                axs.set_ylim(ranges[args.measure[0]][0],ranges[args.measure[0]][1])
            if args.log:
                axs.set_yscale('log')

        # if measurement is cv curve, fit and extract the depletion voltage
        if args.measure[0]=='cv' and args.fit and not args.depletion:
            if args.fit_maxX or args.fit_minX:
                deplV,deplC=deplVoltageRange(axs,data1,args.fit_minX, args.fit_maxX, colors[i])
            else:
                deplV,deplC=deplVoltage(axs,data1,colors[i])
            print('#############################')
            print( perm )
            print('Depletion voltage found to be:    {:.1f} V'.format(deplV))
            print('Capacitance at depletion voltage: {:.4f} fF'.format(deplC*pow(10,15)))
            print('#############################')
            deplVs[i]=deplV
            capCs[i]=deplC
            
        elif args.measure[0]=='cv_b' and args.fit:
            deplV,deplC=deplVoltageRange(axs,data1,args.fit_minX,args.fit_maxX,colors[i])
            print('#############################')
            print( perm )
            print('Depletion voltage found to be:    {:.1f} V'.format(deplV))
            print('Capacitance at depletion voltage: {:.4f} fF'.format(deplC*pow(10,15)))
            print('#############################')
            deplVs[i]=deplV
            capCs[i]=deplC

        
# draw all measured curves
allM=''
for m in args.measure:
    allM=allM+m
outName=allCurvesName(args.project, allM, args.output, 'pdf')
print(outName)

# add ARCADIA label
arcadia='ARCADIA TCAD simulation'

if len(args.measure)>1 or args.measure[0]=='tran_4' or args.measure[0]=='tran_3' or args.measure[0]=='tran' or args.measure[0]=='tran_7' or args.measure[0]=='tran_8':
    if args.measure[0]=='tran_4' or args.measure[0]=='tran_3' or args.measure[0]=='tran' or args.measure[0]=='tran_7' or args.measure[0]=='tran_8':
        plt.subplots_adjust(top=0.8)
        colmn=4
        if len(arrayParPermName)>1:
            colmn=int(len(arrayParPermName)/2.)
        else:
            legTitle=legTitle+'\n'+arrayParPermName[0]
        axs[0].legend(loc='upper center', bbox_to_anchor=(.5, 1.5), fancybox=True, ncol=colmn, title=legTitle)
    else:
        if moreThanOne>1 and len(arrayParPermName)<5:
            axs[0].legend(loc='upper center', bbox_to_anchor=(.5, 1.2), fancybox=True, ncol=1, title=legTitle)
        elif len(arrayParPermName)>4 and numP>3:
            plt.subplots_adjust(right=0.8)
            axs[0].legend(title=legTitle, loc='upper left', bbox_to_anchor=(1, 0.5), fancybox=True)
        else:
            plt.subplots_adjust(right=0.7)
            axs[0].legend(title=legTitle, loc='upper left', bbox_to_anchor=(1, 0.5), fancybox=True)
    axs[len(args.measure)-1].set_xlabel('|V|')
    axs[1].text(0,1.05,arcadia,color='gray',fontsize=10,fontweight='bold')
else:
    if not args.measure[0]=='tran_4' and not args.measure[0]=='tran_3' and not args.measure[0]=='tran' and not args.measure[0]=='tran_7' and not args.measure[0]=='tran_8':
        if len(arrayParPermName)==1:
            legTitle=legTitle+'\n'+arrayParPermName[0]
        if len(arrayParPermName)>4 and numP<4:
            plt.subplots_adjust(right=0.75)
            axs.legend(title=legTitle, loc='upper left', bbox_to_anchor=(1, 0.5), fancybox=True)
        elif len(arrayParPermName)>4 and len(arrayParPermName)<8 and numP>2:
            plt.subplots_adjust(right=0.6)
            axs.legend(title=legTitle, loc='upper left', bbox_to_anchor=(1, 0.5), fancybox=True)
        elif len(arrayParPermName)>8:
            plt.subplots_adjust(right=0.6)
            axs.legend(title=legTitle, loc='upper left', bbox_to_anchor=(1, 0.75), fancybox=True)
        else: 
            axs.legend(loc='upper center', bbox_to_anchor=(.5, 1.1), fancybox=True, ncol=1, title=legTitle)

# print out
fig.savefig(outName)

if args.drawMoreCCE:
    # draw 1-CCE for comparison of different parameters over all channels
    plotOutName=allCurvesName(args.project, 'CCE_'+allM, args.output, 'pdf')
    print('Print 1-CCE: ',plotOutName)
    figCCE, axsCCE = plt.subplots(1,1, sharex=True, sharey=False)
    fixedTime=5. #ns      
    Effs=[0 for x in range(len(arrayParPermName))]
    for i in range(len(arrayParPermName)):
        maxCCE=0
        trial=1
        while maxCCE==0:
            CCEs_loc = CCEs[i][1:len(CCEs)-trial]
            times_loc = times[i][1:len(CCEs)-trial]
            maxCCE = float(CCEs[i][len(CCEs[i])-trial])
            trial+=1
        print("Normalise CCEs to : {:.1f}".format(100*maxCCE) )
        normCCEs = np.array([1 - (x / maxCCE) for x in CCEs_loc])
        normTimes = np.array(times_loc)

        axsCCE.plot(normTimes, normCCEs, color=colors[i], marker=',', label=arrayParName[i])
        axsCCE.set_yscale('log')
        axsCCE.set_xlim(0,args.maxX)
    
        time99 = getTime(normTimes, CCEs_loc,99)
        time95 = getTime(normTimes, CCEs_loc,95)
        time90 = getTime(normTimes, CCEs_loc,90)

        cce99 = normCCEs[(normTimes == time99)][0]
        cce95 = normCCEs[(normTimes == time95)][0]
        cce90 = normCCEs[(normTimes == time90)][0]
        
        #find index of charge collection at 'fixedTime'
        j=0
        for timeVal in times[i]:
            if timeVal < fixedTime:
                j+=1
            else:
                break

        Effs[i] = CCEs[i][j]/ maxCCE

        # 99%
        if i==0:
            plt.hlines(y=cce99, xmin=0, xmax=time99, color=colors[i], label='99%')
        else:
            plt.hlines(y=cce99, xmin=0, xmax=time99, color=colors[i])
        plt.vlines(x=time99, ymin=0, ymax=cce99, color=colors[i])
        # 95%
        #plt.hlines(y=cce95, xmin=0, xmax=time95, color=colors[i], linestyle=lines[1])
        #plt.vlines(x=time95, ymin=0, ymax=cce95, color=colors[i], linestyle=lines[1])
        # 90%
        if i==0:
            plt.hlines(y=cce90, xmin=0, xmax=time90, color=colors[i], linestyle=lines[2], label='90%')
        else:
            plt.hlines(y=cce90, xmin=0, xmax=time90, color=colors[i], linestyle=lines[2])
        plt.vlines(x=time90, ymin=0, ymax=cce90, color=colors[i], linestyle=lines[2])

    plt.subplots_adjust(right=0.75)
    axsCCE.legend(title=legTitle, loc='upper left', bbox_to_anchor=(1, 0.77777775), fancybox=True)
    axsCCE.set_xlabel('time [ns]')
    axsCCE.set_ylabel('1-CCE$_{tot}$')
    figCCE.savefig(plotOutName)                                                                                                                                                                                           
    
    # add efficiency plot
    plotOutName2=allCurvesName(args.project, 'Eff_'+allM, args.output, 'pdf')
    print('Print Efficiency: ', plotOutName2)
    figEff, axsEff = plt.subplots(1,1, sharex=True, sharey=False)
    arrPos=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
    print(Effs)
    axsEff.plot(arrPos[:len(arrayParPermName)], Effs, color='black', marker='o')
    axsEff.set_ylabel('CCE$_{tot}$('+str(fixedTime)+'ns)')
    axsEff.set_xlabel('pos [$\mu$m]')
    axsEff.text(0,1.05,arcadia,color='gray',fontsize=10,fontweight='bold')
    figEff.savefig(plotOutName2)

if args.drawMap: 
    # draw hit maps for trans_4 measurements
    plotOutName=allCurvesName(args.project, 'CCE_map_'+allM, args.output, 'pdf')
    print('#################')
    print('Print CCE map: ',plotOutName)
    # number of transients
    channels = int(re.search(r'\d+', args.measure[0]).group())
    vecCCEs = []
    print("Normalise CCEs to : {:.1f}".format(100*(CCEs[0][len(CCEs[0])-1])) )
    print("CCE of 1st channel: {:.1f}".format(100*(CCEs1[0][len(CCEs1[0])-1])) )
    print("Length(time): ", len(times[0]))
    print("Length(CEEs): ", len(CCEs1[0]))

    for channel in range(0,channels+1):
        # normalise CCEs
        if channel==0:
            normCCEs = [x / CCEs[0][len(CCEs[0])-1] for x in CCEs[0]]
        else:
            normCCEs = [x / CCEs[0][len(CCEs[0])-1] for x in eval('CCEs'+str(channel))[0]]
            print("CCE of {}st channel: {:.1f}".format(channel, 100*(normCCEs[len(normCCEs)-1])) )
        vecCCEs.append(normCCEs)

    drawMap(channels, times[0], vecCCEs, args.pitch, args.positionX, args.positionZ, args.scaleLET, plotOutName, False)

#if args.measure[0]=='tran_3' and args.drawMap:
#    timeBin=math.floor(len(times[0])/10.)
#    # sample time in 10
#    
#    for t in range(1,10):
#        timeValue=int(0)
#        realTime=t*timeBin
#        # for last time bin, use the highest entry
#        if t==9:
#            timeValue=int(times[0][len(times[0])-1])
#        else:
#            timeValue=int(times[0][realTime])
#    
#        plotOutName=allCurvesName(args.project, 'CCE_map_'+str(timeValue)+'ns_'+allM, args.output, 'pdf')
#        print(plotOutName)
#    
#        matrix = 0
#        # draw map in 4x4 if --scaleLET 4
#        if args.scaleLET==4:
#            matrix = 5
#            arrX=[20,10,0,10,20]
#            arrY=[0]
#            arrXYZ=[[0 for x in range(0,5)] for y in range(0,1)]
#            #print(arrXYZ)
#            for pixX in range(0,5):
#                for pixY in range(0,1):
#                    weight=0
#                    if (pixX==0 and pixY==0) or (pixX==4 and pixY==0):
#                        weight=CCEs3[0][realTime]
#                    elif (pixX==1 or pixX==3) and (pixY==0):
#                        weight=CCEs2[0][realTime]
#                    else:
#                        weight=CCEs1[0][realTime]
#                    #print(pixX,pixY)
#                    #print(weight)
#                    arrXYZ[pixY][pixX]=weight*100./4.
#                    #print(arrXYZ)
#                    #print(len(arrXYZ))
#                    
#        # draw map in 4x4 if --scaleLET 4
#        if args.scaleLET==1:
#            matrix = 5
#            arrX=[20,10,0,10,20]
#            arrY=[0]
#            arrXYZ=[[0 for x in range(0,5)] for y in range(0,1)]
#            #print(arrXYZ)
#            for pixX in range(0,5):
#                for pixY in range(0,1):
#                    weight=0
#                    if (pixX==0 and pixY==0) or (pixX==4 and pixY==0):
#                        weight=CCEs1[0][realTime]
#                    elif (pixX==1 or pixX==3) and (pixY==0):
#                        weight=CCEs2[0][realTime]
#                    else:
#                        weight=CCEs3[0][realTime]
#                    #print(pixX,pixY)
#                    #print(weight)
#                    arrXYZ[pixY][pixX]=weight*100.
#                    #print(arrXYZ)
#                    #print(len(arrXYZ))
#
#        fig, ax = plt.subplots()
#        im = ax.imshow(arrXYZ, cmap='viridis', vmin=0, vmax=int(120/float(args.scaleLET)), aspect=5)
#        ax.set_xticks(np.arange(5)) #np.arange(matrix)
#        ax.set_yticks(np.arange(1)) #np.arange(matrix)
#        # ... and label them with the respective list entries
#        ax.set_xticklabels(arrX)
#        ax.set_yticklabels(arrY)
#        #ax.imshow(arrXYZ)
#        ax.set_xticks(np.arange(len(arrXYZ[0])+1)-.5, minor=True)
#        ax.set_yticks(np.arange(len(arrXYZ)+1)-.5, minor=True)
#        ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
#        ax.tick_params(which="minor", bottom=False, left=False)
#        # write values in pixel
#        for pixX in range(0,matrix):
#            for pixY in range(0,1):
#                text = ax.text(pixX, pixY, "{0:.1f}".format(arrXYZ[pixY][pixX]),
#                               ha="center", va="bottom", color="w")
#        
#        # Create colorbar
#        cbar = ax.figure.colorbar(im, ax=ax, cmap="viridis")
#        cbar.ax.set_ylabel('CCE [%] $\Delta$t='+str(timeValue)+'ns', rotation=-90, va="bottom")
#        # add impinging point
#        x = matrix/2. - 0.5 #math.floor(matrix/2.)
#        y = 0 #matrix/2. - 0.5 #math.floor(matrix/2.)
#        # print(x,y)
#        ax.scatter(x,y,color='r')
#        fig.tight_layout()
#        fig.savefig(plotOutName)
#    
#    
#    
## draw hit maps for trans_7 measurements
#if args.measure[0]=='tran_7' and args.drawMap:
#    timeBin=math.floor(len(times[0])/10.)
#    # sample time in 10
#    
#    for t in range(1,10):
#        timeValue=int(0)
#        realTime=t*timeBin
#        # for last time bin, use the highest entry
#        if t==9:
#            timeValue=int(times[0][len(times[0])-1])
#        else:
#            timeValue=int(times[0][realTime])
#    
#        plotOutName=allCurvesName(args.project, 'CCE_map_'+str(timeValue)+'ns_'+allM, args.output, 'pdf')
#        print(plotOutName)
#    
#        matrix = 0
#        # draw map in 4x4 if --scaleLET 4
#
#        if args.scaleLET==4:
#            matrix = 7
#            arrX=[0,10,20,30,40,50,60]
#            arrY=[0]
#            arrXYZ=[[0 for x in range(0,7)] for y in range(0,1)]
#            #print(arrXYZ)
#            for pixX in range(0,7):
#                for pixY in range(0,1):
#                    weight=0
#                    if (pixX==0 and pixY==0):
#                        weight=CCEs1[0][realTime]*4
#                    elif (pixX==1 and pixY==0):
#                        weight=CCEs2[0][realTime]*2
#                    elif (pixX==2 and pixY==0):
#                        weight=CCEs3[0][realTime]*2
#                    elif (pixX==3 and pixY==0):
#                        weight=CCEs4[0][realTime]*2
#                    elif (pixX==4 and pixY==0):
#                        weight=CCEs5[0][realTime]*2
#                    elif (pixX==5 and pixY==0):
#                        weight=CCEs6[0][realTime]*2
#                    elif (pixX==6 and pixY==0):
#                        weight=CCEs7[0][realTime]*2
#		    #print(pixX,pixY)
#                    #print(weight)
#                    arrXYZ[pixY][pixX]=weight*100./4.
#                    #print(arrXYZ)
#                    #print(len(arrXYZ))
#                    
#        # draw map in 4x4 if --scaleLET 4
#        if args.scaleLET==1:
#            matrix = 7
#            arrX=[30,20,10,0,10,20,30]
#            arrY=[0]
#            arrXYZ=[[0 for x in range(0,7)] for y in range(0,1)]
#            #print(arrXYZ)
#            for pixX in range(0,7):
#                for pixY in range(0,1):
#                    weight=0
#                    if (pixX==0 and pixY==0):
#                        weight=CCEs1[0][realTime]
#                    elif (pixX==1 and pixY==0):
#                        weight=CCEs2[0][realTime]
#                    elif (pixX==2 and pixY==0):
#                        weight=CCEs3[0][realTime]
#                    elif (pixX==3 and pixY==0):
#                        weight=CCEs4[0][realTime]
#                    elif (pixX==4 and pixY==0):
#                        weight=CCEs5[0][realTime]
#                    elif (pixX==5 and pixY==0):
#                        weight=CCEs6[0][realTime]
#                    elif (pixX==6 and pixY==0):
#                        weight=CCEs7[0][realTime]
#                    #print(pixX,pixY)
#                    #print(weight)
#                    arrXYZ[pixY][pixX]=weight*100.
#                    #print(arrXYZ)
#                    #print(len(arrXYZ))
#
#        fig, ax = plt.subplots()
#        im = ax.imshow(arrXYZ, cmap='viridis', vmin=0, vmax=int(120/float(args.scaleLET)), aspect=5)
#        ax.set_xticks(np.arange(7)) #np.arange(matrix)
#        ax.set_yticks(np.arange(1)) #np.arange(matrix)
#        # ... and label them with the respective list entries
#        ax.set_xticklabels(arrX)
#        ax.set_yticklabels(arrY)
#        #ax.imshow(arrXYZ)
#        ax.set_xticks(np.arange(len(arrXYZ[0])+1)-.5, minor=True)
#        ax.set_yticks(np.arange(len(arrXYZ)+1)-.5, minor=True)
#        ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
#        ax.tick_params(which="minor", bottom=False, left=False)
#        # write values in pixel
#        for pixX in range(0,matrix):
#            for pixY in range(0,1):
#                text = ax.text(pixX, pixY, "{0:.1f}".format(arrXYZ[pixY][pixX]),
#                               ha="center", va="bottom", color="w")
#        
#        # Create colorbar
#        cbar = ax.figure.colorbar(im, ax=ax, cmap="viridis")
#        cbar.ax.set_ylabel('CCE [%] $\Delta$t='+str(timeValue)+'ns', rotation=-90, va="bottom")
#        # add impinging point
#        if args.scaleLET==1:
#            x = matrix/2. - 0.5 #math.floor(matrix/2.)
#            y = 0 #matrix/2. - 0.5 #math.floor(matrix/2.)
#            # print(x,y)
#            ax.scatter(x,y,color='r')
#        if args.scaleLET==4:
#            x = 0 #matrix/2. - 0.5 #math.floor(matrix/2.)
#            y = 0 #matrix/2. - 0.5 #math.floor(matrix/2.)
#            # print(x,y)
#            ax.scatter(x,y,color='r')
#        fig.tight_layout()
#        fig.savefig(plotOutName)
#
#
## draw hit maps for trans_8 measurements
#if args.measure[0]=='tran_8' and args.drawMap:
#    timeBin=math.floor(len(times[0])/10.)
#    # sample time in 10
#    for t in range(1,10):
#        timeValue=int(0)
#        realTime=t*timeBin
#        # for last time bin, use the highest entry
#        if t==9:
#            timeValue=int(times[0][len(times[0])-1])
#        else:
#            timeValue=int(times[0][realTime])
#    
#        plotOutName=allCurvesName(args.project, 'CCE_map_'+str(timeValue)+'ns_'+allM, args.output, 'pdf')
#        print(plotOutName)
#    
#        matrix = 0
#        #if --scaleLET 4
#        if args.scaleLET==4:
#            matrix = 8
#            arrX=[0,10,20,30,40,50,60,70]
#            arrY=[0]
#            arrXYZ=[[0 for x in range(0,8)] for y in range(0,1)]
#            for pixX in range(0,8):
#                for pixY in range(0,1):
#                    weight=0
#                    if (pixX==0 and pixY==0):
#                        weight=CCEs1[0][realTime]*4 #particle in nwell
#                    elif (pixX==1 and pixY==0):
#                        weight=CCEs2[0][realTime]*2
#                    elif (pixX==2 and pixY==0):
#                        weight=CCEs3[0][realTime]*2
#                    elif (pixX==3 and pixY==0):
#                        weight=CCEs4[0][realTime]*2
#                    elif (pixX==4 and pixY==0):
#                        weight=CCEs5[0][realTime]*2
#                    elif (pixX==5 and pixY==0):
#                        weight=CCEs6[0][realTime]*2
#                    elif (pixX==6 and pixY==0):
#                        weight=CCEs7[0][realTime]*2
#                    elif (pixX==7 and pixY==0):
#                        weight=CCEs8[0][realTime]*2
#                        
#                    arrXYZ[pixY][pixX]=weight*100./4.
#
#        fig, ax = plt.subplots()
#        im = ax.imshow(arrXYZ, cmap='viridis', vmin=0, vmax=int(120/float(args.scaleLET)), aspect=5)
#        ax.set_xticks(np.arange(8)) #np.arange(matrix)
#        ax.set_yticks(np.arange(1)) #np.arange(matrix)
#        # ... and label them with the respective list entries
#        ax.set_xticklabels(arrX)
#        ax.set_yticklabels(arrY)
#        #ax.imshow(arrXYZ)
#        ax.set_xticks(np.arange(len(arrXYZ[0])+1)-.5, minor=True)
#        ax.set_yticks(np.arange(len(arrXYZ)+1)-.5, minor=True)
#        ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
#        ax.tick_params(which="minor", bottom=False, left=False)
#        # write values in pixel
#        for pixX in range(0,matrix):
#            for pixY in range(0,1):
#                text = ax.text(pixX, pixY, "{0:.1f}".format(arrXYZ[pixY][pixX]),
#                               ha="center", va="bottom", color="w")
#        # Create colorbar
#        cbar = ax.figure.colorbar(im, ax=ax, cmap="viridis")
#        cbar.ax.set_ylabel('CCE [%] $\Delta$t='+str(timeValue)+'ns', rotation=-90, va="bottom")
#        # add impinging point
#        if args.scaleLET==4:
#            x = 0
#            y = 0
#            ax.scatter(x,y,color='r')
#        fig.tight_layout()
#        fig.savefig(plotOutName)
