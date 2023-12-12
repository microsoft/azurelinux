Vendor:         Microsoft Corporation
Distribution:   Mariner
# While the headers are architecture independent, the package must be
# built separately on all architectures so that the tests are run
# properly. See also
# https://fedoraproject.org/wiki/Packaging:Guidelines#Packaging_Header_Only_Libraries
%global debug_package %{nil}

Name:    pybind11
Version: 2.6.2
Release: 3%{?dist}
Summary: Seamless operability between C++11 and Python
License: BSD
URL:	 https://github.com/pybind/pybind11
Source0: https://github.com/pybind/pybind11/archive/v%{version}/%{name}-%{version}.tar.gz

# Patch out header path
Patch1:  pybind11-2.6.1-hpath.patch

BuildRequires: make

# Needed to build the python libraries
BuildRequires: python3-devel
BuildRequires: python3-setuptools
# These are only needed for the checks
%if %{with_check}
BuildRequires: python3-pytest
BuildRequires: python3-numpy

# Missing test dependencies:
# BuildRequires: python3-scipy
%endif

BuildRequires: gcc-c++
BuildRequires: cmake

%global base_description \
pybind11 is a lightweight header-only library that exposes C++ types \
in Python and vice versa, mainly to create Python bindings of existing \
C++ code.

%description
%{base_description}

%package devel
Summary:  Development headers for pybind11
# https://fedoraproject.org/wiki/Packaging:Guidelines#Packaging_Header_Only_Libraries
Provides: %{name}-static = %{version}-%{release}
# For dir ownership
Requires: cmake

%description devel
%{base_description}

This package contains the development headers for pybind11.

%package -n     python3-%{name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-pybind11}

Requires: %{name}-devel%{?_isa} = %{version}-%{release}

%description -n python3-%{name}
%{base_description}

This package contains the Python 3 files.

%prep
%setup -q
%patch1 -p1 -b .hpath

%build
pys=""
pys="$pys python3"
for py in $pys; do
    mkdir $py
    %cmake -B $py -DCMAKE_BUILD_TYPE=Release -DPYTHON_EXECUTABLE=%{_bindir}/$py -DPYBIND11_INSTALL=TRUE -DUSE_PYTHON_INCLUDE_DIR=FALSE %{!?with_tests:-DPYBIND11_TEST=OFF}
    %make_build -C $py
done

%py3_build

%check
make -C python3 check %{?_smp_mflags}

%install
%make_install -C python3
# Force install to arch-ful directories instead.
PYBIND11_USE_CMAKE=true %py3_install "--install-purelib" "%{python3_sitearch}"

%files devel
%license LICENSE
%doc README.rst
%{_includedir}/pybind11/
%{_datadir}/cmake/pybind11/
%{_bindir}/pybind11-config

%files -n python3-%{name}
%{python3_sitearch}/%{name}/
%{python3_sitearch}/%{name}-%{version}-py%{python3_version}.egg-info

%changelog
* Thu Aug 31 2023 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.6.2-3
- Disabling missing test dependency.
- License verified.

* Thu Sep 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.6.2-2
- Initial CBL-Mariner import from Fedora 34 (license: MIT).
- Removing Python 2 build steps. Focusing on Python 3.
- Removed BR on "eigen3-devel" - unused.

* Wed Jan 27 2021 Susi Lehtola <jussilehtola@fedoraproject.org> - 2.6.2-1
- Update to 2.6.2.

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Nov 12 2020 Susi Lehtola <jussilehtola@fedoraproject.org> - 2.6.1-1
- Update to 2.6.1.

* Wed Aug 12 2020 Merlin Mathesius <mmathesi@redhat.com> - 2.5.0-5
- Drop Python 2 support for ELN and RHEL9+

* Wed Aug 05 2020 Susi Lehtola <jussilehtola@fedoraproject.org> - 2.5.0-6
- Adapt to new CMake macros.

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-5
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 2.5.0-3
- Rebuilt for Python 3.9

* Mon May 25 2020 Miro Hrončok <mhroncok@redhat.com> - 2.5.0-2
- Bootstrap for Python 3.9

* Wed Apr 01 2020 Susi Lehtola <jussilehtola@fedoraproject.org> - 2.5.0-1
- Update to 2.5.0.

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Oct 15 2019 Susi Lehtola <jussilehtola@fedoraproject.org> - 2.4.3-1
- Update to 2.4.3.

* Tue Oct 08 2019 Susi Lehtola <jussilehtola@fedoraproject.org> - 2.4.2-2
- Fix Python 3.8 incompatibility.

* Sat Sep 28 2019 Susi Lehtola <jussilehtola@fedoraproject.org> - 2.4.2-1
- Update to 2.4.2.

* Fri Sep 20 2019 Susi Lehtola <jussilehtola@fedoraproject.org> - 2.4.1-1
- Update to 2.4.1.

* Fri Sep 20 2019 Susi Lehtola <jussilehtola@fedoraproject.org> - 2.4.0-1
- Update to 2.4.0.

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2.3.0-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 10 2019 Susi Lehtola <jussilehtola@fedoraproject.org> - 2.3.0-1
- Update to 2.3.0.

* Fri May 03 2019 Susi Lehtola <jussilehtola@fedoraproject.org> - 2.2.4-3
- Fix incompatibility with pytest 4.0.

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Sep 18 2018 Susi Lehtola <jussilehtola@fedoraproject.org> - 2.2.4-1
- Remove python2 packages for Fedora >= 30.
- Update to 2.2.4.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 23 2018 Miro Hrončok <mhroncok@redhat.com> - 2.2.3-2
- Rebuilt for Python 3.7

* Fri Jun 22 2018 Susi Lehtola <jussilehtola@fedoraproject.org> - 2.2.3-1
- Update to 2.2.3.

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 2.2.2-4
- Rebuilt for Python 3.7

* Mon Apr 16 2018 Susi Lehtola <jussilehtola@fedorapeople.org> - 2.2.2-3
- Add Python subpackages based on Elliott Sales de Andrade's patch.

* Sat Feb 17 2018 Susi Lehtola <jussilehtola@fedorapeople.org> - 2.2.2-2
- Fix FTBS by patch from upstream.

* Wed Feb 14 2018 Susi Lehtola <jussilehtola@fedorapeople.org> - 2.2.2-1
- Update to 2.2.2.

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Dec 14 2017 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.2.1-1
- Update to latest version
- Update Source URL to include project name.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Feb 27 2017 Susi Lehtola <jussilehtola@fedorapeople.org> - 2.0.1-5
- Full compliance with header only libraries guidelines.

* Thu Feb 23 2017 Susi Lehtola <jussilehtola@fedorapeople.org> - 2.0.1-4
- As advised by upstream, disable dtypes test for now.
- Include patch for tests on bigendian systems.

* Thu Feb 23 2017 Susi Lehtola <jussilehtola@fedorapeople.org> - 2.0.1-3
- Make the package arched so that tests can be run on all architectures.
- Run tests both against python2 and python3.

* Wed Feb 22 2017 Susi Lehtola <jussilehtola@fedorapeople.org> - 2.0.1-2
- Switch to python3 for tests.

* Sun Feb 05 2017 Susi Lehtola <jussilehtola@fedorapeople.org> - 2.0.1-1
- First release.
