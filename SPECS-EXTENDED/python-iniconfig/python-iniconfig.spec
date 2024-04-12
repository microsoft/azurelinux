Vendor:         Microsoft Corporation
Distribution:   Mariner

%undefine mariner_module_ldflags

Name:               python-iniconfig
Version:            1.1.1
Release:            15%{?dist}
Summary:            Brain-dead simple parsing of ini files
# SDPX
License:            MIT
URL:                http://github.com/RonnyPfannschmidt/iniconfig
BuildArch:          noarch
BuildRequires:      python3-devel
BuildRequires:      pyproject-rpm-macros
BuildRequires:      python3-pip
BuildRequires:      python3-setuptools
BuildRequires:      python3-setuptools_scm
BuildRequires:      python3-six
BuildRequires:      python3-wheel

# pytest 6+ needs this and this uses pytest for tests
%bcond_without tests

%if %{with tests}
# We BR pytest manually to avoid a dependency on tox in ELN/RHEL
BuildRequires:      python3-pytest
%endif

Source0:            %{pypi_source iniconfig}

%global _description %{expand:
iniconfig is a small and simple INI-file parser module
having a unique set of features:

* tested against Python2.4 across to Python3.2, Jython, PyPy
* maintains order of sections and entries
* supports multi-line values with or without line-continuations
* supports "#" comments everywhere
* raises errors with proper line-numbers
* no bells and whistles like automatic substitutions
* iniconfig raises an Error if two sections have the same name.}
%description %_description


%package -n python3-iniconfig
Summary:            %{summary}
%description -n python3-iniconfig %_description


%prep
%autosetup -n iniconfig-%{version}
# Remove undeclared dependency on python-py
# Merged upstream https://github.com/pytest-dev/iniconfig/pull/47
sed -i "s/py\.test/pytest/" testing/test_iniconfig.py


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files iniconfig


%if %{with tests}
%check
%pytest -v
%endif


%files -n python3-iniconfig -f %{pyproject_files}
%doc README.txt
%license LICENSE


%changelog
* Fri Apr 12 2024 Bala <balakumaran.kannan@microsoft.com> - 1.1.1-15
- Initial CBL-Mariner import from Fedora 39 (license: MIT)
- License verified.

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jun 16 2023 Python Maint <python-maint@redhat.com> - 1.1.1-13
- Rebuilt for Python 3.12

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 1.1.1-12
- Bootstrap for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Dec 08 2022 Lumír Balhar <lbalhar@redhat.com> - 1.1.1-10
- Fix build with pytest 7.2 and tox 4

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.1.1-8
- Rebuilt for Python 3.11

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.1.1-7
- Bootstrap for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.1.1-4
- Rebuilt for Python 3.10

* Wed Jun 02 2021 Python Maint <python-maint@redhat.com> - 1.1.1-3
- Bootstrap for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Oct 15 2020 Tomas Hrnciar <thrnciar@redhat.com> - 1.1.1-1
- Update to 1.1.1 (#1888157)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 13 2020 Miro Hrončok <mhroncok@redhat.com> - 1.0.0-1
- Initial package (#1856421)
