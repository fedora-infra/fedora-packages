%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?pyver: %define pyver %(%{__python} -c "import sys ; print sys.version[:3]")}

Name:           fedoracommunity
Version:        0.3.6
Release:        2%{?dist}
Summary:        A modular framework for consolidating Fedora Infrastructure 
Group:          Applications/Internet
License:        AGPLv3
URL:            https://fedorahosted.org/fedoracommunity
Source0:        fedoracommunity-%{version}.tar.bz2

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires: python-setuptools-devel
BuildRequires: python-devel
BuildRequires: python-pygments
BuildRequires: pytz
BuildRequires: pyOpenSSL
BuildRequires: moksha

Requires: moksha
Requires: intltool
Requires: koji
Requires: python-fedora
Requires: python-feedparser
Requires: python-iniparse
Requires: pytz
Requires: pyOpenSSL
Requires: python-memcached

Obsoletes: myfedora

%description
Fedora Community is a web application for consolidating Fedora Infrastructure

%prep
%setup -q

%build
%{__python} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build \
    --install-data=%{_datadir} --root %{buildroot}
%{__python} setup.py archive_tw_resources -f -o %{buildroot}%{_datadir}/%{name}/public/toscawidgets

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

%changelog
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
