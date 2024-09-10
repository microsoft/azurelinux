Summary:        Internationalized Domain Names in Applications (IDNA).
Name:           python-idna
Version:        3.7
Release:        1%{?dist}
License:        BSD-like
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Languages/Python
URL:            https://github.com/kjd/idna
#Source0:       https://github.com/kjd/idna/archive/refs/tags/v%{version}.tar.gz
Source0:        idna-%{version}.tar.gz
BuildArch:      noarch

%description
Support for the Internationalised Domain Names in Applications (IDNA) protocol as specified in RFC 5891.

%package -n     python3-idna
Summary:        Internationalized Domain Names in Applications (IDNA).
BuildRequires:  python-flit-core
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
%if %{with_check}
BuildRequires:  python3-pytest
%endif
%description -n python3-idna
Support for the Internationalised Domain Names in Applications (IDNA) protocol as specified in RFC 5891. This is the latest version of the protocol and is sometimes referred to as “IDNA 2008”.

This library also provides support for Unicode Technical Standard 46, Unicode IDNA Compatibility Processing.

This acts as a suitable replacement for the “encodings.idna” module that comes with the Python standard library, but only supports the old, deprecated IDNA specification (RFC 3490).

%prep
%autosetup -n idna-%{version}
# Remove bundled egg-info
rm -rf idna.egg-info

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files idna

%check
pip3 install iniconfig
%pytest

%files -n python3-idna -f %pyproject_files
%defattr(-,root,root,-)
%license LICENSE.md
%doc README.rst

%changelog
* Tue Jul 23 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.7-1
- Auto-upgrade to 3.7 - CVE-2024-3651

* Mon Feb 26 2024 Osama Esmail <osamaesmail@microsoft.com> - 3.6-1
- Auto-upgrade to 3.6 - Azure Linux 3.0 - package upgrades
- Replacing a lot of macros with %%pyproject...
- Adding README.rst to docs

* Tue Feb 15 2022 Nick Samson <nisamson@microsoft.com> - 3.3-1
- Updated Source0 and license file.
- Updated to 3.3.

* Wed Oct 20 2021 Thomas Crain <thcrain@microsoft.com> - 2.7-5
- Add license to python3 package
- Remove python2 package
- Lint spec

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.7-4
- Added %%license line automatically

* Thu Apr 09 2020 Joe Schmitt <joschmit@microsoft.com> - 2.7-3
- Update URL.
- Update Source0 with valid URL.
- Remove sha1 macro.
- License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 2.7-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> - 2.7-1
- Update to version 2.7

* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> - 2.5-2
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.

* Mon Mar 13 2017 Xiaolin Li <xiaolinl@vmware.com> - 2.5-1
- Initial packaging for Photon
