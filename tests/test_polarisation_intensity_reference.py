# tests/test_polarisation_intensity_reference.py
import os
import pickle
import numpy as np
import pytest
import matplotlib.pyplot as plt
from Alpaga import analyze_run, file_management
from Alpaga.Data_tutorial import get_tutorial_path

def test_polarisation_intensity_reference():
    # Directory where tutorial files are stored
    directory = get_tutorial_path('SHS/Eau_polar_V')

    # Input parameters
    prefix_file = False
    L_files_angles = False
    N_iter = False
    extension = '.dat'
    fct_name = file_management.standard_file_name
    name_save_result = ''

    type_cleaning = 'mean'
    L_mean_cleaning_n = [1, 1, 1, 3]
    L_mean_cleaning_evo_max = [2, 1.5, 1.4, 1.3]

    l_cut = [380, 399, 414, 431]
    order_fit_noise = 4
    automatic_l_cut = True
    l_cut_n_n2 = [2, 9]

    bounds_fit_gausse = ([0, 404, 1], [np.inf, 410, 3])
    lambda_0_ref = 407.7
    waist_ref = 2.52
    method_fit_first = 'fit_gauss'
    fixed_para_gauss_fit = True
    method_fit_second = 'both'

    save_result = False
    waiting_time = False

    # Run the analysis
    L_post_prod_gauss_fit_integral = analyze_run.polarisation_intensity(
        directory=directory,
        prefix_file=prefix_file,
        L_files_angles=L_files_angles,
        N_iter=N_iter,
        extension=extension,
        fct_name=fct_name,
        type_cleaning=type_cleaning,
        L_mean_cleaning_n=L_mean_cleaning_n,
        L_mean_cleaning_evo_max=L_mean_cleaning_evo_max,
        automatic_l_cut=automatic_l_cut,
        l_cut=l_cut,
        l_cut_n_n2=l_cut_n_n2,
        order_fit_noise=order_fit_noise,
        method_fit_first=method_fit_first,
        bounds_fit_gausse=bounds_fit_gausse,
        lambda_0_ref=lambda_0_ref,
        waist_ref=waist_ref,
        fixed_para_gauss_fit=fixed_para_gauss_fit,
        method_fit_second=method_fit_second,
        save_result=save_result,
        name_save_result=name_save_result,
        waiting_time=waiting_time, 
        show_figure=False
    )

    # Load reference results
    reference_file = os.path.join(directory, 'post_prod_results.p')
    with open(reference_file, "rb") as filetoload:
        L_post_prod_load = pickle.load(filetoload)
    # List of keys to compare
    L_to_compare = [
        'L_intensity', 'L_intensity_error', 'L_lambda_0', 'L_lambda_0',
        'L_waist', 'L_waist_error',
        'L_intensity_fit_gauss_fixed_para', 'L_intensity_fit_gauss_fixed_para_error',
        'L_intensity_integral_gauss_fixed_para', 'L_intensity_integral_gauss_fixed_para_error'
    ]

    # Compare each key
    for name in L_to_compare:
        print(name)
        print(L_post_prod_gauss_fit_integral[name])
        print(L_post_prod_load[name])
        diff = np.sum((L_post_prod_load[name] - L_post_prod_gauss_fit_integral[name])**2)
        assert diff <= 1e-6, f"Error: Reference values not matched for {name} (diff={diff})"
        
        