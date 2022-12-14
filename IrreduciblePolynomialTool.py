"""
Version: 15 November 2022
Author: Ethan S. Lee
"""

from scipy.special import zeta, zetac, polygamma, factorial, erfc
from numpy import sqrt
import sympy as sym
import mpmath as mpm
import numpy as np
from math import ceil
from pprint import pprint
from mpmath import mpf, nstr, fprod, fsum, fdiv, power, factorial, fmul, fdiv, exp, log, sqrt, pi, erfc, euler, gamma, polyroots

mpm.mp.dps = 100

#A useful function to convert numerical inputs into LaTeX strings with nice formatting.
def latex_float(f,we):
    float_str = format(float(f),we)
    if "E" in float_str:
        base, exponent = float_str.split("E")
        return r"${0}\cdot 10^{{{1}}}$".format(base, int(exponent))
    else:
        return float_str

#The following functions lead to the definition of LambdaK, an important constant.
def em(n):
    return power(pi/4,n)*fdiv(power(n,2*n),power(factorial(n),2))
def Nchoice(n):
    Ns = [2,3,4,5,6,7]
    Ds = [3,23,117,1609,9747,184607]
    if n in Ns:
        d = Ds[n-2]
    else:
        d = em(n)
    return d  
def g_plus(n):
    return 5/8 + fdiv(pi,2) + fdiv(1,n) + 3/(8*power(n,2))
def g_minus(n):
    return 5/8 + fdiv(pi,2) - fdiv(1,n) + 3/(8*power(n,2))
def littlelambdaK(n):
    if n <= 13:
        return power(n+1,fdiv(1,2)-fdiv(1,2*n))*sqrt(g_minus(n))*exp(n*(2.27+fdiv(4*n,n-1)+fdiv(0.01,power(n,2))+fdiv(1,500*power(n,6))))
    elif n > 13:
        return power(n+1,n-fdiv(1,2)-fdiv(1,2*n))*sqrt(g_plus(n))*exp(4.13*n+fdiv(0.02,n))
def LambdaK(n):
    return 0.54*fdiv((3*n-1)*littlelambdaK(n),power(log(em(n)),n-1)*power(n-1,2))*power(n,3/2)*factorial(n)

#The following functions are needed for A2, L: c, d, disc are leading coefficient, degree, and discriminant respectively.
def M1(t):
    counter = 0.0
    for p in sym.primerange(2, t+0.01):
        counter += np.log(p) / p
    return counter
def weighted_disc(c,d,disc):
    return power(abs(c),(d-1)*(d-2))*abs(disc)
def LambdaF(c,d,disc):
    if d == 1:
        return 0
    else:
        return LambdaK(d) * power(weighted_disc(c,d,disc),1/(d+1)) * power(log(weighted_disc(c,d,disc)),d-1)
def CF(d):
    return 1.38*fdiv((d+1)**2,d-1) + 1.52*d*(d-1) + 111.26*d
def QF(c,d,disc,GRH):
    if GRH == False:
        return d*(M1(abs(c)) + M1(sqrt(weighted_disc(c,d,disc))) + 2.52) + 1 + LambdaF(c,d,disc)*sqrt(weighted_disc(c,d,disc))
    else:
        return d*(M1(abs(c)) + M1(sqrt(weighted_disc(c,d,disc))) + 10.79) + log(2) + 4.79*log(weighted_disc(c,d,disc))

#These are L, A1, A2.
def A2(c,d,disc,g,GRH,fctrs=[]):
    if g == 1:
        return 2*max(max(1,d-1)*log(max(2,sqrt(weighted_disc(c,d,disc)))), QF(c,d,disc,GRH))
    else:
        st = [QF(c_factor,d_factor,disc_factor,GRH) for c_factor,d_factor,disc_factor in fctrs]
        return 2*(max(g,d-1)*log(max(2,sqrt(weighted_disc(c,d,disc)))) + g*max(st)) #Complicated because of factors, deal with this later!
def L(c,d,disc,g):
    return A2(c,d,disc,g,GRH)

#These are all of the m-functions we need in the end.
def m0(w,g,A1,A2,L):
    k0 = 10**4
    summ = 0
    for j in range(2, k0+1):
        summ += fdiv(power(A1,j-2)*power(A2,j-2),j*power(log(w),j-2))
    summ += fdiv(power(A1,k0-1)*power(A2,k0-1),power(log(w),k0-1))*((k0+1)*power(1-fdiv(A1*A2,log(w)),-1))
    out = max(fdiv(A2,log(w)) + fdiv(A1*A2,log(w))*(g + fdiv(A2,log(w))), fdiv(L,log(w))) + fdiv(3*g,2*power(log(w),2))
    out += g*log(fdiv(w,w-1))
    out += fdiv(power(A1,2)*A2,log(w))*(g + fdiv(A2,log(w)))*summ
    return out
def m0_hat(w,g,A1,A2,L):
    return log(w)*(power(1+fdiv(1,power(log(w),2)),g)*(1+m0(w,g,A1,A2,L)*exp(m0(w,g,A1,A2,L))) - 1)
def m1(x,d,g,A1,A2,L):
    return A2*(g*log(2) + fdiv(A2,log(sqrt(fdiv(x,d)))) + fdiv(A1*A2,log(sqrt(fdiv(x,d))))*(g + fdiv(A2,log(sqrt(fdiv(x,d))))))
def m2(g,A1,A2,L):
    return fdiv(exp(fdiv(A2,log(2))*(1 + A1*g + fdiv(A1*A2,log(2)))),power(log(2),g))
def m4(g,A1,A2,L):
    return 2*g*exp(1) + fdiv(A2*exp(1),log(2)) + log(2)
def m3(z,lam,g,A1,A2,L):
    return 1 + 2*power(m4(g,A1,A2,L),g)*exp(fdiv(A2,log(2))*(1 + A1*g + fdiv(A1*A2,log(2))) + fdiv(L,log(2)) - lam + exp(lam)*(fdiv(2*g,lam) + fdiv(A2,log(z))))
def r(z,g,A1,A2,L):
    return fdiv(A2 + m1(1,1/2,g,A1,A2,L),log(z))
def m7(z,g,A1,A2,L):
    return fdiv(exp(fdiv((g+1)*r(z,g,A1,A2,L),1-r(z,g,A1,A2,L)))-1,log(z))
def m6(z,g,A1,A2,L):
    return fdiv(r(z,g,A1,A2,L)*log(z),1-r(z,g,A1,A2,L)) + m7(z,g,A1,A2,L) + fdiv(m7(z,g,A1,A2,L)*r(z,g,A1,A2,L),1-r(z,g,A1,A2,L))
def m5(z,lam,g,A1,A2,L):
    t1 = log(z)*(fdiv(m3(z,lam,g,A1,A2,L),exp(g*euler*gamma(g+1)))*(1 + fdiv(m0_hat(z,g,A1,A2,L),log(z))) - 1)
    t2 = m6(z,g,A1,A2,L)*power(1+fdiv(m6(z,g,A1,A2,L),log(z)),-1)
    return min(t1,t2)
def m8(z,X,lam,g,A1,A2,L):
    out = fdiv(2*m5(z,lam,g,A1,A2,L),1-fdiv((4*g+1)*log(log(X)),log(X))) 
    out += fdiv(power(2,-4*g)*power(m2(g,A1,A2,L),4),gamma(g+1)*exp(g*euler))*(1 + fdiv(m0_hat(z,g,A1,A2,L),log(z)))
    return out
def m9(X,g,A1,A2,L):
    return fdiv(4*g+1,1-fdiv((4*g+1)*log(log(X)),log(X)))

def X0_min(a,b):
    return exp(a*power(10,b))
def c0(z,X,lam,g,A1,A2,L):
    return m9(X,g,A1,A2,L) + fdiv(m8(z,X,lam,g,A1,A2,L),log(log(X))) + fdiv(m8(z,X,lam,g,A1,A2,L)*m9(X,g,A1,A2,L),log(log(X)))
def mF(coefficients,x,d):
    summ = 0
    for i in range(1,d+1):
        summ += fdiv(abs(coefficients[i]),coefficients[0])
    return max(power(x,fdiv(1,2*(d-1))), 2*summ)
def c1(X,d,L,coefficients):
    return exp(2*L*(2 + L))*mF(coefficients,X,d)*fdiv(log(X),X)
def c2(z,X,d,lam,g,A1,A2,L,coefficients):
    return c0(z,X,lam,g,A1,A2,L)*(1+fdiv(c1(X,d,L,coefficients),2)) + fdiv(c1(X,d,L,coefficients)*log(X),2*log(log(X)))
def c3(z,X,lam,g,A1,A2,L):
    return 2.00001*(1 + fdiv(c0(z,X,lam,g,A1,A2,L)*log(log(X)),log(X)))
		
def irreducible_polynomial_values(coefficients=[1,0,3], discF=-12, starters=[6.0,40]):
    lcF = coefficients[0]
    degF = len(coefficients) - 1
    wdiscF = weighted_disc(lcF, degF, discF)
    fin_g = 1
    fin_A1 = degF + 1
    GRH_assumed_set = [False, True]
    
    print("degF: ", degF)
    print("lcF: ", lcF)
    print("wdiscF: ", wdiscF)
    print("\n")
    
    for GRH_assumed in GRH_assumed_set:
        fin_A2 = A2(lcF,degF,discF,fin_g,GRH_assumed)
        fin_L = A2(lcF,degF,discF,fin_g,GRH_assumed)

        print("GRH assumed: ", GRH_assumed)
        print("\n")
        print("log(A1): ", latex_float(log(fin_A1),"E"))
        print("log(A2): ", latex_float(log(fin_A2),"E"))
        print("log(L): ", latex_float(log(fin_L),"E"))

        #First, we need to find minimal choices for (a,b) such that exp(a*power(10,b)) satisfies some conditions..
        a_start = starters[0]
        b_start = starters[1]

        print("... computing minimal power ...")
        conds_hold = True
        while conds_hold == True:
            z0 = sqrt(fdiv(X0_min(a_start,b_start),power(log(X0_min(a_start,b_start)),4*fin_g+1)))
            checks = []
            if z0 > max(2,exp(fin_A1*fin_A2)):
                if r(z0,fin_g,fin_A1,fin_A2,fin_L) < 1:
                    if m0_hat(z0,fin_g,fin_A1,fin_A2,fin_L) < log(z0):
                        if abs(fdiv((fin_g+1)*r(z0,fin_g,fin_A1,fin_A2,fin_L),1-r(z0,fin_g,fin_A1,fin_A2,fin_L))) < 1:
                            b_start -= 1
                        else:
                            conds_hold = False
                    else:
                        conds_hold = False
                else:
                    conds_hold = False
            else:
                conds_hold = False
        b_start += 1
        print("... ", b_start, " ...")

        print("... computing minimal coefficient ...")
        conds_hold = True
        while conds_hold == True:
            z0 = sqrt(fdiv(X0_min(a_start,b_start),power(log(X0_min(a_start,b_start)),4*fin_g+1)))
            checks = []
            if z0 > max(2,exp(fin_A1*fin_A2)):
                if r(z0,fin_g,fin_A1,fin_A2,fin_L) < 1:
                    if m0_hat(z0,fin_g,fin_A1,fin_A2,fin_L) < log(z0):
                        if abs(fdiv((fin_g+1)*r(z0,fin_g,fin_A1,fin_A2,fin_L),1-r(z0,fin_g,fin_A1,fin_A2,fin_L))) < 1:
                            a_start -= 0.1
                        else:
                            conds_hold = False
                    else:
                        conds_hold = False
                else:
                    conds_hold = False
            else:
                conds_hold = False
        a_start += 0.1
        print("... ", a_start, " ...")

        #Second, use the above to set the value of X0 and compute values for each m_i..
        X0 = exp(a_start*power(10,b_start))
        z0 = sqrt(fdiv(X0,power(log(X0),4*fin_g+1)))
        
        print("\n")
        print("log(m0_hat): ", latex_float(log(m0_hat(z0,fin_g,fin_A1,fin_A2,fin_L)),"E"))
        print("log(m2): ", latex_float(log(m2(fin_g,fin_A1,fin_A2,fin_L)),"E"))
        print("log(m3): ", latex_float(log(m3(z0,2,fin_g,fin_A1,fin_A2,fin_L)),"E"))
        print("log(m4): ", latex_float(log(m4(fin_g,fin_A1,fin_A2,fin_L)),"E"))
        print("log(m5): ", latex_float(log(m5(z0,2,fin_g,fin_A1,fin_A2,fin_L)),"E"))
        print("log(m6): ", latex_float(log(m6(z0,fin_g,fin_A1,fin_A2,fin_L)),"E"))
        print("log(m8): ", latex_float(log(m8(z0,X0,2,fin_g,fin_A1,fin_A2,fin_L)),"E"))
        print("m9: ", latex_float(m9(X0,fin_g,fin_A1,fin_A2,fin_L),"E"))
        print("\n")
        print("log(c0): ", latex_float(log(c0(z0,X0,2,fin_g,fin_A1,fin_A2,fin_L)),"E"))
        print("log(c1/2): ", latex_float(log(c1(X0,degF,fin_L,coefficients)/2),"E"))
        print("log(c2): ", latex_float(log(c2(z0,X0,degF,2,fin_g,fin_A1,fin_A2,fin_L,coefficients)),"E"))
        print("\n")
				
#Run the following commands to obtain the results in Corollary 1.1 (or change the input polynomial as you choose)..
irreducible_polynomial_values([1,0,3],12,[6.0,40]) 			#This corresponds to k^2 + 3
#irreducible_polynomial_values([1,0,0,-5], 675, [9.9,55]) 		#This corresponds to k^3 - 5
#irreducible_polynomial_values([1,0,0,0,0,3],253125, [9.9,100]) 	#This corresponds to k^5 + 3
#irreducible_polynomial_values([2,0,0,0,0,0,3],-362797056,[9.9,120]) 	#This corresponds to 2*k^6 + 3
