# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           python-rpm-macros
Summary:        The common Python RPM macros

URL:            https://src.fedoraproject.org/rpms/python-rpm-macros/

# Macros:
Source101:      macros.python
Source102:      macros.python-srpm
Source104:      macros.python3
Source105:      macros.pybytecompile

# Lua files
Source201:      python.lua

# Python code
%global compileall2_version 0.8.0
Source301:      https://github.com/fedora-python/compileall2/raw/v%{compileall2_version}/compileall2.py
Source302:      import_all_modules.py
%global pathfix_version 1.0.0
Source303:      https://github.com/fedora-python/pathfix/raw/v%{pathfix_version}/pathfix.py
Source304:      clamp_source_mtime.py

# BRP scripts
# This one is from redhat-rpm-config < 190
# A new upstream is forming in https://github.com/rpm-software-management/python-rpm-packaging/blob/main/scripts/brp-python-bytecompile
# But our version is riddled with Fedora-isms
# We might eventually move to upstream source + Fedora patches, but we are not there yet
Source401:      brp-python-bytecompile
# This one is from https://github.com/rpm-software-management/python-rpm-packaging/blob/main/scripts/brp-python-hardlink
# But we don't use a link in case it changes in upstream, there are no "versions" there yet
# This was removed from RPM 4.17+ so we maintain it here instead
Source402:      brp-python-hardlink
# This one is from redhat-rpm-config < 190
# It has no upstream yet
Source403:      brp-fix-pyc-reproducibility
# brp script to write "rpm" string into the .dist-info/INSTALLER file
Source404:      brp-python-rpm-in-distinfo

# macros and lua: MIT
# import_all_modules.py: MIT
# compileall2.py, clamp_source_mtime.py: PSF-2.0
# pathfix.py: PSF-2.0
# brp scripts: GPL-2.0-or-later
License:        MIT AND PSF-2.0 AND GPL-2.0-or-later

# The package version MUST be always the same as %%{__default_python3_version}.
# To have only one source of truth, we load the macro and use it.
# The macro is defined in python-srpm-macros.
%{lua:
if posix.stat(rpm.expand('%{SOURCE102}')) then
  rpm.load(rpm.expand('%{SOURCE102}'))
elseif posix.stat('macros.python-srpm') then
  -- something is parsing the spec without _sourcedir macro properly set
  rpm.load('macros.python-srpm')
end
}
Version:        %{__default_python3_version}
Release: 6%{?dist}

BuildArch:      noarch

# For %%__default_python3_pkgversion used in %%python_provide
# For python.lua
# For compileall2.py
Requires:       python-srpm-macros = %{version}-%{release}

# The packages are called python(3)-(s)rpm-macros
# We never want python3-rpm-macros to provide python-rpm-macros
# We opt out from all Python name-based automatic provides and obsoletes
%undefine __pythonname_provides
%undefine __pythonname_obsoletes

%description
This package contains the unversioned Python RPM macros, that most
implementations should rely on.

You should not need to install this package manually as the various
python?-devel packages require it. So install a python-devel package instead.


%package -n python-srpm-macros
Summary:        RPM macros for building Python source packages

# For directory structure and flags macros
# Versions before 190 contained some brp scripts moved into python-srpm-macros
Requires:       redhat-rpm-config >= 190

# We bundle our own software here :/
Provides:       bundled(python3dist(compileall2)) = %{compileall2_version}

%description -n python-srpm-macros
RPM macros for building Python source packages.


%package -n python3-rpm-macros
Summary:        RPM macros for building Python 3 packages

# For %%__python3 and %%python3
Requires:       python-srpm-macros = %{version}-%{release}

# For %%py_setup and import_all_modules.py
Requires:       python-rpm-macros = %{version}-%{release}

%description -n python3-rpm-macros
RPM macros for building Python 3 packages.


%prep
%autosetup -c -T
cp -a %{sources} .

# We want to have shebang in the script upstream but not here so
# the package with macros does not depend on Python.
sed -i '1s=^#!/usr/bin/env python3==' pathfix.py


%install
mkdir -p %{buildroot}%{rpmmacrodir}
install -m 644 macros.* %{buildroot}%{rpmmacrodir}/

mkdir -p %{buildroot}%{_rpmluadir}/fedora/srpm
install -p -m 644 -t %{buildroot}%{_rpmluadir}/fedora/srpm python.lua

mkdir -p %{buildroot}%{_rpmconfigdir}/redhat
install -m 644 compileall2.py %{buildroot}%{_rpmconfigdir}/redhat/
install -m 644 clamp_source_mtime.py %{buildroot}%{_rpmconfigdir}/redhat/
install -m 644 import_all_modules.py %{buildroot}%{_rpmconfigdir}/redhat/
install -m 644 pathfix.py %{buildroot}%{_rpmconfigdir}/redhat/
install -m 755 brp-* %{buildroot}%{_rpmconfigdir}/redhat/


# We define our own BRPs here to use the ones from the %%{buildroot},
# that way, this package can be built when it includes them for the first time.
# It also ensures that:
#  - our BRPs can execute
#  - if our BRPs affect this package, we don't need to build it twice
%define add_buildroot() %{lua:print((macros[macros[1]]:gsub(macros._rpmconfigdir, macros.buildroot .. macros._rpmconfigdir)))}
%global __brp_python_bytecompile %{add_buildroot __brp_python_bytecompile}
%global __brp_python_hardlink %{add_buildroot __brp_python_hardlink}
%global __brp_fix_pyc_reproducibility %{add_buildroot __brp_fix_pyc_reproducibility}
%global __brp_python_rpm_in_distinfo %{add_buildroot __brp_python_rpm_in_distinfo}


%check
# no macros in comments
grep -E '^#[^%%]*%%[^%%]' %{buildroot}%{rpmmacrodir}/macros.* && exit 1 || true


%files
%{rpmmacrodir}/macros.python
%{rpmmacrodir}/macros.pybytecompile
%{_rpmconfigdir}/redhat/import_all_modules.py
%{_rpmconfigdir}/redhat/pathfix.py

%files -n python-srpm-macros
%{rpmmacrodir}/macros.python-srpm
%{_rpmconfigdir}/redhat/compileall2.py
%{_rpmconfigdir}/redhat/clamp_source_mtime.py
%{_rpmconfigdir}/redhat/brp-python-bytecompile
%{_rpmconfigdir}/redhat/brp-python-hardlink
%{_rpmconfigdir}/redhat/brp-fix-pyc-reproducibility
%{_rpmconfigdir}/redhat/brp-python-rpm-in-distinfo
%{_rpmluadir}/fedora/srpm/python.lua

%files -n python3-rpm-macros
%{rpmmacrodir}/macros.python3


%changelog
* Mon Aug 11 2025 Lumír Balhar <lbalhar@redhat.com> - 3.14-5
- import_all_modules: Add error handling for import failures

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 21 2025 Íñigo Huguet <ihuguet@riseup.net> - 3.14-3
- pathfix.py: Don't fail on symbolic links

* Sun Jun 29 2025 Miro Hrončok <mhroncok@redhat.com> - 3.14-2
- Deprecate %%py3_build, %%py3_build_wheel, and %%py3_install
- Deprecate %%py_build, %%py_build_wheel, and %%py_install
- https://fedoraproject.org/wiki/Changes/DeprecateSetuppyMacros

* Wed May 28 2025 Karolina Surma <ksurma@redhat.com> - 3.14-1
- Update main Python to 3.14

* Mon Feb 10 2025 Tomáš Hrnčiar <thrnciar@redhat.com> - 3.13-5
- Add brp script to modify .dist-info/INSTALLER file

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jun 25 2024 Cristian Le <fedora@lecris.me> - 3.13-2
- %%python_extras_subpkg: Add option -a to include BuildArch: noarch

* Thu Jun 06 2024 Karolina Surma <ksurma@redhat.com> - 3.13-1
- Update main Python to 3.13

* Thu Mar 28 2024 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.12-9
- Minor improvements to brp-fix-pyc-reproducibility

* Fri Mar 22 2024 Lumír Balhar <lbalhar@redhat.com> - 3.12-8
- Update bundled compileall2 to version 0.8.0

* Thu Jan 25 2024 Miro Hrončok <mhroncok@redhat.com> - 3.12-7
- %%py3_test_envvars: Only set $PYTEST_XDIST_AUTO_NUM_WORKERS if not already set

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Oct 09 2023 Maxwell G <maxwell@gtmx.me> - 3.12-5
- Fix python macro memoizing to account for changing %%__python3

* Tue Sep 05 2023 Maxwell G <maxwell@gtmx.me> - 3.12-4
- Remove %%py3_build_egg and %%py3_install_egg macros.

* Wed Aug 09 2023 Karolina Surma <ksurma@redhat.com> - 3.12-3
- Declare the license as an SPDX expression

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Tomáš Hrnčiar <thrnciar@redhat.com> - 3.12-1
- Update main Python to Python 3.12
- https://fedoraproject.org/wiki/Changes/Python3.12

* Thu Mar 16 2023 Miro Hrončok <mhroncok@redhat.com> - 3.11-10
- Don't assume %%_smp_mflags only ever contains -jX, use -j%%_smp_build_ncpus directly
- Fixes: rhbz#2179149

* Fri Jan 20 2023 Miro Hrončok <mhroncok@redhat.com> - 3.11-9
- Memoize values of macros that execute python to get their value
- Fixes: rhbz#2155505

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.11-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Dec 19 2022 Miro Hrončok <mhroncok@redhat.com> - 3.11-7
- Bytecompilation: Unset $SOURCE_DATE_EPOCH when %%clamp_mtime_to_source_date_epoch is not set
- Bytecompilation: Pass --invalidation-mode=timestamp to compileall (on Python 3.7+)
- Bytecompilation: Clamp source mtime: https://fedoraproject.org/wiki/Changes/ReproducibleBuildsClampMtimes
- Bytecompilation: Compile Python files in parallel, according to %%_smp_mflags

* Sun Nov 13 2022 Miro Hrončok <mhroncok@redhat.com> - 3.11-6
- Set PYTEST_XDIST_AUTO_NUM_WORKERS=%%{_smp_build_ncpus} from %%pytest
- pytest-xdist 3+ respects this value when -n auto is used
- Expose the environment variables used by %%pytest via %%{py3_test_envvars}

* Tue Oct 25 2022 Lumír Balhar <lbalhar@redhat.com> - 3.11-5
- Include pathfix.py in this package

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jul 19 2022 Miro Hrončok <mhroncok@redhat.com> - 3.11-3
- Add "P" to %%py3_shbang_opts, %%py3_shbang_opts_nodash, %%py3_shebang_flags
  and to %%py_shbang_opts, %%py_shbang_opts_nodash, %%py_shebang_flags
- https://fedoraproject.org/wiki/Changes/PythonSafePath

* Mon Jun 20 2022 Miro Hrončok <mhroncok@redhat.com> - 3.11-2
- Define %%python3_cache_tag / %%python_cache_tag, e.g. cpython-311

* Mon Jun 13 2022 Tomáš Hrnčiar <thrnciar@redhat.com> - 3.11-1
- Update main Python to Python 3.11
- https://fedoraproject.org/wiki/Changes/Python3.11

* Thu May 26 2022 Owen Taylor <otaylor@redhat.com> - 3.10-18
- Support installing to %%{_prefix} other than /usr

* Tue Feb 08 2022 Tomas Orsava <torsava@redhat.com> - 3.10-17
- %%py_provides: Do not generate Obsoletes for names containing parentheses

* Mon Jan 31 2022 Miro Hrončok <mhroncok@redhat.com> - 3.10-16
- Explicitly opt-out from Python name-based provides and obsoletes generators

* Tue Dec 21 2021 Tomas Orsava <torsava@redhat.com> - 3.10-15
- Add lua helper functions to make it possible to automatically generate
  Obsoletes tags
- Modify the %%py_provides macro to also generate Obsoletes tags on CentOS/RHEL

* Wed Dec 08 2021 Miro Hrončok <mhroncok@redhat.com> - 3.10-14
- Set %%__python3 value according to %%python3_pkgversion
  I.e. when %%python3_pkgversion is 3.12, %%__python3 is /usr/bin/python3.12

* Mon Nov 01 2021 Karolina Surma <ksurma@redhat.com> - 3.10-13
- Fix multiline arguments processing for %%py_check_import
Resolves: rhbz#2018809
- Fix %%py_shebang_flags handling within %%py_check_import
Resolves: rhbz#2018615
- Process .pth files in buildroot's sitedirs in %%py_check_import
Resolves: rhbz#2018551
- Move import_all_modules.py from python-srpm-macros to python-rpm-macros

* Mon Oct 25 2021 Karolina Surma <ksurma@redhat.com> - 3.10-12
- Introduce -f (read from file) option to %%py{3}_check_import
- Introduce -t (filter top-level modules) option to %%py{3}_check_import
- Introduce -e (exclude module globs) option to %%py{3}_check_import

* Wed Oct 20 2021 Tomas Orsava <torsava@redhat.com> - 3.10-11
- Define a new macros %%python_wheel_dir and %%python_wheel_pkg_prefix

* Tue Oct 12 2021 Lumír Balhar <lbalhar@redhat.com> - 3.10-10
- Non-existing path in py_reproducible_pyc_path causes build to fail
Resolves: rhbz#2011056

* Thu Sep 09 2021 Miro Hrončok <mhroncok@redhat.com> - 3.10-9
- Set $RPM_BUILD_ROOT in %%{python3_...} macros
  to allow selecting alternate sysconfig install scheme based on that variable

* Thu Sep 09 2021 Petr Viktorin <pviktori@redhat.com> - 3.10-8
- Use --hardlink-dupes in %%py_byte_compile and brp-python-bytecompile
  (for Python 3)
- Resolves: rhbz#1977895

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.9-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 07 2021 Miro Hrončok <mhroncok@redhat.com> - 3.10-6
- Move Python related BuildRoot Policy scripts from redhat-rpm-config to python-srpm-macros

* Wed Jul 07 2021 Miro Hrončok <mhroncok@redhat.com> - 3.10-5
- Introduce %%py3_check_import

* Wed Jun 30 2021 Miro Hrončok <mhroncok@redhat.com> - 3.10-4
- Include brp-python-hardlink in python-srpm-macros since it is no longer in RPM 4.17+

* Mon Jun 28 2021 Miro Hrončok <mhroncok@redhat.com> - 3.10-3
- %%pytest: Set $PYTEST_ADDOPTS when %%{__pytest_addopts} is defined
- Related: rhzb#1935212

* Tue Jun 15 2021 Miro Hrončok <mhroncok@redhat.com> - 3.10-2
- Fix %%python_provide when fed python3.10-foo to obsolete python-foo instead of python--foo

* Tue Jun 01 2021 Miro Hrončok <mhroncok@redhat.com> - 3.10-1
- Update main Python to Python 3.10
- https://fedoraproject.org/wiki/Changes/Python3.10

* Tue Apr 27 2021 Miro Hrončok <mhroncok@redhat.com> - 3.9-38
- Escape %% symbols in macro files comments
- Fixes: rhbz#1953910

* Wed Apr 07 2021 Karolina Surma <ksurma@redhat.com> - 3.9-37
- Use sysconfig.get_path() to get %%python3_sitelib and %%python3_sitearch
- Fixes: rhbz#1946972

* Mon Mar 29 2021 Miro Hrončok <mhroncok@redhat.com> - 3.9-36
- Allow commas as argument separator for extras names in %%python_extras_subpkg
- Fixes: rhbz#1936486

* Sat Feb 20 2021 Miro Hrončok <mhroncok@redhat.com> - 3.9-35
- Fix %%python_extras_subpkg with underscores in extras names

* Mon Feb 08 2021 Miro Hrončok <mhroncok@redhat.com> - 3.9-34
- Remove python2-rpm-macros
- https://fedoraproject.org/wiki/Changes/Disable_Python_2_Dist_RPM_Generators_and_Freeze_Python_2_Macros

* Fri Feb 05 2021 Miro Hrončok <mhroncok@redhat.com> - 3.9-13
- Automatically word-wrap the description of extras subpackages
- Fixes: rhbz#1922442

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.9-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Dec 08 2020 Miro Hrončok <mhroncok@redhat.com> - 3.9-11
- Support defining %%py3_shebang_flags to %%nil

* Mon Sep 14 2020 Miro Hrončok <mhroncok@redhat.com> - 3.9-10
- Add %%python3_platform_triplet and %%python3_ext_suffix
- https://fedoraproject.org/wiki/Changes/Python_Upstream_Architecture_Names

* Fri Jul 24 2020 Lumír Balhar <lbalhar@redhat.com> - 3.9-9
- Adapt %%py[3]_shebang_fix to use versioned pathfixX.Y.py

* Fri Jul 24 2020 Lumír Balhar <lbalhar@redhat.com> - 3.9-8
- Disable Python hash seed randomization in %%py_byte_compile

* Tue Jul 21 2020 Lumír Balhar <lbalhar@redhat.com> - 3.9-7
- Make %%py3_dist respect %%python3_pkgversion

* Thu Jul 16 2020 Miro Hrončok <mhroncok@redhat.com> - 3.9-6
- Make the unversioned %%__python macro error
- https://fedoraproject.org/wiki/Changes/PythonMacroError
- Make %%python macros more consistent with %%python3 macros
- Define %%python_platform (as a Python version agnostic option to %%python3_platform)
- Add --no-index --no-warn-script-location pip options to %%pyX_install_wheel

* Wed Jul 08 2020 Miro Hrončok <mhroncok@redhat.com> - 3.9-5
- Introduce %%python_extras_subpkg
- Adapt %%py_dist_name to keep square brackets
- https://fedoraproject.org/wiki/Changes/PythonExtras

* Tue Jun 16 2020 Lumír Balhar <lbalhar@redhat.com> - 3.9-4
- Use compileall from stdlib for Python >= 3.9

* Thu Jun 11 2020 Miro Hrončok <mhroncok@redhat.com> - 3.9-3
- Allow to combine %%pycached with other macros (e.g. %%exclude or %%ghost) (#1838992)

* Sat May 30 2020 Miro Hrončok <mhroncok@redhat.com> - 3.9-2
- Require the exact same version-release of other subpackages of this package

* Thu May 21 2020 Miro Hrončok <mhroncok@redhat.com> - 3.9-1
- https://fedoraproject.org/wiki/Changes/Python3.9
- Switch the %%py_dist_name macro to convert dots (".") into dashes as defined in PEP 503 (#1791530)

* Mon May 11 2020 Miro Hrončok <mhroncok@redhat.com> - 3.8-8
- Implement %%pytest
- Implement %%pyX_shebang_fix
- Strip tildes from %%version in %%pypi_source by default

* Thu May 07 2020 Miro Hrončok <mhroncok@redhat.com> - 3.8-7
- Change %%__default_python3_pkgversion from 38 to 3.8

* Tue May 05 2020 Miro Hrončok <mhroncok@redhat.com> - 3.8-6
- Require recent enough SRPM macros from RPM macros, to prevent missing Lua files

* Tue May 05 2020 Miro Hrončok <mhroncok@redhat.com> - 3.8-5
- Implement %%py_provides

* Mon May 04 2020 Tomas Hrnciar <thrnciar@redhat.com> - 3.8-4
- Make %%py3_install_wheel macro remove direct_url.json file created by PEP 610.
- https://discuss.python.org/t/pep-610-usage-guidelines-for-linux-distributions/4012

* Mon Apr 27 2020 Miro Hrončok <mhroncok@redhat.com> - 3.8-3
- Make pythonX-rpm-macros depend on python-rpm-macros (#1827811)

* Tue Mar 31 2020 Lumír Balhar <lbalhar@redhat.com> - 3.8-2
- Update of bundled compileall2 module to 0.7.1 (bugfix release)

* Mon Mar 23 2020 Miro Hrončok <mhroncok@redhat.com> - 3.8-1
- Hardcode the default Python 3 version in the SRPM macros (#1812087)
- Provide python38-foo for python3-foo and the other way around (future RHEL compatibility)
- %%python_provide: Allow any names starting with "python" or "pypy"

* Mon Feb 10 2020 Miro Hrončok <mhroncok@redhat.com> - 3-54
- Update of bundled compileall2 module to 0.7.0
  Adds the optional --hardlink-dupes flag for compileall2 for pyc deduplication

* Thu Feb 06 2020 Miro Hrončok <mhroncok@redhat.com> - 3-53
- Define %%py(2|3)?_shbang_opts_nodash to be used with pathfix.py -a

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3-52
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Dec 28 2019 Miro Hrončok <mhroncok@redhat.com> - 3-51
- Define %%python, but make it work only if %%__python is redefined
- Add the %%pycached macro
- Remove stray __pycache__ directory from /usr/bin when running %%py_install,
  %%py_install_wheel and %%py_build_wheel macros

* Tue Nov 26 2019 Lumír Balhar <lbalhar@redhat.com> - 3-50
- Update of bundled compileall2 module

* Fri Sep 27 2019 Miro Hrončok <mhroncok@redhat.com> - 3-49
- Define %%python2 and %%python3

* Mon Aug 26 2019 Miro Hrončok <mhroncok@redhat.com> - 3-48
- Drop --strip-file-prefix option from %%pyX_install_wheel macros, it is not needed

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3-47
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jul 12 2019 Miro Hrončok <mhroncok@redhat.com> - 3-46
- %%python_provide: Switch python2 and python3 behavior
- https://fedoraproject.org/wiki/Changes/Python_means_Python3
- Use compileall2 module for byte-compilation with Python >= 3.4
- Do not allow passing arguments to Python during byte-compilation
- Use `-s` argument for Python during byte-compilation

* Tue Jul 09 2019 Miro Hrončok <mhroncok@redhat.com> - 3-45
- %%python_provide: Don't try to obsolete %%_isa provides

* Mon Jun 17 2019 Miro Hrončok <mhroncok@redhat.com> - 3-44
- Make %%__python /usr/bin/python once again until we are ready

* Mon Jun 10 2019 Miro Hrončok <mhroncok@redhat.com> - 3-43
- Define %%python_sitelib, %%python_sitearch, %%python_version, %%python_version_nodots,
  in rpm 4.15 those are no longer defined, the meaning of python is derived from %%__python.
- Usage of %%__python or the above-mentioned macros will error unless user defined.
- The %%python_provide macro no longer gives the arched provide for arched packages (#1705656)

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3-42
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Dec 20 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3-41
- Add %%python_disable_dependency_generator

* Wed Dec 05 2018 Miro Hrončok <mhroncok@redhat.com> - 3-40
- Workaround leaking buildroot PATH in %%py_byte_compile (#1647212)

* Thu Nov 01 2018 Petr Viktorin <pviktori@redhat.com> - 3-39
- Move "sleep 1" workaround from py3_build to py2_build (#1644923)

* Thu Sep 20 2018 Tomas Orsava <torsava@redhat.com> - 3-38
- Move the __python2/3 macros to the python-srpm-macros subpackage
- This facilitates using the %%{__python2/3} in Build/Requires

* Wed Aug 15 2018 Miro Hrončok <mhroncok@redhat.com> - 3-37
- Make %%py_byte_compile terminate build on SyntaxErrors (#1616219)

* Wed Aug 15 2018 Miro Hrončok <mhroncok@redhat.com> - 3-36
- Make %%py_build wokr if %%__python is defined to custom value

* Sat Jul 28 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3-35
- Change way how enabling-depgen works internally

* Sat Jul 14 2018 Tomas Orsava <torsava@redhat.com> - 3-34
- macros.pybytecompile: Detect Python version through sys.version_info instead
  of guessing from the executable name

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Tomas Orsava <torsava@redhat.com> - 3-32
- Fix %%py_byte_compile macro: when invoked with a Python 2 binary it also
  mistakenly ran py3_byte_compile

* Tue Jul 03 2018 Miro Hrončok <mhroncok@redhat.com> - 3-31
- Add %%python3_platform useful for PYTHONPATH on arched builds

* Mon Jun 18 2018 Jason L Tibbitts III <tibbs@math.uh.edu> - 3-30
- Add %%pypi_source macro, as well as %%__pypi_url and
  %%_pypi_default_extension.

* Wed Apr 18 2018 Miro Hrončok <mhroncok@redhat.com> - 3-29
- move macros.pybytecompile from python3-devel

* Fri Apr 06 2018 Tomas Orsava <torsava@redhat.com> - 3-28
- Fix the %%py_dist_name macro to not convert dots (".") into dashes, so that
  submodules can be addressed as well
Resolves: rhbz#1564095

* Fri Mar 23 2018 Miro Hrončok <mhroncok@redhat.com> - 3-27
- make LDFLAGS propagated whenever CFLAGS are

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 19 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3-25
- Add %%python_enable_dependency_generator

* Tue Nov 28 2017 Tomas Orsava <torsava@redhat.com> - 3-24
- Remove platform-python macros (https://fedoraproject.org/wiki/Changes/Platform_Python_Stack)

* Thu Oct 26 2017 Ville Skyttä <ville.skytta@iki.fi> - 3-23
- Use -Es/-I to invoke macro scriptlets (#1506355)

* Wed Aug 02 2017 Tomas Orsava <torsava@redhat.com> - 3-22
- Add platform-python macros (https://fedoraproject.org/wiki/Changes/Platform_Python_Stack)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Mar 03 2017 Michal Cyprian <mcyprian@redhat.com> - 3-20
- Revert "Switch %%__python3 to /usr/libexec/system-python"
  after the Fedora Change https://fedoraproject.org/wiki/Changes/Making_sudo_pip_safe
  was postponed

* Fri Feb 17 2017 Michal Cyprian <mcyprian@redhat.com> - 3-19
- Switch %%__python3 to /usr/libexec/system-python

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 23 2017 Michal Cyprian <mcyprian@redhat.com> - 3-17
- Add --no-deps option to py_install_wheel macros

* Tue Jan 17 2017 Tomas Orsava <torsava@redhat.com> - 3-16
- Added macros for Build/Requires tags using Python dist tags:
  https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Nov 24 2016 Orion Poplawski <orion@cora.nwra.com> 3-15
- Make expanded macros start on the same line as the macro

* Wed Nov 16 2016 Orion Poplawski <orion@cora.nwra.com> 3-14
- Fix %%py3_install_wheel (bug #1395953)

* Wed Nov 16 2016 Orion Poplawski <orion@cora.nwra.com> 3-13
- Add missing sleeps to other build macros
- Fix build_egg macros
- Add %%py_build_wheel and %%py_install_wheel macros

* Tue Nov 15 2016 Orion Poplawski <orion@cora.nwra.com> 3-12
- Add %%py_build_egg and %%py_install_egg macros
- Allow multiple args to %%py_build/install macros
- Tidy up macro formatting

* Wed Aug 24 2016 Orion Poplawski <orion@cora.nwra.com> 3-11
- Use %%rpmmacrodir

* Tue Jul 12 2016 Orion Poplawski <orion@cora.nwra.com> 3-10
- Do not generate useless Obsoletes with %%{?_isa}

* Fri May 13 2016 Orion Poplawski <orion@cora.nwra.com> 3-9
- Make python-rpm-macros require python-srpm-macros (bug #1335860)

* Thu May 12 2016 Jason L Tibbitts III <tibbs@math.uh.edu> - 3-8
- Add single-second sleeps to work around setuptools bug.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 14 2016 Orion Poplawski <orion@cora.nwra.com> 3-6
- Fix typo in %%python_provide

* Thu Jan 14 2016 Orion Poplawski <orion@cora.nwra.com> 3-5
- Handle noarch python sub-packages (bug #1290900)

* Wed Jan 13 2016 Orion Poplawski <orion@cora.nwra.com> 3-4
- Fix python2/3-rpm-macros package names

* Thu Jan 7 2016 Orion Poplawski <orion@cora.nwra.com> 3-3
- Add empty %%prep and %%build

* Mon Jan 4 2016 Orion Poplawski <orion@cora.nwra.com> 3-2
- Combined package

* Wed Dec 30 2015 Orion Poplawski <orion@cora.nwra.com> 3-1
- Initial package
