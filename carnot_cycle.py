import math
from vpython import*
r=1.4
L=1.0
m=0.5
Ra=287
Ti=373.15
Tf=273.15
p0=101300
v0=(pi)*L**3/3
v1=(Ti/Tf)**(1/(r-1))*v0
p1=m*Ra*Tf/v1
v3=1/24*pi*L**3
p3=p0*v0/v3
v2=(Ti/Tf)**(1/(r-1))*v3
p2=p1*v1/v2
W30=m*Ra*Ti*math.log(v0/v3)
W12=-m*Ra*Tf*math.log(v1/v2)
Q30=W30
Q12=-W12
W01=-5/2*m*Ra*(Tf-Ti)
W23=-5/2*m*Ra*(Ti-Tf)
Q01=0
Q23=0
efficiency=1-Tf/Ti
W=W01+W12+W23+W30
Q=Q01+Q12+Q23+Q30

carnot_cycle=graph(width=600,height=600,xtitle='volume',ytitle='pressure',background=vec(0.5,0.5,0))
adiabatic1=gcurve(graph=carnot_cycle,color=color.red)
adiabatic2=gcurve(graph=carnot_cycle,color=color.orange)
isothermal1=gcurve(graph=carnot_cycle,color=color.blue)
isothermal2=gcurve(graph=carnot_cycle,color=color.cyan)

c1=p0*v0**r
c2=p2*v2**r
v=v0
while v0<=v<=v1:
    adiabatic1.plot(pos=(v,c1/v**r))
    v+=0.01
v=v1
while v2<=v<=v1:
    isothermal1.plot(pos=(v,m*Ra*Tf/v))
    v-=0.1
v=v2
while v3<=v<=v2:
    adiabatic2.plot(pos=(v,c2/v**r))
    v-=0.01
v=v3
while v3<=v<=v0:
    isothermal2.plot(pos=(v,m*Ra*Ti/v))
    v+=0.1
