import os, sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy.stats import linregress
import scipy.optimize
import math

def deplVoltage(ax,dat,*col):
    
    x = np.array(-dat.X)
    y = np.array(dat.Y)
    
    # get slope of your data                                          
    dif = np.diff(y) / np.diff(x)
    
    # determine the change of the slope                               
    difdif = np.diff(dif)
    
    # define a threshold for the allowed change of the slope          
    threshold = difdif[0]/10
    
    # get indices where the diff returns value larger than a threshold
    indNZ = np.where(abs(difdif) > threshold)[0]
    
    # this makes plotting easier and avoids a couple of if clauses
    indNZ += 1
    indNZ = np.append(indNZ, len(x))
    indNZ = np.insert(indNZ, 0, 0)

    #store lin functions                               
    f=[None]*0
    cap=[None]*0

    trials=10
    
    while len(f)<2 and trials>1:
        for indi, ind in enumerate(indNZ):
            if ind < len(x):
                slope, intercept, r_value, p_value, std_err = linregress(x[ind:indNZ[indi+1]], y[ind:indNZ[indi+1]])
                if not math.isnan(slope):
                    if len(col)==1:
                        ax.plot(x[ind:indNZ[indi+1]], slope * x[ind:indNZ[indi+1]] + intercept, color=col[0])
                    else:
                        ax.plot(x[ind:indNZ[indi+1]], slope * x[ind:indNZ[indi+1]] + intercept, color=col[0], linestyle=col[1])
                    # fill lin fits to lists
                    f.append(slope * x + intercept)
                    cap.append(intercept)
        
        if len(f)<2:
            print('Found only {} linear fits.. reduce threshold by half.'.format(len(f)))
            threshold = threshold*2.
            print(threshold)
            # reset index and clear list of linear fits
            indNZ = np.where(abs(difdif) > threshold)[0]
            indNZ += 1
            indNZ = np.append(indNZ, len(x))
            indNZ = np.insert(indNZ, 0, 0)
            f.clear()
            trials -= 1

    capDepl=cap[len(cap)-1]
    idx=np.array([0])
    # find intersection of last and second to last linear functions   
    for ifunc,func in enumerate(f):
        if ifunc!=len(f)-2:
            continue

        idx = np.argwhere(np.diff(np.sign(np.array(func) - np.array(f[ifunc+1])))).flatten()
        if len(col)==1:
            ax.plot(x[idx], func[idx], color=col[0], marker='*')
        else:
            ax.plot(x[idx], func[idx], color=col[0], marker='*')

    if len(idx)<1:
        print("No intersection found.. returns Vdpl=0.")
        return 0., capDepl
    else:
        # returns depletion voltag and capacitance above depletion    
        return float(x[idx[0]]), float(capDepl)



def deplVoltageRange(ax,dat,xMin,xMax,*col):

    x_noCut = np.array(-dat.X)
    y_noCut = np.array(dat.Y)
    x = x_noCut[(x_noCut > float(xMin)) & (x_noCut < float(xMax))]
    y = y_noCut[(x_noCut > float(xMin)) & (x_noCut < float(xMax))]

    # get slope of your data
    dif = np.diff(y) / np.diff(x)

    # determine the change of the slope
    difdif = np.diff(dif)

    # define a threshold for the allowed change of the slope
    threshold = difdif[0]/10

    # get indices where the diff returns value larger than a threshold
    indNZ = np.where(abs(difdif) > threshold)[0]

    # this makes plotting easier and avoids a couple of if clauses
    indNZ += 1
    indNZ = np.append(indNZ, len(x))
    indNZ = np.insert(indNZ, 0, 0)

    #store lin functions
    f=[None]*0
    cap=[None]*0

    trials=10

    while len(f)<2 and trials>1:
        for indi, ind in enumerate(indNZ):
            if ind < len(x):
                slope, intercept, r_value, p_value, std_err = linregress(x[ind:indNZ[indi+1]], y[ind:indNZ[indi+1]])
                if not math.isnan(slope):
                    if len(col)==1:
                        ax.plot(x[ind:indNZ[indi+1]], slope * x[ind:indNZ[indi+1]] + intercept, color=col[0])
                    else:
                        ax.plot(x[ind:indNZ[indi+1]], slope * x[ind:indNZ[indi+1]] + intercept, color=col[0], linestyle=col[1])
                    # fill lin fits to lists
                    f.append(slope * x + intercept)
                    cap.append(intercept)
        if len(f)<2:
            print('Found only {} linear fits.. reduce threshold by half.'.format(len(f)))
            threshold = threshold*2.
            print(threshold)
            # reset index and clear list of linear fits
            indNZ = np.where(abs(difdif) > threshold)[0]
            indNZ += 1
            indNZ = np.append(indNZ, len(x))
            indNZ = np.insert(indNZ, 0, 0)
            f.clear()
            trials -= 1
            
    capDepl=cap[len(cap)-1]
    idx=np.array([0])
    # find intersection of last and second to last linear functions
    for ifunc,func in enumerate(f):
        if ifunc!=len(f)-2:
            continue

        idx = np.argwhere(np.diff(np.sign(np.array(func) - np.array(f[ifunc+1])))).flatten()
        if len(col)==1:
            ax.plot(x[idx], func[idx], color=col[0], marker='*')
        else:
            ax.plot(x[idx], func[idx], color=col[0], marker='*')

    if len(idx)<1:
        print("No intersection found.. returns Vdpl=0.")
        return 0., capDepl
    else:
        # returns depletion voltag and capacitance above depletion
        return float(x[idx[0]]), float(capDepl)


def drawGraph(axis,arr1,arr2,col,la):
    axis.plot(arr1,arr2, color=col,marker=',', label=la)

def drawGraphLines(axis,arr1,arr2,col,linestyle,la):
    axis.plot(arr1,arr2, color=col,marker=',', linestyle=linestyle, label=la)

def csvFileName(project, measure, *pars):
    home=os.getcwd()+"/DB/"
    csvName=home+project+"/tmp/"+measure
    for par in pars:
        csvName=csvName+"_"+str(par[0])
    return csvName+".csv"

def allCurvesName(project, measure, form):
    home=os.getcwd()+"/DB/"
    name=home+project+"/tmp/"+measure
    return name+"_all."+str(form)
