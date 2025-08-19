# fresh start
rm -r build  
rm -r dist
rm -r *.egg-info 

# creat the package
python3.7 setup.py sdist

# install the package
python3.7 -m pip install dist/Alpaga-1.2.tar.gz

mkdir -p dist/Wiki_tuto
cp -rf Doc/Html dist/Wiki_tuto/Wiki
cp -rf Doc/Tutorial_files dist/Wiki_tuto/Tutorial
tar -cvf dist/wiki_tuto.tar dist/Wiki_tuto
rm -r dist/Wiki_tuto

# usefull website:
# https://www.activestate.com/resources/quick-reads/how-to-package-python-dependencies-for-publication/
