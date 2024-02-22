Summary:        A configurable sidebar-enabled Sphinx theme
Name:           python-sphinx-theme-alabaster
Version:        0.7.16
Release:        1%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Languages/Python
URL:            https://github.com/bitprophet/alabaster/
Source0:        https://codeload.github.com/sphinx-doc/alabaster/tar.gz/refs/tags/%{version}
BuildArch:      noarch

%description
Alabaster is a visually (c)lean, responsive, configurable theme for the Sphinx documentation system. It is Python 2+3 compatible.

%package -n     python3-sphinx-theme-alabaster
Summary:        A configurable sidebar-enabled Sphinx theme
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-libs

%description -n python3-sphinx-theme-alabaster
Alabaster is a visually (c)lean, responsive, configurable theme for the Sphinx documentation system. It is Python 2+3 compatible.

%prep
%autosetup -n alabaster-%{version}

%build
%py3_build

%install
%py3_install

%files -n python3-sphinx-theme-alabaster
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Wed Feb 21 2024 Nadiia Dubchak <ndubchak@microsoft.com> - 0.7.16-1
- Upgrade to 0.7.16 as part of Mariner 3.0 package upgrades.

* Fri Mar 25 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.7.12-1
- Updating to version 0.7.12.
- Removed invalid '%%check' section.

* Wed Oct 20 2021 Thomas Crain <thcrain@microsoft.com> - 0.7.11-6
- Add license to python3 package
- Remove python2 package
- Lint spec

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 0.7.11-5
- Added %%license line automatically

* Tue Apr 28 2020 Emre Girgin <mrgirgin@microsoft.com> - 0.7.11-4
- Renaming python-alabaster to python-sphinx-theme-alabaster

* Mon Apr 13 2020 Jon Slobodizan <joslobo@microsoft.com> - 0.7.11-3
- Verified license.  Fixed Source0 download link. Remove sha1 define.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 0.7.11-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> - 0.7.11-1
- Update to version 0.7.11

* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> - 0.7.10-3
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.

* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> - 0.7.10-2
- Changed python to python2

* Tue Apr 25 2017 Dheeraj Shetty <dheerajs@vmware.com> - 0.7.10-1
- Initial
