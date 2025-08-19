.. _file_management_page:

File management 
================

In this page, we will explain how the data are handled by Alpaga. First, how the data are expected to be stored and named, then how to open them to start the procedure. 

------------------------
Expected data structure
------------------------

The numerical procedure is built around the experimental one: 

For a given analyser angle (either V/H or S/P depending on how you prefer to call this angle) of the 2 omega photon and other experimental parameters (fundamental power, sample, temperature, number of surfactant/lama per metre square), a directory regroups the measured spectra for one or several incoming polarisation angle. 
In this directory, ''angle'' can vary arbitrary, as long as the name of the file follow this structure: 

prefix_angle-value_iter-number.extention

This structure is defined through several internal function, and more especially by the alpaga.standard_file_name function:

.. autofunction:: file_management.standard_file_name
   :noindex:

You can define another structure for the file, see the last paragraph.

For example, in the directory: /home/lama/Datas/Water_acquisition/V_analser, there are the files: spectra_water_v_2.0_1.dat, spectra_water_v_2.0_2.dat, spectra_water_v_4.0_1.dat, spectra_water_v_4.0_2.dat, spectra_water_v_6.0_1.dat, spectra_water_v_6.0_2.dat . The prefix for all these files is  /home/lama/Datas/Water_acquisition/V_analser/spectra_water_v, the list of the angle is [2.0, 4.0, 6.0] and the total number of iterations is 2. 

.. warning:: The Alpaga developer warmly recommend you to always define an absolute path to your data rather than local one. If you ran the code in the directory  /home/lama/Datas/Water_acquisition, you may indeed use a shorter prefix such as V_analser/spectra_water_v. However, it is more stable to keep with /home/lama/Datas/Water_acquisition/V_analser/spectra_water_v anytime. 

The angles can be whatever string, you can encode other varying properties using this framework: there is no need for this ''list of angle'' to be bounded, or evenly distributed. Be just aware that the very last analysis (:ref:`from the experimental data to the real observable you want like the i4 or surface susceptibility<analysis_SHS_page>` ) may not work as expected.

.. note:: Alpaga can treat all or only part of the 'angle' available in a directory, see :ref:`this page<polarisation_procedure_page>` for more information. 

.. image:: _static/alpaga_6.jpg
   :width: 250
   :align: right


For each acquisition with the same experimental parameters (for instance angle=2.0), several acquisitions will be made in order to average the spectra. See :ref:`the cleaning procedure<cleaning_averaging_spectra_page>` for more details. These acquisitions are stored using different iterations value, from 1 to N. Within this example, there are 2 iterations: spectra_water_v_2.0_1.dat and spectra_water_v_2.0_2.dat which will be used to get a cleaned spectrum for the angle value 2.0. 

.. note:: For all the angle value, the exact same amount of iterations should be given. If you want to average over less iterations then available, you can redefine it using iter_number. See the See :ref:`the cleaning procedure<cleaning_averaging_spectra_page>`.


Now that we have presented the data structure, let's be more explicit. First, we will see how to open a ''single acquisition'', meaning for a given ''angle'': the name should be  prefix_iter-number.extention . Then, we will see how to treat acquisition for several angles, meaning files with names: prefix_angle-value_iter-number.extention . The output given by these functions will be used later on during the procedure. 

------------------------
Open single acquisition
------------------------

To get the Alpaga parameters to treat a single acquisition located in a directory, use the function: 

.. autofunction:: file_management.find_file_iter_from_dir
   :noindex:


------------------------
Open angle acquisition
------------------------

.. _open_angle_acquisition_section:

To get the Alpaga parameters to treat an acquisition with several angle value located in a directory, use the function: 

.. autofunction:: file_management.find_angle_iter_from_dir
   :noindex:
   
.. image:: _static/alpaga_11.jpg
   :width: 250
   :align: right
   
----------------------------
Define your own set of file
----------------------------

In order to go further, you need to have defined a general prefix, list of angles, number of iterations and the extenuation. If you have used the previous procedure, be just aware that you have to set the prefix **with** the general path, *i.e.*: ::

    prefix_general = os.path.join(directory, prefix)

If you want to set yourself these values, you can. Either if you built your own procedure using only piece of Alpaga (therefore you should be good enough in python and thus not need advice), or in the initial parameter of the automatised procedure alpaga.polarisation_intensity, see :ref:`here<polarisation_procedure_page>`. 


Moreover, if you do not use the same structure, you can still use the majority of the code, expect the alpaga.find_file_iter_from_dir and alpaga.find_angle_iter_from_dir function. To do so, you would have to define your own function that define how to built the name of the file provided a 'prefix', 'angle', 'iteration' and 'extension'. In other words, your own alpaga.standard_file_name function. See the tutorial for more example. 

To include this function and replace the standard structure, use the optional argument *fct_name* of the alpaga.averaging_and_cleaning and **alpaga.polarisation_intensity** function.

|

The  :ref:`next procedure step<cleaning_averaging_spectra_page>` is to average the clean every spectrum and to perform the average over all the acquisition ($N_iter$).  

    
:Release: |release|
:Date: |today|








