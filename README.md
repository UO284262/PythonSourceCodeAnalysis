# PythonSourceCodeAnalysis
Python Source Code Analysis is a program designed to extract syntactic information of Python programs.

This information is stored in a relational database and can be used to analyze the information with data mining algorithms.

## Purpose
This program convert graph-like information obtained with the module _ast_ from the _Python Standard Library_ (PSL) into n-dimensional vectors sotres in a relational database. This process creates a _dataset_ with 16 homogeneous tables. 
This convertion allow classic data mining algorithms work with the _dataset_. This data mining algorithms can obtain information such as: most and least used syntactic elements, outlier syntactic patterns and association rules.

In addition to the syntactic information, the program allow the Python files used as argument to be flagged as Expert or Beginner. With this expertice level information linked to data mining results we can clasify new programs into Expert or Beginner programs attending to the presence or not of the different syntactic patterns identified as Expert patterns or Beginner patterns.

This type of information is high value to improve Python programming. We can use it to improve how Python is taught or to improve the tools offered by the different IDEs.

## Dataset generation
The dataset used to the outliers analysis contains more than 13 million database entities. This 13 million entities comes from:
- Student's projects from the subject Introduction to the Programming of the first year of the University of Oviedo degree in [Software Engineering](https://www.uniovi.es/estudia/grados/ingenieria/informaticasoftware)
- Expert's projects obtained with the GitHub API. The list of repositories used to obtain information are listed in the file [github_repos](https://github.com/ComputationalReflection/PythonSourceCodeAnalysis/blob/6444e0ecc23411c7e8a5ed6fdf959572d96a0ac5/github_repos).

## Example
As an example, we will supose that there is a directory named "python_projects". Inside this directory must be a structure a subdirectories with Python files.

The program can recieve up to 3 arguments, with of them optional:
- Directory of the Python programs u want to process
- Expertice level of the programs u want to process (Optional, "BEGINNER" as default)
- Directory and name of any python subdirectory u want to process as a unique program, ignoring program's default detection (Optional, no value by default)

![image](https://github.com/ComputationalReflection/PythonSourceCodeAnalysis/assets/98962592/3985466c-a67b-48a1-a64b-c99f17e8e199)

In this first call, we are processing the ./python_projects directory, flagged as EXPERT programs and following the default program detection system.

![image](https://github.com/ComputationalReflection/PythonSourceCodeAnalysis/assets/98962592/36c9d9f8-9a1b-4015-8b8a-582c3a0a8661)

In this call, we are processing the subdirectorie ./python_projects/program_1, flagged as EXPERT program and ignoring the default program detection system.




