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
import matplotlib.pyplot as plt

from Alpaga.file_management import standard_file_name as standard_file_name
from Alpaga.file_management import third_floor_file_name_builder as third_floor_file_name_builder
from Alpaga.file_management import transform_name_file as transform_name_file
from Alpaga.file_management import find_file_iter_from_dir as find_file_iter_from_dir
from Alpaga.file_management import find_angle_iter_from_dir as find_angle_iter_from_dir

############################################################################################

try:
    from IPython.display import clear_output
except ImportError:
    # fallback for normal Python environment
    def clear_output(wait=False):
        pass  # do nothing
    
############################################################################################
    
############################################################################################
####################### Cleaning and averaging spectra #####################################
############################################################################################

def clean_spectra_mean_n(L_y, L_mean_cleaning_n=[1, 1, 1, 3], L_mean_cleaning_evo_max=[2, 1.5, 1.4, 1.3]):
    """
    Detect spikes in the list of data *L_y* using a local averaging method.  
    This method is designed to avoid removing features that are not actual spikes.  
    Instead of applying a single rough treatment, several small treatments are performed,  
    so that the spectra are affected as little as possible.  

    **Steps**
    
    1) For given *mean_cleaning_n* (integer) and *mean_cleaning_evo_max* (float),  
       the function scans the list *L_y* to clean.  
       For a value L_y[k], it computes the local average:

           ave_k = (L_y[k-mean_cleaning_n] + ... + L_y[k-1] + L_y[k+1] + ... + L_y[k+mean_cleaning_n]) / (2*mean_cleaning_n)

       i.e. the local average over 2*mean_cleaning_n neighbors, **excluding** the point k.

    2) The value L_y[k] is compared against mean_cleaning_evo_max × ave_k.  
       If L_y[k] is larger, it is considered a spike.  
       In this case, L_y[k] is replaced by ave_k **for the spike detection process only (not for the final analysis)**.  
       Spikes are stored in the list *L_population*: if L_population[k] = 0, point k is a spike, otherwise it is 1.  
       The averaging procedure will later use this list to remove the spikes.  

    3) For every *mean_cleaning_n* and *mean_cleaning_evo_max* declared in the input arguments  
       *L_mean_cleaning_n* and *L_mean_cleaning_evo_max*, steps (1) and (2) are repeated,  
       updating *L_y* when spikes are detected.  

    This multi-pass approach helps detect as many spikes as possible, while minimizing false positives.  
    A recommended strategy is to start with stricter parameters, and progressively decrease the threshold.  
    For example:  

        L_mean_cleaning_n = [1, 1, 1, 3]  
        L_mean_cleaning_evo_max = [2, 1.5, 1.2, 1.1]  

    performs 4 treatments.  
    The first 3 use only the two nearest neighbors (L_y[k-1] and L_y[k+1]) to compute the average.  
    In the first pass, a point is flagged as a spike if it is twice this local average.  
    In the second pass, the threshold is 1.5, then 1.2 in the third.  
    The final pass uses 6 neighbors and a 1.1 threshold.  

    This procedure was designed to catch spikes that may span 2–3 consecutive points (rare but possible).  
    It is recommended to experiment with *L_mean_cleaning_n* and *L_mean_cleaning_evo_max*  
    to ensure spikes are removed without altering the rest of the spectra.  
    For instance, try:  

        L_mean_cleaning_n = [1, 1, 1, 3]  
        L_mean_cleaning_evo_max = [2, 1.5, 1.1, 1.05]  

    to see the effect of overly strict parameters.  

    Parameters
    ----------
    L_y : list
        Data to clean.  
    L_mean_cleaning_n : list of int, optional
        List of neighborhood sizes for computing local averages.  
        Must have the same length as *L_mean_cleaning_evo_max*.  
    L_mean_cleaning_evo_max : list of float, optional
        List of maximum coefficients used for spike detection.  
        Values should generally be between 1.1 and 2–3.  
        A point is flagged as a spike if L_y[k] > coeff × local average.  

    Returns
    -------
    L_population : list
        List of the same size as *L_y*, initialized to 1.  
        If a spike is detected at position k, then L_population[k] = 0.  

    Examples
    --------
    For practical usage, see :ref:`alpaga.averaging_and_cleaning function<averaging_spectra_section>`.  

    Notes
    -----
    A Fourier-based cleaning method may be added in the future if requested.  
    However, for short acquisition times, it may distort the spectra.
    """
    L_y_clean = np.array(L_y)
    L_population = np.zeros(len(L_y)) + 1

    # Redefine the value if the old input type is used.
    if isinstance(L_mean_cleaning_n, int):
        L_mean_cleaning_n = [L_mean_cleaning_n]
        if not isinstance(L_mean_cleaning_evo_max, int) and not isinstance(L_mean_cleaning_evo_max, float):
            raise Exception('WARNING: If only one cleaning is required, both L_mean_cleaning_n and L_mean_cleaning_evo_max should be int or float. You should also define them as a list with a single element. Example: L_mean_cleaning_n = [3] and L_mean_cleaning_evo_max = [1.4].')
        else:
            L_mean_cleaning_evo_max = [L_mean_cleaning_evo_max]

    if not isinstance(L_mean_cleaning_n, list) or not isinstance(L_mean_cleaning_evo_max, list):
        raise Exception('WARNING: If several cleanings are required, both L_mean_cleaning_n and L_mean_cleaning_evo_max should be lists.')

    N_cleaning = len(L_mean_cleaning_n)
    for N_c in range(0, N_cleaning, 1):
        mean_cleaning_n_t = L_mean_cleaning_n[N_c]
        if not isinstance(mean_cleaning_n_t, int):
            raise Exception('WARNING: Every element of L_mean_cleaning_n should be an int!')
        for k in range(mean_cleaning_n_t, len(L_y)-mean_cleaning_n_t, 1):
            mean_t = np.mean(np.append(L_y_clean[k-mean_cleaning_n_t:k], L_y_clean[k+1:k+1+mean_cleaning_n_t])) # mean without the point k
            if L_y_clean[k] > mean_t * L_mean_cleaning_evo_max[N_c]:
                L_y_clean[k] = mean_t
                L_population[k] = 0

    return L_population


############################################################################################

def averaging_and_cleaning(name_file, N_iter, L_filename=False, extension='.dat',
                           fct_name=standard_file_name, type_cleaning='mean',
                           L_mean_cleaning_n=[1, 1, 1, 3], L_mean_cleaning_evo_max=[2, 1.5, 1.4, 1.3],
                           show_spectra='average', figure_counter=1):
    """
    For a set of acquisitions with filenames:
    
        *name_file* + '_' + i + *extension*,
    
    return the mean spectra cleaned of spikes. Currently, only one type of averaging and cleaning is available through *type_cleaning*, which is 'mean'.
    
    Each acquisition i is processed using the function :func:`alpaga.clean_spectra_mean_n` 
    with optional arguments *L_mean_cleaning_n* and *L_mean_cleaning_evo_max*, see :ref:`cleaning_averaging_spectra_page` 
    for details. Spikes are detected for each spectrum, and the mean is computed element-wise over all acquisitions, ignoring the spikes.
    
    Example:
    If there are 4 acquisitions, for the k-th element (e.g., wavelength 404 nm):
    
        - If no spikes are detected for all 4 acquisitions, the average is the mean of all 4 values.
        - If the second acquisition has a spike at this element, the average ignores the second acquisition **only for this element**.
        - If all 4 acquisitions have a spike at this element, it may indicate:
            * Detection parameters are too strict: decrease values in *L_mean_cleaning_evo_max*.
            * Acquisition time per spectrum is too long, increasing spike probability.
            * A serious detector issue or other abnormality (e.g., ISS data). 
    
    In such cases, a warning is printed, and the mean value is used for that element, but acquisition parameters should be reconsidered.
    
    Parameters
    ----------
    name_file : str
        Prefix for all acquisition filenames. Use absolute paths; see :ref:`file_management_page` for more details.
    N_iter : int or list of int
        Number of acquisitions to average. If a list is provided, only those iterations are processed.
    L_filename : bool or list of str
        If a list is provided, contains the absolute filenames to process, bypassing generated filenames.
    extension : str
        [Optional] File extension for data files.
    fct_name : function
        [Optional] Function used to generate a filename from prefix, iteration, and extension. Defaults to :func:`alpaga.standard_file_name`.
    type_cleaning : str
        [Optional] Currently only 'mean' is supported.
    L_mean_cleaning_n : list
        [Optional] See :func:`alpaga.clean_spectra_mean_n` for details.
    L_mean_cleaning_evo_max : list
        [Optional] See :func:`alpaga.clean_spectra_mean_n` for details.
    show_spectra : str
        [Optional] 'average' plots only the final averaged spectra, 'all' also plots spike detection for each iteration. Any other value disables plotting.
    figure_counter : int
        [Optional] Number of the first figure for plotting.
    
    Returns
    -------
    L_x_axis : list
        X-axis values from the spectra files.
    L_spectra_t : list
        Averaged and cleaned spectra.
    figure_counter : int
        Updated figure counter for subsequent plots.
    
    Examples
    --------
    ::
    
       names = 'Spectra_4.0'
       N_iter = 4
       L_lambda, L_spectra, _ = alpaga.averaging_and_cleaning(
           names, N_iter, extension='.dat', type_cleaning='mean',
           L_mean_cleaning_n=[1, 1, 1, 3], L_mean_cleaning_evo_max=[2, 1.5, 1.2, 1.1],
           show_spectra='all', figure_counter=10)
    """
    
    if not isinstance(L_filename, bool) and not L_filename:
        raise Exception('WARNING: L_filename is not defined correctly. It should be a non-empty list of strings!')
        
    if isinstance(N_iter, int):
        L_iter = [k for k in range(1, N_iter+1)]
        if show_spectra == 'all':
            print('Averaging will be done for iterations from 1 to', N_iter)
    elif isinstance(N_iter, list):
        L_iter = N_iter
        if show_spectra == 'all':
            print('Averaging will be done for iterations:', N_iter)
        
    if not isinstance(L_filename, bool) and L_filename:
        name_file_t = L_filename[0]
    else: 
        name_file_t = fct_name(name_file, angle=False, iteration=str(L_iter[0]), extension=extension)
        
    spectra = np.loadtxt(name_file_t)
    L_x_axis = spectra.T[0]
    n_lambda = len(L_x_axis)
        
    # Mean-type cleaning
    if type_cleaning == 'mean':
        L_population_t = np.zeros(n_lambda)
        L_spectra = np.zeros((len(L_iter), n_lambda))
        L_spectra_t = np.zeros(n_lambda)
        
        for i in range(len(L_iter)):
            if not isinstance(L_filename, bool) and L_filename:
                name_file_t = L_filename[0]
            else: 
                name_file_t = fct_name(name_file, angle=False, iteration=str(L_iter[i]), extension=extension)
            print(name_file_t)
            spectra = np.loadtxt(name_file_t, skiprows=0)
            
            if show_spectra == 'all':
                plt.figure(figure_counter)
                plt.title(name_file + '_' + str(L_iter[i]))
                plt.plot(L_x_axis, spectra.T[1])
                
            L_population = clean_spectra_mean_n(
                spectra.T[1],
                L_mean_cleaning_n=L_mean_cleaning_n,
                L_mean_cleaning_evo_max=L_mean_cleaning_evo_max
            )
            
            if show_spectra == 'all':
                plt.figure(figure_counter)
                for n in range(len(L_population)):
                    if L_population[n] == 0:
                        plt.plot([L_x_axis[n]], [spectra.T[1][n]], '*')
                figure_counter += 1
            
            L_spectra[i] = spectra.T[1]
            for n in range(len(L_population)):
                if L_population[n] == 0:
                    L_spectra[i][n] = 0
            L_population_t += L_population
            
        L_to_correct = []
        for n in range(len(L_population_t)):
            if L_population_t[n] == 0:
                print(f'Warning: For files with prefix {name_file}, a spike was detected at lambda {L_x_axis[n]} for all iterations! The returned value may not be meaningful.')
                L_population_t[n] = 1
                L_to_correct.append(n)
                    
        for i in range(len(L_iter)):
            L_spectra_t += L_spectra[i]
                
        L_spectra_t /= L_population_t
            
        for n in L_to_correct:  # Avoid zeros in spectra
            borne_min = n - 1
            borne_max = n + 1
            while L_spectra_t[borne_min] == 0:
                borne_min -= 1
            while L_spectra_t[borne_max] == 0:
                borne_max += 1
            L_spectra_t[n] = (L_spectra_t[borne_min] + L_spectra_t[borne_max]) / 2
    
    if show_spectra in ['all', 'average']: 
        plt.figure(figure_counter)
        plt.title(name_file)
        plt.plot(L_x_axis, L_spectra_t)
        figure_counter += 1
    
    return L_x_axis, L_spectra_t, figure_counter

        
############################################################################################
################################# Fit and noise   ##########################################
############################################################################################    

def remove_noise(L_x, L_y, l_cut=[380, 395, 419, 433], order_fit_noise=4, return_fit_noise=False, return_boundary=False, show_spectra=False , figure_counter=1):
    '''
    Remove the noise from a spectrum to make the Gaussian fit easier.
    
    The x-axis is given by *L_x* and the y-axis by *L_y*. Using the list *l_cut*, the spectrum is divided into three areas. 
    The first area is from *l_cut[0]* to *l_cut[1]*, the second from *l_cut[1]* to *l_cut[2]*, and the third from *l_cut[2]* to *l_cut[3]*. 
    The second area is the target area where the Gaussian is expected. The first and third areas are used to define the noise in the target area using a polynomial fit.
    
    This function first identifies the elements of the x-axis that correspond to the three areas. 
    To obtain these elements, set the optional parameter *return_boundary* to True. The function will then return the list *x_cut*, which can be used as follows to define the three areas: ::
        
        L_y_noise = np.append(L_y[x_cut[0]:x_cut[1]], L_y[x_cut[2]:x_cut[3]])  # first and last areas
        L_y_target = L_y[x_cut[1]:x_cut[2]]  # middle area containing the Gaussian
    
    Next, the first and last areas are fitted using a polynomial of order specified by the optional parameter *order_fit_noise*. 
    To obtain the fitted noise, set *return_fit_noise* to True. The function will then return *L_y_noise_fit*, which contains the polynomial values calculated over all three areas.
    
    Finally, the fitted noise is subtracted from all three areas. The first and last areas should be close to zero, while the middle area should contain a clean Gaussian. 
    If this is not the case, try adjusting the *l_cut* values to achieve a better noise fit.
    
    To plot the three areas and the polynomial fit, set *show_spectra* to 'all'. The initial figure number is given by *figure_counter*.
    
    The first returned list is *L_x_cleaned*, the x-axis starting from *l_cut[0]* to *l_cut[3]*.
    The second returned list is *L_y_cleaned*, the y-values with the noise subtracted, matching the size of *L_x_cleaned*.
    
    If *return_fit_noise* is True, the list *L_y_noise_fit* containing the polynomial fit is returned.
    
    If *return_boundary* is True, the list *x_cut*, containing the positions of the *l_cut* values in the original x-axis, is returned.
    
    In all cases, the last returned value is an integer, the next figure number for plotting, ensuring no conflicts with existing figures.
    
    Parameters
    ----------
    L_x: list
        The x-axis used to define the three areas.
    L_y: list
        The y-axis from which the noise will be removed.
    l_cut: list of float
        [Optional] Defines the three areas based on the values in *L_x*. Use actual x-values, not indices.
    order_fit_noise: int
        [Optional] Polynomial order for fitting the noise. Recommended values are 2, 3, or 4. The order has minimal impact if *l_cut* is well chosen.
    return_fit_noise: bool
        [Optional] If True, returns the noise fitted by a polynomial, *L_y_noise_fit*.
    return_boundary: bool
        [Optional] If True, returns *x_cut*, containing the element positions for defining the three areas.
    show_spectra: str
        [Optional] If 'all', plots the areas and polynomial fit.
    figure_counter: int
        [Optional] The starting figure number for plots.
    
    Returns
    -------
    L_x_cleaned: list
        The x-axis corresponding to the three areas.
    L_y_cleaned: list
        The y-values with noise removed, same length as *L_x_cleaned*.
    L_y_noise_fit: list
        The polynomial-fitted noise, returned if *return_fit_noise* is True.
    x_cut: list
        Positions defining the boundaries of the three areas, returned if *return_boundary* is True.
    figure_counter: int
        The next figure number for plotting.
    
    Examples
    --------
    See the tutorial for detailed examples. Example outputs depending on optional parameters: ::
    
        L_x_cleaned, L_y_cleaned, figure_counter = alpaga.remove_noise(L_lambda, L_spectra, l_cut=l_cut, order_fit_noise=order_fit_noise, return_fit_noise=False, return_boundary=False, show_spectra='all', figure_counter=1)
        L_x_cleaned, L_y_cleaned, L_y_noise_fit, figure_counter = alpaga.remove_noise(L_lambda, L_spectra, l_cut=l_cut, order_fit_noise=order_fit_noise, return_fit_noise=True, return_boundary=False, show_spectra='all', figure_counter=1)
        L_x_cleaned, L_y_cleaned, x_cut, figure_counter = alpaga.remove_noise(L_lambda, L_spectra, l_cut=l_cut, order_fit_noise=order_fit_noise, return_fit_noise=False, return_boundary=True, show_spectra='all', figure_counter=1)
        L_x_cleaned, L_y_cleaned, L_y_noise_fit, x_cut, figure_counter = alpaga.remove_noise(L_lambda, L_spectra, l_cut=l_cut, order_fit_noise=order_fit_noise, return_fit_noise=True, return_boundary=True, show_spectra='all', figure_counter=1)
    
    Note: All arguments must be defined prior in the code, see the tutorial.
    '''
    # find where to make the cut to define the noise
    N_lambda = len(L_x)
    KKK = 0
    trotter = 0
    x_cut = np.array([0, 0, 0, 0])
    while trotter<4 or KKK>N_lambda:
        if L_x[KKK] > l_cut[trotter]:
            x_cut[trotter] = int(KKK)
            trotter += 1
        KKK += 1
    L_x_cleaned = L_x[x_cut[0]:x_cut[3]]
    # Fit the noise:
    L_x_noise = np.append(L_x[x_cut[0]:x_cut[1]], L_x[x_cut[2]:x_cut[3]])
    L_y_noise = np.append(L_y[x_cut[0]:x_cut[1]], L_y[x_cut[2]:x_cut[3]])
    z = np.polyfit(L_x_noise, L_y_noise, order_fit_noise)
    p = np.poly1d(z)
    L_y_noise_fit = p(L_x_cleaned)
    L_y_cleaned = L_y[x_cut[0]:x_cut[3]]-L_y_noise_fit
    if show_spectra=='all':
        plt.figure(figure_counter)
        plt.plot(L_x_cleaned, L_y[x_cut[0]:x_cut[3]], 'r*', label='total')
        plt.plot(L_x_noise, L_y_noise, 'b*', label='noise areas')
        plt.plot(L_x_cleaned, L_y_noise_fit, 'k--', label='polynomial fit')
        plt.legend()
        figure_counter += 1
    if not return_fit_noise:
        if not return_boundary:
            return(L_x_cleaned, L_y_cleaned, figure_counter)
        else:
            return(L_x_cleaned, L_y_cleaned, x_cut, figure_counter)
    else:
        if not return_boundary:
            return(L_x_cleaned, L_y_cleaned, L_y_noise_fit, figure_counter)
        else:
            return(L_x_cleaned, L_y_cleaned, L_y_noise_fit, x_cut, figure_counter)

############################################################################################    

def fit_gausse(x, intensity, lambda_0, waist):
    '''
    Function used to define the Gaussian shape in Alpaga.
    
    y = intensity * np.exp(-((x - lambda_0) / waist) ** 2)
    
    Parameters
    ----------
    x: list
        The x values.
    intensity: float
        The Gaussian intensity, the parameter targeted by the whole procedure.
    lambda_0: float
        The position of the Gaussian maximum.
    waist: float
        The waist of the Gaussian.
    
    Returns
    -------
    y: list
        The computed Gaussian values.
    '''
    y=intensity*np.exp(-((x-lambda_0)/waist)**2)
    return(y)

############################################################################################    

def intensity_from_gaussian_integral(L_x_cleaned, L_y_cleaned, lambda_0, waist):
    '''
    Extract the Gaussian intensity using the integration method. 
    The integral is computed using the numpy.trapz function. 
    The intensity is then given by: ::
    
        I0 = integral_value / (waist * np.sqrt(np.pi))
    
    Note that in this procedure, no uncertainty calculations are yet implemented. 
    
    Parameters
    ----------
    L_x_cleaned: list
        The x-axis used to compute the integral. 
        This axis should contain at least the Gaussian peak.
    L_y_cleaned: list
        The y-axis used to compute the integral. 
        Usually, this is the output obtained from the :ref:`alpaga.remove_noise function<remove_noise_section>`. 
        Apart from the Gaussian curve, the other values should be as close to zero as possible. 
        Since the integration is performed over the entire list, non-zero values may affect the final intensity if their average is not zero.
    lambda_0: float
        Unused. This input is kept only for consistency with other methods.
    waist: float
        The waist of the Gaussian, used to extract the Gaussian intensity from the integral value. 
    
    Returns
    -------
    I0: float
        The computed Gaussian intensity.
    '''
    integral_value = np.trapz(L_y_cleaned, L_x_cleaned)
    # int exp(-alpha x**2) = sqrt(pi/alpha)
    # We use: I(x) = I0 exp(- (x-lambda_0)/waist))**2)
    # int I0 exp(- (x-lambda_0)/waist))**2) = I0 waist sqrt(pi)
    I0 = integral_value/(waist*np.sqrt(np.pi))
    return(I0)

############################################################################################    

def fit_gaussian_from_noise(L_x, L_y, l_cut=[380, 395, 419, 433], order_fit_noise=4, method_fit='fit_gauss',
                            bounds_fit_gausse=([0, 395, 1], [np.inf, 410, 25]), lambda_0_ref=403, waist_ref=2,
                            exclu_zone=False, fit_noise=False, show_spectra='all', figure_counter=1):
    '''
    This function returns the intensity *I0*, the maximum position *lambda_0*, and the width *waist* 
    of the Gaussian in *L_y*. The procedure first removes the noise using 
    :ref:`alpaga.remove_noise function<remove_noise_section>`, and then extracts the intensity.  
    Two methods are available to extract the intensity:

    1) If *method_fit* is set to 'fit_gauss':
        
        The intensity is extracted using *scipy.optimize.curve_fit*: ::
                    
            p, q = curve_fit(fit_gausse, L_x_cleaned, L_y_cleaned, bounds=bounds_fit_gausse) 
            I0, lambda_0, waist = p[0], p[1], p[2]
                
        Here, *fit_gausse* is defined in the analyze_run.fit_gausse function. The x and y inputs are the outputs of the cleaning 
        procedure (see :ref:`analyze_run.remove_noise function<remove_noise_section>`), and the bounds 
        are given by the *bounds_fit_gausse* parameter.  
        This method returns the Gaussian intensity *I0*, the central wavelength *lambda_0*, and the 
        width *waist*.  
        This approach is the most versatile and should generally be used first to characterize your 
        experimental laser conditions (*lambda_0* and *waist*).

    2) If *method_fit* is set to 'fit_gauss_w_exclu':
        
        Same method as above, but with an exclusion zone (for example, if a Hyper Raman band is close 
        to the SHG signal).  
        You must specify the exclusion zone with *exclu_zone = [X_min, X_max]*.
                
    3) If *method_fit* is set to 'integral_gauss':
        
        The intensity is extracted using *analyze_run.intensity_from_gaussian_integral*: ::
                    
            I0 = intensity_from_gaussian_integral(L_x_cleaned, L_y_cleaned, lambda_0, waist)
                
        Here, *lambda_0* and *waist* are set by the parameters *lambda_0_ref* and *waist_ref*.  
        Note that *lambda_0_ref* does not affect the result (*I0*); it is only used for plotting.  

    Parameters
    ----------
    L_x: list
        The x-axis data, used for noise removal and fitting.  
    L_y: list
        The y-axis data where the Gaussian intensity should be extracted.  
    l_cut: list of float
        [Optional] Parameters used for noise removal (see :ref:`alpaga.remove_noise function<remove_noise_section>`).  
    order_fit_noise: int
        [Optional] Order of the polynomial used for noise removal.  
    method_fit: str
        [Optional] The method used to extract the intensity once noise is removed.  
    bounds_fit_gausse: list
        [Optional] Bounds for the free parameters in the 'fit_gauss' method.  
        Narrowing the parameter ranges avoids problems with low Gaussian intensity, where the fit 
        may increase the width instead of decreasing *I0*.  
        Example: to restrict *lambda_0* between 401 and 405, and *waist* between 2 and 3, use  
        *bounds_fit_gausse = ([0, 401, 1], [np.inf, 405, 3])*.  
        See *scipy.optimize.curve_fit* documentation for more details.  
    lambda_0_ref: float
        [Optional] Reference value of *lambda_0* for the 'integral_gauss' method.  
        This has no impact on the result but affects plotting.  
    waist_ref: float
        [Optional] Reference value of *waist* for the 'integral_gauss' method.  
        This has a direct impact on *I0*. Choose carefully (see :ref:`polarisation_procedure_page`).  
    exclu_zone: list of float
        [Optional] Pair of floats defining the exclusion zone for 'fit_gauss_w_exclu'.  
    show_spectra: str
        [Optional] If 'all', plots figures to check results. Otherwise, no figures are shown.  
    figure_counter: int
        [Optional] The number assigned to the first figure.  

    Returns
    -------
    L_para_gauss: list
        Gaussian parameters [I0, lambda_0, waist].  
        *I0*: Gaussian intensity  
        *lambda_0*: central wavelength  
        *waist*: Gaussian width  
    L_err: list
        Associated errors [err_I0, err_lambda_0, err_waist].  
        No errors are defined for the 'integral_gauss' method; in this case, the error list contains zeros.  
    figure_counter: int
        Updated figure counter for subsequent plots.  

    Examples
    --------
    See the tutorial for detailed examples. A minimal workflow is: ::
    
        # Define the directory where the data are stored
        directory = os.path.join(WORK_DIR, 'Eau_V_Spectres') 
        
        # Extract Alpaga parameters describing the dataset
        prefix_file, L_files_angles, N_iter, extension = alpaga.find_angle_iter_from_dir(directory)

        # Select one acquisition
        names = os.path.join(directory, prefix_file) + '_' + L_files_angles[0] 
        
        # Clean the acquisition from spikes and average it over N_iter
        L_lambda, L_spectra, _ = alpaga.averaging_and_cleaning(
            names, N_iter, extension='.dat', type_cleaning='mean',
            L_mean_cleaning_n=[1, 1, 1, 3], L_mean_cleaning_evo_max=[2, 1.5, 1.3, 1.3],
            show_spectra=False, figure_counter=1
        )
        
        # Remove noise and extract Gaussian parameters
        intensity, lambda_0, omega, figure_counter = Alpaga.analyze_run.fit_gaussian_from_noise(
            L_lambda, L_spectra, l_cut=[380, 399, 414, 431], order_fit_noise=4,
            bounds_fit_gausse=([0, 395, 1], [np.inf, 410, 25]), show_spectra='all'
        )
        
        print(intensity, lambda_0, omega)
    '''
    if show_spectra == 'all':
        plt.figure(figure_counter)
        plt.plot(L_x, L_y)
        figure_counter += 1
        
    L_x_cleaned, L_y_cleaned, L_fit_noise, figure_counter = remove_noise(L_x, L_y, l_cut=l_cut, order_fit_noise=order_fit_noise, 
                                                            return_fit_noise=True, show_spectra=show_spectra, figure_counter=figure_counter)
    
    if show_spectra == 'all':
        plt.figure(figure_counter)
        plt.plot(L_x_cleaned, L_y_cleaned)
    
    if method_fit == 'fit_gauss':
        p, q = curve_fit(fit_gausse, L_x_cleaned, L_y_cleaned, bounds=bounds_fit_gausse) 
        I0, lambda_0, waist = p[0], p[1], p[2]
        L_para_gauss = np.array([I0, lambda_0, waist])
        
        perr = np.sqrt(np.diag(q))
        I0_serr, lambda_0_serr, waist_serr = perr[0], perr[1], perr[2]
        L_err = np.array([I0_serr, lambda_0_serr, waist_serr])
        if show_spectra == 'all':
            plt.figure(figure_counter)
            plt.plot(L_x_cleaned, fit_gausse(L_x_cleaned, I0, lambda_0, waist))
            
    elif method_fit == 'fit_gauss_w_exclu':
        if exclu_zone == False :
            raise Exception("No exclusion zone defined")
        # find where to make the cut to define the exclusion zone
        N_lambda = len(L_x_cleaned)
        KKK = 0
        trotter = 0
        x_cut = np.array([0, 0])
        while trotter<2 or KKK>N_lambda:
            if L_x_cleaned[KKK] > exclu_zone[trotter]:
                x_cut[trotter] = int(KKK)
                trotter += 1
            KKK += 1
        #define new list without exclusion list
        L_x_cleaned_exclu=np.delete(L_x_cleaned, [i for i in range(x_cut[0],x_cut[1])], 0)
        L_y_cleaned_exclu=np.delete(L_y_cleaned, [i for i in range(x_cut[0],x_cut[1])], 0)
        
            
        p, q = curve_fit(fit_gausse, L_x_cleaned_exclu, L_y_cleaned_exclu, bounds=bounds_fit_gausse) 
        I0, lambda_0, waist = p[0], p[1], p[2]
        L_para_gauss = np.array([I0, lambda_0, waist])
        
        perr = np.sqrt(np.diag(q))
        I0_serr, lambda_0_serr, waist_serr = perr[0], perr[1], perr[2]
        L_err = np.array([I0_serr, lambda_0_serr, waist_serr])
        if show_spectra == 'all':
            plt.figure(figure_counter)
            plt.plot(L_x_cleaned, fit_gausse(L_x_cleaned, I0, lambda_0, waist))
            plt.plot(L_x_cleaned[x_cut[0]:x_cut[1]], L_y_cleaned[x_cut[0]:x_cut[1]],'r*')
    
    elif method_fit == 'integral_gauss':
        I0 = intensity_from_gaussian_integral(L_x_cleaned, L_y_cleaned, lambda_0_ref, waist_ref)
        L_para_gauss = np.array([I0, lambda_0_ref, waist_ref])
        L_err = np.array([0, 0, 0])
        if show_spectra == 'all':
            plt.figure(figure_counter)
            plt.plot(L_x_cleaned, fit_gausse(L_x_cleaned, I0, lambda_0_ref, waist_ref))
            
    else:
        raise Exception("WARNING: method_fit argument not valid. Possible value: 'fit_gauss' or 'integral_gauss'")
        
    figure_counter += 1
    
    if fit_noise == False :
        return(L_para_gauss, L_err, figure_counter)
    else :
        return(L_para_gauss, L_err, L_x_cleaned, L_fit_noise, figure_counter)
    

############################################################################################    
############################  Polarisation procedure  ######################################
############################################################################################      

def polarisation_intensity(directory=False, 
                           L_filename=False, 
                           prefix_file=False, 
                           L_files_angles=False, 
                           N_iter=False, 
                           extension='.dat', 
                           fct_name=standard_file_name, 
                           type_cleaning='mean', 
                           L_mean_cleaning_n=[1, 1, 1, 3], 
                           L_mean_cleaning_evo_max=[2, 1.5, 1.4, 1.3], 
                           automatic_l_cut=True, 
                           l_cut=[380, 395, 419, 433], 
                           l_cut_n_n2=[2, 9], 
                           order_fit_noise=4, 
                           method_fit_first='fit_gauss', 
                           bounds_fit_gausse=([0, 395, 1], [np.inf, 410, 25]), 
                           lambda_0_ref=403, 
                           waist_ref=2, 
                           exclu_zone=False, 
                           fixed_para_gauss_fit=True, 
                           method_fit_second='fit_gauss', 
                           save_result=True, 
                           name_save_result='./post_prod_results.p', 
                           waiting_time=False, 
                           show_figure=True):
    L_input_list = ['directory', 'L_filename', 'prefix_file', 'L_files_angles', 'N_iter', 'extension', 'type_cleaning', 'L_mean_cleaning_n', 'L_mean_cleaning_evo_max', 'automatic_l_cut', 'l_cut', 'l_cut_n_n2', 'order_fit_noise', 'method_fit_first', 'bounds_fit_gausse', 'lambda_0_ref', 'waist_ref', 'fixed_para_gauss_fit', 'method_fit_second', 'save_result', 'name_save_result', 'waiting_time', 'show_figure']
    
    L_post_prod = {}
    if not isinstance(L_filename, bool):
        if not L_filename:
            raise Exception('ERROR: if you provide L_filename, it should be a list of list containing the filenames')
        print('I will use your L_filename to find the files.')
        if isinstance(L_files_angles, bool):
            raise Exception('You have to define a L_files_angles!')
        print('L_files_angles=', L_files_angles)
        if isinstance(N_iter, bool):
            raise Exception('You have to define N_iter!')
        print('N_iter=', N_iter)
        if isinstance(prefix_file, bool):
            prefix_file = ''
        if isinstance(extension, bool):
            extension = ''
    else:  
        L_filename_K = False
        if directory==False:
            print('No directory given, I will use the input from prefix_file, L_files_angles, N_iter and extension.')
            if not prefix_file or not L_files_angles or not N_iter or not extension:
                raise Exception('WARNING: since no directory has been given, I need values for the optional parameters: prefix_file, L_files_angles, N_iter and extension. Please provide all of them or use directory=our_directory_where_the_data_are.')
        else:
            if prefix_file and L_files_angles and N_iter and extension:
                print('I will use your custom parameters for prefixe, L_files_angles, N_iter and extension.')
            else:
                prefix_file_t, L_files_angles_t, N_iter_t, extension = find_angle_iter_from_dir(directory, extension=extension)
                if prefix_file:
                    print('I will use your custom general prefixe instead of the one found in the directory:', prefix_file)
                else:
                    prefix_file = os.path.join(directory, prefix_file_t)

                if L_files_angles:
                    print('I will use your custom L_files_angles instead of the one found in the directory:', L_files_angles)
                else:
                    L_files_angles = L_files_angles_t

                if N_iter:
                    print('I will use your custom N_iter instead of the one found in the directory:', N_iter)
                else:
                    N_iter = N_iter_t
        print('The prefix for all the file are: "' + prefix_file + '" with ' + str(N_iter) + ' iter. The angle are ' + str(L_files_angles) + '. The extension is: ' + extension)
    
    if show_figure:
        show_figure_fit_gauss = 'all'
    else:
        show_figure_fit_gauss = ''
    # save input
    L_post_prod['directory'] = directory
    L_post_prod['L_filename'] = L_filename
    L_post_prod['prefix_file'] = prefix_file
    L_post_prod['N_iter'] = N_iter
    L_post_prod['L_files_angles'] = L_files_angles
    L_post_prod['extension'] = extension
    L_post_prod['type_cleaning'] = type_cleaning
    L_post_prod['L_mean_cleaning_n'] = L_mean_cleaning_n
    L_post_prod['L_mean_cleaning_evo_max'] = L_mean_cleaning_evo_max
    L_post_prod['automatic_l_cut'] = automatic_l_cut
    L_post_prod['l_cut'] = l_cut
    L_post_prod['l_cut_n_n2'] = l_cut_n_n2
    L_post_prod['order_fit_noise'] = order_fit_noise
    L_post_prod['bounds_fit_gausse'] = bounds_fit_gausse
    L_post_prod['lambda_0_ref'] = lambda_0_ref
    L_post_prod['waist_ref'] = waist_ref
    L_post_prod['method_fit_first'] = method_fit_first
    L_post_prod['method_fit_second'] = method_fit_second
    L_post_prod['fixed_para_gauss_fit'] = fixed_para_gauss_fit
    L_post_prod['save_result'] = save_result
    L_post_prod['name_save_result'] = name_save_result
    L_post_prod['waiting_time'] = waiting_time
    L_post_prod['exclu_zone'] = exclu_zone
    
    # the first polarisation analysis
    N_angle = len(L_files_angles)
    L_intensity_angle = np.zeros((N_angle))
    L_lambda_0_angle = np.zeros((N_angle))
    L_waist_angle = np.zeros((N_angle))
    
    L_intensity_angle_err = np.zeros((N_angle))
    L_lambda_0_angle_err = np.zeros((N_angle))
    L_waist_angle_err = np.zeros((N_angle))
    
    LL_noise_param = []
    
    for KKK in range(0, N_angle, 1):
        if not isinstance(L_filename, bool):
            L_filename_K = L_filename[KKK]
        plt.close('all')
        clear_output()
        print('Angle:', L_files_angles[KKK])
        
        names = prefix_file + '_' + L_files_angles[KKK]
        L_lambda, L_spectra, _ = averaging_and_cleaning(names, N_iter, L_filename=L_filename_K, fct_name=fct_name, type_cleaning=type_cleaning, L_mean_cleaning_n=L_mean_cleaning_n, L_mean_cleaning_evo_max=L_mean_cleaning_evo_max, show_spectra=False, extension=extension)
        
        L_para_gauss, L_err, L_x_fit_noise, L_fit_noise, figure_counter = fit_gaussian_from_noise(L_lambda, L_spectra, l_cut=l_cut, order_fit_noise=order_fit_noise, method_fit=method_fit_first, bounds_fit_gausse=bounds_fit_gausse, lambda_0_ref=lambda_0_ref, waist_ref=waist_ref, exclu_zone=exclu_zone, fit_noise= True, show_spectra=show_figure_fit_gauss, figure_counter=1)
        intensity, lambda_0, waist = L_para_gauss
        if automatic_l_cut: # the second run with automatic l_cut
            l_cut_temp=[lambda_0-l_cut_n_n2[1]*waist, lambda_0-l_cut_n_n2[0]*waist, lambda_0+l_cut_n_n2[0]*waist, lambda_0+l_cut_n_n2[1]*waist]
            L_para_gauss, L_err, L_x_fit_noise, L_fit_noise, figure_counter = fit_gaussian_from_noise(L_lambda, L_spectra, l_cut=l_cut_temp, order_fit_noise=order_fit_noise, method_fit=method_fit_first, bounds_fit_gausse=bounds_fit_gausse, lambda_0_ref=lambda_0_ref, waist_ref=waist_ref, fit_noise= True, show_spectra=show_figure_fit_gauss, figure_counter=figure_counter)
            intensity, lambda_0, waist = L_para_gauss
        
        poly = np.polyfit(L_x_fit_noise, L_fit_noise, deg=order_fit_noise)
        LL_noise_param.append(poly)
        
        L_intensity_angle[KKK] = intensity
        L_lambda_0_angle[KKK] = lambda_0
        L_waist_angle[KKK] = waist
        
        L_intensity_angle_err[KKK] = L_err[0]
        L_lambda_0_angle_err[KKK] = L_err[1]
        L_waist_angle_err[KKK] = L_err[2]
        
        if show_figure:
            plt.show()
            
        if not isinstance(waiting_time, bool): # short pause so that the user can see the plots.
            time.sleep(waiting_time)
        plt.clf()
        plt.close('all')
    L_post_prod['L_intensity'] = L_intensity_angle
    L_post_prod['L_intensity_error'] = L_intensity_angle_err
    L_post_prod['L_lambda_0'] = L_lambda_0_angle
    L_post_prod['L_lambda_0_error'] = L_lambda_0_angle_err
    L_post_prod['L_waist'] = L_waist_angle
    L_post_prod['L_waist_error'] = L_waist_angle_err
    L_post_prod['LL_noise_param'] = LL_noise_param
    
    
    # the second polarisation analysis with fixed lambda_0 and waist
    if fixed_para_gauss_fit:
        if method_fit_second == 'fit_gauss' or method_fit_second == 'both':
            L_intensity_angle_fit_gauss_fixed_para = np.zeros((N_angle))
            L_intensity_angle_fit_gauss_fixed_para_err = np.zeros((N_angle))
        
            
        if method_fit_second == 'integral_gauss' or method_fit_second == 'both':
            L_intensity_angle_integral_gauss_fixed_para = np.zeros((N_angle))
            L_intensity_angle_integral_gauss_fixed_para_err = np.zeros((N_angle))
        
        lambda_0_mean = np.mean(L_lambda_0_angle) 
        waist_mean = np.mean(L_waist_angle) 
        L_intensity_angle_fixed_para = np.zeros((N_angle))
        
        if automatic_l_cut: # reset the l_cut using the automatic scheme
            l_cut=[lambda_0_mean-l_cut_n_n2[1]*waist_mean, lambda_0_mean-l_cut_n_n2[0]*waist_mean, lambda_0_mean+l_cut_n_n2[0]*waist_mean, lambda_0_mean+l_cut_n_n2[1]*waist_mean]
        
        for KKK in range(0, N_angle, 1):
            if not isinstance(L_filename, bool):
                L_filename_K = L_filename[KKK]
            plt.close('all')
            clear_output()
            print('Second Run, Angle:', L_files_angles[KKK])
            figure_counter = 1
            names = prefix_file + '_' + L_files_angles[KKK]
            L_lambda, L_spectra, _ = averaging_and_cleaning(names, N_iter, L_filename=L_filename_K, fct_name=fct_name, type_cleaning=type_cleaning, L_mean_cleaning_n=L_mean_cleaning_n, L_mean_cleaning_evo_max=L_mean_cleaning_evo_max, show_spectra=False, extension=extension)
            if show_figure:
                plt.show()
                
            if method_fit_second == 'fit_gauss' or method_fit_second == 'both':
                L_para_gauss, L_err, L_x_fit_noise, L_fit_noise, figure_counter = fit_gaussian_from_noise(L_lambda, L_spectra, l_cut=l_cut, order_fit_noise=order_fit_noise, method_fit='fit_gauss', bounds_fit_gausse=([0, lambda_0_mean-0.00001, waist_mean-0.00001], [np.inf,lambda_0_mean+0.00001, waist_mean+0.00001]), lambda_0_ref=lambda_0_mean, waist_ref=waist_mean, fit_noise= True, show_spectra=show_figure_fit_gauss, figure_counter=figure_counter)
                L_intensity_angle_fit_gauss_fixed_para[KKK] = L_para_gauss[0]
                L_intensity_angle_fit_gauss_fixed_para_err[KKK] = L_err[0]
                        
            if method_fit_second == 'integral_gauss' or method_fit_second == 'both':    
                L_para_gauss, L_err, L_x_fit_noise, L_fit_noise, figure_counter = fit_gaussian_from_noise(L_lambda, L_spectra, l_cut=l_cut, order_fit_noise=order_fit_noise, method_fit='integral_gauss', bounds_fit_gausse=([0, lambda_0_mean-0.00001, waist_mean-0.00001], [np.inf,lambda_0_mean+0.00001, waist_mean+0.00001]), lambda_0_ref=lambda_0_mean, waist_ref=waist_mean, fit_noise= True, show_spectra=show_figure_fit_gauss, figure_counter=figure_counter)
                L_intensity_angle_integral_gauss_fixed_para[KKK] = L_para_gauss[0]
                L_intensity_angle_integral_gauss_fixed_para_err[KKK] = L_err[0]
            if show_figure:
                plt.show()
                
            if not isinstance(waiting_time, bool): # short pause so that the user can see the plots.
                time.sleep(waiting_time)
        
        if method_fit_second == 'fit_gauss' or method_fit_second == 'both':
            L_post_prod['L_intensity_fit_gauss_fixed_para'] = L_intensity_angle_fit_gauss_fixed_para
            L_post_prod['L_intensity_fit_gauss_fixed_para_error'] = L_intensity_angle_fit_gauss_fixed_para_err
                
        if method_fit_second == 'integral_gauss' or method_fit_second == 'both':
            L_post_prod['L_intensity_integral_gauss_fixed_para'] = L_intensity_angle_integral_gauss_fixed_para
            L_post_prod['L_intensity_integral_gauss_fixed_para_error'] = L_intensity_angle_integral_gauss_fixed_para_err
                
        
    # saving the results
    if save_result:
        print('The results will be saved at: ' + name_save_result + '. Please note that this will erase the file with the same name if it exist. Use the optional input name_save_result to change the name. Note that you SHOULD set the general path.')
        if os.path.isfile(name_save_result):
            os.remove(name_save_result)
        with open(name_save_result, "wb" ) as pfile: # which makes sure that the file is properly closed after writing
            pickle.dump(L_post_prod, pfile)
        
        name_save_result_txt =name_save_result[:-2] + '.txt' 
        
        L_float =[ float(i) for i in L_files_angles]
        
        L_to_write = np.array([L_float, L_intensity_angle]).T
        np.savetxt(name_save_result_txt, L_to_write, delimiter='    ')
        
    else:
        print('The results are not saved. Set save_result to True if you want to save them.')
    return(L_post_prod)

############################################################################################     
