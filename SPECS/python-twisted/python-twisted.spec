%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        An asynchronous networking framework written in Python
Name:           python-twisted
Version:        20.3.0
Release:        5%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://twistedmatrix.com
Source0:        https://pypi.python.org/packages/source/T/Twisted/Twisted-%{version}.tar.bz2
Patch0:         extra_dependency.patch
Patch1:         no_packet.patch
Patch2:         CVE-2022-21712.patch
Patch3:         CVE-2022-24801.patch
Patch4:    CVE-2022-39348.patch
Patch5:    CVE-2022-39348-1.patch

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-incremental
BuildRequires:  python-zope-interface
BuildRequires:  python-cryptography
BuildRequires:  pyOpenSSL
BuildRequires:  python-six
%if %{with_check}
BuildRequires:  net-tools
BuildRequires:  shadow-utils
BuildRequires:  sudo
%endif
Requires:       python2
Requires:       python2-libs
Requires:       python-zope-interface
Requires:       python-netaddr
Requires:       python-incremental
Requires:       python-constantly
Requires:       python-hyperlink
Requires:       python-attrs

%description
Twisted is an event-driven networking engine written in Python and licensed under the open source ​MIT license. Twisted runs on Python 2 and an ever growing subset also works with Python 3.

Twisted also supports many common network protocols, including SMTP, POP3, IMAP, SSHv2, and DNS.

%prep
%autosetup -p 1 -n Twisted-%{version}

%build
python2 setup.py build

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
sed -i '/dump_all_version_info.py/d' tox.ini
easy_install_2=$(ls /usr/bin |grep easy_install |grep 2)
route add -net 224.0.0.0 netmask 240.0.0.0 dev lo
$easy_install_2 pip==20.3.4
pip install --upgrade tox
chmod g+w . -R
useradd test -G root -m
LANG=en_US.UTF-8 sudo -u test tox -e py27-alldeps-nocov,

%files
%defattr(-,root,root)
%license LICENSE
%{python2_sitelib}/*
%{_bindir}/twistd
%{_bindir}/trial
%{_bindir}/tkconch
%{_bindir}/pyhtmlizer
%{_bindir}/twist
%{_bindir}/mailmail
%{_bindir}/conch
%{_bindir}/ckeygen
%{_bindir}/cftp

%changelog
* Wed Jan 04 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 20.3.0-5
- Add patch for CVE-2022-39348

* Wed Nov 09 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 20.3.0-4
- Moved Python 3 version to a separate package.

* Wed Jun 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 20.3.0-3
- Patch CVE-2022-24801

* Sun Feb 20 2022 Mariner Autopatcher <cblmargh@microsoft.com> 20.3.0-2
- Added patch file(s) CVE-2022-21712.patch

* Fri Jul 30 2021 Thomas Crain <thcrain@microsoft.com> - 20.3.0-1
- Upgrade to version 20.3.0 to fix CVE-2020-10108, CVE-2020-10109
- Use %%autosetup instead of %%setup and %%patch

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
