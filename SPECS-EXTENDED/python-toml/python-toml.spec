%global pypi_name toml
%global desc TOML aims to be a minimal configuration file format that's easy to read due to \
obvious semantics. TOML is designed to map unambiguously to a hash table. TOML \
should be easy to parse into data structures in a wide variety of languages. \
This package loads toml file into python dictionary and dump dictionary into \
toml file. \
This package is deprecated, use tomllib from the Python standard library \
or tomli/tomli-w.

Name:           python-%{pypi_name}
Version:        0.10.2
Release:        21%{?dist}
Summary:        A deprecated Python Library for Tom's Obvious, Minimal Language
Vendor:         Microsoft Corporation
Distribution:   Azure Linux

License:        MIT
URL:            https://pypi.python.org/pypi/%{pypi_name}
Source0:        %{pypi_source}#/%{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel
# python3 bootstrap: this is rebuilt before the final build of python3, which
# adds the dependency on python3-rpm-generators, so we require it manually
# Note that the package prefix is always python3-, even if we build for 3.X
BuildRequires:  python3-rpm-generators
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-wheel
BuildRequires:  python3-pip
%bcond_without tests

%description
%desc


%package -n     python%{python3_pkgversion}-%{pypi_name}
Summary:        %{summary}
# https://fedoraproject.org/wiki/Changes/DeprecatePythonToml
Provides:       deprecated()

%description -n python%{python3_pkgversion}-%{pypi_name}
%desc


%prep
%autosetup -p1 -n %{pypi_name}-%{version}
# https://github.com/uiri/toml/pull/339
sed -i '/pytest-cov/d' tox.ini


%generate_buildrequires
%pyproject_buildrequires %{?with_tests:-t}


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files %{pypi_name}


%check
python3 -m tox -q --recreate -e py312


%files -n python%{python3_pkgversion}-%{pypi_name} -f %{pyproject_files}
%license LICENSE
%doc README.rst


%changelog
* Fri Feb 21 2025 Archana Shettigar <v-shettigara@microsoft.com> - 0.10.2-21
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.2-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 0.10.2-19
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.2-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 0.10.2-12
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Oct 24 2022 Miro Hrončok <mhroncok@redhat.com> - 0.10.2-10
- This package is now deprecated
- https://fedoraproject.org/wiki/Changes/DeprecatePythonToml

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 17 2022 Python Maint <python-maint@redhat.com> - 0.10.2-8
- Rebuilt for Python 3.11

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.10.2-7
- Bootstrap for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.2-5
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 0.10.2-4
- Rebuilt for Python 3.10

* Wed Jun 02 2021 Python Maint <python-maint@redhat.com> - 0.10.2-3
- Bootstrap for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Nov 23 2020 Miro Hrončok <mhroncok@redhat.com> - 0.10.2-1
- Update to 0.10.2
- Fixes: rhbz#1893498

* Fri Nov 13 2020 Miro Hrončok <mhroncok@redhat.com> - 0.10.1-4
- Don't BR pytest-cov

* Thu Sep 03 2020 Miro Hrončok <mhroncok@redhat.com> - 0.10.1-3
- Use pyproject-rpm-macros

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 19 2020 Miro Hrončok <mhroncok@redhat.com> - 0.10.1-1
- Update to 0.10.1 (#1835567)

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 0.10.0-8
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.10.0-6
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 0.10.0-5
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Feb 11 2019 Miro Hrončok <mhroncok@redhat.com> - 0.10.0-3
- Subpackage python2-toml has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Nov 25 2018 Julien Enselme <jujens@jujens.eu> - 0.10.0-1
- Update to 0.10.0 (#1652946)

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.9.4-4
- Rebuilt for Python 3.7

* Wed Feb 21 2018 Sayan Chowdhury <sayanchowdhury@fedoraproject.org> - 0.9.4-3
- Make changes to build the package for EPEL

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Dec 27 2017 Julien Enselme <jujens@jujens.eu> - 0.9.4-1
- Update to 0.9.4

* Tue Sep 26 2017 Julien Enselme <jujens@jujens.eu> - 0.9.3-1
- Update to 0.9.3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.9.2-2
- Rebuild for Python 3.6

* Thu Sep 01 2016 Julien Enselme <jujens@jujens.eu> - 0.9.2-1
- Update to 0.9.2
- Improve spec with %%summary and %%desc macros

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-7
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Nov 11 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Mon Nov 9 2015 Julien Enselme <jujens@jujens.eu> - 0.9.1-4
- Correct %%python_provides for python3

* Thu Nov 5 2015 Julien Enselme <jujens@jujens.eu> - 0.9.1-3
- Rebuilt for python 3.5

* Sat Aug 8 2015 Julien Enselme <jujens@jujens.eu> - 0.9.1-2
- Enable tests suite
- Build python3 and python2 in the same directory
- Use %%py2_build, %%py3_build, %%py2_install and %%py2_install
- Move python2 package in its own subpackage

* Sat Jul 11 2015 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 0.9.1-1
- Update to 0.9.1 (#1242131)

* Sun Jun 28 2015 Julien Enselme <jujens@jujens.eu> - 0.9.0-2
- Update description to explain what toml is
- Try to import the package in %%check

* Mon Jun 15 2015 Julien Enselme <jujens@jujens.eu> - 0.9.0-1
- Initial packaging

## END: Generated by rpmautospec
