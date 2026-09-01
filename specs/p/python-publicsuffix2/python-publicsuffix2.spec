# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pypi_name publicsuffix2

%global desc This module allows you to get the public suffix, as well as the registrable\
domain, of a domain name using the Public Suffix List from\
http://publicsuffix.org\
\
This module builds the public suffix list as a Trie structure, making it more\
efficient than other string-based modules available for the same purpose. It can\
be used effectively in large-scale distributed environments, such as PySpark.\
\
The code is a fork of the publicsuffix package and includes the same base API.\
In addition, it contains a few variants useful for certain use cases, such as\
the option to ignore wildcards or return only the extended TLD (eTLD). You just\
need to import publicsuffix2 instead.

Name: python-%{pypi_name}
Version: 2.20191221
Release: 21%{?dist}
Summary: Get a public suffix for a domain name using the Public Suffix List
License: MIT
URL: https://github.com/nexb/python-publicsuffix2
Source0: %{pypi_source}
BuildArch: noarch

%description
%{desc}

%package -n python3-%{pypi_name}
Summary: %{summary}
BuildRequires: python3-devel
Requires: publicsuffix-list

%description -n python3-%{pypi_name}
%{desc}

%prep
%autosetup -p1 -n %{pypi_name}-%{version}
rm -r src/%{pypi_name}.egg-info

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -L %{pypi_name}
rm %{buildroot}%{python3_sitelib}/%{pypi_name}/public_suffix_list.dat
ln -s ../../../../share/publicsuffix/public_suffix_list.dat %{buildroot}%{python3_sitelib}/%{pypi_name}

%files -n python3-%{pypi_name} -f %{pyproject_files}
%license %{pypi_name}.LICENSE
%doc README.rst

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 2.20191221-21
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 2.20191221-20
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.20191221-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 21 2025 Dominik Mierzejewski <dominik@greysector.net> 2.20191221-18
- switch to modern python packaging macros (resolves rhbz#2378011)

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 2.20191221-17
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.20191221-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.20191221-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 2.20191221-14
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.20191221-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.20191221-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.20191221-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 2.20191221-10
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.20191221-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.20191221-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2.20191221-7
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.20191221-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.20191221-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.20191221-4
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.20191221-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.20191221-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 01 2020 Dominik Mierzejewski <dominik@greysector.net> 2.20191221-1
- initial build
- unbundle public_suffix_list.dat file
