# WeightWhat

## Elevator pitch intro

a project to fool around with Flask extensions and dbs. Also w weight watch-like app.

## Requirements and dependencies
- Python 3.6 (tested)
- Flask  

## Directory and file structure

    .
        ├── app
        ├── config.py
        ├── migrations
        ├── README.md
        ├── requirements.txt
        ├── tests
        └── weight_what.py


Quick directory and file legend:
- **root**: main directory for the project as a whole
- **app**: houses the app with all it's sections and the app 
factory function (closer look below)
- **config.py**: class based configuration, with some config 
variables read in from env variables 
- **tests**: unittest tests
- **migrations**: Alembic migrations for the db
- **weight_what.py**: main orchestration file. Calls the app factory
function and passes the config object to it. Creates the shell 
context (adding the database and db models) and _test_ CLI command, 
registers the Migrate extension.


## Closer look at the ./app directory file structure

    .
    ├── auth
    │   ├── forms.py
    │   ├── __init__.py
    │   └── views.py
    ├── db_models.py
    ├── email.py
    ├── __init__.py
    ├── main
    │   ├── errors.py
    │   ├── forms.py
    │   ├── __init__.py
    │   ├── plots.py
    │   └── views.py
    ├── static
    │   ├── favicon.ico
    │   ├── img
    │   └── style.css
    └── templates

Quick directory and file legend:
- **auth** : auth blueprint files, including forms for authorization
(e.g. registration, login), views and errors
- **main** : main blueprint. Contains views, errors, forms and plot
definitions for the main app pages.
- **static** : static files: images, css style definitions, icons
- **templates** : all html and txt templates for the app, divided
into main templates in the **/templates** folder and **/auth**
and **/mail** templates as subdirectories
- **email.py** : email function definitions
- **db_models.py** : model definitions for SQL Alchemy. Model
definitions contain a large part of the app's functions as their
methods
- **\_\_init\_\_.py** : file housing the main app factory function.
Imports all the relevant extensions (apart from Migrate) and config 
data, initialises them, then registers blueprints, registers the 
Login Manager, and finally instantiates the app 

## Project flowchart

<img src="doc/weight_what_module_flowchart.png" alt="Architecture image">
                                                                           

_*This flowchart is less of an actual application map or classes 
diagram and more of just a sketch for quick lookups when I'm
getting lost in the local dependency forest. Helps to read the
above paragraphs to get value from it!_

## RAMBLE BREAK: How Blueprints work
Blueprints work as an intermediary grouping layer for view functions 
and error handlers. If you break up your app into functional 
sections (say, picture storage, picture upload, user profile 
settings), you can have a bunch of views/error handlers for each 
section. Instead of importing them all and registering with the app 
itself, we register them with blueprints for each section and then 
register the blueprints with the app in the main app factory 
function (here - in **./app/\__init\__.py**).

The twist is in the fact, that you first instantiate the Blueprint 
and then use the instance reference imported in the files defining 
the view functions and error handlers, which looks circular but is 
not really. The views and handlers are not executed until Bluprint 
imports them, at which point they are decorated to register with 
the Blueprint's instance.

## Installation

### 1. Download

### 2. Checking the installation

## Use cases 

## Further development 

## FAQ

**Q**: 

**A**:

## References
