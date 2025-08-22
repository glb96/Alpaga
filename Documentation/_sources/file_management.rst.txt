.. _file_management_page:

File Management
===============

In this page, we explain how data are handled by Alpaga: first, how the data are expected to be stored and named, and then how to access them to start the analysis procedure.

------------------------
Expected Data Structure
------------------------

The numerical procedure is built around the experimental setup.  

For a given analyzer angle (either V/H or S/P, depending on your terminology) of the 2-omega photon and other experimental parameters (fundamental power, sample, temperature, number of surfactant/layer per square meter), a directory contains the measured spectra for one or more incoming polarization angles.  

In this directory, the "angle" can take arbitrary values, as long as the file names follow this structure:

``prefix_angle-value_iter-number.extension``

This structure is defined through several internal functions, particularly the `alpaga.file_management.standard_file_name` function:

.. autofunction:: file_management.standard_file_name
   :noindex:

You can define another file-naming structure if needed (see the last section).

For example, in the directory:  

``/home/lama/Datas/Water_acquisition/V_analyser``  

the files may include:  

``spectra_water_v_2.0_1.dat``, ``spectra_water_v_2.0_2.dat``, ``spectra_water_v_4.0_1.dat``, ``spectra_water_v_4.0_2.dat``, ``spectra_water_v_6.0_1.dat``, ``spectra_water_v_6.0_2.dat``.  

Here:  
- The prefix for all these files is `/home/lama/Datas/Water_acquisition/V_analyser/spectra_water_v`.  
- The list of angles is `[2.0, 4.0, 6.0]`.  
- The total number of iterations is 2.

.. warning::  
   The Alpaga developers strongly recommend always using an absolute path to your data rather than a relative one. For instance, if you run the code in `/home/lama/Datas/Water_acquisition`, you could use a shorter prefix such as `V_analyser/spectra_water_v`. However, using the full path `/home/lama/Datas/Water_acquisition/V_analyser/spectra_water_v` is more stable.

The angles can be any string; you can encode other varying properties using this framework. The "list of angles" does not need to be bounded or evenly distributed. Be aware, however, that the final analysis (:ref:`from the experimental data to the real observable you want, such as the i4 or surface susceptibility<analysis_SHS_page>`) may not work as expected if the angles are irregular.

.. note::  
   Alpaga can process all or only a subset of the available angles in a directory. See :ref:`this page<polarisation_procedure_page>` for more information.

.. image:: _static/alpaga_6.jpg
   :width: 250
   :align: right

For each acquisition with the same experimental parameters (for example, angle=2.0), several acquisitions are made in order to average the spectra. See :ref:`the cleaning procedure<cleaning_averaging_spectra_page>` for more details. These acquisitions are stored using different iteration numbers, from 1 to N. In this example, there are 2 iterations: `spectra_water_v_2.0_1.dat` and `spectra_water_v_2.0_2.dat`, which will be used to compute a cleaned spectrum for the angle value 2.0.

.. note::  
   For all angles, the exact same number of iterations should be available. If you want to average over fewer iterations than available, you can redefine it using `iter_number`. See :ref:`the cleaning procedure<cleaning_averaging_spectra_page>`.
   
.. note:: 
   In the tutorials and in the code, the number of iteration is often stored in `N_iter`.

Now that we have described the data structure, let's be more explicit. First, we show how to open a "single acquisition" (i.e., for a given angle) with file names like `prefix_iter-number.extension`. Then, we show how to handle acquisitions for multiple angles, with file names like `prefix_angle-value_iter-number.extension`. The output from these functions is used later in the procedure.

------------------------
Open Single Acquisition
------------------------

To get the Alpaga parameters for processing a single acquisition located in a directory, use the function:  

.. autofunction:: file_management.find_file_iter_from_dir
   :noindex:

------------------------
Open Angle Acquisition
------------------------

.. _open_angle_acquisition_section:

To get the Alpaga parameters for processing acquisitions with multiple angles located in a directory, use the function:  

.. autofunction:: file_management.find_angle_iter_from_dir
   :noindex:

.. image:: _static/alpaga_11.jpg
   :width: 250
   :align: right

   
----------------------------
Define Your Own Set of Files
----------------------------

To go further, you need to define a general prefix, a list of angles, the number of iterations, and the file extension. If you followed the previous procedure, be sure to include the full path in the prefix, i.e.:

::

    prefix_general = os.path.join(directory, prefix)

If you want to set these values manually, you can. This may be useful if you built your own procedure using only parts of Alpaga (in which case, you should be comfortable with Python and may not need further guidance), or if you want to set the initial parameters for the automated procedure `alpaga.polarisation_intensity` (see :ref:`here<polarisation_procedure_page>`).

Furthermore, if your file naming structure differs from the standard Alpaga format, you can still use the majority of the code, except for the `alpaga.find_file_iter_from_dir` and `alpaga.find_angle_iter_from_dir` functions. To do so, you must define your own function that specifies how to construct a file name given a `prefix`, `angle`, `iteration`, and `extension`. In other words, you define your own equivalent of `alpaga.standard_file_name`. See the tutorial for more examples.

To use your custom function and replace the standard naming structure, provide it through the optional argument `fct_name` in the `alpaga.averaging_and_cleaning` and `alpaga.polarisation_intensity` functions.

-----------------------------
Different Naming Conventions
-----------------------------

If your file naming convention differs significantly from the standard Alpaga format, you must provide the full path to each acquisition as an `N_angle x N_iter` list. For example, for 2 angles and 3 iterations:

.. code-block:: python

    L_filename = [
        [filename_angle1_iter1, filename_angle1_iter2, filename_angle1_iter3],
        [filename_angle2_iter1, filename_angle2_iter2, filename_angle2_iter3]
    ]

With the correct number of iterations (`N_iter`) and any list of angles:

.. code-block:: python

    L_files_angles = ['angle_value_1', 'angle_value_2']
    N_iter = 3

.. note::
  If you provide your data in this way, be careful when following the `tutorial_spectra_analysis` tutorial, especially during the :ref:`denoising step<cleaning_averaging_spectra_page>` (Part I.B and I.C) and when using the the core function `Alpaga.analyze_run.polarisation_intensity` (Parts III.B and III.C). 

|

The  :ref:`next procedure step<cleaning_averaging_spectra_page>` is to average the clean every spectrum and to perform the average over all the acquisition (`N_iter`).  

    
:Release: |release|
:Date: |today|








