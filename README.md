# Item Catlog

### By Bethapudi Pavani

## About Project

This Project is a RESTful web application utilizing the Flask Framework which accesses a SQL database that populates cricket country categories and their cricket players information. OAuth2 provides authentication for furuther CRUD functionality on the application. Currently OAunt2 is implemented for Google Accounts.

## In This Project

This project has one main python module 'university.py' which runs the flask application. A SQL database is created using the 'university_db.py' module and you can populate the database with test data using 'clg_info.py'

## Software Requirements

* Python3
* VirtualBox
* Vagrant
* Git
* SQLite DB
* Sublime Text3

## Required Skills

* Python3
* HTML
* CSS
* Bootstrap
* OAuth
* Flask Framework
* sqlalchemy

## URL's

- [Git](https://git-scm.com/downloads)
- [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
- [Vagrant](https://www.vagrantup.com/)
- [Vagrantfile](https://https://github.com/udacity/fullstack-nanodegree-vm)
- [Sublime Text](https://www.sublimetext.com/3)

## Some dependencies libraries

* pip install Flask
* pip install sqlalchemy
* pip install requests
* pip install psycopg2
* pip install oauth2client

## How to run python files

- Here we are creating three different files
	
	* university_db.py - It is a database file. In this database files i have created country and college tables.

	* clg_info.py - In this file we are inserting sample data.

	* university.py - It is main file for running application.

- Now open gitbash or commond prompt and inside project folder type python filename.py, 
	1. python university_db.py
	2. python clg_info.py
	3. python university.py


## JSON Endpoints

The following are open to the public:

Country Catalog JSON: `localhost:5000/country/JSON'`
	
	- It displays the whole country catalog. University categories and all college.

Playerwise JSON: `localhost:5000/university/<int:college_id>/menu/JSON`

    - Based on player id it  will displays the particular university college.

Country of particular player details JSON: `localhost:5000/university/<int:university_id>/menu/<int:college_id>/JSON`

    - it displays the particular university of particulr college information.

## Miscellaneous

This project is inspiration from [gmawji](https://github.com/gmawji/item-catalog).# item
# item
