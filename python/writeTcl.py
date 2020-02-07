import glob, os, sys, argparse
import numpy as np
from utils import csvFileName 

parser = argparse.ArgumentParser()

parser.add_argument('--project', type=str, default='ARCADIA25um_surfaceDamage', help='Define patht to project.')
parser.add_argument('--cv', action='store_true', help='Specify if measurement is cv.')
parser.add_argument('--iv', action='store_true', help='Specify if measurement is iv.')
parser.add_argument('--iv_b', action='store_true', help='Specify if measurement is iv.')
parser.add_argument('-pF', '--parFloat', type=float, nargs='+', help='Give parameters as specified in tcad project.')
parser.add_argument('-pI', '--parInt', type=int, nargs='+', help='Give parameters as specified in tcad project.')
parser.add_argument('--run', action='store_true', help='Specify if you want to execute the tcl file.')

args,_=parser.parse_known_args()


# prepare input file name following the structure:
# cv_ac_[...]_ac_des.plt
# iv_[...].plt
# of the tcad outpur files. this needs to be specified in the cmd files.
# the free parameters are given as floats or integers, order matters!, first float then int.
home=os.getcwd()+"/DB/"
measure=''
nameBegin=''
nameEnd=''
figName=''

if args.cv:
    measure='cv'
    nameBegin="cv_ac"
    nameEnd="_ac_des.plt"
elif args.iv:
    measure='iv'
    nameBegin="iv"
    nameEnd=".plt"
elif args.iv_b:
    measure='iv_b'
    nameBegin="iv"
    nameEnd=".plt"

figName=nameBegin
inFileName=home+args.project+"/"+nameBegin
csvFileName=csvFileName(args.project, measure, args.parFloat, args.parInt)

# check if temporary path exist, if not create
workDir=home+args.project+"/tmp/"
if not os.path.isdir(workDir):
    print("Create output directory /tmp/")
    os.system('mkdir '+home+args.project+"/tmp/")

for par in args.parFloat:
    inFileName=inFileName+"_"+str(par)
    figName=figName+"_"+str(par)
for par in args.parInt:
    inFileName=inFileName+"_"+str(par)
    figName=figName+"_"+str(par)

inFileName=inFileName+nameEnd
tclFileName=csvFileName+".tcl"
figName=figName+nameEnd.replace(".plt","")

#Write tcl file
newFile=open(tclFileName, "w")
print(tclFileName)

newFile.write('load_file {}\n'.format(inFileName))
newFile.write('create_plot -1d\n')
newFile.write('select_plots {Plot_1}\n')
newFile.write('#-> Plot_1\n')

if measure=='cv':
    newFile.write('create_curve -plot Plot_1 -dataset {'+str(figName)+'} -axisX v(Pbot) -axisY c(Ntop,Ntop)\n')

elif measure=='iv':
    newFile.write('create_curve -plot Plot_1 -dataset {'+str(figName)+'} -axisX {Pbot OuterVoltage} -axisY {Ntop TotalCurrent}\n')

elif measure=='iv_b':
    newFile.write('create_curve -plot Plot_1 -dataset {'+str(figName)+'} -axisX {Pbot OuterVoltage} -axisY {Ptop TotalCurrent}\n')

newFile.write('#-> Curve_1\n')
newFile.write('export_curves {Curve_1} -plot Plot_1 -filename '+str(csvFileName)+' -format csv -overwrite\n')
newFile.close()

# if you specified that the tcl file is also executed..
if args.run:
    cmd='svisual -b '+str(tclFileName)
    print(cmd)
    os.system(cmd)
    print('Outfile saved as: '+csvFileName)
