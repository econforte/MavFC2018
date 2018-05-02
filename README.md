# mavfc
The official repository of the maverick food computer for Spring 2018 class

Written in Python/Django


Python Version 3.6
Django Version 1.11
Django REST Framework 3.6.2

The source is setup as an Eclipse, PyDev Django Project but could also be set as a project on PyCharm once cloned to a local environment.

Getting Started:

1.  Install Python from https://www.python.org/downloads/

2.  `python get-pip.py`

3.  `pip install Django`

4.  `pip install djangorestframework`

To handle database migrations, navigate to the folder containing manage.py and run the following commands in this order. Have to wait for the first one to complete first.

`python manage.py makemigrations`

`python manage.py migrate`

To run a test server navigate to the folder containing manage.py and run the command. You might have to configure manage.py to point to the right settings, the one used in this manage.py points to the dev environment settings:

`python manage.py runserver`

Navigate to http://127.0.0.1:8000/ to go to the home page.

To login to the application, refer to the material under the docs folder.
