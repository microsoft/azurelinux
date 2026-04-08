# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%if  0%{?rhel} && 0%{?rhel} <= 7
  # There is no python3-gobject-base in RHEL 7. But it exists in EPEL 7.
  %global meson_python_flags -Dwith_py2=true -Dwith_py3=true
  %global build_python2 1
  %global build_python3 1
%else
  %global meson_python_flags -Dwith_py2=false -Dwith_py3=true
  %global build_python2 0
  %global build_python3 1
%endif

%if (0%{?fedora} && 0%{?fedora} <= 50) || (0%{?rhel} && 0%{?rhel} <= 10)
  # Support RHEL 8 module builds with an invalid buildorder.
  %global meson_accept_overflowed_buildorder_flag -Daccept_overflowed_buildorder=true
%else
  %global meson_accept_overflowed_buildorder_flag -Daccept_overflowed_buildorder=false
%endif

%global upstream_name libmodulemd

%if (0%{?rhel} && 0%{?rhel} <= 7)
  %global v2_suffix 2
%endif

Name:           %{upstream_name}%{?v2_suffix}
Version:        2.15.2
Release:        4%{?dist}
Summary:        Module metadata manipulation library

# COPYING:      MIT
## not in any binary package
# contrib/coverity-modeling.c:  GPL-2.0-or-later
# contrib/release-tools/semver: GPL-3.0-only
# modulemd/tests/test_data/f29.yaml:            Apache-2.0
# modulemd/tests/test_data/f29-updates.yaml:    Apache-2.0
# xml_specs/reduced/tests/good/module_stream_build_license.xml: MIT AND GPL-3.0-or-later
License:        MIT
SourceLicense:  %{license} AND GPL-3.0-only AND GPL-3.0-or-later AND GPL-2.0-or-later AND Apache-2.0
URL:            https://github.com/fedora-modularity/libmodulemd
Source0:        %{url}/releases/download/%{version}/modulemd-%{version}.tar.xz
Source1:        %{url}/releases/download/%{version}/modulemd-%{version}.tar.xz.asc
# Key exported from Petr Pisar's keyring
Source2:        gpgkey-E3F42FCE156830A80358E6E94FD1AEC3365AF7BF.gpg

BuildRequires:  gnupg2
BuildRequires:  meson >= 0.47
BuildRequires:  pkgconfig
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(yaml-0.1)
BuildRequires:  pkgconfig(gtk-doc)
BuildRequires:  glib2-doc
BuildRequires:  rpm-devel
%if %{build_python2}
BuildRequires:  python2-devel
BuildRequires:  python-gobject-base
%endif
%if %{build_python3}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-gobject-base
%endif
%if 0%{?fedora} >= 40 && 0%{?fedora} < 42
# glib2 version with g_once_init_enter_pointer symbol, bug #2265336
Requires:       glib2 >= 2.79.0-2
%endif


%description
C library for manipulating module metadata files.
See https://github.com/fedora-modularity/libmodulemd/blob/main/README.md for
more details.


%if %{build_python2}
%package -n python2-%{name}
Summary:        Python 2 bindings for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       python-gobject-base
Requires:       python-six

%description -n python2-%{name}
Python 2 bindings for %{name}.
%endif


%if %{build_python3}
%package -n python%{python3_pkgversion}-%{name}
Summary:        Python 3 bindings for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       python%{python3_pkgversion}-gobject-base
%if (0%{?rhel} && 0%{?rhel} <= 7)
# The py3_dist macro on EPEL 7 doesn't work right at the moment
Requires:       python3.6dist(six)
%else
Requires:       %{py3_dist six}
%endif

%description -n python%{python3_pkgversion}-%{name}
Python %{python3_pkgversion} bindings for %{name}.
%endif


%package devel
Summary:        Development files for libmodulemd
Requires:       %{name}%{?_isa} = %{version}-%{release}
%if (0%{?rhel} && 0%{?rhel} <= 7)
Conflicts:      libmodulemd1-devel
Conflicts:      libmodulemd-devel
%endif


%description devel
Development files for %{name}.


%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -p1 -n modulemd-%{version}


%build
%meson \
    %{meson_accept_overflowed_buildorder_flag} \
    -Drpmio=enabled \
    -Dskip_introspection=false \
    -Dtest_installed_lib=false \
    -Dwith_docs=true \
    -Dwith_manpages=enabled \
    %{meson_python_flags}
%meson_build


%check
export LC_CTYPE=C.utf8
# The tests sometimes time out in CI, so give them a little extra time
%{__meson} test -C %{_vpath_builddir} %{?_smp_mesonflags} --print-errorlogs -t 5


%install
%meson_install

%if ( 0%{?rhel} && 0%{?rhel} <= 7)
# Don't conflict with modulemd-validator from 1.x included in the official
# RHEL 7 repos
mv %{buildroot}%{_bindir}/modulemd-validator \
   %{buildroot}%{_bindir}/modulemd-validator%{?v2_suffix}

mv %{buildroot}%{_mandir}/man1/modulemd-validator.1 \
   %{buildroot}%{_mandir}/man1/modulemd-validator%{?v2_suffix}.1
%endif


%ldconfig_scriptlets


%files
%license COPYING
%doc NEWS README.md
%{_bindir}/modulemd-validator%{?v2_suffix}
%{_mandir}/man1/modulemd-validator%{?v2_suffix}.1*
%{_libdir}/%{upstream_name}.so.2*
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/Modulemd-2.0.typelib


%files devel
%{_libdir}/%{upstream_name}.so
%{_libdir}/pkgconfig/modulemd-2.0.pc
%{_includedir}/modulemd-2.0/
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/Modulemd-2.0.gir
%dir %{_datadir}/gtk-doc
%dir %{_datadir}/gtk-doc/html
%{_datadir}/gtk-doc/html/modulemd-2.0/


%if %{build_python2}
%files -n python2-%{name}
%{python2_sitearch}/gi/overrides/
%endif


%if %{build_python3}
%files -n python%{python3_pkgversion}-%{name}
%{python3_sitearch}/gi/overrides/
%endif


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 2.15.2-4
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 2.15.2-3
- Rebuilt for Python 3.14.0rc2 bytecode

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.15.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jun 18 2025 Petr Pisar <ppisar@redhat.com> - 2.15.2-1
- 2.15.2 bump

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 2.15.1-2
- Rebuilt for Python 3.14

* Fri May 09 2025 Petr Pisar <ppisar@redhat.com> - 2.15.1-1
- 2.15.1 bump

* Mon Jan 20 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.15.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.15.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.15.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 2.15.0-13
- Rebuilt for Python 3.13

* Thu May 16 2024 Petr Pisar <ppisar@redhat.com> - 2.15.0-12
- Use canonical "dnf builddep" command in STI tests

* Wed May 15 2024 Petr Pisar <ppisar@redhat.com> - 2.15.0-11
- Do not install Python 2 packages in Fedora STI tests

* Wed May 15 2024 Petr Pisar <ppisar@redhat.com> - 2.15.0-10
- Fix building with glib2-doc 2.80.1 (upstream bug #619)

* Tue Feb 27 2024 Petr Pisar <ppisar@redhat.com> - 2.15.0-9
- Require glib2 version with g_once_init_enter_pointer symbol (bug #2265336)

* Mon Jan 29 2024 Petr Pisar <ppisar@redhat.com> - 2.15.0-8
- Fix building with glib2-doc 2.79.0

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.15.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.15.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.15.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 2.15.0-4
- Rebuilt for Python 3.12

* Wed May 10 2023 Florian Festi <ffesti@redhat.com>  - 2.15.0-3
- Rebuild for rpm-4.18.90

* Wed May 10 2023 Petr Pisar <ppisar@redhat.com> - 2.15.0-2
- Adapt STI tests to current meson

* Wed May 10 2023 Petr Pisar <ppisar@redhat.com> - 2.15.0-1
- 2.15.0 bump

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2.14.0-3
- Rebuilt for Python 3.11

* Tue Feb 08 2022 Petr Pisar <ppisar@redhat.com> - 2.14.0-2
- Drop removed meson -D developer_build option from CI tests

* Fri Feb 04 2022 Petr Pisar <ppisar@redhat.com> - 2.14.0-1
- 2.14.0 bump

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Sep 14 2021 Petr Pisar <ppisar@redhat.com> - 2.13.0-3
- Accept an invalid buildorder 18446744073709551615 found in RHEL 8 repositories
  (https://pagure.io/koji/issue/3025)

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jul 09 2021 Petr Pisar <ppisar@redhat.com> - 2.13.0-1
- 2.13.0 bump

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.12.1-2
- Rebuilt for Python 3.10

* Mon May 03 2021 Petr Pisar <ppisar@redhat.com> - 2.12.1-1
- 2.12.1 bump

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan 14 2021 Stephen Gallagher <sgallagh@redhat.com> - 2.12.0-1
- Add support for 'buildorder' to Packager documents

* Tue Jan 12 2021 Stephen Gallagher <sgallagh@redhat.com> - 2.11.2-2
- Fix issue with ModuleIndex when input contains only Obsoletes documents
- Fix import issue when built with Python 2 support

* Thu Jan 07 2021 Stephen Gallagher <sgallagh@redhat.com> - 2.11.2-1
- Release 2.11.2
- Extend read_packager_[file|string]() to support overriding the module name
  and stream.

* Thu Dec 17 2020 Stephen Gallagher <sgallagh@redhat.com> - 2.11.1-1
- Release 2.11.1
- Ignore Packager documents when running ModuleIndex.update_from_*()
- Add python overrides for XMD in PackagerV3
- Add python override to ignore the GType return when reading packager files
- Add PackagerV3.get_mdversion()

* Thu Dec 10 2020 Stephen Gallagher <sgallagh@redhat.com> - 2.11.0-1
- Release 2.11.0

* Fri Nov 20 2020 Stephen Gallagher <sgallagh@redhat.com> - 2.10.0-2
- Fix integer size issue on 32-bit platforms

* Fri Nov 20 2020 Stephen Gallagher <sgallagh@redhat.com> - 2.10.0-1
- Release 2.10.0
- https://github.com/fedora-modularity/libmodulemd/releases/tag/libmodulemd-2.10.0

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon May 25 2020 Miro Hrončok <mhroncok@redhat.com> - 2.9.4-2
- Rebuilt for Python 3.9

* Wed May 20 2020 Stephen Gallagher <sgallagh@redhat.com> - 2.9.4-1
- new upstream release: 2.9.4

* Wed May 20 2020 Stephen Gallagher <sgallagh@redhat.com> - 2.9.4-2.9.300520.1gitgc19757c
- new upstream release: 2.9.4

* Wed Apr 08 2020 Stephen Gallagher <sgallagh@redhat.com> - 2.9.3-1
- new upstream release: 2.9.3

* Wed Apr 01 2020 Stephen Gallagher <sgallagh@redhat.com> - 2.9.2-4
- Skip rpmdeplint from gating due to https://github.com/fedora-infra/bodhi/issues/3944

* Wed Apr 01 2020 Stephen Gallagher <sgallagh@redhat.com> - 2.9.2-3
- Fix build against Python 3.9
- Resolves: rhbz#1817665

* Wed Mar 11 2020 Stephen Gallagher <sgallagh@redhat.com> - 2.9.2-2
- new upstream release: 2.9.2

* Wed Mar 11 2020 Stephen Gallagher <sgallagh@redhat.com> - 2.9.2-0.20200311.1gitg31bbd4e
- new upstream release: 2.9.2

* Wed Mar 11 2020 Stephen Gallagher <sgallagh@redhat.com> - 2.9.2-0.20200311.1gitg31bbd4e
- new upstream release: 2.9.2

* Fri Feb 14 2020 Stephen Gallagher <sgallagh@redhat.com> - 2.9.1-1
- new upstream release: 2.9.1

* Wed Feb 12 2020 Stephen Gallagher <sgallagh@redhat.com> - 2.9.0-1
- new upstream release: 2.9.0

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 09 2020 Stephen Gallagher <sgallagh@redhat.com> - 2.8.3-1
- Update to 2.8.3
- Fix compilation issue with glib >= 2.63.3
- Improved modulemd document validation
- Numerous test enhancements

* Thu Oct 24 2019 Stephen Gallagher <sgallagh@redhat.com> - 2.8.2-1
- Update to 2.8.2
- Use safer version of dup()
- Fix loading of YAML module stream with no module or stream name

* Tue Oct 15 2019 Stephen Gallagher <sgallagh@redhat.com> - 2.8.1-1
- Improve the merge logic to handle third-party repos more sanely

* Wed Sep 18 2019 Stephen Gallagher <sgallagh@redhat.com> - 2.8.0-2
- Improvements to ModuleIndex.update_from_defaults_directory()
  * Import each file in the directory as a merge rather than an overwrite so
    we can detect conflicts.
  * Modify the meaning of the 'strict' argument to fail if the merge would
    result in a conflict in the default stream setting of a module.

* Wed Sep 04 2019 Stephen Gallagher <sgallagh@redhat.com> - 2.8.0-1
- Update to 2.8.0
- API Changes
  * Add Modulemd.Module.get_translation() - Retrieve the translations
    associated with a Modulemd.Module
  * Add ModuleIndex.update_from_defaults_directory() - Import defaults from a
    directory of yaml documents, such as fedora-module-defaults, optionally
    providing a second path containing overrides.
- Enhancements
  * Modulemd.ModuleIndex.update_from_file() now supports reading files
    compressed with gzip, bzip2 or xz. (Issue: #208)
  * Documentation updates
- Bugfixes
  * Assorted minor issues discovered by static analysis tools.

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2.7.0-2
- Rebuilt for Python 3.8

* Thu Aug 15 2019 Stephen Gallagher <sgallagh@redhat.com> - 2.7.0-1
- Update to 2.7.0
- Drop libmodulemd1 subpackage which is now packaged separately
- Add support for 'buildroot' and 'srpm-buildroot' arguments to components

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 03 2019 Stephen Gallagher <sgallagh@redhat.com> - 2.6.0-1
- Update to 2.6.0
- New function ModuleIndexMerger.resolve_ext() allowing for strict merging
- Profile.get_description() now properly returns available translations
- Numerous documentation fixes
- Test improvements

* Wed May 29 2019 Stephen Gallagher <sgallagh@redhat.com> - 2.5.0-2
- Fix memory issue with Module.search_streams() in the python bindings

* Wed May 22 2019 Stephen Gallagher <sgallagh@redhat.com> - 2.5.0-1
- Update to 2.5.0 and 1.8.11
- Ensure that XMD is always emitted in the same order
- Add .clear_*() functions for all .add_*() functions
- Add ModuleStream.equals()
- Add ModuleIndex.get_default_streams()

* Mon May 13 2019 Stephen Gallagher <sgallagh@redhat.com> - 2.4.0-1
- Update to 2.4.0 and 1.8.10
- Add ModuleStreamV2.clear_dependencies() and .remove_dependencies()
- Fix bugs and memory issues with the XMD python bindings
- Assorted documentation enhancements

* Fri May 03 2019 Stephen Gallagher <sgallagh@redhat.com> - 2.3.1-1
- Update to 2.3.1
- Make Modulemd.Component.set_*() functions accept NULL
- Fix segmentation fault in XMD code due to improper memory management
- Fix incompatibility in python2-libmodulemd GObject overrides
- Fix assorted documentation issues

* Mon Apr 22 2019 Stephen Gallagher <sgallagh@redhat.com> - 2.3.0-1
- Add ModuleIndex.update_from_custom()
- Add ModuleIndex.dump_to_custom()
- Add Component.equals()
- Add Module.remove_streams_by_NSVCA()
- Fix bug with emitting lists of scalars in XMD
- Fix bug with deduplication in the ModuleIndexMerger
- Fix serious memory leak

* Tue Apr 16 2019 Adam Williamson <awilliam@redhat.com> - 2.2.3-3
- Rebuild with Meson fix for #1699099

* Wed Apr 03 2019 Stephen Gallagher <sgallagh@redhat.com> - 2.2.3-2
- Fix accidental ABI break

* Mon Apr 01 2019 Stephen Gallagher <sgallagh@redhat.com> - 2.2.3-1
- Update to 2.2.3 and 1.8.6
- Fix header issue with ModulemdRpmMapEntry

* Wed Mar 27 2019 Stephen Gallagher <sgallagh@redhat.com> - 2.2.2-2
- Don't run tests on armv7hl/aarch64 since they have timeout problems

* Wed Mar 27 2019 Stephen Gallagher <sgallagh@redhat.com> - 2.2.2-1
- Update to libmodulemd 2.2.2
- Add support for python2 on RHEL and Fedora < 31
- Make python subpackages archful for GObject overrides

* Tue Mar 26 2019 Stephen Gallagher <sgallagh@redhat.com> - 2.2.1-1
- Update to libmodulemd 2.2.1
- Fixes builds on i686
- Fixes an accidental API error

* Tue Mar 26 2019 Stephen Gallagher <sgallagh@redhat.com> - 2.2.0-1
- Update to libmodulemd 2.2.0
- Support for RPM checksums
- Adds a new directive: "buildafter" for specifying build dependencies
- Adds a new directive: "buildonly" to indicate that a component's built
  artifacts should be listed in the "filter" field.
- Deprecate lookup functions by NSVC in favor of NSVCA (including the
  architecture.

* Fri Mar 01 2019 Stephen Gallagher <sgallagh@redhat.com> - 2.1.0-4
- Don't run tests on 32-bit ARM due to performance issues causing timeouts

* Fri Mar 01 2019 Stephen Gallagher <sgallagh@redhat.com> - 2.1.0-3
- Have python3-libmodulemd1 properly Obsolete libmodulemd and
  python3-libmodulemd < 2.

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jan 26 2019 Stephen Gallagher <sgallagh@redhat.com> - 2.1.0-1
- Update to libmodulemd 2.1.0 and 1.8.2
- Drop upstreamed patches
- Add new API ModuleStream.depends_on_stream() and
  ModuleStream.build_depends_on_stream() to help support auto-detection of
  when a module stream may need to be rebuilt when its dependencies change.
- Don't fail merges when default streams differ, treat it as "no default for
  this module"
- Fix error message
- Copy modified value when copying Modulemd.Defaults objects
- Fixes discovered by clang and coverity static analysis tools
- Test improvements

* Fri Jan 11 2019 Stephen Gallagher <sgallagh@redhat.com> - 2.0.0-3
- Fix ordering issue with dependencies
- Use glib2 suppression file when running valgrind tests

* Fri Jan 11 2019 Stephen Gallagher <sgallagh@redhat.com> - 2.0.0-2
- Fix issue reading modified value for defaults from YAML streams

* Thu Dec 13 2018 Stephen Gallagher <sgallagh@redhat.com> - 2.0.0-1
- Update to 2.0.0 final
- Assorted fixes for validation
- Add modulemd-validator tool based on v2 code
- Fix a crash when merging defaults

* Tue Dec 11 2018 Stephen Gallagher <sgallagh@redhat.com> - 2.0.0-0.beta2
- Update to 2.0.0beta2
- Better validation of stored content during read and write operations
- ModuleIndex now returns FALSE if any subdocument fails
- Fix tests on 32-bit platforms
- Make unknown keys in YAML maps non-fatal for libmodulemd1
- Make unknown keys in YAML maps optionally fatal for libmodulemd 2.x
- Fix RPM version requirements for libmodulemd1

* Mon Dec 10 2018 Stephen Gallagher <sgallagh@redhat.com> - 2.0.0-0.beta1
- Update to 2.0.0beta1
- Total rewrite to 2.0 API
- https://sgallagh.fedorapeople.org/docs/libmodulemd/2.0/

* Fri Oct 26 2018 Stephen Gallagher <sgallagh@redhat.com> - 1.7.0-1
- Update to 1.7.0
- Enhance YAML parser for use with `fedmod lint`
- Support running unit tests against installed packages
- Include all NSVCs for ModuleStreams in ImprovedModule

* Tue Sep 18 2018 Stephen Gallagher <sgallagh@redhat.com> - 1.6.4-1
- Update to 1.6.4.
- Add Buildopts to the documentation.
- Deduplicate module streams when merging.
- Drop upstreamed patches.

* Thu Sep 06 2018 Stephen Gallagher <sgallagh@redhat.com> - 1.6.3-2
- Fix generation of module component YAML
- Output NSVC information using decimal version

* Tue Sep 04 2018 Stephen Gallagher <sgallagh@redhat.com> - 1.6.3-1
- Update to 1.6.3
- Drop upstreamed patch
- Don't return ModuleStream objects from modulemd_module_new_all_from_*_ext()
- Ensure that Component buildorder property is signed
- Work around optimization bug
- Don't crash dumping translation events without summary or desc

* Thu Aug 09 2018 Stephen Gallagher <sgallagh@redhat.com> - 1.6.2-2
- Fix backwards-incompatible API change
- Resolves: rhbz#1607083

* Tue Aug 07 2018 Stephen Gallagher <sgallagh@redhat.com> - 1.6.2-1
- Update to 1.6.2
- Make buildorder a signed integer to match modulemd specification

* Mon Jul 23 2018 Stephen Gallagher <sgallagh@redhat.com> - 1.6.1-2
- Obsolete unsupported pythonX-modulemd packages

* Fri Jul 20 2018 Stephen Gallagher <sgallagh@redhat.com> - 1.6.1-1
- Update to 1.6.1
- Fix header include ordering
- Suppress empty sections from .dump() ordering

* Wed Jul 18 2018 Stephen Gallagher <sgallagh@redhat.com> - 1.6.0-1
- Update to 1.6.0
- Adds Modulemd.ModuleStream object, deprecating Modulemd.Module
- Adds Modulemd.Translation and Modulemd.TranslationEntry objects
- Adds Modulemd.ImprovedModule object that collects streams, defaults and
  translations together
- Adds new Modulemd.index_from_*() funtions to get a hash table of
  Modulemd.ImprovedModule objects for easier searching
- Moves function documentation to the public headers
- Corrects the license headers to MIT (they were incorrectly listed as MITNFA
  in previous releases)
- Makes the "eol" field optional for Modulemd.ServiceLevel
- Clean up HTML documentation
- Fixes a type error on 32-bit systems

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 23 2018 Stephen Gallagher <sgallagh@redhat.com> - 1.5.2-1
- Update to libdmodulemd 1.5.2
- Don't free uninitialized memory

* Fri Jun 22 2018 Stephen Gallagher <sgallagh@redhat.com> - 1.5.1-2
- Fix buildopts property not being initialized

* Tue Jun 19 2018 Stephen Gallagher <sgallagh@redhat.com> - 1.5.1-1
- Update to version 1.5.1
- Re-enable build-time tests

* Mon Jun 18 2018 Stephen Gallagher <sgallagh@redhat.com> - 1.5.0-2
- Temporarily disable build-time tests

* Mon Jun 18 2018 Stephen Gallagher <sgallagh@redhat.com> - 1.5.0-1
- Update to version 1.5.0
- Adds support for "intents" in Modulemd.Defaults
- Adds `Modulemd.get_version()`
- Adds support for RPM whitelists in the buildopts
- Adds a new object: Modulemd.Buildopts
- Deprecates Modulemd.Module.get_rpm_buildopts()
- Deprecates Modulemd.Module.set_rpm_buildopts()
- Fixes some missing license blurbs

* Tue May 08 2018 Stephen Gallagher <sgallagh@redhat.com> - 1.4.1-1
- Update to version 1.4.1
- Improve output from modulemd-validator
- Drop upstreamed patches

* Wed Apr 25 2018 Stephen Gallagher <sgallagh@redhat.com> - 1.4.0-2
- Fix pointer math error
- Fix compilation failure in Fedora build system

* Wed Apr 25 2018 Stephen Gallagher <sgallagh@redhat.com> - 1.4.0-1
- Update to version 1.4.0
- Adds new API for returning failed YAML subdocuments
- Stop emitting log messages by default (polluting consumer logs)
- Validate RPM artifacts for proper NEVRA format
- Improve the validator tool
- Drop upstreamed patch

* Mon Apr 16 2018 Stephen Gallagher <sgallagh@redhat.com> - 1.3.0-2
- Fix serious error in modulemd-defaults emitter

* Fri Apr 13 2018 Stephen Gallagher <sgallagh@redhat.com> - 1.3.0-1
- Update to version 1.3.0
- New Public Objects:
  * Modulemd.Prioritizer - tool to merge module defaults
- New Public Functions:
  * Modulemd.SimpleSet.is_equal()
  * Modulemd.Defaults.copy()
  * Modulemd.Defaults.merge()

* Wed Apr 04 2018 Stephen Gallagher <sgallagh@redhat.com> - 1.2.0-1
- Update to version 1.2.0
- New Functions:
  * Modulemd.objects_from_file()
  * Modulemd.objects_from_string()
  * Modulemd.dump()
  * Modulemd.dumps()
  * Modulemd.Defaults.new_from_file()
  * Modulemd.Defaults.new_from_string()
- Deprecated Functions:
  * Modulemd.Module.new_all_from_file()
  * Modulemd.Module.new_all_from_file_ext()
  * Modulemd.Module.new_all_from_string()
  * Modulemd.Module.new_all_from_string_ext()
  * Modulemd.Module.dump_all()
  * Modulemd.Module.dumps_all()
- Bugfixes
  * Properly use G_BEGIN_DECLS and G_END_DECLS in headers
  * Assorted fixes for memory ownership in GObject Introspection

* Fri Mar 23 2018 Stephen Gallagher <sgallagh@redhat.com> - 1.1.3-2
- Fix missing G_END_DECL from public headers

* Mon Mar 19 2018 Stephen Gallagher <sgallagh@redhat.com> - 1.1.3-1
- Fix numerous memory leaks
- Drop upstreamed patch

* Thu Mar 15 2018 Stephen Gallagher <sgallagh@redhat.com> - 1.1.2-1
- Update to version 1.1.2
- Revert backwards-incompatible API change
- Fix version string in pkgconfig file

* Thu Mar 15 2018 Stephen Gallagher <sgallagh@redhat.com> - 1.1.1-1
- Update to version 1.1.1
- Make default stream and profiles optional
- Fixes: https://github.com/fedora-modularity/libmodulemd/issues/25
- Fixes: https://github.com/fedora-modularity/libmodulemd/issues/26
- Fixes: https://github.com/fedora-modularity/libmodulemd/issues/27

* Wed Mar 14 2018 Stephen Gallagher <sgallagh@redhat.com> - 1.1.0-1
- Update to version 1.1.0
- Adds support for handling modulemd-defaults YAML documents
- Adds peek()/dup() routines to all object properties
- Adds Modulemd.Module.dup_nsvc() to retrieve the canonical form of the unique module identifier.
- Adds support for boolean types in the XMD section
- Revert obsoletion of pythonX-modulemd packages for now

* Tue Mar 13 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.0.4-2
- Obsolete unsupported pythonX-modulemd packages

* Tue Feb 27 2018 Stephen Gallagher <sgallagh@redhat.com> - 1.0.4-1
- Update to 1.0.4
- Rework version autodetection
- Avoid infinite loop on unparseable YAML

* Sun Feb 25 2018 Stephen Gallagher <sgallagh@redhat.com> - 1.0.3-1
- RPM components are properly emitted when no module components exist
- Parser works around late determination of modulemd version

* Fri Feb 16 2018 Stephen Gallagher <sgallagh@redhat.com> - 1.0.2-1
- Be more strict with certain parser edge-cases
- Replace popt argument processing with glib
- Drop upstreamed patches

* Thu Feb 15 2018 Stephen Gallagher <sgallagh@redhat.com> - 1.0.1-2
- Handle certain unlikely format violations

* Thu Feb 15 2018 Stephen Gallagher <sgallagh@redhat.com> - 1.0.1-1
- Support modulemd v2
- Add tool to do quick validation of modulemd
- Fix memory management
- Warn and ignore unparseable sub-documents in the YAML
- Fix several memory issues detected by Coverity scan

* Tue Feb 06 2018 Stephen Gallagher <sgallagh@redhat.com> - 0.2.2-1
- Update to libmodulemd 0.2.2
- Fix numerous minor memory leaks
- Fix issues with EOL/SL dates

* Tue Feb 06 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.2.1-3
- Own appropriate directories

* Fri Feb 02 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.2.1-2
- Switch to %%ldconfig_scriptlets

* Fri Jan 05 2018 Stephen Gallagher <sgallagh@redhat.com> - 0.2.1-1
- Update to libmodulemd 0.2.1
- Add 'name' property for Profiles

* Thu Oct 05 2017 Stephen Gallagher <sgallagh@redhat.com> - 0.2.0-2
- Add missing BuildRequires for gtk-doc

* Thu Oct 05 2017 Stephen Gallagher <sgallagh@redhat.com> - 0.2.0-1
- Update to libmodulemd 0.2.0
- Adds gtk-doc generated documentation
- (ABI-break) Makes all optional properties accept NULL as a value to clear
  them
- (ABI-break) Modulemd.SimpleSet takes a STRV (char **) instead of a
  GLib.PtrArray
- Fixes a bug where the name was not always set for components
- Adds support for dumping YAML from the introspected API
- Includes add/remove routines for profiles

* Sat Sep 30 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.1.0-5
- Use %%_isa in Requires for main package from devel

* Mon Sep 18 2017 Stephen Gallagher <sgallagh@redhat.com> - 0.1.0-4
- Correct the license to MIT

* Mon Sep 18 2017 Stephen Gallagher <sgallagh@redhat.com> - 0.1.0-3
- Modifications requested during package review

* Fri Sep 15 2017 Stephen Gallagher <sgallagh@redhat.com> - 0.1.0-2
- First public release

