TurboGears2 Installation
========================
http://turbogears.org/2.0/docs/main/DownloadInstall.html

Additional packages needed:

    hg clone http://beta.toscawidgets.org/hg/tw.jquery/

Running orbited

    ./orbited orbited.cfg

Instead of connecting directly to the TG app, you'll need to connect to
orbited, which will proxy the necessary requests to TG.

    http://localhost:8000


================================================================================


Installation and Setup
======================

Install ``myfedora`` using easy_install::

    easy_install myfedora

Make a config file as follows::

    paster make-config myfedora config.ini

Tweak the config file as appropriate and then setup the application::

    paster setup-app config.ini

Then you are ready to go.

Run the Server
==============
paster serve config.ini


==========================
Creating a new application
==========================

    paster create --template=moksha-app <name>
