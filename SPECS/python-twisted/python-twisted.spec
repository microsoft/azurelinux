%global debug_package %{nil}
Summary:        An asynchronous networking framework written in Python
Name:           python-twisted
Version:        22.10.0
Release:        2%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://twistedmatrix.com
Source0:        https://github.com/twisted/twisted/archive/twisted-%{version}.tar.gz
# Disabling UDP multicast test, which failes in container environments.
# For more details, see: https://twistedmatrix.com/trac/ticket/7494
Patch0:         disable_multicast_test.patch

BuildRequires:  python3-devel
BuildRequires:  python3-incremental
BuildRequires:  python3-pyOpenSSL
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  python3-zope-interface
%if %{with_check}
BuildRequires:  python3-pip
BuildRequires:  net-tools
BuildRequires:  sudo
BuildRequires:  tzdata
BuildRequires:  git
%endif

AutoReqProv:    no

%description
An asynchronous networking framework written in Python

%package -n     python3-twisted
Summary:        An asynchronous networking framework written in Python
Requires:       python3
Requires:       python3-attrs
Requires:       python3-constantly
Requires:       python3-hyperlink
Requires:       python3-incremental
Requires:       python3-netaddr
Requires:       python3-zope-interface
AutoReqProv:    no
Provides:       python3dist(twisted) = %{version}-%{release}
Provides:       python3.7dist(twisted) = %{version}-%{release}

%description -n python3-twisted
Twisted is an event-driven networking engine written in Python and licensed under the open source ​MIT license. Twisted runs on Python 3.6 and above.
Twisted also supports many common network protocols, including SMTP, POP3, IMAP, SSHv2, and DNS.

%prep
%autosetup -p 1 -n twisted-twisted-%{version}

%build
%py3_build

%install
%py3_install
ln -s twistd %{buildroot}/%{_bindir}/twistd3
ln -s trial %{buildroot}/%{_bindir}/trial3
ln -s tkconch %{buildroot}/%{_bindir}/tkconch3
ln -s pyhtmlizer %{buildroot}/%{_bindir}/pyhtmlizer3
ln -s twist %{buildroot}/%{_bindir}/twist3
ln -s conch %{buildroot}/%{_bindir}/conch3
ln -s ckeygen %{buildroot}/%{_bindir}/ckeygen3
ln -s cftp %{buildroot}/%{_bindir}/cftp3

%check
route add -net 224.0.0.0 netmask 240.0.0.0 dev lo
chmod g+w . -R
useradd test -G root -m
sudo -u test pip3 install --upgrade pip
sudo -u test pip3 install 'tox>=3.27.1,<4.0.0' PyHamcrest cython-test-exception-raiser
chmod g+w . -R
LANG=en_US.UTF-8 sudo -u test /home/test/.local/bin/tox -e nocov-posix-alldeps

%files -n python3-twisted
%defattr(-,root,root)
%license LICENSE
%{python3_sitelib}/*
%{_bindir}/twistd
%{_bindir}/trial
%{_bindir}/tkconch
%{_bindir}/pyhtmlizer
%{_bindir}/twist
%{_bindir}/mailmail
%{_bindir}/conch
%{_bindir}/ckeygen
%{_bindir}/cftp
%{_bindir}/twistd3
%{_bindir}/trial3
%{_bindir}/tkconch3
%{_bindir}/pyhtmlizer3
%{_bindir}/twist3
%{_bindir}/conch3
%{_bindir}/ckeygen3
%{_bindir}/cftp3

%changelog
* Fri Dec 16 2022 Sam Meluch <sammeluch@microsoft.com> - 22.10.0-2
- Update version of tox used for package tests

* Mon Oct 31 2022 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 22.10.0-1
- Upgrade to 22.10.0

* Tue May 31 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 22.4.0-1
- Upgrade to version 22.4.0 to fix CVE-2022-24801

* Mon Mar 28 2022 Jon Slobodzian <joslobo@microsoft.com> - 22.2.0-1
- Upgrade to version 22.2.0-1

* Tue Mar 15 2022 Muhammad Falak <mwani@microsoft.com> - 19.2.1-10
- Use `py%{python3_version_nodots}` instead of harcoding `py39`

* Thu Feb 10 2022 Muhammad Falak <mwani@microsoft.com> - 19.2.1-9
- Add an explicit BR on 'pip' & 'sudo'
- Use `py39` as tox environment to enable ptest

* Fri Dec 03 2021 Olivia Crain <oliviacrain@microsoft.com> - 19.2.1-8
- Replace easy_install usage with pip in %%check sections

* Wed Oct 20 2021 Olivia Crain <oliviacrain@microsoft.com> - 19.2.1-7
- Remove python2 package, move default bindaries to python3 package
- Lint spec

* Tue Jan 05 2021 Ruying Chen <v-ruyche@microsoft.com> - 19.2.1-6
- Disable auto dependency generator

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 19.2.1-5
- Added %%license line automatically

* Wed Apr 29 2020 Emre Girgin <mrgirgin@microsoft.com> 19.2.1-4
- Renaming python-zope.interface to python-zope-interface

* Wed Apr 29 2020 Emre Girgin <mrgirgin@microsoft.com> 19.2.1-3
- Renaming python-pyOpenSSL to pyOpenSSL

* Tue Apr 28 2020 Emre Girgin <mrgirgin@microsoft.com> 19.2.1-2
- Renaming python-Twisted to python-twisted

* Thu Mar 19 2020 Paul Monson <paulmon@microsoft.com> 19.2.1-1
- Update to 19.2.1. Fix Source0 URL. License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 18.7.0-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue Oct 30 2018 Tapas Kundu <tkundu@vmware.com> 18.7.0-2
- Moved build requires from subpackage
- Added attrs package in requires.

* Thu Sep 13 2018 Tapas Kundu <tkundu@vmware.com> 18.7.0-1
- Upgraded to release 18.7.0

* Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 17.5.0-3
- Remove BuildArch

* Mon Sep 11 2017 Dheeraj Shetty <dheerajs@vmware.com> 17.5.0-2
- Added python-automat, python-hyperlink and its python3 version to the
- requires.

* Tue Aug 29 2017 Dheeraj Shetty <dheerajs@vmware.com> 17.5.0-1
- Upgrade version

* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 17.1.0-6
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.

* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 17.1.0-5
- Adding python3 scripts to bin directory

* Tue May 09 2017 Rongrong Qiu <rqiu@vmware.com> 17.1.0-4
- Added python-constantly to the requires.

* Mon Mar 27 2017 Xiaolin Li <xiaolinl@vmware.com> 17.1.0-3
- Added python-netaddr and python-incremental to the requires.

* Thu Mar 23 2017 Xiaolin Li <xiaolinl@vmware.com> 17.1.0-2
- Change requires

* Wed Mar 01 2017 Xiaolin Li <xiaolinl@vmware.com> 17.1.0-1
- Added python3 package and updated to version 17.1.0.

* Mon Oct 10 2016 ChangLee <changlee@vmware.com> 15.5.0-3
- Modified %check

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 15.5.0-2
- GA - Bump release of all rpms

* Thu Jan 21 2016 Anish Swaminathan <anishs@vmware.com> 15.5.0-1
- Upgrade version

* Tue Oct 27 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
- Initial packaging for Photon
