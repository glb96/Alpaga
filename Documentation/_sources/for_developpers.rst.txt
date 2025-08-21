.. _for_developpers_page:

For Developpers
================

In this section, we provide some guidance to help developers comtributing to this project. 
In particular, this code is developed using git because of these multiple contributors. Using the github page, one can proposes update of the code, tutorial or wiki using directly the webpage. However, to modify the package (alpaga.tar.gz) or the online wiki (you are currently reading), compilation must be performed. 

Either the github workflow works and you have nothing to do in order to update the package/wiki once you have push something in the master branch, or it fails and you have to perform these part on your computer until you fix the issue. 


How to : compile a new homemade Alpaga version:
---------------------------------------

If you want to develop new functions or modules in Alpaga module, make sure to compile your code into *.tar.gz* file. To do so, one can use the bash script *to_creat_package.sh*.

For windows users, if you have access to a bash terminal, go to the folder where *to_creat_package.sh* is and execute it like that : ::

    C:\your_path_to_alpaga_folder\Alpaga> .\to_creat_package.sh

If not, you can use functions writen inside the .sh file (open it with notepad) directly in a command terminal.

When it's done, your code is compiled and compressed into a *.tar.gz* file. The bash script will also do a clean install of the new Alpaga module.

How to : compile the online wiki:
---------------------------------------

After changing *.rst* file to add the information you want in the wiki, make sure to compile your changes to make it appears in HTML files. To do so, there are some python packages to add before compilation : Sphinx - Sphinxcontrib-bibtex - Recommonmark.

For windows users, you can use : ::

    python -m pip install sphinx
    python -m pip install sphinxcontrib-bibtex
    python -m pip install recommonmark
   
You can then compile your wiki with : ::

    C:\your_path_to_alpaga_folder\Alpaga\Doc\Rst> python -m sphinx -b html . ../Html/.

Your changes should now appear in HTML files.

Scratch git guide:
---------------------------------------

In this section, we will see how we can use git to implement new functions, fix some bugs or edit wiki.

**Installation :**

First of all, we need git on our computer. Most of us are used to use Graphical User Interface (GUI) of git SCM so we are presenting this tool, but feel free to use other software if you're used to. You can have it here :

.. image:: _static/download_page.PNG
   :width: 500
   :align: center


Choose your version of the soft and install it. Once it's done, you can open git GUI. The first step is to link Alpaga gitlab with a new work repertory. To do so, click *clone existing repertory* and then copy the clone as shown in the picture, then choose a directory where to put your working version of Alpaga.

.. image:: _static/procedure_git.jpg
   :width: 700
   :align: center
   
Now we have to import the working branch (usualy Beta branch) into the directory. To do so, click branch / create / then choose option like in the following :

.. image:: _static/create_branch.PNG
   :width: 500
   :align: center
   
|

Well done, you can now contribute to this project !

|


.. image:: _static/alpaga_25.jpg
   :width: 200
   :align: center  
   
|
|

**How to work together : Pull, Push, Fetch, Flush and other lovely stuff**

We recommand to always be sure to have the latest version of the code before doing some modification. This procedure is called Pull and is separated in two : 

- First called **fetch** where you download the latest version of the code from gitlab. This 'download' is not directly visible on your computer. To do so : [ Remote **->** Fetch from **->** origin ].

.. image:: _static/fetch.JPG
   :width: 700
   :align: center 

- Second called **merge**. It will **merge** the version of Alpaga from gitlab with the version that you have modified. It should conserve your change and implement changes from gitlab. To do so : [ Merge **->** Local merge ]. For exemple, if you want to merge the tracking branch Beta with your own Beta branch, select [ Tracking branch **->** origin/beta ] .
   
.. image:: _static/merge.JPG
   :width: 700
   :align: center 
   
   
.. note:: You may have some merging issue if you work on a file which is not the latest version. There will be a conflict between your version of the file and the one in gitlab. If you can't solve this conflict, as a last resort, you should try to save the file in an other folder, redownload the file from gitlab, and then implement your change by hand. We called this process the **Flush**.

When you have finished your job, in order to add your contribution to the Gitlab, you have to **Pull**.

- First of all, you will scan our change from gitlab with [ Rescan ]. You should now see all your changes in the GUI.

.. image:: _static/scan.JPG
   :width: 700
   :align: center 

- Then you have to valid those changes with [ Stage changed ].

.. image:: _static/stage.JPG
   :width: 700
   :align: center 

- You will commit those changes with [ Commit ]. Don't forget to put a little message describing what is the purpose of this commit.

- Finaly, you can push your commits on gitlab. After that, everyone pulling Alpaga will have your contrubtion !





:Release: |release|
:Date: |today|
