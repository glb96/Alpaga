Alpaga
=======


The Alpaga code (AnaLyse en PolArisation de la Generation de second hAmonique) aims to analyse the SHG experimental acquisitions. 


.. image:: _static/alpaga_4.jpg
   :width: 250
   :align: right
   
It first proposes a robust automatic procedure to extract the intensity of the Gaussian peak (here the SHG signal) from spectrum measurements. This automatic procedure is explained here, and follow these steps:
     
    + First it founds, in a given directory, the different files to analyse. More informations are given in the :ref:`file_management_page` section.
    
    + Then, for each acquisition with the same physical parameters, it cleans and averages the numerous acquisitions. The ''cleaning'' refers to the deletion of huge nonphysical spikes -- cosmic particles. This procedure is explained in the :ref:`cleaning_averaging_spectra_page` along with some physical discussions about the acquisition time parameter.

    + Finally, this averaged spectra is fitted by a Gaussian to extract the target intensity. Several options for this important step are available and explained in the section :ref:`fitting_procedure_page`. This step is maybe the one which leads to the largest numerical uncertainty -- depending on the parameters chosen. 

The full automatized procedure is presented in the section :ref:`polarisation_procedure_page`, along with the possible parameters value. 

In the ONLI team we use the code to analyse the results obtained from Surface Second Harmonic Generation (SSHG) experiments and Second Harmonic Scattering (SHS). 
Hence, we presents breifly our formalism and analysis tool to extract from the cleaned data obtained in section :ref:`polarisation_procedure_page` relevent properties regarding the SHS and SSHG in the page :ref:`analysis_SHS_page` and the pahe :ref:`analysis_SSHG_page` respectively. 


.. image:: _static/alpaga_15.jpg
   :width: 250
   :align: left


The installation procedure is quite straightforward and is explained in the :ref:`installation_page` section.

Finally, this wiki propose some numerical (:ref:`python_advice_page`) and experimental (:ref:`experimental_advice_page`) advices. These are not written in articles, maybe in books or deep in the internet. Surely you can find some (all?) from hardened scientists or from our beloved directors. Therefore, if you want to expand these lists, do not hesitate to contact us. 




Contact Us
=============

You can contact us using the :alpaga_zenodo:`Zenodo page<>` or by e-mail at:

    + guillaume.le-breton@ens-lyon.fr
    + oriane.bonhomme@univ-lyon1.fr

Licence
=============

Alpaga is under the Lesser GLP V.2.1 license.

Publications
=============

To cite Alpaga, use the DOI: |alpaga_DOI|.



Here are the list of some usefull references to understand the Second Harmonic Generation in general: :cite:p:`brevet1997surface`, :cite:p:`bruyere2016generation`, :cite:p:`sanchez2018generation`, :cite:p:`pardon2021sonder`, :cite:p:`le2022second`, :cite:p:`fery2025sonder`, and, :cite:p:`rondepierre2025correlations`.


And here the list of the scientific commuinications which have used Alpaga so far: :cite:p:`le2022second`,  :cite:p:`le2023liquid`, :cite:p:`fery2025sonder`, and, :cite:p:`rondepierre2025correlations`.


.. bibliography::


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
   ./alpaga
   ./devs_page
   
:Release: |release|
:Date: |today|
