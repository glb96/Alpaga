.. _fitting_procedure_page:

Fitting the Gaussian 
=====================

In this page, we will see how to extract the Gaussian intensity from a spectrum. This procedure has been optimised in order to get the less possible choice to the operator, and to make this part the most reproducible as possible. Indeed, small change in this procedure parameters can lead to variation of the extracted intensity. Therefore, there are many methods available: it is up to you to choose the one you prefer, and to document which one you have picked! 

.. image:: _static/alpaga_2.jpg
   :width: 350
   :align: right
   
   
First, the background around your Gaussian is most probably not flat. Indeed, due to fluorescence of your sample for instance, you can have a large noise which can make the Gaussian intensity extraction more difficult. Therefore, the first thing to do is to remove this noise.

Then, the extraction of the intensity can be made. Several methods, fit or integral, can be used. 

In this page, it is assumed that the averaged and cleaned spectrum is given (called y value) as input as well as the wave number (called x values), see :ref:`cleaning_averaging_spectra_page` for more information. Note that the value and the unit of the x and y list does not matter for this analysis as long as the parameters respect the same unit and range.  

.. note::
    If your curve is a Lorentzian, you can use the first step to get ride of the noise, then you will have to fit by yourself the intensity. Contact us if you want to implement this new fitting  procedure in Alpaga. 


-----------------
Remove the noise
-----------------

.. _remove_noise_section:

.. image:: _static/alpaga_10.jpg
   :width: 300
   :align: left
   
The spectra will be cut into 3 areas using the x values. The first area and the last one will be used in order to define the noise, while the second one should contain the Gaussian. The first and last area should be large enough in order to be fitted meaningfully by a polynomial function. If this 'noise' area is too large, the part where the Gaussian is located may not be properly fitted and thus modify the final intensity. If this noise area is too small, the noise fit can make no sense. A simple way to check if the area is too small is to add or remove one point to the noise area: the final Gaussian intensity should not be affected. 


   
@Antonin: je te laisse étoffer cette explication en rajoutant des figures? 


For the order of the polynomial function  used to fit the noise, we recommend to use order 2, 3, or 4. We do not recommend to use less since the noise is often not a straight line. Higher term may work, but it can lead to wiggling in the Gaussian area. 


.. autofunction:: analyze_run.remove_noise
   :noindex:



.. note::
    If the noise removal procedure has worked well, the first and last area should be flat and in average zero. The most important is that there is no curvature: otherwise the Gaussian fit below would return wrong value. If you struggle to have a flat first and last area, try to reduce them -- for instance set the first and last area to 10 nm. 

.. image:: _static/gaussian_distribution_meme.png
   :width: 200
   :align: right


------------------------------
Gaussian intensity extraction
------------------------------

.. _gaussian_fit_section:


Now that we have removed the background, the Gaussian spectra should be much easier to fit. There are two ways to extract the Gaussian intensity: by a function fit, or by an integral procedure.


1) Gaussian fit

    This method will fit the curve with a Gaussian function: 
    
    .. math::
    
       f(x) = I_0 \exp \left[ - \left( \frac{ x - \lambda_0}{w_0} \right)^2 \right]
    
    
    and return the intensity :math:`I_0`, the position of the maximum :math:`\lambda_0` and the waist :math:`w_0`. This f(x) function is defined as the *alpaga.fit_gausse* function. 
    
2) Integral method
    This method assumes that the position of the maximum and the waist is known, and extract the intensity using the value of the integral:


    .. math::
    
       f(x) = I_0 \exp \left[ - \left( \frac{ x - \lambda_0}{w_0} \right)^2 \right]
       \int_{-\infty}^{+ \infty} f(x) dx = I_0 w_0 \sqrt \pi
       
    The integral is performed in the *alpaga.intensity_from_gaussian_integral* function, and return the intensity. 


.. image:: _static/alpaga_3.jpg
   :width: 300
   :align: center
   
The function alpaga.fit_gausse defines the gaussian described in the first method. It is not the function that perform the fit, see bellow, but the one that returns a gaussian value for given x and all the other gaussian parameters. You may use this function to check how the ''gaussian'' intensity is defined in Alpaga. 


.. autofunction:: analyze_run.fit_gausse
   :noindex:

And here is the function used to extract the intensity from the integral method:

.. autofunction:: analyze_run.intensity_from_gaussian_integral
   :noindex:


The Gaussian fit is the more versatile method: it can give you the intensity, along with important information: the waist and the maximum position. However, since this method uses a fit through all the curve, it can have an error if the intensity is small. 

On the other hand, the integral method seems more robust to extract the intensity, but it requires to know the waist. For 'easy-to-fit Gaussian curve', the two method return the same result. It is not clear which method is the most precise, therefore they are both always available.


The function to extract the Gaussian intensity uses the previous one, *alpaga.remove_noise*, to get ride of the noise. If you are working already with noise-free curve, this should not be a problem.


.. autofunction:: analyze_run.fit_gaussian_from_noise
   :noindex:
   
----------------------
Towards automating
----------------------


.. image:: _static/alpaga_7.jpg
   :width: 300
   :align: right
   
The extraction of the intensity from the averaged spectra is maybe the part where the numerical parameters influence the more the result. Therefore, it is recommended to:

    1) Try several parameters to see how it fits **your** data. Certain samples may be much easier to fit than others.
    
    2) Use the **same parameters** for all your acquisition. 
    

The full automatic procedure is presented in the ref:`polarisation_procedure_page`. It combines what has been presented in :ref:`file_management_page` , :ref:`cleaning_averaging_spectra_page` and in this page. 


:Release: |release|
:Date: |today|


