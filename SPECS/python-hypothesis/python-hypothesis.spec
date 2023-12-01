Summary:        Python library for creating unit tests which are simpler to write and more powerful
Name:           python-hypothesis
Version:        6.36.2
Release:        1%{?dist}
License:        MPLv2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://github.com/HypothesisWorks/hypothesis-python
Source0:        https://files.pythonhosted.org/packages/24/05/d03211fc959ddf8c4a26d04957d9640a86a723f5d6a4359a4430cf5fa0b4/hypothesis-%{version}.tar.gz
BuildArch:      noarch

%description
Hypothesis is an advanced testing library for Python. It lets you write tests which are parametrized by a source of examples,
and then generates simple and comprehensible examples that make your tests fail. This lets you find more bugs in your code with less work

%package -n     python3-hypothesis
Summary:        Python library for creating unit tests which are simpler to write and more powerful
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-libs

%description -n python3-hypothesis

Hypothesis is an advanced testing library for Python. It lets you write tests which are parametrized by a source of examples,
and then generates simple and comprehensible examples that make your tests fail. This lets you find more bugs in your code with less work

%prep
%autosetup -n hypothesis-%{version}

%build
%py3_build

%install
%py3_install

%check
%make_build -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%files -n python3-hypothesis
%defattr(-,root,root,-)
%license LICENSE.txt
%{python3_sitelib}/*
%{_bindir}/*

%changelog
* Tue Feb 15 2022 Nick Samson <nisamson@microsoft.com> - 6.36.2-1
- Updated source URL, updated to 6.36.2
- Added hypothesis binary

* Wed Oct 20 2021 Olivia Crain <oliviacrain@microsoft.com> - 3.71.0-5
- Add license to python3 package
- Remove python2 package
- Lint spec

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 3.71.0-4
- Added %%license line automatically

* Mon Apr 13 2020 Jon Slobodizan <joslobo@microsoft.com> - 3.71.0-3
- Verified license.  Fixed Source0 download link. Remove sha1 define.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 3.71.0-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> - 3.71.0-1
- Update to version 3.71.0

* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> - 3.8.2-3
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.

* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> - 3.8.2-2
- Changed python to python2

* Tue Apr 25 2017 Dheeraj Shetty <dheerajs@vmware.com> - 3.8.2-1
- Initial
