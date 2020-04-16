import os, sys, argparse, re
from utils import *
import pandas as pd
import numpy as np
from matplotlib import ticker
parser = argparse.ArgumentParser()

parser.add_argument('--project', type=str, default='ARCADIA25um_surfaceDamage', help='Define patht to project.')
parser.add_argument('--writeCSV', action='store_true', help='Convert tcl to csv, if not already done.')
parser.add_argument('-m', '--measure', action='append', type=str, default=[], help='Define which plots you want to draw.', choices=['cv','iv','iv_p','iv_b','cv_b','tran','tran_3','tran_4','tran_7','tran_8','charge'])
# define read-out electrode
parser.add_argument('-el', '--electrode', type=int, help='Possibility to define read-out electrode. Do not use if simulations has only one!', choices=[1,2,3,4,5])
# draw and fit ranges
parser.add_argument('--log', action='store_true', help='Define if y axis on log scale.')
parser.add_argument('--fit', action='store_true', help='Define if cv curve is fitted.')
parser.add_argument('--fit_minX', type=float, default=0., help='Set fit range minimum.')
parser.add_argument('--fit_maxX', type=float, default=100., help='Set fit range maximum.')
parser.add_argument('--free', action='store_true', help='Free y range.')
parser.add_argument('--maxX', type=int, help='Set draw range maximum.')
parser.add_argument('-threeD', '--threeD', action='store_true', help='3D measurement, assumes only particle transient measurement at the moment.')
# options for transient measurements
parser.add_argument('-th', '--thickness', type=int, default=100, help='Define silicon thickness for CCE.', required= 'tran_4' in sys.argv or 'tran' in sys.argv or 'tran_3' in sys.argv or 'tran_7' in sys.argv or 'tran_8' in sys.argv)
parser.add_argument('--LET', type=float, default=1.28, help='Set the LET value for CCE calculation.', required= 'tran_4' in sys.argv or 'tran_3' in sys.argv or 'tran_7' in sys.argv or 'tran_8' in sys.argv)
parser.add_argument('--scaleLET', type=int, default=1, help='Scaling of the LET for CCE.', required= 'tran_4' in sys.argv or 'tran_3' in sys.argv or 'tran_7' in sys.argv or 'tran_8' in sys.argv)
parser.add_argument('--drawMap', action='store_true', help='Print out CCE per pixel in map.')
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

titles = dict([('cv', 'C [F/$\mu$m]'),
               ('iv', 'I [A/$\mu$m]'),
               ('iv_p', 'I$_{ptop}$ [A/$\mu$m]'),
               ('iv_b', 'I$_{back}$ [A/$\mu$m]'),
               ('cv_b', 'C$_{back}$ [F/$\mu$m]'),
               ('tran', 'I$_{front}$ [$\mu$A]'),
               ('tran_3', 'I$_{front}$ [$\mu$A]'),
               ('tran_4', 'I$_{front}$ [$\mu$A]'),
               ('tran_7', 'I$_{front}$ [$\mu$A]'),
               ('tran_8', 'I$_{front}$ [$\mu$A]'),
               ('charge', 'charge [pC]')
               ])

ranges = dict([('cv', [2e-16, 1.5e-15]),
               ('iv', [7e-17, 5e-14]),
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
    titles['iv']='I [A]'

# write parameter permutations..
arrayParPerm=[]
arrayParPermName=[]
legTitle=args.par1Name
for p1 in args.par1:
    parOption='-pS '+p1
    parPermName=p1
    # check of more than 1 par
    if len(args.par2)>0:
        legTitle=args.par1Name+'_'+args.par2Name
        numP=2
        for p2 in args.par2:
            parOption='-pS '+p1+' -pS '+p2
            parPermName=p1+'_'+p2
            if len(args.par3)>0:
                legTitle=args.par1Name+'_'+args.par2Name+'_'+args.par3Name
                numP=3
                for p3 in args.par3:
                    parOption='-pS '+p1+' -pS '+p2+' -pS '+p3
                    parPermName=p1+'_'+p2+'_'+p3
                    if len(args.par4)>0:
                        legTitle=args.par1Name+'_'+args.par2Name+'_'+args.par3Name+'_'+args.par4Name
                        numP=4
                        for p4 in args.par4:
                            parOption='-pS '+p1+' -pS '+p2+' -pS '+p3+' -pS '+p4
                            parPermName=p1+'_'+p2+'_'+p3+'_'+p4
                            if len(args.par5)>0:
                                legTitle=args.par1Name+'_'+args.par2Name+'_'+args.par3Name+'_'+args.par4Name+'_'+args.par5Name
                                numP=5
                                for p5 in args.par5:
                                    parOption='-pS '+p1+' -pS '+p2+' -pS '+p3+' -pS '+p4+' -pS '+p5
                                    parPermName=p1+'_'+p2+'_'+p3+'_'+p4+'_'+p5
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
    else:
        print(parOption)
        arrayParPerm.append(parOption)
        arrayParPermName.append(parPermName)

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
            cmd = 'python3 python/writeTcl.py --project '+str(args.project)+' --'+str(args.measure[0])+' '+parOption+' --run'
            if args.electrode:
                cmd += ' --electrode '+str(args.electrode)
            os.system(cmd)
            
# prepare for drawing
mark=','
lines=['-','--',':','-.']

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
    lab=str(perm)

    # if multiple measurements are analysed draw in multiple subplots
    if len(args.measure)>1:
        for im,m in enumerate(args.measure):
            f2=csvFileName(args.project, m, perm)
            if args.electrode:
                f2=csvFileNameElectrode(args.project, m, perm, args.electrode)

            data2 = pd.read_csv(f2, names=["X","Y"], skiprows=1)
                
            drawGraphLines(axs[im],abs(data2.X), abs(data2.Y),colors[i],lines[0],lab)
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
                ptV,Ipt=punchThrough(axs[im],abs(data2.X),abs(data2.Y),1e-13,colors[i])
                print('#############################')
                print( perm )
                print('Punch-through voltage found to be:  {:.1f} V'.format(ptV))
                print('Current at punch through voltage:   {:.4f} uA'.format(Ipt*pow(10,6)))
                print('#############################')
                ptVs[i]=ptV
                ptIs[i]=Ipt

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
            elif m=='cv' and args.fit:
                if args.fit_maxX or args.fit_minX:
                    deplV,deplC=deplVoltageRange(axs[im],data2,args.fit_minX, args.fit_maxX, colors[i])
                else:
                    deplV,deplC=deplVoltage(axs[im],data2,colors[i])
                print('#############################')
                print('p1='+str(p1)+', p2='+str(p2))
                print('Depletion voltage found to be:    {:.1f} V'.format(deplV))
                print('Capacitance at depletion voltage: {:.4f} fC'.format(deplC*pow(10,15)))
                print('#############################')
                deplVs[i]=deplV
                capCs[i]=deplC

            elif m=='iv' and args.fit:
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
                ptV = newDat1x[int(indMin[0])]
                Ipt = newDat1y[int(indMin[0])]
                drawVoltageLine(axs,ptV,colors[i])

                print('#############################')
                print( perm )
                print('Depletion voltage found to be:    {:.1f} V'.format(ptV))
                print('Current at depletion voltage:     {:.4f} uA'.format(Ipt*pow(10,6)))
                print('#############################')

            elif m=='cv_b' and args.fit:
                deplV,deplC=deplVoltageRange(axs[im],data2,args.fit_minX,args.fit_maxX,colors[i])
                print('#############################')
                print( perm )
                print('Depletion voltage found to be:    {:.1f} V'.format(deplV))
                print('Capacitance at depletion voltage: {:.4f} fC'.format(deplC*pow(10,15)))
                print('#############################')
                deplVs[i]=deplV
                capCs[i]=deplC
                
        for im,m in enumerate(args.measure):
            f2=csvFileName(args.project, m, perm)
            if args.electrode:
                f2=csvFileNameElectrode(args.project, m, perm, args.electrode)

            data2 = pd.read_csv(f2, names=["X","Y"], skiprows=1)
            # check if punch-through/depletion voltage is detemined
            if (m=='iv' or m=='iv_b' or m=='iv_p') and find_element_in_list('cv',args.measure) and args.fit:
                xtmp=np.array(abs(data2.X))
                vbin=np.where((xtmp<deplVs[i]+0.5) & (xtmp>deplVs[i]-0.5) )
                ytmp=np.array(abs(data2.Y))
                idpl=float(ytmp[vbin])
                print('Current at depletion voltage:    {:.4f} pA'.format(idpl*pow(10,12)))
                print('#############################')
                drawVoltagePoint(axs[im],deplVs[i],idpl,colors[i])
                
            elif m=='cv' and ( find_element_in_list('iv_p',args.measure) or find_element_in_list('iv_b',args.measure) ) and args.fit:
                print('#############################')
                print('Draw punch-through.. ', ptVs[i])
                drawVoltageLine(axs[im],ptVs[i],colors[i])

                
    # if only one measurement, draw in one canvas
    else:
        if args.measure[0]=='tran' or args.measure[0]=='tran_3' or args.measure[0]=='tran_4' or args.measure[0]=='tran_7' or args.measure[0]=='tran_8':
            if args.measure[0]=='tran':
                drawGraphLines(axs[0],data1.X*pow(10,9), data1.Y*pow(10,6),colors[i],lines[0],lab)
            elif args.measure[0]=='tran_3':
                draw3MultiGraphLines(axs[0],data1.X*pow(10,9), data1.Y*pow(10,6), data1.Y1*pow(10,6), data1.Y2*pow(10,6), lines[0])
            elif args.measure[0]=='tran_4':
                draw4MultiGraphLines(axs[0],data1.X*pow(10,9), data1.Y*pow(10,6), data1.Y1*pow(10,6), data1.Y2*pow(10,6), data1.Y3*pow(10,6),lines[0])
            elif args.measure[0]=='tran_7':
                draw7MultiGraphLines(axs[0],data1.X*pow(10,9), data1.Y*pow(10,6), data1.Y1*pow(10,6), data1.Y2*pow(10,6), data1.Y3*pow(10,6), data1.Y4*pow(10,6), data1.Y5*pow(10,6), data1.Y6*pow(10,6),lines[0])
            elif args.measure[0]=='tran_8':
                draw8MultiGraphLines(axs[0],data1.X*pow(10,9), data1.Y*pow(10,6), data1.Y1*pow(10,6), data1.Y2*pow(10,6), data1.Y3*pow(10,6), data1.Y4*pow(10,6), data1.Y5*pow(10,6), data1.Y6*pow(10,6), data1.Y7*pow(10,6),lines[0])
                    
            #set x range
            axs[0].set_xlim(-2, axs[0].get_xlim()[1])
            if args.maxX:
                axs[1].set_xlim(-2, xmax)
                axs[0].set_xlim(-2, xmax)

            # fill array with time bins for hit maps
            times[i]=data1.X*pow(10,9)

            if args.measure[0]=='tran_7':
                # integrate current over 200ns
                # C=A*s
                totalCharge=abs(getIntegral(data1.Y3,data1.X)* pow(10,12)) #,0,10*pow(10,-9)) * pow(10,12)
                # search for the LET value in string
                # transform from pC/um to pC
                print("Found LET of: ", args.LET)
                final_let=float( args.LET ) * pow(10,-5) * thickness
                # print("Convert to LET*thickness: ", final_let)
                # normalise to 1/4 when running in 4 pixel domain, assumes particle in 0,0
            
            else:
                # integrate current over 200ns
                # C=A*s
                totalCharge=abs(getIntegral(data1.Y,data1.X)* pow(10,12)) #,0,10*pow(10,-9)) * pow(10,12)
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
            print('Total charge                :    {:.4f}x10^-5 pC'.format(totalCharge*pow(10,5)))
            print('LET                         :    {:.4f}x10^-5 pC'.format(final_let*pow(10,5)))
            print('Charge collection efficiency:    {:.1f} %'.format(cce*100))
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
                CCEs1[i], CCEs2[i], CCEs3[i], CCEs4[i] = draw4MultiCCE(axs[1],data1.X,data1.Y,data1.Y1,data1.Y2,data1.Y3,final_let,lines[0])
                axs[1].set_ylabel(r'CCE $\times$ '+str(args.scaleLET))
                
            # draw CCEs over time and return 7 arrays
            elif args.measure[0]=='tran_7':
                CCEs1[i], CCEs2[i], CCEs3[i], CCEs4[i], CCEs5[i], CCEs6[i], CCEs7[i] = draw7MultiCCE(axs[1],data1.X,data1.Y,data1.Y1,data1.Y2,data1.Y3,data1.Y4,data1.Y5,data1.Y6,final_let,lines[0])
                axs[1].set_ylabel(r'CCE $\times$ '+str(args.scaleLET))

            # draw CCEs over time and return 8 arrays
            elif args.measure[0]=='tran_8':
                CCEs1[i], CCEs2[i], CCEs3[i], CCEs4[i], CCEs5[i], CCEs6[i], CCEs7[i], CCEs8[i] = draw8MultiCCE(axs[1],data1.X,data1.Y,data1.Y1,data1.Y2,data1.Y3,data1.Y4,data1.Y5,data1.Y6,data1.Y7,final_let,lines[0])
                axs[1].set_ylabel(r'CCE $\times$ '+str(args.scaleLET))

            if args.measure[0]=='tran_7':
                time95 = getTime(times[i],CCEs4[i],95)
                time99 = getTime(times[i],CCEs4[i],99)
                
            else:
                time95 = getTime(times[i],CCEs1[i],95)
                time99 = getTime(times[i],CCEs1[i],99)
                
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

            #axs[1].set_ylim(10e-5,2) #lorenzo

        elif args.measure[0]=='charge':
            drawGraphLines(axs,data1.X*pow(10,9), data1.Y*pow(10,12),colors[i],lines[0],lab)
            axs.set_xlabel('time [ns]')
            axs.set_xlim(-2,50)
            axs.set_ylabel(titles[args.measure[0]])
            if not args.free:
                axs.set_ylim(ranges[args.measure[0]][0],ranges[args.measure[0]][1])

        else:
            dat1x=abs(data1.X)
            dat1y=abs(data1.Y)

            if args.measure[0]=='iv_b' or args.measure[0]=='iv_p' or args.measure[0]=='iv':
                drawGraphLines(axs,dat1x,dat1y,colors[i],lines[0],lab)
                # if measure current at back, determine punch through voltage
                if args.measure[0]=='iv_b' and args.fit:
                    # set maximum current to be fitted for detemining punch through.. keep low for set-off
                    ptV,Ipt=punchThrough(axs,dat1x,dat1y,1e-14,colors[i])
                    print('#############################')
                    print( perm )
                    print('Punch-through voltage found to be:  {:.1f} V'.format(ptV))
                    print('Current at punch through voltage:   {:.4f} uA'.format(Ipt*pow(10,6)))
                    print('#############################')

                # if measure current at p well, determine punch through voltage
                elif args.measure[0]=='iv_p' and args.fit:
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

                elif args.measure[0]=='iv' and args.fit:
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

            else:
                drawGraphLines(axs,abs(data1.X), data1.Y,colors[i],lines[0],lab)
            axs.set_xlabel('|V|')
            axs.set_ylabel(titles[args.measure[0]])
            if not args.free:
                axs.set_ylim(ranges[args.measure[0]][0],ranges[args.measure[0]][1])
            if args.log:
                axs.set_yscale('log')
        # if measurement is cv curve, fit and extract the depletion voltage
        if args.measure[0]=='cv' and args.fit:
            if args.fit_maxX or args.fit_minX:
                deplV,deplC=deplVoltageRange(axs,data1,args.fit_minX, args.fit_maxX, colors[i])
            else:
                deplV,deplC=deplVoltage(axs,data1,colors[i])
            print('#############################')
            print( perm )
            print('Depletion voltage found to be:    {:.1f} V'.format(deplV))
            print('Capacitance at depletion voltage: {:.4f} fC'.format(deplC*pow(10,15)))
            print('#############################')
            deplVs[i]=deplV
            capCs[i]=deplC
            
        elif args.measure[0]=='cv_b' and args.fit:
            deplV,deplC=deplVoltageRange(axs,data1,args.fit_minX,args.fit_maxX,colors[i])
            print('#############################')
            print( perm )
            print('Depletion voltage found to be:    {:.1f} V'.format(deplV))
            print('Capacitance at depletion voltage: {:.4f} fC'.format(deplC*pow(10,15)))
            print('#############################')
            deplVs[i]=deplV
            capCs[i]=deplC

        
# draw all measured curves
allM=''
for m in args.measure:
    allM=allM+m
outName=allCurvesName(args.project, allM, args.output, 'pdf')
print(outName)

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
        axs[0].legend(title=legTitle, loc='upper left', bbox_to_anchor=(1, 0.5), fancybox=True)
        axs[len(args.measure)-1].set_xlabel('|V|')
else:
    axs.legend(title=legTitle, loc='center left', bbox_to_anchor=(1, 0.5), fancybox=True)
if not args.measure[0]=='tran_4' and not args.measure[0]=='tran_3' and not args.measure[0]=='tran' and not args.measure[0]=='tran_7' and not args.measure[0]=='tran_8':
    if numP>3:
        plt.subplots_adjust(right=0.5)
    else:
        plt.subplots_adjust(right=0.65)
# print out
fig.savefig(outName)


# to be moved outside
# draw hit maps for trans_4 measurements
if args.measure[0]=='tran_4' and args.drawMap:
    timeBin=math.floor(len(times[0])/10.)
    # sample time in 10
    for t in range(1,10):
        timeValue=int(0)
        realTime=t*timeBin
        # for last time bin, use the highest entry
        if t==9:
            timeValue=int(times[0][len(times[0])-1])
        else:
            timeValue=int(times[0][realTime])

        plotOutName=allCurvesName(args.project, 'CCE_map_'+str(timeValue)+'ns_'+allM, args.output, 'pdf')
        print(plotOutName)

        matrix_X = 0
        matrix_Y = 0
        # draw map in 4x4 if --scaleLET 4
        if args.scaleLET==4:
            matrix_X = 4
            matrix_Y = 4
            arrX=[1,0,0,1]
            arrY=[1,0,0,1]
            arrXYZ=[[0 for x in range(4)] for y in range(4)]
            for pixX in range(0,4):
                for pixY in range(0,4):
                    weight=0
                    if (pixX==0 and pixY==0) or (pixX==3 and pixY==3) or (pixX==0 and pixY==3) or (pixX==3 and pixY==0):
                        weight=CCEs4[0][realTime]
                    elif (pixX==1 or pixX==2) and (pixY==2 or pixY==1):
                        weight=CCEs1[0][realTime]
                    else:
                        weight=CCEs2[0][realTime]
                    #print(pixX,pixY)
                    #print(weight)
                    arrXYZ[pixY][pixX]=weight*100./4.

        # draw map in 3x4 if --scaleLET 4
        if args.scaleLET==2:
            matrix_X = 4
            matrix_Y = 3
            arrX=[1,0,0,1]
            arrY=[1,0,1]
            arrXYZ=[[0 for x in range(4)] for y in range(3)]
            for pixX in range(0,4):
                for pixY in range(0,3):
                    weight=0
                    if (pixX==1 or pixX==2) and pixY==1:
                        weight=CCEs1[0][realTime]
                    elif (pixX==0 and pixY==0) or (pixX==3 and pixY==2) or (pixX==0 and pixY==2) or (pixX==3 and pixY==0):
                        weight=CCEs4[0][realTime]
                    elif (pixX==0 and pixY==1) or (pixX==3 and pixY==1):
                        weight=CCEs3[0][realTime]
                    else:
                        weight=CCEs2[0][realTime]
                    arrXYZ[pixY][pixX]=weight*100./2.

        # draw map in 3x3 if --scaleLET 1
        if args.scaleLET==1:
            matrix_X = 3
            matrix_Y = 3
            arrX=[1,0,1]
            arrY=[1,0,1]
            arrXYZ=[[0 for x in range(3)] for y in range(3)]
            for pixX in range(0,3):
                for pixY in range(0,3):
                    weight=0
                    if (pixX==1 and pixY==1): # or (pixX==3 and pixY==3) or (pixX==0 and pixY==3) or (pixX==3 and pixY==0):
                        weight=CCEs1[0][realTime]
                    elif (pixX==1 or pixY==1):
                        weight=CCEs2[0][realTime]
                    else:
                        weight=CCEs4[0][realTime]
                    arrXYZ[pixX][pixY]=weight*100.

        fig, ax = plt.subplots()
        im = ax.imshow(arrXYZ, cmap='viridis', vmin=0, vmax=int(120/float(args.scaleLET)))
        ax.set_xticks(np.arange(matrix_X))
        ax.set_yticks(np.arange(matrix_Y))
        # ... and label them with the respective list entries
        ax.set_xticklabels(arrX)
        ax.set_yticklabels(arrY)
        #ax.imshow(arrXYZ)
        ax.set_xticks(np.arange(matrix_X+1)-.5, minor=True)
        ax.set_yticks(np.arange(matrix_Y+1)-.5, minor=True)
        ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
        ax.tick_params(which="minor", bottom=False, left=False)
        # write values in pixel
        for pixX in range(0,matrix_X):
            for pixY in range(0,matrix_Y):
                text = ax.text(pixX, pixY, "{0:.1f}".format(arrXYZ[pixY][pixX]),
                               ha="center", va="center", color="w")
        
        # Create colorbar
        cbar = ax.figure.colorbar(im, ax=ax, cmap="viridis")
        cbar.ax.set_ylabel('CCE [%] $\Delta$t='+str(timeValue)+'ns', rotation=-90, va="bottom")
        # add impinging point
        x = matrix_X/2. - 0.5 #math.floor(matrix/2.)
        y = matrix_Y/2. - 0.5 #math.floor(matrix/2.)
        # print(x,y)
        ax.scatter(x,y,color='r')
        fig.tight_layout()
        fig.savefig(plotOutName)





# draw hit maps for trans_3 measurements
if args.measure[0]=='tran_3' and args.drawMap:
    timeBin=math.floor(len(times[0])/10.)
    # sample time in 10
    
    for t in range(1,10):
        timeValue=int(0)
        realTime=t*timeBin
        # for last time bin, use the highest entry
        if t==9:
            timeValue=int(times[0][len(times[0])-1])
        else:
            timeValue=int(times[0][realTime])
    
        plotOutName=allCurvesName(args.project, 'CCE_map_'+str(timeValue)+'ns_'+allM, args.output, 'pdf')
        print(plotOutName)
    
        matrix = 0
        # draw map in 4x4 if --scaleLET 4
        if args.scaleLET==4:
            matrix = 5
            arrX=[20,10,0,10,20]
            arrY=[0]
            arrXYZ=[[0 for x in range(0,5)] for y in range(0,1)]
            #print(arrXYZ)
            for pixX in range(0,5):
                for pixY in range(0,1):
                    weight=0
                    if (pixX==0 and pixY==0) or (pixX==4 and pixY==0):
                        weight=CCEs3[0][realTime]
                    elif (pixX==1 or pixX==3) and (pixY==0):
                        weight=CCEs2[0][realTime]
                    else:
                        weight=CCEs1[0][realTime]
                    #print(pixX,pixY)
                    #print(weight)
                    arrXYZ[pixY][pixX]=weight*100./4.
                    #print(arrXYZ)
                    #print(len(arrXYZ))
                    
        # draw map in 4x4 if --scaleLET 4
        if args.scaleLET==1:
            matrix = 5
            arrX=[20,10,0,10,20]
            arrY=[0]
            arrXYZ=[[0 for x in range(0,5)] for y in range(0,1)]
            #print(arrXYZ)
            for pixX in range(0,5):
                for pixY in range(0,1):
                    weight=0
                    if (pixX==0 and pixY==0) or (pixX==4 and pixY==0):
                        weight=CCEs1[0][realTime]
                    elif (pixX==1 or pixX==3) and (pixY==0):
                        weight=CCEs2[0][realTime]
                    else:
                        weight=CCEs3[0][realTime]
                    #print(pixX,pixY)
                    #print(weight)
                    arrXYZ[pixY][pixX]=weight*100.
                    #print(arrXYZ)
                    #print(len(arrXYZ))

        fig, ax = plt.subplots()
        im = ax.imshow(arrXYZ, cmap='viridis', vmin=0, vmax=int(120/float(args.scaleLET)), aspect=5)
        ax.set_xticks(np.arange(5)) #np.arange(matrix)
        ax.set_yticks(np.arange(1)) #np.arange(matrix)
        # ... and label them with the respective list entries
        ax.set_xticklabels(arrX)
        ax.set_yticklabels(arrY)
        #ax.imshow(arrXYZ)
        ax.set_xticks(np.arange(len(arrXYZ[0])+1)-.5, minor=True)
        ax.set_yticks(np.arange(len(arrXYZ)+1)-.5, minor=True)
        ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
        ax.tick_params(which="minor", bottom=False, left=False)
        # write values in pixel
        for pixX in range(0,matrix):
            for pixY in range(0,1):
                text = ax.text(pixX, pixY, "{0:.1f}".format(arrXYZ[pixY][pixX]),
                               ha="center", va="bottom", color="w")
        
        # Create colorbar
        cbar = ax.figure.colorbar(im, ax=ax, cmap="viridis")
        cbar.ax.set_ylabel('CCE [%] $\Delta$t='+str(timeValue)+'ns', rotation=-90, va="bottom")
        # add impinging point
        x = matrix/2. - 0.5 #math.floor(matrix/2.)
        y = 0 #matrix/2. - 0.5 #math.floor(matrix/2.)
        # print(x,y)
        ax.scatter(x,y,color='r')
        fig.tight_layout()
        fig.savefig(plotOutName)
    
    
    
# draw hit maps for trans_7 measurements
if args.measure[0]=='tran_7' and args.drawMap:
    timeBin=math.floor(len(times[0])/10.)
    # sample time in 10
    
    for t in range(1,10):
        timeValue=int(0)
        realTime=t*timeBin
        # for last time bin, use the highest entry
        if t==9:
            timeValue=int(times[0][len(times[0])-1])
        else:
            timeValue=int(times[0][realTime])
    
        plotOutName=allCurvesName(args.project, 'CCE_map_'+str(timeValue)+'ns_'+allM, args.output, 'pdf')
        print(plotOutName)
    
        matrix = 0
        # draw map in 4x4 if --scaleLET 4

        if args.scaleLET==4:
            matrix = 7
            arrX=[0,10,20,30,40,50,60]
            arrY=[0]
            arrXYZ=[[0 for x in range(0,7)] for y in range(0,1)]
            #print(arrXYZ)
            for pixX in range(0,7):
                for pixY in range(0,1):
                    weight=0
                    if (pixX==0 and pixY==0):
                        weight=CCEs1[0][realTime]*4
                    elif (pixX==1 and pixY==0):
                        weight=CCEs2[0][realTime]*2
                    elif (pixX==2 and pixY==0):
                        weight=CCEs3[0][realTime]*2
                    elif (pixX==3 and pixY==0):
                        weight=CCEs4[0][realTime]*2
                    elif (pixX==4 and pixY==0):
                        weight=CCEs5[0][realTime]*2
                    elif (pixX==5 and pixY==0):
                        weight=CCEs6[0][realTime]*2
                    elif (pixX==6 and pixY==0):
                        weight=CCEs7[0][realTime]*2
		    #print(pixX,pixY)
                    #print(weight)
                    arrXYZ[pixY][pixX]=weight*100./4.
                    #print(arrXYZ)
                    #print(len(arrXYZ))
                    
        # draw map in 4x4 if --scaleLET 4
        if args.scaleLET==1:
            matrix = 7
            arrX=[30,20,10,0,10,20,30]
            arrY=[0]
            arrXYZ=[[0 for x in range(0,7)] for y in range(0,1)]
            #print(arrXYZ)
            for pixX in range(0,7):
                for pixY in range(0,1):
                    weight=0
                    if (pixX==0 and pixY==0):
                        weight=CCEs1[0][realTime]
                    elif (pixX==1 and pixY==0):
                        weight=CCEs2[0][realTime]
                    elif (pixX==2 and pixY==0):
                        weight=CCEs3[0][realTime]
                    elif (pixX==3 and pixY==0):
                        weight=CCEs4[0][realTime]
                    elif (pixX==4 and pixY==0):
                        weight=CCEs5[0][realTime]
                    elif (pixX==5 and pixY==0):
                        weight=CCEs6[0][realTime]
                    elif (pixX==6 and pixY==0):
                        weight=CCEs7[0][realTime]
                    #print(pixX,pixY)
                    #print(weight)
                    arrXYZ[pixY][pixX]=weight*100.
                    #print(arrXYZ)
                    #print(len(arrXYZ))

        fig, ax = plt.subplots()
        im = ax.imshow(arrXYZ, cmap='viridis', vmin=0, vmax=int(120/float(args.scaleLET)), aspect=5)
        ax.set_xticks(np.arange(7)) #np.arange(matrix)
        ax.set_yticks(np.arange(1)) #np.arange(matrix)
        # ... and label them with the respective list entries
        ax.set_xticklabels(arrX)
        ax.set_yticklabels(arrY)
        #ax.imshow(arrXYZ)
        ax.set_xticks(np.arange(len(arrXYZ[0])+1)-.5, minor=True)
        ax.set_yticks(np.arange(len(arrXYZ)+1)-.5, minor=True)
        ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
        ax.tick_params(which="minor", bottom=False, left=False)
        # write values in pixel
        for pixX in range(0,matrix):
            for pixY in range(0,1):
                text = ax.text(pixX, pixY, "{0:.1f}".format(arrXYZ[pixY][pixX]),
                               ha="center", va="bottom", color="w")
        
        # Create colorbar
        cbar = ax.figure.colorbar(im, ax=ax, cmap="viridis")
        cbar.ax.set_ylabel('CCE [%] $\Delta$t='+str(timeValue)+'ns', rotation=-90, va="bottom")
        # add impinging point
        if args.scaleLET==1:
            x = matrix/2. - 0.5 #math.floor(matrix/2.)
            y = 0 #matrix/2. - 0.5 #math.floor(matrix/2.)
            # print(x,y)
            ax.scatter(x,y,color='r')
        if args.scaleLET==4:
            x = 0 #matrix/2. - 0.5 #math.floor(matrix/2.)
            y = 0 #matrix/2. - 0.5 #math.floor(matrix/2.)
            # print(x,y)
            ax.scatter(x,y,color='r')
        fig.tight_layout()
        fig.savefig(plotOutName)


# draw hit maps for trans_8 measurements
if args.measure[0]=='tran_8' and args.drawMap:
    timeBin=math.floor(len(times[0])/10.)
    # sample time in 10
    for t in range(1,10):
        timeValue=int(0)
        realTime=t*timeBin
        # for last time bin, use the highest entry
        if t==9:
            timeValue=int(times[0][len(times[0])-1])
        else:
            timeValue=int(times[0][realTime])
    
        plotOutName=allCurvesName(args.project, 'CCE_map_'+str(timeValue)+'ns_'+allM, args.output, 'pdf')
        print(plotOutName)
    
        matrix = 0
        #if --scaleLET 4
        if args.scaleLET==4:
            matrix = 8
            arrX=[0,10,20,30,40,50,60,70]
            arrY=[0]
            arrXYZ=[[0 for x in range(0,8)] for y in range(0,1)]
            for pixX in range(0,8):
                for pixY in range(0,1):
                    weight=0
                    if (pixX==0 and pixY==0):
                        weight=CCEs1[0][realTime]*4 #particle in nwell
                    elif (pixX==1 and pixY==0):
                        weight=CCEs2[0][realTime]*2
                    elif (pixX==2 and pixY==0):
                        weight=CCEs3[0][realTime]*2
                    elif (pixX==3 and pixY==0):
                        weight=CCEs4[0][realTime]*2
                    elif (pixX==4 and pixY==0):
                        weight=CCEs5[0][realTime]*2
                    elif (pixX==5 and pixY==0):
                        weight=CCEs6[0][realTime]*2
                    elif (pixX==6 and pixY==0):
                        weight=CCEs7[0][realTime]*2
                    elif (pixX==7 and pixY==0):
                        weight=CCEs8[0][realTime]*2
                        
                    arrXYZ[pixY][pixX]=weight*100./4.

        fig, ax = plt.subplots()
        im = ax.imshow(arrXYZ, cmap='viridis', vmin=0, vmax=int(120/float(args.scaleLET)), aspect=5)
        ax.set_xticks(np.arange(8)) #np.arange(matrix)
        ax.set_yticks(np.arange(1)) #np.arange(matrix)
        # ... and label them with the respective list entries
        ax.set_xticklabels(arrX)
        ax.set_yticklabels(arrY)
        #ax.imshow(arrXYZ)
        ax.set_xticks(np.arange(len(arrXYZ[0])+1)-.5, minor=True)
        ax.set_yticks(np.arange(len(arrXYZ)+1)-.5, minor=True)
        ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
        ax.tick_params(which="minor", bottom=False, left=False)
        # write values in pixel
        for pixX in range(0,matrix):
            for pixY in range(0,1):
                text = ax.text(pixX, pixY, "{0:.1f}".format(arrXYZ[pixY][pixX]),
                               ha="center", va="bottom", color="w")
        # Create colorbar
        cbar = ax.figure.colorbar(im, ax=ax, cmap="viridis")
        cbar.ax.set_ylabel('CCE [%] $\Delta$t='+str(timeValue)+'ns', rotation=-90, va="bottom")
        # add impinging point
        if args.scaleLET==4:
            x = 0
            y = 0
            ax.scatter(x,y,color='r')
        fig.tight_layout()
        fig.savefig(plotOutName)
