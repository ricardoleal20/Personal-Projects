!---------------------------------------------------------------!
!This program was made to get the numerical aproximation of a   !
!bar with one radiating end. In this case, the initial temperat-!
!ure distribution is f(x)=x(1-x).                               !
!                                                               !
!The numerical solution was given by using the finite difference!
!method.                                                        !
!                                                               !
!                                                               !
!Created by Ricardo Leal.                                       !
!e-mail: ricardo.lealpz@gmail.com                       13/09/20!
!Github: github.com/ricardoleal20                               !
!---------------------------------------------------------------!


program Heat_Equation
implicit none
real*8::L,der,f,c,k,dx,dt,lambda,n,tf
integer*8::i,j,Nx,Nt,NTerm

real*8,dimension(10000,10000)::u
real*8,dimension(10000,10000)::Dxu
real*8,dimension(10000)::coef
real*8,dimension(10000)::miu
real*8,dimension(10000)::x
real*8,dimension(10000)::t

!open(unit=10, file='Heat3D.txt', status='unknown')
open(unit=11, file='Heat2D.txt', status='unknown')
open(unit=12, file='Graph2D.plt', status='unknown')

write(12,*) "set nokey"
write(12,*) "set  ylabel 'u(x,t)'"
write(12,*) "set xlabel 'x (meters)'"
write(12,*) "plot 'Heat2D.txt' ls 8"

!----------------------------!
!Some variables to use.      !
!----------------------------!

L=1 !Large of the bar.
c=1 !Velocity of propagation of the heat.
k=1 !Heat transfer constant.
n=5 !Terms of the Fourier series.
x(1)=0 !Initial distance of the bar.
t(1)=0 !Initial time of simulation.
tf=0.4 !Final time of simulation.
Nx=501 !Number of partitions in x.
Nt=501 !Number of partitions in t.
dx=L/(Nx-1)
dt=tf/(Nt-1)
lambda=c*(dt/dx) !Our stability condition.

miu(1)=2.0288
miu(2)=4.9132
miu(3)=7.9787
miu(4)=11.0855
miu(5)=14.2074

coef(1)=0.2133
coef(2)=0.1040
coef(3)=-0.0220
coef(4)=0.0187
coef(5)=-0.0083

NTerm=n

if (lambda.le.0.5) then
  print*,'lambda is <0.5',lambda
  
  !----------------------------------------------!
  !The discretization of the time and space.     !
  !----------------------------------------------!
  
  do i=1,Nx
   x(i)=(i-1)*dx
  end do 
  
  do j=1,Nt
   t(j)=(j-1)*dt
  end do
  
  
  !----------------------------------------------!
  !Boundary and initial conditions.              !
  !----------------------------------------------!
  
  do j=1,Nt
   u(1,j)=0
   Dxu(1,j)=0
   Dxu(Nx,j)=-k*u(Nx,j)
  end do
  
  do i=1,Nx
   u(i,1)=f(x(i),NTerm)
  end do
  
  !----------------------------------------------------------!
  !The core of the simulation. The FD equations is here.     !
  !----------------------------------------------------------!
  do j=2,Nt-1
  do i=2,Nx-1      
  u(i,j+1)=u(i,j)+(lambda**2)*(Dxu(i+1,j)-Dxu(i-1,j))
  
  !------------------------------------------!
  !Aproximation to the firs derivative.      !
  !------------------------------------------!
  
  Dxu(i,j)=(u(i+1,j)-u(i-1,j))/dx
  
  end do 
  end do

  do j=1,Nt
       do i=1,Nx
             der=u(i,j)
             !write(10,*) x(i),t(j),der
             if (der.GT.0) then
             write(11,*) x(i),der 
             end if
       end do
  end do 

  CALL SYSTEM('gnuplot -p Graph2D.plt')


else 
      print*, "Lambda is >0.5", lambda
      print*, "The code its not going to work."
      print*, "Hint: c*dt<dx"

end if
end program

function f(xi,NTerm)
real*8:: S,f,xi,n
integer*8:: i,j,Nx,Nt,NTerm
real*8,dimension(10000)::coef
real*8,dimension(10000)::miu
!This is the function f(x)=x(1-x).
!f=xi*(1-xi)

!This is the same function but calculate with Fourier Series.
do i=1,int(n)
 S=coef(i)*sin(miu(i)*xi)
 f=f+S
end do
end function
