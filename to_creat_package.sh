# fresh start
rm -r build  
rm -r dist
rm -r *.egg-info 

# creat the package
python3.7 setup.py sdist
mv dist/*.tar.gz alpaga.tar.gz 
# install the package
python3.7 -m pip install alpaga.tar.gz

# usefull website:
# https://www.activestate.com/resources/quick-reads/how-to-package-python-dependencies-for-publication/
