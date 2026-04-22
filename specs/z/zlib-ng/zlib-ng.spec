## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 2;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond_without compat
%bcond_without sanitizers

# Be explicit about the soname in order to avoid unintentional changes.
# Before modifying any of the sonames, this must be announced to the Fedora
# community as it may break many other packages.
# A change proposal is needed:
# https://docs.fedoraproject.org/en-US/program_management/changes_policy/
%global soname libz-ng.so.2
%global compat_soname libz.so.1

# Compatible with the following zlib version.
%global zlib_ver 1.3.1
# Obsoletes zlib versions less than.
%global zlib_obsoletes 1.3

# ABI files for ix86 and s390x are not available upstream.
%global supported_abi_test aarch64 ppc64le x86_64

Name:		zlib-ng
Version:	2.3.3
Release:	%autorelease
Summary:	Zlib replacement with optimizations
License:	Zlib
Url:		https://github.com/zlib-ng/zlib-ng
Source0:	https://github.com/zlib-ng/zlib-ng/archive/%{version}/%{name}-%{version}.tar.gz

Patch:		far.diff

BuildRequires:	cmake >= 3.1
BuildRequires:	gcc-c++
BuildRequires:	cmake(GTest)
BuildRequires:	libabigail

%description
zlib-ng is a zlib replacement that provides optimizations for "next generation"
systems.

%package	devel
Summary:	Development files for %{name}
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description	devel
The %{name}-devel package contains libraries and header files for developing
application that use %{name}.

%if %{with compat}

%package	compat
Summary:	Zlib implementation provided by %{name}
Provides:	zlib = %{zlib_ver}
Provides:	zlib%{?_isa} = %{zlib_ver}
Conflicts:	zlib%{?_isa}
Obsoletes:	zlib < %{zlib_obsoletes}

%description	compat
zlib-ng is a zlib replacement that provides optimizations for "next generation"
systems.
The %{name}-compat package contains the library that is API and binary
compatible with zlib.

%package	compat-devel
Summary:	Development files for %{name}-compat
Requires:	%{name}-compat%{?_isa} = %{version}-%{release}
Provides:	zlib-devel = %{zlib_ver}
Provides:	zlib-devel%{?_isa} = %{zlib_ver}
Conflicts:	zlib-devel%{?_isa}
Obsoletes:	zlib-devel < %{zlib_obsoletes}

%description	compat-devel
The %{name}-compat-devel package contains libraries and header files for
developing application that use zlib.

%package	compat-static
Summary:	Static libraries for %{name}-compat
Requires:	%{name}-compat-devel%{?_isa} = %{version}-%{release}
Provides:	zlib-static = %{zlib_ver}
Provides:	zlib-static%{?_isa} = %{zlib_ver}
Conflicts:	zlib-static%{?_isa}
Obsoletes:	zlib-static < %{zlib_obsoletes}

%description	compat-static
The %{name}-compat-static package contains static libraries needed for
developing applications that use zlib.

%endif

%prep
%autosetup -p1 -n %{name}-%{version}

%build
cat <<_EOF_
###########################################################################
#
# Build the default zlib-ng library
#
###########################################################################
_EOF_

# zlib-ng uses a different macro for library directory.
%global cmake_param %{?with_sanitizers:-DWITH_SANITIZER=ON} -DWITH_RVV=OFF

%ifarch s390x
%global cmake_param %cmake_param -DWITH_DFLTCC_DEFLATE=ON -DWITH_DFLTCC_INFLATE=ON
%endif

# Setting __cmake_builddir is not necessary in this step, but do it anyway for symmetry.
%global __cmake_builddir %{_vpath_builddir}
%cmake %{cmake_param}
%cmake_build

%if %{with compat}
cat <<_EOF_
###########################################################################
#
# Build the compat mode library
#
###########################################################################
_EOF_

%global __cmake_builddir %{_vpath_builddir}-compat
# defining BUILD_SHARED_LIBS disables the static library
%undefine _cmake_shared_libs
# Disable new strategies in order to keep compatibility with zlib.
%cmake %{cmake_param} -DZLIB_COMPAT=ON -DWITH_NEW_STRATEGIES=OFF -DCMAKE_POSITION_INDEPENDENT_CODE=ON
%cmake_build
%endif

%check
cat <<_EOF_
###########################################################################
#
# Run the zlib-ng tests
#
###########################################################################
_EOF_

%global __cmake_builddir %{_vpath_builddir}
%ctest

%ifarch ppc64le
# Workaround Copr, that sets _target_cpu to ppc64le.
%global target_cpu powerpc64le
%else
%global target_cpu %{_target_cpu}
%endif

%ifarch x86_64
%global cpu_vendor pc
%else
%global cpu_vendor unknown
%endif

%ifarch %{supported_abi_test}
CHOST=%{target_cpu}-%{cpu_vendor}-linux-gnu sh test/abicheck.sh
%endif

%if %{with compat}
cat <<_EOF_
###########################################################################
#
# Run the compat mode tests
#
###########################################################################
_EOF_

%global __cmake_builddir %{_vpath_builddir}-compat
%ctest
%ifarch %{supported_abi_test}
CHOST=%{target_cpu}-%{cpu_vendor}-linux-gnu sh test/abicheck.sh --zlib-compat
%endif
%endif


%install
%global __cmake_builddir %{_vpath_builddir}
%cmake_install

%if %{with compat}
%global __cmake_builddir %{_vpath_builddir}-compat
%cmake_install
%endif

%files
%license LICENSE.md
%doc README.md
%{_libdir}/libz-ng.so.%{version}
%{_libdir}/%{soname}

%files devel
%{_includedir}/zconf-ng.h
%{_includedir}/zlib-ng.h
%{_includedir}/zlib_name_mangling-ng.h
%{_libdir}/libz-ng.so
%{_libdir}/pkgconfig/%{name}.pc
%dir %{_libdir}/cmake/zlib-ng/
%{_libdir}/cmake/zlib-ng/*

%if %{with compat}

%files compat
%{_libdir}/%{compat_soname}
%{_libdir}/libz.so.%{zlib_ver}.zlib-ng

%files compat-devel
%{_includedir}/zconf.h
%{_includedir}/zlib.h
%{_includedir}/zlib_name_mangling.h
%{_libdir}/libz.so
%{_libdir}/pkgconfig/zlib.pc
%dir %{_libdir}/cmake/ZLIB/
%{_libdir}/cmake/ZLIB/*

%files compat-static
%{_libdir}/libz.a


%endif


%changelog
## START: Generated by rpmautospec
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 2.3.3-2
- Latest state for zlib-ng

* Wed Feb 04 2026 Packit <hello@packit.dev> - 2.3.3-1
- Update to 2.3.3 upstream release
- Resolves: rhbz#2436620

* Mon Dec 15 2025 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 2.3.2-2
- Enable DFLTCC on s390x

* Wed Dec 03 2025 Packit <hello@packit.dev> - 2.3.2-1
- Update to 2.3.2 upstream release
- Resolves: rhbz#2418517

* Thu Aug 07 2025 Packit <hello@packit.dev> - 2.2.5-1
- Update to 2.2.5 upstream release
- Resolves: rhbz#2387088

* Thu Feb 27 2025 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 2.2.4-3
- Remove rpmdeplint from gating

* Tue Feb 25 2025 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 2.2.4-2
- Enable -fPIC for static compat libraries

* Mon Feb 10 2025 Packit <hello@packit.dev> - 2.2.4-1
- Update to 2.2.4 upstream release
- Resolves: rhbz#2344792

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jan 08 2025 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 2.2.3-1
- Update to version 2.2.3

* Wed Sep 25 2024 Lukas Javorsky <ljavorsk@redhat.com> - 2.2.2-1
- Rebase to new major version 2.2.2

* Tue Sep 10 2024 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 2.1.7-3
- Fixes rhbz#2307237

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 19 2024 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 2.1.7-1
- Update to zlib-ng 2.1.7
- Fix rhbz#2293101
- Fix rhbz#2293437

* Tue Jun 04 2024 Cristian Le <fedora@lecris.me> - 2.1.6-6
- Avoid using reserved variable vendor. Fix #2284608

* Wed May 29 2024 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 2.1.6-5
- Set ownership of cmake directories. Fix #2283789

* Tue May 21 2024 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 2.1.6-4
- Update the patch that fixes rhbz#2280347

* Tue May 14 2024 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 2.1.6-3
- Fix rhbz#2280347

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 11 2024 Lukas Javorsky <ljavorsk@redhat.com> - 2.1.6-1
- Rebase to version 2.1.6

* Tue Jan 09 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 2.1.5-2
- Add zlib-ng-compat-static to replace zlib-static

* Wed Dec 20 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 2.1.5-1
- Update to zlib-ng 2.1.5

* Wed Oct 18 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 2.1.3-7
- Improve the patch that defines the FAR macro

* Wed Sep 27 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 2.1.3-6
- Add a patch that defines the FAR macro

* Wed Sep 20 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 2.1.3-5
- Fix WITH_SANITIZER

* Tue Sep 19 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 2.1.3-4
- Disable WITH_NEW_STRATEGIES in compat mode

* Thu Aug 24 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 2.1.3-3
- Enable zlib compat build

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Ali Erdinc Koroglu <aekoroglu@fedoraproject.org> - 2.1.3-1
- Update to 2.1.3

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Apr 14 2022 Ali Erdinc Koroglu <aekoroglu@fedoraproject.org> - 2.0.6-1
- New upstream release 2.0.6

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.5-2.20210625gitc69f78bc5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Aug 07 2021 Tulio Magno Quites Machado Filho <tuliom@ascii.art.br> - 2.0.2-5.20210625gitc69f78bc5e
- Update to v2.0.5.

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-2.20210323git5fe25907e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun Apr 18 2021 Tulio Magno Quites Machado Filho <tuliom@ascii.art.br> - 2.0.2-1.20210323gite5fe25907e
- Update to v2.0.2.
- Remove the manpage that got removed from upstream.

* Thu Jan 28 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.9-0.4.20200912gite58738845
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sun Sep 13 2020 Tulio Magno Quites Machado Filho <tuliom@ascii.art.br> - 1.9.9-0.3.20200912gite58738845
- Update to a newer commit.

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.9-0.3.20200609gitfe69810c2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul 09 2020 Tulio Magno Quites Machado Filho <tuliom@ascii.art.br> - 1.9.9-0.2.20200609gitfe69810c2
- Replace cmake commands with new cmake macros

* Mon Jul 06 2020 Tulio Magno Quites Machado Filho <tuliom@ascii.art.br> - 1.9.9-0.1.20200609gitfe69810c2
- Improve the archive name.
- Starte release at 0.1 as required for prerelease.
- Make the devel package require an arch-dependent runtime subpackage.
- Remove %%ldconfig_scriptlets.
- Glob the man page extension.
- Move unversioned shared library to the devel subpackage

* Wed Jul 01 2020 Tulio Magno Quites Machado Filho <tuliom@ascii.art.br> - 1.9.9-0.20200609gitfe69810c2
- Initial commit

## END: Generated by rpmautospec
