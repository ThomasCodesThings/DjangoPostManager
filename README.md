# PostManager

Just a simple Django application to create, edit and delete posts.

Installation guide:

 - [Linux installation](#linux)

### Versions
| Version | Changes |
|--|--|
| 1.0.0 | first working version |
| 1.1.0 | sorted request processing |
| 1.1.1 | final working version |

## Linux
 0. [Before you begin](#0-before-you-begin)
 1. [Install Python](#1-install-python)
 2. [Install PostgreSQL](#2-install-postgresql)
 3. [Create environment for Python](#3-create-environment-for-python)
 4. [Install Django (in new environment)](#4-install-django-in-new-environment)
 5. [Clone GitHub repository with PostManager](#5-clone-github-repository-with-postmanager)
 6. [Create system environment variables](#6-create-system-environment-variables)
 7. [Make & run Django migrations](#-7-make-run-django-migrations)
 8. [Start Django server](#8-start-django-server)

### 0. Before you begin
Update your list of available packages to get most recent version

    sudo apt update

### 1. Install Python

    sudo apt install python3

### 2. Install PostgreSQL
#### Install PostgreSQL service by following command

    sudo apt install postgresql postgresql-contrib

#### Start PostgreSQL service

    sudo systemctl start postgreqsl.service

#### Switch to **postgres** user (default PostgreSQL supervisor account)

    sudo -i -u postgres

#### Enable PostgreSQL CMD interface

    psql

#### Set up password for user **postgres** users need to have password when connecting to database(by default **postgres** does not have any password)

    \password postgres

#### Create database

    createdb <database_name> (e.g. 'amcef_microservice')


### 3. Create environment for Python 
#### Install *pip* and *venv*

    sudo apt install python3-pip python3-venv

#### Create own virtual environment

    python3 -m venv <env_name>

#### Activate it

    source <env_name>/bin/activate

Now you should see **(<env_name>)** in the beginning of command line, that means that you have entered virtual environment interface.

### 4.  Install Django (in new environment)

    pip install django
 
 ### 5. Clone GitHub repository with PostManager
 #### Create new directory
 

    mkdir <project_dir>

#### Create clone GitHub repository

    git clone https://github.com/ThomasCodesThings/DjangoPostManager.git <project_dir>


#### Switch to *DjangoDB* directory

    cd <project_dir>
    cd DjangoDB

 
#### Install required libraries

    pip install psycopg2-binary
	pip install requests
    pip install djangorestframework

#### Create "requirements.txt" file for version and library control

    pip freeze > requirements.txt

### 6. Create system environment variables

	export DB_SECRET_KEY=<django secret_key> (in this case 'django-insecure-xz1i4a9q$bi&+yylq2(y#esmks@fi#!wvykcegvj&i-0x1$&-v')
	export DB_TYPE=<database_btype> (in this case 'pgsql')
	export DB_NAME=<database_name> (in this case 'amcef_microservice')
	export DB_USERNAME=postgres (default PostgreSQL supervisor account)
	export DB_PASSWORD=<password for user 'postgres'> 
	export DB_IP=127.0.0.1 (IP address where database is hosted)
	export DB_PORT=5432 (port where database is running, '5432' is default port)

### 7. Make & run Django migrations

    python manage.py makemigrations <DjangoAppName> (e.g. 'PostManager')
	python manage.py migrate

### 8. start Django server

    python manage.py runserver
