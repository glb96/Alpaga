.. _installation_page:

Installation
============

.. image:: _static/alpaga_22.jpg
   :width: 200
   :align: right
   

The :alpaga_github:`github page<>` provides the latest version.  
You can download the repository by clicking on the green **[<> Code]** button and then choosing either the Git method (clone) or downloading an archive (.zip). 

Installation using pip
-----------------------

Alpaga is a Python module that can be installed using pip.  
The package is provided as *alpaga.tar.gz*. Use: ::

    pip install alpaga.tar.gz
    
to install the package with your default Python version, or: ::

    mypython3.X -m pip install alpaga.tar.gz

to specify a particular Python version (*mypython3.X*).

Installation using conda
------------------------

To install with the graphical Anaconda interface, open the Anaconda shell and run the same pip command.  
Make sure to use the correct *alpaga.tar.gz* file — *i.e.* check that the path corresponds to its actual location on your computer.

.. image:: _static/anaconda_install_alpaga_visualization.png
   :width: 500
   :align: center


Check the installation
----------------------

To use Alpaga, import it in a Python environment with: ::
    
    import Alpaga
    import Alpaga.alpaga as alpaga
    
Make sure you are not in the source code directory when importing, to ensure the installed package is used. 

.. note:: You can run ``print(alpaga)`` to check from where Python is importing the package.


The *alpaga* module contains the core functions.  
Other files are available in the package, in the directory *Data_tutorial*.  
This directory can be accessed with: ::
    
    import os
    import Alpaga
    import Alpaga.Data_tutorial
    Dir_tuto_file = os.path.dirname(Alpaga.Data_tutorial.__file__)
    print(Dir_tuto_file)

These data are used for the tutorials. See the next sections for details. 
    
    
:Release: |release|
:Date: |today|
