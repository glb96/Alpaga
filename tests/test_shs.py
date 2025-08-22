# tests/test_shs.py
import pytest
import os
import numpy as np
import pickle
import matplotlib.pyplot as plt
from Alpaga import shs_module
from Alpaga.Data_tutorial import get_tutorial_path

def test_analyse_polarization_SHS_V():
    directory = get_tutorial_path('SHS')
    ref_file = os.path.join(directory, 'shs_water_pola_V.p')
    with open(ref_file, 'rb') as f:
        L_post_prod_load = pickle.load(f)

    L_files_angles = [float(x) for x in L_post_prod_load['L_files_angles']]
    L_x = np.array(L_files_angles) * 2
    L_y = L_post_prod_load['L_intensity']

    L_SHS_prop, L_SHS_prop_error = shs_module.analyse_polarization_SHS_V(L_x, L_y)
    
    ref_values = [706.292230409337, 686.8871405817122, 104.36976003114427,
                  -0.18019677840226622, 0.14777135516648116,
                  389.65035296199596, 300.5504463695141, 15.080934022025597]

    for val, ref in zip(L_SHS_prop, ref_values):
        assert np.abs(val - ref) < 1e-6

