import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk

#Lhpsh dedomenwn apo arxeio excel me thn bibliothiki pandas (parakalw eisagete to dik;o sas path sto opoio tha balete to arxeio)
txtfile=pd.read_excel('C:\\Users\\dimos\\Desktop\\MyDesktopFolders\\Auth\\AuthRepos\\EidikaThemataSynorth\\Askhsh1\\LyshAskhsh1\\Askhsh1Dedomena.xlsx')

#diaxeirhsh dedomenwn kai dhmioyrgia array mesw ths bibliothikis numpy gia thn eykolh diaxeirhsh twn dedomenwn
timedataset= txtfile['xronos'].to_numpy(dtype='float')

#ypologismos twn hmeromhniwn me megalyterh akribeia
time=np.zeros(len(timedataset))

for i in range(len(timedataset)):
    time[i]=2010+(i/365)

bhta= txtfile['metrhseis'].to_numpy(dtype='float')
timepredict=np.array([2010.089, 2012.10, 2013.10], dtype='float')
c0=3600
akefalaio=862.2438

#ypologismos pinakwn sxediasmoy A kai A' antistoixa
alpha=np.zeros((731,4),dtype='float32')
alphatonos=np.zeros((3,4),dtype='float32')

for i in range(len(time)):
    alpha[i][0]=np.cos(2*np.pi*time[i])
    alpha[i][1]=np.sin(2*np.pi*time[i])
    alpha[i][2]=np.cos(4*np.pi*time[i])
    alpha[i][3]=np.sin(4*np.pi*time[i])

for i in range(len(timepredict)):
    alphatonos[i][0]=np.cos(2*np.pi*time[i])
    alphatonos[i][1]=np.sin(2*np.pi*time[i])
    alphatonos[i][2]=np.cos(4*np.pi*time[i])
    alphatonos[i][3]=np.sin(4*np.pi*time[i])

#dhmiourgeia dataframe gia pio eykolh katanohsh kai probolh twn dedomenwn
alphadf=pd.DataFrame(alpha)
alphatonosdf=pd.DataFrame(alphatonos)
print('Πινακας σχεδιασμου αλφα: ')
print(alphadf)

print('Πινακας σχεδιασμου προβλεπομενων τιμων αλφα')
print(alphatonosdf)

#dhmiourgia pinaka Cv
cv=np.zeros((731,731))

for i in range(len(timedataset)):
    cv[i][i]=1600

cvdf=pd.DataFrame(cv)
print('Πινακας συμμεταβλητοτήτων σφαλματων Cv: ')
print(cvdf)

#dhmiourgia pinaka Cs
cs=np.zeros((731,731))

for i in range(len(time)):
    for j in range(len(time)):
        timeij=abs((time[i]-time[j]))
        cs[i][j]=c0/((1+(akefalaio*(timeij**2)))**2)

csdf=pd.DataFrame(cs)
print('Πινακας συμμεταβλητοτήτων σηματος Cs: ')
print(csdf)

#dhmiourgia pinaka Cs' twn shmatwn
cstonos=np.zeros((3,3))

for i in range(len(timepredict)):
    for j in range(len(timepredict)):
        timeijtonos=abs((timepredict[i]-timepredict[j]))
        cstonos[i][j]=c0/((1+(akefalaio*(timeijtonos**2)))**2)

cstonosdf=pd.DataFrame(cstonos)
print('Πινακας συμμεταβλητοτήτων σηματος προβλεπομενων τιμων Cstonos: ')
print(cstonosdf)

#dhmiourgia pinaka Cs's
cstonoss=np.zeros((len(timepredict),len(time)))

for i in range(len(timepredict)):
    for j in range(len(time)):
        timeijlast=abs((timepredict[i]-time[j]))
        cstonoss[i][j]=c0/((1+(akefalaio*(timeijlast**2)))**2)

cstonossdf=pd.DataFrame(cstonoss)

print('Πινακας συμμεταβλητοτήτων σηματος με σηματα προβλεπομενων τιμων Cstonoss: ')
print(cstonossdf)

#ypologismos ypoloipwn pinakwn
mkefalaio= cvdf+csdf

xkapelooros1=np.linalg.inv(np.matmul((np.matmul(np.transpose(alphadf),np.linalg.inv(mkefalaio))),alpha))
xkapelooros2=np.matmul(np.matmul(np.transpose(alpha),np.linalg.inv(mkefalaio)),bhta)
xkapelo=np.matmul(xkapelooros1,xkapelooros2)
xkapelodf=pd.DataFrame(xkapelo)
print('Πινακας εκτιμημενων παραμετρων συναρτησης X^: ')
print(xkapelodf)

skapelooros1=np.matmul(csdf, np.linalg.inv(mkefalaio))
skapelooros2=bhta-np.matmul(alpha,xkapelo)
skapelo=np.matmul(skapelooros1,skapelooros2)
skapelodf=pd.DataFrame(skapelo)
print('Πινακας εκτιμημενων τιμών σηματος S^: ')
print(skapelodf)

vkapelooros1=np.matmul(cvdf, np.linalg.inv(mkefalaio))
vkapelooros2=bhta-np.matmul(alpha,xkapelo)
vkapelo=np.matmul(vkapelooros1,vkapelooros2)
vkapelodf=pd.DataFrame(vkapelo)
print('Πινακας εκτιμημενων σφαλματων παρατηρησεων: ')
print(vkapelodf)

stonoskapelooros1=np.matmul(cstonossdf, np.linalg.inv(mkefalaio))
stonoskapelooros2=bhta-np.matmul(alpha,xkapelo)
stonoskapelo=np.matmul(stonoskapelooros1,stonoskapelooros2)
stonoskapelodf=pd.DataFrame(stonoskapelo)
print('Πινακας εκτιμημενων τιμων προβλεπομενου σηματος: ')
print(stonoskapelodf)

#dhmioyrgia ektimhmenwn parathrhsewn 
ytonoskapelooros1=np.matmul(alphatonos,xkapelo)
ytonoskapelooros2=stonoskapelo

ytonoskapelo=ytonoskapelooros1+ytonoskapelooros2

ytonoskapelodf=pd.DataFrame(ytonoskapelo)

print('Πινακας εκτιμήσεων παρατηρήσεων προβλεπομενων σημειων: ')
print(ytonoskapelodf)

#dhmioyrgia synarthshs kyrias tashs twn parathrhsewn
synarthshx=np.zeros(len(time))

for i in range(len(time)):
    synarthshx[i]=xkapelo[0]*np.cos(2*np.pi*time[i])+xkapelo[1]*np.sin(2*np.pi*time[i])+xkapelo[2]*np.cos(4*np.pi*time[i])+xkapelo[3]+np.sin(4*np.pi*time[i])

synarthshxdf=pd.DataFrame(synarthshx)

#dhmiourgia synarthshs twn parathrhsewn plhn toy sfalmatos
xs=synarthshx+skapelo
xsdf=pd.DataFrame(xs)
print('Συναρτηση εκτιμημενων παρατηρησεων χωρις θορυβο: ')
print(xs)

#dhmiourgia synarthshs toy sfalmatos twn parathrhsewn me to shma 
signalvol=skapelo+vkapelo

#dhmiourgia synarthshs twn parathrhsewn xwris to shma
bhtavol=synarthshx+vkapelo

#dhmioyrgia pinaka y^
ykapelo=synarthshx+skapelo+vkapelo
ykapelodf=pd.DataFrame(ykapelo)
print('Εκτιμημενες παρατηρησεις y^: ')
print(ykapelodf)

#dhmiourgia pinaka sfalmatwn twn ektimhsewn twn syntelestwn (xkapelo)
cexkapelo=np.linalg.inv(np.matmul((np.matmul(np.transpose(alphadf),np.linalg.inv(mkefalaio))),alpha))
cexkapelodf=pd.DataFrame(cexkapelo)
print('Πινακας συμμεταβλητοτητων εκτιμημενων παραμετρων συναρτησης κυριας τασης: ')
print(cexkapelodf)

#dhmiourgia pinaka sfalmatwn twn ektimhsewn toy shmatos

mantestr=np.linalg.inv(mkefalaio)

cskapelooros1=np.matmul(cs,mantestr)
cskapelooros2=mkefalaio-(np.matmul(np.matmul(alpha,cexkapelo),np.transpose(alpha)))
cskapelooros3=np.matmul(mantestr,cs)

cskapelo=np.matmul(np.matmul(cskapelooros1,cskapelooros2),cskapelooros3)

ceskapelo=cs-cskapelo

print('Πινακας συμμεταβλητοτητων εκτιμημενων σηματων: ')
print(ceskapelo)

#dhmiourgia pinaka sfalmatwn twn ektimhsewn twn parathrhsewn (y^=Ax^+s^+v^)
cexes=-np.matmul((np.matmul(cexkapelo,np.transpose(alpha))),np.matmul(mantestr,cs))

ceykapelooros1=np.matmul(np.matmul(alpha,cexkapelo),np.transpose(alpha))
ceykapelooros2=ceskapelo
ceykapelooros3=-np.matmul(alpha,cexes)
ceykapelooros4=-np.transpose(np.matmul(alpha,cexes))

ceykapelo=ceykapelooros1+ceykapelooros2+ceykapelooros3+ceykapelooros4

print('Πινακας συμμεταβλητοτητων εκτιμημενων παρατηρησεων: ')
print(ceykapelo)

#dhmiourgia pinaka sfalmatwn twn ektimhsewn twn problepseon toy shmatos
cvtonos=np.zeros((3,3))
for i in range(len(cvtonos)):
    cvtonos[i][i]=1600

mtonos=cvtonos+cstonos

mtonosant=np.linalg.inv(mtonos)

cstonoskapelooros1=np.matmul(cstonos,mtonosant)
cstonoskapelooros2=mtonos-(np.matmul(np.matmul(alphatonos,cexkapelo),np.transpose(alphatonos)))
cstonoskapelooros3=np.matmul(mtonosant,cstonoss)

cstonoskapelo=np.matmul(np.matmul(cskapelooros1,cskapelooros2),cskapelooros3)

cestonoskapelo=cstonosdf-cstonoskapelo

print('Πινακας συμμεταβλητοτητων εκτιμημενων προβλεψεων σηματος: ')
print(cestonoskapelo)

#dhmiourgia pinaka symmetavlhtothtwn twn ektimhsewn twn parathrhsewn (y^=Ax^+s^+v^)
cexestonos=-np.matmul((np.matmul(cexkapelo,np.transpose(alphatonos))),np.matmul(mtonosant,cstonoss))

ceykapelooros1=np.matmul(np.matmul(alphatonos,cexkapelo),np.transpose(alphatonos))
ceykapelooros1df=pd.DataFrame(ceykapelooros1)
ceykapelooros2=cestonoskapelo
ceykapelooros2df=pd.DataFrame(ceykapelooros2)
ceykapelooros3=-np.matmul(alphatonos,cexestonos)
ceykapelooros3df=pd.DataFrame(ceykapelooros3)
ceykapelooros4=-np.transpose(np.matmul(alphatonos,cexestonos))
ceykapelooros4df=pd.DataFrame(ceykapelooros4)

ceytonoskapelo=ceykapelooros1df+ceykapelooros2df+ceykapelooros3df+ceykapelooros4df

print('Πινακας συμμεταβλητοτητων εκτιμημενων προβλεπομενων παρατηρησεων: ')
print(ceytonoskapelo)

#paragwgh syntelesth sysxetishs
pxij=np.zeros((len(xkapelo),len(xkapelo)))

for i in range(len(cexkapelo)):
    for j in range(len(cexkapelo)):
        pxij[i][j]= (cexkapelo[i][j])/(np.sqrt(cexkapelo[i][i])*np.sqrt(cexkapelo[j][j]))
pxijdf=pd.DataFrame(pxij)

print('Πινακας συντελεστη συσχετισης X^: ')
print(pxijdf)


#dhmioyrgia argyropoylioy oroy
diafores=np.zeros(len(bhta))
maxdist=max(bhta)-min(bhta)
myindex=np.zeros(len(bhta))
for i in range(len(bhta)):
    diafores[i]=bhta[i]-ykapelo[i]
    myindex[i]=diafores[i]/maxdist
myindexdf=pd.DataFrame(myindex)
diaforesdf=pd.DataFrame(diafores)

print('Διαφορες εκτιμωμενων παρατηρησεων και πραγματικων: ')
print(diaforesdf)
print('Αργυροπουλειος δεικτης των εκτιμομενων παρατηρησεων: ')
print(myindexdf)

#test argyropoyleioy deikth
print(ykapelo[231])
print(bhta[231])

ykapelo[231]=-60
diaforestest=bhta[231]-ykapelo[231]
myindextest=diaforestest/maxdist

print('Αργυροπουλειος δεικτης κανονικης τιμης Y^ στη θεση 231 του πινακα εκτιμησεων παρατηρησεων: ')
print(myindex[231])

print('Αργυροπουλειος δεικτης τεχνιτης τιμης Y^ στη θεση 231 του πινακα εκτιμησεων παρατηρησεων: ')
print(myindextest)

diaforesmyindex=myindextest-myindex[231]

print('Διαφορες τοις εκατο των αργυροπουλειων δεικτων: ')
print(diaforesmyindex*100)

#dhmioyrgia grafhmatwn me thn bibliothiki matplotlib.pyplot
fig1=plt.figure(1)
plt.plot(time,skapelo, label='Signal')
plt.xlabel("Date (in decimal years)")
plt.legend()
plt.title("Graph of the signal of the function")

fig2=plt.figure(2)
plt.plot(time, synarthshx,label='Dominant trend')
plt.xlabel("Date (in decimal years)")
plt.legend()
plt.title("Graph of the dominant trend of the function")

fig3=plt.figure(3)
plt.plot(time, bhta, label='Observations')
plt.xlabel("Date (in decimal years)")
plt.legend()
plt.title("Observations made during the years")

fig4=plt.figure(4)
plt.plot(time, vkapelo, label='Error')
plt.xlabel("Date (in decimal years)")
plt.legend()
plt.title("Error of observations")

fig5=plt.figure(5)
plt.plot(time, xs, label='Trend+signal')
plt.xlabel("Date (in decimal years)")
plt.legend()
plt.title("Function of observations without error")

fig6=plt.figure(6)
plt.plot(time, bhta, color='b', label='Observations')
plt.plot(time, xs, color='r', label='Observations without error')
plt.xlabel("Date (in decimal years)")
plt.legend()
plt.title("Function of observations with/without error")

fig7=plt.figure(7)
plt.scatter(timepredict,stonoskapelo, color='r', marker='x', label='Predicted values')
plt.plot(time, xs, color='b', label='Observations without error')
plt.xlabel("Date (in decimal years)")
plt.legend()
plt.title("Function of observations with/without error")

fig8=plt.figure(8)
plt.plot(time, signalvol, color='b', label='Function of error+signal')
plt.xlabel("Date (in decimal years)")
plt.legend()
plt.title("Function of error+signal")

fig9=plt.figure(9)
plt.plot(time, csdf[0], color='b', label='Function of covariance of signal')
plt.xlabel("Date (in decimal years)")
plt.legend()
plt.title("Function of covariance of signal")

fig10=plt.figure(10)
plt.plot(time, myindex, color='b', label='Function of Argyropoyleioy index')
plt.xlabel("Date (in decimal years)")
plt.legend()
plt.title("Function of Argyropoyleioy index")

plt.show()