Social Analytics Reports
===========================
Social Analytics Report Generator


### Features
* Multiple settings files for different evironments (dev, production, etc).
* A base settings file for settings common across environments
* Relative paths in the settings file
* django-dotenv support in manage.py
* Starter Base Template file
* Starter SASS / Compass styles
* An app directory to keep custom django apps organized and out of the
  project's base directory
* A development Procfile to launch the django dev server and compass
* dj-database-url to make it easier to move DB configuration into a ENV var
* Common Bundled Applications
* A a basic fabric file to help deployment to WebFaction
* A requirements template of basic apps to install

* Create a .env file in root to specifiey the DATABASE_URL and DJANGO_SETTINGS_MODULE, SECRET_KEY, etc _Note: .env files should not be checked into your git repo_



