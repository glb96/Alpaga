# tests/test_exclu_zone.py
import os
import pickle
import numpy as np
import pytest
import matplotlib.pyplot as plt
from Alpaga import analyze_run, file_management
from Alpaga.Data_tutorial import get_tutorial_path

def test_exclu_zone_reference():
    # Directory for exclusion zone tutorial files
    directory = get_tutorial_path("Exclu_zone")

    # Cleaning parameters
    L_mean_cleaning_n = [1, 1, 1, 3]
    L_mean_cleaning_evo_max = [2.2, 1.8, 1.5, 1.5]
    l_cut = [370, 399, 427, 458]
    order_fit_noise = 3
    automatic_l_cut = False
    l_cut_n_n2 = [2, 9]

    bounds_fit_gausse = ([0, 405, 2], [np.inf, 413, 5])
    lambda_0_ref = 409
    waist_ref = 5
    fixed_para_gauss_fit = False
    method_fit_second = 'both'

    # Name function parameters
    prefix_file = False
    L_files_angles = False
    N_iter = False
    extension = '.dat'
    fct_name = file_management.standard_file_name

    save_result = False
    waiting_time = False

    # Exclusion zone
    method_fit_first = 'fit_gauss_w_exclu'
    exclu_zone = [413, 430]

    # Run the analysis
    L_post_prod_gauss_fit_integral = analyze_run.polarisation_intensity(
        directory=directory,
        prefix_file=prefix_file,
        L_files_angles=L_files_angles,
        N_iter=N_iter,
        extension=extension,
        fct_name=fct_name,
        type_cleaning='mean',
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
        exclu_zone=exclu_zone,
        fixed_para_gauss_fit=fixed_para_gauss_fit,
        method_fit_second=method_fit_second,
        save_result=save_result,
        name_save_result='',
        waiting_time=waiting_time,
        show_figure=False
    )

    # Load reference results
    reference_file = os.path.join(directory, 'ref_datas.p')
    with open(reference_file, "rb") as filetoload:
        L_post_prod_load = pickle.load(filetoload)

    # Keys to compare
    L_to_compare = ['L_intensity', 'L_lambda_0', 'L_waist']

    # Compare each key
    for name in L_to_compare:
        diff = np.sum((L_post_prod_load[name] - L_post_prod_gauss_fit_integral[name])**2)
        assert diff <= 1e-6, f"Error: Reference values not matched for {name} (diff={diff})"

