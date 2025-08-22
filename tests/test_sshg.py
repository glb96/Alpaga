# tests/test_sshg.py
import pytest
import numpy as np
import os
import pickle
import matplotlib.pyplot as plt
from Alpaga import sshg_module
from Alpaga.Data_tutorial import get_tutorial_path

def test_analyse_polarization_SSHG():
    directory = get_tutorial_path('SSHG')
    
    # Load S-polarization
    with open(os.path.join(directory, 'sshg_water_pola_S.p'), 'rb') as f:
        L_post_prod_S = pickle.load(f)
    
    # Load P-polarization
    with open(os.path.join(directory, 'sshg_water_pola_P.p'), 'rb') as f:
        L_post_prod_P = pickle.load(f)
    
    L_files_angles = [float(x) for x in L_post_prod_P['L_files_angles']]
    L_polarisation_angle = np.array(L_files_angles) * 2
    
    ai, chi = sshg_module.analyse_polarization_SSHG(
        angle_incidence=70,
        n1_fonda=1,
        n2_fonda=1.339,
        n1_harmo=1,
        n2_harmo=1.329,
        L_polarisation_angle=L_polarisation_angle,
        L_intensity_S=L_post_prod_S['L_intensity_angle'],
        L_intensity_P=L_post_prod_P['L_intensity_angle'],
        XXZ=False
    )

    ref_ai = [0.3542567700981523, -0.3621604694014314, 0.1839850510782555,
              0.366155382521651, 0.3552643798973962, 1.2217304763960306]
    ref_chi = [46.28604700524947, -11.066637940848794, -20.134105808498713,
               46.28604700524947, 11.066637940848794, 111.69619835354911]

    for a, r in zip(ai, ref_ai):
        assert np.abs(a - r) < 1e-6

    for c, r in zip(chi, ref_chi):
        assert np.abs(c - r) < 1e-6

