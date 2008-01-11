TODO:
 - package python-decorator and python-toscawidgets
    http://toshio.fedorapeople.org/packages



Setting up a myfedora development environment

 # yum install TurboGears python-genshi python-feedparser python-simplejson
 $ python setup.py egg_info
 $ tg-admin sql create
 $ ./create-guest-user.py
 $ ./start-myfedora.py
