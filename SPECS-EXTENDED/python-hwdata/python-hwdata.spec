Name:		python-hwdata
Version:	2.4.1
Release:	1%{?dist}
Summary:	Python bindings to hwdata package
BuildArch:  noarch
License:	GPL-2.0-or-later
URL:		https://github.com/xsuchy/python-hwdata
# git clone https://github.com/xsuchy/python-hwdata.git
# cd python-hwdata
# tito build --tgz
Source0:	%{name}-%{version}.tar.gz

%description
Provide python interface to database stored in hwdata package.
It allows you to get human readable description of USB and PCI devices.

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

%prep
%setup -q

rm -rf %{py3dir}
cp -a . %{py3dir}

%build
pushd %{py3dir}
%py3_build
popd

%install
pushd %{py3dir}
%py3_install
popd

%check
pylint-3 hwdata.py example.py || :

%files -n python3-hwdata
%license LICENSE
%doc README.md example.py
%doc html
%{python3_sitelib}/*

%changelog
* Fri Nov 10 2023 Miroslav Suchý <msuchy@redhat.com> 2.4.1-1
- remove python2 code
- spec: generate only python3 package
- use SPDX identifier for license
- add PCI subsystem support (jussi.kuokkanen@protonmail.com)

* Wed Nov 30 2022 Miroslav Suchý <msuchy@redhat.com> 2.3.8-1
- use spdx license
- update README
- Add NotImplementedError (kaveshnikov.denis@hotmail.com)

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.7-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2.3.7-15
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.7-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.7-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.3.7-12
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.7-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.7-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 2.3.7-9
- Rebuilt for Python 3.9

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
