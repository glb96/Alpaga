#!/usr/bin/python
# -*- coding: utf-8 -*-

# Alpaga
# AnaLyse en PolArisation de la Generation de second hArmonique 

import importlib
import numpy as np
import os 
import pickle
import time
from scipy.optimize import curve_fit

import matplotlib
import matplotlib.cm as cm
import matplotlib.pyplot as plt


############################################################################################     

def fct_polar_abc(L_x, a, b, c, alpha_0):
    '''
    Define the function using the a, b and c coefficient to describe the SHS intensity: ::
    
        x = (L_x-alpha_0)*np.pi/180
        L_y = a*(np.cos(x)**4) + b*((np.cos(x)**2)*(np.sin(x)**2)) + c*(np.sin(x)**4)
    
    Parameters
    ----------
    L_x: list
        The polarisation angle of the fundamental in degree. The angle shall be given in degrees!
    a: float
        The a parameter
    b: float
        The b parameter
    c: float
        The c parameter
    alpha_0:
        The polarization angle representing the real 'zero'. 
    Returns
    -------
    L_y: list
        The SHS intensity    
    '''
    x = (L_x-alpha_0)*np.pi/180
    L_y = a*(np.cos(x)**4) + b*((np.cos(x)**2)*(np.sin(x)**2)) + c*(np.sin(x)**4)
    return(L_y)

############################################################################################ 

def calc_i(L_x, L_y, alpha0):
    '''
    Compute the i0, i2 and i4 parameters: ::
    
        i0 = np.mean(L_y)
        i2 = 2*np.mean(L_y*np.cos(2*(np.pi/180)*(L_x-alpha0)))
        i4 = 2*np.mean(L_y*np.cos(4*(np.pi/180)*(L_x-alpha0)))
    
    Parameters
    ----------
    L_x: list
        The polarisation angle of the fundamental in degree. The angle shall be given in degrees!
    L_y: list
        The V (or P) polarization SHS intensity
    alpha0: float
        The polarization angle representing the real 'zero'. 
    Returns
    -------
    i0: float
        The i0 value    
    i2: float
        The i2 value
    i4: float
        The i4 value
    '''
    i0 = np.mean(L_y)
    i2 = 2*np.mean(L_y*np.cos(2*(np.pi/180)*(L_x-alpha0)))
    i4 = 2*np.mean(L_y*np.cos(4*(np.pi/180)*(L_x-alpha0)))
    return(i0, i2, i4)


############################################################################################ 

def analyse_polarization_SHS_V(L_angle, L_intensity, alpha_0=False, L_intensity_error=False):
    '''
    From the polarisation angle and the SHS gaussian intensity, return many properties. 
         
    
    Parameters
    ----------
    L_angle: list
        The polarisation angle of the fundamental in degree.
    L_intensity: list
        The HRS intensity. The size of *L_angle* and *L_intensity* shall match. 
    alpha_0: bool or float
        [Optional] If set to False, then the alph_0 is a fit parameter. If set to a float, the alpha_0 is not a free parameter, an is fixed to the given value. Note that this angle should be given in degree.
    L_intensity_error: bool or float
        [Optional] If set to False, then the uncertanty are not computed. If set to a list, the L_intensity_error is the list of the associated ABSOLUTE error relative to the intensity.
    Returns
    -------
    L_SHS_prop: list
        The list of the computed properties. L_SHS_prop = [a, b, c, Zeta, Depol, i0, i2, i4, alpha_0]
    L_SHS_prop_error: list
        The list of the error relative to the computed properties. L_SHS_prop_error = [a_verr, b_verr, c_verr, Zeta_serr, i0_serr, i2_serr, i4_serr]
    '''
    ################################################ Compute the values ############################################
    # Compute a, b, c
    
    if isinstance(L_intensity_error, bool):
        if isinstance(alpha_0, bool):
            p, q = curve_fit(fct_polar_abc, L_angle, L_intensity, bounds=([0, 0, 0, -180], [2*np.max(L_intensity), 2*np.max(L_intensity), 2*np.max(L_intensity), 180]))
        else: # alpha_0 is no longer a free parameter
            p, q = curve_fit(fct_polar_abc, L_angle, L_intensity, bounds=([0, 0, 0, alpha_0-0.0001], [2*np.max(L_intensity), 2*np.max(L_intensity), 2*np.max(L_intensity), alpha_0+0.0001]))
    else:
        if isinstance(alpha_0, bool):
            p, q = curve_fit(fct_polar_abc, L_angle, L_intensity, sigma=L_intensity_error, bounds=([0, 0, 0, -180], [2*np.max(L_intensity), 2*np.max(L_intensity), 2*np.max(L_intensity), 180]))
        else: # alpha_0 is no longer a free parameter
            p, q = curve_fit(fct_polar_abc, L_angle, L_intensity, sigma=L_intensity_error, bounds=([0, 0, 0, alpha_0-0.0001], [2*np.max(L_intensity), 2*np.max(L_intensity), 2*np.max(L_intensity), alpha_0+0.0001]))
    
    a, b, c, alpha_0 = p[0], p[1], p[2], p[3] 
    perr = np.diag(q) # Variance
    a_verr, b_verr, c_verr, alpha_0_verr = perr[0], perr[1], perr[2], perr[3]
    
    # Compute zeta and Depol
    
    Zeta = (b-a-c)/b
    Depol = c/a
    
    
  
    
    # i0, i2, i4 calculs with Fourier series
    trotter = -1
    while L_angle[trotter]-L_angle[0] >= 360: # to compute the parameter only in 1 frequency
        trotter = trotter - 1

    if trotter == -1:
        i0, i2, i4 = calc_i(L_angle, L_intensity, alpha_0)
    else:
        i0, i2, i4 = calc_i(L_angle[:trotter+1], L_intensity[:trotter+1], alpha_0)
    
    if isinstance(L_intensity_error, bool):
        L_SHS_prop = [a, b, c, Zeta, Depol, i0, i2, i4, alpha_0]
        L_SHS_prop_error = [0, 0, 0, 0, 0, 0, 0]
        return(L_SHS_prop, L_SHS_prop_error)
    
    #####################################################################################################################
    #i0 , i2, i4 calcul with a,b,c coefficients but prefer Fourrier series.
    
    
        # i0, i2, i4 calculs with a, b, c
    #i0_abc = ( 3*a + b + 3*c )/8
    #i2_abc = ( a - c )/2
    #i4_abc = ( a - b + c )/8
    
    #I4_abc = i4_abc/i0_abc
    
    #I4 = i4/i0
    #I4_abs_serr = np.sqrt( (( (4*b)/((3*a + 3*c + b )**2) )**2)*(a_verr + c_verr)     
    #                +  (( (-4*(a+c))/((3*a + 3*c + b )**2) )**2)*b_verr
    #                +  2*( (-16*b*(a+c))/((3*a + 3*c + b )**4) )*(q[0][1] + q[1][2])
    #                +  2*(( (4*b)/((3*a + 3*c + b )**2) )**2) *q[0][2]   
    #                 )
    #print('I4_abc: ', I4_abc, '+-', I4_abs_serr)
    #####################################################################################################################
    
    
    
    
    
    
    
    
    
    ################################################ Compute the uncertanties ############################################
    
    
    #standart deviation of Depol
    
    Depol_serr = np.sqrt( (c**2/a**4)*a_verr + c_verr/a**2 )
    
    
    
    #standart deviation of Zeta
    Zeta_serr = np.sqrt(   (a_verr + c_verr)/b**2  + ((a + b)/b**2)**2 * b_verr )
    ZetaH_serr = np.sqrt( ( 4/(a+c)**2 )*c_verr )   
    
    
    
    #Incertitude i0, i2, i4 using Intensity Residu
    L_res = L_intensity - (i0 + i2*np.cos(2*np.pi/180*(L_angle-alpha_0)) + i4*np.cos(4*np.pi/180*(L_angle-alpha_0)))
    s = np.std(L_res)
    
    i0_serr = s/(np.sqrt(len(L_res)))
    i2_serr = s/(np.sqrt(2*len(L_res)))
    i4_serr = s/(np.sqrt(2*len(L_res)))
    
    
    L_SHS_prop = [a, b, c, Zeta, Depol, i0, i2, i4, alpha_0]
    L_SHS_prop_error = [a_verr, b_verr, c_verr, Zeta_serr, Depol_serr, i0_serr, i2_serr, i4_serr]
    return(L_SHS_prop, L_SHS_prop_error)




def analyse_polarization_SHS_H(L_angle, L_intensity, alpha_0=False, L_intensity_error=False):
    '''
    From the polarisation angle and the SHS gaussian intensity, return many properties. 
    
    
    Parameters
    ----------
    L_angle: list
        The polarisation angle of the fundamental in degree.
    L_intensity: list
        The HRS intensity. The size of *L_angle* and *L_intensity* shall match. 
    alpha_0: bool or float
        [Optional] If set to False, then the alph_0 is a fit parameter. If set to a float, the alpha_0 is not a free parameter, an is fixed to the given value. Note that this angle should be given in degree.
    L_intensity_error: bool or float
        [Optional] If set to False, then the uncertanty are not computed. If set to a list, the L_intensity_error is the list of the associated ABSOLUTE error relative to the intensity.
    Returns
    -------
    L_SHS_prop: list
        The list of the computed properties. L_SHS_prop = [a, b, c, alpha_0, Zeta, Depol, i0, i2, i4]
    L_SHS_prop_error: list
        The list of the error relative to the computed properties. L_SHS_prop_error = [a_verr, b_verr, c_verr, Zeta_serr, i0_serr, i2_serr, i4_serr]
    '''
    ################################################ Compute the values ############################################
    # Compute a, b, c
    if isinstance(L_intensity_error, bool):
        if isinstance(alpha_0, bool):
            p, q = curve_fit(fct_polar_abc, L_angle, L_intensity, bounds=([0, 0, 0, -180], [2*np.max(L_intensity), 2*np.max(L_intensity), 2*np.max(L_intensity), 180]))
        else: # alpha_0 is no longer a free parameter
            p, q = curve_fit(fct_polar_abc, L_angle, L_intensity, bounds=([0, 0, 0, alpha_0-0.0001], [2*np.max(L_intensity), 2*np.max(L_intensity), 2*np.max(L_intensity), alpha_0+0.0001]))
    else:
        if isinstance(alpha_0, bool):
            p, q = curve_fit(fct_polar_abc, L_angle, L_intensity, sigma=L_intensity_error, bounds=([0, 0, 0, -180], [2*np.max(L_intensity), 2*np.max(L_intensity), 2*np.max(L_intensity), 180]))
        else: # alpha_0 is no longer a free parameter
            p, q = curve_fit(fct_polar_abc, L_angle, L_intensity, sigma=L_intensity_error, bounds=([0, 0, 0, alpha_0-0.0001], [2*np.max(L_intensity), 2*np.max(L_intensity), 2*np.max(L_intensity), alpha_0+0.0001]))
    
    a, b, c, alpha_0 = p[0], p[1], p[2], p[3] 
    perr = np.diag(q) # Variance
    a_verr, b_verr, c_verr, alpha_0_verr = perr[0], perr[1], perr[2], perr[3]
    
    # Compute zeta
   
   
    Zeta = (a-c) / (a+c)


    
    
       
    
    ################################################ Compute the uncertanties ############################################
    

    #standart deviation of Zeta
    
    Zeta_serr = np.sqrt( ( 4/(a+c)**2 )*c_verr )   
    
    
   
    
    L_SHS_prop = [a, b, c, Zeta,  alpha_0]
    L_SHS_prop_error = [a_verr, b_verr, c_verr, Zeta_serr]
    return(L_SHS_prop, L_SHS_prop_error)
