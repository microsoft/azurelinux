# The function of bootstrap is that it disables the wheel subpackage
%bcond_with bootstrap
%global pypi_name wheel
%bcond main_python 1
Summary:        Built-package format for Python
Name:           python-%{pypi_name}
Version:        0.46.3
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/pypa/wheel
Source0:        %{url}/archive/%{version}/%{pypi_name}-%{version}.tar.gz
Patch0:         Use-vendored-packaging-to-canonicalize-requirements.patch
%global pypi_name wheel
%global python_wheel_name %{pypi_name}-%{version}-py3-none-any.whl
%global python_wheeldir %{_datadir}/python-wheels
%global _description \
A built-package format for Python.\
\
A wheel is a ZIP-format archive with a specially formatted filename and the\
.whl extension. It is designed to contain all the files for a PEP 376\
compatible install in a way that is very close to the on-disk format.
BuildArch:      noarch
%{?python_enable_dependency_generator}
%if 0%{?with_check}
# several tests compile extensions
# those tests are skipped if gcc is not found
BuildRequires:  gcc
%endif

%description %{_description}

%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pip
%if 0%{?with_check}
BuildRequires:  python3-atomicwrites
BuildRequires:  python3-attrs
BuildRequires:  python3-pytest
BuildRequires:  python3-six
%endif
BuildRequires:  python3-flit-core

%description -n python3-%{pypi_name} %{_description}

Python 3 version.

%if %{without bootstrap}
%package wheel
Summary:        The Python wheel module packaged as a wheel

%description wheel
A Python wheel of wheel to use with virtualenv.
%endif

%prep
%autosetup -n %{pypi_name}-%{version} -p1

# flit_core expects [project].license to be a table/dict, not a string
sed -i 's/^license = "MIT"$/license = { text = "MIT" }/' pyproject.toml

%generate_buildrequires
%pyproject_buildrequires

%build
%global _pyproject_wheeldir dist
%python3 -m flit_core.wheel

%pyproject_wheel

%install
# pip is not available when bootstrapping, so we need to unpack the wheel and
# create the entrypoints manually.
%if %{with bootstrap}
mkdir -p %{buildroot}%{python3_sitelib}
unzip %{_pyproject_wheeldir}/%{python_wheel_name} \
    -d %{buildroot}%{python3_sitelib} -x wheel-%{version}.dist-info/RECORD
install -Dpm 0755 %{SOURCE1} %{buildroot}%{_bindir}/wheel
%py3_shebang_fix %{buildroot}%{_bindir}/wheel
%else
%pyproject_install
%endif

mv %{buildroot}%{_bindir}/%{pypi_name}{,-%{python3_version}}
%if %{with main_python}
ln -s %{pypi_name}-%{python3_version} %{buildroot}%{_bindir}/%{pypi_name}-3
ln -s %{pypi_name}-3 %{buildroot}%{_bindir}/%{pypi_name}
%endif

mkdir -p %{buildroot}%{python_wheel_dir}
install -p %{_pyproject_wheeldir}/%{python_wheel_name} -t %{buildroot}%{python_wheel_dir}

%check
pip3 install iniconfig
# Smoke test
%{py3_test_envvars} wheel-%{python3_version} version
%py3_check_import wheel
%pytest -v --ignore build

%files -n python3-%{pypi_name}
%license LICENSE.txt
%doc README.rst
%{_bindir}/%{pypi_name}-%{python3_version}
%{python3_sitelib}/%{pypi_name}*
%if %{with main_python}
%{_bindir}/%{pypi_name}
%{_bindir}/%{pypi_name}-3
%endif

%if %{without bootstrap}
%files wheel
%license LICENSE.txt
# we own the dir for simplicity
%dir %{python_wheeldir}/
%{python_wheeldir}/%{python_wheel_name}
%endif

%changelog
* Wed Jan 28 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 0.46.3-1
- Updated to 0.46.3 to fix CVE-2026-24049

* Fri May 10 2024 Betty Lakes <bettylakes@microsoft.com> - 0.43.0-1
- Updated to 0.43.0

* Thu Mar 03 2022 Bala <balakumaran.kannan@microsoft.com> - 0.33.6-7
- BR multiple python3 modules for PTest
- pip3 install additional modules which not available as RPM

* Mon Feb 14 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.33.6-6
- License verified.

* Mon Nov 01 2021 Muhammad Falak <mwani@microsft.com> - 0.33.6-5
- Remove epoch

* Wed Nov 04 2020 Joe Schmitt <joschmit@microsoft.com> - 1:0.33.6-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Remove bootstrap code.

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.33.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Sep 09 2019 Miro Hrončok <mhroncok@redhat.com> - 1:0.33.6-2
- Drop python2-wheel

* Tue Aug 27 2019 Miro Hrončok <mhroncok@redhat.com> - 1:0.33.6-1
- Update to 0.33.6 (#1708194)
- Don't add the m ABI flag to wheel names on Python 3.8

* Thu Aug 15 2019 Miro Hrončok <mhroncok@redhat.com> - 1:0.33.1-5
- Rebuilt for Python 3.8

* Wed Aug 14 2019 Miro Hrončok <mhroncok@redhat.com> - 1:0.33.1-4
- Bootstrap for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.33.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 16 2019 Miro Hrončok <mhroncok@redhat.com> - 1:0.33.1-2
- Make /usr/bin/wheel Python 3

* Mon Feb 25 2019 Charalampos Stratakis <cstratak@redhat.com> - 1:0.33.1-1
- Update to 0.33.1

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.32.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Sep 30 2018 Miro Hrončok <mhroncok@redhat.com> - 1:0.32.0-1
- Update to 0.32.0

* Wed Aug 15 2018 Miro Hrončok <mhroncok@redhat.com> - 1:0.31.1-3
- Create python-wheel-wheel package with the wheel of wheel

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.31.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jul 07 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1:0.31.1-1
- Update to 0.31.1

* Mon Jun 18 2018 Miro Hrončok <mhroncok@redhat.com> - 1:0.30.0-3
- Rebuilt for Python 3.7

* Wed Jun 13 2018 Miro Hrončok <mhroncok@redhat.com> - 1:0.30.0-2
- Bootstrap for Python 3.7

* Fri Feb 23 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1:0.30.0-1
- Update to 0.30.0

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.30.0a0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Aug 29 2017 Tomas Orsava <torsava@redhat.com> - 0.30.0a0-8
- Switch macros to bcond's and make Python 2 optional to facilitate building
  the Python 2 and Python 3 modules

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.30.0a0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.30.0a0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 03 2017 Charalampos Stratakis <cstratak@redhat.com> - 0.30.0a0-5
- Enable tests

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 0.30.0a0-4
- Rebuild for Python 3.6 without tests

* Tue Dec 06 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.30.0a0-3
- Add bootstrap method

* Mon Sep 19 2016 Charalampos Stratakis <cstratak@redhat.com> - 0.30.0a0-2
- Use the python_provide macro

* Mon Sep 19 2016 Charalampos Stratakis <cstratak@redhat.com> - 0.30.0a0-1
- Update to 0.30.0a0
- Added patch to remove keyrings.alt dependency

* Wed Aug 10 2016 Igor Gnatenko <ignatenko@redhat.com> - 0.29.0-1
- Update to 0.29.0
- Cleanups and fixes

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.26.0-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.26.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Oct 13 2015 Robert Kuska <rkuska@redhat.com> - 0.26.0-1
- Update to 0.26.0
- Rebuilt for Python3.5 rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.24.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jan 13 2015 Slavek Kabrda <bkabrda@redhat.com> - 0.24.0-3
- Make spec buildable in EPEL 6, too.
- Remove additional sources added to upstream tarball.

* Sat Jan 03 2015 Matej Cepl <mcepl@redhat.com> - 0.24.0-2
- Make python3 conditional (switched off for RHEL-7; fixes #1131111).

* Mon Nov 10 2014 Slavek Kabrda <bkabrda@redhat.com> - 0.24.0-1
- Update to 0.24.0
- Remove patches merged upstream

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Apr 25 2014 Matej Stuchlik <mstuchli@redhat.com> - 0.22.0-3
- Another rebuild with python 3.4

* Fri Apr 18 2014 Matej Stuchlik <mstuchli@redhat.com> - 0.22.0-2
- Rebuild with python 3.4

* Thu Nov 28 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.22.0-1
- Initial package.
