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

## Methodology
In order to achieve the purpose explained before, the program uses the _ast_ module of the _Python Standard Library_ (PSL). This module defines a method that generate the _Abstract Syntax Tree_ (AST) of any _Python_ file that u pass as an argument.
With this AST as base of the program, the program defines a _Visitor_ pattern. The _visitor_ implements a method for every _Python_ element (all the _Python_ elements are listed in the ast module documentation https://docs.python.org/3/library/ast.html). This method collects all the important information from the AST element and, in addition, collects more information about the element's parent and the element's children. The information is collected with two techniques:
- Return-up: The method return information for its parent so it can store information of its children.
- Collect-down: The method recive information from its parent by the arguments and stores it.

Finally, the information stored in n-dimensional vectors is stored in 16 homogeneous tables that puts all the syntax-like elements together (Programs, Funcion definitions, Statements, Expressions, ...). As the syntactic information is now stored in table-like structures, we can apply data mining algorithms. In this repository, we apply a simple algorithm to detect outliers. This outliers let us clasify programs into Expert or Beginner attending to the programs used to generate the _dataset_.

## System
![image](https://github.com/ComputationalReflection/PythonSourceCodeAnalysis/assets/98962592/d693d7d0-cbe1-4338-aa4a-9731a1bfd280)

