## Install Django Web Framework  

Follow the directions below to install Django. Install the relevant version. The documentation below refers to version 3.5x but as of April 2018, the same steps can be used for python 3.6x.
> See [How to Install Django](https://docs.djangoproject.com/en/1.10/topics/install/) for more detail and helpful links.

### Install Python Programming Language
>Install Python by navigating to https://www.python.org/downloads/ and selecting the 3.5x release.
Download the executable specific to the operating system on the local machine. Run it, check the box next to _Add
Python 3.5 to PATH_, and then click _Install Now_.

![pythoninstall](https://cloud.githubusercontent.com/assets/9102699/24379823/70dfaca8-130e-11e7-9b6b-254f7597a858.JPG)

![pythoninstall2](https://cloud.githubusercontent.com/assets/9102699/24379821/70df84f8-130e-11e7-84ef-4f62085af5d6.JPG)

Note: Python 3.5+ cannot be used on Windows XP or earlier.

To check that Python is installed and the version is correct, run `python` in the command prompt.
Enter Ctrl-Z or type `exit()`, and hit Return to exit.

![pythoninstalledcmdprompt](https://cloud.githubusercontent.com/assets/9102699/24379822/70df8c82-130e-11e7-9218-5f7b99ffbcdb.JPG)

Check that Python directories have been added to PATH environment variables. Open the _Control Panel_->_Advanced System
Properties_ and click on _Environment Variables…_. Click on PATH and then _Edit…_. Ensure that the /Pythonxx/ folder
and /Pythonxx/Scripts/ paths are included. Otherwise, add them.

![pythonenvvariables](https://cloud.githubusercontent.com/assets/9102699/24379825/70eef08c-130e-11e7-908c-1debc756b562.JPG)

![pythonenvvariablespath](https://cloud.githubusercontent.com/assets/9102699/24379826/70efc020-130e-11e7-8f96-0fa750f16b2c.JPG)

![pythonenvvariablespath2](https://cloud.githubusercontent.com/assets/9102699/24379828/70f33886-130e-11e7-87d4-b5fc0d066f50.JPG)
### Install pip Python Package Manager
>Pip is already installed with the Python 3.5x package; however, it needs to be upgraded. Open a command
prompt as an administrator (right-click on Command Prompt icon and Run as administrator), navigate
to the
Python/Pythonxx directory, and run

```
python -m pip install -U pip
```
>If this is not successful, download _get-pip.py_ from
[pip.pypa.io](https://pip.pypa.io/en/latest/installing/).
Right-click on the file and save to your /Pythonxx directory. Then open a command prompt as an
administrator,
navigate to the /Pythonxx directory, and run

```
python get-pip.py
```
![pythoninstallpip](https://cloud.githubusercontent.com/assets/9102699/24379819/70df2a8a-130e-11e7-847c-f0602aed4b80.JPG)
### Install Git

Download the relevant version of git from https://git-scm.com/downloads and follow the instructions to install
on the local machine.
If you already have Git installed, you can get the latest development version via Git itself by running git
clone https://github.com/git/git from the command prompt.

### Create a Virtual Environment
The following instructions pertain to Windows OS. For other OS, please consult the Python
[virtualenv](https://pypi.python.org/pypi/virtualenv) and
[virtualenvwrapper](https://pypi.python.org/pypi/virtualenvwrapper-win) pages.

Navigate to a directory to create your virtual environment. You may wish to create a directory for all virtual
environments by running `mkdir virtualenvs` in the desired base directory.

In the command prompt, navigate to your new /virtualenvs folder, run
```
pip install virtualenvwrapper-win
```
followed by
```
mkvirtualenv mavfc
```
to create a new virtual environment called _mavfc_.

This command also activates the virtual environment. The name of the project, in this case _mavfc_, will be
shown next to the command prompt
```
(mavfc) C:\Users\user\virtualenvs\mavfc>
```
To deactivate in order to change virtual environments, simply run `deactivate`

Next, install Django to your new virtualenv with
```
 pip install django
```
Once installed, verify by running
```
 django-admin --version
```
The command should return the relevant django version (1.11.3 at the time of this writing).

### Clone the mavfc git repository
Clone this mavfc repository into your new virtualenv by running
```
git clone https://github.com/econforte/MavFC2018/mavfc.git
```
If you are not logged in to Github, you will be prompted to input your username and password.

![installvirtualenvmavfc2](https://cloud.githubusercontent.com/assets/9102699/24379824/70e15a08-130e-11e7-94da-f258608f5d25.JPG)

### View the source files
The source files are now available in the specified directory. The structure of the mavfc Django project includes a base directory which holds a sub directory of the same name, the .gitignore file, and the README.md file.

![mavfcfilestructure](https://cloud.githubusercontent.com/assets/9102699/24379827/70f0254c-130e-11e7-8cb0-76fffb233278.JPG)

The subdirectory is the main Django app. Within this directory is the site directory. The structure of the
project is as follows.
```
project/
    app/
        manage.py
        site/
            __init__.py
            settings.py
            urls.py
        app/
            models.py
```
![installvirtualenvmavfc3](https://cloud.githubusercontent.com/assets/9102699/24379820/70df83ea-130e-11e7-833f-6ea93280919c.JPG)

The contents of the files can be viewed in the IDE of your choice.  One option, PyCharm, is available for
download at https://www.jetbrains.com/pycharm/download. To use this option, follow the directions to install
PyCharm, open the application, select _Open…_, then navigate to your mavfc project in your /virtualenvs
directory.

### Database Setup
**{this section needs to be modified}**

The database used at the time of this writing is a SQLite binary file.
If migrations have not yet been done, in a command prompt, navigate to the mavfc/mavfc directory. Run python manage.py makemigrations, then run python manage.py migrate.

### Run the mavfc application on local host
In a command prompt, navigate to the /mavfc/mavfc directory. Run
```
python manage.py runserver
```
Open a browser window and navigate to http://127.0.0.1:8000/. The home page of the mavfc application will
display. 

Open another command window to run other commands. To load sample data into your local environment, run the following commands in the given order.

```
python manage.py buildsample
```
```
python manage.py builddata
```
```
python manage.py buildsample
```
After loading this, you can login using the user “genericFCUser”. Password for this user can be found in the file “_builder_handler”  search for it in this file.

You can also create a super user for your application using the following command. This user is the admin. Provide the user details as and when prompted

```
python manage.py createsuperuser
```

Refresh your browser. To view the contents, click on Login at the top right and enter the credentials “genericFCuser” or the superuser credentials you created above. Provide the relevant password. Clicking on the Administrator dropdown and selecting Admin will bring up the Django administration menu.
