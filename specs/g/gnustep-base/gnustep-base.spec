## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 8;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# License
# ===========
#
# The GNUstep libraries and library resources are covered under the GNU
# Lesser Public License.  This means you can use these libraries in any
# program (even non-free programs).

# GNUstep tools, test programs, and other files are covered under the
# GNU Public License.

Name: gnustep-base
Version: 1.31.0
Release: %autorelease
License: GPL-3.0-or-later AND LGPL-2.0-or-later
Summary: GNUstep Base library package
URL:     https://www.gnustep.org/
Source0: https://ftp.gnustep.org/pub/gnustep/core/%{name}-%{version}.tar.gz

# https://bugzilla.redhat.com/show_bug.cgi?id=1179297
Patch0: %{name}-use_system-wide_crypto-policies.patch

Patch1: %{name}-fix_GCC15.patch

Patch2: %{name}-fix_ending_tag_mismatch.patch

Patch3: %{name}-1.31.0-fix_s390x.patch

BuildRequires: gcc
BuildRequires: gcc-objc
BuildRequires: libffi-devel >= 3.0.9
BuildRequires: gnutls-devel
BuildRequires: libxml2-devel
BuildRequires: libxslt-devel
BuildRequires: pkgconfig
BuildRequires: gnustep-make >= 2.9.2
BuildRequires: avahi-compat-libdns_sd-devel
BuildRequires: gmp-devel
BuildRequires: texi2html texinfo-tex
BuildRequires: libicu-devel
BuildRequires: libcurl-devel
BuildRequires: texi2html

Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: make

Conflicts: libFoundation

%description
The GNUstep Base Library is a powerful fast library of general-purpose,
non-graphical Objective C classes, inspired by the superb OpenStep API but
implementing Apple and GNU additions to the API as well.  It includes for
example classes for unicode strings, arrays, dictionaries, sets, byte
streams, typed coders, invocations, notifications, notification dispatchers,
scanners, tasks, files, networking, threading, remote object messaging
support (distributed objects), event loops, loadable bundles, attributed
unicode strings, xml, mime, user defaults. This package includes development
headers too.


%package libs
Summary: GNUStep Base Libraries
Requires: gnustep-make%{?_isa} >= 2.9.2

%description libs
The GNUstep Base Library is a powerful fast library of general-purpose,
non-graphical Objective C classes, inspired by the superb OpenStep API but
implementing Apple and GNU additions to the API as well.  It includes for
example classes for unicode strings, arrays, dictionaries, sets, byte
streams, typed coders, invocations, notifications, notification dispatchers,
scanners, tasks, files, networking, threading, remote object messaging
support (distributed objects), event loops, loadable bundles, attributed
unicode strings, xml, mime, user defaults. This package includes development
headers too.
This packages contains the run-time libraries for %{name}.


%package devel
Summary: Header of the GNUstep Base library packes
Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description devel
This package contains the header files of the gnustep-base package.


%package doc
Summary: Documentation for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: gnustep-filesystem

%description doc
The GNUstep Base Library is a powerful fast library of general-purpose,
non-graphical Objective C classes, inspired by the superb OpenStep API but
implementing Apple and GNU additions to the API as well.  It includes for
example classes for unicode strings, arrays, dictionaries, sets, byte
streams, typed coders, invocations, notifications, notification dispatchers,
scanners, tasks, files, networking, threading, remote object messaging
support (distributed objects), event loops, loadable bundles, attributed
unicode strings, xml, mime, user defaults. This package includes development
headers too.
This package contains the documentation for %{name}

%prep
%autosetup -N

%patch -P 0 -p1 -b .backup
%patch -P 1 -p1 -b .backup
%patch -P 2 -p1 -b .backup
%ifarch s390x
%patch -P 3 -p1 -b .backup
%endif

iconv -f iso-8859-1 -t utf-8 ChangeLog.2 -o ChangeLog.2.utf8
mv ChangeLog.2.utf8 ChangeLog.2

%build
ffi_include=$(pkg-config --cflags-only-I libffi | sed -e 's/^\-\I//')
export LDFLAGS="%{__global_ldflags}"
%gnustep_configure --disable-ffcall --with-ffi-include="$ffi_include"

%gnustep_make -n

%install
%gnustep_install -n

# Rename pl to pllist to fix naming conflict
mv ${RPM_BUILD_ROOT}%{_bindir}/pl ${RPM_BUILD_ROOT}%{_bindir}/pllist

rm -f Examples/.cvsignore
rm -f Examples/.gdbinit

# We need a modified GNUstep.conf, because the DTDs are install not
# on there real destination

sed -e "s|GNUSTEP_SYSTEM_LIBRARY=|GNUSTEP_SYSTEM_LIBRARY=$RPM_BUILD_ROOT|" \
    -e "s|GNUSTEP_SYSTEM_HEADERS=|GNUSTEP_SYSTEM_HEADERS=$RPM_BUILD_ROOT|" \
    %{_sysconfdir}/GNUstep/GNUstep.conf >GNUstep.conf

export LD_LIBRARY_PATH=$RPM_BUILD_ROOT%{_libdir}
export GNUSTEP_CONFIG_FILE=$(pwd)/GNUstep.conf

%gnustep_makedoc
%gnustep_installdoc

%files
%{_bindir}/HTMLLinker
%{_bindir}/autogsdoc
%{_bindir}/cvtenc
%{_bindir}/classes
%{_bindir}/defaults
%{_bindir}/gdnc
%{_bindir}/gdomap
%{_bindir}/gspath
%{_bindir}/make_strings
%{_bindir}/pl2link
%{_bindir}/pldes
%{_bindir}/plget
%{_bindir}/pllist
%{_bindir}/plmerge
%{_bindir}/plparse
%{_bindir}/plser
%{_bindir}/plutil
%{_bindir}/sfparse
%{_bindir}/xmlparse
%{_mandir}/man1/*
%{_mandir}/man8/*
%{gnustep_dtddir}/

%files libs
%doc ANNOUNCE ChangeLog* NEWS README*
%license COPYING.LIB COPYINGv3
%{gnustep_libraries}/
%{_libdir}/libgnustep-base.so.1.31
%{_libdir}/libgnustep-base.so.%{version}
%dir %{_libdir}/GNUstep/Tools
%dir %{_libdir}/GNUstep/Tools/Resources
%dir %{_libdir}/GNUstep/Tools/Resources/autogsdoc
%{_libdir}/GNUstep/Tools/Resources/autogsdoc/default-styles.css

%files devel
%{_includedir}/Foundation/
%{_includedir}/CoreFoundation/
%{_includedir}/GNUstepBase/
%{_libdir}/libgnustep-base.so
%{_libdir}/pkgconfig/gnustep-base.pc
%{gnustep_additional}/base.make
%doc Examples

%files doc
%{_infodir}/*
%dir %{_datadir}/GNUstep/Documentation
%{_datadir}/GNUstep/Documentation/*

%changelog
## START: Generated by rpmautospec
* Mon Apr 06 2026 azldev <> - 1.31.0-8
- Latest state for gnustep-base

* Wed Aug 06 2025 František Zatloukal <fzatlouk@redhat.com> - 1.31.0-7
- Rebuilt for icu 77.1

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.31.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Feb 23 2025 Antonio Trande <sagitter@fedoraproject.org> - 1.31.0-5
- Re-enable default linker flags

* Sun Feb 23 2025 Antonio Trande <sagitter@fedoraproject.org> - 1.31.0-4
- Fix s390x build

* Sat Feb 15 2025 Antonio Trande <sagitter@fedoraproject.org> - 1.31.0-3
- Fix License tag

* Sat Feb 15 2025 Antonio Trande <sagitter@fedoraproject.org> - 1.31.0-2
- Fix shared library

* Sat Feb 15 2025 Antonio Trande <sagitter@fedoraproject.org> - 1.31.0-1
- Release 1.31.0

* Fri Jan 24 2025 Antonio Trande <sagitter@fedoraproject.org> - 1.30.0-8
- Patched for adding -std flags

* Sat Jan 18 2025 Antonio Trande <sagitter@fedoraproject.org> - 1.30.0-7
- Fix GCC15 builds

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.30.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Dec 08 2024 Pete Walter <pwalter@fedoraproject.org> - 1.30.0-5
- Rebuild for ICU 76

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.30.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jun 20 2024 Antonio Trande <sagitter@fedoraproject.org> - 1.30.0-3
- Fix gnustep-make name

* Wed Jun 19 2024 Antonio Trande <sagitter@fedoraproject.org> - 1.30.0-2
- gnustep-base-libs now requires gnustep-make (rhbz#2283758)

* Fri Jun 14 2024 Antonio Trande <sagitter@fedoraproject.org> - 1.30.0-1
- Release 1.30.0

* Wed Jan 31 2024 Pete Walter <pwalter@fedoraproject.org> - 1.29.0-7
- Rebuild for ICU 74

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.29.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.29.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Nov 19 2023 Antonio Trande <sagitter@fedoraproject.org> - 1.29.0-4
- Release 1.29.0 | Explicit version of installed library

* Sun Nov 19 2023 Antonio Trande <sagitter@fedoraproject.org> - 1.29.0-3
- Release 1.29.0 | Remove README file in doc sub-package

* Sun Nov 19 2023 Antonio Trande <sagitter@fedoraproject.org> - 1.29.0-2
- Release 1.29.0 | Fix README files

* Sun Nov 19 2023 Antonio Trande <sagitter@fedoraproject.org> - 1.29.0-1
- Release 1.29.0

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.28.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 František Zatloukal <fzatlouk@redhat.com> - 1.28.0-12
- Rebuilt for ICU 73.2

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.28.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Dec 31 2022 Pete Walter <pwalter@fedoraproject.org> - 1.28.0-10
- Rebuild for ICU 72

* Wed Nov 23 2022 Florian Weimer <fweimer@redhat.com> - 1.28.0-9
- Avoid C89-only constructs during the config stage

* Mon Aug 01 2022 František Zatloukal <fzatlouk@redhat.com> - 1.28.0-8
- Rebuilt for ICU 71.1

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.28.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.28.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Jan 08 2022 Miro Hrončok <miro@hroncok.cz> - 1.28.0-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/LIBFFI34

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.28.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu May 20 2021 Pete Walter <pwalter@fedoraproject.org> - 1.28.0-3
- Rebuild for ICU 69

* Sat May 15 2021 Antonio Trande <sagitter@fedoraproject.org> - 1.28.0-2
- Add new tool

* Sat May 15 2021 Antonio Trande <sagitter@fedoraproject.org> - 1.28.0-1
- Release 1.28.0

* Sat Apr 03 2021 Antonio <sagitter@localhost.localdomain> - 1.27.0-6
- Rebuild for gnustep-make (RHBZ #1923589)

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.27.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.27.0-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.27.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 15 2020 Pete Walter <pwalter@fedoraproject.org> - 1.27.0-2
- Rebuild for ICU 67

* Thu Apr 16 2020 sagitter <sagitter@fedoraproject.org> - 1.27.0-1
- Release 1.27.0

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov 01 2019 Pete Walter <pwalter@fedoraproject.org> - 1.26.0-2
- Rebuild for ICU 65

* Wed Sep 04 2019 sagitter <sagitter@fedoraproject.org> - 1.26.0-1
- Release 1.26.0

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.25.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Mar 07 2019 Tim Landscheidt <tim@tim-landscheidt.de> - 1.25.0-17
- Remove obsolete requirements for %%post/%%preun scriptlets

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.25.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 28 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.25.0-15
- Remove obsolete Group tag

* Sun Jan 27 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.25.0-14
- Remove obsolete scriptlets

* Wed Jan 23 2019 Pete Walter <pwalter@fedoraproject.org> - 1.25.0-13
- Rebuild for ICU 63

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.25.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Pete Walter <pwalter@fedoraproject.org> - 1.25.0-11
- Rebuild for ICU 62

* Mon Apr 30 2018 Pete Walter <pwalter@fedoraproject.org> - 1.25.0-10
- Rebuild for ICU 61.1

* Fri Feb 16 2018 sagitter <sagitter@fedoraproject.org> - 1.25.0-9
- Make arched the -doc sub-package

* Fri Feb 16 2018 sagitter <sagitter@fedoraproject.org> - 1.25.0-8
- Use %%%%ldconfig_scriptlets

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.25.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Nov 30 2017 Pete Walter <pwalter@fedoraproject.org> - 1.25.0-6
- Rebuild for ICU 60.1

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.25.0-5
- Rebuilt for
  https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.25.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Apr 19 2017 sagitter <sagitter@fedoraproject.org> - 1.25.0-3
- Fix Requires

* Sat Apr 15 2017 sagitter <sagitter@fedoraproject.org> - 1.25.0-2
- Remove unknown directory

* Sat Apr 15 2017 sagitter <sagitter@fedoraproject.org> - 1.25.0-1
- Update to 1.25.0

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.24.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Aug 21 2016 sagitter <sagitter@fedoraproject.org> - 1.24.9-1
- Update to 1.24.9

* Fri Apr 15 2016 David Tardon <dtardon@redhat.com> - 1.24.7-8
- rebuild for ICU 57.1

* Wed Feb 03 2016 Dennis Gilmore <dennis@ausil.us> - 1.24.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Oct 28 2015 David Tardon <dtardon@redhat.com> - 1.24.7-6
- rebuild for ICU 56.1

* Wed Jun 17 2015 Dennis Gilmore <dennis@ausil.us> - 1.24.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jan 26 2015 David Tardon <dtardon@redhat.com> - 1.24.7-4
- rebuild for ICU 54.1

* Wed Oct 22 2014 Jochen Schmitt <Jochen@herr-schmitt.de> - 1.24.7-3
- Add texi2html as a BR

* Sun Oct 19 2014 Jochen Schmitt <Jochen@herr-schmitt.de> - 1.24.7-2
- RPMAUTOSPEC: unresolvable merge
## END: Generated by rpmautospec
