## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 3;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global srcname dask

# Requires distributed, which is a loop.
# Also, some tests require packages that require dask itself.
# Force bootstrap for package review.
%bcond bootstrap 0
# We don't have all dependencies available yet.
%bcond docs 0

# We have an arched package to detect arch-dependent issues in dependencies,
# but all of the installable RPMs are noarch and there is no compiled code.
%global debug_package %{nil}

Name:           python-%{srcname}
Version:        2025.10.0
%global tag     %{version}
Release:        %autorelease
Summary:        Parallel PyData with Task Scheduling

License:        BSD-3-Clause
URL:            https://github.com/dask/dask
Source0:        %{pypi_source %{srcname}}
# Fedora-specific patches.
Patch:          0001-Remove-extra-test-dependencies.patch
# https://github.com/dask/dask/pull/11892
Patch:          0002-XFAIL-test-if-NotImplementedError-is-raised.patch
# https://github.com/dask/dask/issues/12043
Patch:          0003-TST-Fall-back-to-cloudpickle-in-more-cases.patch
# Allow an xfail to pass; may be due to the warning filter later.
Patch:          0004-Mark-test_combine_first_all_nans-as-a-non-strict-xfa.patch

# Stop building on i686
# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

%description
Dask is a flexible parallel computing library for analytics.


%package -n     python3-%{srcname}
Summary:        %{summary}

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3dist(graphviz)
BuildRequires:  python3dist(ipython)
%if %{without bootstrap}
BuildRequires:  python3dist(scikit-image)
BuildRequires:  python3dist(xarray)
%endif
# Optional test requirements.
BuildRequires:  python3dist(aiohttp)
BuildRequires:  python3dist(bottleneck)
BuildRequires:  python3dist(crick)
BuildRequires:  python3dist(fastavro)
BuildRequires:  python3dist(h5py)
BuildRequires:  python3dist(jsonschema)
BuildRequires:  python3dist(matplotlib)
BuildRequires:  python3dist(psutil)
BuildRequires:  python3dist(requests)
BuildRequires:  python3dist(python-snappy)
BuildRequires:  python3dist(sqlalchemy)
BuildRequires:  python3dist(tables)
BuildRequires:  python3dist(zarr)

Recommends:     python3-%{srcname}+array = %{version}-%{release}
Recommends:     python3-%{srcname}+bag = %{version}-%{release}
Recommends:     python3-%{srcname}+dataframe = %{version}-%{release}
Recommends:     python3-%{srcname}+delayed = %{version}-%{release}
%if %{without bootstrap}
Recommends:     python3-%{srcname}+distributed = %{version}-%{release}
%endif
# No recent enough Bokeh is packaged
Obsoletes:      python3-%{srcname}+diagnostics < 2022.5.0-1
# dask-expr is part of dask since version 2025.1.0
Obsoletes:      python3-dask-expr < 2025.1.0
Obsoletes:      python3-dask-expr+analyze < 2025.1.0

# There is nothing that can be unbundled; there are some some snippets forked
# or copied from unspecified versions of numpy, under a BSD-3-Clause license
# similar to that of dask itself.
#
# - dask/array/numpy_compat.py:
#     _Recurser, moveaxis, rollaxis, sliding_window_view
# - dask/array/backends.py:
#     _tensordot
# - dask/array/core.py:
#     block
# - dask/array/einsumfuncs.py:
#     parse_einsum_input
# - dask/array/routines.py:
#     cov, _average
Provides:       bundled(numpy)

%description -n python3-%{srcname}
Dask is a flexible parallel computing library for analytics.


%pyproject_extras_subpkg -n python3-%{srcname} -a array bag dataframe delayed
%if %{without bootstrap}
%pyproject_extras_subpkg -n python3-%{srcname} -a distributed
%endif


%if %{with docs}
%package -n python-%{srcname}-doc
Summary:        dask documentation

BuildArch:      noarch

BuildRequires:  python3dist(dask_sphinx_theme) >= 1.3.5
BuildRequires:  python3dist(numpydoc)
BuildRequires:  python3dist(sphinx) >= 4

%description -n python-%{srcname}-doc
Documentation for dask.
%endif


%prep
%autosetup -n %{srcname}-%{version} -p1


%generate_buildrequires
%pyproject_buildrequires -x test,array,bag,dataframe,delayed
%if %{without bootstrap}
%pyproject_buildrequires -x distributed
%endif


%build
%pyproject_wheel

%if %{with docs}
# generate html docs
PYTHONPATH=${PWD} sphinx-build-3 docs/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}
%endif


%install
%pyproject_install

%pyproject_save_files -l %{srcname}


%check
# This test compares against files in .github/. It does not work on the PyPI
# sdist, and is only relevant to upstream CI anyway.
#
# test_development_guidelines_matches_ci fails from sdist
# https://github.com/dask/dask/issues/8499
k="${k-}${k+ and }not test_development_guidelines_matches_ci"

# Fails with Python 3.14: https://github.com/dask/dask/issues/12042
%if 0%{?fedora} >= 43
k="${k-}${k+ and }not test_multiple_repartition_partition_size"
%endif

# Previously excluded for dask-expr. Those tests use parquet files,
# which involves pyarrow.
%ifarch s390x
k="${k-}${k+ and }not test_combine_similar_no_projection_on_one_branch"
k="${k-}${k+ and }not test_parquet_all_na_column"
%endif

pytest_args=(
  -m 'not network'

  -n "auto"

  -k "${k-}"

# Ignore warnings about Pandas deprecations, which should be fixed in the next release.
  -W 'ignore::FutureWarning'

# arrow tests all fail on s390x, it's not at all BE-safe
# https://github.com/dask/dask/issues/11186
%ifarch s390x
  --ignore %{srcname}/dataframe/io/tests/test_parquet.py
%endif

  # Upstream uses 'thread' for Windows, but that kills the whole session, and
  # we'd like to see exactly which tests fail.
  --timeout_method=signal

  --import-mode=importlib
)

%{pytest} "${pytest_args[@]}"

%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.rst
%license dask/array/NUMPY_LICENSE.txt
%{_bindir}/dask

%if %{with docs}
%files -n python-%{srcname}-doc
%doc html
%license dask/array/NUMPY_LICENSE.txt
%endif


%changelog
## START: Generated by rpmautospec
* Mon Apr 06 2026 azldev <> - 2025.10.0-3
- Latest state for python-dask

* Mon Dec 15 2025 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2025.10.0-2
- Drop extraneous patch

* Tue Dec 02 2025 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2025.10.0-1
- Update to latest version (#2404034)

* Sun Sep 21 2025 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2025.9.1-1
- Update to latest version (#2395728)

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 2025.9.0-2
- Rebuilt for Python 3.14.0rc3 bytecode

* Sun Sep 14 2025 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2025.9.0-1
- Update to latest version (#2366171)

* Tue Aug 19 2025 Python Maint <python-maint@redhat.com> - 2025.4.1-5
- Rebuilt for Python 3.14

* Mon Aug 18 2025 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2025.4.1-4
- Fix build with Python 3.14

* Wed Jul 30 2025 Python Maint <python-maint@redhat.com> - 2025.4.1-3
- Bootstrap for Python 3.14

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2025.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon May 05 2025 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2025.4.1-1
- Update to latest version (#2338642)

* Wed Apr 23 2025 Sandro <devel@penguinpee.nl> - 2025.4.0-1
- Update to 2025.4.0 (RHBZ#2338642)
- Fix path for `--ignore` on `s390x`
- Exclude tests previously excluded for dask-expr

* Thu Apr 17 2025 Sandro <devel@penguinpee.nl> - 2025.3.0-1
- Update to 2025.3.0 (RHBZ#2338642)

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2024.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Dec 30 2024 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2024.12.1-1
- Update to latest version (#2330266)

* Wed Nov 27 2024 Richard W.M. Jones <rjones@redhat.com> - 2024.11.2-5
- Rebuild for libarrow 18

* Sun Nov 17 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2024.11.2-3
- Use the new %%pyproject_extras_subpkg -a option for noarch extras

* Sun Nov 17 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2024.11.2-2
- Revert "Manually define the extras metapackages so they can be noarch"

* Sun Nov 17 2024 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2024.11.2-1
- Update to latest version (#2319337)

* Sun Oct 13 2024 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2024.9.1-1
- Update to latest version (#2309030)

* Mon Sep 23 2024 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2024.9.0-1
- Update to latest version (#2309030)

* Wed Aug 07 2024 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2024.8.0-1
- Update to latest version (#2303277)

* Sat Jul 20 2024 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2024.7.1-1
- Update to latest version (#2296060)

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2024.6.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 26 2024 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2024.6.2-4
- Disable bootstrap mode

* Sat Jun 22 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2024.6.2-3
- Manually define the extras metapackages so they can be noarch
- Fixes RHBZ#2293727

* Fri Jun 21 2024 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2024.6.2-1
- Update to latest version (#2293520)

* Tue Jun 18 2024 Adam Williamson <awilliam@redhat.com> - 2024.6.0-3
- Put tests back in the package, hack around s390x issue

* Mon Jun 17 2024 Adam Williamson <awilliam@redhat.com> - 2024.6.0-2
- Strip tests from the installed files

* Mon Jun 17 2024 Adam Williamson <awilliam@redhat.com> - 2024.6.0-1
- Update to 2024.6.0, drop merged/unneeded patches, Python 3.13 fixes

* Mon Jun 17 2024 Python Maint <python-maint@redhat.com> - 2024.2.1-4
- Rebuilt for Python 3.13

* Mon Mar 11 2024 Sandro <devel@penguinpee.nl> - 2024.2.1-3
- Drop i686 support

* Fri Mar 01 2024 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2024.2.1-2
- Fix tests on other architectures

* Sat Feb 24 2024 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2024.2.1-1
- Update to latest version (#2263594)

* Tue Jan 30 2024 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2024.1.1-1
- Update to latest version (#2260587)

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2024.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2024.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 17 2024 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2024.1.0-2
- Backport fix for flaky test

* Mon Jan 15 2024 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2024.1.0-1
- Update to latest version (#2254772)

* Tue Dec 05 2023 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2023.12.0-1
- Update to latest version (#2252494)

* Mon Nov 27 2023 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2023.11.0-2
- Ignore warnings from Pandas

* Sun Nov 26 2023 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2023.11.0-1
- Update to latest version (#2186901)

* Sun Aug 27 2023 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2023.8.1-3
- Fix test on s390x using Debian patch

* Sun Aug 20 2023 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2023.8.1-2
- Skip tables on i686, as it's unavailable

* Sat Aug 19 2023 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2023.8.1-1
- Update to latest version (#2186901)

* Thu Jul 20 2023 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2023.7.1-1
- Update to latest version (#2186901)

* Thu Jul 20 2023 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2023.7.0-2
- Fix tests on 32-bit

* Thu Jul 20 2023 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2023.7.0-1
- Update to latest version (#2186901)

* Wed Jul 19 2023 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2023.4.1-3
- Skip test broken on Python 3.12

* Tue Jul 18 2023 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2023.4.1-2
- Rebuild for python3.12b4 (rhbz#2220181)

* Mon May 08 2023 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2023.4.1-1
- Update to latest version (#2186901)

* Sun Apr 16 2023 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2023.4.0-1
- Update to latest version (#2186901)

* Tue Mar 28 2023 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2023.3.2-1
- Update to latest version (#2173223)

* Mon Feb 20 2023 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2023.2.0-1
- Update to latest version (#2165161)

* Sun Jan 22 2023 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2023.1.0-1
- Update to latest version (#2160834)

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2022.12.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Dec 19 2022 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2022.12.1-3
- Add some more now-available testing dependencies

* Mon Dec 19 2022 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2022.12.1-2
- Fix test on i686 arch

* Sun Dec 18 2022 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2022.12.1-1
- Update to latest version (#2154467)

* Sun Dec 11 2022 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2022.12.0-1
- Update to latest version (#2150408)

* Sun Nov 20 2022 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2022.11.1-1
- Update to latest version (#2115959)

* Sun Oct 16 2022 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2022.10.0-1
- Update to latest version (#2115959)

* Wed Sep 07 2022 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2022.9.0-1
- Update to latest version (#2115959)

* Sun Aug 21 2022 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2022.8.1-1
- Update to latest version (#2115959)

* Sun Aug 14 2022 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2022.8.0-1
- Update to latest version (#2115959)

* Mon Jul 25 2022 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2022.7.1-1
- Update to latest version (#2089862)

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2022.5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 21 2022 Miro Hrončok <miro@hroncok.cz> - 2022.5.0-5
- Don't BuildRequire unused pre-commit

* Tue May 24 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2022.5.0-4
- Skip test_query_with_meta on ALL 32-bit platforms

* Mon May 23 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2022.5.0-3
- Add “pandas[test]” to “test” extra

* Mon May 23 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2022.5.0-2
- Use an arched base package with noarch binary RPMs
- Conditionalize fastavro BR, which is not available on 32-bit
- Run tests on all arches to reliably track arch-dependent bugs
- Add necessary arch-dependent skips for failing tests

* Mon May 23 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2022.5.0-1
- Update to 2022.5.0 (close RHBZ#2065859)
- Drop the “diagnostics” extras metapackage because no recent enough Bokeh
  version is available.
- Switch to the PyPI sdist as source (with workarounds)
- Ensure NUMPY_LICENSE.txt is packaged
- Add Provides: bundled(numpy)

* Sun Mar 06 2022 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2022.2.1-2
- Fix provided version in metadata

* Sun Feb 27 2022 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2022.2.1-1
- Update to latest version (#2058755)

* Sat Feb 12 2022 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2022.2.0-1
- Update to latest version (#2053679)

* Sat Jan 29 2022 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2022.1.1-1
- Update to latest version (#2047914)

* Sun Jan 16 2022 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2022.1.0-3
- Fix version in metadata

* Sun Jan 16 2022 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2022.1.0-2
- Upload sources

* Sun Jan 16 2022 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2022.1.0-1
- Update to latest version (#2040923)

* Mon Dec 20 2021 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2021.12.0-1
- Update to latest version (#2016711)

* Wed Sep 22 2021 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2021.9.1-1
- Update to latest version (#2006577)

* Sat Sep 04 2021 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2021.9.0-1
- Update to latest version (#2001121)

* Sat Aug 21 2021 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2021.8.1-1
- Update to latest version (#1993560)

* Sat Aug 21 2021 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2021.8.0-3
- Add missing diagnostics subpackage.

* Sat Aug 21 2021 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2021.8.0-2
- Switch to latest Python macros.

* Sat Aug 14 2021 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2021.8.0-1
- Update to latest version (#1993560)

* Sat Jul 31 2021 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2021.7.2-1
- Update to latest version (#1985515)

* Mon Jul 26 2021 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2021.7.1-1
- Update to latest version (#1985515)

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2021.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun Jul 11 2021 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2021.7.0-1
- Update to latest version (#1980906)

* Sun Jul 04 2021 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2021.6.2-1
- Update to latest version (#1974872)

* Sat Jun 19 2021 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2021.6.1-1
- Update to latest version (#1973783)

* Thu Jun 17 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2021.6.0-1
- Skip some failing tests for now

* Sun Jun 13 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2021.6.0-1
- Update to latest version (#1965698)

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2021.5.0-2
- Rebuilt for Python 3.10

* Sat May 15 2021 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2021.5.0-1
- Update to latest version (#1960766)

* Sat Apr 24 2021 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2021.4.1-1
- Update to latest version (#1953086)

* Fri Apr 02 2021 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2021.4.0-1
- Update to latest version (#1943694)

* Sun Mar 07 2021 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2021.3.0-1
- Update to latest version (#1936017)

* Fri Feb 05 2021 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2021.2.0-1
- Update to latest version (#1925645)

* Wed Jan 27 2021 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2021.1.1-1
- Update to latest version (#1919397)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2021.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jan 19 2021 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2021.1.0-1
- Update to latest version (#1906637)

* Sat Oct 10 2020 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.30.0-1
- Update to latest version (#1884852)

* Mon Oct 05 2020 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.29.0-1
- Update to latest version (#1884852)

* Sat Sep 26 2020 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.28.0-1
- Update to latest version (#1882873)

* Fri Sep 18 2020 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.27.0-1
- Update to latest version (#1880693)

* Sat Sep 12 2020 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.26.0-1
- Update to latest version (#1878309)

* Fri Aug 28 2020 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.25.0-1
- Update to latest version (#1873659)

* Sun Aug 23 2020 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.24.0-1
- Update to latest version (#1871358)

* Sat Aug 15 2020 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.23.0-1
- Update to latest version (#1868951)

* Sun Aug 02 2020 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.22.0-1
- Update to latest version

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.21.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 18 2020 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.21.0-1
- Update to latest version

* Fri Jul 10 2020 Miro Hrončok <mhroncok@redhat.com> - 2.20.0-2
- Add metadata for Python extras subpackages

* Sun Jul 05 2020 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.20.0-1
- Update to latest version

* Sat Jun 06 2020 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.18.0-1
- Update to latest version

* Sun May 31 2020 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.17.2-1
- Update to latest version

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 2.16.0-2
- Rebuilt for Python 3.9

* Sat May 09 2020 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.16.0-1
- Update to latest version

* Wed Apr 08 2020 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.14.0-1
- Update to latest version

* Thu Mar 26 2020 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.13.0-1
- Update to latest version

* Sat Mar 07 2020 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.12.0-1
- Update to latest version

* Fri Feb 21 2020 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.11.0-3
- Fix typo in dependency
- Fix flaky test

* Wed Feb 19 2020 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.11.0-2
- Fix minimum dependency versions
- Make keeping minimum dependency versions in sync a bit easier

* Wed Feb 19 2020 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.11.0-1
- Update to latest version

* Fri Feb 14 2020 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.10.1-1
- Update to latest version

* Tue Jan 28 2020 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.10.0-1
- Update to latest version

* Thu Jan 09 2020 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.9.1-1
- Update to latest version

* Fri Nov 22 2019 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.8.1-1
- Update to latest version

* Thu Nov 21 2019 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.8.0-1
- Update to latest version

* Tue Nov 12 2019 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.7.0-1
- Update to latest version
- Disabled distributed subpackage until it's available

* Thu Oct 17 2019 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.6.0-1
- Update to latest version

* Sat Oct 05 2019 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.5.2-1
- Update to latest version

* Sat Sep 28 2019 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.5.0-1
- Update to latest version

* Fri Sep 13 2019 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.4.0-1
- Update to latest version

* Thu Sep 12 2019 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.3.0-1
- Update to latest version

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2.1.0-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 23 2019 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 2.1.0-1
- Update to latest version

* Sat Apr 13 2019 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 1.2.0-1
- Update to latest version

* Mon Apr 01 2019 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 1.1.5-1
- Update to latest version

* Sat Mar 09 2019 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 1.1.4-1
- Update to latest version
- Remove now unnecessary patches

* Wed Mar 06 2019 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 1.1.3-3
- Mark partitioning test as expected failure on 32-bit systems as well

* Wed Mar 06 2019 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 1.1.3-2
- Add meta-subpackages for individual features

* Sat Mar 02 2019 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 1.1.3-1
- Initial package.

## END: Generated by rpmautospec
