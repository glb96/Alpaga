.. _installation_page:

Installation
============

.. image:: _static/alpaga_22.jpg
   :width: 200
   :align: right
   

The :alpaga_github:`github page<>` provides the latest version. You can download the directory but clicking on the green [<> code ] and then chosing either the git way (clone) or via an archive (.zip). 

Installation using pip
-----------------------
Alpaga is a python module which can be installed using pip. The package is compiled in the *alpaga.tar.gz* file. Use: ::

    pip install alpaga.tar.gz
    
to install the package in your default python version, or ::


    mypython3.X -m pip install alpaga.tar.gz

to use a particular mypython3.X python version. 

Installation using conda
------------------------

To install using graphical Anaconda, open the Anaconda shell and run the above pip line. Make sure to call the right *alpaga.tar.gz* file -- *i.e* with the correct file location in your computer.

.. image:: _static/anaconda_install_alpaga_visualization.png
   :width: 500
   :align: center


Check the installation
----------------------
To use Alpaga. You can call Alpaga within a python environment using the classical import function: ::
    
    import Alpaga
    import Alpaga.alpaga as alpaga
    
Make sure to be out of the directory where the source code is located to ensure that it is indeed the package that is called. 

.. note:: You can use `print(alpaga)` to see where python import the package.


The *alpaga* module is the one where the core functions are contained. Other files are available in this package, contained in the directory *Data_tutorial*. The directory where is contained these files is accessible using: ::
    
    import os
    import Alpaga
    import Alpaga.Data_tutorial
    Dir_tuto_file = os.path.dirname(Alpaga.Data_tutorial.__file__)
    print(Dir_tuto_file)

You can use these data to try the tutorial. You have one containing only one acquisition, *Single_acquisition*, and the other with a typical polarisation acquisition, *Eau_polar_V*. See the tutorial file for example. 



Custom Installation
-------------------

If you do not want to use pip, you can unzip the *Alpaga-version.tar.gz* file. In this file, find where the *alpaga.py* is located. You have to update your python path so that it contains the directory where is located the *alpaga.py* file: ::
    
    import sys
    Dir_code_alpaga = '/where/is/located/the/alapaga.py/file'
    sys.path.append(Dir_code_alpaga)
    
And to defers to the tutorial documents: ::
    
    import os
    Dir_tuto_file =  os.path.join(Dir_code_alpaga, 'Data_tutorial')
    
    
:Release: |release|
:Date: |today|
    
