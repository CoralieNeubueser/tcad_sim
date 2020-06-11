from utils import *

# draw hit maps for trans_4 measurements                                                                                                                                                                            
def drawMap(trans, times, vecCCEs, pitch, posX, posZ, scale, plotOutName, strps):

    print('Particle impinges at: ', posX, posZ)

    timeBin=math.floor(len(times)/10.)
    # sample time in 10
    for t in range(1,10):
        timeValue=int(0)
        realTime=t*timeBin
        # for last time bin, use the highest entry
        if t==9:
            timeValue=int(times[len(times)-1])
            realTime=len(times)-1
        else:
            timeValue=int(times[realTime])
            
        outName = plotOutName.replace('map_','map_'+str(timeValue)+'ns_')
        matrix_X = 0
        matrix_Y = 0

        # draw map in 4x4 if --scaleLET 4
        if scale==4 and not strps:
            matrix_X = 4
            matrix_Y = 4
            arrX=[-pitch,0,pitch,2*pitch]
            arrY=[2*pitch,pitch,0,-pitch]
            arrXYZ=[[0 for x in range(4)] for y in range(4)]
            for pixX in range(0,4):
                for pixY in range(0,4):
                    weight=0
                    if (pixX==0 and pixY==0) or (pixX==3 and pixY==3) or (pixX==0 and pixY==3) or (pixX==3 and pixY==0):
                        weight=vecCCEs[4][realTime]
                    elif (pixX==1 or pixX==2) and (pixY==2 or pixY==1):
                        weight=vecCCEs[1][realTime]
                    elif (pixX==1 or pixX==2):
                        weight=vecCCEs[2][realTime]
                    else:
                        weight=vecCCEs[3][realTime]

                    arrXYZ[pixY][pixX]=weight*100./4.

        elif scale==4 and strps:
            matrix = 5
            arrX=[20,10,0,10,20] 
            arrY=[0]
            arrXYZ=[[0 for x in range(0,5)] for y in range(0,1)]                                        
            for pixX in range(0,5):
                for pixY in range(0,1):                                                                 
                    weight=0                                                                            
                    if (pixX==0 and pixY==0) or (pixX==4 and pixY==0):                                  
                        weight=vecCCEs[3][realTime]                                                       
                    elif (pixX==1 or pixX==3) and (pixY==0):                                            
                        weight=vecCCEs[2][realTime]                                                       
                    else:                                                                               
                        weight=vecCCEs[1][realTime]                                                       
                    arrXYZ[pixY][pixX]=weight*100./4.

        elif scale==2 and not strps:
            # draw map in 3x4 if --scaleLET 4
            matrix_X = 4
            matrix_Y = 3
            arrX=[-pitch,0,pitch,2*pitch]
            arrY=[pitch,0,-pitch]
            arrXYZ=[[0 for x in range(4)] for y in range(3)]
            for pixX in range(0,4):
                for pixY in range(0,3):
                    weight=0
                    if (pixX==1 or pixX==2) and pixY==1:
                        weight=vecCCEs[1][realTime]
                    elif (pixX==0 and pixY==0) or (pixX==3 and pixY==2) or (pixX==0 and pixY==2) or (pixX==3 and pixY==0):
                        weight=vecCCEs[4][realTime]
                    elif (pixX==0 and pixY==1) or (pixX==3 and pixY==1):
                        weight=vecCCEs[3][realTime]/2.
                    else:
                        weight=vecCCEs[2][realTime]/2.
                    arrXYZ[pixY][pixX]=weight*100./2.

                    # draw map in 2x2 if --scaleLET 1 and non-symmetric posX/posZ
        elif scale==1 and (posX!=posZ or posX>pitch/2.) and not strps:
            matrix_X = 2
            matrix_Y = 2
            arrX=[0,pitch]
            arrY=[0,-pitch]
            arrXYZ=[[0 for x in range(matrix_X)] for y in range(matrix_Y)]
            for pixX in range(0,matrix_X):
                for pixY in range(0,matrix_Y):
                    weight=0
                    if (pixX==1 and pixY==1):
                        weight=vecCCEs[4][realTime]
                    elif (pixX==1 and not pixY==1):
                        weight=vecCCEs[2][realTime]
                    elif (pixY==1 and not pixX==1):
                        weight=vecCCEs[3][realTime]
                    else:
                        weight=vecCCEs[1][realTime]
                    arrXYZ[pixX][pixY]=weight*100.

            # draw map in 3x3 if --scaleLET 1
        elif scale==1 and not strps:
            matrix_X = 3
            matrix_Y = 3
            arrX=[-pitch,0,pitch]
            arrY=[pitch,0,-pitch]
            arrXYZ=[[0 for x in range(3)] for y in range(3)]
            for pixX in range(0,3):
                for pixY in range(0,3):
                    weight=0
                    if (pixX==1 and pixY==1):
                        weight=vecCCEs[1][realTime]
                    elif (pixX==1 and not pixY==1):
                        weight=vecCCEs[2][realTime]/2.
                    elif (pixY==1 and not pixX==1):
                        weight=vecCCEs[3][realTime]/2.
                    else:
                        weight=vecCCEs[4][realTime]/4.
                    arrXYZ[pixX][pixY]=weight*100.

        fig, ax = plt.subplots()
        im = ax.imshow(arrXYZ, cmap='viridis', vmin=0, vmax=int(100/float(scale)))
        ax.set_xticks(np.arange(matrix_X))
        ax.set_yticks(np.arange(matrix_Y))
        # ... and label them with the respective list entries
        ax.set_xticklabels(arrX)
        ax.set_yticklabels(arrY)                                                                                                                                                                                     
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
        x = matrix_X/2. - (1-posX/pitch)
        y = matrix_Y/2. - (1-posZ/pitch)
        if posX==0:
            x = matrix_X/2. - 0.5
        if posZ==0:
            y = matrix_Y/2. - 0.5
        if (posX!=posZ or posX>pitch/2.) and scale==1:
            x = - matrix_X/4. + posX/pitch
            y = - matrix_Y/4. + posZ/pitch
            
        print(outName)
        ax.scatter(x,y,color='r')
        fig.tight_layout()
        fig.savefig(outName)

 
