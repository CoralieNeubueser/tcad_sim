import os, sys, argparse, re
from utils import * 
import pandas as pd
import numpy as np

parser = argparse.ArgumentParser()

parser.add_argument('--project', type=str, default='ARCADIA25um_surfaceDamage', help='Define patht to project.')
parser.add_argument('--writeCSV', action='store_true', help='Convert tcl to csv, if not already done.')
parser.add_argument('-threeD', '--threeD', action='store_true', help='3D measurement, assumes only particle transient measurement at the moment.')
parser.add_argument('-m', '--measure', action='append', type=str, default=[], help='Define which plots you want to draw.', choices=['cv','iv','iv_b','cv_b','tran'])
parser.add_argument('--log', action='store_true', help='Define if y axis on log scale.')
parser.add_argument('-numP', '--Parameters', type=int, default=2, help='Define how many parameters are tested.')
parser.add_argument('-p1', '--par1', action='append', default=[], help='Fill arrays with parameter value.')
parser.add_argument('-p2', '--par2', action='append', default=[], help='Fill arrays with parameter value.')
parser.add_argument('-p3', '--par3', action='append', default=[], help='Fill arrays with parameter value.')
parser.add_argument('-p4', '--par4', action='append', default=[], help='Fill arrays with parameter value.')
parser.add_argument('-p5', '--par5', action='append', default=[], help='Fill arrays with parameter value.')

args,_=parser.parse_known_args()

threeDim = args.threeD
if threeDim:
    print('Running on 3D simulation..')

titles = dict([('cv', 'C [F/$\mu$m]'),
               ('iv', 'I [A/$\mu$m]'),
               ('iv_b', 'I$_{back}$ [A/$\mu$m]'),
               ('cv_b', 'C$_{back}$ [F/$\mu$m]'),
               ('tran', 'I$_{front}$ [$\mu$A]')
               ])

ranges = dict([('cv', [2e-16, 5e-15]),
               ('iv', [7e-17, 5e-14]),
               ('iv_b', [1e-18, 1e-5]),
               ('cv_b', [1e-16, 5e-15]),
               ('tran', [0, 1.2])
           ])

if threeDim:
    ranges['cv']=[0, 2e-14]
    titles['cv']='C [F]'
    titles['iv']='I [A]'


# write parameter permutations.. 
arrayParPerm=[]
arrayParPermName=[]
for p1 in args.par1:
    parOption='-pS '+p1
    parPermName=p1
    # check of more than 1 par
    if len(args.par2)>0:
        for p2 in args.par2:
            parOption='-pS '+p1+' -pS '+p2
            parPermName=p1+'_'+p2
            if len(args.par3)>0:
                for p3 in args.par3:
                    parOption='-pS '+p1+' -pS '+p2+' -pS '+p3
                    parPermName=p1+'_'+p2+'_'+p3
                    if len(args.par4)>0:
                        for p4 in args.par4:
                            parOption='-pS '+p1+' -pS '+p2+' -pS '+p3+' -pS '+p4
                            parPermName=p1+'_'+p2+'_'+p3+'_'+p4
                            if len(args.par5)>0:
                                for p5 in args.par5:
                                    parOption='-pS '+p1+' -pS '+p2+' -pS '+p3+' -pS '+p4+' -pS '+p5
                                    parPermName=p1+'_'+p2+'_'+p3+'_'+p4+'_'+p5
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
                    # write and run tcl files to store csv files in tmp/ for
                    os.system('python3 python/writeTcl.py --project '+str(args.project)+' --'+str(m)+' '+parOption+' --run')
        else:
            # write and run tcl files to store csv files in tmp/ for
            os.system('python3 python/writeTcl.py --project '+str(args.project)+' --'+str(args.measure[0])+' '+parOption+' --run')
            
# prepare for drawing
colors = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c',
          '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5',
          '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f',
          '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5' ]
mark=','
lines=['-','--',':','-.']

print(len(args.measure))
fig, axs = plt.subplots(len(args.measure),1, sharex=True, sharey=False) #, gridspec_kw={'hspace': 0})

# arrays of Vdpl and Cend
deplVs=np.zeros(len(arrayParPermName), dtype=float)
capCs=np.zeros(len(arrayParPermName), dtype=float)
endIs=np.zeros(len(arrayParPermName), dtype=float)

# read csv files and analyse
for i,perm in enumerate(arrayParPermName):

    f1=csvFileName(args.project, args.measure[0], perm)
    print(f1)
    data1 = pd.read_csv(f1, names=["X","Y"], skiprows=1)
    
    lab=str(perm)

    # if multiple measurements are analysed draw in multiple subplots
    if len(args.measure)>1:
        for im,m in enumerate(args.measure):
            f2=csvFileName(args.project, m, perm)
            data2 = pd.read_csv(f2, names=["X","Y"], skiprows=1)
                
            drawGraphLines(axs[im],-data2.X, data2.Y,colors[i],lines[0],lab)
            axs[im].set_ylabel(titles[m])
            axs[im].set_ylim(ranges[m][0],ranges[m][1])
            if args.log:
                axs[im].set_yscale('log')
            
            # if measurement is cv curve, fit and extract the depletion voltage 
            if m=='cv':
                deplV,deplC=deplVoltage(axs[im],data2,colors[i])
                print('#############################')
                print('p1='+str(p1)+', p2='+str(p2))
                print('Depletion voltage found to be:    {:.1f} V'.format(deplV))
                print('Capacitance at depletion voltage: {:.4f} fC'.format(deplC*pow(10,15)))
                print('#############################')
                deplVs[i]=deplV
                capCs[i]=deplC

            elif  m=='cv_b':
                deplV,deplC=deplVoltageRange(axs[im],data2,5,30,colors[i])
                print('#############################')
                print( perm )
                print('Depletion voltage found to be:    {:.1f} V'.format(deplV))
                print('Capacitance at depletion voltage: {:.4f} fC'.format(deplC*pow(10,15)))
                print('#############################')
                deplVs[i]=deplV
                capCs[i]=deplC
                
            elif m=='iv' and m.find('cv'):
                xtmp=np.array(-data2.X)
                vbin=np.where((xtmp<deplVs[i]+0.2) & (xtmp>deplVs[i]-0.2) )
                ytmp=np.array(data2.Y)
                idpl=float(ytmp[vbin])
                print('Current at depletion voltage:    {:.4f} pA'.format(idpl*pow(10,12)))
                print('#############################')
                drawVdpl(axs[im],deplVs[i],idpl,colors[i])
                
    # if only one measurement, draw in one canvas
    else:
        if args.measure[0]=='tran':
            drawGraphLines(axs,data1.X*pow(10,9), data1.Y*pow(10,6),colors[i],lines[0],lab)
        else:        
            drawGraphLines(axs,-data1.X, data1.Y,colors[i],lines[0],lab)
        axs.set_ylabel(titles[args.measure[0]])
        axs.set_xlabel('|V|')
        if args.measure[0]=='tran':
            axs.set_xlabel('time [ns]')
            axs.set_xlim(-2,15)
        axs.set_ylim(ranges[args.measure[0]][0],ranges[args.measure[0]][1])
        if args.log:
            axs.set_yscale('log') 
        
        # if measurement is cv curve, fit and extract the depletion voltage
        if args.measure[0]=='cv':
            deplV,deplC=deplVoltage(axs,data1,colors[i])
            print('#############################')
            print( perm )
            print('Depletion voltage found to be:    {:.1f} V'.format(deplV))
            print('Capacitance at depletion voltage: {:.4f} fC'.format(deplC*pow(10,15)))
            print('#############################')
            deplVs[i]=deplV
            capCs[i]=deplC
            
        elif args.measure[0]=='cv_b':
            deplV,deplC=deplVoltageRange(axs,data1,5,30,colors[i])
            print('#############################')
            print( perm )
            print('Depletion voltage found to be:    {:.1f} V'.format(deplV))
            print('Capacitance at depletion voltage: {:.4f} fC'.format(deplC*pow(10,15)))
            print('#############################')
            deplVs[i]=deplV
            capCs[i]=deplC

        
# draw all CV curves
allM=''
for m in args.measure:
    allM=allM+m
outName=allCurvesName(args.project, allM, 'pdf')
print(outName)

if len(args.measure)>1:
    axs[0].legend(loc='center left', bbox_to_anchor=(1, 0.5), fancybox=True)
    axs[len(args.measure)-1].set_xlabel('|V|')
else:
    if args.log:
        axs.set_yscale('log')
    axs.legend(loc='center left', bbox_to_anchor=(1, 0.5), fancybox=True)
    
plt.subplots_adjust(right=0.7)
fig.savefig(outName)
