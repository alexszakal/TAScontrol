from numpy import *
''' Calculation of spectrometer angles for a given (h,k,l,E) point in 
reciprocal space
'''
#Sample parameters
a1= 5.658 #3.8643   #Direct lattice parameters
a2= 5.658 #3.8643
a3= 5.658 #11.732
alpha1=90  #Direct lattice angles
alpha2=90
alpha3=90

scattSign = 1

#Orienting reflections
h1=matrix('1; 0; 0')  # ('2; 0; 0')
h2=matrix('0; 0; 1')  # ('0; 0; 4')

h1mu=0 #-2.5
h1nu=0
h1om=102.519 #-40.682
th21=25.038  #-78.794

h2mu=0 #-2.5
h2nu=0 #3.5
h2om=12.519 #-116.0
th22=25.038  #-49.43

#Vector for reverse calculation
hkl=matrix('1 0 0')


#calculation of direct lattice vectors
a1v=matrix('{0:.5f} 0 0'.format(a1))
a2v=matrix('{0:.5f} {1:.5f} 0'.format(a2*cos(deg2rad(alpha3)), a2*sin(deg2rad(alpha3))))
a31=cos(deg2rad(alpha2))*a3
a32=(a3*cos(deg2rad(alpha1))-a31*cos(deg2rad(alpha3))) / sin(deg2rad(alpha3))
a33=sqrt(pow(a3,2)-pow(a31,2)-pow(a32,2))
a3v=matrix('{0:.5f} {1:.5f} {2:.5f}'.format(a31,a32,a33))

"""
print 'a1v: ',
print a1v
print '\na2v: ',
print a2v
print '\na3v: ',
print a3v
"""

#calculation of reciprocal lattice
V=dot(cross(a1v, a2v), a3v.transpose())

b1v=2*pi*cross(a2v,a3v)/V
b2v=2*pi*cross(a3v,a1v)/V
b3v=2*pi*cross(a1v,a2v)/V

b1=sqrt(pow(b1v.item(0),2) + pow(b1v.item(1),2) + pow(b1v.item(2),2))
b2=sqrt(pow(b2v.item(0),2) + pow(b2v.item(1),2) + pow(b2v.item(2),2))
b3=sqrt(pow(b3v.item(0),2) + pow(b3v.item(1),2) + pow(b3v.item(2),2))

"""
print b1
print b2
print b3
"""

"""
print '\n\nb1v: ',
print b1v
print '\nb2v: ',
print b2v
print '\nb3v: ',
print b3v
"""

b1=sqrt(pow(b1v[0,0],2)+pow(b1v[0,1],2)+pow(b1v[0,2],2))
b2=sqrt(pow(b2v[0,0],2)+pow(b2v[0,1],2)+pow(b2v[0,2],2))
b3=sqrt(pow(b3v[0,0],2)+pow(b3v[0,1],2)+pow(b3v[0,2],2))

beta1=arccos( dot(b2v,b3v.transpose())/b2/b3 ) /pi *180
beta2=arccos( dot(b1v,b3v.transpose())/b1/b3 ) /pi *180
beta3=arccos( dot(b1v,b2v.transpose())/b1/b2 ) /pi *180

"""
print '\n\n beta1={0}  beta2={1}   beta3={2}\n\n'.format(beta1, beta2, beta3)
"""

#Calculation of B matrix 
B=zeros((3,3))
B[0][0]=float(b1)
B[0][1]=float(b2)*cos(deg2rad(beta3))
B[0][2]=float(b3)*cos(deg2rad(beta2))
B[1][1]=float(b2)*sin(deg2rad(beta3))
B[1][2]=-1*sin(deg2rad(beta2))*cos(deg2rad(alpha1))
B[2][2]=2*pi/float(a3)

"""
print B
"""

#################################
#### CALCULATION OF U matrix ####
#################################

#calculate u_nu1, u_nu2
theta1=th21/2
theta2=th22/2

#Ez megjavitja??
#theta1=180-theta1
#theta2=180-theta2

if scattSign==1:
    omBL1=h1om-theta1  #omega in frame of Busing-Levy definitions
    omBL2=h2om-theta2
elif scattSign == (-1):
    omBL1=180+(h1om-theta1)  #omega in frame of Busing-Levy definitions
    omBL2=180+(h2om-theta2)

uNu1=zeros((3,1))
uNu1[0][0]=cos(deg2rad(omBL1))*cos(deg2rad(h1mu)) * scattSign
uNu1[1][0]=-1*sin(deg2rad(omBL1))*cos(deg2rad(h1nu)) + cos(deg2rad(omBL1))*sin(deg2rad(h1mu))*sin(deg2rad(h1nu)) * scattSign
uNu1[2][0]=sin(deg2rad(omBL1))*sin(deg2rad(h1nu)) + cos(deg2rad(omBL1))*sin(deg2rad(h1mu))*cos(deg2rad(h1nu)) * scattSign

uNu2=zeros((3,1))
uNu2[0][0]=cos(deg2rad(omBL2))*cos(deg2rad(h2mu)) * scattSign
uNu2[1][0]=-1*sin(deg2rad(omBL2))*cos(deg2rad(h2nu)) + cos(deg2rad(omBL2))*sin(deg2rad(h2mu))*sin(deg2rad(h2nu)) * scattSign
uNu2[2][0]=sin(deg2rad(omBL2))*sin(deg2rad(h2nu)) + cos(deg2rad(omBL2))*sin(deg2rad(h2mu))*cos(deg2rad(h2nu)) * scattSign

#Coordinates of the reflections in the cartesian system of the crystal
h1c=dot(B,h1)
h2c=dot(B,h2)

"""
print '\n\nh1c'
print h1c
print '\nh2c'
print h2c
"""

#Construction of T_(crystal cartesian)
Tc=zeros((3,3))
t1c=h1c/linalg.norm(h1c)
Tc[0][0]=t1c[0]
Tc[1][0]=t1c[1]
Tc[2][0]=t1c[2]

t3c=cross(h1c.T,h2c.T)   / linalg.norm(cross(h1c.T,h2c.T))
Tc[0][2]=t3c[0][0]
Tc[1][2]=t3c[0][1]
Tc[2][2]=t3c[0][2]

t2c=-1* cross(t1c.T,t3c) / linalg.norm(cross(t1c.T,t3c))
Tc[0][1]=t2c[0][0]
Tc[1][1]=t2c[0][1]
Tc[2][1]=t2c[0][2]

#Constructions of T_(phi cartesian)
Tphi=zeros((3,3))
t1phi=uNu1/linalg.norm(uNu1)
Tphi[0][0]=t1phi[0]
Tphi[1][0]=t1phi[1]
Tphi[2][0]=t1phi[2]

t3phi=cross(uNu1.T,uNu2.T) / linalg.norm(cross(uNu1.T, uNu2.T))
Tphi[0][2]=t3phi[0][0]
Tphi[1][2]=t3phi[0][1]
Tphi[2][2]=t3phi[0][2]

t2phi=-1*cross(t1phi.T,t3phi) / linalg.norm(cross(t1phi.T,t3phi))
Tphi[0][1]=t2phi[0][0]
Tphi[1][1]=t2phi[0][1]
Tphi[2][1]=t2phi[0][2]

U=dot(Tphi,linalg.inv(Tc))
"""
print '\n\nU:'
print U

print '\n\nUB:'
print dot(U,B)
"""

UB=dot(U,B)

###########################################
### CALCULATION OF ANGELS FOR [HKL, E]  ###
###########################################

#Definition of reciprocal lattice point, dE, Ei

print(hkl)
dE=0 #[meV]
Ei=13.6 #[meV]
Ef=Ei-dE

#End of definition

# Calculate the angles

#     Wavelength and wavevector
lam_i=sqrt(81.808/Ei)
lam_f=sqrt(81.808/Ef)
ki=2*pi/lam_i
kf=2*pi/lam_f

#   Scattering angle
qabs=linalg.norm(dot(B,hkl.T))
phi=rad2deg( arccos( (pow(ki,2) + pow(kf,2) - pow(qabs,2))/(2*ki*kf) ) ) * scattSign
print('phi: {0}'.format(phi))
#   Theta angle
theta = rad2deg( arctan( (ki-kf*cos(deg2rad(phi))) / ( kf * sin(deg2rad(phi)) ) ) )
if scattSign == -1:
    theta = 180+theta
print('theta: {0}'.format(theta))

#   Vector normal to the plane h1 h2
uh1nu=dot(UB,h1) / linalg.norm( dot(UB,h1) )    #h1 in the nu coordinate system
uh2nu=dot(UB,h2) / linalg.norm( dot(UB,h2) )    #h2 in the nu coordinate system
uPlaneNormal=cross(uh1nu.T, uh2nu.T)
print('uh1nu')
print(uh1nu)
print('uh2nu')
print(uh2nu)
print('uPlaneNormal')
print(uPlaneNormal)

#   Normalized Q  (u1nu)in the nu coordinate system:
u1nu = dot( UB, hkl.T) / linalg.norm( dot( UB, hkl.T) )
print('u1nu')
print(u1nu)
#   u2nu (perpendicular to (u1nu anduPlaneNormal)
u2nu = cross(uPlaneNormal, u1nu.T)
print('u2nu')
print(u2nu)


#   Calculate the T matrix
T=zeros((3,3))
#       First column: u1nu
T[0][0]=u1nu[0][0]
T[1][0]=u1nu[1][0]
T[2][0]=u1nu[2][0]
#       Second column: u2nu
T[0][1]=u2nu[0][0]
T[1][1]=u2nu[0][1]
T[2][1]=u2nu[0][2]
#       Third column: cross(u1nu, u2nu)
t3nu=cross(u1nu.T, u2nu)
print('t3nu')
print(t3nu)
T[0][2]=t3nu[0][0]
T[1][2]=t3nu[0][1]
T[2][2]=t3nu[0][2]

#   Calculation of the R matrix
R=linalg.inv(T)

if scattSign==-4:
    print('\nlefut\n')
    R[0][0]=R[0][0]*(-1)
    R[1][0]=R[0][0]*(-1)
    R[2][0]=R[0][0]*(-1)
    
#   Calculation of the angles
mu=rad2deg( arctan(-1*R[2][0] / (sqrt(pow(R[0][0],2) + pow(R[1][0],2) ) )) )
nu=rad2deg( arctan(R[2][1] / R[2][2] ) )
omega=rad2deg( arctan(R[1][0] / R[0][0] ) )
print('omega: {0}'.format(omega))
s=omega + theta
print('s: {0}'.format(s))






























