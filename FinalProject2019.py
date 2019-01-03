from vpython import*
import math
#初始條件
L = 1.0
K,Th,Tc,p0=8.314,213.15,173.15,101300
theta_rod=pi
theta_diff=pi/2
omega=-2*pi
t0=0
t,dt=0,1e-3
R=0.082
r=1.4


scene=canvas(width=800,height=800,x=200,y=0,background=vec(0.2,0.2,0),center=vec(2*L,0,0))
container=cylinder(pos=vec(0,0,0),axis=vec(3*L,0,0),radius=L/2,opacity=0.2)
containerh=cylinder(radius=L/2,opacity=0.2,color=color.red)

#轉盤
wheel_pos=vector(5*L,0,0)
wheel=cylinder(pos=wheel_pos,axis=vec(0,0,L/10),radius=L/2,opacity=0.5,texture=textures.metal)
rod_lengh=L
rodho_lengh=3*L
rodh_x=L*cos(theta_rod)/2
rodh_y=L*sin(theta_rod)/2
rodh=cylinder(pos=wheel.pos+vec(rodh_x,rodh_y,0),axis=vec(-(L**2-rodh_y**2)**0.5,-rodh_y,0),radius=L/30,color=vec(0,0,0.3))
rodho=cylinder(pos=rodh.pos+rodh.axis,axis=vec(-3,0,0),radius=L/30,color=vec(0,0.5,0.5),opacity=0.3)
ratio=1
diskh=cylinder(pos=rodho.pos+rodho.axis,axis=vec(0.01*L,0,0),radius=L/2,texture=textures.metal)

n=p0*pi*(1/2*L)*L**2/4/R/Th
t_T=Tc/Th
C1=p0*(pi*L**3/8)**r
C2=n*R*Tc/(3*L**3/8*pi)*(3*L**3/8*pi)**r

def Vh():#熱庫體積
    return pi*L**2*(diskh.pos.x)/4
def V(): #總體積
    return pi*L**2*(diskh.pos.x)/4
def p(): #壓力
    if rodh_y>0 and pi*L**3/8<=V()<=(Tc/Th)**(1/(r-1))*3*L**3/8*pi:
        return (n*R*Th/V())
    if rodh_y>0 and (Tc/Th)**(1/(r-1))*3*L**3/8*pi<=V()<=pi*L**3*3/8:
        return (C2/V()**r)
    if rodh_y<0 and (Th/Tc)**(1/(r-1))*L**3/8*pi<=V()<=pi*L**3*3/8:    
        return (n*R*Tc/V())
    if rodh_y<0 and pi*L**3/8<=V()<=(Th/Tc)**(1/(r-1))*L**3/8*pi:
        return (C1/V()**r)

    
        
#熱力學參數
Q30=0
Q12=0
v=0
P=p()
v=V()
vh=Vh()
W=0
W_original=0
Q30_original=0
#圖形輸出
scene1=graph(y=400,width=800,height=800,xtitle='V(m**3)',ytitle='P(Pa)',background=vec(0,0,0))
pV=gcurve(color=color.red,graph=scene1)
scene2=graph(y=400,width=800,height=800,xtitle='t(s)',ytitle='Qin(J)',background=vec(0.4,0.4,0))
scene3=graph(y=400,width=800,height=800,xtitle='t(s)',ytitle='Qout(J)',background=vec(0.4,0.4,0))
scene4=graph(y=400,width=800,height=800,xtitle='t(s)',ytitle='thermal efficiency',background=vec(0.4,0.4,0),ymax=1,ymin=0)
scene5=graph(y=400,width=800,height=800,xtitle='t(s)',ytitle='W',background=vec(0.4,0.4,0))
Wdrav=gcurve(color=color.cyan,graph=scene5)#W
Qindrav=gcurve(color=color.red,graph=scene2)#Qin
Qoutdrav=gcurve(color=color.green,graph=scene3)#Qout
efficiency_drav=gcurve(color=color.blue,graph=scene4)#thermal efficiency
carnot_cycle=graph(width=600,height=600,xtitle='volume',ytitle='pressure',background=vec(0.5,0.5,0))
thermal_cycle=gcurve(graph=carnot_cycle,color=color.cyan)


while True:
    t+=dt
    rate(100)
    
    #處理轉動
    theta_original=theta_rod
    theta_rod+=omega*dt
    wheel.rotate(angle=theta_rod-theta_original)
    #操作桿部分
    rodh_x=L*cos(theta_rod)/2
    rodh_y=L*sin(theta_rod)/2
    rodh.pos=vector(rodh_x,rodh_y,0)+wheel.pos
    rodh.axis=vector(-(L**2-rodh_y**2)**0.5,-rodh_y,0)
    rodho.pos=rodh.pos+rodh.axis
    rodho.axis=vector(-(rodho_lengh**2-rodho.pos.y**2)**0.5,-rodho.pos.y,0)

    #活塞部分
    diskh.pos=rodho.pos+rodho.axis
    
    #容器部分
    containerh.axis=diskh.pos
    containerh.pos=container.pos
    container.axis=vector(3*L,0,0)
    
    
    if rodh_y>0 and pi*L**3/8<=V()<=(Tc/Th)**(1/(r-1))*3*L**3/8*pi:
        containerh.color=color.red
        Q30+=p()*(Vh()-vh)
        W+=p()*(Vh()-vh)
        Wdrav.plot(pos=(t,W))
        Qindrav.plot(pos=(t,Q30))
        Qoutdrav.plot(pos=(t,Q12))
        
    if rodh_y>=0 and (Tc/Th)**(1/(r-1))*3*L**3/8*pi<V()<=pi*L**3*3/8:
        containerh.color=color.cyan
        W+=p()*(V()-v)
        Wdrav.plot(pos=(t,W))
        Qindrav.plot(pos=(t,Q30))
        Qoutdrav.plot(pos=(t,Q12))
        
    if rodh_y<0 and (Th/Tc)**(1/(r-1))*L**3/8*pi<=V()<pi*L**3*3/8:  
        containerh.color=color.blue
        Q12+=p()*(V()-v)
        W+=p()*(V()-v)
        Wdrav.plot(pos=(t,W))
        Qindrav.plot(pos=(t,Q30))
        Qoutdrav.plot(pos=(t,Q12))
    if rodh_y<0 and pi*L**3/8<V()<(Th/Tc)**(1/(r-1))*L**3/8*pi:
        containerh.color=color.orange
        W+=p()*(V()-v)
        Wdrav.plot(pos=(t,W))
        Qindrav.plot(pos=(t,Q30))
        Qoutdrav.plot(pos=(t,Q12))
    if V()==L**3/8*pi and t>0:
        efficiency_drav.plot(pos=(t,(W-W_original)/(Q30-Q30_original)))
        W_original=W
        Q30_original=Q30
       
        
    thermal_cycle.plot(pos=(V(),p()))
    P=p()
    v=V()
    vh=Vh()