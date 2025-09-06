.. _polarisation_procedure_page:

Polarisation Procedure
========================

This method regroups the different steps presented previously to automate the analysis.  
The aim is to “press a button” to analyze your results while you enjoy a coffee, tea, or hot chocolate.  
However, before reaching that level of automation, it is recommended to test and understand the many parameters involved. Many of them can be chosen automatically, but verifying each step yourself ensures reliability.

The main function is *analyze_run.polarisation_intensity*. Below, we describe the arguments you can pass to this function, corresponding to different steps in the procedure.

This procedure is explained in Part III of the *tutorial_spectra_analysis* tutorial.

.. autofunction:: analyze_run.polarisation_intensity
   :noindex:
   
-------------------------
Overview of the procedure
-------------------------

1) Open all the files and verify they are correctly read using *alpaga.find_angle_iter_from_dir* (see :ref:`file_management_page`).  
   This step can be bypassed if you define custom values.

2) Perform a first analysis for all polarization angles. For each angle, the function will:  
   a) clean and average the acquisition,  
   b) remove the noise,  
   c) fit the Gaussian peak. 

3) Perform a second analysis, similar to step 2, where some Gaussian fit parameters can be fixed to the average values. This step is optional.

4) Save the results in a dictionary.

.. image:: _static/alpaga_beau_1.jpg
   :width: 450
   :align: center

-----------------------
File selection
-----------------------

This function expects data organized by polarization angle. See the :ref:`file_management_page` for details. You can either: 1) rely on automatic file detection by Alpaga (see *tutorial_spectra_analysis* III.A), 2) provide all the information alongside your filename construction (see *tutorial_spectra_analysis* III.B), or 3) provide the filenames directly (see *tutorial_spectra_analysis* III.C).  

1) Only requires **directory** (automatic detection).  
2) Requires **prefix_file**, **L_files_angles**, **N_iter**, and **extension**. Optionally, **fct_name** depending on your filename convention.  
3) Requires **L_filename**, **L_files_angles**, and **N_iter** (direct file paths).  

- **directory**: str or bool  
  Directory containing the data to analyze. Only one experiment per directory is recommended.  
  If set to False, the function will not search for files automatically; you must provide *prefix_file*, *L_files_angles*, *N_iter*, and *extension*.  

- **prefix_file**: str or bool  
  If False, the prefix is determined automatically. Otherwise, the string is used as the global file prefix.  

- **L_files_angles**: list or bool  
  If False, the angles are determined automatically. Otherwise, the provided list is used.  

- **N_iter**: int or bool  
  Number of acquisitions per angle. Can be provided manually or determined automatically.  

- **extension**: str  
  File extension, default is '.dat'.  

- **fct_name**: function  
  Function to build filenames. Default is *file_management.standard_file_name*. See :ref:`file_management_page` for alternative naming schemes.  

- **L_filename**: list of lists of strings  
  If your files use a non-standard naming convention, provide the full paths for each angle and iteration.  
  See :ref:`file_management_page` for details and section III.C of *tutorial_spectra_analysis* for example usage.

--------------------------
Averaging and cleaning
--------------------------

Cleaning parameters are applied for each angle:

- **type_cleaning**: str, default 'mean'  
- **L_mean_cleaning_n**: list  
- **L_mean_cleaning_evo_max**: list  

For details, see :ref:`cleaning_averaging_spectra_page`.

-------------------------------
Noise removal and Gaussian fit
-------------------------------

Overview
--------

This section describes the **noise management and Gaussian extraction**. These numerical steps have the largest impact on the results, so Alpaga provides a semi-automatic procedure to reduce operator choices and improve reproducibility.  

- Spectra are processed per polarization angle.  
- The goal is to extract **peak intensity**, **central wavelength λ₀**, and **Gaussian width (waist)**.  
- The process is performed in **two runs** for robustness and to allow automated *l_cut* selection.

.. image:: _static/alpaga_beau_2.jpg
   :width: 450
   :align: center

Input parameters
----------------

- **l_cut**: list of 4 numbers.  
  Defines the initial noise and signal regions. See :ref:`alpaga.remove_noise function<remove_noise_section>`.  

- **order_fit_noise**: int.  
  Polynomial order for fitting the noise in the spectra.  

- **bounds_fit_gausse**: list or tuple.  
  Bounds for Gaussian curve fitting. See :ref:`alpaga.fit_gaussian_from_noise function<gaussian_fit_section>`.  

- **lambda_0_ref**: float.  
  Reference lambda_0 used in the integral method.  

- **waist_ref**: float.  
  Reference waist used in the integral method.  

- **method_fit_first**: str (`'fit_gauss'`, `'fit_gauss_w_exclu'` or `'integral_gauss'`).  
  Controls the method for the first run to extract Gaussian parameters.  

- **automatic_l_cut**: bool.  
  If True, a second analysis for each angle is performed using lambda_0 and waist from the first run.  

- **l_cut_n_n2**: list `[n, n2]`.  
  Parameters defining the Gaussian-based regions for automatic *l_cut*.  

- **fixed_para_gauss_fit**: bool.  
  If True, a second run is performed with lambda_0 and waist fixed to mean values.  

- **method_fit_second**: str (`'fit_gauss'`, `'integral_gauss'` or `'both'`).  
  Method for the second run where lambda_0 and waist are fixed.  

- **exclu_zone**: list of 2 numbers.  
  Define borders of exclusion zone if 'fit_gauss_w_exclu' is used for 'method_fit_first'.

- **show_figure**: bool  
  If True, figures are shown. Controls `show_figure_fit_gauss` internally.

First run
---------

The **first run** processes each angle to determine Gaussian parameters and optionally define automatic *l_cut*.  

1. If `automatic_l_cut=False`  
   - Uses the *l_cut* values directly.  
   - Removes noise and fits Gaussian for each angle.  

2. If `automatic_l_cut=True`  
   - In addition, computes lambda_0 and waist for each angle using initial *l_cut*.  

- **Output parameters per angle**:  
  - `L_intensity_angle`: Gaussian peak intensity  
  - `L_lambda_0_angle`: lambda_0  
  - `L_waist_angle`: Gaussian waist  
  - Error estimates for each above  
  - `LL_noise_param`: polynomial coefficients for noise fit  

Second run
----------

The **second run** is optional (`fixed_para_gauss_fit=True`) and fixes lambda_0 and waist to their mean values across all angles. First, it recalculates *l_cut* based on `[lambda_0 - n2*waist, lambda_0 - n*waist, lambda_0 + n*waist, lambda_0 + n2*waist]` with the value obtained in the first run. Then, it performs a second fit using this Gaussian-based *l_cut*.  

- **Method**: controlled by `method_fit_second`.  
  - `'fit_gauss'`: curve fitting with lambda_0 and waist fixed, only intensity free.  
  - `'integral_gauss'`: integral method using mean waist.  
  - `'both'`: performs both analyses.  

- **Automatic l_cut**: if `automatic_l_cut=True`, *l_cut* is recalculated using mean lambda_0 and waist.  

- **Output parameters per angle**:  
  - `L_intensity_fit_gauss_fixed_para` and `_error`  
  - `L_intensity_integral_gauss_fixed_para` and `_error`  

.. note:: The second run ensures more consistent intensity measurements across angles and is particularly useful when using the integral method. 

Recommendation
--------------

We recommend using the intensity computed after the second run, with fixed lambda_0 and waist:

- `method_fit_first = 'fit_gauss'`
- `automatic_l_cut = True`
- `method_fit_second = 'fit_gauss'`
- `fixed_para_gauss_fit = True`

.. note:: This combination is recommended because the first run with 'fit_gauss' reliably determines lambda_0 and waist, the automatic_l_cut ensures robust noise areas, and the second run with fixed parameters avoids angle-dependent fluctuations.

The obtained intensity is saved as: `L_post_prod['L_intensity_fit_gauss_fixed_para']`.
   
-----------------------
Saving results
-----------------------

The results and input arguments are saved in a dictionary, which can also be exported as a pickle file.  

- **save_result**: bool  
  If True, results are saved using the name specified in *name_save_result*.  

- **name_save_result**: str  
  Full path to the pickle file where results and parameters are stored.  
  Must end with '.p'. Example: ::
      
      name_save_result = '/home/lama/Datas/Results/my_results.p'

Once saved, the results can be loaded in Python: ::

   with open(name_save_result, "rb") as filetoload:
       L_post_prod_load = pickle.load(filetoload)

Key entries in the dictionary:

- **L_intensity_angle**: intensity *I0* for each angle (first analysis)  
- **L_lambda_0_angle**: Gaussian peak position for each angle (first analysis)  
- **L_waist_angle**: Gaussian width for each angle (first analysis)  

If *automatic_l_cut* = True, these correspond to the second noise-removal analysis using *n* and *n2*.

Second analysis (if *fixed_para_gauss_fit* = True):

- **L_intensity_angle_fit_gauss_fixed_para**: intensity with Gaussian fit, *lambda_0* and *waist* fixed  
- **L_intensity_angle_integral_gauss_fixed_para**: intensity using integral method with *lambda_0* and *waist* fixed  

Other saved information:

- **LL_noise_param**: polynomial coefficients for noise fits  

----------------------
Other parameters
----------------------

While the function is running, several plots and messages are displayed. These are meant to help monitor the analysis and debug if necessary.  

- **waiting_time**: float or bool  
  If set to a float, the function pauses this many seconds between each angle to allow inspection of plots.  
  If False, the code runs without intentional pauses.  

.. image:: _static/alpaga_19.jpg
   :width: 150
   :align: left

:Release: |release|
:Date: |today|


