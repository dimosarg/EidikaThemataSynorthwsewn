import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def kmhtoms(val):
    valtoms=val*(1000)/3600
    return valtoms

#Reading the excel file
txtfile=pd.read_excel('C:\\Users\\dimos\\Desktop\\MyDesktopFolders\\Auth\\AuthRepos\\EidikaThemataSynorth\\Askisi2\\askisi2.xlsx')

#Split of the excel file
times=txtfile['t'].to_numpy()
xvals=txtfile['x'].to_numpy(dtype='float')
yvals=txtfile['y'].to_numpy(dtype='float')

#Creation of basic matrices (A, Cv and Cw)
alpha=np.array([[1,0,0,0],[0,1,0,0]])
alphatrans=np.transpose(alpha)

cv=np.array([[100,0],[0,100]])

cwbottomvals=kmhtoms(81)

cw= np.array([[2500,0,0,0],[0,2500,0,0],[0,0,cwbottomvals,0],[0,0,0,cwbottomvals]])

#Preparations of making the X+, X-, Cx+ and Cx-
xplus=np.zeros([len(xvals),4])
xminus=np.zeros([len(xvals),4])
cxplus=np.zeros([len(xvals),4,4])
cxminus=np.zeros([len(xvals),4,4])

xplus[0]=np.array([580.3,722.3,kmhtoms(31.5),kmhtoms(35.3)])
cxplus[0]=np.array([[2500,0,0,0],[0,2500,0,0],[0,0,cwbottomvals,0],[0,0,0,cwbottomvals]])

yk=np.zeros([len(xvals),2])

#Creation of observations matrix of GNSS coordinates
for i in range(len(xvals)):
    yk[i][0]=xvals[i]
    yk[i][1]=yvals[i]

#Main loop for creation of the corrected coordinates
for i in range(1,len(xvals)):
    timediff=times[i]-times[i-1]
    fmat=np.array([[1,0,timediff,0],[0,1,0,timediff],[0,0,1,0],[0,0,0,1]])
    xminus[i]=np.matmul(fmat,xplus[i-1])
    cxminus[i]=np.matmul(np.matmul(fmat,cxplus[i-1]),np.transpose(fmat))+cw
    cxplus[i]=np.linalg.inv(np.linalg.inv(cxminus[i])+np.matmul(np.matmul(alphatrans,cv),alpha))
    kprofit=np.matmul(np.matmul(cxplus[i],alphatrans),cv)
    xplusoros1=yk[i]-np.matmul(alpha,xminus[i])
    xplus[i]=xminus[i]+np.matmul(kprofit,xplusoros1)

xplusdf=pd.DataFrame(xplus)
xminusdf=pd.DataFrame(xminus)

xminusxvals=xminusdf[0]
xminusyvals=xminusdf[1]
xplusxvals=xplusdf[0]
xplusyvals=xplusdf[1]

#Differences of observations to minus predictions and plus predictions
#This is used as measure of accuracy between the two different types of measures
xminusobsdif=np.zeros(len(xvals))
xplusobsdif=np.zeros(len(xvals))

for i in range(len(xvals)):
    xminusobsdif[i]=np.sqrt((xminusxvals[i]-xvals[i])**2+(xminusyvals[i]-yvals[i])**2)
    xplusobsdif[i]=np.sqrt((xplusxvals[i]-xvals[i])**2+(xplusyvals[i]-yvals[i])**2)

meandistminus=np.sum(xminusobsdif)/len(xvals)
meandistplus=np.sum(xplusobsdif)/len(xvals)

print('The mean distance between minus values and observations')
print(meandistminus)
print('The mean distance between plus values and observations')
print(meandistplus)

fig1=plt.figure(1)
plt.plot(xvals,yvals, label='Actual observations')
plt.plot(xminusxvals,xminusyvals, color='r', label='X- predictions')
plt.plot(xplusxvals,xplusyvals, color='g', label='X+ predictions')
plt.legend()
plt.title("Graph of observed and corrected paths")

plt.show()