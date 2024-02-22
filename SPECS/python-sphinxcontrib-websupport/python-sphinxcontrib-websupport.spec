%define pkgname sphinxcontrib-websupport
Summary:        Python API to integrate Sphinx into a web application
Name:           python-%{pkgname}
Version:        1.2.7
Release:        1%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/sphinx-doc/sphinxcontrib-websupport
Source0:        https://github.com/sphinx-doc/%{pkgname}/archive/%{version}.tar.gz#/%{pkgname}-%{version}.tar.gz
BuildArch:      noarch

%description
Python API to integrate Sphinx into a web application

%package -n     python3-%{pkgname}
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  python-flit-core
%if %{with check}
BuildRequires:  python-packaging
%endif

Requires:       python3
Requires:       python3-sphinxcontrib-serializinghtml

%description -n python3-%{pkgname}
The python-sphinxcontrib-websupport package provides a Python API to easily integrate Sphinx documentation into your Web application.

%pyproject_extras_subpkg -n python3-%{pkgname} whoosh

%prep
%autosetup -n %{pkgname}-%{version} -p 1

%generate_buildrequires
%pyproject_buildrequires -t

%build
%pyproject_wheel
%install
%pyproject_install
%pyproject_save_files sphinxcontrib

%check
%tox
%files -n python3-%{pkgname} -f %{pyproject_files}
%license LICENSE
%doc README.rst

%changelog
* Mon Feb 19 2024 Karim Eldegwy <karimeldegwy@microsoft.com> - 1.2.7-1
- Auto-upgrade to 1.2.7 - 3.0 - Upgrade
- Use pypi macros

* Wed Apr 27 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2.4-3
- Updating source URL.

* Sun Mar 27 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2.4-2
- Adding a dependency on "python3-sphinxcontrib-serializinghtml".

* Fri Mar 25 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2.4-1
- Updating to version 1.2.4.

* Wed Oct 20 2021 Thomas Crain <thcrain@microsoft.com> - 0.5.0-2
- Remove python2 package
- Lint spec

* Fri Aug 21 2020 Thomas Crain <thcrain@microsoft.com> - 0.5.0-1
- Original version for CBL-Mariner.
- License verified.
