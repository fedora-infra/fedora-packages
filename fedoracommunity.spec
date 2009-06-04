%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?pyver: %define pyver %(%{__python} -c "import sys ; print sys.version[:3]")}

Name:           fedoracommunity
Version:        0.3
Release:        1%{?dist}
Summary:        A modular framework for consolidating Fedora Infrastructure 
Group:          Applications/Internet
License:        AGPLv3
URL:            https://fedorahosted.org/fedoracommunity
Source0:        fedoracommunity-%{version}.tar.bz2

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires: python-setuptools 
BuildRequires: python-setuptools-devel
BuildRequires: python-devel
BuildRequires: python-pygments

Requires: moksha
Requires: intltool
Requires: koji
Requires: python-fedora
Requires: python-feedparser
Requires: python-iniparse

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
* Thu Jun 04 2009 John (J5) Palmieri <johnp@redhat.com> - 0.3-1
- add the makeyumcache script

* Mon Jun 01 2009 John (J5) Palmieri <johnp@redhat.com> - 0.2-1
- first package after myfedora->fedoracommunity transition
