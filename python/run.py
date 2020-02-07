import os, sys, argparse
from utils import * 
import pandas as pd
import numpy as np

parser = argparse.ArgumentParser()

parser.add_argument('--project', type=str, default='ARCADIA25um_surfaceDamage', help='Define patht to project.')
parser.add_argument('--writeCSV', action='store_true', help='Convert tcl to csv, if not already done.')
parser.add_argument('-m', '--measure', action='store', type=str, nargs='+', default=['cv','iv'], help='Define which plots you want to draw.', choices=['cv','iv','iv_b'])

args,_=parser.parse_known_args()

# pre-define the two paramters that you have tested
par1=[0.0, 0.5, 2.0, 4.25]
par2=[10, 100, 1000]

# produce csv files
if args.writeCSV:
    for p1 in par1:
        for p2 in par2:
            # write and run tcl files to store csv files in tmp/ for
            # CV ..
            os.system('python3 python/writeTcl.py --project '+str(args.project)+' --cv -pF '+str(p1)+' -pI '+str(p2)+' --run')
            # and IV.
            os.system('python3 python/writeTcl.py --project '+str(args.project)+' --iv -pF '+str(p1)+' -pI '+str(p2)+' --run')
            # and IV of bottom contact.      
            os.system('python3 python/writeTcl.py --project '+str(args.project)+' --iv_b -pF '+str(p1)+' -pI '+str(p2)+' --run')

# prepare for drawing
colors = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c',
          '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5',
          '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f',
          '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5' ]
mark=','
lines='-','--',':'

print(len(args.measure))
fig, axs = plt.subplots(len(args.measure),1, sharex=True, sharey=False) #, gridspec_kw={'hspace': 0})

i=0

# arrays of Vdpl and Cend
deplVs=np.zeros((len(par1),len(par2)), dtype=float)
capCs=np.zeros((len(par1),len(par2)), dtype=float)
endIs=np.zeros((len(par1),len(par2)), dtype=float)

# read csv files and analyse
for ip1,p1 in enumerate(par1):
    for ip2,p2 in enumerate(par2):

        f1=csvFileName(args.project, args.measure[0], [p1], [p2])
        
        data1 = pd.read_csv(f1, names=["X","Y"], skiprows=1)
        
        lab=str('p1='+str(p1)+', p2='+str(p2))

        if len(args.measure)>1:
            for im,m in enumerate(args.measure):
                f2=csvFileName(args.project, m, [p1], [p2])
                data2 = pd.read_csv(f2, names=["X","Y"], skiprows=1)
                
                drawGraphLines(axs[im],-data2.X, data2.Y,colors[ip1],lines[ip2],lab)
                
                if m=='cv':
                    deplV,deplC=deplVoltage(axs[im],data2,colors[ip1])

                    print('p1='+str(p1)+', p2='+str(p2))
                    print('Depletion voltage found to be:    {:.1f} V'.format(deplV))
                    print('Capacitance at depletion voltage: {:.4f} fC'.format(deplC*pow(10,15)))
                    deplVs[ip1][ip2]=deplV
                    capCs[ip1][ip2]=deplC

        else:
            drawGraphLines(axs,-data1.X, data1.Y,colors[ip1],lines[ip2],lab)
            if args.measure=='cv':
                deplV,deplC=deplVoltage(axs,data1,colors[ip1])
                print('p1='+str(p1)+', p2='+str(p2))
                print('Depletion voltage found to be:    {:.1f} V'.format(deplV))
                print('Capacitance at depletion voltage: {:.4f} fC'.format(deplC*pow(10,15)))
                deplVs[ip1][ip2]=deplV
                capCs[ip1][ip2]=deplC
        i=i+1

        
# draw all CV curves
allM=''
for m in args.measure:
    allM=allM+m
outName=allCurvesName(args.project, allM, 'pdf')
print(outName)

if len(args.measure)>1:
    #axs[len(args.measure)-1].set_yscale('log')
    axs[1].legend(loc='center left', bbox_to_anchor=(1, 0.5), fancybox=True)
    axs[len(args.measure)-1].set_xlabel('|V|')
    
else:
    axs.set_yscale('log')
    axs.legend(loc='center left', bbox_to_anchor=(1, 0.5), fancybox=True)
    axs.set_xlabel('|V|')
    axs.set_ylabel('C')

plt.subplots_adjust(right=0.7)
fig.savefig(outName)


        
