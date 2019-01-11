from vpython import*
import math
import random
#初始條件
L = 1.0
p0=101300
theta_crank=pi
omega=-2*pi
t,dt=0,1e-3
R=0.082
r=1.4
count=0

ask=input('Do you want to choose the high temperature?Yes/No ')
ask=ask.upper()
if ask=='YES':
    Th=float(input('Enter the temperature of the heat bath :'))
    Tc=random.randint(int(Th*(1/3)**(2/5)),int(Th)-1)
elif ask=='NO':
    Th=213.15
    Tc=173.15


scene=canvas(width=800,height=800,x=200,y=0,background=vec(0.2,0.2,0),center=vec(2*L,0,0))
container=cylinder(pos=vec(0,0,0),axis=vec(3*L,0,0),radius=L/2,opacity=0.2)
containerh=cylinder(radius=L/2,opacity=0.2)

direction=arrow(pos=vec(-1.5*L,L/8,0),width=L/4,axis=vec(L,0,0),color=color.red)
#轉盤
wheel=cylinder(pos=vector(5*L,0,0),axis=vec(0,0,L/10),radius=L/2,opacity=0.5,texture=textures.metal)
rod_lengh=3*L
crank_x=L*cos(theta_crank)/2
crank_y=L*sin(theta_crank)/2
crank=cylinder(pos=wheel.pos+vec(crank_x,crank_y,0),axis=vec(-(L**2-crank_y**2)**0.5,-crank_y,0),radius=L/30,color=vec(0,0,0.3))
rod=cylinder(pos=crank.pos+crank.axis,axis=vec(-3,0,0),radius=L/30,color=vec(0,0.5,0.5),opacity=0.3)
diskh=cylinder(pos=rod.pos+rod.axis,axis=vec(0.01*L,0,0),radius=L/2,texture=textures.metal)

n=p0*pi*(1/2*L)*L**2/4/R/Th
C1=p0*(pi*L**3/8)**r
C2=n*R*Tc/(3*L**3/8*pi)*(3*L**3/8*pi)**r

def V(): #總體積
    return pi*L**2*(diskh.pos.x)/4
def p(): #壓力
    if crank_y>0 and pi*L**3/8<=V()<=(Tc/Th)**(1/(r-1))*3*L**3/8*pi:
        return (n*R*Th/V())
    if crank_y>0 and (Tc/Th)**(1/(r-1))*3*L**3/8*pi<=V()<=pi*L**3*3/8:
        return (C2/V()**r)
    if crank_y<0 and (Th/Tc)**(1/(r-1))*L**3/8*pi<=V()<=pi*L**3*3/8:    
        return (n*R*Tc/V())
    if crank_y<0 and pi*L**3/8<=V()<=(Th/Tc)**(1/(r-1))*L**3/8*pi:
        return (C1/V()**r)

#熱力學參數
Q30,Q12=0,0
v=0
P=p()
v=V()
W=0
W30=0
W01=0
W12=0
W23=0
W_original=0
Q30_original=0

#圖形輸出
scene1=graph(y=400,width=800,height=800,xtitle='t(s)',ytitle='Qin(J)',background=vec(0.4,0.4,0))
scene2=graph(y=400,width=800,height=800,xtitle='t(s)',ytitle='Qout(J)',background=vec(0.4,0.4,0))
scene3=graph(y=400,width=800,height=800,xtitle='t(s)',ytitle='thermal efficiency',background=vec(0.4,0.4,0),ymax=1,ymin=0)
scene4=graph(y=400,width=800,height=800,xtitle='t(s)',ytitle='W',background=vec(0.4,0.4,0))
carnot_cycle=graph(width=600,height=600,xtitle='volume',ytitle='pressure',background=vec(0.5,0.5,0))
Qin=gcurve(color=color.red,graph=scene1)#Qin
Qout=gcurve(color=color.blue,graph=scene2)#Qout
efficiency=gcurve(color=color.green,graph=scene3)#thermal efficiency
Work=gcurve(color=color.cyan,graph=scene4)#W
thermal_cycle=gcurve(graph=carnot_cycle,color=color.cyan)

print('High Temperature:',Th,'\nLow Temperature:',Tc)

while True:
    t+=dt
    rate(100)
    
    #轉動
    theta_original=theta_crank
    theta_crank+=omega*dt
    wheel.rotate(angle=theta_crank-theta_original)
    #rod and crank
    crank_x=L*cos(theta_crank)/2
    crank_y=L*sin(theta_crank)/2
    crank.pos=vector(crank_x,crank_y,0)+wheel.pos
    crank.axis=vector(-(L**2-crank_y**2)**0.5,-crank_y,0)
    rod.pos=crank.pos+crank.axis
    rod.axis=vector(-(rod_lengh**2-rod.pos.y**2)**0.5,-rod.pos.y,0)

    #活塞位置
    diskh.pos=rod.pos+rod.axis
    
    #容器
    containerh.axis=diskh.pos
    containerh.pos=container.pos
    container.axis=vector(3*L,0,0)
    
    if crank_y>0 and pi*L**3/8<=V()<=(Tc/Th)**(1/(r-1))*3*L**3/8*pi:
        containerh.color=color.red
        Q30+=p()*(V()-v)
        W+=p()*(V()-v)
        W30+=p()*(V()-v)
        Work.plot(pos=(t,W))
        Qin.plot(pos=(t,Q30))
        Qout.plot(pos=(t,Q12))
        direction.pos.x=-1.5*L
        direction.axis=vec(L,0,0)
        direction.color=color.red 
                    
    if crank_y>=0 and (Tc/Th)**(1/(r-1))*3*L**3/8*pi<V()<=pi*L**3*3/8:
        containerh.color=color.cyan
        W+=p()*(V()-v)
        W01+=p()*(V()-v)
        Work.plot(pos=(t,W))
        Qin.plot(pos=(t,Q30))
        Qout.plot(pos=(t,Q12))
        direction.color=vec(0.2,0.2,0)
                
    if crank_y<0 and (Th/Tc)**(1/(r-1))*L**3/8*pi<=V()<pi*L**3*3/8:  
        containerh.color=color.blue
        Q12+=p()*(V()-v)
        W+=p()*(V()-v)
        W12+=p()*(V()-v)
        Work.plot(pos=(t,W))
        Qin.plot(pos=(t,Q30))
        Qout.plot(pos=(t,Q12))
        direction.pos.x=-0.5*L
        direction.axis=vec(-L,0,0)
        direction.color=color.blue
                
    if crank_y<0 and pi*L**3/8<V()<(Th/Tc)**(1/(r-1))*L**3/8*pi:
        containerh.color=color.orange
        W+=p()*(V()-v)
        W23+=p()*(V()-v)
        Work.plot(pos=(t,W))
        Qin.plot(pos=(t,Q30))
        Qout.plot(pos=(t,Q12))
        direction.color=vec(0.2,0.2,0)
    if V()==L**3/8*pi and t>0:
        count+=1
        efficiency.plot(pos=(t,(W-W_original)/(Q30-Q30_original)))
        if count==1:
            print('Work         Qin         Qout'.rjust(57))
            print('Isothermal   expansion:  %.4f   %.4f       0'%(W30,Q30))
            print('Adiabatic    expansion:  %.4f        0           0'%(W01))
            print('Isothermal compression: %.4f        0     %.4f'%(W12,Q12))
            print('Adiabatic  compression: %.4f        0           0'%(W23))
            
        W_original=W
        Q30_original=Q30
       
        
    thermal_cycle.plot(pos=(V(),p()))
    P=p()
    v=V()
