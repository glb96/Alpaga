.. _polarisation_procedure_page:

Polarisation Procedure
========================

This method regroups the different step presented in the previous part in order to automate them. The aim of this procedure is to literally ''press a button'' to analyse your results so that you can have a coffee (or a tea (or a hot chocolate)) while the code is running. However, before achieving such dream, you should try the many parameters used. Many of them can be chosen automatically, but checking the different step by yourself is always a good behaviour. 

The function to use is *alpaga.polarisation_intensity*, and below is presented the different argument that can be passed, corresponding to the different procedure step.

.. autofunction:: analyze_run.polarisation_intensity
   :noindex:
   
-------------------------
Overview of the procedure
-------------------------

    1) Open all the file and make sure they work using alpaga.find_angle_iter_from_dir ADD ref. Can be bypassed is you define your custom values.

    2) Perform a first analysis for all the angles. For every angle, it will a) cleaned and averaged the acquisition, b) remove the noise and c) fit the Gaussian. 
    
    3) Perform a second analysis very similar to the step 2), but where some parameters (for the Gaussian fit for instance) can be fixed to the average calculated value. This step is optional.
    
    4) Save the results using a dictionary.


.. image:: _static/alpaga_beau_1.jpg
   :width: 450
   :align: center

Below is presented the argument that you can pass to the function depending on what step it refers to. Many explanations are provided in other pages of the wiki, so if some argument feels unfamiliar to you, you may want to read the corresponding page. 


-----------------------
Which file to analyse?
-----------------------

This method expects to analyse data with several 'polarisation angle'. The expected data architecture and the function that will be used to open them are presented in the :ref:`file_management_page` page. If you want to use all the data available in a given directory, you just have to set the *directory* argument -- and maybe the *extension* if your data files are not in the .dat format. The others are there for more specific usage. 

    + **directory**: str or bool
        
        If string: The directory where is located the data you want to analyse. Please note that only one 'experiment' should be stored in this directory. See :ref:`file_management_page` page.
        
        If set to False: The procedure to find the files, the number of iterations and the list of angles is bypass. Therefore, you should provide these values using all the following argument: *prefix_file*, *L_files_angles*, *N_iter* and *extension*. 
        
        .. note:: If any of these arguments (*prefix_file*, *L_files_angles*, *N_iter*) is set to a value while a *directory* argument is given, the function will first define these value using the :ref:`alpaga.find_angle_iter_from_dir function<open_angle_acquisition_section>`. Then, it will replace the found value by the one given by these arguments.  
        
    + **prefix_file**: str or bool
        
        If set to False, the prefix of the files is found automatically
        
        If set to a string, the prefix will be used rather than the one found automatically. Note that the prefix should point to a global location -- for instance '/home/lama/Datas/Water/spectre_water'
       
    + **L_files_angles**: list or bool
        
        If set to False, the list of the angle to treat is the found automatically
        
        If set to a list, this list of angle will be used rather than the one found automatically. This can be handy if you want to analyse only a part of your data, or check if a smaller sampling of your angles is good enough. 
    
    + **N_iter**: int or bool
    
        If set to False, the number of acquisitions per angle is the one found automatically.
        
        If set to an integer, this *N_iter* will be used instead of the one found automatically. This can be handy if you want to check if the total acquisition time is good enough -- for instance by comparing with a smaller one, *i.e.* smaller *N_iter* value. 
    
    + **extension**: str
        
        The extension of your data files. By default '.dat' . 
    
    + **fct_name**: function
        The function used to built the name of a file given the prefix, angle, iteration and extension. By default, the alpaga.standard_file_name function is used. 


.. image:: _static/alpaga_21.jpg
   :width: 450
   :align: center

--------------------------
Averaging the acquisition
--------------------------

As explained in the :ref:`cleaning_averaging_spectra_page` page, this step does not depend a lot on the parameter chosen. Therefore, try to clean the spectra for a single angle, the parameters found should be sufficient. The parameters set here are the same for every angle of the analysis. 

    + **type_cleaning**: str
        The only possible value actually is 'mean'. 
        
    + **L_mean_cleaning_n**: list
        See the :ref:`alpaga.clean_spectra_mean_n function<cleaning_spectra_section>`
        
    + **L_mean_cleaning_evo_max**: list
        See the :ref:`alpaga.clean_spectra_mean_n function<cleaning_spectra_section>`
        
---------------------------------------------------
Noise removal, Gaussian fit and automatic feedback
---------------------------------------------------

The noise management and the extraction of the Gaussian are the numerical part where the parameters have the biggest impact on the result. Therefore, in this automatic function, several analyses can be performed in order to reduce the 'operator choices'. The aim is to provide a robust and objective way of choosing the parameters, as well as saving time. Indeed, analysing your data with these 'automatic' parameters provide you better reproducibility compared to the case where you choose the parameter for every acquisition! 

.. image:: _static/alpaga_beau_2.jpg
   :width: 450
   :align: center
   
First, there are the parameters already defined in the :ref:`fitting_procedure_page` page:
        
    + **l_cut**: list
        List of four x values (wave-length value for instance) used to define the 3 areas for the noise removal. See the :ref:`alpaga.remove_noise function<remove_noise_section>` for more information.
        
    + **order_fit_noise**: int
        The polynomial function order used for the noise fit. See the :ref:`alpaga.remove_noise function<remove_noise_section>` for more information.
        
     + **bounds_fit_gausse**:str
        The bound used in the case the curve fit procedure is used to extract the Gaussian intensity. See the :ref:`alpaga.fit_gaussian_from_noise function<gaussian_fit_section>` for more information.
        
    + **lambda_0_ref**: float
        The maximal wave-length value used if the integral procedure is used to extract the Gaussian intensity. See the :ref:`alpaga.fit_gaussian_from_noise function<gaussian_fit_section>` for more information.
        
    + **waist_ref**:float
        The waist used if the integral procedure is used to extract the Gaussian intensity. See the :ref:`alpaga.fit_gaussian_from_noise function<gaussian_fit_section>` for more information.


Using the *l_cut* argument, the values defined are used for all the angle. If you spend some time to tune these parameters, it should work well. However, to get an automatic procedure, two arguments have been added: *automatic_l_cut* and *l_cut_n_n2*. The idea is to define the area using the Gaussian parameters rather than absolute values.

Once the maximal intensity position, *lambda_0*, and Gaussian waist, *waist*, is known for a spectrum, the 3 areas can be defined as follows: 
    
    1) The area where the Gaussian is located (the second one) is defined using a parameter, *n*, and the *waist*: from *lambda_0* - *n* x *waist* to  *lambda_0* + *n* x *waist*. Typically, *n* = 2.
    
    2) The noise areas (the first and last) are defined using two parameters, *n* and *n2*, and the *waist*: from *lambda_0* - *n2* x *waist* to  *lambda_0* - *n* x *waist* for the first one, and  from *lambda_0* + *n* x *waist* to  *lambda_0* + *n2* x *waist* for the last one. Typically, *n2* = 9.
    
In other words, the *l_cut* argument becomes: lambda_0 + [*lambda_0* - *n2* x *waist*, *lambda_0* - *n* x *waist*, *lambda_0* + *n* x *waist*, *lambda_0* + *n2* x *waist*]
    
    
This method has the advantage to be robust, but the *lambda_0* and the *waist* should be known. Therefore, for every angle, the *l_cut* value is used first to remove the noise, then get the value of *lambda_0* and the *waist*. After, a second analysis is made with a *l_cut* defined using the *n* and *n2* parameters. The new intensity, *lambda_0* and *waist* are updated. 

    + **automatic_l_cut**: bool
        If set to True, the second analysis for every angle value is performed using the found *lambda_0* and *waist* values. 
        
        If set to False, no second analysis is performed.
        
    + **l_cut_n_n2**: list
        If *automatic_l_cut* is set to True, contains the value used to define the *n* and *n2* parameter. l_cut_n_n2 = [n, n2]. *n* and *n2* can be float or int, typically 2 and 9 respectively. 
        
.. warning:: This second analysis is performed, is based on the result found by the first one using the *l_cut* value defined in the argument. Therefore, even if you want to use this automatic method, be sure to use reasonable *l_cut* values!!!

.. note:: To use efficiently this technique, you should have solid values for *lambda_0* and *waist*. Therefore, it may have some trouble if the Gaussian intensity is very low -- and thus, the *waist* is not well defined.

.. image:: _static/alpaga_beau_3.jpg
   :width: 450
   :align: center
   
Two possible methods to extract the Gaussian intensity are available: 'fit_gauss' or 'integral_gauss', see :ref:`here function<gaussian_fit_section>`. To choose the method, use the parameter *method_fit_first*:

    + **method_fit_first**: str
        If set to 'fit_gauss', use the curve fit procedure to extract the intensity of the Gaussian, *I0*, as well as the maximum position, *lambda_0*, and the waist of the Gaussian, *waist*. 
       
        If set to 'integral_gauss', use the integral method to extract the intensity of the Gaussian, *I0*. 

However, it seems to us that to make the method the more autonomy possible, the curve fit method present more advantages since no value of *lambda_0* and *waist* are needed. Of course, you can set the *lambda_0_ref* and *waist_ref* value to precise value (that you have calculated previously), but it needs more work for the operator. Moreover, the integral method depends on a lot of the *waist* value past: it must be very precise.

Finally, in order to use the automatic *l_cut* selection, it makes more sense to use the curve fit method since it returns the *lambda_0* and *waist* value of every angle. 

But you may want to use this integral method anyway, and if possible with meaningful *waist* value. That is why, a second analysis of *all* the angle is possible using the argument *fixed_para_gauss_fit*:

    + **fixed_para_gauss_fit**: bool
        If set to True, run a second time the analysis for every angle. For this second run, *lambda_0* is no longer angle dependent and is fixed to the mean value found across all the angles treated. Same for the *waist*.
        
        If set to False, no second analysis is performed.
        
In this analysis, the *lambda_0* and *waist* are no longer free parameters. 

If *automatic_l_cut* = True, the *l_cut* is calculated using the mean *lambda_0* and *waist*. The same definition of the 3 areas will be used for all the angle -- using still the *n* and *n2* given initially. 
    
If for the method to extract the Gaussian intensity is the curve fit method, 
    + **method_fit_second**: str
    
        Chose the method used to extract the Gaussian intensity for the second analysis where the *lambda_0* and *waist* are fixed to their mean value.
        
        If set to 'fit_gauss', use the curve fit procedure to extract the intensity of the Gaussian, *I0*. However, the bound for the *lambda_0* and *waist* free parameters are narrowed down so that the *lambda_0* and *waist* found are equal to the mean value. In other words, *lambda_0* and *waist* are no longer free parameters that can be used to fit the curve, only *I0*.
        
        If set to 'integral_gauss', use the integral method to extract the intensity of the Gaussian, *I0*. The *waist* value used for all the angle is the averaged one. 
        
        If set to 'both', perform the 2 analyses.
        
-----------------------
How the data are saved
-----------------------

The results and the input argument are saved using a dictionary. This dictionary can be saved in a 'pickle', that can be opened easily in python. To define the name of this file, use the argument *name_save_result*:
    
    + **save_result**: bool
        If set to True, save the results using the name *name_save_result*.
        
    + **name_save_result**: str
        The name of the pickle that contains the results and also all the parameters used for the analysis. Note that the name of the file **SHALL** ends by '.p', and that should refer to a global location. For instance: ::
            
            name_save_result = '/home/lama/Datas/Results/my_results.p'

.. note:: If the analysis crash, no data is saved. If the name you want to use to save the data correspond to an already existing file, this file is replaced by the new one. 

Once the function has finished, you can have access to your results by loading the pickle where the results have been saved. For instance: :: 

   name_save_result = '/home/lama/Datas/Results/my_results.p'

    with open(name_save_result, "rb") as filetoload:
        L_post_prod_load = pickle.load(filetoload)

Where the dictionary *LL_post_prod_load* contains all the results. The function return also this dictionary as its only output. 

.. image:: _static/alpaga_20.jpg
   :width: 450
   :align: center

If you want to remember which parameters you have chosen to perform this particular analysis, for instance the list of angle *L_files_angles*, use: ::
    
    L_files_angles = L_post_prod_load['L_files_angles']

You can call all the arguments presented above this way. The same procedure is used to find the results:

    + **L_intensity_angle**: list
        The list of the extracted intensity *I0* during the first analysis for every angle. 
        
        If *automatic_l_cut* = True, the value extracted correspond to the second noise removal -- with the *n* and *n2* method.
        
    + **L_lambda_0_angle**: list
        The list of the *lambda_0* found during the first analysis for every angle. 
        
        If *automatic_l_cut* = True, the value extracted correspond to the second noise removal -- with the *n* and *n2* method.
        
        If the method used is the integral method, the element are equal to *lambda_0_ref*.
        
    + **L_waist_angle**: list
        The list of the *waist* found during the first analysis for every angle. 
        
        If *automatic_l_cut* = True, the value extracted correspond to the second noise removal -- with the *n* and *n2* method.
        
        If the method used is the integral method, the element is equal to *waist_ref*.
    
    + **L_intensity_angle_fit_gauss_fixed_para**: list
        The list of the extracted intensity *I0* during the second analysis for every angle if the method chosen is: *method_fit_second* = 'fit_gauss' or 'both'. In this case, the *lambda_0* and *waist* are no longer free parameters for the fitting procedure and is fixed to the mean value of *L_lambda_0_angle* and *L_waist_angle*. 
        
        If *automatic_l_cut* = True, the areas are built using the mean value of *L_lambda_0_angle* and *L_waist_angle*.
        
    + **L_intensity_angle_integral_gauss_fixed_para**: list
        The list of the extracted intensity *I0* during the second analysis for every angle if the method chosen is: *method_fit_second* = 'integral_gauss' or 'both'. In this case, the *lambda_0* and *waist* used are equal to the mean value of *L_lambda_0_angle* and *L_waist_angle*. 
        
        If *automatic_l_cut* = True, the areas are built using the mean value of *L_lambda_0_angle* and *L_waist_angle*.


If you want to have some example of plots using these results, see the notebook tutorial. 

----------------------
Some other parameters
----------------------

.. image:: _static/alpaga_19.jpg
   :width: 150
   :align: left


While the function is running, several lines and plots are shown. Do not worry, they are here in case the execution crashes to help you find the error. If you are fast enough, you can even check that the procedure for every angle is well executed. If you want to have more time to see that, you can set the variable *waiting_time* to a float value. The code will stop from time to time. Note that this slows the procedure...   

    + **waiting_time**: float or bool
        
        If set to False, the function does not wait intentionally
        
        If set to a float value, the function stops from time to time to let you see the plots. The unit is second. 


:Release: |release|
:Date: |today|



