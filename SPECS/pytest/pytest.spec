Summary:        pytest is a mature full-featured Python testing tool that helps you write better programs
Name:           pytest
Version:        7.4.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://docs.pytest.org
Source0:        https://files.pythonhosted.org/packages/a7/f3/dadfbdbf6b6c8b5bd02adb1e08bc9fbb45ba51c68b0893fa536378cdf485/%{name}-%{version}.tar.gz
BuildArch:      noarch

%description
pytest framework makes it easy to write small tests, yet scales to support complex functional testing for applications and libraries.

%package -n     python3-pytest
Summary:        pytest is a mature full-featured Python testing tool that helps you write better programs
BuildRequires:  python3-devel
BuildRequires:  python3-hypothesis
BuildRequires:  python3-py
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm
BuildRequires:  python3-twisted
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-setuptools
Requires:       python3-py
Requires:       python3-attrs
Requires:       python3-atomicwrites
Requires:       python3-pluggy
Requires:       python3-more-itertools
Requires:       python3-six
AutoReqProv:    no
Provides:       python3dist(pytest) = %{version}-%{release}
Provides:       python3.7dist(pytest) = %{version}-%{release}

%description -n python3-pytest
pytest framework makes it easy to write small tests, yet scales to support complex functional testing for applications and libraries.

%prep
%autosetup

%build
%py3_build

%install
%py3_install

mv %{buildroot}%{_bindir}/pytest %{buildroot}%{_bindir}/pytest%{python3_version}
ln -snf pytest%{python3_version} %{buildroot}%{_bindir}/pytest
ln -snf pytest%{python3_version} %{buildroot}%{_bindir}/pytest3

mv %{buildroot}%{_bindir}/py.test %{buildroot}%{_bindir}/py.test%{python3_version}
ln -snf py.test%{python3_version} %{buildroot}%{_bindir}/py.test
ln -snf py.test%{python3_version} %{buildroot}%{_bindir}/py.test3

%check
%make_build -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%files -n python3-pytest
%defattr(-,root,root,-)
%license LICENSE
%{_bindir}/pytest*
%{_bindir}/py.test*
%{python3_sitelib}/*

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 7.4.0-1
- Auto-upgrade to 7.4.0 - Azure Linux 3.0 - package upgrades

* Wed Jan 11 2023 Riken Maharjan <rmaharjan@microsoft.com> - 3.8.2-10
- Adding missing runtime dependencies.

* Fri Mar 25 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.8.2-9
- Adding missing links to `/usr/bin/pytest' and '/usr/bin/py.test' to fix the '%pytest' macro.

* Wed Oct 20 2021 Thomas Crain <thcrain@microsoft.com> - 3.8.2-8
- Add license to python3 package
- Remove python2 package
- Lint spec

* Tue Jan 05 2021 Ruying Chen <v-ruyche@microsoft.com> - 3.8.2-7
- Disable auto dependency generator.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 3.8.2-6
- Added %%license line automatically

* Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> 3.8.2-5
- Renaming python-pytest to pytest

* Tue Apr 28 2020 Emre Girgin <mrgirgin@microsoft.com> 3.8.2-4
- Renaming python-Twisted to python-twisted

* Mon Apr 20 2020 Eric Li <eli@microsoft.com> 3.8.2-3
- Update Source0:, add #Source0, and delete sha1. License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 3.8.2-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue Oct 09 2018 Tapas Kundu <tkundu@vmware.com> 3.8.2-1
- Updated to release 3.8.2
- Removed buildrequires from subpackage.

* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 3.0.7-3
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.

* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.0.7-2
- Use python2 instead of python and rename the scripts in bin directory

* Tue Apr 25 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.0.7-1
- Initial
