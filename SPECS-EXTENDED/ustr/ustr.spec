
%define show_all_cmds       1
%define broken_fed_dbg_opts 0
%define multilib_inst       1

%if %{show_all_cmds}
%define policy_cflags_hide HIDE=
%else
%define policy_cflags_hide %{nil}
%endif

%if %{broken_fed_dbg_opts}
# Variable name explains itself.
%define policy_cflags_broken DBG_ONLY_BAD_POLICIES_HAVE_THIS_EMPTY_CFLAGS=
%else
%define policy_cflags_broken %{nil}
%endif

%define policy_cflags %{policy_cflags_hide}  %{policy_cflags_broken}

%if %{multilib_inst}
%define ustr_make_install install-multilib-linux
%else
%define ustr_make_install install
%endif


Name: ustr
Version: 1.0.4
Release: 31%{?dist}
Summary: String library, very low memory overhead, simple to import
License: MIT or LGPLv2+ or BSD
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL: https://www.and.org/ustr/
Source0: https://www.and.org/ustr/%{version}/%{name}-%{version}.tar.bz2
Patch0: c99-inline.patch
# BuildRequires: make gcc sed

BuildRequires:  gcc
%description
 Micro string library, very low overhead from plain strdup() (Ave. 44% for
0-20B strings). Very easy to use in existing C code. At it's simplest you can
just include a single header file into your .c and start using it.
 This package also distributes pre-built shared libraries.

%package devel
Summary: Development files for %{name}
# This isn't required, but Fedora policy makes it so
Requires: pkgconfig >= 0.14
Requires: %{name} = %{version}-%{release}

%description devel
 Header files for the Ustr string library, and the .so to link with.
 Also includes a %{name}.pc file for pkg-config usage.
 Includes the ustr-import tool, for if you jsut want to include
the code in your projects ... you don't have to link to the shared lib.

%package static
Summary: Static development files for %{name}
Requires: %{name}-devel = %{version}-%{release}

%description static
 Static library for the Ustr string library.

%package debug
Summary: Development files for %{name}, with debugging options turned on
# This isn't required, but Fedora policy makes it so
Requires: pkgconfig >= 0.14
Requires: %{name}-devel = %{version}-%{release}

%description debug
 Header files and dynamic libraries for a debug build of the Ustr string
library.
 Also includes a %{name}-debug.pc file for pkg-config usage.

%package debug-static
Summary: Static development files for %{name}, with debugging options turned on
Requires: %{name}-debug = %{version}-%{release}

%description debug-static
 Static library for the debug build of the Ustr string library.

%prep
%setup -q
%patch 0 -p1

%build
make %{?_smp_mflags} all-shared CFLAGS="${CFLAGS:-%optflags}  -fgnu89-inline" \
  LDFLAGS="$RPM_LD_FLAGS" %{policy_cflags}

%check
%if %{?chk}%{!?chk:1}
make %{?_smp_mflags} check CFLAGS="${CFLAGS:-%optflags}  -fgnu89-inline"
  LDFLAGS="$RPM_LD_FLAGS" %{policy_cflags}
%endif

%install
rm -rf $RPM_BUILD_ROOT
make $@ %{ustr_make_install} prefix=%{_prefix} \
                bindir=%{_bindir}         mandir=%{_mandir} \
                datadir=%{_datadir}       libdir=%{_libdir} \
                includedir=%{_includedir} libexecdir=%{_libexecdir} \
                DOCSHRDIR=%{_datadir}/doc/ustr-devel \
                DESTDIR=$RPM_BUILD_ROOT LDCONFIG=/bin/true HIDE=

%ldconfig_scriptlets

%ldconfig_scriptlets debug

%files
%{_libdir}/libustr-1.0.so.*
%{!?_licensedir:%global license %%doc}
%license LICENSE*
%doc ChangeLog README NEWS

%files devel
%{_datadir}/ustr-%{version}
%{_bindir}/ustr-import
%if %{multilib_inst}
%{_libexecdir}/ustr-%{version}
%endif
%{_includedir}/ustr.h
%{_includedir}/ustr-*.h
%exclude %{_includedir}/ustr*debug*.h
%{_libdir}/pkgconfig/ustr.pc
%{_libdir}/libustr.so
%{_datadir}/doc/ustr-devel
%{_mandir}/man1/*
%{_mandir}/man3/*

%files static
%{_libdir}/libustr.a

%files debug
%{_libdir}/libustr-debug-1.0.so.*
%{_libdir}/libustr-debug.so
%{_includedir}/ustr*debug*.h
%{_libdir}/pkgconfig/ustr-debug.pc

%files debug-static
%{_libdir}/libustr-debug.a


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.4-31
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 23 2018 Florian Weimer <fweimer@redhat.com> - 1.0.4-26
- Use LDFLAGS from redhat-rpm-config

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Oct 30 2015 James Antill <james@fedoraproject.org> - 1.0.4-20
- Move doc/ustr-devel-<version> to doc/ustr-devel. BZ 993940.
- Use -fgnu89-inline workaround for gcc5.

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug  6 2014 Tom Callaway <spot@fedoraproject.org> - 1.0.4-17
- fix license handling

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Aug 11 2009 Ville Skyttä <ville.skytta@iki.fi> - 1.0.4-10
- Use bzipped upstream tarball.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jun 13 2008 James Antill <james@fedoraproject.org> - 1.0.4-7
- Fix c99 inline problems, newer GCC

* Sun Mar  9 2008 James Antill <james@fedoraproject.org> - 1.0.4-6
- Fix dir. ownership bug.
- Resolves: rhbz#436711

* Wed Mar  5 2008 James Antill <james@fedoraproject.org> - 1.0.4-5
- New new upstream: 1.0.4

* Thu Feb 21 2008 Dennis Gilmore <dennis@ausil.us> - 1.0.3-5
- set broken_fed_dbg_opts to 0 its the recomended option upstream
- this works around sparc GCC problems
- add smpflags and cflags to make check

* Wed Feb 13 2008 James Antill <james@fedoraproject.org> - 1.0.3-4
- Preserve timestamps for shared multilib. files.
- Relates: bug#343351

* Sun Feb 10 2008 James Antill <james@fedoraproject.org> - 1.0.3-3
- Add upstream multilib patch for ustr-import
- Resolves: bug#343351

* Mon Jan 14 2008 James Antill <james@fedoraproject.org> - 1.0.3-2
- Build new upstream in Fedora

* Tue Oct 30 2007 James Antill <james@and.org> - 1.0.2-2
- Build new upstream in Fedora

* Mon Oct 29 2007 James Antill <james@and.org> - 1.0.2-1
- New release

* Tue Aug 28 2007 James Antill <jantill@redhat.com> - 1.0.1-6
- Add options for fedora policy brokeness, so it's easy to undo.
- Rebuild for buildid.

* Wed Aug  8 2007 James Antill <james@and.org> - 1.0.1-5
- Import fix for ustr-import, wrt. repl <=> replace

* Sun Aug  5 2007 James Antill <james@and.org> - 1.0.1-4
- Patches for minor GIT HEAD documentation fixes.
- Install mkdir_p and fgrep examples.

* Sat Aug  4 2007 James Antill <james@and.org> - 1.0.1-2
- First upload to Fedora repos.

* Fri Aug  3 2007 James Antill <james@and.org> - 1.0.1-0.10.fc7
- Re-fix dups in -devel and -debug file lists.
- Change license to new format

* Thu Aug  2 2007 James Antill <james@and.org> - 1.0.1-0.9.fc7
- Fix dups in -devel and -debug file lists.

* Wed Aug  1 2007 James Antill <james@and.org> - 1.0.1-0.8.fc7
- Required to make DBG_ONLY_BAD_POLICIES_HAVE_THIS_EMPTY_CFLAGS empty
- due to so called "review"

* Fri Jul 27 2007 James Antill <james@and.org> - 1.0.1-0.2.fc7
- Next test release of 1.0.1, lots of fixes from Fedora review.

* Wed Jul 25 2007 James Antill <james@and.org> - 1.0.1-0
- Test release of 1.0.1.

* Wed Jul 11 2007 James Antill <james@and.org> - 1.0.0-1
- Upgrade to 1.0.0
- Minor fixes on specfile

* Sun Jun  3 2007 James Antill <james@and.org> - 0.99.2-1
- Upgrade to 0.99.2

* Thu May 24 2007 James Antill <james@and.org> - 0.99.1-2
- Fix ver typo to be version.

* Fri May 18 2007 James Antill <james@and.org> - 0.99.1-1
- Use all-shared to get GCC-ish specific shared libs.

* Mon May 14 2007 James Antill <james@and.org> - 0.98.1-0
- Initial spec

