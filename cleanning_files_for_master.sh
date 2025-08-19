git rm -r Alpaga.egg-info  
git rm -r build
mv dist/*.tar.gz .  
git rm -r dist  
git rm -r Doc/Rst  
git rm -r setup.py
git rm -r Test  
git rm -r to_creat_package.sh
git rm -r cleanning_files_for_master.sh
git commit -a -m'cleaning for master version after merge'
git push

