.. _python_advice_page:

Python advice
==============

Dear student, PhD, doctor, professor and guests, or Igor user,

Here is some advice that you may be found useful to work with Alpaga or python in general. This page does not pretend to help you as much as a course, but I hope it can help. If you have any trick or advice, please do not hesitate to contact the HYPERLINK Alpaga maintainer to make them add to this list.


------------
Some habits
------------

The Alpaga developer propose you some habits that can make your code mode reader-friendly (or at least understand better how the Alpaga code is written).

Do not call the version of your code something like ''new_analyse'' or ''fix_bug_analysis''. If you do not want to use versioning software such as git, name it using: 'analysis_1', 'analysis_2'...

The name of every variable should be the more explicit as possible. Do not call the list where the angles are stored ''list_a'', but ''L_angle''. Keep the closest as possible to actual name you would use in your report/manuscript/article. 

If it is a list, name it with a prefix *L_*

If it is a directory/list with a lot of dimensions, name it with a prefix *LL_*

If it is a temporary variable (within a loop), use the suffix *_t* or *_temp* . 

Initialise the size of the list if you know the dimension. It would help you to spot unexpected behaviour. 

--------------------
Tricks to save time
--------------------

    + If you copy-past, a piece of code more than 5-6 times, maybe it is time to define a new function.

    + At the very beginning of the code, you should define a WORK_DIR and SAVE_DIR variable. In the case you move the analysis code, the data, or you change the computer where you work, these variables will help you. You just have to set the absolute path until the data directory/where you want to save your figure once, and then everything will be updated. Example: ::

        import os # this package should be already installed in every decent python environment
        WORK_DIR = '/home/lama/Datas'
        SAVE_DIR = '/home/lama/Article/MyNextNature'

    Then, you just have to declare the directory where are located the data as: ::

        directory = os.path.join(WORK_DIR, 'your_directory/other_one')
        figure_name_save = os.path.join(SAVE_DIR, 'Main/figure_2.pdf')

    This way, you do not have to worry about where is located the analysis software: you just have to check the WORK_DIR and SAVE_DIR variables.  

    + We recommend to keep the code that created a figure you used in your report/article. Even better, to copy this code and save it where the figure is located to make sure you can regenerate it if needed. 



--------------------------------------------
Useful data structure in python: dictionary
--------------------------------------------

To store several datas/list/anything in one 'place' in python, you can use a dictionary. 

A dictionary is created using: ::

     LL_mydict = {}

You can add a value associated with a key using: ::
    
    LL_mydict['lama_1_name'] = 'Alpaga'
    LL_mydict['lama_1_age'] = 1.5
    LL_mydict['lama_1_habits'] = ['eat cheese', 'sleep']

You can access these values using: ::

    print(LL_mydict['lama_1_name'])
    age = LL_mydict['lama_1_age']
    print(age)
    
It can be useful if you want to automatize the name of your data in python. For instance, let's say you have performed several experiments with names 'C_1', 'C_2', 'C_5', 'C_10', 'C_20'. The concentration used are: :: 
    
    L_C = [1, 2, 5, 10, 20]
    
Treat every experiment, and store the result using: ::
    
    name_key = 'my_observable_' + str(concentration_value)
    LL_mydict[name_key] = my_observable_at_this_concentration
    
You should have at the end in your directory the key: 'my_observable_1', 'my_observable_2', 'my_observable_5', 'my_observable_10' 'my_observable_20'. The advantage is that you can loop over the name using dictionary: ::

    for concentration in L_C:
        name_key_t = 'my_observable_' + str(concentration)
        print(LL_mydict[name_key_t])
 
 
Of course, you can define as many variable as observable and concentrations ::
     
     
     observable_c_1 = the_value_for_c_1 # C = 1
     observable_c_2 = the_value_for_c_2 # C = 2
     observable_c_5 = the_value_for_c_5 # C = 5
     observable_c_10 = the_value_for_c_10 # C = 10
     
     
But you cannot access them (the observable_c_n variable) automatically. Moreover, you are very likely to make mistakes during the numerous copy-past you will face. Storing all the result in a single object (dictionary or user-defined object if you are a purist) with key generated automatically is the best way to have maintainable and safe data structure! 


------------------------------
How to access the data: pickle 
------------------------------

Another useful aspect of the dictionary (where all your results are saved), is that you can save them easily using the pickle format. It is a python-friendly format, but not human readable. To open a pickle, use: ::
    
    import pickle
    name_file = '/some/directory/with/your/pickle/file.p' 
    with open(name_file, "rb") as filetoload:  # which makes sure that the file is properly closed after reading
        LL_what_is_in_your_pickle = pickle.load(filetoload)


To save something in a pickle: ::

    with open(name_file, "wb" ) as pfile: # which makes sure that the file is properly closed after writing
            pickle.dump(LL_what_to_save, pfile)




:Release: |release|
:Date: |today|


