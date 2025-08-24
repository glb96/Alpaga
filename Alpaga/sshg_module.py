#!/usr/bin/python
# -*- coding: utf-8 -*-

# Alpaga
# AnaLyse en PolArisation de la Generation de second hArmonique 

import numpy as np
from scipy.optimize import curve_fit

############################################################################################
############################################################################################
############################################################################################

#ai calculation (biblio these Aurelie Bruyere p70 à 81, Bruyère, A. (2016). Génération de second harmonique sur des films moléculaires chiraux (Doctoral dissertation, Université de Lyon).)

def r_s(n1,n2,angle_1,angle_2): #Fresnel coeff for a sagittal reflected wave
    return (n1*np.cos(angle_1) - n2*np.cos(angle_2))/(n1*np.cos(angle_1) + n2*np.cos(angle_2))

def r_p(n1,n2,angle_1,angle_2): #Fresnel coeff for a parallel reflected wave
    return -(n2*np.cos(angle_1) - n1*np.cos(angle_2))/(n1*np.cos(angle_2) + n2*np.cos(angle_1))

def t_s(n1,n2,angle_1,angle_2): #Fresnel coeff for a sagittal transmited wave
    return 2*n1*np.cos(angle_1)/(n1*np.cos(angle_1) + n2*np.cos(angle_2))

def t_p(n1,n2,angle_1,angle_2): #Fresnel coeff for a parallel transmited wave
    return 2*n1*np.cos(angle_1)/(n2*np.cos(angle_1) + n1*np.cos(angle_2))

############################################################################################
############################################################################################
############################################################################################

# Calcul des coeff de fresnel "modifié" (ai) par le modèle de la feuille de polarisation
def ai_coeff(angle1,n1,n2,N1,N2):
    """
    From the experimental angle of incidence and the refractive index values of the materials 
    (for both the fundamental and harmonic wavelengths), compute the *ai* coefficients and 
    the reflection angle of the harmonic wave.  

    For details of the calculation, see Aurélie Bruyère's thesis, pp. 70–81.
     
    Parameters
    ----------
    angle1 : float
        Experimental angle of incidence.
    n1 : float
        Refractive index of medium 1 at the fundamental wavelength.
    n2 : float
        Refractive index of medium 2 at the fundamental wavelength.
    N1 : float
        Refractive index of medium 1 at the harmonic wavelength.
    N2 : float
        Refractive index of medium 2 at the harmonic wavelength.
    
    Returns
    -------
    ai : list 
        A list containing the computed *ai* coefficients and the reflection angle of the harmonic wave.  
        The structure of the list is:  

        ``[a1, a2, a3, a4, a5, reflection_angle]``.
    """
    nm=(n1+n2)/2 #refractive index mean value between medium 1 and 2 for fundamental wave
    Nm=(N1+N2)/2 #refractive index mean value between medium 1 and 2 for harmonic wave
    
    angle_1=angle1*np.pi/180
    
    arg_angle_m = n1*np.sin(angle_1)/nm
    arg_angle_2 = n1*np.sin(angle_1)/n2
    
    if arg_angle_m < -1 or arg_angle_m > 1 or arg_angle_2 < -1 or arg_angle_2 > 1:
        raise Exception("Total reflection condition")
    
    angle_m = np.arcsin(n1*np.sin(angle_1)/ nm)
    angle_2 = np.arcsin(n1*np.sin(angle_1)/ n2)
    
    arg_ANGLE_M = nm*np.sin(angle_m)/Nm
    
    if arg_ANGLE_M < -1 or arg_ANGLE_M > 1 :
        raise Exception("Total reflection condition")  
    
    ANGLE_M = np.arcsin(nm*np.sin(angle_m)/Nm)
    
    arg_ANGLE_1 = Nm*np.sin(ANGLE_M)/N1
    arg_ANGLE_2 = Nm*np.sin(ANGLE_M)/N2
    
    if arg_ANGLE_1 < -1 or arg_ANGLE_1 > 1 or arg_ANGLE_2 < -1 or arg_ANGLE_2 > 1:
        raise Exception("Total reflection condition")
    
    ANGLE_1 = np.arcsin(Nm*np.sin(ANGLE_M)/N1)
    ANGLE_2 = np.arcsin(Nm*np.sin(ANGLE_M)/N2)
    
    e_x = t_p(n1,nm,angle_1,angle_m) * (r_p(nm,n2,angle_m,angle_2) - 1) * np.cos(angle_m)
    e_y = t_s(n1,nm,angle_1,angle_m) * (r_s(nm,n2,angle_m,angle_2) + 1)
    e_z = t_p(n1,nm,angle_1,angle_m) * (r_p(nm,n2,angle_m,angle_2) + 1) * np.sin(angle_m)

    E_x = t_p(Nm,N1,ANGLE_M,ANGLE_1) * (r_p(Nm,N2,ANGLE_M,ANGLE_2) - 1) * np.cos(ANGLE_M)
    E_y = t_s(Nm,N1,ANGLE_M,ANGLE_1) * (r_s(Nm,N2,ANGLE_M,ANGLE_2) + 1)
    E_z = t_p(Nm,N1,ANGLE_M,ANGLE_1) * (r_p(Nm,N2,ANGLE_M,ANGLE_2) + 1) * np.sin(ANGLE_M)

    a1 = e_y * e_z * E_y
    a2 = - 2 * e_x * e_z * E_x
    a3 = e_x * e_x * E_z
    a4 = e_z * e_z * E_z
    a5 = e_y * e_y * E_z
    
    return [a1,a2,a3,a4,a5,ANGLE_1]

############################################################################################
############################################################################################
############################################################################################

#Definition of fiting equation for S and P polarisation
def fit_polaS(x, chi_XXZ, ai):
    """
    Defines the theoretical equation for S-polarized SHG intensity.
   
    Parameters
    ----------
    x : list
        The polarization angles of the fundamental wave, in degrees.
    chi_XXZ : float
        The value of the chi_XXZ tensor element.
    ai : list
        List of the ai coefficients, with the same structure as the output of *sshg_module.ai_coeff*.
    
    Returns
    -------
    y : list
        The S-polarized SHG intensity corresponding to the input angles.
    """
    X=[2*i for i in x]
    y = (ai[0]*np.sin(X)*chi_XXZ)**2
    return (y)
    
############################################################################################

def fit_polaP(x,  chi_XXZ, chi_ZXX, chi_ZZZ, ai):
    """
    Defines the theoretical equation for P-polarized SHG intensity.
   
    Parameters
    ----------
    x : list
        The polarization angles of the fundamental wave, in degrees.
    chi_XXZ : float
        The value of the chi_XXZ tensor element.
    chi_ZXX : float
        The value of the chi_ZXX tensor element.
    chi_ZZZ : float
        The value of the chi_ZZZ tensor element.
    ai : list
        List of the ai coefficients, with the same structure as the output of *sshg_module.ai_coeff*.
     
    Returns
    -------
    y : list
        The P-polarized SHG intensity corresponding to the input angles.
    """
    y = ((ai[1]*chi_XXZ+ai[2]*chi_ZXX+ai[3]*chi_ZZZ)*(np.cos(x))**2+ai[4]*chi_ZXX*(np.sin(x))**2)**2
    return (y)    

############################################################################################

def fit_pola45(x,  chi_XXZ, chi_ZXX, chi_ZZZ, ai):
    """
    Defines the theoretical equation for 45°-polarized SHG intensity.
   
    Parameters
    ----------
    x : list
        The polarization angles of the fundamental wave, in degrees.
    chi_XXZ : float
        The value of the chi_XXZ tensor element.
    chi_ZXX : float
        The value of the chi_ZXX tensor element.
    chi_ZZZ : float
        The value of the chi_ZZZ tensor element.
    ai : list
        List of the ai coefficients, with the same structure as the output of *sshg_module.ai_coeff*.
     
    Returns
    -------
    y : list
        The 45°-polarized SHG intensity corresponding to the input angles.
    """
    deuxX=[2*i for i in x]
    mix = ai[1]*chi_XXZ+ai[2]*chi_ZXX+ai[3]*chi_ZZZ
    y = ((mix*(np.cos(x))**2+ai[4]*chi_ZXX*(np.sin(x))**2+ai[0]*np.sin(deuxX)*chi_XXZ)/2)**2
    return y
    
############################################################################################
    
def analyse_polarization_SSHG(angle_incidence, n1_fonda, n2_fonda, n1_harmo, n2_harmo, L_polarisation_angle, L_intensity_S, L_intensity_P, XXZ=False) :
    """
    From the experimental angle of incidence, refractive indices of the materials 
    for fundamental and harmonic wavelengths, polarization angles, and the SSHG 
    Gaussian intensity, this function returns the ai coefficients and chi coefficients 
    for an isotropic, achiral interface. 
    Reference: Aurèlie Bruyere Thesis, pp. 70–81.
    
    Parameters
    ----------
    angle1 : float
        Experimental angle of incidence.
    n1 : float
        Refractive index of medium 1 for the fundamental wavelength.
    n2 : float
        Refractive index of medium 2 for the fundamental wavelength.
    N1 : float
        Refractive index of medium 1 for the harmonic wavelength.
    N2 : float
        Refractive index of medium 2 for the harmonic wavelength.
    L_polarisation_angle : list
        The polarization angles of the fundamental in degrees.
    L_intensity_S : list
        The SSHG intensity for S-polarized analyzer. The sizes of *L_polarisation_angle* 
        and *L_intensity_S* must match.
    L_intensity_P : list
        The SSHG intensity for P-polarized analyzer. The sizes of *L_polarisation_angle* 
        and *L_intensity_P* must match.
    XXZ : float or bool
        Optional parameter to fix the value of chi_XXZ. If, for example, the S polarization 
        is flat, this avoids fitting the noise and recovering a non-physical value. 
        By default, this is set to False, in which case chi_XXZ is extracted by fitting 
        the S polarization.
    
    Returns
    -------
    ai : list
        Contains the ai coefficients and the angle of the harmonic reflected wave.
        Structure:
        [a1,
         a2,
         a3,
         a4,
         a5,
         reflected angle of reflected wave]
    
    list_chi : list
        Contains two mathematical solutions for the chi coefficients.
        Structure:
        [chi_XXZ,
         chi_ZXX,
         chi_ZZZ,
         chi_XXZset2,
         chi_ZXXset2,
         chi_ZZZset2]
    """
    ai=ai_coeff(angle_incidence,n1_fonda,n2_fonda,n1_harmo,n2_harmo)
    
    L_angle_rad = [i*np.pi/180 for i in L_polarisation_angle]

    if XXZ==False:
        def helper_S(x, chi_XXZ): #fitting of chi parametre only (not a1 parametre)
            return(fit_polaS(x, chi_XXZ, ai))
    
        p_s, q_s = curve_fit(helper_S, L_angle_rad, L_intensity_S)
        XXZ = p_s[0]
        
    chi_XXZ=XXZ
    
    def helper_P(x, chi_ZXX, chi_ZZZ): #fitting of ZXX and ZZZ chi parametres only (not a2,3,4,5 and XXZ parametres)
        return fit_polaP(x, chi_XXZ, chi_ZXX, chi_ZZZ, ai)
    
    p_p, q_p = curve_fit(helper_P, L_angle_rad, L_intensity_P)
    ZXX = p_p[0]
    ZZZ = p_p[1]
    
    
    XXZset2=XXZ
    ZXXset2=-ZXX
    ZZZset2=(ai[1]*2*XXZ/ai[3]+ZZZ)*-1 #ZZZ'=-(2*a2*XXZ/a4+ZZZ)
    
    list_chi = [XXZ, ZXX, ZZZ, XXZset2, ZXXset2, ZZZset2]
    
    return ( ai, list_chi)
    
############################################################################################ 
