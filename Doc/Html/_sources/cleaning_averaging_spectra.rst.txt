.. |delta|    unicode:: U+0394 .. DELTA SIGN 

.. _cleaning_averaging_spectra_page:

Cleaning and Averaging Spectra
===============================

In this page, we will see how the cleaning and averaging procedure is performed. For the same experimental parameters (for instance the same fundamental polarisation angle), several acquisitions, *N_iter*, is made for a total acquisition time of :math:`T = \Delta t \times N\_iter`, where :math:`\Delta t` is the acquisition time for a single spectrum. 

But why not make only one spectrum with :math:`T = \Delta t`, instead of many with smaller acquisition time?



-------------------------------
How to get ride of the spikes?
-------------------------------

.. _cleaning_spectra_section:

.. image:: _static/alpaga_5.jpg
   :width: 250
   :align: right


The reason is that there are some 'spikes' in a spectrum, due to detection troubles, see Figure TOADD. Add: origine de ces spickes?
These spikes are completely unwanted and can make the detection of the gaussian difficult. In the worst-case scenario, a pick right at the gaussian maximum can make the acquisition not exploitable. Since it is very hard to avoid them during the experiment, we have better to remove them during the treatment of the data.

Therefore, Alpaga propose to detect the spike using the function:

.. autofunction:: analyze_run.clean_spectra_mean_n
   :noindex:



In order to help the detection of spike, it is better to have many acquisitions for small acquisition time, than few acquisition with large acquisition time. In the Figure TOADD is plotted the number of spikes found by the alpaga.clean_spectra_mean_n function for the same set of data, but with different acquisition time. @Antonin: je te laisse terminer ici. 


Once the spikes have been detected, we have to choose how to deal with them.

------------------------
Averaging procedure 
------------------------

.. _averaging_spectra_section:

To average the *N_iter* spectra and remove the spikes, use the function:  

.. autofunction:: analyze_run.averaging_and_cleaning
   :noindex:


.. image:: _static/alpaga_16.jpg
   :width: 400
   :align: center

------------------------------
Towards the gaussian intensity
------------------------------



The cleaning and averaging procedure are not very sensitive to the numerical parameters you can set to Alpaga. However, it is important to have spectra with small enough acquisition time to make the spike detection easy. Moreover, it is important to have an important number of spectra to have well converged averaged spectra. To check the (total) time needed to have converged data, we recommend to check your final observable rather than the spectra. 

The :ref:`next section<fitting_procedure_page>` is the fit of this average spectrum to find the intensity of the gaussian. Therefore, the input will be the x value (the wave number) and the y averaged one (the spectra value).  



:Release: |release|
:Date: |today|


