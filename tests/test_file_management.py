import pytest
import os
import matplotlib.pyplot as plt
from Alpaga import file_management
from Alpaga.Data_tutorial import get_tutorial_path

def test_find_file_iter_from_dir():
    directory = get_tutorial_path("SHS/Single_angle")
    prefix_file, N_iter, extension = file_management.find_file_iter_from_dir(directory)
    assert isinstance(prefix_file, str)
    assert isinstance(N_iter, int)
    assert isinstance(extension, str)

def test_find_angle_iter_from_dir():
    directory = get_tutorial_path("SHS/Eau_polar_V")
    prefix_file, L_files_angles, N_iter, extension = file_management.find_angle_iter_from_dir(directory)
    assert isinstance(prefix_file, str)
    assert isinstance(L_files_angles, list)
    assert isinstance(N_iter, int)
    assert isinstance(extension, str)
