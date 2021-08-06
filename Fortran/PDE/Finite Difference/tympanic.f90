      program Wave_Equation
      !***************************************************************!
      !This program is the numerical solution to the one dimensional  !
      !equation of a mechanical wave, this to verify the vibrational  !
      !modes of that wave with special initial conditions to simulate !
      !the tympanic membrane.                                         !
      !                                                               !
      !The numerical solution was given by using the finite difference!
      !method.                                                        !
      !                                                               !
      !                                                               !
      !Created by Ricardo Leal, Abel Hernandez and Alexis Gomez.      !
      !e-mail: ricardo.lealpz@gmail.com                       22/05/20!
      !Github: github.com/ricardoleal20                               !
      !***************************************************************!


      implicit none 
      real*8 L,tf,u0,uf,vinitial,c,dx,dt,lambda,pi,erre,f,z,SC
      real*8 E,rho,miu,velocity,n,unumeric,ureal,error
      integer Nt,Nx,i,j
      real*8,dimension (10000,10000)::u
      real*8,dimension (10000)::x
      real*8,dimension (10000)::t

      open(unit=10, file="xVSuVSt.txt", status="unknown")
      open(unit=11, file="Graph.plt", status="unknown")
      open(unit=12, file="Graph2.plt", status="unknown")
      open(unit=100,file="uanalitic.txt", status="unknown")
      open(unit=200,file="diference_analitic.txt", status="unknown")
      open(unit=20, file='xvsu.txt', status='unknown')
      
      write(11,*) "set nokey"
      write(11,*) "set  zlabel 'u(x,t)'"
      write(11,*) "set xlabel 'x (meters)'"
      write(11,*) "set ylabel 't (seconds)'"
      !write(11,*) "set xrange[0:0.001]"
      write(11,*) "splot 'xVSuVSt.txt' ls 8"

      write(12,*) "set nokey"
      write(12,*) "set xlabel 'x (meters)'"
      write(12,*) "set ylabel 'u(x,t)'"
      !write(12,*) "set xrange[0:0.001]"
      write(12,*) "plot 'xvsu.txt' ls 8"

       !**********************!
       !Several values to use.!
       !**********************!
       L=4.0E-5 !Tense part.
       !L=0.001   !Flacid part.
       n=3 !Vibrational mode.
       t(1)=0   !Initial time.
       tf=2.42E-7
       pi=3.141592654
       u0=0 !The boundary condition u(0,t)
       uf=0 !The boundary condition u(L,t)
       vinitial=0  !Initil velocity in u(x,0)  
       E=2.0E+7 !Its the same for the both parts.
       rho=1000 !Tense part.
       !rho=1200 !Flacid part.
       miu=0.3  !Its the same for the both parts.
       c=sqrt((E/rho)*((1-miu)/((1+miu)*(1-2*miu)))) !Propagation velocity of the wave.
       Nx=1201 !Number of grids on the x dimension.
       Nt=1201 !Number of grids on the time.
       dx=L/(Nx-1) !Infinitesimal distance.
       dt=tf/(Nt-1) !Infinitesimal time.
       lambda=(c*dt/dx)**2 !Our stability condition.


       if (lambda.le.1) then !This check the stability condition.
            print*,'lamda is <0.5',lambda

       !*****************************************!
       !Discretization of the time and space.    !   
       !*****************************************!

       do i=1,Nx
            x(i)=(i-1)*dx
       end do 

       do j=1,Nt
            t(j)=(j-1)*dt
       end do


       !*******************************************************!
       !Cicle to put the initial and boundary conditions.      !
       !*******************************************************!

       do i=1,Nx
       u(i,1)=f(x(i),pi,n,L)  !u(x,0)=position in t=0
       u(i,2)=u(i,1)+dt*velocity(x(i),pi,n,L,c)
       end do 

       !This is for the boundary conditions of the system.
       do j=1,Nt
            u(1,j)=u0    
            u(Nx,j)=uf   
       end do 

       !**********************************************************!
       !The core of the simulation. The FD equations is here.     !
       !**********************************************************!
       do j=2,Nt-1
       do i=2,Nx-1      
       u(i,j+1)=2*u(i,j)-u(i,j-1)+lambda*(u(i+1,j)-2*u(i,j)+u(i-1,j))
       end do 
       end do

       do j=1,Nt
            do i=1,Nx
                  z=u(i,j)
                  write(10,*) x(i),t(j),z
                  write(20,*) x(i),z
            end do 
       end do 

       do j=1,Nt
            do i=1,Nx-1
                  unumeric=u(i,j)
                  ureal=cos((n*pi*c*t(j))/L)*sin((n*pi*x(i))/L)
                  write(100,*) x(i),ureal
            end do 
      end do 

      error=ABS((ureal-unumeric)/ureal)*100
    
    write(200,*) "Unumeric,   UReal,   %Error"
    write(200,*) unumeric,ureal,error
      

      !This part of the program is used to call Gnuplot to plot our data.
      call system('gnuplot -p Graph.plt')

      call system('gnuplot -p Graph2.plt')



      
      else 
            print*, "Lambda is >0.5", lambda
            print*, "The code its not going to work."
            print*, "Hint: c*dt<dx"
      end if 


       end program


       function f(xi,pi,n,L)
            implicit none 
            real*8 xi,f,pi,n,L
            integer i
            !f=sin(pi*xi)
            !f=sin(pi*xi)+0.5*sin(3*pi*xi)
            !f=sin((pi*xi)/L)
            f=sin((n*pi*xi)/L)
            !f=0
            !do i=1,int(n)
            !     f=f+sin((n*pi*xi)/L)
            !end do
            return
      end function

      function velocity(xi,pi,n,L,c)
            implicit none
            real*8 velocity,xi,pi,L,n,c
            integer i
            !velocity=((n*pi*xi)/L)*sin((n*pi*xi)/L)
            !velocity=4*pi*sin(2*pi*xi)
            velocity=0
            !do i=1,int(n)
            !   velocity=velocity+((n*pi*c)/L)*sin((n*pi*xi)/L)
            !end do 
            return
            end function






