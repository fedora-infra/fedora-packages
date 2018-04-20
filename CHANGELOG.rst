4.1.1
-----

Pull Requests

- (cverna)          #358,  Add f28 to the active release overview
  https://github.com/fedora-infra/fedora-packages/pull/358
- (cverna)          #347, Add basic info about creating a new release
  https://github.com/fedora-infra/fedora-packages/pull/347

Commits

- 643263d4 Update unit tests
https://github.com/fedora-infra/fedora-packages/commit/643263d4
- f314776c Add pending release to the Active release overview
https://github.com/fedora-infra/fedora-packages/commit/f314776c
- 902ffa44 Oops forgot to add the signed tag
https://github.com/fedora-infra/fedora-packages/commit/902ffa44
- 74de4b89 Add basic info about creating a new release
https://github.com/fedora-infra/fedora-packages/commit/74de4b89


4.1.0
-----

Pull Requests

- (cverna)            #345, Use the new bodhi client provided by the bodhi-client package
  https://github.com/fedora-infra/fedora-packages/pull/345
- (@cverna)           #344, Fix the sources tab in the development environment
  https://github.com/fedora-infra/fedora-packages/pull/344
- (@cverna)           #343, Index packager
  https://github.com/fedora-infra/fedora-packages/pull/343
- (@cverna)           #342, Add some basic test for the indexer
  https://github.com/fedora-infra/fedora-packages/pull/342
- (@cverna)           #340, Delete the old document after an update.
  https://github.com/fedora-infra/fedora-packages/pull/340
- (@cverna)           #339, Add a docker-compose dev environment
  https://github.com/fedora-infra/fedora-packages/pull/339
- (@cverna)           #338, Update the fedmsg consumer code with newer xapain bindings.
  https://github.com/fedora-infra/fedora-packages/pull/338
- (@cverna)           #337, Remove result highlighting
  https://github.com/fedora-infra/fedora-packages/pull/337
- (@cverna)           #336, Remove module that are not used anymore
  https://github.com/fedora-infra/fedora-packages/pull/336
- (@cverna)           #335, Remove the widgets that are not used by the current app
  https://github.com/fedora-infra/fedora-packages/pull/335
- (@cverna)           #334, Load the logging configuration.
  https://github.com/fedora-infra/fedora-packages/pull/334
- (@cverna)           #327, Simplify how we get the active Fedora releases
  https://github.com/fedora-infra/fedora-packages/pull/327
- (@cverna)           #326, Use mdapi to get the upstream url instead of pdc
  https://github.com/fedora-infra/fedora-packages/pull/326

Commits

- f78f9cc9 Use the new bodhi client provided by the bodhi-client package
  https://github.com/fedora-infra/fedora-packages/commit/f78f9cc9
- a1457d56 Adding test for indexing the point of contact
  https://github.com/fedora-infra/fedora-packages/commit/a1457d56
- b87e0d77 Index the point of contact of a package.
  https://github.com/fedora-infra/fedora-packages/commit/b87e0d77
- 5343d698 We need to close the database after creating documents
  https://github.com/fedora-infra/fedora-packages/commit/5343d698
- 54022dab Fix the sources tab in the development environment
  https://github.com/fedora-infra/fedora-packages/commit/54022dab
- edb73761 Flake8 cleanup and use conftest.py
  https://github.com/fedora-infra/fedora-packages/commit/edb73761
- ae1afa4c Add some super simple test to begin with indexer testing
  https://github.com/fedora-infra/fedora-packages/commit/ae1afa4c
- eb44f829 Update indexer following bodhi API change.
  https://github.com/fedora-infra/fedora-packages/commit/eb44f829
- 09d5b5ed Delete the old document after an update.
  https://github.com/fedora-infra/fedora-packages/commit/09d5b5ed
- f92bb8ef Add a docker-compose dev environment
  https://github.com/fedora-infra/fedora-packages/commit/f92bb8ef
- d22ec10f Update the fedmsg consumer code with newer xapain bindings.
  https://github.com/fedora-infra/fedora-packages/commit/d22ec10f
- 07c78dab flake8 cleanup
  https://github.com/fedora-infra/fedora-packages/commit/07c78dab
- b072a3cc Remove result highlighting
  https://github.com/fedora-infra/fedora-packages/commit/b072a3cc
- 13f9b0a8 Remove module that are not used anymore
  https://github.com/fedora-infra/fedora-packages/commit/13f9b0a8
- eefaa126 Remove the widgets that are not used by the current app
  https://github.com/fedora-infra/fedora-packages/commit/eefaa126
- 91de5efe Load the logging configuration.
  https://github.com/fedora-infra/fedora-packages/commit/91de5efe
- fa4e3fc3 Simplify how we get the active Fedora releases
  https://github.com/fedora-infra/fedora-packages/commit/fa4e3fc3
- fcbabacb Use mdapi to get the upstream url instead of pdc
  https://github.com/fedora-infra/fedora-packages/commit/fcbabacb

4.0.0
-----

Pull Requests

- (@puiterwijk)           #316, Fix tw2 resource path when mounted outside siteroot.
  https://github.com/fedora-infra/fedora-packages/pull/316
- (@pypingou)             #315, Fixes
  https://github.com/fedora-infra/fedora-packages/pull/315
- (@pypingou)             #313, Couple of fixes
  https://github.com/fedora-infra/fedora-packages/pull/313
- (@cverna)               #312, Fix tw2 resource path when mounted outside siteroot
  https://github.com/fedora-infra/fedora-packages/pull/312
- (@cverna)               #304, Create the logger for the package overview widget.
  https://github.com/fedora-infra/fedora-packages/pull/304
- (@cverna)               #302, Remove fedorahosted link from Readme and only keep Vagrant setup for now.
  https://github.com/fedora-infra/fedora-packages/pull/302
- (@cverna)               #301, Remove dependency to xappy.
  https://github.com/fedora-infra/fedora-packages/pull/301
- (@cverna)               #300, Fix the default url to call pagure's api.
  https://github.com/fedora-infra/fedora-packages/pull/300
- (@cverna)               #297, Flake8 cleanup of index.py with max-line-length=90.
  https://github.com/fedora-infra/fedora-packages/pull/297
- (@cverna)               #295, Making the indexing more robust.
  https://github.com/fedora-infra/fedora-packages/pull/295
- (@cverna)		            #292, Replace python-appstream by the Gobject python bindings.
  https://github.com/fedora-infra/fedora-packages/pull/292
- (@cverna)               #290, Remove pkgdb pr280.
  https://github.com/fedora-infra/fedora-packages/pull/290
- (@techtonik)            #287, Rename README.txt to README.md for readability.
  https://github.com/fedora-infra/fedora-packages/pull/287
- (@yashvardhannanavati)  #283, point scm links to pagure instead of cgit.
  https://github.com/fedora-infra/fedora-packages/pull/283
- (@yashvardhannanavati)  #281, Final elimination of pkgdb.
  https://github.com/fedora-infra/fedora-packages/pull/281
- (@cverna)               #273, Use f25 in the vagrant env.
  https://github.com/fedora-infra/fedora-packages/pull/273
- (@ryanlech)             #266, Fedora bootstrap.
  https://github.com/fedora-infra/fedora-packages/pull/266
- (@ryanlech)             #263, change koji link in development.ini to https.
  https://github.com/fedora-infra/fedora-packages/pull/263
- (@lubomir)              #262, Use src.fedoraproject.org instead of pkgs.fp.o.
  https://github.com/fedora-infra/fedora-packages/pull/262
- (@xsuchy)               #255, add link to FAF.
  https://github.com/fedora-infra/fedora-packages/pull/255
- (@ryanlech)             #253, Added vagrant setup.
  https://github.com/fedora-infra/fedora-packages/pull/253
- (@cicku)                #249, Update default version of EPEL bug.
  https://github.com/fedora-infra/fedora-packages/pull/249
- (@puiterwijk)           #237, Make clear that bugs for packages aren't in this repo.
  https://github.com/fedora-infra/fedora-packages/pull/237
- (@ralphbean)            #234, Update xapian index when pkgdb_updater changes things like upstream_url.
  https://github.com/fedora-infra/fedora-packages/pull/234
- (@ralphbean)            #232, Add caching and cache invalidation to the bugzilla tab.
  https://github.com/fedora-infra/fedora-packages/pull/232
- (@thunderoy)            #227, My branch.
  https://github.com/fedora-infra/fedora-packages/pull/227

Commits

- 2da2b066b Fix tw2 resource path when mounted outside siteroot.
  https://github.com/fedora-infra/fedora-packages/commit/2da2b066b
- 0f3f1f422 Merge pull request #315 from fedora-infra/fixes
  https://github.com/fedora-infra/fedora-packages/commit/0f3f1f422
- a0408a7ef Make the package description look prettier by respecting their break line
  https://github.com/fedora-infra/fedora-packages/commit/a0408a7ef
- fa24bdc30 Fix small html error.
  https://github.com/fedora-infra/fedora-packages/commit/fa24bdc30
- 4c20b82d7 Merge pull request #313 from fedora-infra/icon_url.
  https://github.com/fedora-infra/fedora-packages/commit/4c20b82d7
- 8c9bfcc91 The new indexing get the full name of the icons with the .png.
  https://github.com/fedora-infra/fedora-packages/commit/8c9bfcc91
- 49404054f Widget templates are not full HTML pages...
  https://github.com/fedora-infra/fedora-packages/commit/49404054f
- e204eedca Fix url to the icon since the new indexer returns the full name.
  https://github.com/fedora-infra/fedora-packages/commit/e204eedca
- 1bf1face0 Create the logger for the package overview widget.
  https://github.com/fedora-infra/fedora-packages/commit/1bf1face0
- af4be7984 Refactor Indexing http get requests.
  https://github.com/fedora-infra/fedora-packages/commit/af4be7984
- 124d8ac15 Catch all exception to avoid Threads form dying.
  https://github.com/fedora-infra/fedora-packages/commit/124d8ac15
- 2deab5ed8 Prevent infinite call of latest_active method.
  https://github.com/fedora-infra/fedora-packages/commit/2deab5ed8
- 51e2d0352 Add weight to xapian indexing and complete indexing.
  https://github.com/fedora-infra/fedora-packages/commit/51e2d0352
- 206323b36 Removal of xappy depedency.
  https://github.com/fedora-infra/fedora-packages/commit/206323b36
- 8cb3fc7f5 Remove fedorahosted link from Readme and only keep Vagrant setup for now.
  https://github.com/fedora-infra/fedora-packages/commit/8cb3fc7f5
- b5d8619af Fix the default url to call pagure's api.
  https://github.com/fedora-infra/fedora-packages/commit/b5d8619af
- 55d832b88 Flake8 cleanup of index.py with max-line-length=90
  https://github.com/fedora-infra/fedora-packages/commit/55d832b88
- 5d54d0ad6 Check the main package branch info if we are checking a sub package.
  https://github.com/fedora-infra/fedora-packages/commit/5d54d0ad6
- b0545d23d Handle execption for mdapi.
  https://github.com/fedora-infra/fedora-packages/commit/b0545d23d
- b3b7d39ae Ask pdc to return 100 results per pages to speed things up.
  https://github.com/fedora-infra/fedora-packages/commit/b3b7d39ae
- 8f7b75dc2 Replace python-appstream by the Gobject python bindings.
  https://github.com/fedora-infra/fedora-packages/commit/8f7b75dc2
- 8ea5e8680 Merge pull request #281 from yashvardhannanavati/pkgdb-Massacre.
  https://github.com/fedora-infra/fedora-packages/commit/8ea5e8680
- f957a2b6d Merge branch 'develop' into pkgdb-Massacre.
  https://github.com/fedora-infra/fedora-packages/commit/f957a2b6d
- 495bfa655 Cleanup after code review.
  https://github.com/fedora-infra/fedora-packages/commit/495bfa655
- 0e3b81ba8 Initial massacre.
  https://github.com/fedora-infra/fedora-packages/commit/0e3b81ba8
- f5c30dd92 Initial removal of pkgdb.
  https://github.com/fedora-infra/fedora-packages/commit/f5c30dd92
- b2a27ee28d style fedora-packages to use the new fedora-bootstrap.
  https://github.com/fedora-infra/fedora-packages/commit/b2a27ee28
- 347f7383c Update README.md
  https://github.com/fedora-infra/fedora-packages/commit/347f7383c
- 6361e9538 Update and rename README.txt to README.md
  https://github.com/fedora-infra/fedora-packages/commit/6361e9538
- 08c1ea5dd point scm links to pagure instead of cgit
  https://github.com/fedora-infra/fedora-packages/commit/08c1ea5dd
- 491d6e4e5 Final elimination of pkgdb
  https://github.com/fedora-infra/fedora-packages/commit/491d6e4e5
- f678688d6 Use f25 in the vagrant environment. crank need to be set to 0.7.x for Turbogears2
  https://github.com/fedora-infra/fedora-packages/commit/f678688d6
- e602d29ac Use src.fedoraproject.org instead of pkgs.fp.o
  https://github.com/fedora-infra/fedora-packages/commit/e602d29ac
- 9183426d0 change koji link in development.ini to https
  https://github.com/fedora-infra/fedora-packages/commit/9183426d0
- 4320af5d9 add link to FAF
  https://github.com/fedora-infra/fedora-packages/commit/4320af5d9
- 537cb3d72 sort applications alphabeticaly
  https://github.com/fedora-infra/fedora-packages/commit/537cb3d72
- 3b31d2cba Added vagrant setup
  https://github.com/fedora-infra/fedora-packages/commit/3b31d2cba
- 0ff024ed1 Make clear that bugs for packages aren't in this repo
  https://github.com/fedora-infra/fedora-packages/commit/0ff024ed1
- 7c13cfbd9 Update xapian index when pkgdb_updater changes things like upstream_url.
  https://github.com/fedora-infra/fedora-packages/commit/7c13cfbd9
- 9e34af6cc Add caching and cache invalidation to the bugzilla tab.
  https://github.com/fedora-infra/fedora-packages/commit/9e34af6cc
- 6a90c33b4 Fix ez_setup like in #221.
  https://github.com/fedora-infra/fedora-packages/commit/6a90c33b4
- cbfc1bac4 added some missing dependencies
  https://github.com/fedora-infra/fedora-packages/commit/cbfc1bac4

3.0.4
-----

Pull Requests

- (@ralphbean)      #225, Streamline mdapi updates.
  https://github.com/fedora-infra/fedora-packages/pull/225

Commits

- 0b24e1438 specbump
  https://github.com/fedora-infra/fedora-packages/commit/0b24e1438
- 57d7637f3 Streamline mdapi updates.
  https://github.com/fedora-infra/fedora-packages/commit/57d7637f3

3.0.3
-----

Pull Requests

- (@ralphbean)      #212, Handle past and future mdapi json keys.
  https://github.com/fedora-infra/fedora-packages/pull/212
- (@ralphbean)      #214, Handle failure to copy an icon.
  https://github.com/fedora-infra/fedora-packages/pull/214
- (@ralphbean)      #218, Try a second icon_dir location.
  https://github.com/fedora-infra/fedora-packages/pull/218
- (@ralphbean)      #219, Try real hard to get a write lock for xapian.
  https://github.com/fedora-infra/fedora-packages/pull/219

Commits

- f378758a1 Specbump.
  https://github.com/fedora-infra/fedora-packages/commit/f378758a1
- 540079884 Handle past and future mdapi json keys.
  https://github.com/fedora-infra/fedora-packages/commit/540079884
- 47da24a64 Adjust key name as per review feedback.
  https://github.com/fedora-infra/fedora-packages/commit/47da24a64
- 9c63da97e Handle failure to copy an icon.
  https://github.com/fedora-infra/fedora-packages/commit/9c63da97e
- f688f30f2 Try a second icon_dir location.
  https://github.com/fedora-infra/fedora-packages/commit/f688f30f2
- 5b124ee39 Try real hard to get a write lock for xapian.
  https://github.com/fedora-infra/fedora-packages/commit/5b124ee39

3.0.2
-----

Pull Requests

- (@ralphbean)      #209, Use a threadpool when refreshing cache items.
  https://github.com/fedora-infra/fedora-packages/pull/209

3.0.1
-----

Pull Requests

- (@ralphbean)      #204, Log a warning, but don't email us.
  https://github.com/fedora-infra/fedora-packages/pull/204
- (@ralphbean)      #199, Fix icon suffix.
  https://github.com/fedora-infra/fedora-packages/pull/199
- (@ralphbean)      #201, Remove broken/unused rhbz stuff.
  https://github.com/fedora-infra/fedora-packages/pull/201
- (@ralphbean)      #202, Fix .spec pygments lexer.
  https://github.com/fedora-infra/fedora-packages/pull/202
- (@ralphbean)      #203, Fix git scraping.
  https://github.com/fedora-infra/fedora-packages/pull/203
- (@ralphbean)      #207, Remove rhel5 links.
  https://github.com/fedora-infra/fedora-packages/pull/207
- (@ralphbean)      #208, Change text from Owner to Point of Contact.
  https://github.com/fedora-infra/fedora-packages/pull/208
- (@ralphbean)      #200, Fix up links to bodhi and koji.
  https://github.com/fedora-infra/fedora-packages/pull/200

Commits

- 600480058 Raise a keyerror just to make this simpler.
  https://github.com/fedora-infra/fedora-packages/commit/600480058
- 0c5ab0a58 Move xapian document preparation out of the threadpool.  The bindings aren't threadsafe on el6.
  https://github.com/fedora-infra/fedora-packages/commit/0c5ab0a58
- a891c2938 Also, log, so we know where we are on the fan-in thread.
  https://github.com/fedora-infra/fedora-packages/commit/a891c2938
- 7202059f4 Fix icon suffix.
  https://github.com/fedora-infra/fedora-packages/commit/7202059f4
- 1dfb63dbb Add build links on the Active Releases page.
  https://github.com/fedora-infra/fedora-packages/commit/1dfb63dbb
- 777f0ea55 Make koji builds a link to koji.
  https://github.com/fedora-infra/fedora-packages/commit/777f0ea55
- 1651a67a4 Remove broken/unused rhbz stuff.
  https://github.com/fedora-infra/fedora-packages/commit/1651a67a4
- e4e6cb79e Fix .spec pygments lexer.
  https://github.com/fedora-infra/fedora-packages/commit/e4e6cb79e
- 6d9dd0da7 Fix git scraping.
  https://github.com/fedora-infra/fedora-packages/commit/6d9dd0da7
- 84ddb19a4 Log a warning, but don't email us.
  https://github.com/fedora-infra/fedora-packages/commit/84ddb19a4
- dcdeaaf90 Remove rhel5 links.  Fixes #205.
  https://github.com/fedora-infra/fedora-packages/commit/dcdeaaf90
- 954b76de3 Change text from Owner to Point of Contact.
  https://github.com/fedora-infra/fedora-packages/commit/954b76de3

2.0.20
------

Pull Requests

- (@lmacken)        #94, Gracefully handle requests for invalid tabs
  https://github.com/fedora-infra/fedora-packages/pull/94
- (@relrod)         #115, darken footer text slightly, fix #114
  https://github.com/fedora-infra/fedora-packages/pull/115
- (@ralphbean)      #121, Force stuff down to ascii in the overview widget.
  https://github.com/fedora-infra/fedora-packages/pull/121
- (@ralphbean)      #123, Get epel7 releases working.
  https://github.com/fedora-infra/fedora-packages/pull/123
- (@Fale)           #120, Fix broken urls
  https://github.com/fedora-infra/fedora-packages/pull/120
- (@jasontibbitts)  #137, Wrap "LATEST BUILD" field.
  https://github.com/fedora-infra/fedora-packages/pull/137
- (@ralphbean)      #148, Add fedmenu.
  https://github.com/fedora-infra/fedora-packages/pull/148
- (@ralphbean)      #149, Fix bugzilla + tw2.
  https://github.com/fedora-infra/fedora-packages/pull/149
- (@genodeftest)    #165, Use HTTPS where possible
  https://github.com/fedora-infra/fedora-packages/pull/165
- (@pypingou)       #166, Use the same approach as elsewhere to include the bodhi image
  https://github.com/fedora-infra/fedora-packages/pull/166
- (@ralphbean)      #179, Get fedora-packages working with bodhi2.
  https://github.com/fedora-infra/fedora-packages/pull/179
- (@ralphbean)      #180, Remove broken link from the builds tab.
  https://github.com/fedora-infra/fedora-packages/pull/180
- (@ralphbean)      #182, Fix koji search links.
  https://github.com/fedora-infra/fedora-packages/pull/182
- (@ralphbean)      #181, Fix the spec widget.
  https://github.com/fedora-infra/fedora-packages/pull/181
- (@ralphbean)      #183, Move datagrepper query to the client side.
  https://github.com/fedora-infra/fedora-packages/pull/183
- (@ralphbean)      #184, Lots of quoting/escapery fixes.
  https://github.com/fedora-infra/fedora-packages/pull/184
- (@ralphbean)      #185, Handle more bodhi2 cases.
  https://github.com/fedora-infra/fedora-packages/pull/185
- (@ralphbean)      #186, Tell python-bugzilla that we don't want to cache cookies or tokens.
  https://github.com/fedora-infra/fedora-packages/pull/186
- (@ralphbean)      #187, Add a search field to the bugs table.
  https://github.com/fedora-infra/fedora-packages/pull/187

Commits

- af09bf509 Gracefully handle requests for invalid tabs
  https://github.com/fedora-infra/fedora-packages/commit/af09bf509
- 9067ca35e darken footer test slightly, fix #114
  https://github.com/fedora-infra/fedora-packages/commit/9067ca35e
- 2635e08d0 Fix broken urls
  https://github.com/fedora-infra/fedora-packages/commit/2635e08d0
- 7e03df8c1 Force stuff down to ascii in the overview widget.
  https://github.com/fedora-infra/fedora-packages/commit/7e03df8c1
- 8c0ba0b98 Get epel7 releases working.
  https://github.com/fedora-infra/fedora-packages/commit/8c0ba0b98
- 564ee475f Wrap "LATEST BUILD" field.
  https://github.com/fedora-infra/fedora-packages/commit/564ee475f
- db0cb2852 Add fedmenu.
  https://github.com/fedora-infra/fedora-packages/commit/db0cb2852
- ef9e6743f Fix bugzilla + tw2.
  https://github.com/fedora-infra/fedora-packages/commit/ef9e6743f
- e3a95d63f Remove libravatar.
  https://github.com/fedora-infra/fedora-packages/commit/e3a95d63f
- ddb935e4c Use HTTPS where possible
  https://github.com/fedora-infra/fedora-packages/commit/ddb935e4c
- 8ae822bc2 Use the same approach as elsewhere to include the bodhi image
  https://github.com/fedora-infra/fedora-packages/commit/8ae822bc2
- 1cf29d4c3 Fix busted change from #166.
  https://github.com/fedora-infra/fedora-packages/commit/1cf29d4c3
- aa237e8ce Get fedora-packages working with bodhi2.
  https://github.com/fedora-infra/fedora-packages/commit/aa237e8ce
- bcc145b07 Remove broken link from the builds tab.
  https://github.com/fedora-infra/fedora-packages/commit/bcc145b07
- 9981a9880 Remove ascii encoding bit now that tw2.core uses render_unicode.
  https://github.com/fedora-infra/fedora-packages/commit/9981a9880
- 4a962f34f Fix the spec widget.
  https://github.com/fedora-infra/fedora-packages/commit/4a962f34f
- b9b69dc5c Fix koji search links.
  https://github.com/fedora-infra/fedora-packages/commit/b9b69dc5c
- 0d13f4b6a Move datagrepper query to the client side.
  https://github.com/fedora-infra/fedora-packages/commit/0d13f4b6a
- d6e157fb4 Add a space.
  https://github.com/fedora-infra/fedora-packages/commit/d6e157fb4
- 4d1d15e74 Imports.
  https://github.com/fedora-infra/fedora-packages/commit/4d1d15e74
- 84ba8633b Move unquoting out of the search filter util and into the search connector.
  https://github.com/fedora-infra/fedora-packages/commit/84ba8633b
- fcf3ecd9f Move this to the right place, but escape before applying regexes.
  https://github.com/fedora-infra/fedora-packages/commit/fcf3ecd9f
- 9c8b77189 Don't unquote so aggressively in the connector middleware.
  https://github.com/fedora-infra/fedora-packages/commit/9c8b77189
- ccb306cea Handle more bodhi2 cases.
  https://github.com/fedora-infra/fedora-packages/commit/ccb306cea
- 218e5b4bd Tell python-bugzilla that we don't want to cache cookies or tokens.
  https://github.com/fedora-infra/fedora-packages/commit/218e5b4bd
- ba3c82e10 Add a search field to the bugs table.
  https://github.com/fedora-infra/fedora-packages/commit/ba3c82e10
- 7fe64a9c9 Remove changelog header.
  https://github.com/fedora-infra/fedora-packages/commit/7fe64a9c9

2.0.17
------

- make the bz cookiefile location configurable. `b90adc962 <https://github.com/fedora-infra/fedora-packages/commit/b90adc96215c38e152fdffe20aa0f0eeef6a6434>`_
- Merge pull request #32 from fedora-infra/feature/configurable-bz-cookiefile `3081e1f27 <https://github.com/fedora-infra/fedora-packages/commit/3081e1f2704554531bb51fb98a8debd9d3f23027>`_
- 2.0.10 `37861bde8 <https://github.com/fedora-infra/fedora-packages/commit/37861bde8f64073517752bcb2421fb2b5734ed28>`_
- Add a link to Fedora's cgit from the package chrome. `e9c50bf76 <https://github.com/fedora-infra/fedora-packages/commit/e9c50bf76dcb5822286cf269a6416511c5071306>`_
- Resize all images in the "In Other Apps" bar to 16x16 (as suggested by Ralph Bean). `3ede52c37 <https://github.com/fedora-infra/fedora-packages/commit/3ede52c37577025733e8e900fa0c1681397bbd38>`_
- Merge pull request #33 from tjanez/add_cgit_link `3a3d8f4de <https://github.com/fedora-infra/fedora-packages/commit/3a3d8f4de221a542456a70fbb5d3556b2a2fd8cc>`_
- Correct the woefully incorrect distmappings table. `d5e9113fb <https://github.com/fedora-infra/fedora-packages/commit/d5e9113fbbf03fa5fadb7014d0460c02052ecbf8>`_
- Fedora 17 is EOL.  Long live Fedora 20! `bcc20abbe <https://github.com/fedora-infra/fedora-packages/commit/bcc20abbe00227ce07c21af3bf7b46da6f9588f7>`_
- Update the footer with the link to file a ticket. `5fd837b96 <https://github.com/fedora-infra/fedora-packages/commit/5fd837b96d3026defb4aee5716609e876f6ecbe4>`_
- Merge pull request #34 from fedora-infra/feature/more-distmappings-fixes `3b76b3121 <https://github.com/fedora-infra/fedora-packages/commit/3b76b3121a0d99d27d10fa8b93a5cc6b6364da70>`_
- Merge pull request #36 from fedora-infra/feature/ticket-link `81d6202a5 <https://github.com/fedora-infra/fedora-packages/commit/81d6202a58cffb562be9cd40b0dcdf14a45ae710>`_
- Add a space to the response from the bodhi connector. `4a9302454 <https://github.com/fedora-infra/fedora-packages/commit/4a9302454d133e708cfddf70e61683a79bb19dce>`_
- Try to future-proof against future pylons-less tg. `5e592550e <https://github.com/fedora-infra/fedora-packages/commit/5e592550e15a5fa2cff0fc4341df9865cd1a0c9f>`_
- Merge pull request #46 from fedora-infra/feature/added-space `3366cef0a <https://github.com/fedora-infra/fedora-packages/commit/3366cef0a3c5d91db51910d436314091d9a0f541>`_
- Merge pull request #47 from fedora-infra/feature/pylons-import `2d252fefc <https://github.com/fedora-infra/fedora-packages/commit/2d252fefc8b47099350eef3c32ac600d8bf52e86>`_
- Include epel bugs in the bugs list.  Fixes #6. `78761e26b <https://github.com/fedora-infra/fedora-packages/commit/78761e26bd8cc592f642333d47be89e167efffdc>`_
- PEP8: ez_setup/__init__.py and remove import unused shutil `082537430 <https://github.com/fedora-infra/fedora-packages/commit/0825374307404b8f0289eb2a0eb4cd74e55ec91d>`_
- Fix string in the version setuptools `68b758cb4 <https://github.com/fedora-infra/fedora-packages/commit/68b758cb49acfada04fe215fb70d9cdb44114d11>`_
- PEP8: config package `62e65f7d0 <https://github.com/fedora-infra/fedora-packages/commit/62e65f7d0780eac2263cd72e60924abcd3ebc089>`_
- PEP8: fedoracommunity/connector/api package and refactoring code. `fd93b30ef <https://github.com/fedora-infra/fedora-packages/commit/fd93b30efbd4b973787997d39e8ec23e915c120a>`_
- Change in widgets package and bodhiconnector.py `371c1c28d <https://github.com/fedora-infra/fedora-packages/commit/371c1c28df989d55371a902ccd8675bde681be92>`_
- PEP8: bugzillaconnector.py `90d76ad60 <https://github.com/fedora-infra/fedora-packages/commit/90d76ad60fd83854ea4d54bae9efa362a9a4d76f>`_
- PEP8: fasconnector.py `35d991791 <https://github.com/fedora-infra/fedora-packages/commit/35d991791c3297e064d7ed135b3f529a3bcfdc8b>`_
- PEP8: websetup.py `6f32d2671 <https://github.com/fedora-infra/fedora-packages/commit/6f32d267134a613cce121effa995ab398191b7bc>`_
- PEP8: stats.py `3fe651b2c <https://github.com/fedora-infra/fedora-packages/commit/3fe651b2c1cf1e44484f14a50403681f963ae437>`_
- PEP8: distmappings.py `cc86c989c <https://github.com/fedora-infra/fedora-packages/commit/cc86c989cdf9b8301686d4fc2da8654d47454967>`_
- Change in faswhoplugin.py `9d6c28861 <https://github.com/fedora-infra/fedora-packages/commit/9d6c288618646e97e25c5a8d8f786d4ffc9b0f08>`_
- Changes in gitconnector.py `0613eef3a <https://github.com/fedora-infra/fedora-packages/commit/0613eef3af66da4c5446f46838bbdeec1159b44e>`_
- Changes in jsonconnector.py `8bc5549e9 <https://github.com/fedora-infra/fedora-packages/commit/8bc5549e9f965e1d0f756abf78b371f843052462>`_
- Changes in kojiconnector.py `a26a2f51b <https://github.com/fedora-infra/fedora-packages/commit/a26a2f51b515a64f133ea51e9d6877c21eb02ac5>`_
- Merge pull request #50 from echevemaster/develop `cc5c1e720 <https://github.com/fedora-infra/fedora-packages/commit/cc5c1e720b249eac34e0e8d02b077638ef9f181f>`_
- Merge pull request #49 from yograterol/develop `a63744ca5 <https://github.com/fedora-infra/fedora-packages/commit/a63744ca502f84f494be97ad65a57b3526971cd8>`_
- Merge pull request #48 from fedora-infra/feature/epel-bugs `b806c9c3b <https://github.com/fedora-infra/fedora-packages/commit/b806c9c3bfa9c397e95994985dd3ebbea5051472>`_
- Provide a way for the koji builds indexer to initialize itself. `247fc1004 <https://github.com/fedora-infra/fedora-packages/commit/247fc10041e36597fa67b387049bf922bf641e4f>`_
- Merge pull request #51 from fedora-infra/feature/builds-action `c639ade7f <https://github.com/fedora-infra/fedora-packages/commit/c639ade7fea23f1aad7016a9c03b2dd864300eca>`_
- Get fedora-packages working again against modern TG2+crank. `57ed33fd7 <https://github.com/fedora-infra/fedora-packages/commit/57ed33fd7b742fbde311d3ac3110463a1404dd4e>`_
- Remove widgets that we don't actually use but which have a dep on broken repoze.who/what `3b655a931 <https://github.com/fedora-infra/fedora-packages/commit/3b655a9314bea55fa88bf453abf22645868a865a>`_
- Forgot to rm this template too. `c71c7cbeb <https://github.com/fedora-infra/fedora-packages/commit/c71c7cbeba9f1192ac8e177c33e9f368f5315150>`_
- Merge pull request #52 from fedora-infra/feature/remove-repoze `a1553bd2d <https://github.com/fedora-infra/fedora-packages/commit/a1553bd2d886b793e3d9264f9bb8584ab9efa8bf>`_
- Quote up the search term to make it url safe. `dd46b8592 <https://github.com/fedora-infra/fedora-packages/commit/dd46b85929419996716e046543a65851f78d9266>`_
- Doubly encode search term to allow slashes input by various means. `c61781cc4 <https://github.com/fedora-infra/fedora-packages/commit/c61781cc4bf547cced37abf7137e1be40261fb93>`_
- Remove a space. `197d12afc <https://github.com/fedora-infra/fedora-packages/commit/197d12afcb157bcce3b98006609f40c7f91e09a3>`_
- The last piece to get searches with slashes working. `ea1a906c9 <https://github.com/fedora-infra/fedora-packages/commit/ea1a906c99932c9c7b83529cf82638851391fc3a>`_
- Merge pull request #53 from fedora-infra/feature/search-with-slash `50e8e27c2 <https://github.com/fedora-infra/fedora-packages/commit/50e8e27c26b43771e7ab37cb2dd08ba7b85274e1>`_
- 2.0.11 `f4cb9ca09 <https://github.com/fedora-infra/fedora-packages/commit/f4cb9ca09d0f160e8e3b1547249fb27646ed3db9>`_
- Fix regression introduced in 62e65f7d0780eac2263cd72e60924abcd3ebc089. `67632cadd <https://github.com/fedora-infra/fedora-packages/commit/67632cadd3c5b1d3c58d73a3ac564164c2ce6806>`_
- Merge pull request #54 from fedora-infra/feature/fix-config-regression `a0704a72c <https://github.com/fedora-infra/fedora-packages/commit/a0704a72ce729eeea855e9661ad2bbb3d2c6a308>`_
- 2.0.12 `bb800cf09 <https://github.com/fedora-infra/fedora-packages/commit/bb800cf0982d62925566360f20f9fa9dfc0d36f2>`_
- added message cards link at search results `e3afe3378 <https://github.com/fedora-infra/fedora-packages/commit/e3afe33781e267dc586c6e3eb08c35a049d8dfd5>`_
- Fix "File a ticket" link `d40400cd8 <https://github.com/fedora-infra/fedora-packages/commit/d40400cd8314055a4b5bbe4771432e6966bef301>`_
- Merge pull request #57 from nanonyme/patch-1 `4a3a1cad8 <https://github.com/fedora-infra/fedora-packages/commit/4a3a1cad89663392a549be36af80eb1240731196>`_
- removed hardcoded message cards link `9c2947c90 <https://github.com/fedora-infra/fedora-packages/commit/9c2947c905f6ae3edd0b0e13bdb84ebd73e04c55>`_
- added definition for message card's link `5e1485110 <https://github.com/fedora-infra/fedora-packages/commit/5e1485110b158575200c80a42e30abe9ed76c8a1>`_
- added template to render message card's link `3a9801467 <https://github.com/fedora-infra/fedora-packages/commit/3a9801467c9cb89a61a8043090c8f11751572985>`_
- added new line at the end of file `26d2a43f5 <https://github.com/fedora-infra/fedora-packages/commit/26d2a43f59ea693222620c17495f8d39adaabac3>`_
- added a function to get datagrepper url and package name `ef3d9221d <https://github.com/fedora-infra/fedora-packages/commit/ef3d9221dbdc08be937ee28d2b4839417d76d73b>`_
- added datagrepper base url i.e. http://localhost:5000 `66f5b48d5 <https://github.com/fedora-infra/fedora-packages/commit/66f5b48d5e9fdf52a1e648ba480f3bfe4bd438ac>`_
- render message cards url `6c049f267 <https://github.com/fedora-infra/fedora-packages/commit/6c049f2670e1faf18eb04172b105c7e05580c709>`_
- changed datagrepper_url `ea853310a <https://github.com/fedora-infra/fedora-packages/commit/ea853310ac8d016b130e349a3e05e187f6349d8c>`_
- render message cards `25cc90073 <https://github.com/fedora-infra/fedora-packages/commit/25cc900734d217b39d925d437fd4f8dd895af0ab>`_
- added function to retrieve message cards from datagrepper `9bd8f757d <https://github.com/fedora-infra/fedora-packages/commit/9bd8f757d1aa10a8a65fc28596568328bd02ee39>`_
- added chrome as parameters `ff4f7644c <https://github.com/fedora-infra/fedora-packages/commit/ff4f7644cf21fbc6738872ccad8790a8cca9e906>`_
- adding css for history cards `b0304f1ed <https://github.com/fedora-infra/fedora-packages/commit/b0304f1ed01191aee6ea70e2d143edd12fd199fb>`_
- added definition for .details-history class to shift link to the right `f3f2f2def <https://github.com/fedora-infra/fedora-packages/commit/f3f2f2defafa784a1818344702b9f9e95b0c2e14>`_
- added css for history-cards and message-card classes `d3e5037fe <https://github.com/fedora-infra/fedora-packages/commit/d3e5037feaee00f969eac7ff2679cc44f04acd7f>`_
- added new line at the end of file `8eeec6aed <https://github.com/fedora-infra/fedora-packages/commit/8eeec6aed070ba713cc0b30476caa6613f6082cb>`_
- Merge pull request #56 from charulagrl/develop `b894a035c <https://github.com/fedora-infra/fedora-packages/commit/b894a035c1ed71564c9636b0d9e2880a0392058e>`_
- Use a blocking call to retask to improve cache worker performance.  Fixes #59. `4936da666 <https://github.com/fedora-infra/fedora-packages/commit/4936da666de46843e8bab3d06df9963108230035>`_
- Merge pull request #60 from fedora-infra/feature/async-worker `5f37d4fc4 <https://github.com/fedora-infra/fedora-packages/commit/5f37d4fc4e4063372419c7c9453822882e3a6a1c>`_
- Fix a syntax error in the latest builds indexer `72e6f8631 <https://github.com/fedora-infra/fedora-packages/commit/72e6f8631b2da5059e7945bad900e7ffade22b55>`_
- Update distmappings `6e288e276 <https://github.com/fedora-infra/fedora-packages/commit/6e288e276280b2f3a58ffd49d1f1aac3641f9600>`_
- Needed this to develop locally... `3733ce7e9 <https://github.com/fedora-infra/fedora-packages/commit/3733ce7e98906d2a873a0b9592982fa35c8225c4>`_
- Typeahead! `a954bf3c3 <https://github.com/fedora-infra/fedora-packages/commit/a954bf3c3ac4ea0faf51d24979c9ae9f90e1d17a>`_
- fix width `82172db1c <https://github.com/fedora-infra/fedora-packages/commit/82172db1c5a7c307bd3ccf7eb558d7ebdd9011d8>`_
- Move the history block down one. `a8055f2fb <https://github.com/fedora-infra/fedora-packages/commit/a8055f2fb0380b6ea52d53684787fb464cfb907e>`_
- 2.0.13 `56c5c1d77 <https://github.com/fedora-infra/fedora-packages/commit/56c5c1d7741edc5d8171cc9a93b49bf963c25b99>`_
- Spec bump. `b32fe1ce0 <https://github.com/fedora-infra/fedora-packages/commit/b32fe1ce06ca717024b45dbd06107c326b450ced>`_
- Merge pull request #62 from fedora-infra/typeahead `b79814cd4 <https://github.com/fedora-infra/fedora-packages/commit/b79814cd48e49e8e0fdca0749f5d908e44033a99>`_
- added css for datetime `b444faf6a <https://github.com/fedora-infra/fedora-packages/commit/b444faf6a77caa262e482776c76aec8953264e89>`_
- Merge pull request #63 from charulagrl/develop `9dc9c2ec9 <https://github.com/fedora-infra/fedora-packages/commit/9dc9c2ec9049597ef30dbcb79d23a99b2d09f64f>`_
- Avoid crashing if datagrepper is not available. `924de7f09 <https://github.com/fedora-infra/fedora-packages/commit/924de7f092e37edcbc68dc915afde4738bde18e9>`_
- Avoid defaulting to armv7hl on relationships tabs. `93960cd67 <https://github.com/fedora-infra/fedora-packages/commit/93960cd675226c9e8f43062f6eef1c898e6552c2>`_
- Merge pull request #65 from fedora-infra/feature/default-x86 `7a2864473 <https://github.com/fedora-infra/fedora-packages/commit/7a2864473ad878fb03dc2c707777dc1e56ebc509>`_
- Merge pull request #64 from fedora-infra/feature/safe-datagrepper `49423d0a9 <https://github.com/fedora-infra/fedora-packages/commit/49423d0a93476fc6938bac1cd69e3760e9024d3f>`_
- Reorganize the params argument for style. `eaec03b67 <https://github.com/fedora-infra/fedora-packages/commit/eaec03b67d0730665c1d38bf58ff86e65fd53226>`_
- Add exclusive arguments to the datagrepper query. `18b80ba0c <https://github.com/fedora-infra/fedora-packages/commit/18b80ba0c90d9de1140bff0503ad98573d56b619>`_
- Merge pull request #67 from fedora-infra/feature/exclude-datagrepper-spam `b9bdc647f <https://github.com/fedora-infra/fedora-packages/commit/b9bdc647f5a4e799ffa0881d82426c32406383d2>`_
- Make datagrepper icons square. `a0bcfa41c <https://github.com/fedora-infra/fedora-packages/commit/a0bcfa41c52f3513e7bf6346f7b143f081d20e28>`_
- Merge pull request #69 from fedora-infra/feature/square-icons `18f4a808e <https://github.com/fedora-infra/fedora-packages/commit/18f4a808e18cb4a35bdb5f717d9127da69a93399>`_
- Use a lockfile for yum stuff. `45ca0f52b <https://github.com/fedora-infra/fedora-packages/commit/45ca0f52b2f50d27ca782d3095227c85b2bde864>`_
- Merge pull request #70 from fedora-infra/feature/yumlock `3e3d91213 <https://github.com/fedora-infra/fedora-packages/commit/3e3d91213814cf9cb3c351cc9c7299cb4ce599d9>`_
- 2.0.14 `97a5496d7 <https://github.com/fedora-infra/fedora-packages/commit/97a5496d7e1f538f852e1369605f1f5ecc9e1e38>`_
- Bump spec. `61577ecfb <https://github.com/fedora-infra/fedora-packages/commit/61577ecfb86934d6377e08ca072ec19162e4aead>`_
- Defer yumlock creation until runtime. `1f354589b <https://github.com/fedora-infra/fedora-packages/commit/1f354589ba153a67eb344557b81b654059201894>`_
- Quick release. `3ba73f9d9 <https://github.com/fedora-infra/fedora-packages/commit/3ba73f9d9000ff8c25076fad475fec39d8e5c772>`_
- Merge pull request #73 from fedora-infra/feature/adjusted-yumlock `15b74ecf7 <https://github.com/fedora-infra/fedora-packages/commit/15b74ecf7d2bca110ab10b9e7ecda6285656e3e9>`_
- Log exceptions. `5aee21231 <https://github.com/fedora-infra/fedora-packages/commit/5aee212312ef870632e80cb157a2887c21cfece5>`_
- Merge pull request #74 from fedora-infra/feature/log-exceptions-plz `5d2940c78 <https://github.com/fedora-infra/fedora-packages/commit/5d2940c78e51cd6b577b6df76e2d1c2a6436c53e>`_
- Try to be smarter with our locking. `3213aa794 <https://github.com/fedora-infra/fedora-packages/commit/3213aa7941bbccb1e62e5d9791b95e04a86b75d2>`_
- Remove the locking stuff. `d5ca72b13 <https://github.com/fedora-infra/fedora-packages/commit/d5ca72b133d09ed861f4746ed6f8ed7bdecd2ed2>`_
- Merge pull request #75 from fedora-infra/feature/roll-that-locking-stuff-back `6c85d3a53 <https://github.com/fedora-infra/fedora-packages/commit/6c85d3a53271e543dde641611bd75e0f011ea066>`_
- 2.0.15 `17a8905ff <https://github.com/fedora-infra/fedora-packages/commit/17a8905ff85bd56a115421f3a1ad640888c9a900>`_
- A blossom of hatred. `9f00d1bf8 <https://github.com/fedora-infra/fedora-packages/commit/9f00d1bf84aa152863d370c1a1edef5c347335de>`_
- Add a configurable timestamp to this tool. `ce7efe680 <https://github.com/fedora-infra/fedora-packages/commit/ce7efe680dd536d36f0e9594350c67b9aad084d9>`_
- Merge pull request #78 from fedora-infra/feature/configurable-timestamp `b8901cfb8 <https://github.com/fedora-infra/fedora-packages/commit/b8901cfb871479b4f872f9fccb096eff3d548a58>`_
- Remove the relationships tab from the UI. `a9893b61d <https://github.com/fedora-infra/fedora-packages/commit/a9893b61d9fbac3c726a7dd048b05063b8c4f067>`_
- Merge pull request #84 from fedora-infra/feature/all-good-things `1506dc97e <https://github.com/fedora-infra/fedora-packages/commit/1506dc97efb1018970c617ab67cac639d627f2c0>`_
- :fire: Do the pkgdb2 thing :fire: `732be9a8a <https://github.com/fedora-infra/fedora-packages/commit/732be9a8aedaf7721da569f5b52d6abc149ea5b1>`_
- Also, require this lib. `12da36cbd <https://github.com/fedora-infra/fedora-packages/commit/12da36cbdb0978a5b74a5d4112dc6c8d4dece99f>`_
- Switch to pkgdb2 api in the indexer. `a06c97e0d <https://github.com/fedora-infra/fedora-packages/commit/a06c97e0d23c6324875e1d8464490a686b80614f>`_
- Merge pull request #85 from fedora-infra/feature/pkgdb2 `b301a677a <https://github.com/fedora-infra/fedora-packages/commit/b301a677ad1d7dca1bc4745dc46167cb58a4fb54>`_
- gitbranchname -> branchname. `3f659e20b <https://github.com/fedora-infra/fedora-packages/commit/3f659e20bd5b960c5d775bef49fb47adf6227279>`_
- 2.0.16 `82ac17951 <https://github.com/fedora-infra/fedora-packages/commit/82ac1795149c944b55ecaf62d8c73e32659a9159>`_
- Update links to pkgdb2. `2f5cbffcf <https://github.com/fedora-infra/fedora-packages/commit/2f5cbffcfd97c5a68ee7132c1f13184ca5a9e6a3>`_
- Merge pull request #86 from fedora-infra/feature/pkgdb2-link `8991633b6 <https://github.com/fedora-infra/fedora-packages/commit/8991633b66bb86f6fd8b71c2499c6a3b897603d8>`_
- Protocol agnosticism.  Fixes #79. `0c1ff2c07 <https://github.com/fedora-infra/fedora-packages/commit/0c1ff2c07137f55eca34d69d8fb4fed1135318d5>`_
- Fix logic. `8af096df3 <https://github.com/fedora-infra/fedora-packages/commit/8af096df33cee5866b26297accf00f737ecdafe4>`_
- Merge pull request #90 from fedora-infra/feature/ssl `89d33dfac <https://github.com/fedora-infra/fedora-packages/commit/89d33dfaca30993acaf22d7596e80980a4ba73f1>`_
- Merge pull request #91 from fedora-infra/feature/pkgdb2-fix `7a6ea8a27 <https://github.com/fedora-infra/fedora-packages/commit/7a6ea8a277c113b5d2dc8f6dd27ad8fd5f1dbb9f>`_

2.0.9
-----

- Import old code from python-moksha-wsgi-1.2.0. `ed1e07d71 <https://github.com/fedora-infra/fedora-packages/commit/ed1e07d710da22bfa1ffa38e70506e617694c85b>`_

2.0.8
-----

- Modernize distmappings. `175ff35bc <https://github.com/fedora-infra/fedora-packages/commit/175ff35bc387a17e731bc50fc1d9c3280eb5908f>`_
- Unescape JSON so the relationships tab (and other things) work. `74fe187ed <https://github.com/fedora-infra/fedora-packages/commit/74fe187ed216bf569f3328c21d3dff4667ee304a>`_
- Ignore version map from cronjob. `d14c44e62 <https://github.com/fedora-infra/fedora-packages/commit/d14c44e6253f0059eba3a8a35396620e809290e6>`_
- Merge pull request #25 from fedora-infra/feature/unescape-that-json `d58c46816 <https://github.com/fedora-infra/fedora-packages/commit/d58c468162f41f1d2dab0be43038b9c7d45e35b9>`_
- Remove error obfuscation. `99a63bb32 <https://github.com/fedora-infra/fedora-packages/commit/99a63bb32b61aa86392880a5c7a7ce5ba238cc9b>`_
- Move exception handling into call_get_file_tree for consistency. `6aea9bb49 <https://github.com/fedora-infra/fedora-packages/commit/6aea9bb49a6eeceb9b96115f79a7a7786f54919e>`_
- Merge pull request #27 from fedora-infra/feature/remove-obfuscation `232681011 <https://github.com/fedora-infra/fedora-packages/commit/232681011bed6cac820487d8ed5633a9c736c888>`_
- Update hotpatch for bugzilla-0.9.0. `ff3ea739e <https://github.com/fedora-infra/fedora-packages/commit/ff3ea739eaa7a511998b57a5caf4e3ee987ea69a>`_
- Karma_level needs to be double nested here in order to work. `e2c878809 <https://github.com/fedora-infra/fedora-packages/commit/e2c87880991bbc33a12272afce0a1a744a5ace9c>`_
- Sometimes latest_builds itself is None. `bba62f8cc <https://github.com/fedora-infra/fedora-packages/commit/bba62f8cc482958503911df8357509dfe0e3de9c>`_
- Merge pull request #30 from fedora-infra/feature/latest-builds-bugfix `039a34dc3 <https://github.com/fedora-infra/fedora-packages/commit/039a34dc3b7c0cde624dc09fd38ef69804e47918>`_
- Merge branch 'feature/double-nesting-craziness' into develop `092e08951 <https://github.com/fedora-infra/fedora-packages/commit/092e08951627075b583232f395c4fb4f0e799ed7>`_
- Protect version comparison against 2.3.0dev `ad2c47f0a <https://github.com/fedora-infra/fedora-packages/commit/ad2c47f0a2e2ce1eeb0534dc4796451d277e8111>`_
- Really disable those request extensions. `6378a8758 <https://github.com/fedora-infra/fedora-packages/commit/6378a87581ae5cbe6f6689260d94f3a4abfb1166>`_

2.0.7
-----

- Add in python-memcached dependency to bootstrap.py and setup.py `4c57d59dd <https://github.com/fedora-infra/fedora-packages/commit/4c57d59ddc8692f1240ba1cd72592400a0a91ffa>`_
- Merge pull request #7 from daviddavis/develop `bd932195b <https://github.com/fedora-infra/fedora-packages/commit/bd932195b2cc5fc4d91a62ccdc387ac87fa6ce0b>`_
- Link dogpile into our virtualenv `e7861885b <https://github.com/fedora-infra/fedora-packages/commit/e7861885b741be92ba3fe3a7e4792a539ae071b2>`_
- Link memcache into our virtualenv `a7f078d4c <https://github.com/fedora-infra/fedora-packages/commit/a7f078d4c111f6b2f7a4379840e2290be16ac1cf>`_
- we need memcached too `bcd9df12c <https://github.com/fedora-infra/fedora-packages/commit/bcd9df12cbc290bf79dcb6f6c00f10e09a804305>`_
- Get BodhiConnector.query_active_releases working without a WSGI environ (#11) `46c332599 <https://github.com/fedora-infra/fedora-packages/commit/46c33259991608f572d942b6ad0c6b654cabba0a>`_
- Changes to karma image. Adding colors. `6b109068b <https://github.com/fedora-infra/fedora-packages/commit/6b109068b74c58a4cf33f64828fe2ca836ab99d0>`_
- Merge pull request #15 from marijar/karma `d287c7364 <https://github.com/fedora-infra/fedora-packages/commit/d287c73647a188a7e26323a6944ea2066cb74f40>`_
- Support bugzilla-0.8.0 `60f3d6591 <https://github.com/fedora-infra/fedora-packages/commit/60f3d6591e89e2f525bd6fb94a75b01f86933937>`_
- Update the bugzillahacks.py for 0.8.0 `3c4cc9fb0 <https://github.com/fedora-infra/fedora-packages/commit/3c4cc9fb0e8b6947f8078fb528e0a8737a7c5cb6>`_
- Get off of the old moksha.common.lib.helpers stuff. `a8a8662ba <https://github.com/fedora-infra/fedora-packages/commit/a8a8662baa9ac2e883eb8ee53bfc3953a6e78a52>`_
- Don't escape the spec file widget. `ac00f53e6 <https://github.com/fedora-infra/fedora-packages/commit/ac00f53e67bce662b7095ede200bb8c202a99567>`_
- Fix misleading text in bugs widget. `792511fb6 <https://github.com/fedora-infra/fedora-packages/commit/792511fb6ba802b9019ce43b9ae8955ab619b372>`_
- The latest from updates-testing is no longer necessary for development. `dce25ee02 <https://github.com/fedora-infra/fedora-packages/commit/dce25ee02af8a28999aad44d9ac04221996ba638>`_
- Make the redis queue not connect at import time. `59d3763ba <https://github.com/fedora-infra/fedora-packages/commit/59d3763bad6a75f977222488a8cfe44399cf9601>`_
- Turn off memcached stuff by default for development. `55a94cb71 <https://github.com/fedora-infra/fedora-packages/commit/55a94cb7137c33b06f063a6b4f3e9d8a47c4037e>`_
- Merge pull request #17 from fedora-infra/feature/optional-caching-for-development `1c27cd54a <https://github.com/fedora-infra/fedora-packages/commit/1c27cd54aad4a91d96ac76c233f86b210a526e36>`_
- Merge pull request #18 from fedora-infra/feature/no-updates-testing-plz `fd718d5f6 <https://github.com/fedora-infra/fedora-packages/commit/fd718d5f64ca7084bdde17dc38ce17fff921e6b6>`_
- Merge pull request #19 from fedora-infra/feature/fix-bugs-text `9a9910c78 <https://github.com/fedora-infra/fedora-packages/commit/9a9910c78aa32b65a371ff96b0ea29842f658870>`_
- If bug_version is a string, don't truncate it otherwise return the first element only `58452a8e6 <https://github.com/fedora-infra/fedora-packages/commit/58452a8e6156e5341a932e920f3d77ffe10e4fe3>`_
- Merge pull request #23 from fedora-infra/feature/fix_bugs_release `0f1720f3b <https://github.com/fedora-infra/fedora-packages/commit/0f1720f3bef10c68753cca848c599d45d02f4427>`_
- You've got to be kidding me. `1b008dbf4 <https://github.com/fedora-infra/fedora-packages/commit/1b008dbf422f5e9a6a5d463b25e13ed18774f4a9>`_

2.0.6
-----

- Cleanup. `2ea45de61 <https://github.com/fedora-infra/fedora-packages/commit/2ea45de61e2f05ea0cc27e59e93e767eaa13ae02>`_
- Be yet still more conservative with memcached connections in the cache worker daemon. `155e88a12 <https://github.com/fedora-infra/fedora-packages/commit/155e88a1294b39866dd2ea774922552997ae11e1>`_

2.0.5
-----

- Provide example of the distributed_lock argument to dogpile.cache. `b9d8831c2 <https://github.com/fedora-infra/fedora-packages/commit/b9d8831c26cbd4e72efa41b52e1a7e5584cbff65>`_
- Fix inconsistent dogpile keys due to randomized dict order. `32ba269f8 <https://github.com/fedora-infra/fedora-packages/commit/32ba269f87268f9747fe71152cb7edee3175813a>`_
- Use experimental dogpile background refresh. `c211bc671 <https://github.com/fedora-infra/fedora-packages/commit/c211bc67118db6af2c1ca97d967eb1942783f6d2>`_
- Release bump. `4f2da59ae <https://github.com/fedora-infra/fedora-packages/commit/4f2da59ae21c2e4b95be124ac5aa9cb95d92e5fc>`_
- Correct version for new bug link for Fedora EPEL packages. `eef70e6ba <https://github.com/fedora-infra/fedora-packages/commit/eef70e6ba739ec2c5b63620f71349f113d4cb1f0>`_
- Fix that bonkers SSL timeout with bugzilla. `32c0fb907 <https://github.com/fedora-infra/fedora-packages/commit/32c0fb9075b44e3533e48c07eef13b05413fd57b>`_
- Update to use latest experimental dogpile async stuff. `919e4de15 <https://github.com/fedora-infra/fedora-packages/commit/919e4de1549afe54c2c5369e0f62d7a3ae7cf0fb>`_
- Release bump. `54edb2426 <https://github.com/fedora-infra/fedora-packages/commit/54edb2426f100c09941d25c1adb0e519d74b9e39>`_
- Py2.6 support for the bugzilla SSL hack. `d823e1671 <https://github.com/fedora-infra/fedora-packages/commit/d823e1671f5d4e6a256f8f6ed93a0927a88f15a9>`_
- Release bump. `dc73e3aed <https://github.com/fedora-infra/fedora-packages/commit/dc73e3aed371ffb8cd135ba271e62366f7ac9ff5>`_
- Fix bug where /packages/qt returned a 404. `ad438ffc9 <https://github.com/fedora-infra/fedora-packages/commit/ad438ffc90ac7c1ff1edc354c9930385beb21ca5>`_
- Fix "python-webob1.2" 404 error. `93abf4389 <https://github.com/fedora-infra/fedora-packages/commit/93abf4389078700f3d320bf4111e8efba8e6dc2b>`_
- Redirect to search instead of /error in case of 404 on package name. `4d9c426c6 <https://github.com/fedora-infra/fedora-packages/commit/4d9c426c6ef2131d675740fe4eb3d0ba85087c2d>`_
- Use a more modern hardcoded url at the bottom of search/index.py. `6c5b19417 <https://github.com/fedora-infra/fedora-packages/commit/6c5b19417e677d40de41122860476ec6f8dc685b>`_
- Release bump. `94c2948b6 <https://github.com/fedora-infra/fedora-packages/commit/94c2948b6081788480914b8c6b2800109ab6dfb4>`_
- Fix a pesky spelling error. `525383f9d <https://github.com/fedora-infra/fedora-packages/commit/525383f9d8ac606f8cd15fff365f7b997baabad7>`_
- Disable fancy-patched dogpile stuff until it is generally available. `c7bc19f25 <https://github.com/fedora-infra/fedora-packages/commit/c7bc19f259619a12bc05a30b7d03aaa0839bd022>`_
- Add dogpile to bootstrap.py. `2d4aea06a <https://github.com/fedora-infra/fedora-packages/commit/2d4aea06a8c6bfa6ab17fe9725b5db1b10e0be5b>`_
- dist-rawhide is gone `4fd257a08 <https://github.com/fedora-infra/fedora-packages/commit/4fd257a08655a5651c86d71ab2c14ea8b1398d58>`_
- Make the dogpile caching optional. `bb18eb7b2 <https://github.com/fedora-infra/fedora-packages/commit/bb18eb7b208cf280bbc44115f48f7dd248f05948>`_
- Simplify dogpile cache interfaces. `c897dbc6d <https://github.com/fedora-infra/fedora-packages/commit/c897dbc6d314d9fc44e9d2843d219961404e03d4>`_
- Use python-retask to distribute cache refreshing to a worker proc. `ae6d8c7d4 <https://github.com/fedora-infra/fedora-packages/commit/ae6d8c7d4ca4e60b6034ce11da3744a71c73c16a>`_
- Tweak to get koji connector working. `8c74c4924 <https://github.com/fedora-infra/fedora-packages/commit/8c74c4924ccb473714461f06889c115653e39639>`_
- Tweak to get yum connector working. `5df0c06e8 <https://github.com/fedora-infra/fedora-packages/commit/5df0c06e8d26ec039aca5278e49dbd000ec56ec6>`_
- Specfile updated with new deps. `eb73d9adb <https://github.com/fedora-infra/fedora-packages/commit/eb73d9adbb7cb67abd84117da7478f3eb3654c85>`_
- Merge pull request #1 from fedora-infra/feature/optional-dogpile `462737762 <https://github.com/fedora-infra/fedora-packages/commit/46273776237a2b4745faef1ea9f7ec902eb55e15>`_
- Merge pull request #2 from fedora-infra/feature/long-running-queue `f31795b4f <https://github.com/fedora-infra/fedora-packages/commit/f31795b4fec041606ed69f2bb7fcfeac800fb664>`_
- Half-working daemon setup. `9fe610e5f <https://github.com/fedora-infra/fedora-packages/commit/9fe610e5fa2a9a18a46246cf5d18a574e4badfce>`_
- Better setup for daemon-hood.  pkgdb and bodhi connectors are still broken. `40ff5c37b <https://github.com/fedora-infra/fedora-packages/commit/40ff5c37b64adb5a17cbe6f38b98f27b1cadb1b7>`_
- Tweaks to try and get the daemon to work.  Nothing significant. `a7d2298e3 <https://github.com/fedora-infra/fedora-packages/commit/a7d2298e3e766e7bb15b2d895e8c1604521d2017>`_
- Merge pull request #3 from fedora-infra/feature/worker-as-a-daemon `d5d997dcc <https://github.com/fedora-infra/fedora-packages/commit/d5d997dcc9ee187634a795582abcb48b5b727eab>`_
- Don't install dogpile from fedora just yet.  What we need hasn't hit updates-testing yet. `9134423dd <https://github.com/fedora-infra/fedora-packages/commit/9134423dd9b0c46ac7239dbf2baf0a838b41ee12>`_
- Use updates-testing.  :P `bfba73852 <https://github.com/fedora-infra/fedora-packages/commit/bfba73852f79976b046f1a83a4369c77fc593af9>`_
- Add a link to Fedora Tagger from the package chrome. `b73c67b58 <https://github.com/fedora-infra/fedora-packages/commit/b73c67b58b4827b8037d929e5d96eb188173a6a9>`_
- Call Thread.start(), not run() `b75d37bd3 <https://github.com/fedora-infra/fedora-packages/commit/b75d37bd30acf82ca84c78f4226b1f61617afae5>`_
- Merge branch 'develop' of github.com:fedora-infra/fedora-packages into develop `b85723329 <https://github.com/fedora-infra/fedora-packages/commit/b857233297b5b9098be73a410578a95b761a9053>`_
- Deth to pyCurl! `cdbe2d4f9 <https://github.com/fedora-infra/fedora-packages/commit/cdbe2d4f969fed88d40a05140d17ca9fcc9b27cb>`_
- Fix the raw patch links `75c0e25c9 <https://github.com/fedora-infra/fedora-packages/commit/75c0e25c9bf50e237223fc7ff5a9eae09561b5f4>`_
- Include init script for fcomm-cache-worker. `1e0287cbf <https://github.com/fedora-infra/fedora-packages/commit/1e0287cbfa9987b140dde70ccd89637242a1cdba>`_
- Merge branch 'develop' of github.com:fedora-infra/fedora-packages into develop `552d537c6 <https://github.com/fedora-infra/fedora-packages/commit/552d537c6d7599fecd3c6874c88fcb2f2bbb0e26>`_
- Fix crazy sigterm bug in the cache worker. `6fbfa731f <https://github.com/fedora-infra/fedora-packages/commit/6fbfa731ffd1a5779b11ec54e2eeb4ddcca5751b>`_
- Config for the cache-worker daemon. `e34f9fbb3 <https://github.com/fedora-infra/fedora-packages/commit/e34f9fbb3880c2a77a921e676d027ddc16c56044>`_
- Merge branch 'feature/kill-pycurl' into release/2.0.5 `1ee2cc643 <https://github.com/fedora-infra/fedora-packages/commit/1ee2cc64394245df8e7865486ebb77457dd6bdc1>`_
- Revert "Deth to pyCurl!" `7de233bfd <https://github.com/fedora-infra/fedora-packages/commit/7de233bfdcac73334a537ee0bb305ef98e076bfe>`_

2.0.4
-----

- Provide example of the distributed_lock argument to dogpile.cache. `b9d8831c2 <https://github.com/fedora-infra/fedora-packages/commit/b9d8831c26cbd4e72efa41b52e1a7e5584cbff65>`_
- Fix inconsistent dogpile keys due to randomized dict order. `32ba269f8 <https://github.com/fedora-infra/fedora-packages/commit/32ba269f87268f9747fe71152cb7edee3175813a>`_
- Use experimental dogpile background refresh. `c211bc671 <https://github.com/fedora-infra/fedora-packages/commit/c211bc67118db6af2c1ca97d967eb1942783f6d2>`_
- Release bump. `4f2da59ae <https://github.com/fedora-infra/fedora-packages/commit/4f2da59ae21c2e4b95be124ac5aa9cb95d92e5fc>`_
- Correct version for new bug link for Fedora EPEL packages. `eef70e6ba <https://github.com/fedora-infra/fedora-packages/commit/eef70e6ba739ec2c5b63620f71349f113d4cb1f0>`_
- Fix that bonkers SSL timeout with bugzilla. `32c0fb907 <https://github.com/fedora-infra/fedora-packages/commit/32c0fb9075b44e3533e48c07eef13b05413fd57b>`_
- Update to use latest experimental dogpile async stuff. `919e4de15 <https://github.com/fedora-infra/fedora-packages/commit/919e4de1549afe54c2c5369e0f62d7a3ae7cf0fb>`_
- Release bump. `54edb2426 <https://github.com/fedora-infra/fedora-packages/commit/54edb2426f100c09941d25c1adb0e519d74b9e39>`_
- Py2.6 support for the bugzilla SSL hack. `d823e1671 <https://github.com/fedora-infra/fedora-packages/commit/d823e1671f5d4e6a256f8f6ed93a0927a88f15a9>`_
- Release bump. `dc73e3aed <https://github.com/fedora-infra/fedora-packages/commit/dc73e3aed371ffb8cd135ba271e62366f7ac9ff5>`_
- Fix bug where /packages/qt returned a 404. `ad438ffc9 <https://github.com/fedora-infra/fedora-packages/commit/ad438ffc90ac7c1ff1edc354c9930385beb21ca5>`_
- Fix "python-webob1.2" 404 error. `93abf4389 <https://github.com/fedora-infra/fedora-packages/commit/93abf4389078700f3d320bf4111e8efba8e6dc2b>`_
- Redirect to search instead of /error in case of 404 on package name. `4d9c426c6 <https://github.com/fedora-infra/fedora-packages/commit/4d9c426c6ef2131d675740fe4eb3d0ba85087c2d>`_
- Use a more modern hardcoded url at the bottom of search/index.py. `6c5b19417 <https://github.com/fedora-infra/fedora-packages/commit/6c5b19417e677d40de41122860476ec6f8dc685b>`_
- Release bump. `94c2948b6 <https://github.com/fedora-infra/fedora-packages/commit/94c2948b6081788480914b8c6b2800109ab6dfb4>`_
- Fix a pesky spelling error. `525383f9d <https://github.com/fedora-infra/fedora-packages/commit/525383f9d8ac606f8cd15fff365f7b997baabad7>`_
- Disable fancy-patched dogpile stuff until it is generally available. `c7bc19f25 <https://github.com/fedora-infra/fedora-packages/commit/c7bc19f259619a12bc05a30b7d03aaa0839bd022>`_
- Add dogpile to bootstrap.py. `2d4aea06a <https://github.com/fedora-infra/fedora-packages/commit/2d4aea06a8c6bfa6ab17fe9725b5db1b10e0be5b>`_
- dist-rawhide is gone `4fd257a08 <https://github.com/fedora-infra/fedora-packages/commit/4fd257a08655a5651c86d71ab2c14ea8b1398d58>`_
- Make the dogpile caching optional. `bb18eb7b2 <https://github.com/fedora-infra/fedora-packages/commit/bb18eb7b208cf280bbc44115f48f7dd248f05948>`_
- Simplify dogpile cache interfaces. `c897dbc6d <https://github.com/fedora-infra/fedora-packages/commit/c897dbc6d314d9fc44e9d2843d219961404e03d4>`_
- Use python-retask to distribute cache refreshing to a worker proc. `ae6d8c7d4 <https://github.com/fedora-infra/fedora-packages/commit/ae6d8c7d4ca4e60b6034ce11da3744a71c73c16a>`_
- Tweak to get koji connector working. `8c74c4924 <https://github.com/fedora-infra/fedora-packages/commit/8c74c4924ccb473714461f06889c115653e39639>`_
- Tweak to get yum connector working. `5df0c06e8 <https://github.com/fedora-infra/fedora-packages/commit/5df0c06e8d26ec039aca5278e49dbd000ec56ec6>`_
- Specfile updated with new deps. `eb73d9adb <https://github.com/fedora-infra/fedora-packages/commit/eb73d9adbb7cb67abd84117da7478f3eb3654c85>`_
- Merge pull request #1 from fedora-infra/feature/optional-dogpile `462737762 <https://github.com/fedora-infra/fedora-packages/commit/46273776237a2b4745faef1ea9f7ec902eb55e15>`_
- Merge pull request #2 from fedora-infra/feature/long-running-queue `f31795b4f <https://github.com/fedora-infra/fedora-packages/commit/f31795b4fec041606ed69f2bb7fcfeac800fb664>`_
- Half-working daemon setup. `9fe610e5f <https://github.com/fedora-infra/fedora-packages/commit/9fe610e5fa2a9a18a46246cf5d18a574e4badfce>`_
- Better setup for daemon-hood.  pkgdb and bodhi connectors are still broken. `40ff5c37b <https://github.com/fedora-infra/fedora-packages/commit/40ff5c37b64adb5a17cbe6f38b98f27b1cadb1b7>`_
- Tweaks to try and get the daemon to work.  Nothing significant. `a7d2298e3 <https://github.com/fedora-infra/fedora-packages/commit/a7d2298e3e766e7bb15b2d895e8c1604521d2017>`_
- Merge pull request #3 from fedora-infra/feature/worker-as-a-daemon `d5d997dcc <https://github.com/fedora-infra/fedora-packages/commit/d5d997dcc9ee187634a795582abcb48b5b727eab>`_
- Don't install dogpile from fedora just yet.  What we need hasn't hit updates-testing yet. `9134423dd <https://github.com/fedora-infra/fedora-packages/commit/9134423dd9b0c46ac7239dbf2baf0a838b41ee12>`_
- Use updates-testing.  :P `bfba73852 <https://github.com/fedora-infra/fedora-packages/commit/bfba73852f79976b046f1a83a4369c77fc593af9>`_
- Add a link to Fedora Tagger from the package chrome. `b73c67b58 <https://github.com/fedora-infra/fedora-packages/commit/b73c67b58b4827b8037d929e5d96eb188173a6a9>`_
- Call Thread.start(), not run() `b75d37bd3 <https://github.com/fedora-infra/fedora-packages/commit/b75d37bd30acf82ca84c78f4226b1f61617afae5>`_
- Merge branch 'develop' of github.com:fedora-infra/fedora-packages into develop `b85723329 <https://github.com/fedora-infra/fedora-packages/commit/b857233297b5b9098be73a410578a95b761a9053>`_
- Deth to pyCurl! `cdbe2d4f9 <https://github.com/fedora-infra/fedora-packages/commit/cdbe2d4f969fed88d40a05140d17ca9fcc9b27cb>`_
- Fix the raw patch links `75c0e25c9 <https://github.com/fedora-infra/fedora-packages/commit/75c0e25c9bf50e237223fc7ff5a9eae09561b5f4>`_
- Include init script for fcomm-cache-worker. `1e0287cbf <https://github.com/fedora-infra/fedora-packages/commit/1e0287cbfa9987b140dde70ccd89637242a1cdba>`_
- Merge branch 'develop' of github.com:fedora-infra/fedora-packages into develop `552d537c6 <https://github.com/fedora-infra/fedora-packages/commit/552d537c6d7599fecd3c6874c88fcb2f2bbb0e26>`_
- Fix crazy sigterm bug in the cache worker. `6fbfa731f <https://github.com/fedora-infra/fedora-packages/commit/6fbfa731ffd1a5779b11ec54e2eeb4ddcca5751b>`_
- Config for the cache-worker daemon. `e34f9fbb3 <https://github.com/fedora-infra/fedora-packages/commit/e34f9fbb3880c2a77a921e676d027ddc16c56044>`_
- Merge branch 'feature/kill-pycurl' into release/2.0.5 `1ee2cc643 <https://github.com/fedora-infra/fedora-packages/commit/1ee2cc64394245df8e7865486ebb77457dd6bdc1>`_
- Revert "Deth to pyCurl!" `7de233bfd <https://github.com/fedora-infra/fedora-packages/commit/7de233bfdcac73334a537ee0bb305ef98e076bfe>`_
- 2.0.5 with cache daemon craziness. `4527fe20c <https://github.com/fedora-infra/fedora-packages/commit/4527fe20cdc9f119ecda179c09872d4a12dcd596>`_
- Cleanup. `2ea45de61 <https://github.com/fedora-infra/fedora-packages/commit/2ea45de61e2f05ea0cc27e59e93e767eaa13ae02>`_
- Be yet still more conservative with memcached connections in the cache worker daemon. `155e88a12 <https://github.com/fedora-infra/fedora-packages/commit/155e88a1294b39866dd2ea774922552997ae11e1>`_
- 2.0.6 `15e25f045 <https://github.com/fedora-infra/fedora-packages/commit/15e25f045b1c3e45bb292b9a320abf638a29fb52>`_
- Add in python-memcached dependency to bootstrap.py and setup.py `4c57d59dd <https://github.com/fedora-infra/fedora-packages/commit/4c57d59ddc8692f1240ba1cd72592400a0a91ffa>`_
- Merge pull request #7 from daviddavis/develop `bd932195b <https://github.com/fedora-infra/fedora-packages/commit/bd932195b2cc5fc4d91a62ccdc387ac87fa6ce0b>`_
- Link dogpile into our virtualenv `e7861885b <https://github.com/fedora-infra/fedora-packages/commit/e7861885b741be92ba3fe3a7e4792a539ae071b2>`_
- Link memcache into our virtualenv `a7f078d4c <https://github.com/fedora-infra/fedora-packages/commit/a7f078d4c111f6b2f7a4379840e2290be16ac1cf>`_
- we need memcached too `bcd9df12c <https://github.com/fedora-infra/fedora-packages/commit/bcd9df12cbc290bf79dcb6f6c00f10e09a804305>`_
- Get BodhiConnector.query_active_releases working without a WSGI environ (#11) `46c332599 <https://github.com/fedora-infra/fedora-packages/commit/46c33259991608f572d942b6ad0c6b654cabba0a>`_
- Changes to karma image. Adding colors. `6b109068b <https://github.com/fedora-infra/fedora-packages/commit/6b109068b74c58a4cf33f64828fe2ca836ab99d0>`_
- Merge pull request #15 from marijar/karma `d287c7364 <https://github.com/fedora-infra/fedora-packages/commit/d287c73647a188a7e26323a6944ea2066cb74f40>`_
- Support bugzilla-0.8.0 `60f3d6591 <https://github.com/fedora-infra/fedora-packages/commit/60f3d6591e89e2f525bd6fb94a75b01f86933937>`_
- Update the bugzillahacks.py for 0.8.0 `3c4cc9fb0 <https://github.com/fedora-infra/fedora-packages/commit/3c4cc9fb0e8b6947f8078fb528e0a8737a7c5cb6>`_
- Get off of the old moksha.common.lib.helpers stuff. `a8a8662ba <https://github.com/fedora-infra/fedora-packages/commit/a8a8662baa9ac2e883eb8ee53bfc3953a6e78a52>`_
- Don't escape the spec file widget. `ac00f53e6 <https://github.com/fedora-infra/fedora-packages/commit/ac00f53e67bce662b7095ede200bb8c202a99567>`_
- Fix misleading text in bugs widget. `792511fb6 <https://github.com/fedora-infra/fedora-packages/commit/792511fb6ba802b9019ce43b9ae8955ab619b372>`_
- The latest from updates-testing is no longer necessary for development. `dce25ee02 <https://github.com/fedora-infra/fedora-packages/commit/dce25ee02af8a28999aad44d9ac04221996ba638>`_
- Make the redis queue not connect at import time. `59d3763ba <https://github.com/fedora-infra/fedora-packages/commit/59d3763bad6a75f977222488a8cfe44399cf9601>`_
- Turn off memcached stuff by default for development. `55a94cb71 <https://github.com/fedora-infra/fedora-packages/commit/55a94cb7137c33b06f063a6b4f3e9d8a47c4037e>`_
- Merge pull request #17 from fedora-infra/feature/optional-caching-for-development `1c27cd54a <https://github.com/fedora-infra/fedora-packages/commit/1c27cd54aad4a91d96ac76c233f86b210a526e36>`_
- Merge pull request #18 from fedora-infra/feature/no-updates-testing-plz `fd718d5f6 <https://github.com/fedora-infra/fedora-packages/commit/fd718d5f64ca7084bdde17dc38ce17fff921e6b6>`_
- Merge pull request #19 from fedora-infra/feature/fix-bugs-text `9a9910c78 <https://github.com/fedora-infra/fedora-packages/commit/9a9910c78aa32b65a371ff96b0ea29842f658870>`_
- If bug_version is a string, don't truncate it otherwise return the first element only `58452a8e6 <https://github.com/fedora-infra/fedora-packages/commit/58452a8e6156e5341a932e920f3d77ffe10e4fe3>`_
- Merge pull request #23 from fedora-infra/feature/fix_bugs_release `0f1720f3b <https://github.com/fedora-infra/fedora-packages/commit/0f1720f3bef10c68753cca848c599d45d02f4427>`_
- You've got to be kidding me. `1b008dbf4 <https://github.com/fedora-infra/fedora-packages/commit/1b008dbf422f5e9a6a5d463b25e13ed18774f4a9>`_
- 2.0.7-2 `9a09cfa72 <https://github.com/fedora-infra/fedora-packages/commit/9a09cfa72eafe291c9370507eb0b913a476f71b0>`_
- Modernize distmappings. `175ff35bc <https://github.com/fedora-infra/fedora-packages/commit/175ff35bc387a17e731bc50fc1d9c3280eb5908f>`_
- Unescape JSON so the relationships tab (and other things) work. `74fe187ed <https://github.com/fedora-infra/fedora-packages/commit/74fe187ed216bf569f3328c21d3dff4667ee304a>`_
- Ignore version map from cronjob. `d14c44e62 <https://github.com/fedora-infra/fedora-packages/commit/d14c44e6253f0059eba3a8a35396620e809290e6>`_
- Merge pull request #25 from fedora-infra/feature/unescape-that-json `d58c46816 <https://github.com/fedora-infra/fedora-packages/commit/d58c468162f41f1d2dab0be43038b9c7d45e35b9>`_
- Remove error obfuscation. `99a63bb32 <https://github.com/fedora-infra/fedora-packages/commit/99a63bb32b61aa86392880a5c7a7ce5ba238cc9b>`_
- Move exception handling into call_get_file_tree for consistency. `6aea9bb49 <https://github.com/fedora-infra/fedora-packages/commit/6aea9bb49a6eeceb9b96115f79a7a7786f54919e>`_
- Merge pull request #27 from fedora-infra/feature/remove-obfuscation `232681011 <https://github.com/fedora-infra/fedora-packages/commit/232681011bed6cac820487d8ed5633a9c736c888>`_
- Update hotpatch for bugzilla-0.9.0. `ff3ea739e <https://github.com/fedora-infra/fedora-packages/commit/ff3ea739eaa7a511998b57a5caf4e3ee987ea69a>`_
- Karma_level needs to be double nested here in order to work. `e2c878809 <https://github.com/fedora-infra/fedora-packages/commit/e2c87880991bbc33a12272afce0a1a744a5ace9c>`_
- Sometimes latest_builds itself is None. `bba62f8cc <https://github.com/fedora-infra/fedora-packages/commit/bba62f8cc482958503911df8357509dfe0e3de9c>`_
- Merge pull request #30 from fedora-infra/feature/latest-builds-bugfix `039a34dc3 <https://github.com/fedora-infra/fedora-packages/commit/039a34dc3b7c0cde624dc09fd38ef69804e47918>`_
- Merge branch 'feature/double-nesting-craziness' into develop `092e08951 <https://github.com/fedora-infra/fedora-packages/commit/092e08951627075b583232f395c4fb4f0e799ed7>`_
- Protect version comparison against 2.3.0dev `ad2c47f0a <https://github.com/fedora-infra/fedora-packages/commit/ad2c47f0a2e2ce1eeb0534dc4796451d277e8111>`_
- Really disable those request extensions. `6378a8758 <https://github.com/fedora-infra/fedora-packages/commit/6378a87581ae5cbe6f6689260d94f3a4abfb1166>`_
- 2.0.8 `f198fb0e9 <https://github.com/fedora-infra/fedora-packages/commit/f198fb0e9f0bc4229c25e6a350a645eed0633896>`_
- Import old code from python-moksha-wsgi-1.2.0. `ed1e07d71 <https://github.com/fedora-infra/fedora-packages/commit/ed1e07d710da22bfa1ffa38e70506e617694c85b>`_
- 2.0.9 `42e81154b <https://github.com/fedora-infra/fedora-packages/commit/42e81154b316f32cf87b74752ada2eaaa66f2f9d>`_
- make the bz cookiefile location configurable. `b90adc962 <https://github.com/fedora-infra/fedora-packages/commit/b90adc96215c38e152fdffe20aa0f0eeef6a6434>`_
- Merge pull request #32 from fedora-infra/feature/configurable-bz-cookiefile `3081e1f27 <https://github.com/fedora-infra/fedora-packages/commit/3081e1f2704554531bb51fb98a8debd9d3f23027>`_
- 2.0.10 `37861bde8 <https://github.com/fedora-infra/fedora-packages/commit/37861bde8f64073517752bcb2421fb2b5734ed28>`_
- Add a link to Fedora's cgit from the package chrome. `e9c50bf76 <https://github.com/fedora-infra/fedora-packages/commit/e9c50bf76dcb5822286cf269a6416511c5071306>`_
- Resize all images in the "In Other Apps" bar to 16x16 (as suggested by Ralph Bean). `3ede52c37 <https://github.com/fedora-infra/fedora-packages/commit/3ede52c37577025733e8e900fa0c1681397bbd38>`_
- Merge pull request #33 from tjanez/add_cgit_link `3a3d8f4de <https://github.com/fedora-infra/fedora-packages/commit/3a3d8f4de221a542456a70fbb5d3556b2a2fd8cc>`_
- Correct the woefully incorrect distmappings table. `d5e9113fb <https://github.com/fedora-infra/fedora-packages/commit/d5e9113fbbf03fa5fadb7014d0460c02052ecbf8>`_
- Fedora 17 is EOL.  Long live Fedora 20! `bcc20abbe <https://github.com/fedora-infra/fedora-packages/commit/bcc20abbe00227ce07c21af3bf7b46da6f9588f7>`_
- Update the footer with the link to file a ticket. `5fd837b96 <https://github.com/fedora-infra/fedora-packages/commit/5fd837b96d3026defb4aee5716609e876f6ecbe4>`_
- Merge pull request #34 from fedora-infra/feature/more-distmappings-fixes `3b76b3121 <https://github.com/fedora-infra/fedora-packages/commit/3b76b3121a0d99d27d10fa8b93a5cc6b6364da70>`_
- Merge pull request #36 from fedora-infra/feature/ticket-link `81d6202a5 <https://github.com/fedora-infra/fedora-packages/commit/81d6202a58cffb562be9cd40b0dcdf14a45ae710>`_
- Add a space to the response from the bodhi connector. `4a9302454 <https://github.com/fedora-infra/fedora-packages/commit/4a9302454d133e708cfddf70e61683a79bb19dce>`_
- Try to future-proof against future pylons-less tg. `5e592550e <https://github.com/fedora-infra/fedora-packages/commit/5e592550e15a5fa2cff0fc4341df9865cd1a0c9f>`_
- Merge pull request #46 from fedora-infra/feature/added-space `3366cef0a <https://github.com/fedora-infra/fedora-packages/commit/3366cef0a3c5d91db51910d436314091d9a0f541>`_
- Merge pull request #47 from fedora-infra/feature/pylons-import `2d252fefc <https://github.com/fedora-infra/fedora-packages/commit/2d252fefc8b47099350eef3c32ac600d8bf52e86>`_
- Include epel bugs in the bugs list.  Fixes #6. `78761e26b <https://github.com/fedora-infra/fedora-packages/commit/78761e26bd8cc592f642333d47be89e167efffdc>`_
- PEP8: ez_setup/__init__.py and remove import unused shutil `082537430 <https://github.com/fedora-infra/fedora-packages/commit/0825374307404b8f0289eb2a0eb4cd74e55ec91d>`_
- Fix string in the version setuptools `68b758cb4 <https://github.com/fedora-infra/fedora-packages/commit/68b758cb49acfada04fe215fb70d9cdb44114d11>`_
- PEP8: config package `62e65f7d0 <https://github.com/fedora-infra/fedora-packages/commit/62e65f7d0780eac2263cd72e60924abcd3ebc089>`_
- PEP8: fedoracommunity/connector/api package and refactoring code. `fd93b30ef <https://github.com/fedora-infra/fedora-packages/commit/fd93b30efbd4b973787997d39e8ec23e915c120a>`_
- Change in widgets package and bodhiconnector.py `371c1c28d <https://github.com/fedora-infra/fedora-packages/commit/371c1c28df989d55371a902ccd8675bde681be92>`_
- PEP8: bugzillaconnector.py `90d76ad60 <https://github.com/fedora-infra/fedora-packages/commit/90d76ad60fd83854ea4d54bae9efa362a9a4d76f>`_
- PEP8: fasconnector.py `35d991791 <https://github.com/fedora-infra/fedora-packages/commit/35d991791c3297e064d7ed135b3f529a3bcfdc8b>`_
- PEP8: websetup.py `6f32d2671 <https://github.com/fedora-infra/fedora-packages/commit/6f32d267134a613cce121effa995ab398191b7bc>`_
- PEP8: stats.py `3fe651b2c <https://github.com/fedora-infra/fedora-packages/commit/3fe651b2c1cf1e44484f14a50403681f963ae437>`_
- PEP8: distmappings.py `cc86c989c <https://github.com/fedora-infra/fedora-packages/commit/cc86c989cdf9b8301686d4fc2da8654d47454967>`_
- Change in faswhoplugin.py `9d6c28861 <https://github.com/fedora-infra/fedora-packages/commit/9d6c288618646e97e25c5a8d8f786d4ffc9b0f08>`_
- Changes in gitconnector.py `0613eef3a <https://github.com/fedora-infra/fedora-packages/commit/0613eef3af66da4c5446f46838bbdeec1159b44e>`_
- Changes in jsonconnector.py `8bc5549e9 <https://github.com/fedora-infra/fedora-packages/commit/8bc5549e9f965e1d0f756abf78b371f843052462>`_
- Changes in kojiconnector.py `a26a2f51b <https://github.com/fedora-infra/fedora-packages/commit/a26a2f51b515a64f133ea51e9d6877c21eb02ac5>`_
- Merge pull request #50 from echevemaster/develop `cc5c1e720 <https://github.com/fedora-infra/fedora-packages/commit/cc5c1e720b249eac34e0e8d02b077638ef9f181f>`_
- Merge pull request #49 from yograterol/develop `a63744ca5 <https://github.com/fedora-infra/fedora-packages/commit/a63744ca502f84f494be97ad65a57b3526971cd8>`_
- Merge pull request #48 from fedora-infra/feature/epel-bugs `b806c9c3b <https://github.com/fedora-infra/fedora-packages/commit/b806c9c3bfa9c397e95994985dd3ebbea5051472>`_
- Provide a way for the koji builds indexer to initialize itself. `247fc1004 <https://github.com/fedora-infra/fedora-packages/commit/247fc10041e36597fa67b387049bf922bf641e4f>`_
- Merge pull request #51 from fedora-infra/feature/builds-action `c639ade7f <https://github.com/fedora-infra/fedora-packages/commit/c639ade7fea23f1aad7016a9c03b2dd864300eca>`_
- Get fedora-packages working again against modern TG2+crank. `57ed33fd7 <https://github.com/fedora-infra/fedora-packages/commit/57ed33fd7b742fbde311d3ac3110463a1404dd4e>`_
- Remove widgets that we don't actually use but which have a dep on broken repoze.who/what `3b655a931 <https://github.com/fedora-infra/fedora-packages/commit/3b655a9314bea55fa88bf453abf22645868a865a>`_
- Forgot to rm this template too. `c71c7cbeb <https://github.com/fedora-infra/fedora-packages/commit/c71c7cbeba9f1192ac8e177c33e9f368f5315150>`_
- Merge pull request #52 from fedora-infra/feature/remove-repoze `a1553bd2d <https://github.com/fedora-infra/fedora-packages/commit/a1553bd2d886b793e3d9264f9bb8584ab9efa8bf>`_
- Quote up the search term to make it url safe. `dd46b8592 <https://github.com/fedora-infra/fedora-packages/commit/dd46b85929419996716e046543a65851f78d9266>`_
- Doubly encode search term to allow slashes input by various means. `c61781cc4 <https://github.com/fedora-infra/fedora-packages/commit/c61781cc4bf547cced37abf7137e1be40261fb93>`_
- Remove a space. `197d12afc <https://github.com/fedora-infra/fedora-packages/commit/197d12afcb157bcce3b98006609f40c7f91e09a3>`_
- The last piece to get searches with slashes working. `ea1a906c9 <https://github.com/fedora-infra/fedora-packages/commit/ea1a906c99932c9c7b83529cf82638851391fc3a>`_
- Merge pull request #53 from fedora-infra/feature/search-with-slash `50e8e27c2 <https://github.com/fedora-infra/fedora-packages/commit/50e8e27c26b43771e7ab37cb2dd08ba7b85274e1>`_
- 2.0.11 `f4cb9ca09 <https://github.com/fedora-infra/fedora-packages/commit/f4cb9ca09d0f160e8e3b1547249fb27646ed3db9>`_
- Fix regression introduced in 62e65f7d0780eac2263cd72e60924abcd3ebc089. `67632cadd <https://github.com/fedora-infra/fedora-packages/commit/67632cadd3c5b1d3c58d73a3ac564164c2ce6806>`_
- Merge pull request #54 from fedora-infra/feature/fix-config-regression `a0704a72c <https://github.com/fedora-infra/fedora-packages/commit/a0704a72ce729eeea855e9661ad2bbb3d2c6a308>`_
- 2.0.12 `bb800cf09 <https://github.com/fedora-infra/fedora-packages/commit/bb800cf0982d62925566360f20f9fa9dfc0d36f2>`_
- added message cards link at search results `e3afe3378 <https://github.com/fedora-infra/fedora-packages/commit/e3afe33781e267dc586c6e3eb08c35a049d8dfd5>`_
- Fix "File a ticket" link `d40400cd8 <https://github.com/fedora-infra/fedora-packages/commit/d40400cd8314055a4b5bbe4771432e6966bef301>`_
- Merge pull request #57 from nanonyme/patch-1 `4a3a1cad8 <https://github.com/fedora-infra/fedora-packages/commit/4a3a1cad89663392a549be36af80eb1240731196>`_
- removed hardcoded message cards link `9c2947c90 <https://github.com/fedora-infra/fedora-packages/commit/9c2947c905f6ae3edd0b0e13bdb84ebd73e04c55>`_
- added definition for message card's link `5e1485110 <https://github.com/fedora-infra/fedora-packages/commit/5e1485110b158575200c80a42e30abe9ed76c8a1>`_
- added template to render message card's link `3a9801467 <https://github.com/fedora-infra/fedora-packages/commit/3a9801467c9cb89a61a8043090c8f11751572985>`_
- added new line at the end of file `26d2a43f5 <https://github.com/fedora-infra/fedora-packages/commit/26d2a43f59ea693222620c17495f8d39adaabac3>`_
- added a function to get datagrepper url and package name `ef3d9221d <https://github.com/fedora-infra/fedora-packages/commit/ef3d9221dbdc08be937ee28d2b4839417d76d73b>`_
- added datagrepper base url i.e. http://localhost:5000 `66f5b48d5 <https://github.com/fedora-infra/fedora-packages/commit/66f5b48d5e9fdf52a1e648ba480f3bfe4bd438ac>`_
- render message cards url `6c049f267 <https://github.com/fedora-infra/fedora-packages/commit/6c049f2670e1faf18eb04172b105c7e05580c709>`_
- changed datagrepper_url `ea853310a <https://github.com/fedora-infra/fedora-packages/commit/ea853310ac8d016b130e349a3e05e187f6349d8c>`_
- render message cards `25cc90073 <https://github.com/fedora-infra/fedora-packages/commit/25cc900734d217b39d925d437fd4f8dd895af0ab>`_
- added function to retrieve message cards from datagrepper `9bd8f757d <https://github.com/fedora-infra/fedora-packages/commit/9bd8f757d1aa10a8a65fc28596568328bd02ee39>`_
- added chrome as parameters `ff4f7644c <https://github.com/fedora-infra/fedora-packages/commit/ff4f7644cf21fbc6738872ccad8790a8cca9e906>`_
- adding css for history cards `b0304f1ed <https://github.com/fedora-infra/fedora-packages/commit/b0304f1ed01191aee6ea70e2d143edd12fd199fb>`_
- added definition for .details-history class to shift link to the right `f3f2f2def <https://github.com/fedora-infra/fedora-packages/commit/f3f2f2defafa784a1818344702b9f9e95b0c2e14>`_
- added css for history-cards and message-card classes `d3e5037fe <https://github.com/fedora-infra/fedora-packages/commit/d3e5037feaee00f969eac7ff2679cc44f04acd7f>`_
- added new line at the end of file `8eeec6aed <https://github.com/fedora-infra/fedora-packages/commit/8eeec6aed070ba713cc0b30476caa6613f6082cb>`_
- Merge pull request #56 from charulagrl/develop `b894a035c <https://github.com/fedora-infra/fedora-packages/commit/b894a035c1ed71564c9636b0d9e2880a0392058e>`_
- Use a blocking call to retask to improve cache worker performance.  Fixes #59. `4936da666 <https://github.com/fedora-infra/fedora-packages/commit/4936da666de46843e8bab3d06df9963108230035>`_
- Merge pull request #60 from fedora-infra/feature/async-worker `5f37d4fc4 <https://github.com/fedora-infra/fedora-packages/commit/5f37d4fc4e4063372419c7c9453822882e3a6a1c>`_
- Fix a syntax error in the latest builds indexer `72e6f8631 <https://github.com/fedora-infra/fedora-packages/commit/72e6f8631b2da5059e7945bad900e7ffade22b55>`_
- Update distmappings `6e288e276 <https://github.com/fedora-infra/fedora-packages/commit/6e288e276280b2f3a58ffd49d1f1aac3641f9600>`_
- Needed this to develop locally... `3733ce7e9 <https://github.com/fedora-infra/fedora-packages/commit/3733ce7e98906d2a873a0b9592982fa35c8225c4>`_
- Typeahead! `a954bf3c3 <https://github.com/fedora-infra/fedora-packages/commit/a954bf3c3ac4ea0faf51d24979c9ae9f90e1d17a>`_
- fix width `82172db1c <https://github.com/fedora-infra/fedora-packages/commit/82172db1c5a7c307bd3ccf7eb558d7ebdd9011d8>`_
- Move the history block down one. `a8055f2fb <https://github.com/fedora-infra/fedora-packages/commit/a8055f2fb0380b6ea52d53684787fb464cfb907e>`_
- 2.0.13 `56c5c1d77 <https://github.com/fedora-infra/fedora-packages/commit/56c5c1d7741edc5d8171cc9a93b49bf963c25b99>`_
- Spec bump. `b32fe1ce0 <https://github.com/fedora-infra/fedora-packages/commit/b32fe1ce06ca717024b45dbd06107c326b450ced>`_
- Merge pull request #62 from fedora-infra/typeahead `b79814cd4 <https://github.com/fedora-infra/fedora-packages/commit/b79814cd48e49e8e0fdca0749f5d908e44033a99>`_
- added css for datetime `b444faf6a <https://github.com/fedora-infra/fedora-packages/commit/b444faf6a77caa262e482776c76aec8953264e89>`_
- Merge pull request #63 from charulagrl/develop `9dc9c2ec9 <https://github.com/fedora-infra/fedora-packages/commit/9dc9c2ec9049597ef30dbcb79d23a99b2d09f64f>`_
- Avoid crashing if datagrepper is not available. `924de7f09 <https://github.com/fedora-infra/fedora-packages/commit/924de7f092e37edcbc68dc915afde4738bde18e9>`_
- Avoid defaulting to armv7hl on relationships tabs. `93960cd67 <https://github.com/fedora-infra/fedora-packages/commit/93960cd675226c9e8f43062f6eef1c898e6552c2>`_
- Merge pull request #65 from fedora-infra/feature/default-x86 `7a2864473 <https://github.com/fedora-infra/fedora-packages/commit/7a2864473ad878fb03dc2c707777dc1e56ebc509>`_
- Merge pull request #64 from fedora-infra/feature/safe-datagrepper `49423d0a9 <https://github.com/fedora-infra/fedora-packages/commit/49423d0a93476fc6938bac1cd69e3760e9024d3f>`_
- Reorganize the params argument for style. `eaec03b67 <https://github.com/fedora-infra/fedora-packages/commit/eaec03b67d0730665c1d38bf58ff86e65fd53226>`_
- Add exclusive arguments to the datagrepper query. `18b80ba0c <https://github.com/fedora-infra/fedora-packages/commit/18b80ba0c90d9de1140bff0503ad98573d56b619>`_
- Merge pull request #67 from fedora-infra/feature/exclude-datagrepper-spam `b9bdc647f <https://github.com/fedora-infra/fedora-packages/commit/b9bdc647f5a4e799ffa0881d82426c32406383d2>`_
- Make datagrepper icons square. `a0bcfa41c <https://github.com/fedora-infra/fedora-packages/commit/a0bcfa41c52f3513e7bf6346f7b143f081d20e28>`_
- Merge pull request #69 from fedora-infra/feature/square-icons `18f4a808e <https://github.com/fedora-infra/fedora-packages/commit/18f4a808e18cb4a35bdb5f717d9127da69a93399>`_
- Use a lockfile for yum stuff. `45ca0f52b <https://github.com/fedora-infra/fedora-packages/commit/45ca0f52b2f50d27ca782d3095227c85b2bde864>`_
- Merge pull request #70 from fedora-infra/feature/yumlock `3e3d91213 <https://github.com/fedora-infra/fedora-packages/commit/3e3d91213814cf9cb3c351cc9c7299cb4ce599d9>`_
- 2.0.14 `97a5496d7 <https://github.com/fedora-infra/fedora-packages/commit/97a5496d7e1f538f852e1369605f1f5ecc9e1e38>`_
- Bump spec. `61577ecfb <https://github.com/fedora-infra/fedora-packages/commit/61577ecfb86934d6377e08ca072ec19162e4aead>`_
- Defer yumlock creation until runtime. `1f354589b <https://github.com/fedora-infra/fedora-packages/commit/1f354589ba153a67eb344557b81b654059201894>`_
- Quick release. `3ba73f9d9 <https://github.com/fedora-infra/fedora-packages/commit/3ba73f9d9000ff8c25076fad475fec39d8e5c772>`_
- Merge pull request #73 from fedora-infra/feature/adjusted-yumlock `15b74ecf7 <https://github.com/fedora-infra/fedora-packages/commit/15b74ecf7d2bca110ab10b9e7ecda6285656e3e9>`_
- Log exceptions. `5aee21231 <https://github.com/fedora-infra/fedora-packages/commit/5aee212312ef870632e80cb157a2887c21cfece5>`_
- Merge pull request #74 from fedora-infra/feature/log-exceptions-plz `5d2940c78 <https://github.com/fedora-infra/fedora-packages/commit/5d2940c78e51cd6b577b6df76e2d1c2a6436c53e>`_
- Try to be smarter with our locking. `3213aa794 <https://github.com/fedora-infra/fedora-packages/commit/3213aa7941bbccb1e62e5d9791b95e04a86b75d2>`_
- Remove the locking stuff. `d5ca72b13 <https://github.com/fedora-infra/fedora-packages/commit/d5ca72b133d09ed861f4746ed6f8ed7bdecd2ed2>`_
- Merge pull request #75 from fedora-infra/feature/roll-that-locking-stuff-back `6c85d3a53 <https://github.com/fedora-infra/fedora-packages/commit/6c85d3a53271e543dde641611bd75e0f011ea066>`_
- 2.0.15 `17a8905ff <https://github.com/fedora-infra/fedora-packages/commit/17a8905ff85bd56a115421f3a1ad640888c9a900>`_
- A blossom of hatred. `9f00d1bf8 <https://github.com/fedora-infra/fedora-packages/commit/9f00d1bf84aa152863d370c1a1edef5c347335de>`_
- Add a configurable timestamp to this tool. `ce7efe680 <https://github.com/fedora-infra/fedora-packages/commit/ce7efe680dd536d36f0e9594350c67b9aad084d9>`_
- Merge pull request #78 from fedora-infra/feature/configurable-timestamp `b8901cfb8 <https://github.com/fedora-infra/fedora-packages/commit/b8901cfb871479b4f872f9fccb096eff3d548a58>`_
- Remove the relationships tab from the UI. `a9893b61d <https://github.com/fedora-infra/fedora-packages/commit/a9893b61d9fbac3c726a7dd048b05063b8c4f067>`_
- Merge pull request #84 from fedora-infra/feature/all-good-things `1506dc97e <https://github.com/fedora-infra/fedora-packages/commit/1506dc97efb1018970c617ab67cac639d627f2c0>`_
- :fire: Do the pkgdb2 thing :fire: `732be9a8a <https://github.com/fedora-infra/fedora-packages/commit/732be9a8aedaf7721da569f5b52d6abc149ea5b1>`_
- Also, require this lib. `12da36cbd <https://github.com/fedora-infra/fedora-packages/commit/12da36cbdb0978a5b74a5d4112dc6c8d4dece99f>`_
- Switch to pkgdb2 api in the indexer. `a06c97e0d <https://github.com/fedora-infra/fedora-packages/commit/a06c97e0d23c6324875e1d8464490a686b80614f>`_
- Merge pull request #85 from fedora-infra/feature/pkgdb2 `b301a677a <https://github.com/fedora-infra/fedora-packages/commit/b301a677ad1d7dca1bc4745dc46167cb58a4fb54>`_
- gitbranchname -> branchname. `3f659e20b <https://github.com/fedora-infra/fedora-packages/commit/3f659e20bd5b960c5d775bef49fb47adf6227279>`_

2.0.16
------

- A blossom of hatred. `9f00d1bf8 <https://github.com/fedora-infra/fedora-packages/commit/9f00d1bf84aa152863d370c1a1edef5c347335de>`_
- Add a configurable timestamp to this tool. `ce7efe680 <https://github.com/fedora-infra/fedora-packages/commit/ce7efe680dd536d36f0e9594350c67b9aad084d9>`_
- Merge pull request #78 from fedora-infra/feature/configurable-timestamp `b8901cfb8 <https://github.com/fedora-infra/fedora-packages/commit/b8901cfb871479b4f872f9fccb096eff3d548a58>`_
- Remove the relationships tab from the UI. `a9893b61d <https://github.com/fedora-infra/fedora-packages/commit/a9893b61d9fbac3c726a7dd048b05063b8c4f067>`_
- Merge pull request #84 from fedora-infra/feature/all-good-things `1506dc97e <https://github.com/fedora-infra/fedora-packages/commit/1506dc97efb1018970c617ab67cac639d627f2c0>`_
- :fire: Do the pkgdb2 thing :fire: `732be9a8a <https://github.com/fedora-infra/fedora-packages/commit/732be9a8aedaf7721da569f5b52d6abc149ea5b1>`_
- Also, require this lib. `12da36cbd <https://github.com/fedora-infra/fedora-packages/commit/12da36cbdb0978a5b74a5d4112dc6c8d4dece99f>`_
- Switch to pkgdb2 api in the indexer. `a06c97e0d <https://github.com/fedora-infra/fedora-packages/commit/a06c97e0d23c6324875e1d8464490a686b80614f>`_
- Merge pull request #85 from fedora-infra/feature/pkgdb2 `b301a677a <https://github.com/fedora-infra/fedora-packages/commit/b301a677ad1d7dca1bc4745dc46167cb58a4fb54>`_
- gitbranchname -> branchname. `3f659e20b <https://github.com/fedora-infra/fedora-packages/commit/3f659e20bd5b960c5d775bef49fb47adf6227279>`_

2.0.15
------

- Bump spec. `61577ecfb <https://github.com/fedora-infra/fedora-packages/commit/61577ecfb86934d6377e08ca072ec19162e4aead>`_
- Defer yumlock creation until runtime. `1f354589b <https://github.com/fedora-infra/fedora-packages/commit/1f354589ba153a67eb344557b81b654059201894>`_
- Quick release. `3ba73f9d9 <https://github.com/fedora-infra/fedora-packages/commit/3ba73f9d9000ff8c25076fad475fec39d8e5c772>`_
- Merge pull request #73 from fedora-infra/feature/adjusted-yumlock `15b74ecf7 <https://github.com/fedora-infra/fedora-packages/commit/15b74ecf7d2bca110ab10b9e7ecda6285656e3e9>`_
- Log exceptions. `5aee21231 <https://github.com/fedora-infra/fedora-packages/commit/5aee212312ef870632e80cb157a2887c21cfece5>`_
- Merge pull request #74 from fedora-infra/feature/log-exceptions-plz `5d2940c78 <https://github.com/fedora-infra/fedora-packages/commit/5d2940c78e51cd6b577b6df76e2d1c2a6436c53e>`_
- Try to be smarter with our locking. `3213aa794 <https://github.com/fedora-infra/fedora-packages/commit/3213aa7941bbccb1e62e5d9791b95e04a86b75d2>`_
- Remove the locking stuff. `d5ca72b13 <https://github.com/fedora-infra/fedora-packages/commit/d5ca72b133d09ed861f4746ed6f8ed7bdecd2ed2>`_
- Merge pull request #75 from fedora-infra/feature/roll-that-locking-stuff-back `6c85d3a53 <https://github.com/fedora-infra/fedora-packages/commit/6c85d3a53271e543dde641611bd75e0f011ea066>`_

2.0.14
------

- Needed this to develop locally... `3733ce7e9 <https://github.com/fedora-infra/fedora-packages/commit/3733ce7e98906d2a873a0b9592982fa35c8225c4>`_
- Typeahead! `a954bf3c3 <https://github.com/fedora-infra/fedora-packages/commit/a954bf3c3ac4ea0faf51d24979c9ae9f90e1d17a>`_
- fix width `82172db1c <https://github.com/fedora-infra/fedora-packages/commit/82172db1c5a7c307bd3ccf7eb558d7ebdd9011d8>`_
- Spec bump. `b32fe1ce0 <https://github.com/fedora-infra/fedora-packages/commit/b32fe1ce06ca717024b45dbd06107c326b450ced>`_
- Merge pull request #62 from fedora-infra/typeahead `b79814cd4 <https://github.com/fedora-infra/fedora-packages/commit/b79814cd48e49e8e0fdca0749f5d908e44033a99>`_
- added css for datetime `b444faf6a <https://github.com/fedora-infra/fedora-packages/commit/b444faf6a77caa262e482776c76aec8953264e89>`_
- Merge pull request #63 from charulagrl/develop `9dc9c2ec9 <https://github.com/fedora-infra/fedora-packages/commit/9dc9c2ec9049597ef30dbcb79d23a99b2d09f64f>`_
- Avoid crashing if datagrepper is not available. `924de7f09 <https://github.com/fedora-infra/fedora-packages/commit/924de7f092e37edcbc68dc915afde4738bde18e9>`_
- Avoid defaulting to armv7hl on relationships tabs. `93960cd67 <https://github.com/fedora-infra/fedora-packages/commit/93960cd675226c9e8f43062f6eef1c898e6552c2>`_
- Merge pull request #65 from fedora-infra/feature/default-x86 `7a2864473 <https://github.com/fedora-infra/fedora-packages/commit/7a2864473ad878fb03dc2c707777dc1e56ebc509>`_
- Merge pull request #64 from fedora-infra/feature/safe-datagrepper `49423d0a9 <https://github.com/fedora-infra/fedora-packages/commit/49423d0a93476fc6938bac1cd69e3760e9024d3f>`_
- Reorganize the params argument for style. `eaec03b67 <https://github.com/fedora-infra/fedora-packages/commit/eaec03b67d0730665c1d38bf58ff86e65fd53226>`_
- Add exclusive arguments to the datagrepper query. `18b80ba0c <https://github.com/fedora-infra/fedora-packages/commit/18b80ba0c90d9de1140bff0503ad98573d56b619>`_
- Merge pull request #67 from fedora-infra/feature/exclude-datagrepper-spam `b9bdc647f <https://github.com/fedora-infra/fedora-packages/commit/b9bdc647f5a4e799ffa0881d82426c32406383d2>`_
- Make datagrepper icons square. `a0bcfa41c <https://github.com/fedora-infra/fedora-packages/commit/a0bcfa41c52f3513e7bf6346f7b143f081d20e28>`_
- Merge pull request #69 from fedora-infra/feature/square-icons `18f4a808e <https://github.com/fedora-infra/fedora-packages/commit/18f4a808e18cb4a35bdb5f717d9127da69a93399>`_
- Use a lockfile for yum stuff. `45ca0f52b <https://github.com/fedora-infra/fedora-packages/commit/45ca0f52b2f50d27ca782d3095227c85b2bde864>`_
- Merge pull request #70 from fedora-infra/feature/yumlock `3e3d91213 <https://github.com/fedora-infra/fedora-packages/commit/3e3d91213814cf9cb3c351cc9c7299cb4ce599d9>`_

2.0.13
------

- added message cards link at search results `e3afe3378 <https://github.com/fedora-infra/fedora-packages/commit/e3afe33781e267dc586c6e3eb08c35a049d8dfd5>`_
- Fix "File a ticket" link `d40400cd8 <https://github.com/fedora-infra/fedora-packages/commit/d40400cd8314055a4b5bbe4771432e6966bef301>`_
- Merge pull request #57 from nanonyme/patch-1 `4a3a1cad8 <https://github.com/fedora-infra/fedora-packages/commit/4a3a1cad89663392a549be36af80eb1240731196>`_
- removed hardcoded message cards link `9c2947c90 <https://github.com/fedora-infra/fedora-packages/commit/9c2947c905f6ae3edd0b0e13bdb84ebd73e04c55>`_
- added definition for message card's link `5e1485110 <https://github.com/fedora-infra/fedora-packages/commit/5e1485110b158575200c80a42e30abe9ed76c8a1>`_
- added template to render message card's link `3a9801467 <https://github.com/fedora-infra/fedora-packages/commit/3a9801467c9cb89a61a8043090c8f11751572985>`_
- added new line at the end of file `26d2a43f5 <https://github.com/fedora-infra/fedora-packages/commit/26d2a43f59ea693222620c17495f8d39adaabac3>`_
- added a function to get datagrepper url and package name `ef3d9221d <https://github.com/fedora-infra/fedora-packages/commit/ef3d9221dbdc08be937ee28d2b4839417d76d73b>`_
- added datagrepper base url i.e. http://localhost:5000 `66f5b48d5 <https://github.com/fedora-infra/fedora-packages/commit/66f5b48d5e9fdf52a1e648ba480f3bfe4bd438ac>`_
- render message cards url `6c049f267 <https://github.com/fedora-infra/fedora-packages/commit/6c049f2670e1faf18eb04172b105c7e05580c709>`_
- changed datagrepper_url `ea853310a <https://github.com/fedora-infra/fedora-packages/commit/ea853310ac8d016b130e349a3e05e187f6349d8c>`_
- render message cards `25cc90073 <https://github.com/fedora-infra/fedora-packages/commit/25cc900734d217b39d925d437fd4f8dd895af0ab>`_
- added function to retrieve message cards from datagrepper `9bd8f757d <https://github.com/fedora-infra/fedora-packages/commit/9bd8f757d1aa10a8a65fc28596568328bd02ee39>`_
- added chrome as parameters `ff4f7644c <https://github.com/fedora-infra/fedora-packages/commit/ff4f7644cf21fbc6738872ccad8790a8cca9e906>`_
- adding css for history cards `b0304f1ed <https://github.com/fedora-infra/fedora-packages/commit/b0304f1ed01191aee6ea70e2d143edd12fd199fb>`_
- added definition for .details-history class to shift link to the right `f3f2f2def <https://github.com/fedora-infra/fedora-packages/commit/f3f2f2defafa784a1818344702b9f9e95b0c2e14>`_
- added css for history-cards and message-card classes `d3e5037fe <https://github.com/fedora-infra/fedora-packages/commit/d3e5037feaee00f969eac7ff2679cc44f04acd7f>`_
- added new line at the end of file `8eeec6aed <https://github.com/fedora-infra/fedora-packages/commit/8eeec6aed070ba713cc0b30476caa6613f6082cb>`_
- Merge pull request #56 from charulagrl/develop `b894a035c <https://github.com/fedora-infra/fedora-packages/commit/b894a035c1ed71564c9636b0d9e2880a0392058e>`_
- Use a blocking call to retask to improve cache worker performance.  Fixes #59. `4936da666 <https://github.com/fedora-infra/fedora-packages/commit/4936da666de46843e8bab3d06df9963108230035>`_
- Merge pull request #60 from fedora-infra/feature/async-worker `5f37d4fc4 <https://github.com/fedora-infra/fedora-packages/commit/5f37d4fc4e4063372419c7c9453822882e3a6a1c>`_
- Fix a syntax error in the latest builds indexer `72e6f8631 <https://github.com/fedora-infra/fedora-packages/commit/72e6f8631b2da5059e7945bad900e7ffade22b55>`_
- Update distmappings `6e288e276 <https://github.com/fedora-infra/fedora-packages/commit/6e288e276280b2f3a58ffd49d1f1aac3641f9600>`_
- Move the history block down one. `a8055f2fb <https://github.com/fedora-infra/fedora-packages/commit/a8055f2fb0380b6ea52d53684787fb464cfb907e>`_

2.0.12
------

- Fix regression introduced in 62e65f7d0780eac2263cd72e60924abcd3ebc089. `67632cadd <https://github.com/fedora-infra/fedora-packages/commit/67632cadd3c5b1d3c58d73a3ac564164c2ce6806>`_
- Merge pull request #54 from fedora-infra/feature/fix-config-regression `a0704a72c <https://github.com/fedora-infra/fedora-packages/commit/a0704a72ce729eeea855e9661ad2bbb3d2c6a308>`_

2.0.11
------

- Add a link to Fedora's cgit from the package chrome. `e9c50bf76 <https://github.com/fedora-infra/fedora-packages/commit/e9c50bf76dcb5822286cf269a6416511c5071306>`_
- Resize all images in the "In Other Apps" bar to 16x16 (as suggested by Ralph Bean). `3ede52c37 <https://github.com/fedora-infra/fedora-packages/commit/3ede52c37577025733e8e900fa0c1681397bbd38>`_
- Merge pull request #33 from tjanez/add_cgit_link `3a3d8f4de <https://github.com/fedora-infra/fedora-packages/commit/3a3d8f4de221a542456a70fbb5d3556b2a2fd8cc>`_
- Correct the woefully incorrect distmappings table. `d5e9113fb <https://github.com/fedora-infra/fedora-packages/commit/d5e9113fbbf03fa5fadb7014d0460c02052ecbf8>`_
- Fedora 17 is EOL.  Long live Fedora 20! `bcc20abbe <https://github.com/fedora-infra/fedora-packages/commit/bcc20abbe00227ce07c21af3bf7b46da6f9588f7>`_
- Update the footer with the link to file a ticket. `5fd837b96 <https://github.com/fedora-infra/fedora-packages/commit/5fd837b96d3026defb4aee5716609e876f6ecbe4>`_
- Merge pull request #34 from fedora-infra/feature/more-distmappings-fixes `3b76b3121 <https://github.com/fedora-infra/fedora-packages/commit/3b76b3121a0d99d27d10fa8b93a5cc6b6364da70>`_
- Merge pull request #36 from fedora-infra/feature/ticket-link `81d6202a5 <https://github.com/fedora-infra/fedora-packages/commit/81d6202a58cffb562be9cd40b0dcdf14a45ae710>`_
- Add a space to the response from the bodhi connector. `4a9302454 <https://github.com/fedora-infra/fedora-packages/commit/4a9302454d133e708cfddf70e61683a79bb19dce>`_
- Try to future-proof against future pylons-less tg. `5e592550e <https://github.com/fedora-infra/fedora-packages/commit/5e592550e15a5fa2cff0fc4341df9865cd1a0c9f>`_
- Merge pull request #46 from fedora-infra/feature/added-space `3366cef0a <https://github.com/fedora-infra/fedora-packages/commit/3366cef0a3c5d91db51910d436314091d9a0f541>`_
- Merge pull request #47 from fedora-infra/feature/pylons-import `2d252fefc <https://github.com/fedora-infra/fedora-packages/commit/2d252fefc8b47099350eef3c32ac600d8bf52e86>`_
- Include epel bugs in the bugs list.  Fixes #6. `78761e26b <https://github.com/fedora-infra/fedora-packages/commit/78761e26bd8cc592f642333d47be89e167efffdc>`_
- PEP8: ez_setup/__init__.py and remove import unused shutil `082537430 <https://github.com/fedora-infra/fedora-packages/commit/0825374307404b8f0289eb2a0eb4cd74e55ec91d>`_
- Fix string in the version setuptools `68b758cb4 <https://github.com/fedora-infra/fedora-packages/commit/68b758cb49acfada04fe215fb70d9cdb44114d11>`_
- PEP8: config package `62e65f7d0 <https://github.com/fedora-infra/fedora-packages/commit/62e65f7d0780eac2263cd72e60924abcd3ebc089>`_
- PEP8: fedoracommunity/connector/api package and refactoring code. `fd93b30ef <https://github.com/fedora-infra/fedora-packages/commit/fd93b30efbd4b973787997d39e8ec23e915c120a>`_
- Change in widgets package and bodhiconnector.py `371c1c28d <https://github.com/fedora-infra/fedora-packages/commit/371c1c28df989d55371a902ccd8675bde681be92>`_
- PEP8: bugzillaconnector.py `90d76ad60 <https://github.com/fedora-infra/fedora-packages/commit/90d76ad60fd83854ea4d54bae9efa362a9a4d76f>`_
- PEP8: fasconnector.py `35d991791 <https://github.com/fedora-infra/fedora-packages/commit/35d991791c3297e064d7ed135b3f529a3bcfdc8b>`_
- PEP8: websetup.py `6f32d2671 <https://github.com/fedora-infra/fedora-packages/commit/6f32d267134a613cce121effa995ab398191b7bc>`_
- PEP8: stats.py `3fe651b2c <https://github.com/fedora-infra/fedora-packages/commit/3fe651b2c1cf1e44484f14a50403681f963ae437>`_
- PEP8: distmappings.py `cc86c989c <https://github.com/fedora-infra/fedora-packages/commit/cc86c989cdf9b8301686d4fc2da8654d47454967>`_
- Change in faswhoplugin.py `9d6c28861 <https://github.com/fedora-infra/fedora-packages/commit/9d6c288618646e97e25c5a8d8f786d4ffc9b0f08>`_
- Changes in gitconnector.py `0613eef3a <https://github.com/fedora-infra/fedora-packages/commit/0613eef3af66da4c5446f46838bbdeec1159b44e>`_
- Changes in jsonconnector.py `8bc5549e9 <https://github.com/fedora-infra/fedora-packages/commit/8bc5549e9f965e1d0f756abf78b371f843052462>`_
- Changes in kojiconnector.py `a26a2f51b <https://github.com/fedora-infra/fedora-packages/commit/a26a2f51b515a64f133ea51e9d6877c21eb02ac5>`_
- Merge pull request #50 from echevemaster/develop `cc5c1e720 <https://github.com/fedora-infra/fedora-packages/commit/cc5c1e720b249eac34e0e8d02b077638ef9f181f>`_
- Merge pull request #49 from yograterol/develop `a63744ca5 <https://github.com/fedora-infra/fedora-packages/commit/a63744ca502f84f494be97ad65a57b3526971cd8>`_
- Merge pull request #48 from fedora-infra/feature/epel-bugs `b806c9c3b <https://github.com/fedora-infra/fedora-packages/commit/b806c9c3bfa9c397e95994985dd3ebbea5051472>`_
- Provide a way for the koji builds indexer to initialize itself. `247fc1004 <https://github.com/fedora-infra/fedora-packages/commit/247fc10041e36597fa67b387049bf922bf641e4f>`_
- Merge pull request #51 from fedora-infra/feature/builds-action `c639ade7f <https://github.com/fedora-infra/fedora-packages/commit/c639ade7fea23f1aad7016a9c03b2dd864300eca>`_
- Get fedora-packages working again against modern TG2+crank. `57ed33fd7 <https://github.com/fedora-infra/fedora-packages/commit/57ed33fd7b742fbde311d3ac3110463a1404dd4e>`_
- Remove widgets that we don't actually use but which have a dep on broken repoze.who/what `3b655a931 <https://github.com/fedora-infra/fedora-packages/commit/3b655a9314bea55fa88bf453abf22645868a865a>`_
- Forgot to rm this template too. `c71c7cbeb <https://github.com/fedora-infra/fedora-packages/commit/c71c7cbeba9f1192ac8e177c33e9f368f5315150>`_
- Merge pull request #52 from fedora-infra/feature/remove-repoze `a1553bd2d <https://github.com/fedora-infra/fedora-packages/commit/a1553bd2d886b793e3d9264f9bb8584ab9efa8bf>`_
- Quote up the search term to make it url safe. `dd46b8592 <https://github.com/fedora-infra/fedora-packages/commit/dd46b85929419996716e046543a65851f78d9266>`_
- Doubly encode search term to allow slashes input by various means. `c61781cc4 <https://github.com/fedora-infra/fedora-packages/commit/c61781cc4bf547cced37abf7137e1be40261fb93>`_
- Remove a space. `197d12afc <https://github.com/fedora-infra/fedora-packages/commit/197d12afcb157bcce3b98006609f40c7f91e09a3>`_
- The last piece to get searches with slashes working. `ea1a906c9 <https://github.com/fedora-infra/fedora-packages/commit/ea1a906c99932c9c7b83529cf82638851391fc3a>`_
- Merge pull request #53 from fedora-infra/feature/search-with-slash `50e8e27c2 <https://github.com/fedora-infra/fedora-packages/commit/50e8e27c26b43771e7ab37cb2dd08ba7b85274e1>`_

2.0.10
------

- turn connector profiling on `7665d4568 <https://github.com/fedora-infra/fedora-packages/commit/7665d456887b9afdc8557c718b9a2bdcd4e0ad5f>`_
- Fixed updates widget to work with new tagging scheme `0e0bdf7b2 <https://github.com/fedora-infra/fedora-packages/commit/0e0bdf7b2a04a0f30d2973e51d01fa6fb71ae081>`_
- Fixed the downloads package maintenance for new tagging scheme. pkgdb.get_fedora_releases() now provides branchname, name version, and koji_name as list. `8dfc1c79d <https://github.com/fedora-infra/fedora-packages/commit/8dfc1c79d5e724c37ab8cda581d2229c6ccdda41>`_
- Use new pkgdb gitbranchname instead of old cvs branchname Metrics still use branchname due to bodhi dep `7bb64434c <https://github.com/fedora-infra/fedora-packages/commit/7bb64434cfc1829bcb20df8489cf048ba23c3ae8>`_
- Converted spec download from old cvs to new git repo `6e210e446 <https://github.com/fedora-infra/fedora-packages/commit/6e210e44694ed7bf147a94163f143610cb72d892>`_
- 0.4.2 `630403856 <https://github.com/fedora-infra/fedora-packages/commit/630403856136c222b39d47be79482cd1d95a1456>`_
- The pytz egg-info may not be available for RHEL5 `d95de5551 <https://github.com/fedora-infra/fedora-packages/commit/d95de555118b0f20afc67f518a342550c481200d>`_
- Remove a stray print statement `aff0eb02c <https://github.com/fedora-infra/fedora-packages/commit/aff0eb02cd77870f2bf075e0bc2bae9da2655cc5>`_
- Update our manifest to ensure we pull in all data files `31c7ef194 <https://github.com/fedora-infra/fedora-packages/commit/31c7ef194ec6e85b5cc8f0b817be7bf537d70029>`_
- Merge branch 'master' of git+ssh://git.fedorahosted.org/git/fedoracommunity `dd2863895 <https://github.com/fedora-infra/fedora-packages/commit/dd28638951b390d54c088073cfe27c9b46022af7>`_
- add xapian search `7f66ec477 <https://github.com/fedora-infra/fedora-packages/commit/7f66ec47739e1fdbffa519ab438002386ab1a6f2>`_
- focus FC on search instead of a portal page `73f424fb5 <https://github.com/fedora-infra/fedora-packages/commit/73f424fb5a38184ac1c23e2c509fd42a460924c2>`_
- New fedoracommunity search engine. `01a68b83c <https://github.com/fedora-infra/fedora-packages/commit/01a68b83cf30d103a8aa830e84d05fe5aca2fc5f>`_
- Require xappy for now `235bec7fd <https://github.com/fedora-infra/fedora-packages/commit/235bec7fdaff7cc504404d89eb4e03f4a7d7a1fd>`_
- index sub packages and play with weighting `8df9793ce <https://github.com/fedora-infra/fedora-packages/commit/8df9793ced8a0eb7c8d81ec6ecd7c43257360703>`_
- use json for the data payload and add code for better exact matching `d77a8f296 <https://github.com/fedora-infra/fedora-packages/commit/d77a8f29683dd5a8353732afd34eb4c545cb720e>`_
- have search use new updated format for xapian db `2cc53dde6 <https://github.com/fedora-infra/fedora-packages/commit/2cc53dde6717a842427a816cf9fae17d7c84c279>`_
- add template which uses the new templating plugin to output subpackages `a2c841a42 <https://github.com/fedora-infra/fedora-packages/commit/a2c841a4261d7df6839704cf3637b4e8ee50f066>`_
- add fonts to the install and link to css files so they can find the fonts `af238c009 <https://github.com/fedora-infra/fedora-packages/commit/af238c009d9ac9079e786619fc84dd30291b4541>`_
- turn off crsf connector `bb8357090 <https://github.com/fedora-infra/fedora-packages/commit/bb835709074d9851bd997259add6b03f3d05b809>`_
- remove a bit of debug code that got checked in `2911a06b5 <https://github.com/fedora-infra/fedora-packages/commit/2911a06b5d64b42cb293ac15b6b89bf101c906c3>`_
- add highlighting `9cb8d8e86 <https://github.com/fedora-infra/fedora-packages/commit/9cb8d8e86b8a3b37a2522f46ef461bb342b5ae0f>`_
- add subpackage names to the xapian results weighting `5dda3f520 <https://github.com/fedora-infra/fedora-packages/commit/5dda3f5207d1f2006d64a840d80cceabc44e50c9>`_
- remove some of the old cruft `32c0200bd <https://github.com/fedora-infra/fedora-packages/commit/32c0200bdaef6bcc42335043fe49836056cea4d7>`_
- move the xapian seach into the widgets directory `1104a502d <https://github.com/fedora-infra/fedora-packages/commit/1104a502dfb331989ed8979c6949cd1bd310c52f>`_
- cleanup `fe05e5b36 <https://github.com/fedora-infra/fedora-packages/commit/fe05e5b36acebcb79baa412fa5086d57235a09af>`_
- add a package widget for viewing package info `57a80a185 <https://github.com/fedora-infra/fedora-packages/commit/57a80a1850a4077e17db1845214bd50acdafe249>`_
- filter search and index terms to get better results `e7d084b8b <https://github.com/fedora-infra/fedora-packages/commit/e7d084b8b71a3e7f6af0a7a56ee8ad1da1159168>`_
- extract .desktop files from rpms and index the Categories entry `49cd1c282 <https://github.com/fedora-infra/fedora-packages/commit/49cd1c2820c597c9dc16f7636d92335e2976da9d>`_
- update git-ignore `823dfbcd2 <https://github.com/fedora-infra/fedora-packages/commit/823dfbcd20303d2df5dac031280652e921089cc1>`_
- move root controller to the root.py file instead of the fedoracommunity app `2fe7144f5 <https://github.com/fedora-infra/fedora-packages/commit/2fe7144f5da3000dacf77f01e3fc5ff22737ffae>`_
- add *.rpm to the .gitignore file since search caches these `f45c52123 <https://github.com/fedora-infra/fedora-packages/commit/f45c521239d81f4c5fd8fcdf8d34be2cef907dd2>`_
- improve indexing on actual rpms and subpackages `f73584141 <https://github.com/fedora-infra/fedora-packages/commit/f73584141b8f391a7bcb3527e991682803dfb56c>`_
- make xapian connector more versitile `56fee6bab <https://github.com/fedora-infra/fedora-packages/commit/56fee6babe4a5327b9b435a8727a353ca708e894>`_
- implement the package pages `aeb62eac8 <https://github.com/fedora-infra/fedora-packages/commit/aeb62eac80ab3e99faf28bab7206a82a9e46720d>`_
- add overrview and bugs widget stubs to the entry points `f4bfdfcca <https://github.com/fedora-infra/fedora-packages/commit/f4bfdfccad612c1095610ebc39d4519a87f94b48>`_
- start excising moksha apps in favor of using widget loading `751b3a67b <https://github.com/fedora-infra/fedora-packages/commit/751b3a67b129fcf9cc6131567a7caaef819c655b>`_
- move main templates to their own toplevel src dir `c50d3af9d <https://github.com/fedora-infra/fedora-packages/commit/c50d3af9d2acc0fb437f2dde335da299713643c8>`_
- excise all mokshaapps as we move to a simpler widget based loading `8b95e4043 <https://github.com/fedora-infra/fedora-packages/commit/8b95e4043721d9f61cefa3659da236aae8e35099>`_
- add overview widget stubs and fix url rewriting `2001d5226 <https://github.com/fedora-infra/fedora-packages/commit/2001d5226add35ec9f59f4ee0d5c2c17afda2a89>`_
- pass package_name as a keyword so it cascades to child widgets `fb40bf96d <https://github.com/fedora-infra/fedora-packages/commit/fb40bf96d10aa47c2b349767d422883088c4de41>`_
- allow base_url to take a mako template thatis parsed when the widget is rendered `f0325a3e0 <https://github.com/fedora-infra/fedora-packages/commit/f0325a3e0a92648fddbaed6d77312133baf10b5c>`_
- get info for filling out the details page `61cd44353 <https://github.com/fedora-infra/fedora-packages/commit/61cd44353d3e39d358a6e38236f158d27953d781>`_
- use get_connector instead of instantiating the connector ourselves `0d7a4203a <https://github.com/fedora-infra/fedora-packages/commit/0d7a4203af3f705be3b30db922bb7fcaa73caee8>`_
- add the latest release widget and latest build display `3ba90be99 <https://github.com/fedora-infra/fedora-packages/commit/3ba90be99bbaa50b8889970d656ed96261e180f7>`_
- add initial css styling to match mockups `5f29c06cc <https://github.com/fedora-infra/fedora-packages/commit/5f29c06ccbbf1351a7662aa7fa7ef5aebcb40474>`_
- Work around a bug in yum.disablePlugins() in our search indexer `13ed17c6e <https://github.com/fedora-infra/fedora-packages/commit/13ed17c6eaff39ddf7e640443645dfd4deb37b74>`_
- Reference bug number `7d478193c <https://github.com/fedora-infra/fedora-packages/commit/7d478193ced5f73c5c1d0451c3d6f74ac97afaaa>`_
- make tabs highlight when selected and hovered over using css and javascript `757ee518b <https://github.com/fedora-infra/fedora-packages/commit/757ee518b6a6f84243b74b1d1d2db0e57e7e7e79>`_
- don't consume arg which belongs to tab widget `326e5f170 <https://github.com/fedora-infra/fedora-packages/commit/326e5f1708c3797b20960ba4ed2338146742dd01>`_
- fix typo `6872e0d3f <https://github.com/fedora-infra/fedora-packages/commit/6872e0d3f49eb9f361090d9e6289f6e6045bfe04>`_
- Fix the header/footer namespace in our mako templates `e8f6bd19b <https://github.com/fedora-infra/fedora-packages/commit/e8f6bd19b798c9b73319b406e81e90f1629dd05f>`_
- Disable connector profiling by default `e9319fbfd <https://github.com/fedora-infra/fedora-packages/commit/e9319fbfda864fb33cdafcefe34c5000e3e55ee3>`_
- Update to use our new moksha.utils.get_widget API `350144c75 <https://github.com/fedora-infra/fedora-packages/commit/350144c75132d2b92e403a686cbea7da3a68fbcb>`_
- add images `b0c3cb0c1 <https://github.com/fedora-infra/fedora-packages/commit/b0c3cb0c118c8b25cb830eee70c534774da0829a>`_
- Initial port to ToscaWidgets2! `12dd3d3b9 <https://github.com/fedora-infra/fedora-packages/commit/12dd3d3b9b043e86e6ecf20d0e406a8d1cc518ad>`_
- Disable the moksha live socket, for now `34a5ff1aa <https://github.com/fedora-infra/fedora-packages/commit/34a5ff1aad3d942a5a5adcbaa3f23156a4d7f790>`_
- make cahching more efficent `9d0af5179 <https://github.com/fedora-infra/fedora-packages/commit/9d0af5179d15cfe05b402f7f8a053ad73d6722d0>`_
- make getting files from rpms much faster `919d89822 <https://github.com/fedora-infra/fedora-packages/commit/919d89822879cc4e42e848a7cdf399b3a90781dd>`_
- add the yum.conf we use for getting our repos `46a2d34b3 <https://github.com/fedora-infra/fedora-packages/commit/46a2d34b37f095abf3a1737f6c2e7547db1defe4>`_
- Be explicit with our base_url mako Template usage `a9ac3b2ab <https://github.com/fedora-infra/fedora-packages/commit/a9ac3b2ab7d79f21f397aa94ccb0589f659e6e10>`_
- Fix the location of our custom yum.conf `55f9b1fe8 <https://github.com/fedora-infra/fedora-packages/commit/55f9b1fe879f3f26b38aaa0b3ec1bbbed049a5dc>`_
- Port from the fedora.client.ProxyClient to the proper PackageDB Python API `e9ecf898f <https://github.com/fedora-infra/fedora-packages/commit/e9ecf898fb4c05e2866ce9d8bf0acb41412f08c5>`_
- Add a tool for linking in global python modules into our virtualenv `5f2e986a9 <https://github.com/fedora-infra/fedora-packages/commit/5f2e986a9dbc8cf82e55fd711dbe9931b4b3edc4>`_
- cache owners from pkgdb for fast lookup and add owners to search payload `49285e421 <https://github.com/fedora-infra/fedora-packages/commit/49285e4218a98598145e676c3a7fcb705279f01d>`_
- parse .spec files to grab the url element `f50c16d91 <https://github.com/fedora-infra/fedora-packages/commit/f50c16d917caab686aa1d32c91263122611168f9>`_
- add owner and url to the package overview `c6efbf86b <https://github.com/fedora-infra/fedora-packages/commit/c6efbf86b5ef56d10b6a8b7fb0c5931ad8ed797c>`_
- correctly display owner `e0c775649 <https://github.com/fedora-infra/fedora-packages/commit/e0c77564909f312603e1bc5eba0011563dfab4ea>`_
- correctly highlight the selected tab on static load `20bce6a38 <https://github.com/fedora-infra/fedora-packages/commit/20bce6a38963e81702b358ca60d63ebf135b15ca>`_
- update template to tw2 syntax when displaying widgets `b07bb3c36 <https://github.com/fedora-infra/fedora-packages/commit/b07bb3c367404024315615841ba9017dce806ac4>`_
- remove footter copyright notices for now `cce9d8df4 <https://github.com/fedora-infra/fedora-packages/commit/cce9d8df420ff284afb023adf22fdd85d5f864c5>`_
- add the initial builds page `858900be7 <https://github.com/fedora-infra/fedora-packages/commit/858900be72ad1d949d7438502c43a932f1442e86>`_
- add full html tags (html, head, body) so that javascript renders on dynamic load `a8ec9135d <https://github.com/fedora-infra/fedora-packages/commit/a8ec9135dcd146c300be90df0755386d3b6ad2ce>`_
- move parsers to seperate module and create a simple rpm spec file parser `986996ac3 <https://github.com/fedora-infra/fedora-packages/commit/986996ac31165f1cbf9f42b06381b0bb141a43fd>`_
- make sure we filter search terms when getting info `6b3ab5169 <https://github.com/fedora-infra/fedora-packages/commit/6b3ab516989bbb43fefc453cf1cdb23fd5059b1a>`_
- cache icons in the indexer and show them on the package chrome `0cd1ff67d <https://github.com/fedora-infra/fedora-packages/commit/0cd1ff67df5b15e512e984200f4ec2cb53151f6b>`_
- make the builds table show all types of builds `3c0ec21d9 <https://github.com/fedora-infra/fedora-packages/commit/3c0ec21d982fbd705a2a76c5dec5444626153476>`_
- Optimize our Active Releases widget to utilize koji multicalls `0e2a51f48 <https://github.com/fedora-infra/fedora-packages/commit/0e2a51f480772cf96104e721610d4ee2be4c0965>`_
- Cache our Fedora releases in the PackageDB connector `3f1eaf909 <https://github.com/fedora-infra/fedora-packages/commit/3f1eaf9093245341c4d3214f8a601d6ab3f6bd6d>`_
- More optimization of the Active Releases widget `cce6e792a <https://github.com/fedora-infra/fedora-packages/commit/cce6e792a0da8e5cd858d1e1565d091ee89e56af>`_
- Minor cleanups `9a1a2dc75 <https://github.com/fedora-infra/fedora-packages/commit/9a1a2dc7590f864c74cd8ff29a016e30da9b819c>`_
- add smart icon caching to the search index which picks the best icon to display `91be633ce <https://github.com/fedora-infra/fedora-packages/commit/91be633ce075a9d0d5d2679aacd3518c898bad11>`_
- add icons directory to setup.py `284c97466 <https://github.com/fedora-infra/fedora-packages/commit/284c97466c4044cc2e631e129ce91dfcaf5971f8>`_
- add a couple of directories to .gitignore `88b38d894 <https://github.com/fedora-infra/fedora-packages/commit/88b38d89453e20629fe33cef3cca24747af20998>`_
- Use the 6-hour collection table cache timeout `7e9b0b51f <https://github.com/fedora-infra/fedora-packages/commit/7e9b0b51fb09671ab78d81fdb25042df1471b9df>`_
- fixing the front page logo so that the 'packages' sublogo text doesn't have an underline `75f06c79d <https://github.com/fedora-infra/fedora-packages/commit/75f06c79d2331386c0b079eaa7a0fadb328430f1>`_
- Merge branch 'fedora-packages' of ssh://git.fedorahosted.org/git/fedoracommunity into fedora-packages `b30ea3ecc <https://github.com/fedora-infra/fedora-packages/commit/b30ea3ecc798907f11a6ecd9e7540ca656c79cfe>`_
- hiding the 'search' and 'browse' links for now since they aren't used yet `9ab597cd1 <https://github.com/fedora-infra/fedora-packages/commit/9ab597cd1c10a044670b2b2e61b984396e7ef4a9>`_
- adjusted color of tab container & adjusted color / margins of package name for package profile pages `97b05ebc8 <https://github.com/fedora-infra/fedora-packages/commit/97b05ebc8289e6d8893c4ecffb8fb34fd31c1ce3>`_
- darkening the short description for packages in the header of the package profile `f060beb0e <https://github.com/fedora-infra/fedora-packages/commit/f060beb0eb0c63b3b0e6112075eac6a644f103ef>`_
- some stylistic tweaks for tab container on package profile `48da2167e <https://github.com/fedora-infra/fedora-packages/commit/48da2167e7edf707502ce04fca0bbd2e60d258f0>`_
- h1's should be outside of a tags, not vice-versa; it makes it easier to style without affecting non-logo links in the header. `02ea81829 <https://github.com/fedora-infra/fedora-packages/commit/02ea818294be610d4abef639e60f6c7c4207da5d>`_
- adding logo for package details pages blue bar `21bf248f3 <https://github.com/fedora-infra/fedora-packages/commit/21bf248f30a926abbb2969258636058a9c59718e>`_
- Have our PackageWidget fail gracefully if Koji is unavailable `bec343e2e <https://github.com/fedora-infra/fedora-packages/commit/bec343e2e9014a47f4ebe75da4e44d7ceebea722>`_
- adjustments to logos on the search and profile pages `ea0dae14a <https://github.com/fedora-infra/fedora-packages/commit/ea0dae14ac601daacd78a45f2aa165455a3efe60>`_
- adjustments to templates for logo style `c418d4647 <https://github.com/fedora-infra/fedora-packages/commit/c418d46474a3b87d81245834afe8623555980990>`_
- Merge branch 'fedora-packages' of ssh://git.fedorahosted.org/git/fedoracommunity into fedora-packages `ef4c21934 <https://github.com/fedora-infra/fedora-packages/commit/ef4c2193442f8449cd683ae9465f0be80463945c>`_
- making fedora packages logo in package profiles clickable `c142529b1 <https://github.com/fedora-infra/fedora-packages/commit/c142529b16aee135dbdb627796c914ad0ebca20c>`_
- Only show the version-release in the 'latest build' section `59b88ad20 <https://github.com/fedora-infra/fedora-packages/commit/59b88ad20e4211f9e2847ac5a1369e75d6c5ce1a>`_
- Remove some stray widget instances `ccd9166ed <https://github.com/fedora-infra/fedora-packages/commit/ccd9166ed4a2824c9c06e86916987c443582d8c6>`_
- Port our BugsWidget to TW2 `1f2f464c9 <https://github.com/fedora-infra/fedora-packages/commit/1f2f464c99fbc04d840bcdfe419418d458c79dbb>`_
- Fix our Bugzilla version string `afa0a6cd8 <https://github.com/fedora-infra/fedora-packages/commit/afa0a6cd8bcb6672f9d486d2c82226fb751e10ec>`_
- Initial port of the package updates widget `2b699a3d6 <https://github.com/fedora-infra/fedora-packages/commit/2b699a3d6feaf8f5fb0aec46beaeef1ca26127c1>`_
- adjusting the second-level nav so that there's no little grey tip on the left end; sizing and spacing out a bit too `c0aeca830 <https://github.com/fedora-infra/fedora-packages/commit/c0aeca830e9d51b6fa5d76cef42e41babbf7c256>`_
- Merge branch 'fedora-packages' of ssh://git.fedorahosted.org/git/fedoracommunity into fedora-packages `9dbc403b5 <https://github.com/fedora-infra/fedora-packages/commit/9dbc403b5b5d3023408a8db383823744021d3627>`_
- style changes for darkening headers and body text in package profile pages `cae55b017 <https://github.com/fedora-infra/fedora-packages/commit/cae55b0172fbb55eba64aed6a3262f52c7765430>`_
- tweaking the active releases overview (and all lists for that matter) to have larger, more readable fonts and nicer link colors `15ae3d5c9 <https://github.com/fedora-infra/fedora-packages/commit/15ae3d5c90b413a575acd68d3277934a8f7f7cf2>`_
- tweaking the package tree widget on the package profile pages to have space for longer names... `57cecd349 <https://github.com/fedora-infra/fedora-packages/commit/57cecd349d3bee2970d3f658bbe2383c2ec70cc1>`_
- some spacing / adjustment for the left sidebar in the package details pages `85b1126df <https://github.com/fedora-infra/fedora-packages/commit/85b1126df1f1b3d5fa8719a8fa14be84984c2300>`_
- css adjustments to the owner section of the package details' left sidebar `e3d1e116b <https://github.com/fedora-infra/fedora-packages/commit/e3d1e116b220265ffd824bb3f89ccb98d990041d>`_
- w00t!!!! got line wrapping working for really long package names in the package tree in the left sidebar of package details pages...! `560dab17c <https://github.com/fedora-infra/fedora-packages/commit/560dab17cd46e7da8e84f1e1c90d507cd28ff210>`_
- link colors should be fedora blue! `ebcadc888 <https://github.com/fedora-infra/fedora-packages/commit/ebcadc88819346613eddff8cdef30d14d1f78385>`_
- add changelog tab `63fc981e7 <https://github.com/fedora-infra/fedora-packages/commit/63fc981e702fd54b5a5727d504bab47c8da5d3e0>`_
- do not error out on bad icons `46cae9a29 <https://github.com/fedora-infra/fedora-packages/commit/46cae9a29edc87be7f3015f24928c73e35be6a5b>`_
- Use relative image paths in our css. `6da4aaee5 <https://github.com/fedora-infra/fedora-packages/commit/6da4aaee5b3dfd779776140be9c533f684d1201c>`_
- Add a 1x1 pixel empty image for our initial hidden build state image. `775a858ad <https://github.com/fedora-infra/fedora-packages/commit/775a858addfb3c7eea4fc5e5408caccf002a1467>`_
- Create another empty icon, this time for our update karma icons. `8c7023bcd <https://github.com/fedora-infra/fedora-packages/commit/8c7023bcde4ef04cdf6562e616793942c47a8b3e>`_
- maps package versions to their dists in a xapian database `40ff39829 <https://github.com/fedora-infra/fedora-packages/commit/40ff398295c7be17999390fccebf33d943ce2da8>`_
- fix variable scope issue; record timestamp on success; pretty print timestamp `0dc81f922 <https://github.com/fedora-infra/fedora-packages/commit/0dc81f9224bdf77820b3d6c417f661ca1caf40a1>`_
- correctly print out version `df0546d96 <https://github.com/fedora-infra/fedora-packages/commit/df0546d96a56fba6869a5bf913dbc770ad36c35a>`_
- Apply a patch from Brennan Ashton to reflect recent Koji rawhide tag changes. `d734f7e89 <https://github.com/fedora-infra/fedora-packages/commit/d734f7e8956b06ef9bf38cdabda8552a63b186fc>`_
- 0.4.3 version bump `5d60824f3 <https://github.com/fedora-infra/fedora-packages/commit/5d60824f38f6c994170a50817b890dc994d5f13f>`_
- add methods for getting info from the version mapper db `77a446872 <https://github.com/fedora-infra/fedora-packages/commit/77a446872b604f924c383914aac595e977041583>`_
- fix typo in version mapper `364821cfb <https://github.com/fedora-infra/fedora-packages/commit/364821cfb63ac6563552f15dba2bd6085a027f88>`_
- add rpm downloading and rpm layout views to the connector `85e9fad71 <https://github.com/fedora-infra/fedora-packages/commit/85e9fad71c6aa11bb8a3cff57cd7b0faaaf38f20>`_
- have changelog use the versionmapper xapian db instead of querying koji `49919ed4e <https://github.com/fedora-infra/fedora-packages/commit/49919ed4e95e4b1c54d206e2057658624c06b961>`_
- add the contents tab which displays files in an rpm `67d668a94 <https://github.com/fedora-infra/fedora-packages/commit/67d668a945fc95c71e26d0a8eeaf8a89d52ab2e2>`_
- don't put new package into found package cache as we don't have a doc id yet `6e1cb2940 <https://github.com/fedora-infra/fedora-packages/commit/6e1cb2940b85305da45e6ea64515dc453497d1e4>`_
- add boilerplate for requires, depends, provides, obsoletes and conflicts tabs `cbd39537e <https://github.com/fedora-infra/fedora-packages/commit/cbd39537e7a69802092ebba617f0dfd316081338>`_
- add connectors for provides, requires, conflicts and obsoletes `61ead5cfb <https://github.com/fedora-infra/fedora-packages/commit/61ead5cfb3d2944ba35486ec3c62765d16d0ae9d>`_
- Remove references to Koji tag dist-rawhide in favor of new rawhide tag. `fb80dd31c <https://github.com/fedora-infra/fedora-packages/commit/fb80dd31c9002ee03b5288ee68dd7b17b3dfbcc1>`_
- fix some typos in the koji connector `4ff111704 <https://github.com/fedora-infra/fedora-packages/commit/4ff111704b89762826ac35a1ced14e701e8e0316>`_
- add requires table `aebceb43e <https://github.com/fedora-infra/fedora-packages/commit/aebceb43ecfee1b2c7ee1fffeef3d53a78ba2001>`_
- add conflicts, obsoletes and provides pages `f5c559371 <https://github.com/fedora-infra/fedora-packages/commit/f5c55937181e3f6f8035d2436b74dc01be6b0cb5>`_
- Initial commit of fcomm-ctl.py helper script. `cf53262a4 <https://github.com/fedora-infra/fedora-packages/commit/cf53262a45c8fa0eeef866b1f2b5e4d9a1bc680f>`_
- Add xappy to our gitignore `4e75c2989 <https://github.com/fedora-infra/fedora-packages/commit/4e75c29895a0f7abe294726d1d0e0b737e6413e0>`_
- Pull in virtualenvcontext when we need it `5ede4d913 <https://github.com/fedora-infra/fedora-packages/commit/5ede4d91376e7e3760e7bddac3ea5a6e0ce203d0>`_
- Have fcomm-ctl download our xapian db snapshot `ad5224236 <https://github.com/fedora-infra/fedora-packages/commit/ad5224236a2203153b187d01970df307e7487edc>`_
- Try to automatically generate the moksha ctl.cfg if we can `99bcdb238 <https://github.com/fedora-infra/fedora-packages/commit/99bcdb238e75b5cd7696829f6d996ff7c3028f44>`_
- Create the logs directory if it doesn't exist in our development setup `7383a69da <https://github.com/fedora-infra/fedora-packages/commit/7383a69da43932dd5217575cc5ac9322c401a42a>`_
- Pull in the latest xapian db snapshot `64bbe38db <https://github.com/fedora-infra/fedora-packages/commit/64bbe38db1a0b84aa8a3f8b641f18ce1a35b877b>`_
- Make our bugzilla dashboard handle packages that have a ton of closed bugs `45fc9f839 <https://github.com/fedora-infra/fedora-packages/commit/45fc9f839c7681dd33ad91b4c02c47c29f75996d>`_
- Disable our aggressive bugzilla grid caching. `55afedc8c <https://github.com/fedora-infra/fedora-packages/commit/55afedc8ccf8f56fe23f45773b1b780fdfc8622f>`_
- do not try to retrive task info for pacakages not built in a repo `7f8e4a549 <https://github.com/fedora-infra/fedora-packages/commit/7f8e4a54932debdb968a45006d6f4c9d526914b8>`_
- Use consistent spacing. `b0e21695a <https://github.com/fedora-infra/fedora-packages/commit/b0e21695a2a32bfc114fcccb5b47d40cac937284>`_
- Add a `fcomm-ctl.py download_icons` function `99363d551 <https://github.com/fedora-infra/fedora-packages/commit/99363d5518a043f13b2c3b26036fc80f2e6ac94b>`_
- first stab at supporting subpackages `eac7f1704 <https://github.com/fedora-infra/fedora-packages/commit/eac7f170400f1d9bf34c3b45e10a02c31275ef5c>`_
- add jstree jquery plugin and have it populate content view `66620eb0f <https://github.com/fedora-infra/fedora-packages/commit/66620eb0fb20892950ab673c4f212ee0327d9ccf>`_
- Add our initial Sources section, with a basic specfile viewer `ecd39a556 <https://github.com/fedora-infra/fedora-packages/commit/ecd39a556ffed428424233d70817758447924b3f>`_
- Set our default git repo path `bc6b3a5be <https://github.com/fedora-infra/fedora-packages/commit/bc6b3a5bef70f9c0ccef5938db3aa3c2afbd588a>`_
- Disable our FAS authentication layer `fce0bd56a <https://github.com/fedora-infra/fedora-packages/commit/fce0bd56a942bf94a29e7ed1b36af990dda279ee>`_
- Add placeholders for the rest of our Sources widgets. `5ac25436c <https://github.com/fedora-infra/fedora-packages/commit/5ac25436c175dd42a0ad249049ebe214e8a5fc26>`_
- Add an initial barebones Patches widget. `8b8b3f164 <https://github.com/fedora-infra/fedora-packages/commit/8b8b3f1645e48df8b0d0332d924ac234f4c4e19c>`_
- Hack around GitPython not being automatically installed by our setup.py `8775a11fc <https://github.com/fedora-infra/fedora-packages/commit/8775a11fce029c6f8c41a1268f6779414d24f18a>`_
- Fix our GitPython easy_install workaround `029edff3f <https://github.com/fedora-infra/fedora-packages/commit/029edff3fb72d5f3535ea6e34ce4364745969045>`_
- Fix a bug in our initial fedpkg clone `55e73a72b <https://github.com/fedora-infra/fedora-packages/commit/55e73a72b0a16d3f98d0fbacbd506af583dfdee4>`_
- Add a basic patch viewer with syntax highlighting. `80dbe214a <https://github.com/fedora-infra/fedora-packages/commit/80dbe214ac33f5c84315877490be02218d24d6dc>`_
- new icons and fix css for displaying file trees `5ceea1e5f <https://github.com/fedora-infra/fedora-packages/commit/5ceea1e5fc39bcd05087bbfb2ad4c0e8cd46ec00>`_
- Show the diffstat of our patches `3ba1f093e <https://github.com/fedora-infra/fedora-packages/commit/3ba1f093ed287e0bdf1cfd3ec35dac48a4d7a00b>`_
- Add the summary of changes across all patches. `b0b06606e <https://github.com/fedora-infra/fedora-packages/commit/b0b06606e89dbf3c9adbadae59bb204a8b7a0763>`_
- Improve rendering of our diffstat output. `30dfbe85c <https://github.com/fedora-infra/fedora-packages/commit/30dfbe85ce1111147dac3f948bb30ceb73c621f3>`_
- We now require diffstat and fedpkg `60b663732 <https://github.com/fedora-infra/fedora-packages/commit/60b6637329df1f3aff7514b198cee49e75bca8c3>`_
- no need for a custom cssclass for our pygments HtmlFormatter `f5e94de45 <https://github.com/fedora-infra/fedora-packages/commit/f5e94de4525933e1ba42dd97e9d4f1df3d722a6e>`_
- Add link to raw patch in footer `6fd2ea3a5 <https://github.com/fedora-infra/fedora-packages/commit/6fd2ea3a5fb5794db3f1a41bb010d401f188cdd0>`_
- Display patch changelogs. `a12f6edb4 <https://github.com/fedora-infra/fedora-packages/commit/a12f6edb47bcd41d5829bdb3065f019917e6b54c>`_
- Comments are good `8ab8a1978 <https://github.com/fedora-infra/fedora-packages/commit/8ab8a19784cacc8b88d4daf5c2580095558a8c90>`_
- Use kitchen to convert our spec & patch bytes to unicode. `3206ee5bf <https://github.com/fedora-infra/fedora-packages/commit/3206ee5bf0c2edb3ce82f73e5ec30bd3d7b2467b>`_
- changing label in changelog dropdown from build to release ('build' is wrong in this context) `bf73edea0 <https://github.com/fedora-infra/fedora-packages/commit/bf73edea0bb8f52eff8073d3d18453c0d6db98f3>`_
- removing unnecessary header `31ff28e87 <https://github.com/fedora-infra/fedora-packages/commit/31ff28e87f560909ac61bff6f81e5f82d47281d2>`_
- git troubles Revert "removing unnecessary header" `5bbbf7bf1 <https://github.com/fedora-infra/fedora-packages/commit/5bbbf7bf1269cd5775b8fa8e04cdb14e32d85f10>`_
- git troubles Revert "changing label in changelog dropdown from build to release ('build' is wrong in this context)" `8b2ca52d1 <https://github.com/fedora-infra/fedora-packages/commit/8b2ca52d11e3aeb9623ba1c20ad1372ac91c0728>`_
- adding some padding to the bottoms of pages so it's not so abrupt. i guess the footer is disabled? `d38b1fe03 <https://github.com/fedora-infra/fedora-packages/commit/d38b1fe033fb598b62decfcbb7531756094f75d5>`_
- removing header; think it's extraneous `548aa0d1b <https://github.com/fedora-infra/fedora-packages/commit/548aa0d1b7190b92986a75f2606c55ffb2defb97>`_
- removing header / extraneous `19ba4ea20 <https://github.com/fedora-infra/fedora-packages/commit/19ba4ea208870cb87110d5bc0bd3181f66ed08ec>`_
- tweaks to the appearance of the filter bar on the contents page `468da2aec <https://github.com/fedora-infra/fedora-packages/commit/468da2aec910553bedc15dcb196684f5508e4583>`_
- correctly url rewrite links and use subpackage links in search `bde4485ce <https://github.com/fedora-infra/fedora-packages/commit/bde4485cedbd0beba1d30b8db01973db7bd76d10>`_
- use dot syntax for mako template referencing `ec55a2694 <https://github.com/fedora-infra/fedora-packages/commit/ec55a2694e7d117d89ffabd037ea953579b7b00a>`_
- link to css resources indirectly `7c6d6c867 <https://github.com/fedora-infra/fedora-packages/commit/7c6d6c86716fb05995e224d44a055896b0ba551a>`_
- up the version and fixup the spec file to correctly package tw2 `4ccac6b79 <https://github.com/fedora-infra/fedora-packages/commit/4ccac6b799fe77f858b84d7c543d3b4b607a734e>`_
- use dot format for referencing mako templates `7370285fd <https://github.com/fedora-infra/fedora-packages/commit/7370285fd24a9e26640b70be16d46bcaf0cca62c>`_
- spacing out the entries in the content tab tree more `3fb9ce2b5 <https://github.com/fedora-infra/fedora-packages/commit/3fb9ce2b58874d221e841c8f4791fc1b382a5222>`_
- get CSS links right and make sure all css files are in the manifest `181487166 <https://github.com/fedora-infra/fedora-packages/commit/181487166060121912ccacccde3de7cf26698c2d>`_
- correctly set up the path to the tw2 resources `f0ca37c0a <https://github.com/fedora-infra/fedora-packages/commit/f0ca37c0ab5bd41b50a57cd2625e4ef7ce179ec5>`_
- Subclass tg AppConfig and do our TW2 customization in there. `7a674244a <https://github.com/fedora-infra/fedora-packages/commit/7a674244aa1f96b1dd0855ff663651fbb8b00df2>`_
- Remove the unused orbited config `d1875ae08 <https://github.com/fedora-infra/fedora-packages/commit/d1875ae0844428847f3edbae09e6721e3b72598b>`_
- Get the initial Sources->Tarballs widget up and running. `1aacb0f79 <https://github.com/fedora-infra/fedora-packages/commit/1aacb0f79bde525d838b09c7b70a2e87d727ad47>`_
- Hide some widgets that are "on hold" `60efd7a4b <https://github.com/fedora-infra/fedora-packages/commit/60efd7a4b34e8efc6eed9648df1cbec8820796ad>`_
- Use the BashLexer to highlight the specfile `9123cf460 <https://github.com/fedora-infra/fedora-packages/commit/9123cf4607b4342b8e1890360aed998a6938922f>`_
- Minor comment fix `46de1faff <https://github.com/fedora-infra/fedora-packages/commit/46de1faff0081541997971c18284cb041e593584>`_
- Use dotted template notation `f489f459c <https://github.com/fedora-infra/fedora-packages/commit/f489f459c469609eedc882d940e0b17b4ee93b26>`_
- add a archive_fedoracommunity_resources dist command `81d1847f5 <https://github.com/fedora-infra/fedora-packages/commit/81d1847f5a8dc3c913c3c123a5e71af0136f2410>`_
- import the tw2 version of the widget directly `625421ef8 <https://github.com/fedora-infra/fedora-packages/commit/625421ef85bb7edbb101df91664434811c46242c>`_
- Move our Git logic into a GitConnector `df5b5cc10 <https://github.com/fedora-infra/fedora-packages/commit/df5b5cc104ed49c22e1c25d7b2c16cca37404c76>`_
- Add a releases dropdown filter for our specfile viewer `f49ba6f31 <https://github.com/fedora-infra/fedora-packages/commit/f49ba6f31c423043f570a3776188997877cba372>`_
- Display the local URL when running fcomm-ctl.py start `9152284c8 <https://github.com/fedora-infra/fedora-packages/commit/9152284c8242e137b8d3f3576b8cb2c93218bf3f>`_
- patch tweaks for css `6716f4c1e <https://github.com/fedora-infra/fedora-packages/commit/6716f4c1e4cf3fd34092daa8557ec2b85ac3b6d3>`_
- Merge branch 'fedora-packages' of ssh://git.fedorahosted.org/git/fedoracommunity into fedora-packages `5f42caa18 <https://github.com/fedora-infra/fedora-packages/commit/5f42caa188774cc7f622844adec79cc0cbffeda1>`_
- Set some CSS classes for our active patch & content `c81932410 <https://github.com/fedora-infra/fedora-packages/commit/c81932410b54fce666ed73b58380932c7226d679>`_
- Try using 'inline' line numbers for our patches `ef10e058c <https://github.com/fedora-infra/fedora-packages/commit/ef10e058c50cfc068eb68c70e8c597c57a278b99>`_
- Revert "Try using 'inline' line numbers for our patches" `9a6d4d78a <https://github.com/fedora-infra/fedora-packages/commit/9a6d4d78aaf8a566256251d6434f1d025e1a424a>`_
- Disable line numbers in our patches `0a9763cec <https://github.com/fedora-infra/fedora-packages/commit/0a9763cecd5829cf9af072bf813b617cec0bb3e6>`_
- Add a release filter for our patches widget `e3b86e505 <https://github.com/fedora-infra/fedora-packages/commit/e3b86e505bc0bc3d9449fc207867273bc1f487cb>`_
- Remove our git connector, since I'm taking a different approach. `1c1147ac9 <https://github.com/fedora-infra/fedora-packages/commit/1c1147ac99b94f2d3e2ae490252e32347969ac43>`_
- Don't import the GitConnector anymore `2d68753a2 <https://github.com/fedora-infra/fedora-packages/commit/2d68753a219e0c6c5a525bd206c91b7089373179>`_
- Hide releases that the package is not branched for `183da83da <https://github.com/fedora-infra/fedora-packages/commit/183da83da16ae7c638599cb38d179c044b74cc6e>`_
- Add a release filter to our tarballs widget `bb53817d3 <https://github.com/fedora-infra/fedora-packages/commit/bb53817d35242c06bc55d05814cefced484efbe9>`_
- use tg.url to rewrite links if needed `a98677b66 <https://github.com/fedora-infra/fedora-packages/commit/a98677b6660a53c092229221622217f90c6af71c>`_
- make sure image files are deployed `409c4aa8e <https://github.com/fedora-infra/fedora-packages/commit/409c4aa8e1679ab924b97b7ec69077f08d9b9643>`_
- add tg2.widgets entry point so resources get deployed `4ba6cdd8b <https://github.com/fedora-infra/fedora-packages/commit/4ba6cdd8b672272cbdcafc0292f36043c0950bd0>`_
- Automatically link up bugs and CVEs in patch ChangeLogs. `3eead37ba <https://github.com/fedora-infra/fedora-packages/commit/3eead37baa7b1eddf179bdccf2e5f9ff8a1536b4>`_
- Reverse the ordering of our Release dropdown. `99497027e <https://github.com/fedora-infra/fedora-packages/commit/99497027edf8596e04f72f643aa9a460c22ad37b>`_
- Improve our bugzilla regex `20fd0239f <https://github.com/fedora-infra/fedora-packages/commit/20fd0239f0a1d87055cc0b5fb337484b5676daf6>`_
- pull the link injection out into its own method `d016cd480 <https://github.com/fedora-infra/fedora-packages/commit/d016cd480b920ab2d5e0afe48bc8cf79890259c7>`_
- More bug number regex improvements `58347f876 <https://github.com/fedora-infra/fedora-packages/commit/58347f8764d6ebbe98eb49f9b029489f4ab76ee6>`_
- Get our Sources widgets working with dead packages. `fcad91dd4 <https://github.com/fedora-infra/fedora-packages/commit/fcad91dd40702cebc184feb115d5232dd3605a6c>`_
- Add consistent labels to our release filter `19793b42f <https://github.com/fedora-infra/fedora-packages/commit/19793b42fe3bba59f916e33cced95b260f668168>`_
- Pull out some unused imports `8f763c22e <https://github.com/fedora-infra/fedora-packages/commit/8f763c22edfc2205d11adf52f86289cbdb6973b8>`_
- Use Bugzilla multicalls to optimize our Bug Stats widget. `32012b6ef <https://github.com/fedora-infra/fedora-packages/commit/32012b6efc77fb7155a877af3d6a78c8785247ff>`_
- Manually chose the RHBugzilla3 class to speed up initialization. `84408691f <https://github.com/fedora-infra/fedora-packages/commit/84408691f4c28b5f005334c960dd01a87ae5fcb2>`_
- add a collection.OrderedDict class if it doesn't exist `c0e4d28a8 <https://github.com/fedora-infra/fedora-packages/commit/c0e4d28a84da8be34c2f8e3af13b8921b2a26f53>`_
- some more path fixes `fc9a3afa5 <https://github.com/fedora-infra/fedora-packages/commit/fc9a3afa5a1a66a4e21f52c36df966ff368a2164>`_
- force WebOb >= 1.0 to load `c4754f9db <https://github.com/fedora-infra/fedora-packages/commit/c4754f9dbae1ccdab8847cc700761cec387141a6>`_
- bump version `3953f96ff <https://github.com/fedora-infra/fedora-packages/commit/3953f96ff81ddfcba36c02138dfd3efefb228903>`_
- explicitly define OrderedDict in module instead of monkey patching `886dbb018 <https://github.com/fedora-infra/fedora-packages/commit/886dbb018b3a36e22c486b7a511fc859b887dddf>`_
- a bunch of CSS voodoo to make the patches UI look more like the mockups, including the magenta highlight around active / open patches. still a work-in-progress. `75b30bae7 <https://github.com/fedora-infra/fedora-packages/commit/75b30bae791b9113e06f4b1559b2ed555bdc06f1>`_
- fix typo `ecea55e15 <https://github.com/fedora-infra/fedora-packages/commit/ecea55e1500aff83a6f639b58f190c30d6de7987>`_
- Merge branch 'fedora-packages' of ssh://git.fedorahosted.org/git/fedoracommunity into fedora-packages `29ec2625b <https://github.com/fedora-infra/fedora-packages/commit/29ec2625b2579ef9eaca115f15a19520c86d8bf8>`_
- Merge branch 'fedora-packages' of ssh://git.fedorahosted.org/git/fedoracommunity into fedora-packages `6322b0961 <https://github.com/fedora-infra/fedora-packages/commit/6322b096102233af47fa5861b5b42ad87065edbd>`_
- use getattr to check for OrderedDict `6c90f2738 <https://github.com/fedora-infra/fedora-packages/commit/6c90f2738ff9aafa530dfcf657ab6f988508b5cb>`_
- Fix a broken OrderedDict `280a87850 <https://github.com/fedora-infra/fedora-packages/commit/280a87850eea6747a085b5d934a8499e554256dc>`_
- Fix a broken OrderedDict `1ec8dda81 <https://github.com/fedora-infra/fedora-packages/commit/1ec8dda81e8f3fc88e3d050db39ba8c01630d7f8>`_
- Merge fedoracommunity.lib.helpers into fedoracommunity.lib.utils `1afb15ed4 <https://github.com/fedora-infra/fedora-packages/commit/1afb15ed476c04cbb3e7a6b10416f8b27767eb39>`_
- use the ordereddict module if official OrderedDict is not available `d4055283a <https://github.com/fedora-infra/fedora-packages/commit/d4055283a8887146db16ee5909ea3ad03c32ea31>`_
- manually init the tw2 middleware so we work with older TurboGears `019542246 <https://github.com/fedora-infra/fedora-packages/commit/019542246a477d1484d832f823f0f37270c196eb>`_
- move a few more widgets to tw2 `eeae7511e <https://github.com/fedora-infra/fedora-packages/commit/eeae7511e2b5123af14cc6504276c163b1dc735e>`_
- add back footter info to comply with AGPL linking requirements `b590c431c <https://github.com/fedora-infra/fedora-packages/commit/b590c431c7f80a3aae63783818b88543f5e6d79c>`_
- put a dependency on python-ordereddict `ceec7b139 <https://github.com/fedora-infra/fedora-packages/commit/ceec7b139f0b8d81898d7a159454922a8b60ce30>`_
- checkin the build.ini file `9717701e2 <https://github.com/fedora-infra/fedora-packages/commit/9717701e2f8d99a6e74efc71710e34afc4b15c47>`_
- typo s/lamda/lambda/ `464b056b7 <https://github.com/fedora-infra/fedora-packages/commit/464b056b7102e6b6bc860409a063dadfdd169b3e>`_
- remove old import `c2b9879be <https://github.com/fedora-infra/fedora-packages/commit/c2b9879bef6e295cf6e1af9ae498a22671093059>`_
- add empty helpers.py file which turbogears seems to need `7a0e16da3 <https://github.com/fedora-infra/fedora-packages/commit/7a0e16da31210ea9337158cf11fe63eeeaae37ac>`_
- make sure custom_tw2_config member exists before using it `a807c369f <https://github.com/fedora-infra/fedora-packages/commit/a807c369f94a51bdeff77d08979b1105d8b69fc5>`_
- we need to import the empty helpers file so it shows up in the module `1b9d7a29c <https://github.com/fedora-infra/fedora-packages/commit/1b9d7a29c6927426a04c3a80d0c66a5bb8089f1a>`_
- import tw2.core as twc (twc isn't a module of tw2.core) `c7da56ded <https://github.com/fedora-infra/fedora-packages/commit/c7da56ded3af76626068a60955da79ee41d3aa82>`_
- Fix an incorrect variable name `2129f1a5f <https://github.com/fedora-infra/fedora-packages/commit/2129f1a5fc4d6b43dd00410f95e3a27a6e4e99eb>`_
- Fix yet another typo `9ea9ac69c <https://github.com/fedora-infra/fedora-packages/commit/9ea9ac69cb7ede1ef46f4b43f23398792aef6f5b>`_
- lots more pretty for the patches UI. but again, work-in-progress! `4319d4558 <https://github.com/fedora-infra/fedora-packages/commit/4319d4558b61c2346afb48bf49aa5b205c6599fc>`_
- Merge branch 'fedora-packages' of ssh://git.fedorahosted.org/git/fedoracommunity into fedora-packages `a36190f91 <https://github.com/fedora-infra/fedora-packages/commit/a36190f91bab51ae1fd9621e96c0addc62a7ee7d>`_
- use tw2 middleware hack for only TurboGears < 2.1 `430db942c <https://github.com/fedora-infra/fedora-packages/commit/430db942ce921eaf7b3d0fb4b1a3158486f9d039>`_
- make indexers more flexable by spliting into modules and binaries `db9a3c733 <https://github.com/fedora-infra/fedora-packages/commit/db9a3c733dee7b3cdabab6257b8f65bd4ec7a131>`_
- split version mapper into a module and executable for running in cron `70b60942a <https://github.com/fedora-infra/fedora-packages/commit/70b60942a887e7ab10e362344a423b51d2f99adc>`_
- more refinements on patches CSS and toning down AGPL footer `957dfe842 <https://github.com/fedora-infra/fedora-packages/commit/957dfe842b78747bf724a11c95ba627b7f2ca48f>`_
- Merge branch 'fedora-packages' of ssh://git.fedorahosted.org/git/fedoracommunity into fedora-packages `7fe21117a <https://github.com/fedora-infra/fedora-packages/commit/7fe21117a3c25b9e6890f613c0843d88b50e7197>`_
- install scripts to bin dir `fd1a52b85 <https://github.com/fedora-infra/fedora-packages/commit/fd1a52b855cc67272acd35cfbd976135c16277ce>`_
- add locking for rpm file downloads `0e6d2e932 <https://github.com/fedora-infra/fedora-packages/commit/0e6d2e9322f7a5c08f2ea45ab0464aaf9e14661c>`_
- more patches refinement: added a more prominent 'get raw patch' link, available without diving into individual patches. also a row hover effect in the patches list. also an improved header for individual patches. finally, some footer / agpl notice improvements. `adaa00d82 <https://github.com/fedora-infra/fedora-packages/commit/adaa00d82782dfa48289b111f7925c43d4602c3b>`_
- new hotness, new spinner `881117620 <https://github.com/fedora-infra/fedora-packages/commit/881117620f6e082932383535ccd0c23da377112a>`_
- fixing the css goof that made the all patch summary open by default `1ff358d7a <https://github.com/fedora-infra/fedora-packages/commit/1ff358d7aaa19eb3e16f8f0dcf2b8d46f9423086>`_
- fixing the link text replacement so it shows 'hide' when it's open instead of 'show' `fb3c76964 <https://github.com/fedora-infra/fedora-packages/commit/fb3c769646e3dcb782f80fdc11bb500a7d1aa17b>`_
- adding new spinner for in-list loading `e168f4273 <https://github.com/fedora-infra/fedora-packages/commit/e168f427334190f45e0b9217e901553d1907d131>`_
- making the patch hotness first under sources `8fe0875d1 <https://github.com/fedora-infra/fedora-packages/commit/8fe0875d1d677fe84a999173928b0cd4533892fb>`_
- make older verisions of lockfile work `084419624 <https://github.com/fedora-infra/fedora-packages/commit/084419624983bd51b87ac05b4571656c897ca858>`_
- fast heartbeat monitoring for proxy servers `90ca6632d <https://github.com/fedora-infra/fedora-packages/commit/90ca6632d3b2830db7aeb2ab35b1bc31148904da>`_
- use the Image module instead of GdkPixbuf for RHEL6 support `ec91dd420 <https://github.com/fedora-infra/fedora-packages/commit/ec91dd42066be9afe2dccfc8de5f0a43569da66d>`_
- fix path issues with indexers `a68179afc <https://github.com/fedora-infra/fedora-packages/commit/a68179afc9b783ce3f7555254a9cf626e8209500>`_
- make sure to import FileLock as LockFile `4476c15a3 <https://github.com/fedora-infra/fedora-packages/commit/4476c15a32f5f033f68458bad6c17d4a1a09f3c0>`_
- fixing the styling oddities on the relationships tab lists `a95fc32c3 <https://github.com/fedora-infra/fedora-packages/commit/a95fc32c3f2a768cfe32091cd95dc898694b4624>`_
- fix typo s/icons_dir/icon_dir `ce3a9d426 <https://github.com/fedora-infra/fedora-packages/commit/ce3a9d4262374f4030426c3d93bd7e04b23a0353>`_
- whoops didn't set sources to open first to 'patches', just moved patches nav position. setting it to open first now. `ae6e22b93 <https://github.com/fedora-infra/fedora-packages/commit/ae6e22b93357b5da10578503891a99c3d5c2c01a>`_
- Require python-tw2-jquery-ui `7da9c03e0 <https://github.com/fedora-infra/fedora-packages/commit/7da9c03e03402a2f9115d2c29edccd910bf35e66>`_
- Merge branch 'fedora-packages' of ssh://git.fedorahosted.org/git/fedoracommunity into fedora-packages `e5e1ad92e <https://github.com/fedora-infra/fedora-packages/commit/e5e1ad92e7189c946660e541b0814eba598af3d5>`_
- Merge branch 'fedora-packages' of ssh://git.fedorahosted.org/git/fedoracommunity into fedora-packages `7fc06c512 <https://github.com/fedora-infra/fedora-packages/commit/7fc06c512d90ff5b622c81d7fa7f1473d7df357d>`_
- cd back into the cache directory when running system commands `651a31b77 <https://github.com/fedora-infra/fedora-packages/commit/651a31b77738b1e8abf796364adc9ed85fdb91ca>`_
- fix typo `15a8b1858 <https://github.com/fedora-infra/fedora-packages/commit/15a8b18586d7124e5523a182d2c7b025dbc9f16a>`_
- use subprocess.Popen instead of os.system so we don't have to cd `84bb10a9e <https://github.com/fedora-infra/fedora-packages/commit/84bb10a9e06e46b89753ff28e76809b5fb63012f>`_
- don't error out if we can't load an icon, just use default `53e2dc47d <https://github.com/fedora-infra/fedora-packages/commit/53e2dc47d644f8a4b007de554c8d36ccac51ee48>`_
- Update our specfile requirements `98ef85f5e <https://github.com/fedora-infra/fedora-packages/commit/98ef85f5e495c8281c8fcd395df5fda07f2a91ee>`_
- Work with python-lockfile 0.8 and 0.9 `c91d864d8 <https://github.com/fedora-infra/fedora-packages/commit/c91d864d87d915b062eb9625edf8f9af9869048b>`_
- Dynamically load the patches into an outer patches_container. `3673c231b <https://github.com/fedora-infra/fedora-packages/commit/3673c231b3eb7bcc6e2177db6f6d62478df42058>`_
- More dynamic widget loading container fixes. `3b8995f9f <https://github.com/fedora-infra/fedora-packages/commit/3b8995f9fe95e1453cc34664219c1bef07d809fd>`_
- use Popen properly with pipes `4bea9232c <https://github.com/fedora-infra/fedora-packages/commit/4bea9232cb1aa28844d3fe326d5c78454f82d9d2>`_
- ditch lazy loading of icons so that we can discard icons we can't read `1b7fffc13 <https://github.com/fedora-infra/fedora-packages/commit/1b7fffc13657d7854efac70cb6842ea295f03c45>`_
- Create a 'default' method along with '_default' to work with older TG2 `c017f4099 <https://github.com/fedora-infra/fedora-packages/commit/c017f4099878699ead0ab906a7486bd681c560c6>`_
- Require python-xappy and rpmdevtools `1f3654d08 <https://github.com/fedora-infra/fedora-packages/commit/1f3654d085f9cc7ffec3178bf86ce90f3e384456>`_
- amke sure to correctly rewrite url `833e2d869 <https://github.com/fedora-infra/fedora-packages/commit/833e2d869e70bd6cbcf128d15071cb61c22423c6>`_
- moksha.url wrap a couple of more urls `6a795177e <https://github.com/fedora-infra/fedora-packages/commit/6a795177ed67495f7b0c41c225528c109ad6e5b3>`_
- Set the WSGIApplicationGroup %{GLOBAL} in our mod_wsgi config `3a5a3af22 <https://github.com/fedora-infra/fedora-packages/commit/3a5a3af224ebc480dae61917db3c45a7f51d4115>`_
- Disable the xappy egg-info requirement for now. `8617179fa <https://github.com/fedora-infra/fedora-packages/commit/8617179fa885dc8d0ab02857705d81d33f36dc3f>`_
- Remove a stray print statement `6cf1add7e <https://github.com/fedora-infra/fedora-packages/commit/6cf1add7efde33dc2bff3318e7153e5092c0fdde>`_
- don't parse spec files directly so we don't need to download all packages `d33195f96 <https://github.com/fedora-infra/fedora-packages/commit/d33195f96935b9d0e958a53d8dcfec515b9a3683>`_
- Use moksha.url when loading patches `459ce33b9 <https://github.com/fedora-infra/fedora-packages/commit/459ce33b9ffe3a9a237aa5cadb4a9af0b836d3d9>`_
- Fix our logo link `f1b2b48e5 <https://github.com/fedora-infra/fedora-packages/commit/f1b2b48e5393eeed9717a461b7ca77a09db35247>`_
- Render our Patch widget via /_w/, and fix the arg passing. `c20f86611 <https://github.com/fedora-infra/fedora-packages/commit/c20f866110f0e75dfc0273dcacf6156a67ef2eaf>`_
- Sort our patches by age `d1ca334f9 <https://github.com/fedora-infra/fedora-packages/commit/d1ca334f9abcc7e6a6b3ad9f5f7b1a10cb5c6458>`_
- More improvements to our bugzilla detection regexes `243a9e70b <https://github.com/fedora-infra/fedora-packages/commit/243a9e70b4d9606a4b67fac565f1b6dace215511>`_
- Patch widget usability tweaks. `bd1d6c386 <https://github.com/fedora-infra/fedora-packages/commit/bd1d6c386bf0898f6b7546f941f4e9cfafc2a978>`_
- Minor formatting tweak `2cab55278 <https://github.com/fedora-infra/fedora-packages/commit/2cab552784ee7840f5ee4c5f93148aa97d71e59e>`_
- Fix the url for our list_tree_marker.png `3e4b3d5ec <https://github.com/fedora-infra/fedora-packages/commit/3e4b3d5ecb7d3f907c27abe9a486fc6db8772214>`_
- properly move db files and remove any extranious files `1287961aa <https://github.com/fedora-infra/fedora-packages/commit/1287961aab84a37e54ac07d08d946eaedca8392b>`_
- correctly move icon files `5e59ac53a <https://github.com/fedora-infra/fedora-packages/commit/5e59ac53a061a078fde854877331d25c87cf7a31>`_
- fixups for the indexer when moving files `c9ad97ef8 <https://github.com/fedora-infra/fedora-packages/commit/c9ad97ef82d9401b00a5ea1f29c566c2eaec4c71>`_
- Add a release script to automate spinning up a new release. `b84eb70f8 <https://github.com/fedora-infra/fedora-packages/commit/b84eb70f83f9d865dd461163bcc88e8b35ba241d>`_
- Add a script that can be run on our puppet box to update our dev instance `d1a9e15f0 <https://github.com/fedora-infra/fedora-packages/commit/d1a9e15f0c0f17b9da672486567f3fade2dcc53f>`_
- More bug number detection improvements `a86b12b2a <https://github.com/fedora-infra/fedora-packages/commit/a86b12b2ada635fda868ddd8886a0387081be57a>`_
- Add the bottom border back to our patch widget `621e3df67 <https://github.com/fedora-infra/fedora-packages/commit/621e3df67054c7d1bab388e3b288cf26a96cad37>`_
- We jumped the gun on 0.5.0, go back to a pre-release `a54fb0bc5 <https://github.com/fedora-infra/fedora-packages/commit/a54fb0bc5a9739997f17b5273046f4ca58baffdd>`_
- Fix the resource injection in our Updates widget `ba710fce7 <https://github.com/fedora-infra/fedora-packages/commit/ba710fce797e1917b96e9ba5e91181392923b9ce>`_
- Fix the resource injection in our bug widget `5a951a9fe <https://github.com/fedora-infra/fedora-packages/commit/5a951a9fee43e229b74ec4d69533f74ad5f51bdc>`_
- only copy name to link if link doesn't exist yet `458795e74 <https://github.com/fedora-infra/fedora-packages/commit/458795e745fa338ccabf1e623f26f48bea8886cd>`_
- initial port of the relationship tabs to yum instead of koji `e97737608 <https://github.com/fedora-infra/fedora-packages/commit/e977376084f6ad9d84b58ffb0c4035ad4f40a837>`_
- make sure rawhide and rawhide-source are enabled for the indexer `098d305bd <https://github.com/fedora-infra/fedora-packages/commit/098d305bdfcf3c7b3b10ebafc29fa5d5b64f143b>`_
- First pass at some basic jQuery optimizations of our bodhi.js `f2a7bf682 <https://github.com/fedora-infra/fedora-packages/commit/f2a7bf6824dead5b2b1b0328e1c9c4e346b83522>`_
- fix up some of the relationship stuff in the yum connector `968cfe560 <https://github.com/fedora-infra/fedora-packages/commit/968cfe5604a5e81d80ecec7dfdc5f358b6cbdfce>`_
- move builds and updates to top level nav `8790e79c6 <https://github.com/fedora-infra/fedora-packages/commit/8790e79c6d2f5e5817ed9d229d9fddc3395023ef>`_
- fix getting -testing data and the links to the yum mirror lists `ba4156a2a <https://github.com/fedora-infra/fedora-packages/commit/ba4156a2aa67614d827b1416ff66290a4f166774>`_
- create file tree from yum data `f0bec66cb <https://github.com/fedora-infra/fedora-packages/commit/f0bec66cb4964b5f42002f900e2e7f649959d7be>`_
- hook up file tree viewer to use the yum connector `5a8494c6d <https://github.com/fedora-infra/fedora-packages/commit/5a8494c6d9476378a95baabbd331ae0a94dd1ee9>`_
- some packages don't output a main package so use the source package info `16184f62d <https://github.com/fedora-infra/fedora-packages/commit/16184f62d609c20b44b3cd387bf88603b03952ef>`_
- Fix a bug in the bugs widget template `1849167cd <https://github.com/fedora-infra/fedora-packages/commit/1849167cd63abb7a7f6a27c0afb69563a8d409c9>`_
- tg.url the package link for sub packages `3846c7f7e <https://github.com/fedora-infra/fedora-packages/commit/3846c7f7ebc2d65333085959c07f5a13ad09298a>`_
- Remove the old bodhi.js and get the archive_tw2_resources for bodhi.js working again[:wq `59c6d3242 <https://github.com/fedora-infra/fedora-packages/commit/59c6d3242fdf03d0f4e2d509b41e23b995c3db53>`_
- Remove some unnecessary fonts that were clogging up the tubes `97d4209a8 <https://github.com/fedora-infra/fedora-packages/commit/97d4209a82a32a77d7d11aa672165b4b33304445>`_
- Add a new bulletproof @font-face syntax from http://www.fontspring.com/blog/the-new-bulletproof-font-face-syntax `3892a09da <https://github.com/fedora-infra/fedora-packages/commit/3892a09dacdcf7f91bde290702333b309bea1d38>`_
- There is no widget to render in our invalid_path template `9fb59e52b <https://github.com/fedora-infra/fedora-packages/commit/9fb59e52b972c7acda6cadebf85515004b7211fa>`_
- Disable some duplicate global resources that are getting pulled in `5b774b3c5 <https://github.com/fedora-infra/fedora-packages/commit/5b774b3c54fecbf6c1750d76762f47a94338a27b>`_
- add arch support to the yum connector and config `849e53129 <https://github.com/fedora-infra/fedora-packages/commit/849e53129e0ec209582d774807afac89cc900847>`_
- source repo doesn't have an arch `53f9a146e <https://github.com/fedora-infra/fedora-packages/commit/53f9a146ed34e741cf1401b7c78cc7dfd1274f2c>`_
- avoid initial search load if no search term was given `2997388db <https://github.com/fedora-infra/fedora-packages/commit/2997388dbee8fd232b30208d4f2ef04fd22a10ad>`_
- pass a subpackage_of parameter in the kwd param to child widgets `e94ae96d1 <https://github.com/fedora-infra/fedora-packages/commit/e94ae96d19950667c1cd1ceb2ffdf9cb8dfb4350>`_
- fix builds to handle subpackages `47b3d2121 <https://github.com/fedora-infra/fedora-packages/commit/47b3d212198ad9b2a3121c53451989adcd3e9508>`_
- fix updates to work with subpackages `6c9a7f1a8 <https://github.com/fedora-infra/fedora-packages/commit/6c9a7f1a84958f5ab83f998942a827d3b4c4d42f>`_
- fix content to understand subpackages `3e820cb04 <https://github.com/fedora-infra/fedora-packages/commit/3e820cb04e656fa0c750359c9e913995c1c18f16>`_
- fix Changelog to handle subpackages `a17edbabf <https://github.com/fedora-infra/fedora-packages/commit/a17edbabf95d591312e247046e62d579abbab303>`_
- fixed Bugs to understand subpackages `5539981b8 <https://github.com/fedora-infra/fedora-packages/commit/5539981b81941b34ff11d3d48c289eb4c542ffde>`_
- initially hide pagers and info controls `bb958092c <https://github.com/fedora-infra/fedora-packages/commit/bb958092cab871b04c1cc4a786d57030a28202ec>`_
- use empty string instead of None to mark package as main package `a65d28af2 <https://github.com/fedora-infra/fedora-packages/commit/a65d28af21570d4a54b487fa388441c4899d13cc>`_
- integrate tagger into indexer `08d65c287 <https://github.com/fedora-infra/fedora-packages/commit/08d65c2874c4fd4289d3218115deb6b7506aab8c>`_
- fix typo in indexer `92383a925 <https://github.com/fedora-infra/fedora-packages/commit/92383a925edf13f2728f7482342802f5285631e1>`_
- Pull the repeater.png into our own repo `983380339 <https://github.com/fedora-infra/fedora-packages/commit/983380339aef0578e55c26733d00402c27dcd796>`_
- Add python-bunch to our BuildRequires `c76df46ca <https://github.com/fedora-infra/fedora-packages/commit/c76df46ca30ffa8ba06ac1621cde583fe7d23d9f>`_
- add switches to specify various base urls for koji and pkgdb `0b9f33219 <https://github.com/fedora-infra/fedora-packages/commit/0b9f33219bbd0ce19bee567fb2fce9ad50ce3361>`_
- correctly pass base urls `2bf33ab0e <https://github.com/fedora-infra/fedora-packages/commit/2bf33ab0e449a8255fca631a60254f55b06aa00c>`_
- change wording for obsoletes grid message `8e54fded6 <https://github.com/fedora-infra/fedora-packages/commit/8e54fded6582fae6fca96a4d6d0d2acd2f5e8f0e>`_
- add the provided by column for Requires relationships `1173a993f <https://github.com/fedora-infra/fedora-packages/commit/1173a993f4fa5c0fb4c0aabb1d0fa68d2ee67b88>`_
- fixing the spacing issues and html issues on the overview page. there was an unclosed p tag and a stray close div tag. also fixed some css errors that got introduced somehow. overview looking a lot better now. `222dbe235 <https://github.com/fedora-infra/fedora-packages/commit/222dbe235bde4f8c8c87dd65a7282a38182e910c>`_
- Merge branch 'fedora-packages' of ssh://git.fedorahosted.org/git/fedoracommunity into fedora-packages `63ff27ef4 <https://github.com/fedora-infra/fedora-packages/commit/63ff27ef4fb62e1e750e03a7ebc4722b92de94f6>`_
- fix sources widgets to handle subpackages `1e5683cb4 <https://github.com/fedora-infra/fedora-packages/commit/1e5683cb4fd6c1d313abea8b02af75b8268ccb2e>`_
- update the changelog info display to the new javascript templating format `995caab44 <https://github.com/fedora-infra/fedora-packages/commit/995caab44099d775a9b7e4860fd826200f953fd3>`_
- use tg.url where needed `388a028eb <https://github.com/fedora-infra/fedora-packages/commit/388a028eb6009ff1754083d0f93a6426ae9febb1>`_
- render the details as html so it isn't escaped `4b4fcb43c <https://github.com/fedora-infra/fedora-packages/commit/4b4fcb43c87452a4cdb47a55db7a131e10244ca9>`_
- enable x86_64 repo if looking for noarch packages `6d21dd298 <https://github.com/fedora-infra/fedora-packages/commit/6d21dd298ac43f7978672974bad4e86b285d465c>`_
- add quotes to the arch string `4323eec55 <https://github.com/fedora-infra/fedora-packages/commit/4323eec550ce1facebd5147fc0fdb916bb185b7c>`_
- fix loading of resources for updates widget `190bd55c3 <https://github.com/fedora-infra/fedora-packages/commit/190bd55c34018c5cb7d233ae8a7a73cde08988b2>`_
- clean up main templates `e3483f992 <https://github.com/fedora-infra/fedora-packages/commit/e3483f9924146ed4e678f08f2cff0559d9e94d93>`_
- remove more flash messages `99b03b18b <https://github.com/fedora-infra/fedora-packages/commit/99b03b18b04c0e5384cddeae4ffe8a13c6520294>`_
- better weighting for name `cc9fc986b <https://github.com/fedora-infra/fedora-packages/commit/cc9fc986ba2b98f153735f67d1cc2a69ef5336e1>`_
- add spell checking to queries based on package name and tags `88437f3a4 <https://github.com/fedora-infra/fedora-packages/commit/88437f3a49f12a323a88a23c8f807427c181b2e8>`_
- encode tags as utf-8 `dc5265110 <https://github.com/fedora-infra/fedora-packages/commit/dc5265110df763003243efb29cc89491bb0b0f12>`_
- various search and indexing fixes `86e3a6c9f <https://github.com/fedora-infra/fedora-packages/commit/86e3a6c9f0def73fb8bee4b9dec76d53a1e58985>`_
- Disable tarballs until we can get it working in production `492dde952 <https://github.com/fedora-infra/fedora-packages/commit/492dde952363d8322cac8d5186f13217f46e06b3>`_
- handle icons which already have a .png appended `58a95ac01 <https://github.com/fedora-infra/fedora-packages/commit/58a95ac01150cf2cea9ebeb4a7ab918b12a9f69a>`_
- weight summary * 4 `a5a59e31f <https://github.com/fedora-infra/fedora-packages/commit/a5a59e31f27d7d4759c4377b4e2f66ba8dc7d809>`_
- if viewing subpkg display its icon if it has one `3b0d4c0ea <https://github.com/fedora-infra/fedora-packages/commit/3b0d4c0ead7d1a7c3f639703ee729ba82fccb1a5>`_
- use subpkg icon if main package doesn't have one `7a544741c <https://github.com/fedora-infra/fedora-packages/commit/7a544741ccc5cef39b26e974f9b6d4b19f1f8954>`_
- package_name is in the kwds param not an attr of the widget `27bcbc9c1 <https://github.com/fedora-infra/fedora-packages/commit/27bcbc9c12b9418e331fff37874956ff4890dde9>`_
- improved error message `23dbaa75e <https://github.com/fedora-infra/fedora-packages/commit/23dbaa75ec387891399ac91f522d2bc9ad8da1b8>`_
- remove invalid code `cb21ee8bf <https://github.com/fedora-infra/fedora-packages/commit/cb21ee8bf097210509fea921861472cb36cf9322>`_
- Handle cases where subpackage_of isn't passed in `4e0c4425e <https://github.com/fedora-infra/fedora-packages/commit/4e0c4425efc05b078bff1482e163ccaca2fe92a2>`_
- Add a shiny new error page with graphics from mizmo. `cf8510280 <https://github.com/fedora-infra/fedora-packages/commit/cf8510280a3f7eacea98b7171e21e9c2dbe3baab>`_
- make search work with browsers that don't support JavaScript `aeecbeece <https://github.com/fedora-infra/fedora-packages/commit/aeecbeece84786bf7d5ad1f84b4688e4bdb2636c>`_
- check for error and return it `2e205c2c5 <https://github.com/fedora-infra/fedora-packages/commit/2e205c2c5859b8ec437e444fa3fc4089a82915ce>`_
- Merge branch 'fedora-packages' of git+ssh://git.fedorahosted.org/git/fedoracommunity into fedora-packages `42f07fffc <https://github.com/fedora-infra/fedora-packages/commit/42f07fffcbdaf0b26f303642ce3d46638b918ce5>`_
- New panda image from mizmo! `57a94c0f3 <https://github.com/fedora-infra/fedora-packages/commit/57a94c0f3f43a82c65247891afc949a601843576>`_
- if there is no 'provided by' data don't error out `86abbf53e <https://github.com/fedora-infra/fedora-packages/commit/86abbf53e87db221e02dfe87f9d4100d017e5708>`_
- paginate provides `d6601afad <https://github.com/fedora-infra/fedora-packages/commit/d6601afad0d5650bbd4a2f9fe35192a558caaf9a>`_
- Add an RPMSpec Pygments Lexer from Steve Milner `8ed03f81c <https://github.com/fedora-infra/fedora-packages/commit/8ed03f81ca443a83c40f60242d743abed39cab6c>`_
- add required by tab in relationships `c0ce4533c <https://github.com/fedora-infra/fedora-packages/commit/c0ce4533c1bce2a45b817d16892c212a2b41d625>`_
- a bit more bling to the error page `aa274bddb <https://github.com/fedora-infra/fedora-packages/commit/aa274bddb6820aaca9dd0cd20a3d9699b6ded7b5>`_
- Merge branch 'fedora-packages' of ssh://git.fedorahosted.org/git/fedoracommunity into fedora-packages `6e53e9161 <https://github.com/fedora-infra/fedora-packages/commit/6e53e916109d2cc3979e5939cafb72c027ebb609>`_
- allow spaces in tab names by converting key spaces to underscore `11a2c9802 <https://github.com/fedora-infra/fedora-packages/commit/11a2c980224ef2c7ef5b85c4c7869bb0b4a1a20e>`_
- Merge branch 'fedora-packages' of ssh://git.fedorahosted.org/git/fedoracommunity into fedora-packages `46700d36d <https://github.com/fedora-infra/fedora-packages/commit/46700d36d5eee60c9989b11c73de2ff12583b0d6>`_
- whoops, removing static link, making properly relative `ee6acaf1a <https://github.com/fedora-infra/fedora-packages/commit/ee6acaf1a0b25086e770315d861d178a8c306b40>`_
- attach entire search string as a phrase `bc33296d0 <https://github.com/fedora-infra/fedora-packages/commit/bc33296d017499f5063e77bcb093a26c12523e34>`_
- use near phrase searching also `48209a375 <https://github.com/fedora-infra/fedora-packages/commit/48209a375aa2e697c90c396f62c380b891137a7e>`_
- check if return is a dict before checking for the error attr `78519afc2 <https://github.com/fedora-infra/fedora-packages/commit/78519afc2adbfbe389b81d700acf36bf26fc75fe>`_
- do a more specific search when trying to get an exact package `7ea74eb63 <https://github.com/fedora-infra/fedora-packages/commit/7ea74eb63bf9c3aaff2d15176930d50f027828a4>`_
- Fix a typo `42675e42e <https://github.com/fedora-infra/fedora-packages/commit/42675e42e5596caeb5d9296061cfc8348ab3b76a>`_
- filter out non packages that we are not processing in the count `7145d5290 <https://github.com/fedora-infra/fedora-packages/commit/7145d5290ede2f3e591f732ff800cc17d5b48c60>`_
- Update to a newer jquery.expander.js `f612a0bda <https://github.com/fedora-infra/fedora-packages/commit/f612a0bda69a619e9c697165548a7a111a66d3d6>`_
- Fix a bug with our expander and the new jquery.tmpl.js `bb1dd7776 <https://github.com/fedora-infra/fedora-packages/commit/bb1dd77762df940506f2de09300511bfdbf2c025>`_
- Pull in the expander_js from our updates widget `b7040bfdd <https://github.com/fedora-infra/fedora-packages/commit/b7040bfddb5b67c6009356bb8439d0fd9d53ce96>`_
- Fix our arrow image URLs `7e6125446 <https://github.com/fedora-infra/fedora-packages/commit/7e612544650ea89007350c43373e36a8d8b616b3>`_
- Added parallax effects to error page `7616ed365 <https://github.com/fedora-infra/fedora-packages/commit/7616ed3657960c909503d40ac585bde0dc91c6d1>`_
- Fix our bodhi URLs in the active releases widget. `cd98aec07 <https://github.com/fedora-infra/fedora-packages/commit/cd98aec075df748a6caabf451b6bdc40acf6b4c7>`_
- Actually fix the bug this time `90a84411f <https://github.com/fedora-infra/fedora-packages/commit/90a84411f1406e18edc3e7fef070dea62e7b6f6a>`_
- display multiple 'provided by' packages if they exist `0c59802ff <https://github.com/fedora-infra/fedora-packages/commit/0c59802ff3c3a7d1e4ac010d3a7f00f13bc5649f>`_
- use the json_data plugin instead of html_data fixes jsTree rendering `4be528077 <https://github.com/fedora-infra/fedora-packages/commit/4be528077acbceb228a4b1344d9cd2530075f8b9>`_
- don't error out on empty search strings `040f775de <https://github.com/fedora-infra/fedora-packages/commit/040f775de2bbb062e8aacb5f0ae4c2e71d6c3562>`_
- Use tw2 to inject jQuery instead of doing it manually on our error page `31497f8af <https://github.com/fedora-infra/fedora-packages/commit/31497f8af44db444c5a16a5ae93e4666bf68f4fa>`_
- Make our error page work when being hit directly `a73b6abeb <https://github.com/fedora-infra/fedora-packages/commit/a73b6abeb72cddde1500397003646f540da1524b>`_
- Don't trigger a traceback for invalid packages `e8c2b7249 <https://github.com/fedora-infra/fedora-packages/commit/e8c2b724943158aedc3ed4f061418cb2139d7c80>`_
- Add a script that keeps our git repos up to date `f3e71413b <https://github.com/fedora-infra/fedora-packages/commit/f3e71413bd38e749ac532090b6413ec0aa4b036d>`_
- Set widget defaults for summary and latest_build to fix a Traceback `087c67893 <https://github.com/fedora-infra/fedora-packages/commit/087c678931bbc705072d7d23697ee8b4bb790b13>`_
- If we don't find an exact match and there are no subpkgs: error `37bc8210c <https://github.com/fedora-infra/fedora-packages/commit/37bc8210c45c1e50ab98bd1f8f197ae135c170c2>`_
- Some unused module cleanups `669ab45ee <https://github.com/fedora-infra/fedora-packages/commit/669ab45eea147fbcb3b88a7230d3b80de77edbc3>`_
- Add a PackageWidget.__repr__ `385cb6745 <https://github.com/fedora-infra/fedora-packages/commit/385cb6745824fae93f13214b8a3d2b9d41a21ea9>`_
- Move update-git-repos to production/ `149d27c84 <https://github.com/fedora-infra/fedora-packages/commit/149d27c840b8e153a226d261f761314d2d384b7b>`_
- Explicitly define the variables we're using in our Details widget template `cf8411c6b <https://github.com/fedora-infra/fedora-packages/commit/cf8411c6b61c0ec1affc991a77382b6ec96f0c94>`_
- Improved handling of unknown packages. `5de44c0d0 <https://github.com/fedora-infra/fedora-packages/commit/5de44c0d087e783eeccc2841a79cf2435a35ef26>`_
- Remove a stray semicolon `2bfa2e243 <https://github.com/fedora-infra/fedora-packages/commit/2bfa2e2432051e3f417ea118d33dc5672dec061f>`_
- Only 'git pull' repos that have had koji builds since our last run. `2b0777893 <https://github.com/fedora-infra/fedora-packages/commit/2b0777893c066ec7f3cbfb2150564ada2fca5172>`_
- Fix our koji.listBuilds queryOpts `4b3f08e6e <https://github.com/fedora-infra/fedora-packages/commit/4b3f08e6e34b6bddede3b469eedb735470eef530>`_
- Have our error page use javascript to actually 'Go Back' `472f88a4f <https://github.com/fedora-infra/fedora-packages/commit/472f88a4f410092509a2d9a853ac84bd12c83502>`_
- Require svn for fedcomm to setup. `11f503c2f <https://github.com/fedora-infra/fedora-packages/commit/11f503c2f141bb878b293a11db6a755c2f4acba1>`_
- Ignore paster.pid.  Its created by "fcomm-ctl.py start" `67b0c8f9b <https://github.com/fedora-infra/fedora-packages/commit/67b0c8f9b449ef6e4422683f5a88c5a072665c65>`_
- Work with packages that don't have a URL in their spec (like autofs). `9145a67c7 <https://github.com/fedora-infra/fedora-packages/commit/9145a67c7427b41cef8f0c4518d2f39fc91d08b3>`_
- The Great Connector API Migration of 2012 `54d493bd3 <https://github.com/fedora-infra/fedora-packages/commit/54d493bd39f7a3f4f5f23fa7e96d15bbff80eaf2>`_
- Hack for tests on python2.7 `56479f1d7 <https://github.com/fedora-infra/fedora-packages/commit/56479f1d7ac2e4425bb8dfe4dad70d011f2c7148>`_
- Ignoring icons directory. `99266eae0 <https://github.com/fedora-infra/fedora-packages/commit/99266eae0e2da29cb522744d84f1251b4722ea85>`_
- Moved connector API docs from moksha to fedoracommunity. `d50b2c60d <https://github.com/fedora-infra/fedora-packages/commit/d50b2c60d35adab115775a14edd6debfcedd7cd3>`_
- Moved moksha.widgets.jquery_template to fedoracommunity. `317d56cce <https://github.com/fedora-infra/fedora-packages/commit/317d56ccefebab253613e39fcfa705963c2cdf74>`_
- Fix a race-condition in our patch viewer widget (#384) `130221512 <https://github.com/fedora-infra/fedora-packages/commit/130221512ef893d219811a6fa562dc459b781f04>`_
- Rename to fedora-packages and bump to 2.0 `f4f2a2de1 <https://github.com/fedora-infra/fedora-packages/commit/f4f2a2de1db50bcc36d1fd88a0a5a04e1ed5058c>`_
- Rename our RPM to fedora-packages and bump version to 2.0 `8f90d167c <https://github.com/fedora-infra/fedora-packages/commit/8f90d167ca9f8a020ee3f3d7f7a74169b42f884f>`_
- python-tw2-jquery-ui was renamed to python-tw2-jqplugins-ui `b75a8df45 <https://github.com/fedora-infra/fedora-packages/commit/b75a8df450b48f18a0fdbda6d2ccce309bfb9227>`_
- First stab at porting the last of the tw1 widgets. `3929d30ac <https://github.com/fedora-infra/fedora-packages/commit/3929d30acc771577906a09fe4f46a3f6917e449b>`_
- Merge branch 'connector-migrate' into tw2-all-in `4b3a39555 <https://github.com/fedora-infra/fedora-packages/commit/4b3a395554dd47c7c0238dd8785c671d30d1d7fb>`_
- Fix regression in mokshagrid. `38e8e00d4 <https://github.com/fedora-infra/fedora-packages/commit/38e8e00d44bb67be6c538fa31249e19aecb4734c>`_
- Make the script_name configurable, for tw2 `cb87c2a9e <https://github.com/fedora-infra/fedora-packages/commit/cb87c2a9e180ecd6d783580c2314a902c6def921>`_
- Latest update to work against moksha>=0.8.0 `0346f890c <https://github.com/fedora-infra/fedora-packages/commit/0346f890c0d6ba61f2658fd7f8f3f9ab2acfdb5f>`_
- Need repoze.tm during rebuild. `02b559478 <https://github.com/fedora-infra/fedora-packages/commit/02b559478276688294d37ccd317a75633b0d8c03>`_
- Fix to Koji Connector; use local request instead of pylons global. `7bc962614 <https://github.com/fedora-infra/fedora-packages/commit/7bc9626140b7f285e582bb80d977323db3ff9425>`_
- Avoid using tg.url in our bodhi connector `a991c65a0 <https://github.com/fedora-infra/fedora-packages/commit/a991c65a0bf0536e3bf9010a36427b7ea84acc4d>`_
- Grab the beaker cache from the environ, instead of using pylons.cache `9e777d1d3 <https://github.com/fedora-infra/fedora-packages/commit/9e777d1d359ed2d62c742e20a7f87e3db24d1b54>`_
- The new Bugzilla apparently doesn't let us specify the order `97228f995 <https://github.com/fedora-infra/fedora-packages/commit/97228f9959243ac11199368f3da5856c73da9e5b>`_
- Add sqlalchemy>=0.6 to our __requires__ hack `adfbad35f <https://github.com/fedora-infra/fedora-packages/commit/adfbad35f62f85e06e537571d7ba18c009493f01>`_
- Remove all pylons.cache usage from our connectors. `7a02941c4 <https://github.com/fedora-infra/fedora-packages/commit/7a02941c46cb9cce5ad2247bcf43213df0ffcdbe>`_
- Manually put some TW2 resources in the proper places, to work around some bugs. `86a7a0ba8 <https://github.com/fedora-infra/fedora-packages/commit/86a7a0ba80378b79861e6955381bb7f33a356a2c>`_
- Merge branch 'tw2-all-in' into fedora-packages `bf53943d6 <https://github.com/fedora-infra/fedora-packages/commit/bf53943d6c027b0dc7b3e3b6f923c731eb2856a1>`_
- The torrent connector actually needs tg.config. `45fc196b6 <https://github.com/fedora-infra/fedora-packages/commit/45fc196b6040a149124243329a2584f61da7b5b1>`_
- Strip out duplicate resources when loading patches `ee1e3ffc7 <https://github.com/fedora-infra/fedora-packages/commit/ee1e3ffc77cac86d44eb314fc29aeabbe97eae96>`_
- We don't need repoze.tm `0a16f1bd9 <https://github.com/fedora-infra/fedora-packages/commit/0a16f1bd98a18425dfa3309a121a201effe8c49c>`_
- Multicall support is broken after the latest Bugzilla upgrade `a09789d63 <https://github.com/fedora-infra/fedora-packages/commit/a09789d639c1369230b5537fac52a8c76dd80cab>`_
- Singleton for self._bugzilla. `137680e66 <https://github.com/fedora-infra/fedora-packages/commit/137680e66858f93bc24eb0c37607ace0f919a5cd>`_
- Workaround to handle querying tons of bugs. `ba8c7867b <https://github.com/fedora-infra/fedora-packages/commit/ba8c7867bcfb10f70bf47a0cb611dc2eaeacdf4d>`_
- Show bugs in other states.  #382, #317, #381 `201c7912f <https://github.com/fedora-infra/fedora-packages/commit/201c7912f9f8f425caf879134da9f6bf0746009a>`_
- Allow the "n new this week" bug info to link through to bugzilla.  For ticket #382 `2013d74d8 <https://github.com/fedora-infra/fedora-packages/commit/2013d74d87e4970dcf1a03c3c30309a6def9ea75>`_
- Separate buttons for reporting new Fedora and Fedora EPEL bugs.  #381. `b2269e37d <https://github.com/fedora-infra/fedora-packages/commit/b2269e37d8b7956f88b4fa6c20dd67c3c85294b1>`_
- Add an "all" option for bug reports. `8f8847052 <https://github.com/fedora-infra/fedora-packages/commit/8f8847052c2b57d191bad5c92005f432baf6d8f3>`_
- Support for the {package}/bugs/all path.  Fixes #390. `ef6af5a75 <https://github.com/fedora-infra/fedora-packages/commit/ef6af5a753f7b124f3829014ec88c77a7b92eb6a>`_
- Match up braces to cut down on log spam. `614131d2c <https://github.com/fedora-infra/fedora-packages/commit/614131d2c61bc120876e36ed496505594d0e8fd5>`_
- .gitignore some more products of running in development. `68075eb03 <https://github.com/fedora-infra/fedora-packages/commit/68075eb03ad410aad2624a8600771df6414909d5>`_
- Sort bugs like pkgdb do. `baa9bea56 <https://github.com/fedora-infra/fedora-packages/commit/baa9bea569785fbc25cdf591d83893def5ef5107>`_
- No more ass match.  Fixes #393. `863362a47 <https://github.com/fedora-infra/fedora-packages/commit/863362a477aeed32af5f3cdc4bd14a20120b2437>`_
- Gracefully handle dumb calls to our API (stop the flood of emails). `04741309e <https://github.com/fedora-infra/fedora-packages/commit/04741309e1f66beb6a991c26d3b217ce4e815ad4>`_
- Gracefully handle packages with no Rawhide build (stop the flood of emails). `276920193 <https://github.com/fedora-infra/fedora-packages/commit/276920193531472a07e137eb6111e7968c245599>`_
- Added myself to the AUTHORS file. `4b9d8a851 <https://github.com/fedora-infra/fedora-packages/commit/4b9d8a8519f7b6e6435b02779c953eedd9889217>`_
- Typo fix. `b9c3122e9 <https://github.com/fedora-infra/fedora-packages/commit/b9c3122e945e6dafab8a1a83f09269a6a1434012>`_
- Version bump:  2.0.1-1 `bc917ef82 <https://github.com/fedora-infra/fedora-packages/commit/bc917ef82e15268210f89cdcfea144de7c4085fc>`_
- Version bump for being.. not-a-ninja. `03c4043fd <https://github.com/fedora-infra/fedora-packages/commit/03c4043fd1c409c0a7f11226d82a9405c4c9f2a3>`_
- Replaced README with a link to the wiki page on development. `bce58f99c <https://github.com/fedora-infra/fedora-packages/commit/bce58f99c93cc028f2e16931784638199dbad02f>`_
- Port forward to using moksha >= 1.0.0 `32610fd9b <https://github.com/fedora-infra/fedora-packages/commit/32610fd9bbbb93a69f0a2c783a8719dc4f486afe>`_
- Use HTML5 autofocus to select search input on page load.  Issue #398. `acf58de82 <https://github.com/fedora-infra/fedora-packages/commit/acf58de825e5fd186ce97b66ff42a4c12ecd982d>`_
- Better searching. `6739f34f1 <https://github.com/fedora-infra/fedora-packages/commit/6739f34f17f766c7c950eb5541bf3c10b2d85c99>`_
- Fix tw2 resource archival. `f54e3dc62 <https://github.com/fedora-infra/fedora-packages/commit/f54e3dc62a298f16bbe960c2dd97548cfae3dd72>`_
- 2.0.3 `94cabfd82 <https://github.com/fedora-infra/fedora-packages/commit/94cabfd82604709494fe7ad9b7b6c0eee81e525c>`_
- Query for more bug status types when searching for "Open" bugs `81bf33703 <https://github.com/fedora-infra/fedora-packages/commit/81bf33703299645d8d05ff887da03a8be0ce3dce>`_
- Add our fcomm-dev-update script `6ec8ef93d <https://github.com/fedora-infra/fedora-packages/commit/6ec8ef93d2e95bb2a20c707dfb3033d23d290ccd>`_
- Organize our production helper scripts `572369555 <https://github.com/fedora-infra/fedora-packages/commit/57236955566dc0753806ad8d761c2f4746004fbc>`_
- Remove the fedora-announce-to-rss code & xml `6fc36adfe <https://github.com/fedora-infra/fedora-packages/commit/6fc36adfe8f336bf60b4c2e6a17b1943106bb796>`_
- We no longer require SQLAlchemy `57a7f8a4c <https://github.com/fedora-infra/fedora-packages/commit/57a7f8a4c33034ec63adfdbe0bf6d3ba403025cc>`_
- Change the WSGIScriptAlias to /packages `09b484b18 <https://github.com/fedora-infra/fedora-packages/commit/09b484b18f97eff89a3c90fd9f41fdf5d688359b>`_
- Add a new bootstrappings tool. `b27679bf3 <https://github.com/fedora-infra/fedora-packages/commit/b27679bf37707a08969e3c6f8d63e901284b8bd2>`_
- Install wget from our bootstrap.py `48f253310 <https://github.com/fedora-infra/fedora-packages/commit/48f2533108e63e1d760a60e6436da8ccb0cd77e6>`_
- Install TurboGears2 `b5edd46aa <https://github.com/fedora-infra/fedora-packages/commit/b5edd46aa2c23bc018bc13ec5775cce418288770>`_
- Remove trailing slash from snapshot url `b98600ce8 <https://github.com/fedora-infra/fedora-packages/commit/b98600ce824bddbaf426fe56a23cc7e85d6eaa5d>`_
- Link to profile of owner `d897e585e <https://github.com/fedora-infra/fedora-packages/commit/d897e585ef85af167b39396cc6e062121d39e6e2>`_
- For package -maint owners, link to the pkgdb package profile `3cdefeda0 <https://github.com/fedora-infra/fedora-packages/commit/3cdefeda0e244a31bb20a529656c9a4bbcea0882>`_
- Fix link to bodhi update from updates table. `084fa53ec <https://github.com/fedora-infra/fedora-packages/commit/084fa53ec423c200d403a432e5d3c03434f40f41>`_
- Add a link to the fedorahosted trac from the footer. `0d140e1ff <https://github.com/fedora-infra/fedora-packages/commit/0d140e1ff90f2df780de72df634b606a33c30a99>`_
- In Other Apps `902ec17fd <https://github.com/fedora-infra/fedora-packages/commit/902ec17fd7340d28bd382715a9bd7676376b555b>`_
- Fixup bz and pkgdb links. `a4bfea26a <https://github.com/fedora-infra/fedora-packages/commit/a4bfea26af0313f4b711a8675ffaca26c9c6e171>`_
- Tweaks to get stuff working on TG-2.3. `e8f114378 <https://github.com/fedora-infra/fedora-packages/commit/e8f114378c051405941d3f775afb122e34803a5b>`_
- Remove the total new and closed bug stats `cce4aa8eb <https://github.com/fedora-infra/fedora-packages/commit/cce4aa8ebaf85328eb35f7e4dd6b8343a2777ed3>`_
- Query bug stats for EPEL as well `753b80b84 <https://github.com/fedora-infra/fedora-packages/commit/753b80b84217eaab482da730404764d67d0edd09>`_
- In Other Apps changes `17cb5a8aa <https://github.com/fedora-infra/fedora-packages/commit/17cb5a8aa51a749ad121176ecf9f2e1b2566321f>`_
- Owner links styling `0b8f0b05d <https://github.com/fedora-infra/fedora-packages/commit/0b8f0b05d39d65fbbbe6f61d8ca80d6434f56d6f>`_
- Force the css resources to be injected in particular order. `888b7b81c <https://github.com/fedora-infra/fedora-packages/commit/888b7b81cae3a3253c123b7842c316599e211ce0>`_
- Fix ordering of css.  Fixes #396 `283c9a376 <https://github.com/fedora-infra/fedora-packages/commit/283c9a37657f52cb6a74eb50a4900325b77f6282>`_
- PEP8 `9d430b61c <https://github.com/fedora-infra/fedora-packages/commit/9d430b61c9c85bcfb229b895f8d723e924b1ed20>`_
- Add a count of Blocking Bugs `0cdfce216 <https://github.com/fedora-infra/fedora-packages/commit/0cdfce21644ca887de821dd05049918e4a509bfe>`_
- Remove some unused params from the bugs widget `d0ccf9b8c <https://github.com/fedora-infra/fedora-packages/commit/d0ccf9b8cd6dc2b7ca0574c2579db5c4fe7b882f>`_
- Use dogpile.cache for bug stats. `33754ebf4 <https://github.com/fedora-infra/fedora-packages/commit/33754ebf4abef872c2db14590bdb576c7ba081b7>`_
- Some simplification to the bugzilla connector. `558ad7ddb <https://github.com/fedora-infra/fedora-packages/commit/558ad7ddb55fb3f3088044cb25d4bf6114db4eb3>`_
- More simplifications of bug_stats. `364f3561f <https://github.com/fedora-infra/fedora-packages/commit/364f3561f1787de6b62a10861ad55299f7ad31fa>`_
- Bugfix to blocker bug cacheing. `105f59a31 <https://github.com/fedora-infra/fedora-packages/commit/105f59a318475969f02c24ca3868fa9e5a659ef2>`_
- Fine-grained cacheing of bug details. `5132b7704 <https://github.com/fedora-infra/fedora-packages/commit/5132b77047f5ccb1798bb901c81cd9aa08ee41be>`_
- Fix indentation error. `84643e61c <https://github.com/fedora-infra/fedora-packages/commit/84643e61c7e5db7893023956a44251f32966dcfe>`_
- Use dogpile.cache in every connector. `5947b3b0f <https://github.com/fedora-infra/fedora-packages/commit/5947b3b0f9390c6a860e306d9c5a61b950da6d5a>`_
- Change name of bugzilla cache config params to match up with the general connector ones. `df7b8e9ab <https://github.com/fedora-infra/fedora-packages/commit/df7b8e9ab663425cd8be38105c5cafd0a0156a62>`_
- Use different dbm backends for different caches. `06d4f82f4 <https://github.com/fedora-infra/fedora-packages/commit/06d4f82f4df666de1e8d735ca39f08fcc00b2827>`_
- Use cache_on_arguments decorator. `59979a740 <https://github.com/fedora-infra/fedora-packages/commit/59979a740d7a11ebd8acb69a99a61cc8706749be>`_
- Use dogpile key_mangler for memcached support. `20b4f24cf <https://github.com/fedora-infra/fedora-packages/commit/20b4f24cf5c112dbab75f7b0f309e3a2bca011e1>`_
- Include example memcached configuration in development.ini. `56a1816eb <https://github.com/fedora-infra/fedora-packages/commit/56a1816eb465359f23be16999c05e68fdce8dbe8>`_
- Added a warning about cacheing in the footer. `4e73b03c4 <https://github.com/fedora-infra/fedora-packages/commit/4e73b03c4c3a9fa1f0316e81022b02725da75d36>`_
- Generate the url to a packages blocker bugs. `6469cdb29 <https://github.com/fedora-infra/fedora-packages/commit/6469cdb2956f4122eb0cfc6b9d9384c3f86f60a2>`_
- Adjust blocking_bug url patch. `ff40020d6 <https://github.com/fedora-infra/fedora-packages/commit/ff40020d6f5e635ad2b3c21503555d6c5f34ce87>`_
- Some reorganization to avoid storing python-bugzilla proxy objects in the cache.  They are unstable when retrieved. `a6b29cbd9 <https://github.com/fedora-infra/fedora-packages/commit/a6b29cbd9730169e57dad79a79755591039384e5>`_
- Indentation (cosmetic) `569cd4e20 <https://github.com/fedora-infra/fedora-packages/commit/569cd4e20dcfefba6c7d13e57acc62f9d29830af>`_
- Hardcode css list in base templates.  No more inconsistencies (I hope). `52995227e <https://github.com/fedora-infra/fedora-packages/commit/52995227e9289686d82ec8b3c1ddecec919b8411>`_
- 2.0.4 `fe90d34e5 <https://github.com/fedora-infra/fedora-packages/commit/fe90d34e52ef3d7e582d1429b2123b43e8109278>`_
- Provide example of the distributed_lock argument to dogpile.cache. `b9d8831c2 <https://github.com/fedora-infra/fedora-packages/commit/b9d8831c26cbd4e72efa41b52e1a7e5584cbff65>`_
- Fix inconsistent dogpile keys due to randomized dict order. `32ba269f8 <https://github.com/fedora-infra/fedora-packages/commit/32ba269f87268f9747fe71152cb7edee3175813a>`_
- Use experimental dogpile background refresh. `c211bc671 <https://github.com/fedora-infra/fedora-packages/commit/c211bc67118db6af2c1ca97d967eb1942783f6d2>`_
- Release bump. `4f2da59ae <https://github.com/fedora-infra/fedora-packages/commit/4f2da59ae21c2e4b95be124ac5aa9cb95d92e5fc>`_
- Correct version for new bug link for Fedora EPEL packages. `eef70e6ba <https://github.com/fedora-infra/fedora-packages/commit/eef70e6ba739ec2c5b63620f71349f113d4cb1f0>`_
- Fix that bonkers SSL timeout with bugzilla. `32c0fb907 <https://github.com/fedora-infra/fedora-packages/commit/32c0fb9075b44e3533e48c07eef13b05413fd57b>`_
- Update to use latest experimental dogpile async stuff. `919e4de15 <https://github.com/fedora-infra/fedora-packages/commit/919e4de1549afe54c2c5369e0f62d7a3ae7cf0fb>`_
- Release bump. `54edb2426 <https://github.com/fedora-infra/fedora-packages/commit/54edb2426f100c09941d25c1adb0e519d74b9e39>`_
- Py2.6 support for the bugzilla SSL hack. `d823e1671 <https://github.com/fedora-infra/fedora-packages/commit/d823e1671f5d4e6a256f8f6ed93a0927a88f15a9>`_
- Release bump. `dc73e3aed <https://github.com/fedora-infra/fedora-packages/commit/dc73e3aed371ffb8cd135ba271e62366f7ac9ff5>`_
- Fix bug where /packages/qt returned a 404. `ad438ffc9 <https://github.com/fedora-infra/fedora-packages/commit/ad438ffc90ac7c1ff1edc354c9930385beb21ca5>`_
- Fix "python-webob1.2" 404 error. `93abf4389 <https://github.com/fedora-infra/fedora-packages/commit/93abf4389078700f3d320bf4111e8efba8e6dc2b>`_
- Redirect to search instead of /error in case of 404 on package name. `4d9c426c6 <https://github.com/fedora-infra/fedora-packages/commit/4d9c426c6ef2131d675740fe4eb3d0ba85087c2d>`_
- Use a more modern hardcoded url at the bottom of search/index.py. `6c5b19417 <https://github.com/fedora-infra/fedora-packages/commit/6c5b19417e677d40de41122860476ec6f8dc685b>`_
- Release bump. `94c2948b6 <https://github.com/fedora-infra/fedora-packages/commit/94c2948b6081788480914b8c6b2800109ab6dfb4>`_
- Fix a pesky spelling error. `525383f9d <https://github.com/fedora-infra/fedora-packages/commit/525383f9d8ac606f8cd15fff365f7b997baabad7>`_
- Disable fancy-patched dogpile stuff until it is generally available. `c7bc19f25 <https://github.com/fedora-infra/fedora-packages/commit/c7bc19f259619a12bc05a30b7d03aaa0839bd022>`_
- Add dogpile to bootstrap.py. `2d4aea06a <https://github.com/fedora-infra/fedora-packages/commit/2d4aea06a8c6bfa6ab17fe9725b5db1b10e0be5b>`_
- dist-rawhide is gone `4fd257a08 <https://github.com/fedora-infra/fedora-packages/commit/4fd257a08655a5651c86d71ab2c14ea8b1398d58>`_
- Make the dogpile caching optional. `bb18eb7b2 <https://github.com/fedora-infra/fedora-packages/commit/bb18eb7b208cf280bbc44115f48f7dd248f05948>`_
- Simplify dogpile cache interfaces. `c897dbc6d <https://github.com/fedora-infra/fedora-packages/commit/c897dbc6d314d9fc44e9d2843d219961404e03d4>`_
- Use python-retask to distribute cache refreshing to a worker proc. `ae6d8c7d4 <https://github.com/fedora-infra/fedora-packages/commit/ae6d8c7d4ca4e60b6034ce11da3744a71c73c16a>`_
- Tweak to get koji connector working. `8c74c4924 <https://github.com/fedora-infra/fedora-packages/commit/8c74c4924ccb473714461f06889c115653e39639>`_
- Tweak to get yum connector working. `5df0c06e8 <https://github.com/fedora-infra/fedora-packages/commit/5df0c06e8d26ec039aca5278e49dbd000ec56ec6>`_
- Specfile updated with new deps. `eb73d9adb <https://github.com/fedora-infra/fedora-packages/commit/eb73d9adbb7cb67abd84117da7478f3eb3654c85>`_
- Merge pull request #1 from fedora-infra/feature/optional-dogpile `462737762 <https://github.com/fedora-infra/fedora-packages/commit/46273776237a2b4745faef1ea9f7ec902eb55e15>`_
- Merge pull request #2 from fedora-infra/feature/long-running-queue `f31795b4f <https://github.com/fedora-infra/fedora-packages/commit/f31795b4fec041606ed69f2bb7fcfeac800fb664>`_
- Half-working daemon setup. `9fe610e5f <https://github.com/fedora-infra/fedora-packages/commit/9fe610e5fa2a9a18a46246cf5d18a574e4badfce>`_
- Better setup for daemon-hood.  pkgdb and bodhi connectors are still broken. `40ff5c37b <https://github.com/fedora-infra/fedora-packages/commit/40ff5c37b64adb5a17cbe6f38b98f27b1cadb1b7>`_
- Tweaks to try and get the daemon to work.  Nothing significant. `a7d2298e3 <https://github.com/fedora-infra/fedora-packages/commit/a7d2298e3e766e7bb15b2d895e8c1604521d2017>`_
- Merge pull request #3 from fedora-infra/feature/worker-as-a-daemon `d5d997dcc <https://github.com/fedora-infra/fedora-packages/commit/d5d997dcc9ee187634a795582abcb48b5b727eab>`_
- Don't install dogpile from fedora just yet.  What we need hasn't hit updates-testing yet. `9134423dd <https://github.com/fedora-infra/fedora-packages/commit/9134423dd9b0c46ac7239dbf2baf0a838b41ee12>`_
- Use updates-testing.  :P `bfba73852 <https://github.com/fedora-infra/fedora-packages/commit/bfba73852f79976b046f1a83a4369c77fc593af9>`_
- Add a link to Fedora Tagger from the package chrome. `b73c67b58 <https://github.com/fedora-infra/fedora-packages/commit/b73c67b58b4827b8037d929e5d96eb188173a6a9>`_
- Call Thread.start(), not run() `b75d37bd3 <https://github.com/fedora-infra/fedora-packages/commit/b75d37bd30acf82ca84c78f4226b1f61617afae5>`_
- Merge branch 'develop' of github.com:fedora-infra/fedora-packages into develop `b85723329 <https://github.com/fedora-infra/fedora-packages/commit/b857233297b5b9098be73a410578a95b761a9053>`_
- Deth to pyCurl! `cdbe2d4f9 <https://github.com/fedora-infra/fedora-packages/commit/cdbe2d4f969fed88d40a05140d17ca9fcc9b27cb>`_
- Fix the raw patch links `75c0e25c9 <https://github.com/fedora-infra/fedora-packages/commit/75c0e25c9bf50e237223fc7ff5a9eae09561b5f4>`_
- Include init script for fcomm-cache-worker. `1e0287cbf <https://github.com/fedora-infra/fedora-packages/commit/1e0287cbfa9987b140dde70ccd89637242a1cdba>`_
- Merge branch 'develop' of github.com:fedora-infra/fedora-packages into develop `552d537c6 <https://github.com/fedora-infra/fedora-packages/commit/552d537c6d7599fecd3c6874c88fcb2f2bbb0e26>`_
- Fix crazy sigterm bug in the cache worker. `6fbfa731f <https://github.com/fedora-infra/fedora-packages/commit/6fbfa731ffd1a5779b11ec54e2eeb4ddcca5751b>`_
- Config for the cache-worker daemon. `e34f9fbb3 <https://github.com/fedora-infra/fedora-packages/commit/e34f9fbb3880c2a77a921e676d027ddc16c56044>`_
- Merge branch 'feature/kill-pycurl' into release/2.0.5 `1ee2cc643 <https://github.com/fedora-infra/fedora-packages/commit/1ee2cc64394245df8e7865486ebb77457dd6bdc1>`_
- Revert "Deth to pyCurl!" `7de233bfd <https://github.com/fedora-infra/fedora-packages/commit/7de233bfdcac73334a537ee0bb305ef98e076bfe>`_
- 2.0.5 with cache daemon craziness. `4527fe20c <https://github.com/fedora-infra/fedora-packages/commit/4527fe20cdc9f119ecda179c09872d4a12dcd596>`_
- Cleanup. `2ea45de61 <https://github.com/fedora-infra/fedora-packages/commit/2ea45de61e2f05ea0cc27e59e93e767eaa13ae02>`_
- Be yet still more conservative with memcached connections in the cache worker daemon. `155e88a12 <https://github.com/fedora-infra/fedora-packages/commit/155e88a1294b39866dd2ea774922552997ae11e1>`_
- 2.0.6 `15e25f045 <https://github.com/fedora-infra/fedora-packages/commit/15e25f045b1c3e45bb292b9a320abf638a29fb52>`_
- Add in python-memcached dependency to bootstrap.py and setup.py `4c57d59dd <https://github.com/fedora-infra/fedora-packages/commit/4c57d59ddc8692f1240ba1cd72592400a0a91ffa>`_
- Merge pull request #7 from daviddavis/develop `bd932195b <https://github.com/fedora-infra/fedora-packages/commit/bd932195b2cc5fc4d91a62ccdc387ac87fa6ce0b>`_
- Link dogpile into our virtualenv `e7861885b <https://github.com/fedora-infra/fedora-packages/commit/e7861885b741be92ba3fe3a7e4792a539ae071b2>`_
- Link memcache into our virtualenv `a7f078d4c <https://github.com/fedora-infra/fedora-packages/commit/a7f078d4c111f6b2f7a4379840e2290be16ac1cf>`_
- we need memcached too `bcd9df12c <https://github.com/fedora-infra/fedora-packages/commit/bcd9df12cbc290bf79dcb6f6c00f10e09a804305>`_
- Get BodhiConnector.query_active_releases working without a WSGI environ (#11) `46c332599 <https://github.com/fedora-infra/fedora-packages/commit/46c33259991608f572d942b6ad0c6b654cabba0a>`_
- Changes to karma image. Adding colors. `6b109068b <https://github.com/fedora-infra/fedora-packages/commit/6b109068b74c58a4cf33f64828fe2ca836ab99d0>`_
- Merge pull request #15 from marijar/karma `d287c7364 <https://github.com/fedora-infra/fedora-packages/commit/d287c73647a188a7e26323a6944ea2066cb74f40>`_
- Support bugzilla-0.8.0 `60f3d6591 <https://github.com/fedora-infra/fedora-packages/commit/60f3d6591e89e2f525bd6fb94a75b01f86933937>`_
- Update the bugzillahacks.py for 0.8.0 `3c4cc9fb0 <https://github.com/fedora-infra/fedora-packages/commit/3c4cc9fb0e8b6947f8078fb528e0a8737a7c5cb6>`_
- Get off of the old moksha.common.lib.helpers stuff. `a8a8662ba <https://github.com/fedora-infra/fedora-packages/commit/a8a8662baa9ac2e883eb8ee53bfc3953a6e78a52>`_
- Don't escape the spec file widget. `ac00f53e6 <https://github.com/fedora-infra/fedora-packages/commit/ac00f53e67bce662b7095ede200bb8c202a99567>`_
- Fix misleading text in bugs widget. `792511fb6 <https://github.com/fedora-infra/fedora-packages/commit/792511fb6ba802b9019ce43b9ae8955ab619b372>`_
- The latest from updates-testing is no longer necessary for development. `dce25ee02 <https://github.com/fedora-infra/fedora-packages/commit/dce25ee02af8a28999aad44d9ac04221996ba638>`_
- Make the redis queue not connect at import time. `59d3763ba <https://github.com/fedora-infra/fedora-packages/commit/59d3763bad6a75f977222488a8cfe44399cf9601>`_
- Turn off memcached stuff by default for development. `55a94cb71 <https://github.com/fedora-infra/fedora-packages/commit/55a94cb7137c33b06f063a6b4f3e9d8a47c4037e>`_
- Merge pull request #17 from fedora-infra/feature/optional-caching-for-development `1c27cd54a <https://github.com/fedora-infra/fedora-packages/commit/1c27cd54aad4a91d96ac76c233f86b210a526e36>`_
- Merge pull request #18 from fedora-infra/feature/no-updates-testing-plz `fd718d5f6 <https://github.com/fedora-infra/fedora-packages/commit/fd718d5f64ca7084bdde17dc38ce17fff921e6b6>`_
- Merge pull request #19 from fedora-infra/feature/fix-bugs-text `9a9910c78 <https://github.com/fedora-infra/fedora-packages/commit/9a9910c78aa32b65a371ff96b0ea29842f658870>`_
- If bug_version is a string, don't truncate it otherwise return the first element only `58452a8e6 <https://github.com/fedora-infra/fedora-packages/commit/58452a8e6156e5341a932e920f3d77ffe10e4fe3>`_
- Merge pull request #23 from fedora-infra/feature/fix_bugs_release `0f1720f3b <https://github.com/fedora-infra/fedora-packages/commit/0f1720f3bef10c68753cca848c599d45d02f4427>`_
- You've got to be kidding me. `1b008dbf4 <https://github.com/fedora-infra/fedora-packages/commit/1b008dbf422f5e9a6a5d463b25e13ed18774f4a9>`_
- 2.0.7-2 `9a09cfa72 <https://github.com/fedora-infra/fedora-packages/commit/9a09cfa72eafe291c9370507eb0b913a476f71b0>`_
- Modernize distmappings. `175ff35bc <https://github.com/fedora-infra/fedora-packages/commit/175ff35bc387a17e731bc50fc1d9c3280eb5908f>`_
- Unescape JSON so the relationships tab (and other things) work. `74fe187ed <https://github.com/fedora-infra/fedora-packages/commit/74fe187ed216bf569f3328c21d3dff4667ee304a>`_
- Ignore version map from cronjob. `d14c44e62 <https://github.com/fedora-infra/fedora-packages/commit/d14c44e6253f0059eba3a8a35396620e809290e6>`_
- Merge pull request #25 from fedora-infra/feature/unescape-that-json `d58c46816 <https://github.com/fedora-infra/fedora-packages/commit/d58c468162f41f1d2dab0be43038b9c7d45e35b9>`_
- Remove error obfuscation. `99a63bb32 <https://github.com/fedora-infra/fedora-packages/commit/99a63bb32b61aa86392880a5c7a7ce5ba238cc9b>`_
- Move exception handling into call_get_file_tree for consistency. `6aea9bb49 <https://github.com/fedora-infra/fedora-packages/commit/6aea9bb49a6eeceb9b96115f79a7a7786f54919e>`_
- Merge pull request #27 from fedora-infra/feature/remove-obfuscation `232681011 <https://github.com/fedora-infra/fedora-packages/commit/232681011bed6cac820487d8ed5633a9c736c888>`_
- Update hotpatch for bugzilla-0.9.0. `ff3ea739e <https://github.com/fedora-infra/fedora-packages/commit/ff3ea739eaa7a511998b57a5caf4e3ee987ea69a>`_
- Karma_level needs to be double nested here in order to work. `e2c878809 <https://github.com/fedora-infra/fedora-packages/commit/e2c87880991bbc33a12272afce0a1a744a5ace9c>`_
- Sometimes latest_builds itself is None. `bba62f8cc <https://github.com/fedora-infra/fedora-packages/commit/bba62f8cc482958503911df8357509dfe0e3de9c>`_
- Merge pull request #30 from fedora-infra/feature/latest-builds-bugfix `039a34dc3 <https://github.com/fedora-infra/fedora-packages/commit/039a34dc3b7c0cde624dc09fd38ef69804e47918>`_
- Merge branch 'feature/double-nesting-craziness' into develop `092e08951 <https://github.com/fedora-infra/fedora-packages/commit/092e08951627075b583232f395c4fb4f0e799ed7>`_
- Protect version comparison against 2.3.0dev `ad2c47f0a <https://github.com/fedora-infra/fedora-packages/commit/ad2c47f0a2e2ce1eeb0534dc4796451d277e8111>`_
- Really disable those request extensions. `6378a8758 <https://github.com/fedora-infra/fedora-packages/commit/6378a87581ae5cbe6f6689260d94f3a4abfb1166>`_
- 2.0.8 `f198fb0e9 <https://github.com/fedora-infra/fedora-packages/commit/f198fb0e9f0bc4229c25e6a350a645eed0633896>`_
- Import old code from python-moksha-wsgi-1.2.0. `ed1e07d71 <https://github.com/fedora-infra/fedora-packages/commit/ed1e07d710da22bfa1ffa38e70506e617694c85b>`_
- 2.0.9 `42e81154b <https://github.com/fedora-infra/fedora-packages/commit/42e81154b316f32cf87b74752ada2eaaa66f2f9d>`_
- make the bz cookiefile location configurable. `b90adc962 <https://github.com/fedora-infra/fedora-packages/commit/b90adc96215c38e152fdffe20aa0f0eeef6a6434>`_
- Merge pull request #32 from fedora-infra/feature/configurable-bz-cookiefile `3081e1f27 <https://github.com/fedora-infra/fedora-packages/commit/3081e1f2704554531bb51fb98a8debd9d3f23027>`_

0.4.3
-----

- The pytz egg-info may not be available for RHEL5 `d95de5551 <https://github.com/fedora-infra/fedora-packages/commit/d95de555118b0f20afc67f518a342550c481200d>`_
- Remove a stray print statement `aff0eb02c <https://github.com/fedora-infra/fedora-packages/commit/aff0eb02cd77870f2bf075e0bc2bae9da2655cc5>`_
- Update our manifest to ensure we pull in all data files `31c7ef194 <https://github.com/fedora-infra/fedora-packages/commit/31c7ef194ec6e85b5cc8f0b817be7bf537d70029>`_
- Merge branch 'master' of git+ssh://git.fedorahosted.org/git/fedoracommunity `dd2863895 <https://github.com/fedora-infra/fedora-packages/commit/dd28638951b390d54c088073cfe27c9b46022af7>`_
- Apply a patch from Brennan Ashton to reflect recent Koji rawhide tag changes. `d734f7e89 <https://github.com/fedora-infra/fedora-packages/commit/d734f7e8956b06ef9bf38cdabda8552a63b186fc>`_
- 0.4.3 version bump `5d60824f3 <https://github.com/fedora-infra/fedora-packages/commit/5d60824f38f6c994170a50817b890dc994d5f13f>`_

0.4.2
-----

- Use the http url for the koji hub. `84d5fcf2c <https://github.com/fedora-infra/fedora-packages/commit/84d5fcf2c8cfe18f4f1b606934a5fb81e54f822e>`_
- Fix our usage of the new WebHelpers API `f5b8611e7 <https://github.com/fedora-infra/fedora-packages/commit/f5b8611e785fc5e833d2b257dd05231893aa71b5>`_
- Make our update statistics app work with again with F14 `8caaf44ae <https://github.com/fedora-infra/fedora-packages/commit/8caaf44ae773a32a377cd33f8de929a4607af59d>`_
- Show EPEL builds in our Package Sources app (#305) `a272bb9fc <https://github.com/fedora-infra/fedora-packages/commit/a272bb9fcd11ec7e10520cdb7905c62f3870d283>`_
- Apply a patch from dtimms to fix some broken links in our tour (#343) `f4263f266 <https://github.com/fedora-infra/fedora-packages/commit/f4263f26644dd0a7a04a2546fa33deb0832366a6>`_
- add a tab index to search field `76bf187d1 <https://github.com/fedora-infra/fedora-packages/commit/76bf187d196b82033737de1261f16136ea28e596>`_
- Fixed updates widget to work with new tagging scheme `0e0bdf7b2 <https://github.com/fedora-infra/fedora-packages/commit/0e0bdf7b2a04a0f30d2973e51d01fa6fb71ae081>`_
- Fixed the downloads package maintenance for new tagging scheme. pkgdb.get_fedora_releases() now provides branchname, name version, and koji_name as list. `8dfc1c79d <https://github.com/fedora-infra/fedora-packages/commit/8dfc1c79d5e724c37ab8cda581d2229c6ccdda41>`_
- Use new pkgdb gitbranchname instead of old cvs branchname Metrics still use branchname due to bodhi dep `7bb64434c <https://github.com/fedora-infra/fedora-packages/commit/7bb64434cfc1829bcb20df8489cf048ba23c3ae8>`_
- Converted spec download from old cvs to new git repo `6e210e446 <https://github.com/fedora-infra/fedora-packages/commit/6e210e44694ed7bf147a94163f143610cb72d892>`_
