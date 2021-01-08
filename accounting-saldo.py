import numpy as np
import matplotlib.pyplot as plt
import re
import glob
import gzip
import os
import sys
import matplotlib.ticker as mticker
import matplotlib.lines as mlines

def stringtodate(stri):
    y = int(stri[0:4])
    m = int(stri[4:6])
    d = int(stri[6:8])
    try:
        dt =     datetime.datetime(y, m, d, 0, 0, 0)
    except:
        return (False)
    return dt

def loopDates(firstdate,lastdate):
#  print(firstdate,lastdate)
  first_y = int(firstdate[0:4])
  last_y = int(lastdate[0:4])

  first_m = int(firstdate[4:6])
  last_m = int(lastdate[4:6])

  first_d = int(firstdate[6:8])
  last_d = int(lastdate[6:8])

  loop = []
  s_y=first_y
  s_m = first_m
  s_d = first_d
#  print(s_y,s_m,s_d,last_y, last_m, last_d, s_y<last_y or (last_y==s_y and s_m<last_m or (last_y==s_y and s_m == last_m and s_d <= last_d)))
  while s_y<last_y or (last_y==s_y and s_m<last_m or (last_y==s_y and s_m == last_m and s_d <= last_d))  :
#    print (str(s_y)+str(s_m).zfill(2)+str(s_d).zfill(2))
    loop.append(str(s_y)+str(s_m).zfill(2)+str(s_d).zfill(2))
    s_d = s_d+1
    if s_d > 31:
        s_d = 1
        s_m = s_m+1
    if s_m> 12:
        s_m=1
        s_y=s_y+1
  return loop



def myFunc(e):
  (m,d) = e.split('/')
  return int(d)+int(m)*30

def computeDurationFromSaldo(du):
    #4013:04:36
    (h,m,s)= du.split(":")
    return (int(s)+ int(m)*60+int(h)*3600)*1./3600

def toDate(du):
  y = du[0:4]
  m= du[4:6]
  d = du[6:8]
#  print ("DATE",y,m,d)
  return y+"-"+m+"-"+d


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

filename = 'accounting-saldo.out'
bydate= {}
file=open (filename,"r")


for l in file.readlines():
     if re.search("---------------------Total",l) !=None:
         break
     if re.search("----------",l) != None:
         continue;
     if re.search("Consumed/h",l) != None:
         continue;
     if re.search("date        username    account",l) != None:
         continue;
     if re.search('20',l) == None:
         continue
#     print ("LINE",l, l.split())
     (date, user, project, cons, jobs) = l.split()
#     print ("LLLLL",l)
     vo = getVO(user)
     submitted_d = toDate(date)
#     print (submitted_d)
     duration = computeDurationFromSaldo(cons)
#     print ("linea" ,user,vo, submitted_d,duration)
     if date not in bydate:
         bydate[date] = {}
     if vo not in bydate[date]:
         bydate[date][vo] =0
     bydate[date][vo] = bydate[date][vo]+int(duration)

file.close()


firstdate = sorted(bydate.keys())[0]
lastdate = sorted(bydate.keys())[-1]
for i in loopDates(firstdate,lastdate):
    if i not in bydate.keys():
#        print ("ADDING", i)
        bydate[i] = {}

#print ("By DATE ",bydate )
#
# plot
#
N = len(bydate)
dates = (list(bydate.keys()))
dates.sort()
#print (dates)
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
        tots['na']= tots['na']+ bydate[d]['n/a']
    else:
        na.append(0)

cmsday=[]
atlasday=[]
lhcbday=[]
aliceday=[]
naday=[]
unusedday=[]
cmstot=[]
atlastot=[]
lhcbtot=[]
alicetot=[]
natot=[]
unusedtot = []
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
    cmsday.append(cms[i])
    atlasday.append(atlas[i])
    lhcbday.append(lhcb[i])
    aliceday.append(alice[i])
    naday.append(na[i])
    unus = 30e6-cmstot[-1]-atlastot[-1]-lhcbtot[-1]-alicetot[-1]-natot[-1]
    if unus>0:
        unusedtot.append(30e6-cmstot[-1]-atlastot[-1]-lhcbtot[-1]-alicetot[-1]-natot[-1])
    else:
        unusedtot.append(0)
    unusedday.append(288*68*24-cmsday[-1]-atlasday[-1]-lhcbday[-1]-aliceday[-1]-naday[-1])

tottot=0
for i in (cmstot,atlastot,lhcbtot,alicetot,natot):
    tottot = tottot+i[-1]

print ("Total used is ",tottot,"hours out of 30M, which is",int(tottot/30e6*100), "%")
print ("It is distributed like:")
print ("ATLAS: ",int(atlastot[-1]/30e6*100), "%")
print ("CMS  : ",int(cmstot[-1]/30e6*100), "%")
print ("ALICE: ",int(alicetot[-1]/30e6*100), "%")
print ("LHCb : ",int(lhcbtot[-1]/30e6*100), "%")



# calculate speed
speed=0
for i in range(len(cms)-10,len(cms)):
    speed = speed+cms[i]+atlas[i]+alice[i]+lhcb[i]+na[i]
import datetime

print ("Speed of utilization in the last 10 days:", speed/10., "per day.")#" At this speed, there are", round((30e6-tottot)/(speed/10.)), "days left to reach 30e6.")
print ("It is", round (1000*speed/10./30e6)/10.,"% per day.")#" That date would be",datetime.date.today()+datetime.timedelta(days=round((30e6-tottot)/(speed/10.))))
deltadays = (datetime.datetime(2021, 2, 28, 23, 59, 59)-datetime.datetime.today()).days
print ("Extrapolation to Feb 28th  (",deltadays,"days ) gives a total of",int(tottot/30e6*100)+deltadays*  round (1000*speed/10./30e6)/10. ,"%" )



ind = np.arange(N)    # the x locations for the groups
width = 0.35       # the width of the bars: can also be len(x) sequence
cms=np.array(cmstot)
atlas=np.array(atlastot)
lhcb=np.array(lhcbtot)
alice=np.array(alicetot)
na=np.array(natot)
unused = np.array(unusedtot)

cmsd = np.array(cmsday)
atlasd = np.array(atlasday)
lhcbd = np.array(lhcbday)
aliced = np.array(aliceday)
nad = np.array(naday)
nad = np.array(naday)
unusedd=np.array(unusedday)
#print (cms,atlas, lhcb, alice,na)



# numbers for danilo
startgrant=datetime.datetime(2019, 4, 1, 0, 0, 0)
endgrant = datetime.datetime(2021, 2, 28, 23, 59, 59)
print ("=== CMS Accounting ===")
for num in range(0,len(dates)):
    dt = stringtodate(dates[num])
    if dt != False and dt.weekday()==6 and dt> datetime.datetime(2019, 7, 31, 23, 59, 59):
        print (dates[num],'Fraction of grant used',round(cms[num]/(30e6/4)*100),'%;', 'Fraction of grant time', round(((dt-startgrant).days*1.)/((endgrant-startgrant).days)*1000)/10., "%. Grant (Million h):",7.5, " Used (Million h):", round(cms[num]/1e6*10)/10)
    #print (num)
print ("============")

plt.figure(figsize=(6,10))


plt.subplot(3, 1, 1)

#p1 = plt.bar(ind, cms, width)
#p2 = plt.bar(ind, atlas, width,bottom=cms)
#p3 = plt.bar(ind, lhcb, width, bottom=cms+atlas)
#p4 = plt.bar(ind, alice, width, bottom=cms+atlas+lhcb)
#p5 = plt.bar(ind, na, width, bottom=cms+alice+atlas+lhcb)

plt.stackplot(dates,[ cms,atlas, lhcb,alice,na,unused])

plt.ylabel('Core h')
plt.title('Core h by VO')
plt.xticks(ind, dates)
plt.legend(('CMS', 'ATLAS','LHCb', 'ALICE', 'N/A', "Unused"),loc='upper left')
scale = (cmstot[-1]+atlastot[-1]+lhcbtot[-1]+alicetot[-1]+natot[-1])*2
axes = plt.gca()
#axes.set_xlim([xmin,xmax])
axes.set_ylim([0,80e6])
#plt.locator_params(nbins=5)
#plt.yscale("log")

#l = mlines.Line2D([0,1000], [30e6,30e6])
#axes.add_line(l)
plt.subplot(3, 1, 2)

#p1 = plt.bar(ind, cms, width)
#p2 = plt.bar(ind, atlas, width,bottom=cms)
#p3 = plt.bar(ind, lhcb, width, bottom=cms+atlas)
#p4 = plt.bar(ind, alice, width, bottom=cms+atlas+lhcb)
#p5 = plt.bar(ind, na, width, bottom=cms+alice+atlas+lhcb)

plt.stackplot(dates,[ cmsd,atlasd, lhcbd,aliced,nad,unusedd])

plt.ylabel('Core h')
plt.title('Core h by VO per day')
plt.xticks(ind, dates)
plt.legend(('CMS', 'ATLAS','LHCb', 'ALICE', 'N/A', "Unused"),loc='upper left')
scale = (cmstot[-1]+atlastot[-1]+lhcbtot[-1]+alicetot[-1]+natot[-1])*2
axes = plt.gca()
#axes.set_xlim([xmin,xmax])
axes.set_ylim([0,300*68*24])
#plt.locator_params(nbins=5)
#plt.yscale("log")

#l = mlines.Line2D([0,1000], [30e6,30e6])
#axes.add_line(l)





plt.subplot(3, 1, 3)
explode = (0.2, 0.2, 0.2, 0.2, 0.2)
plt.pie(tots.values(),explode=explode, startangle=0,labels=('CMS', 'ATLAS','LHCb', 'ALICE', 'N/A'),autopct='%1.1f%%', shadow=True)

#plt.show()

tots['Unused'] = 30e6-tottot
if tots['Unused'] <0:
        tots['Unused']=0


#plt.subplot(4, 1, 4)
#explode = (0.5, 0.5, 0.5, 0.5, 0.5,0.)
#plt.pie(tots.values(),explode=explode, startangle=180,labels=('CMS', 'ATLAS','LHCb', 'ALICE', 'N/A','Unused'),autopct='%1.1f%%', shadow=True)

#plt.show()
plt.savefig('accounting-cineca.png')

#repeat the first plot alone
plt.figure(figsize=(5,5))
plt.stackplot(dates,[ cms,atlas, lhcb,alice,na,unused])

plt.ylabel('Core h')
plt.title('Core h by VO')
plt.xticks(ind, dates)
plt.legend(('CMS', 'ATLAS','LHCb', 'ALICE', 'N/A', "Grant"),loc='upper left')
scale = (cmstot[-1]+atlastot[-1]+lhcbtot[-1]+alicetot[-1]+natot[-1])*2
axes = plt.gca()
#axes.set_xlim([xmin,xmax])
axes.set_ylim([0,60e6])
plt.savefig('accounting-cineca-for-compops.png')
