%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?pyver: %define pyver %(%{__python} -c "import sys ; print sys.version[:3]")}

%define oldname fedoracommunity

Name:           fedora-packages
Version:        3.0.4
Release:        1%{?dist}
Summary:        A modular framework for consolidating Fedora Infrastructure
Group:          Applications/Internet
License:        AGPLv3
URL:            https://fedorahosted.org/fedoracommunity
Source0:        fedoracommunity-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

%if 0%{?rhel}
%if "%rhel" < "6"
BuildRequires: python-setuptools
%else
BuildRequires: python-setuptools-devel
%endif
%else
BuildRequires: python-setuptools-devel
%endif

BuildRequires: python-devel
BuildRequires: python-pygments
BuildRequires: pytz
BuildRequires: pyOpenSSL
BuildRequires: TurboGears2
BuildRequires: python-moksha-wsgi
BuildRequires: python-tw2-jqplugins-ui
BuildRequires: python-bunch
BuildRequires: python-dogpile-core > 0.4.0
BuildRequires: python-dogpile-cache > 0.4.1
BuildRequires: python-memcached
BuildRequires: python-markdown
BuildRequires: pygobject3
BuildRequires: fedmsg
BuildRequires: python-daemon

%if 0%{?el6} || 0%{?el5}
BuildRequires:  python-ordereddict
Requires:       python-ordereddict
BuildRequires:  python-webob1.0
Requires:       python-webob1.0
%endif

Requires: TurboGears2
Requires: python-moksha-wsgi
Requires: intltool
Requires: koji
Requires: python-fedora
Requires: python-feedparser
Requires: python-iniparse
Requires: pytz
Requires: pyOpenSSL
Requires: httpd
Requires: mod_wsgi
Requires: diffstat
Requires: fedpkg
Requires: python-ordereddict
Requires: python-lockfile
Requires: python-tw2-jqplugins-ui
Requires: python-bugzilla
Requires: xapian-bindings-python
Requires: python-xappy
Requires: python-dogpile-core > 0.4.0
Requires: python-dogpile-cache > 0.4.1
Requires: python-memcached
Requires: packagedb-cli
Requires: python-markdown
Requires: pygobject3
Requires: fedmsg
# For spectool
Requires: rpmdevtools
Requires: python-daemon

Obsoletes: myfedora
Conflicts: fedoracommunity


%description
Fedora Community is a set of web applications for consolidating Fedora Infrastructure

%prep
%setup -q -n fedoracommunity-%{version}

%if %{?rhel}%{!?rhel:0} >= 6
# Make sure that epel/rhel picks up the correct version of webob
awk 'NR==1{print "import __main__; __main__.__requires__ = __requires__ = [\"WebOb==1.0.8\", \"sqlalchemy>=0.7\"]; import pkg_resources"}1' setup.py > setup.py.tmp
mv setup.py.tmp setup.py
%endif


%build
%{__python} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build \
    --install-data=%{_datadir} --root %{buildroot}
%{__python} setup.py archive_fedoracommunity_resources -f -o %{buildroot}%{_datadir}/%{oldname}/public/toscawidgets -d moksha -d fedoracommunity

# Hack, to work around tw2 resource archiving issues
%{__mkdir_p} %{buildroot}%{_datadir}/%{oldname}/public/toscawidgets/resources/fedoracommunity.widgets.jquery_template/static/javascript
cp fedoracommunity/widgets/static/javascript/jquery.tmpl.js %{buildroot}%{_datadir}/%{oldname}/public/toscawidgets/resources/fedoracommunity.widgets.jquery_template/static/javascript
%{__mkdir_p} %{buildroot}%{_datadir}/%{oldname}/public/toscawidgets/resources/fedoracommunity.connectors.widgets.widgets/static/js
cp fedoracommunity/connectors/widgets/static/js/fcomm.js %{buildroot}%{_datadir}/%{oldname}/public/toscawidgets/resources/fedoracommunity.connectors.widgets.widgets/static/js
%{__mkdir_p} %{buildroot}%{_datadir}/%{oldname}/public/toscawidgets/resources/fedoracommunity.widgets.grid/static/javascript/ui/
cp fedoracommunity/widgets/static/javascript/ui/moksha.ui.{grid,popup}.js %{buildroot}%{_datadir}/%{oldname}/public/toscawidgets/resources/fedoracommunity.widgets.grid/static/javascript/ui
%{__mkdir_p} %{buildroot}%{_datadir}/%{oldname}/public/toscawidgets/resources/fedoracommunity.widgets.package.updates/static/javascript/
cp fedoracommunity/widgets/package/static/javascript/bodhi.js %{buildroot}%{_datadir}/%{oldname}/public/toscawidgets/resources/fedoracommunity.widgets.package.updates/static/javascript/
%{__mkdir_p} %{buildroot}%{_datadir}/%{oldname}/public/toscawidgets/resources/fedoracommunity.widgets.expander/static/javascript/
cp fedoracommunity/widgets/static/javascript/jquery.expander.js %{buildroot}%{_datadir}/%{oldname}/public/toscawidgets/resources/fedoracommunity.widgets.expander/static/javascript/
%{__mkdir_p} %{buildroot}%{_datadir}/%{oldname}/public/toscawidgets/resources/fedoracommunity.widgets.tree/static/javascript/
cp fedoracommunity/widgets/static/javascript/jquery.jstree.js %{buildroot}%{_datadir}/%{oldname}/public/toscawidgets/resources/fedoracommunity.widgets.tree/static/javascript/

%{__mkdir_p} %{buildroot}/var/lib/
%{__mkdir_p} %{buildroot}%{_datadir}/%{oldname}/production/apache
%{__mkdir_p} -m 0755 %{buildroot}/%{_localstatedir}/log/%{oldname}
%{__mkdir_p} -m 0700 %{buildroot}/%{_localstatedir}/cache/%{oldname}

%{__install} -m 640 production/apache/%{oldname}.conf %{buildroot}%{_datadir}/%{oldname}/production/apache
%{__install} production/apache/%{oldname}.wsgi %{buildroot}%{_datadir}/%{oldname}/production/apache/%{oldname}.wsgi
%{__install} production/sample-production.ini %{buildroot}%{_datadir}/%{oldname}/production

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README.txt COPYING AUTHORS
%{python_sitelib}/%{oldname}/
%attr(-,apache,root) %dir %{_datadir}/%{oldname}
%attr(-,apache,root) %{_datadir}/%{oldname}/production
%attr(-,apache,root) %{_datadir}/%{oldname}/public
%attr(-,apache,root) %{_localstatedir}/log/%{oldname}
%{python_sitelib}/%{oldname}-%{version}-py%{pyver}.egg-info/
#%{python_sitelib}/%{oldname}-%{version}-py%{pyver}-nspkg.pth
%attr(-,apache,apache) %dir %{_localstatedir}/cache/%{oldname}
%{_bindir}/fcomm-index-packages

%changelog
* Tue Mar 01 2016 Ralph Bean <rbean@redhat.com> - 3.0.4-1
- new version

* Fri Jan 08 2016 Ralph Bean <rbean@redhat.com> - 3.0.3-1
- new version

* Mon Nov 23 2015 Ralph Bean <rbean@redhat.com> - 3.0.2-1
- ThreadPool for the fedmsg cache worker.

* Mon Nov 23 2015 Ralph Bean <rbean@redhat.com> - 3.0.1-1
- Minor release with small enhancements and bugfixes.

* Tue Nov 17 2015 Ralph Bean <rbean@redhat.com> - 3.0.0-3
- Major rewrite of backend.
- Removed all yum and rpm cache management.
- Introduced new service dep on mdapi.
- Replaced cronjobs with a fedmsg updater.

* Tue Oct 20 2015 Ralph Bean <rbean@redhat.com> - 2.0.20-1
- new version

* Wed May 14 2014 Ralph Bean <rbean@redhat.com> - 2.0.16-2
- Further pkgdb2 updates.

* Wed May 14 2014 Ralph Bean <rbean@redhat.com> - 2.0.16-1
- Updates for pkgdb2 compatibility.

* Tue Mar 11 2014 Ralph Bean <rbean@redhat.com> - 2.0.15-1
- Roll back the yumlock stuff in a rich blossom of hatred.

* Mon Mar 10 2014 Ralph Bean <rbean@redhat.com> - 2.0.14-2
- Patch to fix a bug with the new yumlock stuff.

* Mon Mar 10 2014 Ralph Bean <rbean@redhat.com> - 2.0.14-1
- Add typeahead plugin from relrod.
- Make datagrepper icons square.
- Exclude some datagrepper spam.
- Avoid default to armv7hl on relationships tab.
- Experiment with yumlocking.

* Sun Feb 09 2014 Ralph Bean <rbean@redhat.com> - 2.0.13-1
- Add HTML cards from charulagrl.

* Fri Jan 10 2014 Ralph Bean <rbean@redhat.com> - 2.0.12-2
- Small regression fix for older TG2.

* Fri Jan 10 2014 Ralph Bean <rbean@redhat.com> - 2.0.11-1
- Added link to cgit.
- Fix icon sizes.
- Library compat updates.
- Include epel bugs in bug list.
- Search can now accept slashes.

* Mon Aug 05 2013 Ralph Bean <rbean@redhat.com> - 2.0.10-1
- Bugfix - allow bugzilla cookiefile to be configurable.

* Wed Jul 31 2013 Ralph Bean <rbean@redhat.com> - 2.0.9-1
- Bugfix - import refactored code from python-moksha-wsgi.
  The tabbedcontainer and the dashboardcontainer.

* Mon Jul 15 2013 Ralph Bean <rbean@redhat.com> - 2.0.8-1
- Unescape JSON so the relationships tab (and other things) work.
- Move exception handling into call_get_file_tree for consistency.
- Fix karma_level css on the updates page.
- Some fixes for f19/tg2-2.3.0 compatibility.

* Mon Jun 10 2013 Ralph Bean <rbean@redhat.com> - 2.0.7-2
- Emergency bugfix release.
- Get off of the old moksha.common.lib.helpers stuff.
- Fix bugs release from pingou.
- Fix misleading text in bugs widget.
- Don't escape the spec file widget.
- Support bugzilla 0.8.0
- Added buildrequires on python-memcached.

* Tue Jan 29 2013 Ralph Bean <rbean@redhat.com> - 2.0.6-1
- Include explicit memcached cleanup in the cache worker.

* Thu Jan 24 2013 Ralph Bean <rbean@redhat.com> - 2.0.5-6
- Include an fcomm-cache-worker daemon which picks tasks off a redis queue and
  does work to refresh the values in memcached.

* Mon Jan 14 2013 Ralph Bean <rbean@redhat.com> - 2.0.4-6.20130114git6c5b194
- Fix bug where /packages/qt returned a 404
- Fix bug where /packages/python-webob1.2 returned a 404
- Redirecting users with 404s to the search interface
- Update hardcoded URL in fedoracommunity/search/index.py

* Fri Jan 11 2013 Ralph Bean <rbean@redhat.com> - 2.0.4-5.20130111gitd823e16
- Py2.6 bugfix for the SSL/bugzilla hack.

* Fri Jan 11 2013 Ralph Bean <rbean@redhat.com> - 2.0.4-4.20130111git919e4de
- Fixed a link for new EPEL bugs
- Fixed that bonkers SSL timeout with bugz
- Update to latest experimental dogpile cache refresh.

* Thu Jan 03 2013 Ralph Bean <rbean@redhat.com> - 2.0.4-3.20130103gitc211bc6
- Moved to git checkout.
- Experimenting with background dogpile cache refresh.

* Fri Dec 14 2012 Ralph Bean <rbean@redhat.com> - 2.0.4-2
- Fixed and enhanced developer bootstrapping (Luke Macken)
- Added Blocker Bugs to the stats widget (Luke Macken)
- Links to other apps (Marija Radevskaa)
- Link to owner profile (Marija Radevskaa)
- Connector cacheing with dogpile (Ralph Bean)
- Fixed CSS resource inconsistencies (Ralph Bean)

* Thu Sep 20 2012 Ralph Bean <rbean@redhat.com> - 2.0.3-1
- Smarter searching.
- Fixed tw2 resource archival for deployment.
- HTML5 autofocus on search bar on main page.
- Port forward to using the latest moksha.

* Thu Aug 23 2012 Ralph Bean <rbean@redhat.com> - 2.0.2-1
- Something got messed up with the versioning.  New tarball.

* Wed Aug 22 2012 Ralph Bean <rbean@redhat.com> - 2.0.1-1
- Workaround bugzilla ssl timeouts
- Expanded /bugs page - http://bit.ly/TCMoXc
- Lots of little traceback fixes.
- Added newly required dependency on TurboGears2

* Wed Apr 25 2012 Luke Macken <lmacken@redhat.com> - 2.0-2
- python-tw2-jquery-ui was renamed to python-tw2-jqplugins-ui

* Tue Feb 28 2012 Luke Macken <lmacken@redhat.com> - 2.0-1
- Rename to fedora-packages and bump to 2.0

* Mon Dec 19 2011 Luke Macken <lmacken@redhat.com> - 0.5.1-2
- Update our requirements

* Thu Dec 01 2011 John (J5) Palmieri <johnp@redhat.com> - 0.5.1-1
- fixups for deployment on RHEL6

* Thu Dec 01 2011 John (J5) Palmieri <johnp@redhat.com> - 0.5.0-1
- release of the development version of the packager branch

* Wed Jul 21 2010 Luke Macken <lmacken@redhat.com> - 0.4.1-1
- 0.4.1 bugfix release

* Fri Mar 26 2010 Luke Macken <lmacken@redhat.com> - 0.4.0-1
- 0.4.0 final release

* Wed Mar 24 2010 Luke Macken <lmacken@redhat.com> - 0.4.0-0.beta.1
- 0.4.0 beta1 release

* Wed Feb 10 2010 Luke Macken <lmacken@redhat.com> - 0.3.10-1
- 0.3.10 release

* Fri Jan 22 2010 Luke Macken <lmacken@redhat.com> - 0.3.9-1
- 0.3.9 release

* Mon Jan 04 2010 Luke Macken <lmacken@redhat.com> - 0.3.8.2-2
- Require httpd and mod_wsgi

* Mon Nov 02 2009 John (J5) Palmieri <johnp@redhat.com> - 0.3.8.2-1
- 0.3.8.2 - make sure toscawidgets finds the js files

* Thu Oct 29 2009 John (J5) Palmieri <johnp@redhat.com> - 0.3.8.1-1
- 0.3.8.1 - make sure js files are packaged

* Thu Oct 29 2009 John (J5) Palmieri <johnp@redhat.com> - 0.3.8-1
- 0.3.8 - add demos tab w/ amqp demo app 

* Tue Sep 22 2009 Luke Macken <lmacken@redhat.com> - 0.3.7-1
- 0.3.7

* Fri Sep 04 2009 Luke Macken <lmacken@redhat.com> - 0.3.6-2
- Require python-memcached for production environments

* Wed Sep 02 2009 Luke Macken <lmacken@redhat.com> - 0.3.6-1
- 0.3.6

* Wed Sep 02 2009 Luke Macken <lmacken@redhat.com> - 0.3.5-1
- 0.3.5

* Mon Aug 03 2009 Luke Macken <lmacken@redhat.com> - 0.3.4-1
- 0.3.4, bugfix release

* Mon Jul 27 2009 Luke Macken <lmacken@redhat.com> - 0.3.3-1
- 0.3.3, bugfix release

* Mon Jul 27 2009 Luke Macken <lmacken@redhat.com> - 0.3.2-1
- 0.3.2, bugfix release

* Thu Jun 11 2009 Luke Macken <lmacken@redhat.com> - 0.3.1-1
- New bugfix release

* Wed Jun 10 2009 Luke Macken <lmacken@redhat.com> - 0.3-6
- Revision bump to fix some unmerged changes

* Wed Jun 10 2009 Luke Macken <lmacken@redhat.com> - 0.3-5
- Fix a trivial bug in the BugsStatsWidget

* Sat Jun 06 2009 Luke Macken <lmacken@redhat.com> - 0.3-4
- Extract our widget resources

* Thu Jun 04 2009 Luke Macken <lmacken@redhat.com> - 0.3-3
- Fix namespace package issues.

* Thu Jun 04 2009 John (J5) Palmieri <johnp@redhat.com> - 0.3-1
- add the makeyumcache script

* Wed Jun 03 2009 Luke Macken <lmacken@redhat.com> - 0.2-2
- Require pytz and pyOpenSSL, and Moksha

* Mon Jun 01 2009 John (J5) Palmieri <johnp@redhat.com> - 0.2-1
- first package after myfedora->fedoracommunity transition
