# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# do not require a standalone uthash when built as part of RHEL
%bcond system_uthash %[0%{?fedora} || 0%{?epel}]

# build process has race conditions, force single thread
%global _smp_mflags -j1

%global srcname editorconfig-core-c

%global common_description %{expand:
EditorConfig makes it easy to maintain the correct coding style when
switching between different text editors and between different projects.
The EditorConfig project maintains a file format and plugins for various
text editors which allow this file format to be read and used by those
editors.}

Name:           editorconfig
Summary:        Parser for EditorConfig files written in C
Version:        0.12.10
Release: 2%{?dist}

# The entire source is BSD-2-Clause, except:
#   BSD-3-Clause: src/lib/ini.h
#                 src/lib/ini.c
#   BSD-1-Clause: src/lib/utarray.h
# Additionally, the following build-system files do not contribute to the
# licenses of the binary RPMs:
#   MIT: CMake_Modules/FindPCRE2.cmake
# The file src/lib/utarray.h is unbundled in %%prep, as part of the uthash
# header-only library; however, since packaging guidelines treat header-only
# libraries as a kind of static library, and the entire contents are still
# compiled into the binary RPMs, its license still contributes to the overall
# license of the binary RPMs.
License:        BSD-2-Clause AND BSD-3-Clause AND BSD-1-Clause
URL:            https://github.com/editorconfig/editorconfig-core-c
Source0:        %{url}/archive/v%{version}/%{srcname}-%{version}.tar.gz

# Downstream-only: Do not compile with -Werror
#
# This makes sense upstream, but is too strict for downstream packaging
# across various architectures, compiler versions, and so on.
Patch0:         0001-Downstream-only-Do-not-compile-with-Werror.patch

BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  gcc
BuildRequires:  pcre2-devel
%if %{with system_uthash}
# Header-only library; BR on -static required by guidelines
BuildRequires:  uthash-static
%endif

Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description %common_description


%package        libs
Summary:        Parser library for EditorConfig files (shared library)

# Files src/lib/ini.h and src/lib/ini.c are a forked copy of inih:
#   https://src.fedoraproject.org/rpms/inih
#   https://github.com/benhoyt/inih
# Since it has different hard-coded limits, among other changes from upstream,
# we expect that it will not be possible to unbundle it. Still, we have
# contacted upstream as required in
#   https://docs.fedoraproject.org/en-US/packaging-guidelines/#bundling
# via a GitHub issue:
#   Path to using a system copy of inih?
#   https://github.com/editorconfig/editorconfig-core-c/issues/91
# Upstream agreed that the bundled version has diverged too much.
#
# The files were added in commit 24cc68431848c6d53a877ff82a4ee4ce7ff67b7f on
# 2011-10-23; their contents at that time were an exact match for the
# then-latest commit in inih, 328c3d4f8ac3715fc7024af09372a479f028450f in
# today’s git repository. Since inih did not carry a version number, and the
# Google Code SVN hash at the time is lost to history, we use the git hash in
# the current repository to indicate the snapshot from which the bundled
# version was forked.
Provides:       bundled(inih) = 0^20110627git328c3d4
%if %{without system_uthash}
# src/lib/utarray.h:UTARRAY_VERSION
Provides:       bundled(uthash) = 2.3.0
%endif

%description    libs %common_description

This package contains the shared library.


%package        devel
Summary:        Parser library for EditorConfig files (development files)

Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       cmake

%description    devel %common_description

This package contains the files needed for development.


%prep
%autosetup -n %{srcname}-%{version} -p1
%if %{with system_uthash}
# Unbundle uthash
rm -vf src/lib/utarray.h
%endif


%build
%cmake
%cmake_build


%install
%cmake_install

# Remove static library
rm %{buildroot}/%{_libdir}/libeditorconfig_static.a


%files
%doc README.md
%license LICENSE

%{_bindir}/editorconfig
%{_bindir}/editorconfig-%{version}

%{_mandir}/man1/editorconfig.1*

%files libs
%doc README.md
%license LICENSE

%{_libdir}/libeditorconfig.so.0*

%{_mandir}/man3/editorconfig*
%{_mandir}/man5/editorconfig*

%files devel
%{_includedir}/editorconfig/

%{_libdir}/libeditorconfig.so
%{_libdir}/cmake/EditorConfig/
%{_libdir}/pkgconfig/editorconfig.pc


%changelog
* Thu Jan 22 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 0.12.10-1
- Update to 0.12.10 (close RHBZ#2401398)

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jul 13 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.12.9-1
- Update to 0.12.9 (close RHBZ#2292615)

* Thu Jun 13 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.12.8-1
- Update to 0.12.8 (close RHBZ#2292212)

* Wed Apr 03 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.12.7-1
- Update to 0.12.7 (close RHBZ#2272370)

* Fri Mar 08 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 0.12.6-5
- Use bundled uthash in RHEL builds

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Jan 22 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0.12.6-1
- Update to 0.12.6 (close RHBZ#2162811)
- Update License to SPDX
- Document and/or unbundle all bundled libraries

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 17 2021 Fabio Valentini <decathorpe@gmail.com> - 0.12.5-1
- Update to version 0.12.5.

* Thu Feb 04 2021 Fabio Valentini <decathorpe@gmail.com> - 0.12.4-3
- Force single-threaded build to work around race conditions.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Aug 31 2020 Fabio Valentini <decathorpe@gmail.com> - 0.12.4-1
- Update to version 0.12.4.

* Sat Aug 01 2020 Fabio Valentini <decathorpe@gmail.com> - 0.12.3-7
- Adapt to new cmake macros.

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.3-6
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Nov 16 2018 Fabio Valentini <decathorpe@gmail.com> - 0.12.3-1
- Update to version 0.12.3.

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu May 03 2018 Fabio Valentini <decathorpe@gmail.com> - 0.12.2-3
- Fix broken ldconfig_scriptlets use.

* Wed May 02 2018 Fabio Valentini <decathorpe@gmail.com> - 0.12.2-2
- Use single-job make for building.
- Added missing ldconfig scriptlets.
- Rewritten summaries.

* Thu Mar 22 2018 Fabio Valentini <decathorpe@gmail.com> - 0.12.2-1
- Initial package.

