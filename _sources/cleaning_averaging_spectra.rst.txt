.. |delta|    unicode:: U+0394 .. DELTA SIGN 

.. _cleaning_averaging_spectra_page:

Cleaning and Averaging Spectra
===============================

When repeating the same measurement, several spectra (*N_iter*) are acquired.  
This improves statistics and helps remove unwanted artifacts such as spikes.

---------------------------------
Why multiple short acquisitions?
---------------------------------

.. _cleaning_spectra_section:

.. image:: _static/spikes_problem.png
   :width: 350
   :align: right

Individual spectra often contain sudden spikes caused by detector instabilities or electronic noise.  
These spikes are random, unwanted, and may distort the Gaussian signal.  

To deal with them, Alpaga provides:

.. autofunction:: analyze_run.clean_spectra_mean_n
   :noindex:

.. image:: _static/alpaga_5.jpg
   :width: 250
   :align: right
   
The method detects points that strongly deviate from the average across iterations, and replaces them with more reliable values.  
Shorter acquisitions with more repetitions make spike detection easier.

------------------------
Averaging procedure 
------------------------

.. _averaging_spectra_section:

Once cleaned, the spectra are averaged to obtain a stable signal:  

.. autofunction:: analyze_run.averaging_and_cleaning
   :noindex:

This function applies the cleaning step to all spectra, then returns the averaged result for each angle.  

.. image:: _static/alpaga_16.jpg
   :width: 400
   :align: center

------------------------------
Towards the Gaussian intensity
------------------------------

The procedure is not very sensitive to parameter tuning.  
The key is to record many short spectra so that spikes can be removed and the average converges.  

The next step is to fit this averaged spectrum to extract the Gaussian intensity  
(:ref:`see fitting procedure<fitting_procedure_page>`).
