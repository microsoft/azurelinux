# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# without means enabled
%bcond_with doc

# Pythran is an optional build dependency.
# When used, it makes some modules faster,
# but it is usually not available soon enough for new major Python versions.
%if 0%{?rhel}
%bcond_with pythran
%bcond_with pooch
%bcond_with tests
%else
%bcond_without pythran
%bcond_without pooch
%bcond_without tests
%endif

# The code is not safe to build with LTO
%global _lto_cflags %{nil}

%ifarch %{ix86}
# On i686, there is a confusion whether Fortran INTEGER should be
# translated as int or long.
# <https://github.com/scipy/scipy/issues/19993>
%global build_type_safety_c 2
%endif

# Set to pre-release version suffix if building pre-release, else %%{nil}
%global rcver %{nil}

%if 0%{?fedora} >= 33 || 0%{?rhel} >= 9
%global blaslib flexiblas
%global blasvar %{nil}
%else
%global blaslib openblas
%global blasvar p
%endif

%global build_backend_args %{shrink:
    -Csetup-args=-Dblas=%{blaslib}%{blasvar}
    -Csetup-args=-Dlapack=%{blaslib}%{blasvar}
    %{!?with_pythran:-Csetup-args=-Duse-pythran=false}
}

Summary:    Scientific Tools for Python
Name:       scipy
Version:    1.16.2
Release:    1%{?dist}

# BSD-3-Clause -- whole package except:
# BSD-2-Clause -- scipy/_lib/_pep440.py
#                 scipy/_lib/decorator.py
#                 scipy/optimize/lbfgsb_src
#                 scipy/special/_ellip_harm.pxd
# MIT -- scipy/cluster/_optimal_leaf_ordering.pyx
#        scipy/io/_idl.py
#        scipy/linalg/_basic.py (in part)
#        scipy/optimize/_direct
#        scipy/optimize/_highs
#        scipy/optimize/_lbfgsb_py.py
#        scipy/optimize/_tnc.py
#        scipy/optimize/_trlib
#        scipy/optimize/tnc
#        scipy/special/Faddeeva.{cc,hh}
# BSL-1.0 -- scipy/_lib/boost_math
#            scipy/special/cephes
# Boehm-GC -- scipy/sparse/linalg/_dsolve/SuperLU
# Qhull -- scipy/spatial/qhull_src
# LicenseRef-Fedora-Public-Domain -- scipy/odr/__odrpack.c
License:    BSD-3-Clause AND BSD-2-Clause AND MIT AND BSL-1.0 AND Boehm-GC AND Qhull AND LicenseRef-Fedora-Public-Domain
Url:        https://scipy.org/
Source0:    https://github.com/scipy/scipy/releases/download/v%{version}/scipy-%{version}.tar.gz

BuildRequires: %{blaslib}-devel
BuildRequires: gcc-gfortran, gcc-c++

BuildRequires:  pybind11-devel
BuildRequires:  python3-devel, python3-numpy-f2py

# for %%pyproject_buildrequires -p:
BuildRequires:  pyproject-rpm-macros >= 1.15

%ifarch %{power64}
# scipy segfaults with netlib/atlas on ppc64le
BuildRequires:  flexiblas-openblas-openmp
%endif

%if %{with doc}
BuildRequires:  python3-sphinx
BuildRequires:  python3-matplotlib
BuildRequires:  python3-numpydoc
%endif

%global _description %{expand:
Scipy is open-source software for mathematics, science, and
engineering. The core library is NumPy which provides convenient and
fast N-dimensional array manipulation. The SciPy library is built to
work with NumPy arrays, and provides many user-friendly and efficient
numerical routines such as routines for numerical integration and
optimization. Together, they run on all popular operating systems, are
quick to install, and are free of charge. NumPy and SciPy are easy to
use, but powerful enough to be depended upon by some of the world's
leading scientists and engineers.}

%description %_description

%package -n python3-scipy
Summary:    Scientific Tools for Python
Requires:   python3-numpy, python3-f2py
%if %{with pooch}
Requires:   python3-pooch
%endif
Provides:   bundled(arpack) = 3.9.1
Provides:   bundled(biasedurn)
Provides:   bundled(boost-math)
Provides:   bundled(coin-or-HiGHS) = 1.2
Provides:   bundled(direct)
Provides:   bundled(Faddeeva)
Provides:   bundled(id)
Provides:   bundled(l-bfgs-b) = 3.0
Provides:   bundled(LAPJVsp)
Provides:   bundled(python3-decorator) = 4.0.5
Provides:   bundled(python3-pep440)
Provides:   bundled(python3-pypocketfft) = bf2c431c21213b7c5e23c2f542009b0bd3ec1445
Provides:   bundled(qhull) = 2019.1
Provides:   bundled(SuperLU) = 5.2.0
Provides:   bundled(unuran) = 1.8.1
%description -n python3-scipy %_description

%if %{with doc}
%package -n python3-scipy-doc
Summary:    Scientific Tools for Python - documentation
Requires:   python3-scipy = %{version}-%{release}
%description -n python3-scipy-doc
HTML documentation for Scipy
%endif

%if %{with tests}
%package -n python3-scipy-tests
Summary:    Scientific Tools for Python - test files
Requires:   python3-scipy = %{version}-%{release}
Requires:   python3-pytest
%description -n python3-scipy-tests
Scipy test files
%endif

%prep
%autosetup -p1 -n %{name}-%{version}%{?rcver}

%if %{without pythran}
# Remove pythran dependency if not explicitly required
sed -i '/pythran/d' pyproject.toml
%else
# Relax it otherwise
sed -i 's/pythran>=0.14.0,<0.18.0/pythran>=0.14.0/' pyproject.toml
%endif
%if %{without pooch}
sed -i '/pooch/d' pyproject.toml
%endif

rm $(grep -rl '/\* Generated by Cython') PKG-INFO

# Do not do benchmarking, coverage, or timeout testing for RPM builds
sed -Ei '/^[[:blank:]]*"(asv|pytest-cov|pytest-timeout)"/d' pyproject.toml

# No scikit-umfpack in Fedora
sed -i '/^[[:blank:]]*"scikit-umfpack"/d' pyproject.toml

# No pytest-xdist in RHEL
%if 0%{?rhel}
sed -i '/^[[:blank:]]*"pytest-xdist"/d' pyproject.toml
%endif

# Loosen the upper bound on numpy
sed -i "/numpy/s/,<2\.3//" pyproject.toml

# Loosen the lower bound on array-api-strict
sed -i "/array-api-strict/s/>=2\.3\.1/>=2/" pyproject.toml

# Loosen the upper bound on Cython
# This can be removed from scipy >= 1.16.0
sed -i '/Cython/s/,<3\.1\.0//' pyproject.toml

%generate_buildrequires
%pyproject_buildrequires -p %{?with_tests:-x test} %{build_backend_args}

%build
%pyproject_wheel %{build_backend_args}

%if %{with doc}
for PY in %{python3_version}; do
  pushd doc
  export PYTHONPATH=$(echo ../build/lib.linux-*-$PY/)
  make html SPHINXBUILD=sphinx-build-$PY
  rm -rf build/html/.buildinfo
  mv build build-$PY
  popd
done
%endif

%install
%pyproject_install
%pyproject_save_files scipy

# Some files got ambiguous python shebangs, we fix them after everything else is done
%py3_shebang_fix %{buildroot}%{python3_sitearch}

%check
# Check section disabled: Disabling checks for initial set of failures.
exit 0

%if %{with tests}
# check against the reference BLAS/LAPACK
export FLEXIBLAS=netlib

%ifarch %{power64}
# scipy segfaults with netlib/atlas on ppc64le
export FLEXIBLAS=openblas-openmp
%endif

# TestDatasets try to download from the internet
SKIP_ALL="not TestDatasets"
export PYTEST_ADDOPTS="-k '$SKIP_ALL'"

%ifarch aarch64
# TestConstructUtils::test_concatenate_int32_overflow is flaky on aarch64
export PYTEST_ADDOPTS="-k '$SKIP_ALL and \
not test_concatenate_int32_overflow'"
%endif

%ifarch s390x
# https://bugzilla.redhat.com/show_bug.cgi?id=1959353
export PYTEST_ADDOPTS="-k '$SKIP_ALL and \
not test_distance_transform_cdt05'"
%endif

%ifarch x86_64
%if 0%{?rhel}
# test_minimize_constrained started failing on ELN without any direct changes to scipy
export PYTEST_ADDOPTS="-k '$SKIP_ALL and \
not test_gh7799 and \
not test_minimize_constrained'"
%endif
%endif

%ifarch i686
# https://github.com/scipy/scipy/issues/17213
export PYTEST_ADDOPTS="-k '$SKIP_ALL and \
not test_examples and \
not test_shifts and \
not test_svdp and \
not TestMMIO and \
not test_mmio and \
not test_threadpoolctl and \
not test_gh11389 and \
not test_gh18123 and \
not test_gh_17782_segfault and \
not test_svd_gesdd_nofegfault'"
%endif

%ifarch riscv64
export PYTEST_ADDOPTS="-k '$SKIP_ALL and \
not TestSchur and \
not test_gejsv_general and \
not test_kendall_p_exact_large and \
not test_gejsv_edge_arguments and \
not test_gh12999 and \
not test_propack and \
not test_milp and \
not test_gejsv_NAG'"
%endif

pushd %{buildroot}/%{python3_sitearch}
# Ignoring the datasets tests as we don't have the optional pooch
# dependency on RHEL.
%{pytest} %{!?with_pooch:--ignore=scipy/datasets/tests/test_data.py} scipy %{?!rhel:--numprocesses=auto}
# Remove test remnants
rm -rf gram{A,B}
rm -rf .pytest_cache
popd
%endif

%files -n python3-scipy -f %{pyproject_files}
%license LICENSE.txt LICENSES_bundled.txt
%exclude %{python3_sitearch}/scipy/*/tests/
%exclude %{python3_sitearch}/scipy/*/*/tests/
%exclude %{python3_sitearch}/scipy/*/*/*/tests/
%exclude %{python3_sitearch}/scipy/*/*/*/*/tests/ 

%if %{with tests}
%files -n python3-scipy-tests
%{python3_sitearch}/scipy/*/tests/
%{python3_sitearch}/scipy/*/*/tests/
%{python3_sitearch}/scipy/*/*/*/tests/
%{python3_sitearch}/scipy/*/*/*/*/tests/
%endif

%if %{with doc}
%files -n python3-scipy-doc
%license LICENSE.txt
%doc doc/build-%{python3_version}/html
%endif

%changelog
* Mon Sep 29 2025 Nikola Forró <nforro@redhat.com> - 1.16.2-1
- New upstream release 1.16.2
- Work around ppc64le FTBFS with netlib/atlas

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.15.3-6
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.15.3-5
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 08 2025 Charalampos Stratakis <cstratak@redhat.com> - 1.15.3-3
- Loosen the upper bound on Cython

* Mon Jun 16 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.15.3-2
- Bump EVR

* Fri Jun 06 2025 Python Maint <python-maint@redhat.com> - 1.14.1-5
- Rebuilt for Python 3.14

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 1.14.1-4
- Bootstrap for Python 3.14

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Dec 14 2024 Orion Poplawski <orion@nwra.com> - 1.14.1-2
- Rebuild with numpy 2.0
- Skip failing test_gh7799 on x86_64

* Fri Sep 13 2024 Nikola Forró <nforro@redhat.com> - 1.14.1-1
- New upstream release 1.14.1

* Tue Jul 30 2024 Nikola Forró <nforro@redhat.com> - 1.11.3-15
- Loosen the upper bound on pybind11

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Jun 16 2024 Python Maint <python-maint@redhat.com> - 1.11.3-13
- Rebuilt for Python 3.13

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 1.11.3-12
- Bootstrap for Python 3.13

* Sat Jun 08 2024 Miro Hrončok <mhroncok@redhat.com> - 1.11.3-11
- Relax the pythran dependency

* Wed May 22 2024 Pavel Simovec <psimovec@redhat.com> - 1.11.3-10
- Remove python3-pooch optional dependency from RHEL

* Thu May 02 2024 Pavel Simovec <psimovec@redhat.com> - 1.11.3-9
- Build without pythran in RHEL by default

* Wed Apr 17 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 1.11.3-8
- Allow building with meson-python 0.16
- Allow building with pybind11 2.12

* Fri Feb 02 2024 Maxwell G <maxwell@gtmx.me> - 1.11.3-7
- Use dynamic BuildRequires for python runtime dependencies

* Tue Jan 30 2024 Miro Hrončok <mhroncok@redhat.com> - 1.11.3-6
- Skip fewer tests during build

* Mon Jan 29 2024 Florian Weimer <fweimer@redhat.com> - 1.11.3-5
- Disable incompatible-pointer-types errors on i686 (#2258823)

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Nov 30 2023 Karolina Surma <ksurma@redhat.com> - 1.11.3-3
- Fix the build without pythran

* Wed Nov 01 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.11.3-2
- Patch error collecting tests with pytest-xdist

* Wed Oct 11 2023 Jerry James <loganjerry@gmail.com> - 1.11.3-1
- New upstream release 1.11.3
  resolves: #2211813
- Convert License tag to SPDX
- Add Provides for bundled projects
- Disable LTO
- Pythran works on 32-bit architectures again
- Fix detection of open_memstream
- Use pyproject macros instead of the deprecated py3 macros
- Reenable some tests that work again
- Remove unused BuildRequires

* Wed Jul 12 2023 psimovec <psimovec@redhat.com> - 1.11.1-1
- New upstream release 1.11.1
  resolves: #2211813
- Separate tests into subpackage python3-scipy-tests

* Mon Jul 10 2023 Python Maint <python-maint@redhat.com> - 1.10.1-5
- Rebuilt for Python 3.12

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 1.10.1-4
- Bootstrap for Python 3.12

* Tue May 23 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 1.10.1-3
- Avoid pytest-xdist dependency in RHEL builds

* Wed Mar 15 2023 Pavel Šimovec <psimovec@redhat.com> - 1.10.1-2
- Remove workaround for linking issue on x86_64
- resolves: #2068530

* Wed Feb 22 2023 Pavel Šimovec <psimovec@redhat.com> - 1.10.1-1
- New upstream release 1.10.1
  resolves: #2101172
- Use the optional python3-pooch dependency

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Jul  3 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.8.1-5
- Fix linalg.lapack syevr segfault (#2099102)

* Fri Jun 17 2022 Python Maint <python-maint@redhat.com> - 1.8.1-4
- Rebuilt for Python 3.11

* Tue Jun 14 2022 Python Maint <python-maint@redhat.com> - 1.8.1-3
- Bootstrap for Python 3.11

* Tue Jun 14 2022 Python Maint <python-maint@redhat.com> - 1.8.1-2
- Rebuilt for Python 3.11

* Thu Jun 09 2022 Nikola Forró <nforro@redhat.com> - 1.8.1-1
- New upstream release 1.8.1
  resolves: #2088437

* Sat Mar 26 2022 Nikola Forró <nforro@redhat.com> - 1.8.0-3
- Skip test_cython_api also on armv7hl

* Sat Mar 26 2022 Nikola Forró <nforro@redhat.com> - 1.8.0-2
- Disable pythran on armv7hl as well

* Mon Feb 07 2022 Nikola Forró <nforro@redhat.com> - 1.8.0-1
- New upstream release 1.8.0
  resolves: #2035126

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Dec 21 2021 Nikola Forró <nforro@redhat.com> - 1.7.3-1
- New upstream release 1.7.3
  resolves: #1988883

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 14 2021 Miro Hrončok <mhroncok@redhat.com> - 1.7.0-2
- Use the optional Pythran build dependency

* Wed Jun 23 2021 Nikola Forró <nforro@redhat.com> - 1.7.0-1
- New upstream release 1.7.0
  resolves: #1953422

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.6.2-4
- Rebuilt for Python 3.10

* Fri Apr 23 2021 Nikola Forró <nforro@redhat.com> - 1.6.2-3
- Remove RPATH from certain shared object files

* Tue Mar 30 2021 Jonathan Wakely <jwakely@redhat.com> - 1.6.2-2
- Rebuilt for removed libstdc++ symbol (#1937698)

* Thu Mar 25 2021 Nikola Forró <nforro@redhat.com> - 1.6.2-1
- New upstream release 1.6.2
  resolves: #1942896

* Thu Feb 18 2021 Nikola Forró <nforro@redhat.com> - 1.6.1-1
- New upstream release 1.6.1
  resolves: #1929994

* Wed Feb 03 2021 Nikola Forró <nforro@redhat.com> - 1.6.0-3
- Increase test timeout on s390x

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 04 2021 Nikola Forró <nforro@redhat.com> - 1.6.0-1
- New upstream release 1.6.0
  resolves: #1906692

* Wed Nov 25 2020 Nikola Forró <nforro@redhat.com> - 1.5.4-2
- Skip factorial() float tests on Python 3.10
  resolves: #1898157

* Thu Nov 05 2020 Nikola Forró <nforro@redhat.com> - 1.5.4-1
- New upstream release 1.5.4
- Increase test timeout, 300 seconds is not always enough
  for test_logpdf_overflow on s390x
  resolves: #1894887

* Mon Oct 19 2020 Nikola Forró <nforro@redhat.com> - 1.5.3-1
- New upstream release 1.5.3
  resolves: #1889132

* Wed Sep 30 2020 Nikola Forró <nforro@redhat.com> - 1.5.2-2
- Skip one more test expected to fail on 32-bit architectures

* Mon Aug 31 2020 Nikola Forró <nforro@redhat.com> - 1.5.2-1
- New upstream release 1.5.2
  resolves: #1853871 and #1840077

* Sun Aug 16 2020 Iñaki Úcar <iucar@fedoraproject.org> - 1.5.0-4
- https://fedoraproject.org/wiki/Changes/FlexiBLAS_as_BLAS/LAPACK_manager

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 1.5.0-1
- Update to latest version

* Mon May 25 2020 Miro Hrončok <mhroncok@redhat.com> - 1.4.1-2
- Rebuilt for Python 3.9

* Sun Mar 01 2020 Orion Poplawski <orion@nwra.com> - 1.4.1-1
- Update to 1.4.1 (bz#1771154)
- Workaround FTBFS with gcc 10 (bz#1800078)

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Oct 18 2019 Miro Hrončok <mhroncok@redhat.com> - 1.3.1-1
- Update to 1.3.1 (#1674101)
- Drop Python 2 packages (not supported by SciPy >= 1.3)
- Backported upstream patch for cKDTree (fixes FTBFS)

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.2.1-8
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.2.1-7
- Rebuilt for Python 3.8

* Tue Jul 30 2019 Petr Viktorin <pviktori@redhat.com> - 1.2.1-6
- Remove build dependency on python2-pytest-xdist and python2-pytest-timeout
- Enable parallel tests in Python 3 %%check
- Use macros for Python interpreter in tests

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun 10 2019 Marcel Plch <mplch@redhat.com> - 1.2.1-4
- Fix FTBFS with Py3.8 (#1606315)

* Thu May 16 2019 Orion Poplawski <orion@nwra.com> - 1.2.1-3
- Build only against openblasp (bugz#1709161)

* Fri Apr 26 2019 Orion Poplawski <orion@nwra.com> - 1.2.1-2
- Do not create *-PYTEST.pyc files

* Tue Apr 23 2019 Orion Poplawski <orion@nwra.com> - 1.2.1-1
- Update to 1.2.1
- Drop scipy2-doc

* Wed Feb 06 2019 Charalampos Stratakis <cstratak@redhat.com> - 1.2.0-1
- Update to 1.2.0

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 23 2018 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-2
- Don't ignore the tests results but rather have a tolerance rate
- Skip test_decomp on ppc64le as it currently segfaults

* Fri Jun 22 2018 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-1
- Update to 1.1.0 (#1560265, #1594355)

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.0.0-8
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Feb 02 2018 Petr Viktorin <pviktori@redhat.com> - 1.0.0-6
- Link with -lm to build with new stricter Fedora flags
  https://bugzilla.redhat.com/show_bug.cgi?id=1541416

* Wed Jan 31 2018 Christian Dersch <lupinix@mailbox.org> - 1.0.0-5
- rebuilt for GCC 8.x (gfortran soname bump)

* Mon Dec 11 2017 Lumír Balhar <lbalhar@redhat.com> - 1.0.0-4
- Disable tests on s390x

* Mon Nov 20 2017 Lumír Balhar <lbalhar@redhat.com> - 1.0.0-3
- New subpackages with HTML documentation

* Tue Oct 31 2017 Christian Dersch <lupinix@mailbox.org> - 1.0.0-2
- Use openblas where available https://fedoraproject.org/wiki/Changes/OpenBLAS_as_default_BLAS
- Remove ppc64 hackery for OpenBLAS
- Don't run tests in parallel as pytest crashes
- Don't run test_denormals as it tends to stuck

* Thu Oct 26 2017 Thomas Spura <tomspur@fedoraproject.org> - 1.0.0-1
- update to 1.0.0 and use pytest instead of nose
- use timeout during parallel %%check

* Wed Oct 04 2017 Christian Dersch <lupinix@mailbox.org> - 0.19.1-5
- Use openblas where available (except ppc64), to use same as numpy (BZ 1472318)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 07 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.19.1-2
- Rebuild due to bug in RPM (RHBZ #1468476)

* Tue Jun 27 2017 Christian Dersch <lupinix@mailbox.org> - 0.19.1-1
- new version

* Wed Jun 07 2017 Christian Dersch <lupinix@mailbox.org> - 0.19.0-1
- new version

* Tue Jan 31 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.18.0-3
- Rebuild for libgfortran.so.3

* Mon Dec 12 2016 Stratakis Charalampos <cstratak@redhat.com> - 0.18.0-2
- Rebuild for Python 3.6

* Tue Jul 26 2016 Than Ngo <than@redhat.com> - 0.18.0-1
- 0.18.0
- %%check: make non-fatal as temporary workaround for scipy build on arm

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17.0-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue May 31 2016 Nils Philippsen <nils@redhat.com>
- fix source URL

* Mon Feb 15 2016 Orion Poplawski <orion@cora.nwra.com> - 0.17.0-1
- Update to 0.17.0
- Drop ctypes patch applied upstream

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Nov 21 2015 Kalev Lember <klember@redhat.com> - 0.16.1-6
- Add provides to satisfy scipy%%{_isa} requires in other packages

* Sun Nov 15 2015 Björn Esser <fedora@besser82.io> - 0.16.1-5
- Revert "Discard results of testsuite on %%{arm} for now"

* Sat Nov 14 2015 Björn Esser <besser82@fedoraproject.org> - 0.16.1-4
- Discard results of testsuite on %%{arm} for now
  Segfaults on non-aligned memory test (expected for arm)

* Sat Nov 14 2015 Thomas Spura <tomspur@fedoraproject.org> - 0.16.1-3
- Add patch to fix ctypes test
- Move requires to correct python2 subpackage
- Add FFLAGS also in %%install

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16.1-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Mon Oct 26 2015 Orion Poplawski <orion@cora.nwra.com> - 0.16.1-1
- Update to 0.16.1

* Wed Oct 14 2015 Thomas Spura <tomspur@fedoraproject.org> - 0.16.0-1
- Update to 0.16.0
- Use python_provide macro

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Mar 31 2015 Orion Poplawski <orion@cora.nwra.com> - 0.15.1-1
- Update to 0.15.1

* Sun Jan 4 2015 Orion Poplawski <orion@cora.nwra.com> - 0.14.1-1
- Update to 0.14.1

* Wed Aug 20 2014 Kevin Fenzi <kevin@scrye.com> - 0.14.0-5
- Rebuild for rpm bug 1131892

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May 10 2014 Orion Poplawski <orion@cora.nwra.com> - 0.14-2
- Rebuild with Python 3.4

* Tue May  6 2014 Orion Poplawski <orion@cora.nwra.com> - 0.14-1
- Update to 0.14
- Do not use system python-six (bug #1046817)

* Thu Feb 20 2014 Thomas Spura <tomspur@fedoraproject.org> - 0.13.3-2
- use python2 macros everywhere (Requested by Han Boetes)

* Tue Feb  4 2014 Thomas Spura <tomspur@fedoraproject.org> - 0.13.3-1
- Update to 0.13.3

* Mon Dec 9 2013 Orion Poplwski <orion@cora.nwra.com> - 0.13.2-1
- Update to 0.13.2

* Fri Dec 06 2013 Nils Philippsen <nils@redhat.com> - 0.13.1-2
- rebuild (suitesparse)

* Sun Nov 17 2013 Orion Poplwski <orion@cora.nwra.com> - 0.13.1-1
- Update to 0.13.1

* Wed Oct 23 2013 Tomas Tomecek <ttomecek@redhat.com> - 0.13.0-2
- Update to 0.13.0 final

* Tue Oct 15 2013 Orion Poplwski <orion@cora.nwra.com> - 0.13.0-0.4.rc1
- Update to 0.13.0rc1

* Tue Oct 01 2013 Tomas Tomecek <ttomecek@redhat.com> - 0.13.0-0.3.b1
- rebuilt with atlas 3.10

* Mon Sep 9 2013 Orion Poplwski <orion@cora.nwra.com> - 0.13.0-0.2.b1
- Unbundle python-six (bug #1005350)

* Thu Aug 29 2013 Orion Poplwski <orion@cora.nwra.com> - 0.13.0-0.1.b1
- Update to 0.13.0b1
- Drop patches applied upstream
- Fixup changelog and summary

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 30 2013 Tomas Tomecek <ttomecek@redhat.com> - 0.12.0-4
- Fix rpmlint warnings
- License update
- Add patch to use build_dir argument in build_extension

* Wed May 15 2013 Orion Poplawski <orion@cora.nwra.com> - 0.12.0-3
- Remove old ufsparse references, use suitesparse
- Spec cleanup

* Mon Apr 15 2013 Orion Poplawski <orion@cora.nwra.com> - 0.12.0-2
- Add patch to fix segfaul in test of sgeqrf

* Wed Apr 10 2013 Orion Poplawski <orion@cora.nwra.com> - 0.12.0-1
- Update to 0.12.0 final
- No longer remove weave from python3 build

* Sat Feb 16 2013 Orion Poplawski <orion@cora.nwra.com> - 0.12.0-0.1.b1
- Update to 0.12.0b1
- Drop upstreamed linalg patch

* Wed Feb 13 2013 Orion Poplawski <orion@cora.nwra.com> - 0.11.0-4
- Add patch from upstream to fix python3.3 issues in linalg routines

* Tue Feb 12 2013 Orion Poplawski <orion@cora.nwra.com> - 0.11.0-3
- Disable python3 tests for now

* Mon Oct  8 2012 Orion Poplawski <orion@cora.nwra.com> - 0.11.0-2
- Add requires python3-numpy, python3-f2py for python3-scipy (bug 863755)

* Sun Sep 30 2012 Orion Poplawski <orion@cora.nwra.com> - 0.11.0-1
- Update to 0.11.0 final

* Thu Aug 23 2012 Orion Poplawski <orion@cora.nwra.com> - 0.11.0-0.1.rc2
- Update to 0.11.0rc2

* Mon Aug  6 2012 Orion Poplawski <orion@cora.nwra.com> - 0.10.1-4
- Rebuild for python 3.3

* Fri Aug  3 2012 David Malcolm <dmalcolm@redhat.com> - 0.10.1-3
- remove rhel logic from with_python3 conditional

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Mar 16 2012 Orion Poplawski <orion@cora.nwra.com> - 0.10.1-1
- Update to 0.10.1

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 14 2011 Orion Poplawski <orion@cora.nwra.com> - 0.10.0-1
- Update to 0.10.0

* Sat Sep  3 2011 Thomas Spura <tomspur@fedoraproject.org> - 0.9.0-2
- little cosmetic changes
- filter provides in python_sitearch

* Fri Sep 02 2011 Andrew McNabb <amcnabb@mcnabbs.org>
- add python3 subpackage

* Fri Apr 1 2011 Orion Poplawski <orion@cora.nwra.com> - 0.9.0-1
- Update to 0.9.0
- Drop all stsci sources and patches, dropped from upstream
- Drop gcc and py27 patches fixed upstream
- Add %%check section to run tests

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 31 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.7.2-3
- Fix scipy build on python-2.7

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Jul 1 2010 Jef Spaleta <jspaleta@fedoraproject.org> - 0.7.2-1
- New upstream release

* Sun Apr 11 2010 Jef Spaleta <jspaleta@fedoraproject.org> - 0.7.1-3
- Bump for rebuild against numpy 1.3

* Thu Apr  1 2010 Jef Spaleta <jspaleta@fedoraproject.org> - 0.7.1-2
- Bump for rebuild against numpy 1.4.0

* Thu Dec 10 2009 Jon Ciesla <limb@jcomserv.net> - 0.7.1-1
- Update to 0.7.1.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jun 14  2009 Jef Spaleta <jspaleta@fedoraproject.org> - 0.7.0-4
- Fix for gcc34 weave blitz bug #505379

* Tue Apr 7  2009 Jef Spaleta <jspaleta@fedoraproject.org> - 0.7.0-3
- Add f2py requires to prepared for numpy packaging split

* Sun Mar 1  2009 Jef Spaleta <jspaleta@fedoraproject.org> - 0.7.0-2
- Patch for stsci image function syntax fix.

* Thu Feb 26 2009 Jef Spaleta <jspaleta@fedoraproject.org> - 0.7.0-1
- Update to final 0.7 release

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-0.3.b1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 15 2008 Deji Akingunola <dakingun@gmail.com> - 0.7.0-0.2.b1
- Rebuild for atlas-3.8.2

* Mon Dec 01 2008  Jef Spaleta <jspaleta@fedoraproject.org> - 0.7.0-0.1.b1
- Update to latest beta which lists python 2.6 support

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.6.0-8
- Rebuild for Python 2.6

* Fri Oct 03 2008 Jef Spaleta <jspaleta@fedoraproject.org> - 0.6.0-7
- fix the stsci fix

* Thu Oct 02 2008 Jef Spaleta <jspaleta@fedoraproject.org> - 0.6.0-6
- include missing setup files for stsci module

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.6.0-5
- Autorebuild for GCC 4.3

* Fri Jan 04 2008 Jef Spaleta <jspaleta@fedoraproject.org> - 0.6.0-4
- fix for egg-info file creation

* Wed Oct 03 2007 Jef Spaleta <jspaleta@gmail.com> - 0.6.0-3
- include_dirs changes for ufsparse change in development

* Tue Oct 02 2007 Jef Spaleta <jspaleta@gmail.com> - 0.6.0-2
- Fix licensing to match Fedora packaging guidance
- Remove unnecessary library deps

* Tue Sep 25 2007 Jarrod Millman <millman@berkeley.edu> - 0.6.0-1
- update to new upstream source
- update Summary, License, Url, and description
- added extra dependencies
- remove symlink since Lib has been renamed scipy

* Tue Aug 21 2007 Jef Spaleta <jspaleta@gmail.com> - 0.5.2.1-1
- Update to new upstream source

* Tue Aug 21 2007 Jef Spaleta <jspaleta@gmail.com> - 0.5.2-3
- fix licensing tag and bump for buildid rebuild

* Wed Apr 18 2007 Jef Spaleta <jspaleta@gmail.com> - 0.5.2-2.2
- go back to using gfortran now that numpy is patched

* Sat Apr 14 2007 Jef Spaleta <jspaleta@gmail.com> - 0.5.2-2.1
- minor correction for f77 usage

* Sat Apr 14 2007 Jef Spaleta <jspaleta@gmail.com> - 0.5.2-2
- revert to f77 due to issue with numpy in development

* Sat Apr 14 2007 Jef Spaleta <jspaleta@gmail.com> - 0.5.2-1.1
- remove arch specific optimizations

* Wed Feb 21 2007 Jef Spaleta <jspaleta@gmail.com> - 0.5.2-1
- Update for new upstream release

* Mon Dec  11 2006 Jef Spaleta <jspaleta@gmail.com> - 0.5.1-5
- Bump for rebuild against python 2.5 in devel tree

* Sun Dec  3 2006 Jef Spaleta <jspaleta@gmail.com> - 0.5.1-4
- Minor adjustments to specfile for packaging guidelines.
- Changed buildrequires fftw version 3  from fftw2

* Sat Dec  2 2006 Jef Spaleta <jspaleta@gmail.com> - 0.5.1-2
- Updated spec for FE Packaging Guidelines and for upstream version 0.5.1

* Mon May  8 2006 Neal Becker <ndbecker2@gmail.com> - 0.4.8-4
- Add BuildRequires gcc-c++
- Add python-devel
- Add libstdc++

* Mon May  8 2006 Neal Becker <ndbecker2@gmail.com> - 0.4.8-3
- Add BuildRequires gcc-gfortran

* Sun May  7 2006 Neal Becker <ndbecker2@gmail.com> - 0.4.8-3
- Add BuildRequires numpy


* Wed May  3 2006 Neal Becker <ndbecker2@gmail.com> - 0.4.8-2
- Fix BuildRoot
- Add BuildRequires, Requires
- Test remove d1mach patch
- Fix defattr
- Add changelog
- Removed Prefix, Vendor
- Fix Source0
