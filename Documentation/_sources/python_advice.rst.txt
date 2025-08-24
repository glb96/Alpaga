.. _python_advice_page:

Python advice
=============

Dear student, PhD, doctor, professor, and guests, or Igor user,

Here are some pieces of advice that you may find useful when working with Alpaga or Python in general. This page is not meant to replace a full course, but I hope it can help. If you have any tricks or advice, please do not hesitate to contact the Alpaga maintainer to have them added to this list.

------------
Some habits
------------

The Alpaga developer recommends some habits that can make your code more readable (or at least easier to understand, especially how the Alpaga code is written).

- Do not name your code versions something like ``new_analyse`` or ``fix_bug_analysis``.  
  If you do not want to use versioning software such as git, name them sequentially like ``analysis_1``, ``analysis_2``, etc.

- The name of every variable should be as explicit as possible. Do not call the list where the angles are stored ``list_a``; instead, use ``L_angle``. Try to stay close to the names you would use in your report, manuscript, or article.

- If it is a list, name it with the prefix *L_*.

- If it is a directory or a list with multiple dimensions, name it with the prefix *LL_*.

- If it is a temporary variable (within a loop), use the suffix *_t* or *_temp*.

- Initialize the size of a list if you know the dimension. This helps to spot unexpected behavior.

--------------------
Tricks to save time
--------------------

- If you copy and paste a piece of code more than 5-6 times, it may be time to define a new function.

- At the beginning of your code, define `WORK_DIR` and `SAVE_DIR` variables. This is helpful if you move your analysis code, data, or change computers.  
  You just have to set the absolute path to the data directory and where you want to save your figures once, and everything else will update automatically.  
  Example::

      import os  # this package should be installed in every standard Python environment
      WORK_DIR = '/home/lama/Datas'
      SAVE_DIR = '/home/lama/Article/MyNextNature'

  Then, declare your data directory and figure save path::

      directory = os.path.join(WORK_DIR, 'your_directory/other_one')
      figure_name_save = os.path.join(SAVE_DIR, 'Main/figure_2.pdf')

  This way, you do not have to worry about the software location—just check the `WORK_DIR` and `SAVE_DIR` variables.

- We recommend keeping the code that created a figure used in your report or article. Even better: copy this code and save it with the figure to ensure you can regenerate it if needed.

--------------------------------------------
Useful data structures in Python: dictionary
--------------------------------------------

To store multiple pieces of data (lists, arrays, etc.) in one place in Python, you can use a dictionary.

- Create a dictionary::

      LL_mydict = {}

- Add values associated with a key::

      LL_mydict['lama_1_name'] = 'Alpaga'
      LL_mydict['lama_1_age'] = 1.5
      LL_mydict['lama_1_habits'] = ['eat cheese', 'sleep']

- Access values::

      print(LL_mydict['lama_1_name'])
      age = LL_mydict['lama_1_age']
      print(age)

- Automating naming with dictionaries:  
  Suppose you performed several experiments with names ``C_1``, ``C_2``, ``C_5``, ``C_10``, ``C_20`` and corresponding concentrations::

      L_C = [1, 2, 5, 10, 20]

  Treat each experiment and store the result using::

      name_key = 'my_observable_' + str(concentration_value)
      LL_mydict[name_key] = my_observable_at_this_concentration

  At the end, the dictionary keys will be:  
  ``my_observable_1``, ``my_observable_2``, ``my_observable_5``, ``my_observable_10``, ``my_observable_20``.  
  You can loop over them::

      for concentration in L_C:
          name_key_t = 'my_observable_' + str(concentration)
          print(LL_mydict[name_key_t])

- Using individual variables like ``observable_c_1``, ``observable_c_2`` etc. is possible but not recommended. You cannot access them automatically in a loop, and copy-pasting increases the chance of mistakes.  
  Storing results in a single object (dictionary or user-defined object) with automatically generated keys is safer and more maintainable.

------------------------------
How to access the data: pickle
------------------------------

Another advantage of using dictionaries is easy storage in pickle format. Pickle is Python-friendly but not human-readable.  

- To open a pickle::

      import pickle
      name_file = '/some/directory/with/your/pickle/file.p' 
      with open(name_file, "rb") as filetoload:  # ensures proper closure after reading
          LL_what_is_in_your_pickle = pickle.load(filetoload)

- To save data in a pickle::

      with open(name_file, "wb") as pfile:  # ensures proper closure after writing
          pickle.dump(LL_what_to_save, pfile)


:Release: |release|
:Date: |today|
