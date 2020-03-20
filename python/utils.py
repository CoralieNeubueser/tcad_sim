import os, sys, argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy.stats import linregress
from scipy import integrate
import scipy.optimize
import math

# if element is found it returns True else returns False
def find_element_in_list(element, list_element):
    try:
        index_element = list_element.index(element)
        return True
    except ValueError:
        return False

def getIntegral(y, x): #, xMin, xMax):
    integral=np.trapz(y, x=x)
    return integral

def drawVoltagePoint(axs,parX,parY,col):
    axs.plot(parX, parY, color=col,marker='*')
    
def drawVoltageLine(axs,parX,col):
    arrY=np.linspace(axs.get_ylim()[0],axs.get_ylim()[1],100)
    arrX=linFunction(arrY,float(parX))
    axs.plot(arrX, arrY, color=col, linestyle=':')

def linFit(x,y):
    # fit of shape x+a
    fitfunc=lambda params, x: params[0] + x * params[1]
    errfunc=lambda p,x,y: fitfunc(p, x) -y
    init_a=0.5
    init_b=1.
    init_arr=[init_a,init_b]
    p1,success=scipy.optimize.leastsq(errfunc,init_arr, args=(x,y))
    f=fitfunc(p1,x)
    return p1,f

def linFunction(x,a):
    return a + x*0

def deplVoltage(ax,dat,*col):
    
    x = np.array(-dat.X)
    y = np.array(dat.Y)
    
    # get slope of your data                                          
    dif = np.diff(y) / np.diff(x)
    
    # determine the change of the slope                               
    difdif = np.diff(dif)
    
    # define a threshold for the allowed change of the slope          
    threshold = difdif[5]/100
    
    # get indices where the diff returns value larger than a threshold
    indNZ = np.where(abs(difdif) > threshold)[0]
    
    # this makes plotting easier and avoids a couple of if clauses
    indNZ += 1
    indNZ = np.append(indNZ, len(x))
    indNZ = np.insert(indNZ, 0, 0)

    #store lin functions                               
    f=[None]*0
    xran=[None]*0
    yran=[None]*0
    cap=[None]*0

    trials=10
    
    while len(f)<2 and trials>1:
        for indi, ind in enumerate(indNZ):
            if ind < len(x):
                slope, intercept, r_value, p_value, std_err = linregress(x[ind:indNZ[indi+1]], y[ind:indNZ[indi+1]])
                if not math.isnan(slope):
                    # fill lin fits to lists
                    f.append(slope * x + intercept)
                    xran.append(x[ind:indNZ[indi+1]])
                    yran.append(slope * x[ind:indNZ[indi+1]] + intercept)
                    cap.append(intercept)
        
        if len(f)<2:
            print('Found only {} linear fits.. reduce threshold by half.'.format(len(f)))
            threshold = threshold/2.
            print(threshold)
            # reset index and clear list of linear fits
            indNZ = np.where(abs(difdif) > threshold)[0]
            indNZ += 1
            indNZ = np.append(indNZ, len(x))
            indNZ = np.insert(indNZ, 0, 0)
            f.clear()
            xran.clear()
            yran.clear()
            trials -= 1

    capDepl=cap[len(cap)-1]
    idx=np.array([0])
    # find intersection of last and second to last linear functions   
    for ifunc,func in enumerate(f):
        # draw found fits
        if len(col)==1:
            ax.plot(xran[ifunc], yran[ifunc], color=col[0])
        else:
            ax.plot(xran[ifunc], yran[ifunc], color=col[0], linestyle=col[1])

        if ifunc!=len(f)-2:
            continue
        # calculate intersection of last and second last fit
        idx = np.argwhere(np.diff(np.sign(np.array(func) - np.array(f[ifunc+1])))).flatten()
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
    threshold = abs(difdif[0]/10.)

    # get indices where the diff returns value larger than a threshold
    indNZ = np.where(abs(difdif) > threshold)[0]

    # this makes plotting easier and avoids a couple of if clauses
    indNZ += 1
    indNZ = np.append(indNZ, len(x))
    indNZ = np.insert(indNZ, 0, 0)

    # store lin functions, ranges, and capacitances
    f=[None]*0
    xran=[None]*0
    yran=[None]*0
    cap=[None]*0

    trials=10

    while len(f)<2 and trials>1:
        for indi, ind in enumerate(indNZ):
            if ind < len(x):
                slope, intercept, r_value, p_value, std_err = linregress(x[ind:indNZ[indi+1]], y[ind:indNZ[indi+1]])
                if not math.isnan(slope):
                    # fill lin fits to lists
                    f.append(slope * x + intercept)
                    xran.append(x[ind:indNZ[indi+1]])
                    yran.append(slope * x[ind:indNZ[indi+1]] + intercept)
                    cap.append(intercept)

        if len(f)<2:
            if trials>2:
                print('Found only {} linear fits.. reduce threshold by half.'.format(len(f)))
                threshold = threshold/2.
                print(threshold)
            else:
                print('Found only {} linear fits.. last try, reduce threshold to minimum.'.format(len(f)))
                threshold = abs(difdif.min())
                print(threshold)
            # reset index and clear list of linear fits
            indNZ = np.where(abs(difdif) > threshold)[0]
            indNZ += 1
            indNZ = np.append(indNZ, len(x))
            indNZ = np.insert(indNZ, 0, 0)
            f.clear()
            xran.clear()
            yran.clear()
            cap.clear()
            trials -= 1
            
    idx=np.array([0])
    print ("Found {} linear fits. ".format(len(f)))
    # find intersection of last and second to last linear functions
    for ifunc,func in enumerate(f):
        # draw found fits
        if len(col)==1:
            ax.plot(xran[ifunc], yran[ifunc], color='black') #col[0])
        else:
            ax.plot(xran[ifunc], yran[ifunc], color=col[0], linestyle=col[1])
        if ifunc!=len(f)-1:
            continue
        # find intersection of last and second last fit
        idx = np.argwhere(np.diff(np.sign(np.array(func) - np.array(f[ifunc-1])))).flatten()
        if not idx:
            print ("Find intersection between last and x to last fit..")
            for ifunctions in range(1,len(f)):
                idx = np.argwhere(np.diff(np.sign(np.array(func) - np.array(f[len(f)-ifunctions])))).flatten()
                print (idx)
        ax.plot(x[idx], func[idx], color=col[0], marker='*')

    if len(f)<1:
        print("No fits found.. returns Vdpl=0.")
        return 0., 0.
    elif len(idx)<1:
        print("No intersection found.. returns Vdpl=0.")
        return 0., 0.
    else:
        capDepl=cap[len(cap)-1]
        # returns depletion voltag and capacitance above depletion
        return float(x[idx[0]]), float(capDepl)

def punchThrough(ax,datX,datY,yMax,*col):

    x_noCut = np.array(datX)
    y_noCut = np.array(datY)
    x1 = x_noCut[(x_noCut > float(2)) & (y_noCut < float(yMax))]
    y1 = y_noCut[(x_noCut > float(2)) & (y_noCut < float(yMax))]

    # get slope of your data
    dif = np.diff(y1) / np.diff(x1)
    
    # determine the change of the slope
    difdif = np.diff(dif)

    # define a threshold for the allowed change of the slope
    thresholdLow = difdif[5]/100
    thresholdHigh = difdif[5]

    # get indices where the diff returns value larger than a threshold
    indNZLow = np.where(abs(difdif) > abs(thresholdLow))[0]
    indNZHigh = np.where(abs(difdif) > abs(thresholdHigh))[0]

    # this makes plotting easier and avoids a couple of if clauses
    indNZLow += 1
    indNZLow = np.append(indNZLow, len(x1))
    indNZLow = np.insert(indNZLow, 0, 0)
    indNZHigh += 1
    indNZHigh = np.append(indNZHigh, len(x1))
    indNZHigh = np.insert(indNZHigh, 0, 0)

    #store lin functions                                    
    f=[None]*0
    xran=[None]*0
    yran=[None]*0
    Ipt=[None]*0

    trials=10

    while len(f)<2 and trials>1:
        for indi, ind in enumerate(indNZLow):
            if ind < len(x1):
                slope, intercept, r_value, p_value, std_err = linregress(x1[ind:indNZLow[indi+1]], y1[ind:indNZLow[indi+1]])
                #err, function=linFit(x[ind:indNZ[indi+1]], y[ind:indNZ[indi+1]])
                #print(err)
                #print(function)
                if not math.isnan(slope):
                    # fill lin fits to lists
                    f.append(slope * x1 + intercept)
                    xran.append(x1[ind:indNZLow[indi+1]])
                    yran.append(slope * x1[ind:indNZLow[indi+1]] + intercept)
                    Ipt.append(intercept)
                    indRm = np.where(indNZHigh < indNZLow[ind+1])
                    np.delete(indNZHigh, indRm)
                    print('Found first fit.. \n')
                    break
                    

        for indi, ind in enumerate(indNZHigh):
            if ind < len(x1):
                slope, intercept, r_value, p_value, std_err = linregress(x1[ind:indNZHigh[indi+1]], y1[ind:indNZHigh[indi+1]])
                if not math.isnan(slope):
                    # fill lin fits to lists 
                    f.append(slope * x1 + intercept)
                    xran.append(x1[ind:indNZHigh[indi+1]])
                    yran.append(slope * x1[ind:indNZHigh[indi+1]] + intercept)
                    Ipt.append(intercept)
                    print('Found second fit.. \n')
                    #break

        if len(f)<2:
            print('Found only {} linear fits.. reduce threshold by half.'.format(len(f)))
            threshold = threshold/2.
            print(threshold)
            # reset index and clear list of linear fits
            indNZLow = np.where(abs(difdif) > abs(threshold))[0]
            indNZLow += 1
            indNZLow = np.append(indNZLow, len(x1))
            indNZLow = np.insert(indNZLow, 0, 0)
            f.clear()
            xran.clear()
            yran.clear()
            Ipt.clear()
            trials -= 1
            
    if len(Ipt)==0:
        print("Could not find 2 or more linear fits.")
        return 0.,0.
        quit()

    iDepl=Ipt[len(Ipt)-1]
    idx=np.array([0])

    # find intersection of first and second linear functions
    for ifunc,func in enumerate(f):
        # draw found fits
        if ifunc==0 or ifunc==len(f)-1:
            if len(col)==1:
                ax.plot(xran[ifunc], yran[ifunc], color=col[0])
            else:
                ax.plot(xran[ifunc], yran[ifunc], color=col[0], linestyle=col[1])
        
        if ifunc!=0:
            continue
        
        idx = np.argwhere(np.diff(np.sign(np.array(func) - np.array(f[len(f)-1])))).flatten()
        if not idx:
            for ifunctions in range(1,len(f)):
                idx = np.argwhere(np.diff(np.sign(np.array(func) - np.array(f[len(f)-ifunctions])))).flatten()

        curr_pt=np.linspace(ax.get_ylim()[0],ax.get_ylim()[1],100)
        print(float(x1[idx]))
        vol_pt=linFunction(curr_pt,float(x1[idx]))
        ax.plot(vol_pt, curr_pt, color=col[0], linestyle=':')
    
    if len(idx)<1:
        print("No intersection found.. returns Vdpl=0.")
        return 0., iDepl
    else:
        # returns depletion voltag and current
        return float(x1[idx[0]]), float(iDepl)


def drawGraph(axis,arr1,arr2,col,la):
    axis.plot(arr1,arr2, color=col,marker=',', label=la)

def drawGraphLines(axis,arr1,arr2,col,linestyle,la):
    axis.plot(arr1,arr2, color=col,marker=',', linestyle=linestyle, label=la)

def drawMultiGraphLines(axis,arr1,arr2,arr3,arr4,arr5,linestyle):
    axis.plot(arr1,arr2, color='black',marker=',', linestyle=linestyle, label="Ntop_0_0")
    axis.plot(arr1,arr3, color='red',marker=',', linestyle=linestyle, label="Ntop_0_1")
    axis.plot(arr1,arr4, color='blue',marker=',', linestyle=linestyle, label="Ntop_1_0")
    axis.plot(arr1,arr5, color='orange',marker=',', linestyle=linestyle, label="Ntop_1_1")

def csvFileName(project, measure, pars):
    home=os.getcwd()+"/DB/"
    csvName=home+project+"/tmp/"+measure
    csvName=csvName+"_"+str(pars)
    return csvName+".csv"

def allCurvesName(project, measure, op, form):
    home=os.getcwd()+"/DB/"
    name=home+project+"/tmp/"+measure
    return name+op+"all."+str(form)

def drawCCE(axis,arr1,arr2,norm,col,linestyle,la):
    eff=np.zeros(len(arr2))
    current=np.array(arr2) # A
    time=np.array(arr1) # s
    
    for it,t in enumerate(time):
        dt = t-time[it-1]
        if it==0:
            dt=time[it+1]-t
            eff[it] = current[it]*dt*pow(10,12)/norm
            continue
        # convert to pC and normalise  
        eff[it] = eff[it-1] + current[it]*dt*pow(10,12)/norm 
    # time in ns
    axis.plot(time*pow(10,9),eff,color=col,marker=',',linestyle=linestyle,label=la)
    return eff

def getTime(vecTime,vecCCEs,perc):
    time = np.array(vecTime)
    cces = np.array(vecCCEs)
    maxCCE = float(vecCCEs[len(vecCCEs)-1])
    ccePerc = maxCCE*perc/100.
    print("{}% are in absolut values: {:.2f}".format(perc, ccePerc))
    timesWithPerc = time[cces > ccePerc]
    if len(timesWithPerc)>1:
        return int(timesWithPerc[0])
    else:
        return int(timesWithPerc[0])

def drawMultiCCE(axis,arr1,arr2,arr3,arr4,arr5,norm,linestyle):
    eff1=np.zeros(len(arr2))
    eff2=np.zeros(len(arr3))
    eff3=np.zeros(len(arr4))
    eff4=np.zeros(len(arr5))
    current1=np.array(arr2) # A                 
    # print(current1)
    current2=np.array(arr3) # A
    current3=np.array(arr4) # A
    current4=np.array(arr5) # A
    time=np.array(arr1) # s              
    # print(time)
    for it,t in enumerate(time):
        dt = t-time[it-1]
        if it==0:
            dt=t
            eff1[it] = current1[it]*dt*pow(10,12)/norm
            eff2[it] = current2[it]*dt*pow(10,12)/norm
            eff3[it] = current3[it]*dt*pow(10,12)/norm
            eff4[it] = current4[it]*dt*pow(10,12)/norm
            continue
        # convert to pC and normalise  
        eff1[it] = eff1[it-1] + (current1[it]*dt*pow(10,12))/norm
        #print(eff1[it])
        eff2[it] = eff2[it-1] + (current2[it]*dt*pow(10,12))/norm
        eff3[it] = eff3[it-1] + (current3[it]*dt*pow(10,12))/norm
        eff4[it] = eff4[it-1] + (current4[it]*dt*pow(10,12))/norm
    # time in ns
    axis.plot(time*pow(10,9),eff1,color='black',marker=',',linestyle=linestyle,label="Ntop_0_0")
    axis.plot(time*pow(10,9),eff2,color='red',marker=',',linestyle=linestyle,label="Ntop_0_1")
    axis.plot(time*pow(10,9),eff3,color='blue',marker=',',linestyle=linestyle,label="Ntop_1_0")
    axis.plot(time*pow(10,9),eff4,color='orange',marker=',',linestyle=linestyle,label="Ntop_1_1")
    
    return eff1, eff2, eff3, eff4
