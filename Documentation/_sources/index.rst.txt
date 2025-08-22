Alpaga
=======


The Alpaga code (AnaLyse en PolArisation de la Génération de second hAmonique) aims to analyse the SHG experimental acquisitions. 


.. image:: _static/alpaga_4.jpg
   :width: 250
   :align: right
   
It first proposes a robust automatic procedure to extract the intensity of the Gaussian peak (here the SHG signal) from spectral measurements. This automatic procedure is explained here and follows these steps:

    + First it finds, in a given directory, the different files to analyse. More information are given in the :ref:`file_management_page` section.
    
    + Then, for each acquisition with the same physical parameters, it cleans and averages the numerous acquisitions. The ''cleaning'' refers to the deletion of large non-physical spikes, such as "cosmic particles". This procedure is explained in the :ref:`cleaning_averaging_spectra_page` along with a discussion about the acquisition time parameter.

    + Finally, this averaged spectrum is fitted by a Gaussian to extract the target intensity. Several options for this important step are available and explained in the section :ref:`fitting_procedure_page`. This step is probably the one that leads to the largest numerical uncertainty, depending on the parameters chosen. 

The full automated procedure is presented in the section :ref:`polarisation_procedure_page`, along with the possible parameter values. 

At Institut Lumière Matière (ILM), we use the code to analyse the results obtained from Surface Second Harmonic Generation (SSHG) experiments and Second Harmonic Scattering (SHS). Hence, we briefly present our formalism and analysis tool to extract from the cleaned data obtained in section :ref:`polarisation_procedure_page` relevant properties regarding SHS and SSHG in the pages :ref:`analysis_SHS_page` and :ref:`analysis_SSHG_page`, respectively.

.. image:: _static/alpaga_15.jpg
   :width: 250
   :align: left


The installation procedure is straightforward and is explained in the :ref:`installation_page` section. Section :ref:`for_developpers_page` provides some general guidance regarding Git and how to update the code or wiki.


Finally, this wiki proposes some numerical (:ref:`python_advice_page`) and experimental (:ref:`experimental_advice_page`) advice. These are not typically found in articles, but perhaps in books or deep on the Internet. You may be able to find some (or all) from experienced scientists or our directors. If you want to expand these lists, please do not hesitate to contact us.



Contact Us
=============

You can contact us using the :alpaga_github:`github page<>` or by e-mail at:

    + guillaume_le_breton@live.fr
    + oriane.bonhomme@univ-lyon1.fr

Licence
=============

Alpaga is under the Lesser GPL v2.1 license.

Publications
=============

To cite Alpaga, use the DOI: |alpaga_DOI|.

Here is a list of some useful references to understand Second Harmonic Generation in general: :cite:p:`brevet1997surface`, :cite:p:`bruyere2016generation`, :cite:p:`sanchez2018generation`, :cite:p:`pardon2021sonder`, :cite:p:`le2022second`, :cite:p:`fery2025sonder`, and :cite:p:`rondepierre2025correlations`.

Here is the list of scientific communications that have used Alpaga so far: :cite:p:`le2022second`, :cite:p:`le2023liquid`, :cite:p:`fery2025sonder`, and :cite:p:`rondepierre2025correlations`.

The references are shown in the :ref:`reference` page.

.. toctree::
   :maxdepth: 3
   :numbered:
   :hidden:

   ./installation
   ./file_management
   ./cleaning_averaging_spectra
   ./fitting_procedure
   ./polarisation_procedure
   ./analysis_SHS
   ./analysis_SSHG
   ./python_advice
   ./experimental_advice
   ./for_developpers
   ./alpaga
   ./devs_page
   ./reference
   
:Release: |release|
:Date: |today|
