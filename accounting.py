import numpy as np
import matplotlib.pyplot as plt
import re
import glob
import gzip
import os
def myFunc(e):
  (m,d) = e.split('/')
  return int(d)+int(m)*30 

def computeDuration(du):
  (dh,m,s)= du.split(":")
  (d,h) = dh.split("+")
#  if d=='1':
#    print ("CONV",du,d,h,m,s)
  return (int(s)+60*int(m)+3600*int(h)+86400*int(d))*1./3600

def getVO(u):
    vo= 'n/a'
    if (re.search('cms',u) != None):
            vo= 'cms'
    if (re.search('atl', u) != None):
            vo= 'atlas'
    if (re.search('lhc',u) != None):
            vo= 'lhcb'
    if (re.search('ali',u) != None):
            vo= 'alice'
#    print ("VO", u, vo)
    return vo
    
filenames = 'accounting-*.dat.gz'
files = sorted(glob.glob(filenames))
mydict= {}

for f in files:
    file = gzip.open(f, 'r')
    print ("Working on file",f)

    for l in file.readlines():
     fields = l.split()
#     print (fields)
     if len (fields)<8:
         continue
     num = fields[0].decode("UTF-8")
     if num =='ID':
         continue
     user = fields[1].decode("UTF-8")
     vo = getVO(user)
     submitted_d = (fields[2]).decode("UTF-8")
#     print (submitted_d)
     sumbitted_t = (fields[3]).decode("UTF-8")
     duration = 68*computeDuration((fields[4]).decode("UTF-8"))
     status = (fields[5].decode("UTF-8"))
     end_d = (fields[6].decode("UTF-8"))
     end_t=(fields[7]).decode("UTF-8")
#     print (user,status, duration)
     mydict[num] = (user,vo, submitted_d,duration)
     file.close()
# analyze
bydate = {}
for e in mydict.keys():
    if mydict[e][2] not in bydate:
        bydate[mydict[e][2]] ={}
    if mydict[e][1] not in bydate[mydict[e][2]] :
        bydate[mydict[e][2]][mydict[e][1] ]=0
    bydate[mydict[e][2]][mydict[e][1]] = bydate[mydict[e][2]][mydict[e][1]] + mydict[e][3]

print ("By DATE ",bydate )
#
# plot
#
N = len(bydate)
dates = (list(bydate.keys()))
dates.sort(key=myFunc)
print (dates)
atlas = []
cms = []
lhcb = []
alice=[]
na = []
tots={}
tots['cms']=0
tots['atlas']=0
tots['lhcb']=0
tots['alice']=0
tots['na']=0
for d in dates:
    if 'cms' in bydate[d]:
        cms.append(bydate[d]['cms'])
        tots['cms']= tots['cms']+ bydate[d]['cms']
    else:
        cms.append(0)
    if 'atlas' in bydate[d]:
        atlas.append(bydate[d]['atlas'])
        tots['atlas']= tots['atlas']+ bydate[d]['atlas']
    else:
        atlas.append(0)
    if 'lhcb' in bydate[d]:
        lhcb.append(bydate[d]['lhcb'])
        tots['lhcb']= tots['lhcb']+ bydate[d]['lhcb']
    else:
        lhcb.append(0)
    if 'alice' in bydate[d]:
        alice.append(bydate[d]['alice'])
        tots['alice']= tots['alice']+ bydate[d]['alice']

    else:
        alice.append(0)
    if 'n/a' in bydate[d]:
        na.append(bydate[d]['n/a'])
        tots['na']= tots['na']+ bydate[d]['na']

    else:
        na.append(0)

cmstot=[]
atlastot=[]
lhcbtot=[]
alicetot=[]
natot=[]
for i in range(0,len(cms)):
    if i ==0:
        cmstot.append(cms[i])
        atlastot.append(atlas[i])
        lhcbtot.append(lhcb[i])
        alicetot.append(alice[i])
        natot.append(na[i])
    else:
        cmstot.append(cms[i]+cmstot[i-1])
        atlastot.append(atlas[i]+atlastot[i-1])
        lhcbtot.append(lhcb[i]+lhcbtot[i-1])
        alicetot.append(alice[i]+alicetot[i-1])
        natot.append(na[i]+natot[i-1])

        

ind = np.arange(N)    # the x locations for the groups
width = 0.35       # the width of the bars: can also be len(x) sequence
cms=np.array(cmstot)
atlas=np.array(atlastot)
lhcb=np.array(lhcbtot)
alice=np.array(alicetot)
na=np.array(natot)

#print (cms,atlas, lhcb, alice,na)

plt.subplot(2, 1, 1)

#p1 = plt.bar(ind, cms, width)
#p2 = plt.bar(ind, atlas, width,bottom=cms)
#p3 = plt.bar(ind, lhcb, width, bottom=cms+atlas)
#p4 = plt.bar(ind, alice, width, bottom=cms+atlas+lhcb)
#p5 = plt.bar(ind, na, width, bottom=cms+alice+atlas+lhcb)

plt.stackplot(dates,[ cms,atlas, lhcb,alice,na])

plt.ylabel('Core h')
plt.title('Core h by VO')
plt.xticks(ind, dates)
plt.legend(('CMS', 'ATLAS','LHCb', 'ALICE', 'N/A'),loc='upper left')
scale = (cmstot[-1]+atlastot[-1]+lhcbtot[-1]+alicetot[-1]+natot[-1])*2

axes = plt.gca()
#axes.set_xlim([xmin,xmax])
axes.set_ylim([0,scale])
#plt.yscale("log")

plt.subplot(2, 1, 2)

plt.pie(tots.values(),labels=('CMS', 'ATLAS','LHCb', 'ALICE', 'N/A'))

#plt.show()
plt.savefig('accounting-cineca-recent.png')
