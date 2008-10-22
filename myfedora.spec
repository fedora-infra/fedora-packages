%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?pyver: %define pyver %(%{__python} -c "import sys ; print sys.version[:3]")}

Name:           myfedora 
Version:        0.1dev
Release:        0.gitfdc9a27c%{?dist}
Summary:        A modular framework for consolidating Fedora Infrastructure 
Group:          Applications/Internet
License:        GPLv2+
URL:            https://fedorahosted.org/myfedora
Source0:        myfedora-%{version}.tar.bz2

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires: python-setuptools 
BuildRequires: python-setuptools-devel
BuildRequires: python-devel

Requires: TurboGears2
Requires: intltool
Requires: koji
Requires: python-fedora
Requires: mod_wsgi
Requires: mod_nss
Requires: python-cjson
Requires: python-simplejson
Requires: python-turbojson
Requires: python-feedparser
Requires: python-iniparse
Requires: python-tw-jquery
Requires: python-repoze-who 

%description
MyFedora is a web application for consolidating Fedora Infrastructure

%prep
%setup -q

%build
%{__python} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build \
    --install-data=%{_datadir} --root %{buildroot}

%{__mkdir_p} %{buildroot}/var/lib/bodhi
%{__mkdir_p} %{buildroot}%{_sysconfdir}/httpd/conf.d
%{__mkdir_p} %{buildroot}%{_sysconfdir}/myfedora
%{__mkdir_p} %{buildroot}%{_datadir}/%{name}
%{__mkdir_p} -m 0755 %{buildroot}/%{_localstatedir}/log/myfedora

%{__install} -m 640 apache/%{name}.conf %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf
%{__install} -m 640 %{name}.cfg %{buildroot}%{_sysconfdir}/%{name}/
%{__install} apache/%{name}.wsgi %{buildroot}%{_datadir}/%{name}/%{name}.wsgi

%clean
%{__rm} -rf %{buildroot}


%files 
%defattr(-,root,root,-)
%doc README COPYING
%{python_sitelib}/%{name}/
%{_bindir}/%{name}-*
%{_sysconfdir}/httpd/conf.d/myfedora.conf
%attr(-,apache,root) %{_datadir}/%{name}
%attr(-,apache,root) %config(noreplace) %{_sysconfdir}/myfedora/*
%attr(-,apache,root) %{_localstatedir}/log/myfedora
%{python_sitelib}/%{name}-%{version}-py%{pyver}.egg-info/

%changelog
* Tue Oct 21 2008 John (J5) Palmieri <lmacken@redhat.com> - 0.1-0.git5083686a
- first package

