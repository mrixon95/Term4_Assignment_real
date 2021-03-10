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