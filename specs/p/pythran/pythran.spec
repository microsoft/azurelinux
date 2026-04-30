## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 8;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           pythran
Version:        0.18.0
Release:        %autorelease
Summary:        Ahead of Time Python compiler for numeric kernels

# pythran is BSD-3-Clause
# pythran/graph.py has bits of networkx, also BSD-3-Clause
# pythran/pythonic/patch/complex is MIT OR NCSA
License:        BSD-3-Clause AND (MIT OR NCSA)

# see pythran/pythonic/patch/README.rst
# The version is probably somewhat around 3
Provides:       bundled(libcxx) = 3

# see pythran/graph.py
# Only bundles one function from networkx
Provides:       bundled(python3dist(networkx)) = 2.6.1


%py_provides    python3-%{name}

URL:            https://github.com/serge-sans-paille/pythran
Source:         %{url}/archive/%{version}/%{name}-%{version}.tar.gz

# Fix test failures:
# - Use more generic way of checking bool value of an object
# - Add support for numpy.frombuffer
# - Do not test binary mode of numpy.fromstring for recent
# - Adjust doc validation to recent python 3.13
Patch:          https://github.com/serge-sans-paille/pythran/pull/2323.patch
# - Provide a small workaround for gast not doing its portability job for dumping
Patch:          https://github.com/serge-sans-paille/pythran/commit/05f6f2b24a.patch

# there is no actual arched content
# yet we want to test on all architectures
# and we also might need to skip some
%global debug_package %{nil}

BuildRequires:  make
BuildRequires:  boost-devel
BuildRequires:  flexiblas-devel
BuildRequires:  gcc-c++
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-devel
BuildRequires:  xsimd-devel >= 8

# For docs
BuildRequires:  pandoc

# For tests
BuildRequires:  /usr/bin/python
# this is used for supporting -n auto in %%pytest
BuildRequires:  python3-pytest-xdist

# This is a package that compiles code, it runtime requires devel packages
Requires:       flexiblas-devel
Requires:       gcc-c++
Requires:       python3-devel
Requires:       boost-devel
Requires:       xsimd-devel >= 8

%description
Pythran is an ahead of time compiler for a subset of the Python language, with
a focus on scientific computing. It takes a Python module annotated with a few
interface description and turns it into a native Python module with the same
interface, but (hopefully) faster. It is meant to efficiently compile
scientific programs, and takes advantage of multi-cores and SIMD
instruction units.


%prep
%autosetup -p1 -n %{name}-%{version}
find -name '*.hpp' -exec chmod -x {} +
sed -i '1{/#!/d}' pythran/run.py

# Remove bundled header libs and use the ones from system
rm -r pythran/boost pythran/xsimd

# Use FlexiBLAS
sed -i 's|blas=blas|blas=flexiblas|' pythran/pythran-linux*.cfg
sed -i 's|include_dirs=|include_dirs=/usr/include/flexiblas|' pythran/pythran-linux*.cfg

# This test explicitly tests with OpenBLAS
# But we want to avoid OpenBLAS dependency to verify everything works with FlexiBLAS
# https://github.com/serge-sans-paille/pythran/pull/2244#issuecomment-2441215988
sed -i 's/openblas/flexiblas/' pythran/tests/test_distutils/pythran.rc

# not yet available in Fedora
sed -i '/guzzle_sphinx_theme/d' docs/conf.py
sed -i 's/, "guzzle_sphinx_theme"//' pyproject.toml
sed -i 's/, "nbval"//' pyproject.toml

# The tests have some cflags in them
# We need to adapt the flags to play nicely with other Fedora's flags
# E.g. fortify source implies at least -O1
sed -i -e 's/-O0/-O1/g' -e 's/-Werror/-w/g' pythran/tests/__init__.py


%generate_buildrequires
%pyproject_buildrequires -x doc,test


%build
%pyproject_wheel

PYTHONPATH=$PWD make -C docs html
rm -rf docs/_build/html/.{doctrees,buildinfo}


%install
%pyproject_install
%pyproject_save_files %{name} omp


%check
# https://bugzilla.redhat.com/show_bug.cgi?id=1747029#c12
k="not test_numpy_negative_binomial"
# https://github.com/serge-sans-paille/pythran/issues/2214
k="$k and not (TestDoctest and test_tutorial)"
# https://github.com/serge-sans-paille/pythran/pull/2310#issuecomment-2873711746
k="$k and not test_ndenumerate and not test_ndindex1 and not test_ndindex2"
%if 0%{?__isa_bits} == 32
# These tests cause memory (address space) exhaustion; see discussion in
# https://src.fedoraproject.org/rpms/pythran/pull-request/28.
for t in test_fftn_{8,16,17,20,22} \
    test_{h,ih,ir}fft_{8,14} \
    test_{,i}fft_3d{,_axis,f64_axis,int64_axis} \
    test_numpy_random_bytes1 \
    test_convolve_2b
do
  k="$k and not ${t}"
done
%endif
%ifarch aarch64
# the test is so flaky it makes the build fail almost all the time
k="$k and not test_interp_8"
%endif
%ifarch %{power64}
# https://github.com/serge-sans-paille/pythran/pull/1946#issuecomment-992460026
k="$k and not test_setup_bdist_install3"
%endif

# Don’t run tests in parallel on 32-bit architecutres. Running tests in serial
# makes memory errors, which occur in some tests on 32-bit architectures, more
# reproducible, and makes the output when they occur less confusing: we tend to
# get individual test failures rather than a pytest INTERNALERROR.
%if 0%{?__isa_bits} != 32
%global use_pytest_xdist 1
%endif

%pytest %{?use_pytest_xdist:-n auto} -k "$k"


%files -f %{pyproject_files}
%license LICENSE
%doc README.rst
%doc docs/_build/html
%{_bindir}/%{name}
%{_bindir}/%{name}-config


%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 0.18.0-8
- test: add initial lock files

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.18.0-7
- Rebuilt for Python 3.14.0rc3 bytecode

* Tue Aug 19 2025 Miro Hrončok <miro@hroncok.cz> - 0.18.0-6
- Fix test failures
- Rebuilt for Python 3.14.0rc2 bytecode
- Fixes: rhbz#2385557

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.18.0-4
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jun 05 2025 Python Maint <python-maint@redhat.com> - 0.18.0-2
- Rebuilt for Python 3.14

* Sun May 25 2025 Miro Hrončok <miro@hroncok.cz> - 0.18.0-1
- Update to 0.18.0
- Fixes: rhbz#2341244
- Fixes: rhbz#2368169

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Oct 31 2024 Miro Hrončok <miro@hroncok.cz> - 0.17.0-1
- Update to 0.17.0

* Wed Aug 28 2024 Miro Hrončok <miro@hroncok.cz> - 0.16.1-5
- Convert the License tag to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 15 2024 Python Maint <python-maint@redhat.com> - 0.16.1-2
- Rebuilt for Python 3.13

* Tue May 28 2024 sergesanspaille <serge.guelton@telecom-bretagne.eu> - 0.16.1-1
- Update to 0.16.1
- Fixes: rhbz#2257193

* Thu Jan 25 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.14.0-8
- Apply upstream PR#2149 to fully remove numpy.distutils

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Oct 05 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0.14.0-2
- Fix FTBFS: skip tests that need numpy.distutils
- On 32-bit, run tests in serial and skip those that exhaust memory
- Drop obsolete conditionals for 32-bit ARM

* Thu Sep 07 2023 Miro Hrončok <mhroncok@redhat.com> - 0.14.0-1
- Update to 0.14.0
- Fixes: rhbz#2237784

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jul 03 2023 Miro Hrončok <mhroncok@redhat.com> - 0.13.1-1
- Update to 0.13.1

* Mon Jul 03 2023 Python Maint <python-maint@redhat.com> - 0.12.1-4
- Rebuilt for Python 3.12

* Wed Jan 25 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 0.12.1-3
- Avoid ipython test dependency in RHEL builds

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Jan 15 2023 Serge Guelton <serge.guelton@telecom-bretagne.eu> - 0.12.1-1
- Update to 0.12.1

* Wed Sep 28 2022 Miro Hrončok <mhroncok@redhat.com> - 0.12.0-1
- Update to 0.12.0
- Fixes: rhbz#2130464

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 15 2022 Python Maint <python-maint@redhat.com> - 0.11.0-5
- Rebuilt for Python 3.11

* Tue Mar 15 2022 Miro Hrončok <mhroncok@redhat.com> - 0.11.0-4
- Add a workaround for setuptools 60+,
  use distutils from the standard library during the tests

* Mon Mar 14 2022 Serge Guelton - 0.11.0-3
- Fix gcc12 build
- Fixes: rhbz#2046923

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Dec 14 2021 Miro Hrončok <mhroncok@redhat.com> - 0.11.0-1
- Update to 0.11.0
- Fixes: rhbz#2032254

* Fri Sep 17 2021 Miro Hrončok <mhroncok@redhat.com> - 0.10.0-1
- Update to 0.10.0
- Fixes: rhbz#2003905

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.12.post1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 14 2021 Miro Hrončok <mhroncok@redhat.com> - 0.9.12.post1-1
- Update to 0.9.12.post1
- Fixes: rhbz#1982196

* Wed Jul 14 2021 Miro Hrončok <mhroncok@redhat.com> - 0.9.12-1
- Update to 0.9.12
- Fixes: rhbz#1981981
- Fixes: rhbz#1927172

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.9.11-2
- Rebuilt for Python 3.10

* Sun May 23 2021 sguelton@redhat.com - 0.9.11-1
- Update to 0.9.11

* Sun May 9 2021 sguelton@redhat.com - 0.9.10-1
- Update to 0.9.10

* Wed Mar 31 2021 sguelton@redhat.com - 0.9.9-1
- Update to 0.9.9

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.8^post3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 18 2021 Serge Guelton - 0.9.8^post3-2
- Apply compatibility patch with numpy 1.20

* Sun Dec 13 2020 sguelton@redhat.com - 0.9.8^post3-1
- Update to 0.9.8post3
- No longer recommend SciPy

* Wed Sep 23 2020 Miro Hrončok <mhroncok@redhat.com> - 0.9.7-1
- Update to 0.9.7
- Rebuilt for Python 3.9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild
- https://fedoraproject.org/wiki/Changes/FlexiBLAS_as_BLAS/LAPACK_manager
- Fixes: rhbz#1818006
- Fixes: rhbz#1787813

* Fri Mar 13 2020 Miro Hrončok <mhroncok@redhat.com> - 0.9.5-2
- Fix tests with ipython 7.12+ (#1813075)

* Fri Jan 31 2020 Miro Hrončok <mhroncok@redhat.com> - 0.9.5-1
- Update to 0.9.5 (#1787813)

* Tue Dec 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.9.4post1-1
- Update to 0.9.4post1 (#1747029)

* Tue Aug 20 2019 Miro Hrončok <mhroncok@redhat.com> - 0.9.3-1
- Update to 0.9.3 (#1743187)
- Allow 32bit architectures

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jun 26 2019 Miro Hrončok <mhroncok@redhat.com> - 0.9.2-1
- Initial package

## END: Generated by rpmautospec
