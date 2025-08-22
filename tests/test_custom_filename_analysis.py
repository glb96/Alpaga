import os
import pytest
import numpy as np
import matplotlib.pyplot as plt
from Alpaga import analyze_run
from Alpaga.Data_tutorial import get_tutorial_path

def my_convention_file_name(prefixe, angle=False, iteration=False, extension='.dat'):
    """
    Custom file naming convention, equivalent to Alpaga.file_management.standard_file_name.
    """
    if isinstance(angle, bool):
        if isinstance(iteration, bool):
            name = prefixe + extension
        else:
            name = prefixe + '_' + iteration + extension
    else:
        if isinstance(iteration, bool):
            name = prefixe + '_' + angle + extension
        else: 
            name = prefixe + '_' + angle + '_' + iteration + extension
    return name

def test_polarisation_intensity_custom_filename():
    # Directory and file settings
    directory = get_tutorial_path("SHS/Eau_polar_V")
    prefix_file = os.path.join(directory, 'Spectre')
    L_files_angles = ['4.0', '12.0', '24.0']
    N_iter = 5
    extension = '.dat'
    fct_name = my_convention_file_name

    # Cleaning parameters
    type_cleaning = 'mean'
    L_mean_cleaning_n = [1, 1, 1, 3]
    L_mean_cleaning_evo_max = [2, 1.5, 1.4, 1.3]

    # Noise parameters
    l_cut = [380, 399, 414, 431]
    order_fit_noise = 4
    automatic_l_cut = True
    l_cut_n_n2 = [2, 9]

    # Gaussian fit parameters
    bounds_fit_gausse = ([0, 404, 1], [np.inf, 410, 3])
    lambda_0_ref = 407.7
    waist_ref = 2.52
    method_fit_first = 'fit_gauss'
    fixed_para_gauss_fit = True
    method_fit_second = 'both'

    # Save result
    save_result = False
    name_save_result = os.path.join("SomePath", 'post_prod_results.p')
    waiting_time = 0

    # Run the analysis
    L_post_prod_gauss_fit_integral = analyze_run.polarisation_intensity(
        directory=False,
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
    # Simple sanity checks
    assert isinstance(L_post_prod_gauss_fit_integral, dict)
    expected_keys = ['L_intensity', 'L_intensity_error', 'L_lambda_0', 'L_waist']
    for key in expected_keys:
        assert key in L_post_prod_gauss_fit_integral
        assert len(L_post_prod_gauss_fit_integral[key]) > 0
        assert isinstance(L_post_prod_gauss_fit_integral[key][0], (int, float, np.float64))
