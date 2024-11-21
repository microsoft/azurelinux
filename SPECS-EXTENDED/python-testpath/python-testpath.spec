%global pypi_name testpath

Summary:        Test utilities for code working with files and commands
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           python-%{pypi_name}
Version:        0.5.0
Release:        4%{?dist}
License:        MIT
URL:            https://github.com/jupyter/testpath
Source0:        %pypi_source
BuildArch:      noarch

BuildRequires:  python3-pip
BuildRequires:  python3-devel
BuildRequires:  python3-flit
BuildRequires:  python3-sphinx
BuildRequires:  python3-sphinx_rtd_theme

%if 0%{?with_check}
# Tests:
BuildRequires:  python3-pytest
%endif

%global _description \
Testpath is a collection of utilities for Python code working with files and \
commands. \
\
It contains functions to check things on the filesystem, and tools for \
mocking system commands and recording calls to those.

%description %_description

%package -n     python3-%{pypi_name}
Summary:        %summary
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}

%_description

%package        doc
Summary:        %{name} documentation
%description doc
Documentation for %{name}.


%prep
%autosetup -n %{pypi_name}-%{version}

# The exe files are only needed on Microsoft Windows
rm -f %{pypi_name}/*.exe

%build
# this package has no setup.py
# and upstream does not want one
# https://github.com/takluyver/flit/issues/74
# we use flit to create a wheel from sources
flit build --format wheel

# generate html docs
sphinx-build-3 doc html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}


%install
# We install the wheel created at %%build
%py3_install_wheel %{pypi_name}-%{version}-py3-none-any.whl



%check
%{__python3} -m pytest -v


%files -n python3-%{pypi_name}
%doc README.rst
%license LICENSE
%{python3_sitelib}/%{pypi_name}-%{version}.dist-info/
%{python3_sitelib}/%{pypi_name}/

%files doc
%doc html

%changelog
* Fri Mar 03 2023 Muhammad Falak <mwani@microsoft.com> - 0.5.0-4
- Initial CBL-Mariner import from Fedora 36 (license: MIT).
- License verified

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 08 2021 Tomas Hrnciar <thrnciar@redhat.com> - 0.5.0-1
- Update to 0.5.0

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.4.4-5
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 0.4.4-2
- Rebuilt for Python 3.9

* Thu May 14 2020 Tomas Hrnciar <thrnciar@redhat.com> - 0.4.4-1
- Update to 0.4.4

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.3.1-10
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Sun Aug 18 2019 Miro Hrončok <mhroncok@redhat.com> - 0.3.1-9
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 15 2019 Miro Hrončok <mhroncok@redhat.com> - 0.3.1-7
- Subpackage python2-testpath has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.3.1-4
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed May 31 2017 Miro Hrončok <mhroncok@redhat.com> - 0.3.1-1
- New version 0.3.1 (#1455375)
- Uses pathlib2 instead of pathlib

* Wed Mar 08 2017 Miro Hrončok <mhroncok@redhat.com> - 0.3-1
- initial package

