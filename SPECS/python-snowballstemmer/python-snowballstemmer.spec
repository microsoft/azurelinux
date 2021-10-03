Summary:        Python stemming library
Name:           python-snowballstemmer
Version:        1.2.1
Release:        5%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://github.com/shibukawa/snowball_py
Source0:        https://pypi.python.org/packages/20/6b/d2a7cb176d4d664d94a6debf52cd8dbae1f7203c8e42426daa077051d59c/snowballstemmer-%{version}.tar.gz

%description
This package provides 16 stemmer algorithms (15 + Poerter English stemmer) generated from Snowball algorithms.

%package -n     python3-snowballstemmer
Summary:        Python stemming library
BuildRequires:  python3
BuildRequires:  python3-devel
Requires:       python3
Requires:       python3-libs

%description -n python3-snowballstemmer
This package provides 16 stemmer algorithms (15 + Poerter English stemmer) generated from Snowball algorithms.
It includes following language algorithms:

* Danish
* Dutch
* English (Standard, Porter)
* Finnish
* French
* German
* Hungarian
* Italian
* Norwegian
* Portuguese
* Romanian
* Russian
* Spanish
* Swedish
* Turkish

%prep
%autosetup -n snowballstemmer-%{version}

%build
%py3_build

%install
%py3_install

%check
%make_build -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%files -n python3-snowballstemmer
%defattr(-,root,root,-)
%license LICENSE.rst
%{python3_sitelib}/*

%changelog
* Fri Oct 01 2021 Thomas Crain <thcrain@microsoft.com> - 1.1.0-7
- Add license to python3 package
- Remove python2 package
- Lint spec

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.2.1-4
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 1.2.1-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> - 1.2.1-2
- Use python2 explicitly

* Tue Apr 25 2017 Dheeraj Shetty <dheerajs@vmware.com> - 1.2.1-1
- Initial
