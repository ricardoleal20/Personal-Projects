import math as math
import cmath as cmath

a=1         #This value is because we use the equation x**2+bx+c=0
b=-2        #Give an arbitrarie value for b.
c=1         #Give an arbitrarie value for c.

def solve_quad(b,c):
    """Solve a quadratic equation, x**2 + bx + c = 0.
    
    Parameters
    ----------
    b, c : float
       Coefficients
       
    Returns
    -------
    x1, x2 : float or complex
       Roots.
    """
    
    value=(b**2)-(4*c)
    
    if (value>=0):
        f_term=-b/2              #Is the first term to use to get the roots x1 and x2.
        s_root=math.sqrt(value)  #Is the root in the general formule.
        s_term=(s_root)/2        #Is the second term to use to get the roots.
    else:
        f_term=-b/2
        s_root=cmath.sqrt(value)
        s_term=(s_root)/2
    
    
    #Here we are going to put the exact solutions for the roots x1 and x2:
    #--------------------------------------------------------#
    #This is for x1.                                         #
    x1=f_term+s_term                                         #
    #--------------------------------------------------------#
    
    #--------------------------------------------------------#
    #This is for x2.                                         #
    x2=f_term-s_term                                         #
    #--------------------------------------------------------#
    
    return x1, x2

x1,x2=solve_quad(b,c)

print(x1)
print(x2)