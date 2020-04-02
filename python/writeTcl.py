import glob, os, sys, argparse
import numpy as np
from utils import csvFileName 

parser = argparse.ArgumentParser()

parser.add_argument('--project', type=str, default='ARCADIA25um_surfaceDamage', help='Define patht to project.')
parser.add_argument('--cv', action='store_true', help='Specify if measurement is cv.')
parser.add_argument('--iv', action='store_true', help='Specify if measurement is iv.')
parser.add_argument('--iv_p', action='store_true', help='Specify if measurement is iv on pwell.')
parser.add_argument('--iv_b', action='store_true', help='Specify if measurement is iv.')
parser.add_argument('--cv_b', action='store_true', help='Specify if measurement is cv.')
parser.add_argument('--tran', action='store_true', help='Specify if measurement is particle.')
parser.add_argument('--tran_3', action='store_true', help='Specify if measurement is particle.')
parser.add_argument('--tran_4', action='store_true', help='Specify if measurement is particle.')
parser.add_argument('--tran_7', action='store_true', help='Specify if measurement is particle.')
parser.add_argument('--charge', action='store_true', help='Specify if measurement is particle.')
parser.add_argument('-pS', '--parStr', action='append', default=[], help='Give parameters as specified in tcad project.')
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
elif args.iv_p:
    measure='iv_p'
    nameBegin="iv"
    nameEnd=".plt"
elif args.iv_b:
    measure='iv_b'
    nameBegin="iv"
    nameEnd=".plt"
elif args.cv_b:
    measure='cv_b'
    nameBegin="cv_ac"
    nameEnd="_ac_des.plt"
elif args.tran:
    measure='tran'
    nameBegin="tran"
    nameEnd=".plt"
elif args.tran_3:
    measure='tran_3'
    nameBegin="tran"
    nameEnd=".plt"
elif args.tran_4:
    measure='tran_4'
    nameBegin="tran"
    nameEnd=".plt"
elif args.tran_7:
    measure='tran_7'
    nameBegin="tran"
    nameEnd=".plt"
elif args.charge:
    measure='charge'
    nameBegin="tran"
    nameEnd=".plt"

figName=nameBegin
inFileName=home+args.project+"/"+nameBegin
options=str()
for ipar,par in enumerate(args.parStr):
    options+=str(par)
    if ipar<(len(args.parStr)-1):
        options+='_'
csvFile=csvFileName(args.project, measure, options)

# check if temporary path exist, if not create
workDir=home+args.project+"/tmp/"
if not os.path.isdir(workDir):
    print("Create output directory /tmp/")
    os.system('mkdir '+home+args.project+"/tmp/")
if os.path.isfile(csvFile):
    print("CSV file already exists.")
    os.system('rm '+csvFile)
    args.run=True
# set parameters in file names
for par in args.parStr:
    inFileName+="_"+str(par)
    figName+="_"+str(par)

inFileName=inFileName+nameEnd
tclFileName=csvFile+".tcl"
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

elif measure=='iv_p':
    newFile.write('create_curve -plot Plot_1 -dataset {'+str(figName)+'} -axisX {Pbot OuterVoltage} -axisY {Ptop TotalCurrent}\n')

elif measure=='iv_b':
    newFile.write('create_curve -plot Plot_1 -dataset {'+str(figName)+'} -axisX {Pbot OuterVoltage} -axisY {Pbot TotalCurrent}\n')

elif measure=='cv_b':
    newFile.write('create_curve -plot Plot_1 -dataset {'+str(figName)+'} -axisX v(Pbot) -axisY c(Ptop,Ptop)\n')

elif measure=='tran':
    newFile.write('create_curve -plot Plot_1 -dataset {'+str(figName)+'} -axisX time -axisY {Ntop TotalCurrent}\n')

elif measure=='charge':
    newFile.write('create_curve -plot Plot_1 -dataset {'+str(figName)+'} -axisX time -axisY {Ntop Charge}\n')

if measure=='tran_4':
    newFile.write('create_curve -plot Plot_1 -dataset {'+str(figName)+'} -axisX time -axisY {Ntop_0_0 TotalCurrent}\n')
    newFile.write('create_curve -plot Plot_1 -dataset {'+str(figName)+'} -axisX time -axisY {Ntop_0_1 TotalCurrent}\n')
    newFile.write('create_curve -plot Plot_1 -dataset {'+str(figName)+'} -axisX time -axisY {Ntop_1_0 TotalCurrent}\n')
    newFile.write('create_curve -plot Plot_1 -dataset {'+str(figName)+'} -axisX time -axisY {Ntop_1_1 TotalCurrent}\n')
    newFile.write('#-> Curve_1\n')
    newFile.write('export_curves {Curve_1 Curve_2 Curve_3 Curve_4} -plot Plot_1 -filename '+str(csvFile)+' -format csv -overwrite\n')

elif measure=='tran_3':
    newFile.write('create_curve -plot Plot_1 -dataset {'+str(figName)+'} -axisX time -axisY {Ntop1 TotalCurrent}\n')
    newFile.write('create_curve -plot Plot_1 -dataset {'+str(figName)+'} -axisX time -axisY {Ntop2 TotalCurrent}\n')
    newFile.write('create_curve -plot Plot_1 -dataset {'+str(figName)+'} -axisX time -axisY {Ntop3 TotalCurrent}\n')
    newFile.write('#-> Curve_1\n')
    newFile.write('export_curves {Curve_1 Curve_2 Curve_3} -plot Plot_1 -filename '+str(csvFile)+' -format csv -overwrite\n')

elif measure=='tran_7':
    newFile.write('create_curve -plot Plot_1 -dataset {'+str(figName)+'} -axisX time -axisY {Ntop1 TotalCurrent}\n')
    newFile.write('create_curve -plot Plot_1 -dataset {'+str(figName)+'} -axisX time -axisY {Ntop2 TotalCurrent}\n')
    newFile.write('create_curve -plot Plot_1 -dataset {'+str(figName)+'} -axisX time -axisY {Ntop3 TotalCurrent}\n')
    newFile.write('create_curve -plot Plot_1 -dataset {'+str(figName)+'} -axisX time -axisY {Ntop4 TotalCurrent}\n')
    newFile.write('create_curve -plot Plot_1 -dataset {'+str(figName)+'} -axisX time -axisY {Ntop5 TotalCurrent}\n')
    newFile.write('create_curve -plot Plot_1 -dataset {'+str(figName)+'} -axisX time -axisY {Ntop6 TotalCurrent}\n')
    newFile.write('create_curve -plot Plot_1 -dataset {'+str(figName)+'} -axisX time -axisY {Ntop7 TotalCurrent}\n')
    newFile.write('#-> Curve_1\n')
    newFile.write('export_curves {Curve_1 Curve_2 Curve_3 Curve_4 Curve_5 Curve_6 Curve_7} -plot Plot_1 -filename '+str(csvFile)+' -format csv -overwrite\n')

else:
    newFile.write('#-> Curve_1\n')
    newFile.write('export_curves {Curve_1} -plot Plot_1 -filename '+str(csvFile)+' -format csv -overwrite\n')

newFile.close()

# if you specified that the tcl file is also executed..
if args.run:
    cmd='svisual -b '+str(tclFileName)
    print(cmd)
    os.system(cmd)
    print('Outfile saved as: '+csvFile)
    os.system('rm '+str(tclFileName))
