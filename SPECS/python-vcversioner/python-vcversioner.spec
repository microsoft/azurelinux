%define LICENSE_PATH COPYING
Summary:        Python version extractor
Name:           python-vcversioner
Version:        2.16.0.0
Release:        6%{?dist}
License:        ISC
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://github.com/habnabit/vcversioner
# Using the pypi tarball because building this rpm doesn't work with tarball from github.
#Source0:       https://pypi.python.org/packages/source/v/vcversioner/vcversioner-2.16.0.0.tar.gz
Source0:        vcversioner-%{version}.tar.gz
Source1:        https://raw.githubusercontent.com/habnabit/vcversioner/%{version}/%{LICENSE_PATH}
BuildArch:      noarch

%description
Elevator pitch: you can write a setup.py with no version information specified, and vcversioner will find a recent, properly-formatted VCS tag and extract a version from it.

%package -n     python3-vcversioner
Summary:        Python version extractor
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3

%description -n python3-vcversioner
Elevator pitch: you can write a setup.py with no version information specified, and vcversioner will find a recent, properly-formatted VCS tag and extract a version from it.

%prep
%autosetup -n vcversioner-%{version}
cp %{SOURCE1} .

%build
%py3_build

%install
%py3_install

%check
%python3 setup.py test

%files -n python3-vcversioner
%license %{LICENSE_PATH}
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Tue Feb 08 2022 Muhammad Falak <mwani@microsoft.com> - 2.16.0.0-6
- Fix typo `s/setup/setup.py/` in `%check` section to enable ptest

* Wed Oct 20 2021 Olivia Crain <oliviacrain@microsoft.com> - 2.16.0.0-5
- Add license to python3 package
- Remove python2 package
- Lint spec

* Fri May 29 2020 Mateusz Malisz <mamalisz@microsoft.com> - 2.16.0.0-4
- Add quiet option to setup.
- Add %%license macro.
- Add COPYING file.

* Wed May 06 2020 Paul Monson <paulmon@microsoft.com> - 2.16.0.0-3
- Restore vcversioner
- Url verified.
- License verified.
- Fix Source0.

* Thu Aug 08 2019 Mateusz Malisz <mamalisz@microsoft.com> - 2.16.0.0-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue Oct 23 2018 Sujay G <gsujay@vmware.com> - 2.16.0.0-1
- Initial version
