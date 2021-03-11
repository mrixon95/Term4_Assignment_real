# YourHealth: Better you, everyday!

This project is for tracking the overall physical, mental and financial health of an individual. 

Before commencing this project, a design stage was conducted and documentation was written. This included listing out the intended functionality, tech stack, user stories, drawing up wireframes and describing the planning methodology to be used for this project. 

The designing and planning documentation is located towards the end of this markdown file.



## Proposed Entity Relationship Diagram

- Each User can have multiple profile images, exercise log items, health insights, weekly sources of income and expenses, daily physical health records and goals.
- Each User can answer many questions for mental health surveys. The answer itself is made by one user for one particular question. Also a response option must be selected as part of each answer. 
- The survey questions belongs to one particular mental health survey and each question has its own question number.



![ERD](./docs/ERD.png)



## Project Management (Trello Board)



The Trello board screenshots track my progress throughout the project. It covers the application development, testing and deployment process.



### March 5

Lay out all the tasks for the YourHealth app and assign them all to the *To do List*. Also spin up an AWS EC2 instance and install a PostgreSQL database, ready to host database tables for the app.

![Trello_Board_2021_03_05](./docs/Trello_Board_2021_03_05.PNG)



### March 6

All tasks have been laid out and development is almost ready to commence. An AWS EC2 has been spun up and is hosting a PostgreSQL database, however it currently does not contain any tables for our application. 

Before populating the database with tables for the app, an Entity Relationship Diagram is essential. This is especially needed for the *YourHealth* app because the mental health survey, question, option and answer tables have a complicated set of relationships between them. They also requiring implementing both **composite primary and foreign keys**, so careful attention to the development code is needed. This includes importing models in the correct order so that no circular imports arise. Also, composite foreign keys need to be linked to the correct table and have a unique constraint. Without this constraint, the database integrity will be undermined.



![Trello_Board_2021_03_06](./docs/Trello_Board_2021_03_06.PNG)



### March 7

The Entity Relationship Diagram has been completed. The primary key of each table is bolded and the various relationships between tables are clearly identified. It is now time to write all the **endpoints** of the Flask Application and test them out. Additionally, a special endpoint will be included which downloads all the data. Each database table will have its entries saved to a **separate csv file**. This is to ensure that an admin user can quickly check that all the entries in the database are correct.



![Trello_Board_2021_03_07](./docs/Trello_Board_2021_03_07.PNG)



## DRY principle examples

My flask application makes heavy user of functions so the same code is not repeated multiple times. Each controller has a **url prefix**. This ensures that the same word is not needlessly repeated at the start of each endpoint definition. Below is an example of the prefix being used in the *goal* controller.

![url_prefix](./docs/url_prefix.PNG)



Each web controller has jinja templates that **inherit from the base.html file**. This ensures that the links for the google fonts, Bootstrap CSS, the title name and the authentication checks do not need to be re-written for each html page. Without inheriting code from the *base.html* file, a lot of code would need to be repeated, hence extending from the *base.html* file keeps the code dry.

![extends_base](.\docs\extends_base.PNG)



In order to not repeat the same form, I have created a forms file which has **classes for each form**. This allows for **reusability** of forms throughout the application.



![forms](.\docs\forms.PNG)









## Description of libraries used

My code uses many different flask libraries for reasons including user authentication, migrating databases, validating data and hashing passwords. Below, I import several flask libraries into my application code.



![libraries_used](.\docs\libraries_used.PNG)





The *flask_marshmallow* library is used to validate data inputted from the user. It ensures that the data types are correct, required fields are provided and the data passes validation checks. Here is an example below.



![flask_marshmallow](.\docs\flask_marshmallow.PNG)



As can be seen above, the health type field can only accept 1 of the 3 values. This ensures that there are only 3 different kinds of health insights that the application will accept. Also the degree of good or bad for each insight is restricted to being 1 of 5 possible values.

Additionally, the datatype for each field is specified. Without datatype constraint, a string like "Feb 2021" would be accepted in the date field, even though its not in the proper date format.  By using datatype constraints, the *date* entered must indeed be a valid date. Without this data type constraint, the integrity of the database could be compromised. 

Also, the *date* is required and cannot be left empty. The schema above will raise an error if the new insight is missing a *date*. This makes sense to be required since each insight would need to be recorded on a particular date.





The *flask_jwt_extended* library is used to require users to provide an authentication token when using a particular endpoint. This ensures that the identity of the user is known to the endpoint function. In order to retrieve that identity from the token, the *get_jwt_identity* function is implemented. By using this library, I can easily record which user created each *weekly income source*.



![authenticate identity](.\docs\authenticate identity.PNG)



Additionally, before deleting a *weekly income source*, I can verify that the user making the delete request is indeed the user who initially created it. Without this important check, a user could go into the app and delete any other user's data.





The *flask_migrate* library is used when making changes to the database tables. It automatically detects any differences between the tables in the current database and the tables in the newly changed database. The Flask-Migrate module stores the upgrade function needed to change the database from the previous to the current state it is in. Very importantly, it also ensures that the **current data is maintained**. This is critical because no data should be lost when making changes to our tables. The versions of the database are stored in the *versions* folder within the *migrations* directory so that there is a history of all the database changes.



![flask_migrate](.\docs\flask_migrate.PNG)





The *flask_bcrypt* library is used for security purposes. It has the functions *generate_password_hash* and *check_password_hash* which are used in my app to ensure that plain text passwords do not need to be stored in a database table. Instead, the hashed password gets stored so that the plain text password can remain secret. 

This is done for the sake of the user and their own security. Many users reuse the same password on multiple applications. If their plain text password is exposed on just one of those applications, then all their other accounts on other applications would then become venerable. Therefore, to avoid this occurring, the hashed password is stored instead of the plain text password. 

Additionally, bcrypt is different to other hashing algorithms like MD5 and SHA1 in that bcrypt is deliberately structured to be slow. Therefore, it would take an enormous amount of time to try out all possible passwords and attempt to hack a user's account. The slow pace of the bcrypt algorithm makes it more secure. 

Below, the library's function *check_password_hash* is used to compare the hashed submitted password to the hashed user password. If they are not the same hash value, then the password submitted must be incorrect. 



![flask_bcrypt](.\docs\flask_bcrypt.PNG)







## Installation

Steps:

1. Install python 3.8, python3.8-venv and python3-pip on your system.
   On Ubuntu run ```sudo apt install python3.8 python3.8-venv```
   Confirm installation occurred successfully by running ```python3.8 --version```

2. Install pip3 the python3 package manager.
   On Ubuntu run ```sudo apt-get install python3-pip```
   or ```python3 -m pip install pip```

3. Clone the app by running  ```git clone https://github.com/mrixon95/Term4_Assignment.git``` and cd into the newly cloned directory
   
4. On an Ubuntu OS, run the command ```python3 -m venv venv``` to download the venv module
   and ```source venv/bin/activate``` to activate the virtual environment.
5. The application has several dependencies which can be installed by running ```pip3 install -r requirements.txt``` within the virtual environment.


## Setup
Within the `src` folder, there is a ```.env.example``` template. Create a new file named`.env` and copy into it the contents of the `.env.example` file.  Finally, fill in the values of each variable to the right of the `=` sign.

## Custom Commands
These following flask commands below are for automating tasks related to database tables and for testing during the development phase.
1. ```flask db create```: creates database tables defined in registered models.
2. ```flask db seed```: populates database tables with dummy data using faker module.
3. ```flask db drop```: drops all database tables defined in registered models.



# CI/CD Pipeline



A CI/CD pipeline can be created as part of the continuous integration workflow when pushing modified code to GitHub.

1. The test_suite job will run on one of GitHub's VMs using the latest Ubuntu operating system. The new code pushed to GitHub is checked out into this VM.
2. The VM installs python3.8 and installs the dependencies. These dependencies and their version number are written on separate lines in the requirements.txt file.
3. The automated tests in the tests directory are ran 
4. The .py files are checked against the PEP8 style guide by running flake8



## Migrations

If you make any adjustments to the database tables eg. adding a new column to a table, then migrations are needed for recording those changes. The sqlachemy package```flask-migrate``` is in the requirements.txt file so no need to pip install it again.

To set it up:

1. Run `flask db init` and then drop everything in the database using ``` flask db-custom drop```
2. Create the migration using ```flask db migrate -m "Initial migration"``` and then run the migration using ```flask db upgrade```

You are now ready to make changes to the model that will automatically recorded every single time you migrate.