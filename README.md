# "OpenFoodFacts App"


## "What is the goal of this application ?"

This application allows a user to find information on all common food products (ingredients, nutriscore, brand ...) and to search for healthier substitutes with the aim of a better diet.  
To do this, the application queries the API of the OpenFoodFacts website and records all the existing products in an SQL database, classifying them by categories.  
The user will also have the possibility to register the food products which interest him as well as the corresponding substitutes.  
Finally, it will be possible for the user to request the update of the database by downloading the latest information available on the API of the OpenFoodFacts site. 


## "How to install the app ?"

1) To install this application, you have to download all the files and folders contained in the following Github repository : https://github.com/MINCARELLI13/Projet_OFF.git  then save everything in a 'Project_OFF' folder for example (obviously, you can name this folder whatever you want).
2) Secondly you can create a virtual environment so as not to pollute the Python of your system with libraries which are only useful for this particular project (look at the end of this 'Readme' for know how to install a virtual environment). 
3) Finally, you will have to launch the 'requirements.txt' file which contains all the softwares (requests, mysql-connector-python and virtualenv) used by the application.  
(nota bene: this application is encoded with the python 3 language).


## "How to start the app?"

1) To start this application you need to open a command prompt and go to the 'Project_OFF' folder where you saved all the contents of the Github directory.
2) Then, you must activate the virtual environment created in step 2 of the section 'How to install the app?' (look at step 3 of the section 'How to create and use virtual environment?'). 
3) Finally you just have to run the "main.py" file with the following command : " python main.py ".


## "How to create and use virtual environnement ?"

1) In your command prompt, you must first install the "virtualenv" application by typing the following command : " pip install virtualenv " (that means installes "virtualenv" with "pip" application).
2) In the folder of the project, create the virtual environnement in typing the command line : " virtualenv -p python3 project_venv " (where "project_venv" is the name of the created virtual environment and "python3" is the version of python used in this new virtual environment).
3) To activate the virtual environment, type the commands :
	- " cd project_venv/Scripts " , because the "activate" file is located in the project_venv/Scripts /" folder,
	- " activate " to launch the virtual environnement.  
Finally type twice the command "cd .." to return to the source folder of your project.
4) You must too specify the external packages necessary for the project. To do this, put a file named "requirements.txt" in the source folder of your project.
5) Now you just have to install the dependencies useful for the project in typing the following command : " pip install -r requirements.txt "
6) Finally, to launch the application in the virtual environment "projet_venv", you must type the following command : "python main.py"
7) At the end, to quit the virtual environment "projet_venv", you just have to type : " deactivate "


## "Options :"

1) In order to optimize the performance of the application, only products of a few categories are downloaded from the API of the OpenFoodFacts site. These categories are: Savory Snacks, Cakes, Sodas, Frozen Desserts, and Ready Meals.  
You can modify this list of categories by modifying the variable 'CATEGORIES' located in the 'config.py' module which is in the 'Config' library of the 'Projet_OFF' folder.  

2) For the same reasons as mentioned above, for each of the categories only 20 products can be downloaded from the API OFF.  
You can also modify the number of products to download for each category by modifying the variable 'PRODUCTS_NB' located in the 'config.py' module which is in the 'Config' library of the 'Projet_OFF' folder.
