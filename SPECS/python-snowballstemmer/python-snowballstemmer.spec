# Note that python-snowballstemmer currently has a package repository on github here: https://github.com/snowballstem/snowball
# The source on github provides "snowball".  The Snowball source generates snowballstemmer for several languages.  
# If you clone and run "make dist" one of the output folders, "python_out", contains the python-snowballstemmer source.   
# This SPEC provides the source from pypi.

Summary:        Python stemming library
Name:           python-snowballstemmer
Version:        2.2.0
Release:        1%{?dist}
License:        BSD-3-Clause
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://snowballstem.org/
Source0:        https://files.pythonhosted.org/packages/44/7b/af302bebf22c749c56c9c3e8ae13190b5b5db37a33d9068652e8f73b7089/snowballstemmer-%{version}.tar.gz#/snowballstemmer-%{version}.tar.gz
BuildArch:      noarch

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
%make_build -k check_python |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%files -n python3-snowballstemmer
%defattr(-,root,root,-)
%license COPYING
%{python3_sitelib}/*

%changelog
* Fri Mar 25 2022 Jon Slobodzian <joslobo@microsoft.com> - 2.2.0-1
- Upgrade to latest version

* Wed Oct 20 2021 Olivia Crain <oliviacrain@microsoft.com> - 1.1.0-7
- Add license to python3 package
- Remove python2 package
- Lint spec
- License verified

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.2.1-4
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 1.2.1-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> - 1.2.1-2
- Use python2 explicitly

* Tue Apr 25 2017 Dheeraj Shetty <dheerajs@vmware.com> - 1.2.1-1
- Initial
