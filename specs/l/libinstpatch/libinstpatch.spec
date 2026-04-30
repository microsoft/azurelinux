## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 3;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# https://github.com/swami/libinstpatch/issues/34
#
# Since this has never worked, we do not have %%files entries for the result.
%bcond introspection 0

Name:           libinstpatch
Version:        1.1.7
%global api_version 1.0
%global so_version 2
Release:        %autorelease
Summary:        Instrument file software library

URL:            http://www.swamiproject.org/
# The entire source is LGPL-2.1-only, except:
# • The following are LicenseRef-Fedora-Public-Domain:
#     - libinstpatch/md5.{c,h}
#         The algorithm is due to Ron Rivest.  This code was
#         written by Colin Plumb in 1993, no copyright is claimed.
#         This code is in the public domain; do with it what you wish.
#     - examples/create_sf2.c
#         Use this example as you please (public domain)
#     - examples/split_sfont.c
#         Public domain use as you please
#   Texts were added to public-domain-text.txt in fedora-license-data:
#   https://gitlab.com/fedora/legal/fedora-license-data/-/merge_requests/228
License:        LGPL-2.1-only AND LicenseRef-Fedora-Public-Domain
# Additionally, the following unused files are removed in %%prep:
# • The following are GPL-2.0-only:
#     - utils/ipatch_convert.c
#
# …and the following files are used only for build-time testing and do not
# contribute to the licenses of the binary RPMs:
# • The following are LicenseRef-Fedora-Public-Domain:
#     - tests/*.py
#         License: Public Domain
SourceLicense:  %{license} AND GPL-2.0-only

%global forgeurl https://github.com/swami/libinstpatch
Source:         %{forgeurl}/archive/v%{version}/libinstpatch-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  ninja-build

BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gthread-2.0)
BuildRequires:  pkgconfig(sndfile)
# GTKDOC_ENABLED
BuildRequires:  pkgconfig(gtk-doc)
%if %{with introspection}
# INTROSPECTION_ENABLED
BuildRequires:  pkgconfig(gobject-introspection-1.0)
%endif

# This is a forked copy:
# Changed so as no longer to depend on Colin Plumb's `usual.h' header
# definitions; now uses stuff from dpkg's config.h.
#  - Ian Jackson <ijackson@nyx.cs.du.edu>.
# Josh Coalson: made some changes to integrate with libFLAC.
# Josh Green: made some changes to integrate with libInstPatch.
Provides:       bundled(md5-plumb)

%description
libInstPatch stands for lib-Instrument-Patch and is a library for processing
digital sample based MIDI instrument “patch” files. The types of files
libInstPatch supports are used for creating instrument sounds for wavetable
synthesis. libInstPatch provides an object framework (based on GObject) to load
patch files into, which can then be edited, converted, compressed and saved.


%package devel
Summary:        Development files for libinstpatch
# The entire source is LGPL-2.1-only, except:
# • The following are LicenseRef-Fedora-Public-Domain:
#     - libinstpatch/md5.{c,h}
#     - examples/create_sf2.c
#     - examples/split_sfont.c
# See the comment above the License field for the base package for full
# details.
# None of the LicenseRef-Fedora-Public-Domain files are included in this
# subpackage.
License:        LGPL-2.1-only

Requires:       libinstpatch%{?_isa} = %{version}-%{release}
Requires:       glib2-devel%{?_isa}
Requires:       libsndfile-devel%{?_isa}

%description devel
The libinstpatch-devel package contains libraries and header files for
developing applications that use libinstpatch.


%package doc
Summary:        Documentation and examples for libinstpatch
BuildArch:      noarch
# The entire source is LGPL-2.1-only, except:
# • The following are LicenseRef-Fedora-Public-Domain:
#     - libinstpatch/md5.{c,h}
#     - examples/create_sf2.c
#     - examples/split_sfont.c
# See the comment above the License field for the base package for full
# details.
#
# The examples are included in this subpackage. The License is implicitly the
# same as the base package.

%description doc
The libinstpatch-doc package contains documentation and examples for
libinstpatch.


%prep
%autosetup -p1

# Remove example for nonexistent Python bindings
find examples -type f -name '*.py' -print -delete


%conf
%cmake \
    -DGTKDOC_ENABLED:BOOL=ON \
    -DINTROSPECTION_ENABLED:BOOL=\
%{?with_introspection:ON}%{!?with_introspection:OFF} \
    -GNinja


%build
%cmake_build


%install
%cmake_install


# Upstream provides no tests.


%files
%license COPYING
%{_libdir}/libinstpatch-%{api_version}.so.%{so_version}{,.*}


%files devel
%{_includedir}/libinstpatch-%{so_version}/
%{_libdir}/libinstpatch-%{api_version}.so
%{_libdir}/pkgconfig/libinstpatch-%{api_version}.pc


%files doc
%license COPYING
%doc ABOUT-NLS
%doc AUTHORS
%doc ChangeLog
%doc README.md
%doc TODO.tasks
%doc examples/
# gtkdoc
%doc %{_vpath_builddir}/docs/reference/html/


%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 1.1.7-3
- test: add initial lock files

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue May 20 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1.1.7-1
- Update to 1.1.7

* Tue May 20 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1.1.6-36
- Update .rpmlintrc file for current rpmlint

* Tue Apr 29 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1.1.6-35
- Update .rpmlintrc file for current rpmlint

* Wed Mar 05 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1.1.6-34
- Patch for CMake 4.0

* Fri Jan 31 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1.1.6-33
- Fix the gtkdoc build more elegantly

* Thu Jan 16 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1.1.6-32
- Fix compilation with GCC 15 / C23

* Fri Dec 13 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 1.1.6-31
- Add a SourceLicense field

* Fri Nov 01 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 1.1.6-30
- Invoke %%cmake in %%conf rather than in %%build

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu May 30 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 1.1.6-27
- Use a more reliable workaround for gtkdoc dependency bug

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Jun 18 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.1.6-21
- Use new (rpm 4.17.1+) bcond style

* Mon May 29 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.1.6-20
- Safer enforcement of serial build
- Override _smp_ncpus_max instead of _smp_build_ncpus

* Fri May 26 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.1.6-19
- Set _smp_build_ncpus instead of using %%constrain_build
- Works around RHBZ#2210347

* Mon Apr 10 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.1.6-17
- Note that public-domain texts were added to license data (close
  RHBZ#2177295)

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 18 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.1.6-15
- Fix warning from libinstpatch-scan.c (gtkdoc)

* Wed Dec 21 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.1.6-14
- Use constrain_build instead of setting _smp_build_ncpus

* Tue Dec 20 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.1.6-13
- Indicate dirs. in files list with trailing slashes

* Tue Dec 20 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.1.6-12
- Trivially simplify one files list

* Tue Oct 18 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.1.6-11
- Drop EPEL7 conditionals

* Tue Oct 18 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.1.6-10
- Enable gtkdoc documentation; build a -doc subpackage

* Tue Oct 18 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.1.6-9
- Update License to SPDX

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Aug 02 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.1.6-6
- Clean up gtkdoc build conditional

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jul 09 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.1.6-3
- Switch License field to “effective license” of LGPLv2

* Mon May 17 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.1.6-2
- Add EPEL7 compatibility

* Fri Apr 16 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.1.6-1
- New upstream version 1.1.6 with so-version bump from 0 to 2 and altered
  include path
- Upstream tarball now comes from GitHub
- Build with ninja backend instead of make

* Fri Apr 16 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.0.0-24.20110806svn386
- Adjust whitespace and ordering to personal preference
- Drop obsolete ldconfig scriptlets
- Use much stricter file globs
- Change library BR’s to pkgconfig() format
- Use autosetup macro
- Correct License field from “LGPLv2+” to “LGPLv2 and GPLv2 and Public Domain”
- Add virtual Provides for bundled MD5 implementation
- Properly install license file
- Add ABOUT-NLS and TODO.tasks to doc files

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-23.20110806svn386
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Aug 03 2020 Erich Eickmeyer <erich@ericheickmeyer.com> - 1.0.0-22.20110806svn386
- Fix for new cmake macros
- Resolves: #1864003

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-21.20110806svn386
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-20.20110806svn386
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-19.20110806svn386
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-18.20110806svn386
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-17.20110806svn386
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-16.20110806svn386
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-15.20110806svn386
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-14.20110806svn386
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-13.20110806svn386
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-12.20110806svn386
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-11.20110806svn386
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-10.20110806svn386
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-9.20110806svn386
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-8.20110806svn386
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-7.20110806svn386
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-6.20110806svn386
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-5.20110806svn386
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-4.20110806svn386
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Aug 07 2011 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.0.0-3.20110806svn386
- Include the COPYING file. oops.
- Fix main package Requires of the devel package

* Sat Aug 06 2011 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.0.0-2.20110806svn386
- Update to svn after upstream accepted our build patches, switched to cmake and fixed the licensing
- Prepare for submission for review

* Wed Oct 27 2010 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.0.0-1
- Update to 1.0.0

* Thu Mar 26 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.0.0-0.1.297svn
- Initial Fedora build

## END: Generated by rpmautospec
