TurboGears2 Installation
========================
http://turbogears.org/2.0/docs/main/DownloadInstall.html

Additional packages needed:

    hg clone http://beta.toscawidgets.org/hg/tw.jquery/

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
