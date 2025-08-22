import os

def get_tutorial_path(name="SHS/Eau_polar_V"):
    """
    Return the absolute path to a tutorial dataset.
    """
    import Alpaga.Data_tutorial
    base_dir = os.path.dirname(Alpaga.Data_tutorial.__file__)
    return(os.path.join(base_dir, name))