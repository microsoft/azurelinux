%global common_description %{expand:
Twisted is a networking engine written in Python, supporting numerous protocols.
It contains a web server, numerous chat clients, chat servers, mail servers
and more.}

Summary:        Twisted is a networking engine written in Python
Name:           python-twisted
Version:        24.11.0
Release:        3%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Languages/Python
URL:            https://twisted.org/
Source0:        https://github.com/twisted/twisted/archive/refs/tags/twisted-%{version}.tar.gz#/twisted-%{version}.tar.gz
# Disable tests that fail in the AzureLinux build system
Patch0:         Disable-multicast-and-ssl-tests.patch
Patch1:         CVE-2026-42304.patch

BuildArch:      noarch

%description %{common_description}

%package -n python3-twisted
Summary:        %{summary}

BuildRequires:  git-core
BuildRequires:  python3-devel >= 3.8
BuildRequires:  python3-bcrypt
BuildRequires:  python3-cryptography
BuildRequires:  python3-hypothesis
BuildRequires:  python3-pyasn1-modules
BuildRequires:  python3-pyOpenSSL
BuildRequires:  python3-pynacl
BuildRequires:  python3-subunit

BuildRequires:  python3-pip
BuildRequires:  python3-hatchling
BuildRequires:  python3-hatch-fancy-pypi-readme
BuildRequires:  python3-incremental
BuildRequires:  python3-pathspec
BuildRequires:  python3-pluggy
BuildRequires:  python3-trove-classifiers
BuildRequires:  shadow-utils
BuildRequires:  net-tools
BuildRequires:  sudo
BuildRequires:  tzdata
Recommends:     python3-twisted+tls

%description -n python3-twisted %{common_description}

%pyproject_extras_subpkg -n python3-twisted tls

%prep
%autosetup -p 1 -n twisted-twisted-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
mkdir -p %{buildroot}%{_mandir}/man1/
for s in conch core mail; do
  cp -a docs/$s/man/*.1 %{buildroot}%{_mandir}/man1/
done

mkdir -p %{buildroot}%{python3_sitelib}/twisted/plugins

ln -s ./trial  %{buildroot}%{_bindir}/trial-3
ln -s ./twistd %{buildroot}%{_bindir}/twistd-3

%pyproject_save_files twisted 
echo "%ghost %{python3_sitelib}/twisted/plugins/dropin.cache" >> %{pyproject_files}

%check
export TZ=UTC
route add -net 224.0.0.0 netmask 240.0.0.0 dev lo
chmod g+w . -R
useradd test -G root -m
sudo -u test pip3 install --user --upgrade pip
sudo -u test pip3 install --user packaging==23.2 'tox>=3.27.1,<4.0.0' PyHamcrest cython-test-exception-raiser py
chmod g+w . -R
LANG=en_US.UTF-8 sudo -u test /home/test/.local/bin/tox -e nocov-posix-alldeps

%files -n python3-twisted -f %{pyproject_files}
%doc NEWS.rst README.rst
%license LICENSE
%{_bindir}/cftp
%{_bindir}/ckeygen
%{_bindir}/conch
%{_bindir}/mailmail
%{_bindir}/pyhtmlizer
%{_bindir}/tkconch
%{_bindir}/trial
%{_bindir}/twist
%{_bindir}/twistd
%{_bindir}/trial-3
%{_bindir}/twistd-3
%{_mandir}/man1/cftp.1*
%{_mandir}/man1/ckeygen.1*
%{_mandir}/man1/conch.1*
%{_mandir}/man1/mailmail.1*
%{_mandir}/man1/pyhtmlizer.1*
%{_mandir}/man1/tkconch.1*
%{_mandir}/man1/trial.1*
%{_mandir}/man1/twistd.1*

%changelog
* Tue Jun 02 2026 Aditya Singh <v-aditysing@microsoft.com> - 24.11.0-3
- Initial AzureLinux import from Fedora (License MIT).
- License verified.
- Patch for  CVE-2026-42304

* Thu May 14 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 22.10.0-5
- Patch for CVE-2026-42304

* Mon Feb 03 2025 Jyoti Kanase <v-jykanase@microsoft.com> - 22.10.0-4
- Fix CVE-2023-46137

* Thu Aug 01 2024 Sindhu Karri <lakarri@microsoft.com> - 22.10.0-3
- Fix CVE-2024-41671 and CVE-2024-41810 with patches

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

* Fri Dec 03 2021 Thomas Crain <thcrain@microsoft.com> - 19.2.1-8
- Replace easy_install usage with pip in %%check sections

* Wed Oct 20 2021 Thomas Crain <thcrain@microsoft.com> - 19.2.1-7
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
