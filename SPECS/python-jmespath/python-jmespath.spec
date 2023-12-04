Summary:        Query Language for JSON
Name:           python-jmespath
Version:        1.0.1
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://pypi.python.org/pypi/jmespath
Source0:        https://github.com/jmespath/jmespath.py/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if %{with_check}
BuildRequires:  python3-pip
%endif
BuildArch:      noarch

%description
JMESPath (pronounced “james path”) allows you to declaratively specify how to extract elements from a JSON document.

%package -n     python3-jmespath
Summary:        Query Language for JSON
Requires:       python3

%description -n python3-jmespath
JMESPath (pronounced “james path”) allows you to declaratively specify how to extract elements from a JSON document.

%prep
%autosetup -n jmespath.py-%{version}

%build
%py3_build

%install
%{py3_install "--single-version-externally-managed"}
ln -sfv jp.py %{buildroot}%{_bindir}/jp.py-%{python3_version}

%check
pip3 install nose mock
%python3 setup.py test

%files -n python3-jmespath
%defattr(-,root,root)
%license LICENSE.txt
%{python3_sitelib}/*
%{_bindir}/jp.py
%{_bindir}/jp.py-%{python3_version}

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.0.1-1
- Auto-upgrade to 1.0.1 - Azure Linux 3.0 - package upgrades

* Mon Mar 14 2022 Thomas Crain <thcrain@microsoft.com> - 0.10.0-1
- Upgrade to latest upstream version
- Switch source from PyPI to GitHub

* Fri Dec 03 2021 Thomas Crain <thcrain@microsoft.com> - 0.9.3-6
- Replace easy_install usage with pip in %%check sections

* Wed Oct 20 2021 Thomas Crain <thcrain@microsoft.com> - 0.9.3-5
- Add license to python3 package
- Remove python2 package
- Lint spec
- License verified

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 0.9.3-4
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 0.9.3-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Wed Nov 28 2018 Tapas Kundu <tkundu@vmware.com> - 0.9.3-2
- Fix make check
- moved the build requires from subpackages

* Sun Jan 07 2018 Kumar Kaushik <kaushikk@vmware.com> - 0.9.3-1
- Initial packaging for photon.
