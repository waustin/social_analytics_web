"""
WSGI config for uam project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""
import os
import site

# ADD YOUR Webfaction Username and Virtual Env name to the settings below
webfaction_username = ""
virtualenv_name = ""

if webfaction_username == "" or virtualenv_name == "":
    raise NotImplementedError("Web Faction Username and VirtualEnv name are required in {0}".format(__file__))

ve_site_packages_path = "/home/{0}/.virtualenvs/{1}/lib/python2.7/site-packages".format(webfaction_username, virtualenv_name)

site.addsitedir(ve_site_packages_path)

# READ DOT ENV FILE to get settings and database url
env_file_name = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
import dotenv
dotenv.read_dotenv(env_file_name)


from django.core.wsgi import get_wsgi_application
from dj_static import Cling, MediaCling
application = Cling(MediaCling(get_wsgi_application()))


