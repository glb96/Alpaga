.. _fitting_procedure_page:

Fitting the Gaussian 
=====================

In this page, we explain how to extract the Gaussian intensity from a spectrum.  
This procedure has been optimized to minimize user choices and make the process as reproducible as possible.  
Small changes in the procedure’s parameters can lead to variations in the extracted intensity.  
Therefore, several methods are available: it is up to you to choose the one you prefer, and to document which one you used!  

This procedure is explained in Part II of the *tutorial_spectra_analysis* tutorial.

.. image:: _static/alpaga_2.jpg
   :width: 350
   :align: right
   
First, note that the background around your Gaussian is most likely not flat.  
For example, due to sample fluorescence, a large noise component may appear, making Gaussian intensity extraction more difficult.  
The first step is therefore to remove this background noise.  

Once the background has been removed, the Gaussian intensity can be extracted using different methods: either a curve fit or an integral procedure.  

In this page, we assume that the averaged and cleaned spectrum is provided as input (called the *y values*), along with the wave numbers (called the *x values*).  
See :ref:`cleaning_averaging_spectra_page` for more details.  
Note that the units of the x and y values do not matter, as long as they are consistent and within a reasonable range.  

.. note::
    If your curve is Lorentzian, you can still use the noise-removal step.  
    However, you will then need to fit the intensity manually.  
    Contact us if you would like to contribute a new Lorentzian fitting procedure to Alpaga.  


-----------------
Remove the noise
-----------------

.. _remove_noise_section:

.. image:: _static/alpaga_10.jpg
   :width: 300
   :align: left
   
The spectrum is divided into three regions using the x values.  
The first and last regions are used to define the noise, while the central region should contain the Gaussian peak.  
The first and last regions must be large enough to be meaningfully fitted with a polynomial function.  

- If the noise regions are too large, the Gaussian area may not be properly fitted, altering the final intensity.  
- If the noise regions are too small, the polynomial fit may be meaningless.  

A simple way to check this is to add or remove a point from the noise region: the final Gaussian intensity should remain unchanged.  

.. image:: _static/l_cut_definition.png
   :width: 600
   :align: center
   
For the polynomial order used to fit the noise, we recommend 2, 3, or 4.  
Lower orders are not suitable since the noise is rarely linear.  
Higher orders may work but can introduce oscillations in the Gaussian region.  

.. autofunction:: analyze_run.remove_noise
   :noindex:

.. note::
    If noise removal worked correctly, the first and last regions should be flat and close to zero on average.  
    Most importantly, there should be no curvature: otherwise the Gaussian fit below will return incorrect values.  
    If you cannot achieve flat first and last regions, try reducing their size (e.g., set them to 10 nm).  

.. image:: _static/gaussian_distribution_meme.png
   :width: 200
   :align: right


------------------------------
Gaussian intensity extraction
------------------------------

.. _gaussian_fit_section:

Once the background has been removed, the Gaussian spectrum should be much easier to fit.  
There are two ways to extract the Gaussian intensity: fitting a Gaussian function or using an integral method.  

.. image:: _static/gaussian_fit.png
   :width: 600
   :align: center

1) Gaussian fit

    This method fits the curve with a Gaussian function: 
    
    .. math::
    
       f(x) = I_0 \exp \left[ - \left( \frac{ x - \lambda_0}{w_0} \right)^2 \right]
    
    and returns the intensity :math:`I_0`, the peak position :math:`\lambda_0`, and the waist :math:`w_0`.  
    This function is defined in *alpaga.fit_gausse*.  
    
2) Integral method

    This method assumes that the peak position and waist are known, and extracts the intensity using the integral:
    
    .. math::
    
       f(x) = I_0 \exp \left[ - \left( \frac{ x - \lambda_0}{w_0} \right)^2 \right]
       \int_{-\infty}^{+ \infty} f(x) dx = I_0 w_0 \sqrt \pi
       
    The integral is implemented in *alpaga.intensity_from_gaussian_integral*, which returns the intensity.  

.. image:: _static/alpaga_3.jpg
   :width: 300
   :align: center
   
The function *alpaga.fit_gausse* defines the Gaussian described above.  
It does not perform the fit itself (see below), but simply returns a Gaussian value for given x and parameters.  
You can use this function to verify how Gaussian intensity is defined in Alpaga.  

.. autofunction:: analyze_run.fit_gausse
   :noindex:

The function used to extract the intensity with the integral method is:

.. autofunction:: analyze_run.intensity_from_gaussian_integral
   :noindex:

The Gaussian fit method is more versatile: it provides not only the intensity but also the waist and peak position.  
However, because it relies on fitting the entire curve, it can be less accurate when the signal is weak.  

The integral method, on the other hand, is often more robust for intensity extraction, but it requires prior knowledge of the waist.  
For well-behaved Gaussian curves, both methods yield the same result.  
Since it is unclear which method is most precise, both are always available.  

The Gaussian intensity extraction function also relies on *alpaga.remove_noise* to remove the background.  
If your curve is already noise-free, this step should not be a problem.  

.. autofunction:: analyze_run.fit_gaussian_from_noise
   :noindex:
   

----------------------
Towards automation
----------------------

.. image:: _static/alpaga_7.jpg
   :width: 300
   :align: right
   
Extracting intensity from averaged spectra is perhaps the step where numerical parameters most strongly influence the results.  
Therefore, we recommend:  

1. Testing several parameters to see which best fit **your** data (some samples are easier to fit than others).  
2. Using the **same parameters** consistently for all acquisitions.  

The fully automated procedure is presented in :ref:`polarisation_procedure_page`.  
It combines the approaches described in :ref:`file_management_page`, :ref:`cleaning_averaging_spectra_page`, and this page.  

:Release: |release|  
:Date: |today|  
