# ISQA 8086-002 IoT, Big Data, Cloud Computing - MavFC Django Python App on Heroku

The following code updates were made for the Django Python application to be hosted on
Heroku:

*	File structure updated to drop root directory down one level:

  ![1](https://cloud.githubusercontent.com/assets/9102699/25315174/b8d96950-2816-11e7-96ea-8c54cc3a4c79.png)

*	Directory static added in main application mavfc with blank file (git does not recognize
  empty folders)

*	Settings file modified as follows:

 *	Heroku allowed as host:

      ```
      ALLOWED_HOSTS = ['mavistfc.herokuapp.com']
      ```

 *	Static file handling moved to WhiteNoise:

      ```
      INSTALLED_APPS = [ ... ,
      'whitenoise.runserver_nostatic',
      'django.contrib.staticfiles',
      'rest_framework.authtoken',]
      PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
      STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
      STATIC_URL = '/static/'
      STATICFILES_DIRS = (os.path.join(PROJECT_ROOT, 'static'),)
      STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
      ```

 *	Databases updated following initial declaration. This will utilize the PostgreSQL
 add-on we configure in Heroku:

      ```
      import dj_database_url
      db_from_env = dj_database_url.config(conn_max_age=500)
      DATABASES['default'].update(db_from_env)
      ```

*	pip requirements file to specify Python package dependencies, in root
directory: requirements.txt

  ![2](https://cloud.githubusercontent.com/assets/9102699/25315172/b8d857ae-2816-11e7-9d29-4a22217ed3c1.png)

  https://pip.pypa.io/en/stable/user_guide/#requirements-files

*	Profile to declare the commands run by the application’s dynos, in root directory:
Procfile (named exactly)

 *	For our application, we use the Gunicorn (“Green Unicorn”) pure-Python HTTP server for
 WSGI applications, to run multiple Python processes within a single dyno. We have the
 single command line for the web server:

       ```
       web: gunicorn mavfc.wsgi --log-file -
       ```
       https://devcenter.heroku.com/articles/procfile
       https://devcenter.heroku.com/articles/python-gunicorn


*	Python runtime file to specify Python version, in root directory: runtime.txt

  ![3](https://cloud.githubusercontent.com/assets/9102699/25315173/b8d88ba2-2816-11e7-8279-4dcf50c758ee.png)

  https://devcenter.heroku.com/articles/python-runtimes

To deploy to Heroku:

*	Create a Heroku account and download the Heroku CLI.
  https://devcenter.heroku.com/articles/heroku-cli

*	Log in to Heroku via the command line:

  ![4](https://cloud.githubusercontent.com/assets/9102699/25315175/b8dc68bc-2816-11e7-9850-90b61f03e287.png)

  ![5](https://cloud.githubusercontent.com/assets/9102699/25315171/b8d85a10-2816-11e7-864d-000c45cb97c5.png)

*	Navigate to the root directory of the project.

*	Enter command
```
heroku create
```
A Heroku app is created with a randomly generated name,
unless a name is specified (random name used here for documentation purposes).

  ![6](https://cloud.githubusercontent.com/assets/9102699/25315176/b8e04fe0-2816-11e7-86ce-8ca20069f814.png)

*	Enter command
```
git push heroku master
```
Heroku will recognize and install the Python
buildpack, download and install the package dependencies, copy static files, discover
process types, and deploy.

  ![7](https://cloud.githubusercontent.com/assets/9102699/25315177/b8e44bcc-2816-11e7-888e-707f75fc6dac.png)

  ![8](https://cloud.githubusercontent.com/assets/9102699/25315179/b8e54d38-2816-11e7-8d96-81ec05c64906.png)

*	When Heroku recognizes a Django app, it automatically provisions a Heroku Postgres
hobby-dev database and populates the DATABASE_URL environment variable.

  ![9](https://cloud.githubusercontent.com/assets/9102699/25315178/b8e542c0-2816-11e7-8d79-2450242d898f.png)

  ![10](https://cloud.githubusercontent.com/assets/9102699/25315180/b8e79778-2816-11e7-8a3f-5e007b91a23f.png)

*	To apply the migrations, enter command

  ```
  heroku run python manage.py migrate:
  ```

  ![11](https://cloud.githubusercontent.com/assets/9102699/25315181/b8e84fd8-2816-11e7-91f7-31bb0aa8f3c8.png)

*	Create a superuser with the command heroku run python manage.py createsuperuser:

  ![12](https://cloud.githubusercontent.com/assets/9102699/25315183/b8f21036-2816-11e7-80da-8f2a308ec1cb.png)

*	Navigate to the admin page of the Heroku application (e.g.
https://fierce-beach-23417.herokuapp.com/admin/) and log in with the superuser
credentials created:

  ![13](https://cloud.githubusercontent.com/assets/9102699/25315182/b8f067fe-2816-11e7-815e-904f4bf0a3df.png)

*	Create a flat page by clicking on Add and entering URL “/”, Title “Home Page” and Site
“example.com”:

  ![14](https://cloud.githubusercontent.com/assets/9102699/25315170/b8d5e366-2816-11e7-9cf3-d2d70b167b64.png)

*	The site is now navigable and all features should be operable. Changes to code may be
pushed directly to Heroku, or a Github repository may be linked for deployment.
