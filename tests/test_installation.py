import pytest
import matplotlib.pyplot as plt

def test_import_alpaga():
    import Alpaga
    # Check main modules exist
    assert hasattr(Alpaga, 'file_management')
    assert hasattr(Alpaga, 'analyze_run')
    assert hasattr(Alpaga, 'shs_module')
    assert hasattr(Alpaga, 'sshg_module')

