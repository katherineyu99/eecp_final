from vpython import*
#初始條件
L = 1.0
K,T,Th,Tc,p0=8.314,273.15,373.15,173.15,101300
theta_rod=pi
theta_diff=pi/2
omega=-2*pi
t0=0
t,dt=0,1e-3
R=0.082

#display
scene=canvas(width=800,height=800,x=200,y=0,background=vec(0.2,0.2,0),center=vec(2*L,0,0))
#container
container=cylinder(pos=vec(0,0,0),axis=vec(3*L,0,0),radius=L/2,opacity=0.2)
containerh=cylinder(radius=L/2,opacity=0.2)
containerc=cylinder(radius=L/2,opacity=0.2)
#轉盤
wheel_pos=vector(5*L,0,0)
wheel=cylinder(pos=wheel_pos,axis=vec(0,0,L/10),radius=L/2,opacity=0.3)#,material=materials.wood

rod_lengh=L
rodco_lengh=1.5*L
rodho_lengh=3*L
rodc_x=L*cos(theta_rod)/2
rodc_y=L*sin(theta_rod)/2
rodc=cylinder(pos=wheel.pos+vec(rodc_x,rodc_y,0),axis=vec(-(L**2-rodc_y**2)**0.5,-rodc_y,0),radius=L/30,color=vec(0,0,0.3))
rodco=cylinder(pos=rodc.pos+rodc.axis,axis=vec(0,0,0),radius=L/30,color=vec(0,0.5,0.5),opcity=0.3)
rodco.axis=vector(-(rodco_lengh**2-rodco.pos.y**2)**0.5,-rodc.pos.y,0)

rodh_x=L*cos(theta_rod-theta_diff)/2
rodh_y=L*sin(theta_rod-theta_diff)/2
rodh=cylinder(pos=wheel.pos+vec(rodh_x,rodh_y,0),axis=vec(-(L**2-rodh_y**2)**0.5,-rodh_y,0),radius=L/50,color=vec(0.3,0,0))
rodho=cylinder(pos=rodh.pos+rodh.axis,axis=vec(0,0,0),radius=L/50,color=vec(0.5,0.5,0))
rodh.axis=vec(-(rodho_lengh**2-rodho.pos.y**2)**0.5,-rodho.pos.y,0)

ratio=1
diskh=cylinder(pos=rodho.pos+rodho.axis,axis=vec(0.01*L,0,0),radius=ratio*L/2)
diskc=cylinder(pos=rodco.pos+rodco.axis,axis=vec(0.01*L,0,0),radius=L/2)

#函式庫
Vsh=pi*L**3/4
Vdh=pi*L**2*(wheel_pos.x-wheel.radius-rod_lengh-rodho_lengh)/4
Vsc=Vsh
Vdc=pi*L**2*(rodho_lengh-rodco_lengh-2*wheel.radius)/4

n=p0*pi*(wheel_pos.x-rod_lengh-rodco_lengh)*L**2/4/R/T
t_T=Tc/Th

def Vh():#熱庫體積
    return pi*L**2*(diskh.pos.x)/4
def Vc():#冷庫體積
    return pi*L**2*(diskc.pos.x)/4-pi*L**2*(diskh.pos.x)/4
def V(): #總體積
    return pi*L**2*(diskc.pos.x)/4
def p(): #壓力
    return (n*R*Tc/(t_T*Vh()+Vc()))

#熱力學參數
Qin=0
Oout=0
v=0
P=p()
v=V()
vh=Vh()
vc=Vc()
W=0

#圖形輸出
scene1=graph(y=400,width=800,height=800,xtitle='V(m**3)',ytitle='P(Pa)',background=vec(0.5,0.5,0))
pV=gcurve(color=color.red,graph=scene1)
scene2=graph(y=400,width=800,height=800,xtitle='t(s)',ytitle='W(J),Qin(J)',background=vec(0.4,0.4,0))
scene3=graph(y=400,width=800,height=800,xtitle='t(s)',ytitle='thermal efficiency',background=vec(0.4,0.4,0))
Wdrav=gcurve(color=color.cyan,graph=scene2)#W
Qindrav=gcurve(color=color.red,graph=scene2)#Qin
efficiency_drav=gdots(color=color.blue,graph=scene3)#thermal efficiency
rfefdrav=gdots(color=color.cyan,graph=scene3)#theory_thermal efficiency

while True:
    t+=dt
    rate(0.1/dt)
    
    #處理轉動
    theta_original=theta_rod
    theta_rod+=omega*dt
    wheel.rotate(angle=theta_rod-theta_original)
    
    #操作桿部分
    rodc_x=L*cos(theta_rod)/2
    rodc_y=L*sin(theta_rod)/2
    rodc.pos=vector(rodc_x,rodc_y,0)+wheel.pos
    rodc.axis=vector(-(L**2-rodc_y**2)**0.5,-rodc_y,0)
    rodco.pos=rodc.pos+rodc.axis
    rodco.axis=vector(-(rodco_lengh**2-rodco.pos.y**2)**0.5,-rodco.pos.y,0)
    
    rodh_x=L*cos(theta_rod-theta_diff)/2
    rodh_y=L*sin(theta_rod-theta_diff)/2
    rodh.pos=vector(rodh_x,rodh_y,0)+wheel.pos
    rodh.axis=vector(-(L**2-rodh_y**2)**0.5,-rodh_y,0)
    rodho.pos=rodh.pos+rodh.axis
    rodho.axis=vector(-(rodho_lengh**2-rodho.pos.y**2)**0.5,-rodho.pos.y,0)

    #活塞部分
    diskc.pos=rodco.pos+rodco.axis
    diskh.pos=rodho.pos+rodho.axis
    
    #容器部分
    containerh.axis=diskh.pos-vector(0,0,0)
    containerc.pos=diskh.pos
    containerc.axis=diskc.pos-diskh.pos
    container.pos=diskc.pos
    container.axis=vector(3*L,0,0)-diskc.pos
    
    #熱力過程
    W+=1.5*(P+p())*(V()-v)
    Qin+=1.5*(P+p())*(Vh()-vh)
    if(theta_rod-theta_original)+(theta_rod-theta_original+omega*dt)<=0: #每週期輸出一次
        Wdrav.plot(pos=(t,W))
        Qindrav.plot(pos=(t,Qin))
        if 0<W/Qin<1:
            efficiency_drav.plot(pos=(t,W/Qin))
            
        theta_original-=-2*pi
    P=p()
    v=V()
    vh=Vh()
    vc=Vc()
    pV.plot(pos=(V(),p()))
