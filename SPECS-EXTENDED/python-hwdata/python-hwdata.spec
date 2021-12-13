Vendor:         Microsoft Corporation
Distribution:   Mariner

# Enable python3 build by default
%bcond_without python3

# Disable python2 build by default
%bcond_with python2

Name:		python-hwdata
Version:	2.3.7
Release:	9%{?dist}
Summary:	Python bindings to hwdata package
BuildArch:  noarch
License:	GPLv2
URL:		https://github.com/xsuchy/python-hwdata
# git clone https://github.com/xsuchy/python-hwdata.git
# cd python-hwdata
# tito build --tgz
Source0:	%{name}-%{version}.tar.gz

%description
Provide python interface to database stored in hwdata package.
It allows you to get human readable description of USB and PCI devices.

%if %{with python2}
%package -n python2-hwdata
Summary:	Python bindings to hwdata package

BuildRequires: python2-devel

Requires:	hwdata
%{?python_provide:%python_provide python2-hwdata}
%if 0%{?rhel} < 8
Provides:	python-hwdata = %{version}-%{release}
%endif

%description -n python2-hwdata
Provide python interface to database stored in hwdata package.
It allows you to get human readable description of USB and PCI devices.

This is the Python 2 build of the module.
%endif # with python2

%if %{with python3}
%package -n python3-hwdata
Summary:	Python bindings to hwdata package

BuildRequires:	python3-devel
BuildRequires:	python3-pylint
Requires:	hwdata

%{?python_provide:%python_provide python3-hwdata}

%description -n python3-hwdata
Provide python interface to database stored in hwdata package.
It allows you to get human readable description of USB and PCI devices.

This is the Python 3 build of the module.
%endif # with python3

%prep
%setup -q

%if %{with python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with python3

%build
%if %{with python2}
%py2_build
%endif # with python2

%if %{with python3}
pushd %{py3dir}
%py3_build
popd
%endif # with python3

%install
%if %{with python2}
%py2_install
%endif # with python2

%if %{with python3}
pushd %{py3dir}
%py3_install
popd
%endif # with python3

%check
%if %{with python3}
pylint-3 hwdata.py example.py || :
%endif # with python3

%if %{with python2}
%files -n python2-hwdata
%license LICENSE
%doc README.md example.py
%doc html
%{python2_sitelib}/*
%endif # with python2

%if %{with python3}
%files -n python3-hwdata
%license LICENSE
%doc README.md example.py
%doc html
%{python3_sitelib}/*
%endif # with python3

%changelog
* Fri Mar 05 2021 Henry Li <lihl@microsoft.com> - 2.3.7-9
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Fix distro checking to enable python3 build and disable python2 build

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 2.3.7-7
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2.3.7-6
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 2.3.7-2
- Rebuilt for Python 3.7

* Fri Mar 23 2018 Miroslav Suchý <msuchy@redhat.com> 2.3.7-1
- remove python2 subpackage for F30+

* Mon Feb 12 2018 Miroslav Suchý <msuchy@redhat.com> 2.3.6-1
- Update Python 2 dependency declarations to new packaging standards

* Wed Aug 09 2017 Miroslav Suchý <msuchy@redhat.com> 2.3.5-1
- create python2-hwdata subpackage
- use dnf instead of yum in README
- remove rhel5 compatibilities from spec

* Thu Sep 22 2016 Miroslav Suchý <miroslav@suchy.cz> 2.3.4-1
- run pylint in %%check
- require hwdata in python 3 package too (jdobes@redhat.com)
- implement PNP interface
- errors in usb.ids should not be fatal
- change upstream url in setup.py

* Wed Jan 28 2015 Miroslav Suchý <msuchy@redhat.com> 2.3.3-1
- upstream location changed

* Wed Jan 28 2015 Miroslav Suchý <msuchy@redhat.com>
- move upstream location

* Wed Dec 04 2013 Miroslav Suchý <msuchy@redhat.com> 1.10.1-1
- create python3-hwdata subpackage
- Bumping package versions for 1.9
- %%defattr is not needed since rpm 4.4

* Fri Mar 02 2012 Miroslav Suchý 1.7.3-1
- 798375 - fix PCI device name translation (Joshua.Roys@gtri.gatech.edu)
- use setup from distutils

* Fri Mar 02 2012 Jan Pazdziora 1.7.2-1
- Update the copyright year info.

* Fri Mar 02 2012 Jan Pazdziora 1.7.1-1
- correct indentation (mzazrivec@redhat.com)

* Mon Oct 31 2011 Miroslav Suchý 1.6.2-1
- point URL to specific python-hwdata page

* Fri Jul 22 2011 Jan Pazdziora 1.6.1-1
- We only support version 14 and newer of Fedora, removing conditions for old
  versions.

* Mon Apr 26 2010 Miroslav Suchý <msuchy@redhat.com> 1.2-1
- 585138 - change %%files section and patial support for python3

* Fri Apr 23 2010 Miroslav Suchý <msuchy@redhat.com> 1.1-1
- initial release
