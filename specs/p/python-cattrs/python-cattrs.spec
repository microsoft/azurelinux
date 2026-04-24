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

# Requires python-pymongo 4.4.0 or later, so disable for F41/F42.
# F43: disable until RHBZ#2356166 is fixed in python-pymongo.
%bcond bson %[ %{undefined fc42} && %{undefined fc41} ]
%bcond cbor2 1
%bcond msgpack 1
%bcond msgspec 1
%bcond orjson 1

#global commit xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#global snapdate YYYYMMDD

Name:           python-cattrs
Version:        25.3.0%{?commit:^%{snapdate}git%{sub %{commit} 1 7}}
Release:        %autorelease
Summary:        Python library for structuring and unstructuring data

# SPDX
License:        MIT
URL:            https://github.com/python-attrs/cattrs
# The GitHub archive contains tests and docs, which the PyPI sdist lacks
%if %{undefined commit}
Source:         %{url}/archive/v%{version}/cattrs-%{version}.tar.gz
%global srcversion %{version}
%else
Source:         %{url}/archive/%{commit}/cattrs-%{commit}.tar.gz
%global srcversion %(echo %{version} | cut -d '^' -f 1)
%endif

# Downstream: temporarily loosen version bounds on some test dependencies
Patch:          0001-Downstream-temporarily-loosen-version-bounds-on-some.patch

# Because an extras metapackage is conditionalized on architecture, the base
# package cannot be noarch – but the rest of the binary packages *are* noarch,
# with no compiled code.
%global debug_package %{nil}

BuildRequires:  python3-devel
BuildRequires:  tomcli

%global msgspec_enabled 0
%if %{with msgspec}
%ifnarch s390x %{ix86}
%global msgspec_enabled 1
%endif
%endif

%global _description %{expand:
cattrs is an open source Python library for structuring and
unstructuring data. cattrs works best with attrs classes and the usual
Python collections, but other kinds of classes are supported by
manually registering converters.}

%description %_description


%package -n python3-cattrs
Summary:        %{summary}

BuildArch:      noarch

%if %{without bson}
Obsoletes:      python3-cattrs+bson < 25.1.1-2
%endif
# Removed for Fedora 42; we can drop the Obsoletes after Fedora 44.
Obsoletes:      python-cattrs-doc < 24.1.2^20241004gitae80674-6

%description -n python3-cattrs %_description


# Most extras metapackages are noarch:
%pyproject_extras_subpkg -n python3-cattrs -a ujson pyyaml tomlkit
%if %{with bson}
%pyproject_extras_subpkg -n python3-cattrs -a bson
%endif
%if %{with cbor2}
%pyproject_extras_subpkg -n python3-cattrs -a cbor2
%endif
%if %{msgspec_enabled}
# python-msgspec is ExcludeArch: s390x i686; the extras metapackage is arched
# because it is not present on every architecture
%pyproject_extras_subpkg -n python3-cattrs msgspec
%endif
%if %{with msgpack}
%pyproject_extras_subpkg -n python3-cattrs -a msgpack
%endif
%if %{with orjson}
%pyproject_extras_subpkg -n python3-cattrs -a orjson
%endif


%prep
%autosetup -n cattrs-%{?!commit:%{version}}%{?commit:%{commit}}

# Don’t run benchmarks when testing
tomcli set pyproject.toml lists delitem 'dependency-groups.test' \
    'pytest-benchmark\b.*'
sed -r -i 's/ --benchmark[^[:blank:]"]*//g' pyproject.toml
# https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#_linters
tomcli set pyproject.toml lists delitem 'dependency-groups.test' \
    'coverage\b.*'

# Remove bundled fonts to show they are not packaged:
rm -rv docs/_static/fonts/


%generate_buildrequires
export SETUPTOOLS_SCM_PRETEND_VERSION='%{srcversion}'
%{pyproject_buildrequires \
    -x ujson \
%if %{with orjson}
    -x orjson \
%endif
%if %{with msgpack}
    -x msgpack \
%endif
    -x pyyaml \
    -x tomlkit \
%if %{with cbor2}
    -x cbor2 \
%endif
%if %{with bson}
    -x bson \
%endif
%if %{msgspec_enabled}
    -x msgspec \
%endif
    -g test}


%build
export SETUPTOOLS_SCM_PRETEND_VERSION='%{srcversion}'
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l cattrs cattr


%check
%if %{without bson} || %{without cbor2}
# These unconditionally import bson and cbor2, so they error during test
# collection
ignore="${ignore-} --ignore=tests/test_preconf.py"
ignore="${ignore-} --ignore=tests/preconf/test_pyyaml.py"
%endif

%if !%{msgspec_enabled}
k="${k-}${k+ and }not test_literal_dicts_msgspec"
k="${k-}${k+ and }not test_msgspec_efficient_enum"
k="${k-}${k+ and }not test_msgspec_json_converter"
k="${k-}${k+ and }not test_msgspec_json_unions"
k="${k-}${k+ and }not test_msgspec_json_unstruct_collection_overrides"
k="${k-}${k+ and }not test_msgspec_native_enums"
# These unconditionally import msgspec, so they error during test collection
ignore="${ignore-} --ignore=tests/preconf/test_msgspec_cpython.py"
%endif

%pytest --ignore-glob='bench/*' ${ignore-} -k "${k-}" -n auto


%files -n python3-cattrs -f %{pyproject_files}
%doc HISTORY.md
%doc README.md


%changelog
## START: Generated by rpmautospec
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 25.3.0-3
- Latest state for python-cattrs

* Sun Oct 12 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 25.3.0-2
- Add some additional test skips for msgspec

* Tue Oct 07 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 25.3.0-1
- Update to 25.3.0 (close RHBZ#2392250)

* Mon Oct 06 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 25.1.1-7
- Re-enable the bson extra in Fedora 43

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 25.1.1-6
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 25.1.1-5
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 25.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jun 06 2025 Python Maint <python-maint@redhat.com> - 25.1.1-3
- Rebuilt for Python 3.14

* Thu Jun 05 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 25.1.1-2
- Drop the bson extra until pymongo is fixed for Python 3.14

* Thu Jun 05 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 25.1.1-1
- Update to 25.1.1 (close RHBZ#2370344)

* Mon Jun 02 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 25.1.0-4
- Remove conditional support for building PDF documentation

* Mon Jun 02 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 25.1.0-3
- Skip tests failing on Python 3.14 until upstream acts

* Mon Jun 02 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 25.1.0-2
- No longer skip test_simple_roundtrip_defaults

* Mon Jun 02 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 25.1.0-1
- Update to 25.1.0 (close RHBZ#2354879)

* Thu Feb 27 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 24.1.2^20241004gitae80674-11
- Drop EPEL10-related conditionals
- EPEL10’s python-typing-extensions is too old to merge this back

* Thu Feb 27 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 24.1.2^20241004gitae80674-10
- Enable the bson extra starting with Fedora 43

* Thu Feb 27 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 24.1.2^20241004gitae80674-9
- Enable the msgpack extra in EPEL10

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 24.1.2^20241004gitae80674-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Jan 06 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 24.1.2^20241004gitae80674-6
- Drop Sphinx-generated PDF docs and obsolete `-doc` subpackage in F42+

* Mon Jan 06 2025 Miro Hrončok <miro@hroncok.cz> - 24.1.2^20241004gitae80674-4
- Avoid unneeded doc dependency on the furo theme

* Fri Oct 11 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 24.1.2^20241004gitae80674-3
- Deconditionalize using pytest-xdist
- It is now available in EPEL10.

* Fri Oct 11 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 24.1.2^20241004gitae80674-2
- Enable the msgspec extra on Fedora F41 and later
- The python-msgspec package now works with Python 3.13.

* Mon Oct 07 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 24.1.2^20241004gitae80674-1
- Update to a post-release snapshot with better Python 3.13 support

* Sun Sep 22 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 24.1.2-1
- Update to 24.1.2 (close RHBZ#2314095)

* Tue Sep 17 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 24.1.1-2
- Add conditionals to prepare for EPEL10 branching

* Mon Sep 16 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 24.1.1-1
- Update to 24.1.1 (close RHBZ#2301121, fix RHBZ#2309012)

* Mon Sep 16 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 23.2.3-10
- Enable the cbor2 extra

* Mon Sep 16 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 23.2.3-9
- Remove bundled fonts before building to show they are not packaged

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 23.2.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Python Maint <python-maint@redhat.com> - 23.2.3-6
- Rebuilt for Python 3.13

* Mon Jun 10 2024 Miro Hrončok <miro@hroncok.cz> - 23.2.3-5
- Drop unneeded build dependency on sphinx-autobuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 23.2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 23.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Jan 02 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 23.2.3-2
- Assert that the .dist-info directory contains a license file
- Do not package a duplicate license file

* Tue Dec 12 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 23.2.3-1
- Update to 23.2.3 (close RHBZ#2252344, fix RHBZ#2237277)
- Drop “bson” extra because python-pymongo is too old

* Tue Dec 12 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 23.1.2-2
- Confirm License is SPDX MIT

* Mon Aug 28 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 23.1.2-1
- Update to 23.1.2 (close RHBZ#2211212)

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 22.2.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Apr 13 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 22.2.0-13
- Depend on python-orjson now that it is available

* Sat Mar 18 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 22.2.0-12
- Don’t assume %%_smp_mflags is -j%%_smp_build_ncpus

* Wed Mar 01 2023 Miro Hrončok <miro@hroncok.cz> - 22.2.0-11
- Explicitly BuildRequire setuptools to build the documentation

* Thu Jan 26 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 22.2.0-10
- Build and package Sphinx documentation

* Thu Jan 26 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 22.2.0-9
- Run the tests

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 22.2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Dec 07 2022 Ankur Sinha (Ankur Sinha Gmail) <sanjay.ankur@gmail.com> - 22.2.0-7
- chore: check in sources

* Wed Dec 07 2022 Ankur Sinha (Ankur Sinha Gmail) <sanjay.ankur@gmail.com> - 22.2.0-6
- feat: remove more more unneeded BRs

* Wed Dec 07 2022 Ankur Sinha (Ankur Sinha Gmail) <sanjay.ankur@gmail.com> - 22.2.0-5
- feat: remove unneeded BRs

* Wed Dec 07 2022 Ankur Sinha (Ankur Sinha Gmail) <sanjay.ankur@gmail.com> - 22.2.0-4
- chore: remove macro for consistency

* Wed Dec 07 2022 Ankur Sinha (Ankur Sinha Gmail) <sanjay.ankur@gmail.com> - 22.2.0-3
- fix: explicitly mention license file

* Wed Dec 07 2022 Ankur Sinha (Ankur Sinha Gmail) <sanjay.ankur@gmail.com> - 22.2.0-2
- feat: loosed poetry call

* Wed Dec 07 2022 Ankur Sinha (Ankur Sinha Gmail) <sanjay.ankur@gmail.com> - 22.2.0-1
- feat: ready for re-review

* Wed Dec 07 2022 Ankur Sinha (Ankur Sinha Gmail) <sanjay.ankur@gmail.com> - 22.1.0-1
- wip: requires orjson, which requires maturin

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.9.0-5
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Oct 17 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.9.0-2
- Subpackage python2-cattrs has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Thu Sep 13 2018 Miro Hrončok <mhroncok@redhat.com> - 0.9.0-1
- Update to 0.9.0 to fix Python 3.7 FTBFS (#1605625)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.6.0-4
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 29 2018 Eric Smith <brouhaha@fedoraproject.org> 0.6.0-2
- Added missing BuildRequires for python2-enum34.

* Thu Jan 11 2018 Eric Smith <brouhaha@fedoraproject.org> 0.6.0-1
- Initial version.

## END: Generated by rpmautospec
