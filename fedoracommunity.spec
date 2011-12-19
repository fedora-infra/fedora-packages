%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?pyver: %define pyver %(%{__python} -c "import sys ; print sys.version[:3]")}

Name:           fedoracommunity
Version:        0.5.1
Release:        1%{?dist}
Summary:        A modular framework for consolidating Fedora Infrastructure 
Group:          Applications/Internet
License:        AGPLv3
URL:            https://fedorahosted.org/fedoracommunity
Source0:        fedoracommunity-%{version}.tar.bz2

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
BuildRequires: moksha
BuildRequires: python-tw2-jquery-ui

%if 0%{?el6} || 0%{?el5}
BuildRequires: python-ordereddict
Requires: python-ordereddict
%endif

Requires: moksha >= 0.4.3
Requires: intltool
Requires: koji
Requires: python-fedora
Requires: python-feedparser
Requires: python-iniparse
Requires: pytz
Requires: pyOpenSSL
Requires: python-memcached
Requires: httpd
Requires: mod_wsgi
Requires: diffstat
Requires: fedpkg
Requires: python-ordereddict
Requires: python-lockfile
Requires: python-tw2-jquery-ui
Requires: python-bugzilla
Requires: xapian-bindings-python

Obsoletes: myfedora

%description
Fedora Community is a set of web applications for consolidating Fedora Infrastructure

%prep
%setup -q

%build
%{__python} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build \
    --install-data=%{_datadir} --root %{buildroot}
%{__python} setup.py archive_fedoracommunity_resources -f -o %{buildroot}%{_datadir}/%{name}/public/toscawidgets -d moksha -d fedoracommunity

%{__mkdir_p} %{buildroot}/var/lib/
%{__mkdir_p} %{buildroot}%{_datadir}/%{name}/production/apache
%{__mkdir_p} -m 0755 %{buildroot}/%{_localstatedir}/log/%{name}
%{__mkdir_p} -m 0700 %{buildroot}/%{_localstatedir}/cache/%{name}

%{__install} -m 640 production/apache/%{name}.conf %{buildroot}%{_datadir}/%{name}/production/apache
%{__install} production/apache/%{name}.wsgi %{buildroot}%{_datadir}/%{name}/production/apache/%{name}.wsgi
%{__install} production/sample-production.ini %{buildroot}%{_datadir}/%{name}/production

%clean
%{__rm} -rf %{buildroot}


%files 
%defattr(-,root,root,-)
%doc README.txt COPYING AUTHORS
%{python_sitelib}/%{name}/
%attr(-,apache,root) %dir %{_datadir}/%{name}
%attr(-,apache,root) %{_datadir}/%{name}/production
%attr(-,apache,root) %{_datadir}/%{name}/public
%attr(-,apache,root) %{_localstatedir}/log/%{name}
%{python_sitelib}/%{name}-%{version}-py%{pyver}.egg-info/
#%{python_sitelib}/%{name}-%{version}-py%{pyver}-nspkg.pth
%attr(-,apache,apache) %dir %{_localstatedir}/cache/%{name}
%{_bindir}/fedoracommunity_makeyumcache
%{_bindir}/fcomm-index-packages
%{_bindir}/fcomm-index-latest-builds

%changelog
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
