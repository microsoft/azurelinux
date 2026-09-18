# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond_with jar
%bcond_with java
# Disabled lto flags on i686 to avoid lto memory allocation error
%ifarch i686
%global _lto_cflags %{nil}
%endif

Summary: GNU tools and libraries for localized translated messages
Name: gettext
Version: 0.25.1
Release: 2%{?dist}

# The following are licensed under LGPLv2+:
# - libintl and its headers
# - libasprintf and its headers
# - libintl.jar
# - GNU.Gettext.dll
# - gettext.sh
# The following are licensed under GFDL:
# - gettext-tools/doc/FAQ.html
# - gettext-tools/doc/tutorial.html
# - gettext info files
# - libasprintf info files
# - libtextstyle info files
# Everything else is GPLv3+
License: GPL-3.0-or-later and LGPL-2.0-or-later and GFDL-1.2-or-later
URL: https://www.gnu.org/software/gettext/
Source: https://ftp.gnu.org/pub/gnu/%{name}/%{name}-%{version}.tar.gz
Source2: msghack.py
Source3: msghack.1

Patch1: gettext-0.21.1-covscan.patch
# for bootstrapping
# BuildRequires: autoconf >= 2.62
BuildRequires: automake
BuildRequires: libtool
# BuildRequires: bison

BuildRequires: gcc-c++
%if %{with java}
# libintl.jar requires gcj >= 4.3 to build
BuildRequires: gcc-java, libgcj
# For javadoc
BuildRequires: java-1.6.0-openjdk-devel
%if %{with jar}
BuildRequires: %{_bindir}/fastjar
# require zip and unzip for brp-java-repack-jars
BuildRequires: zip, unzip
%endif
%endif
# for po-mode.el
BuildRequires: emacs
# ensure 'ARCHIVE_FORMAT=dirxz'
BuildRequires: xz
# for documentation
BuildRequires: teckit
BuildRequires: texlive-dvips
BuildRequires: texlive-dvipdfmx
BuildRequires: texinfo-tex
BuildRequires: texlive-xetex
# following suggested by DEPENDENCIES:
BuildRequires: ncurses-devel
BuildRequires: libxml2-devel
BuildRequires: glib2-devel
BuildRequires: libacl-devel
BuildRequires: libunistring-devel
# for the tests
BuildRequires: glibc-langpack-de
BuildRequires: glibc-langpack-en
BuildRequires: glibc-langpack-fa
BuildRequires: glibc-langpack-fr
BuildRequires: glibc-langpack-ja
BuildRequires: glibc-langpack-tr
BuildRequires: glibc-langpack-zh
BuildRequires: make
Provides: bundled(gnulib)
Requires: %{name}-runtime = %{version}-%{release}
Requires: libtextstyle%{?_isa} = %{version}-%{release}

%description
The GNU gettext package provides a set of tools and documentation for
producing multi-lingual messages in programs. Tools include a set of
conventions about how programs should be written to support message
catalogs, a directory and file naming organization for the message
catalogs, a runtime library which supports the retrieval of translated
messages, and stand-alone programs for handling the translatable and
the already translated strings. Gettext provides an easy to use
library and tools for creating, using, and modifying natural language
catalogs and is a powerful and simple method for internationalizing
programs.


%package runtime
Summary: GNU runtime libraries and programs for producing multi-lingual messages
License: GPL-3.0-or-later and LGPL-2.0-or-later
# Depend on the exact version of the library sub package
Requires: %{name}-libs%{_isa} = %{version}-%{release}
Requires: %{name}-envsubst = %{version}-%{release}
Conflicts: %{name} <= 0.21-15%{?dist}.0.20220203


%description runtime
The GNU gettext-runtime package provides an easy to use runtime libraries and
programs for creating, using, and modifying natural language catalogs
and is a powerful and simple method for internationalizing programs.


%package common-devel
Summary: Common development files for %{name}
# autopoint archive
License: GPL-3.0-or-later
BuildArch: noarch

%description common-devel
This package contains common architecture independent gettext development files.


%package devel
Summary: Development files for %{name}
# autopoint is GPLv3+
# libasprintf is LGPLv2+
# libgettextpo is GPLv3+
License: LGPL-2.0-or-later and GPL-3.0-or-later and GFDL-1.2-or-later
Requires: %{name} = %{version}-%{release}
Requires: %{name}-libs = %{version}-%{release}
Requires: %{name}-common-devel = %{version}-%{release}
Requires: xz
Requires: diffutils
Obsoletes: gettext-autopoint < 0.18.1.1-3
Provides: gettext-autopoint = %{version}-%{release}

%description devel
This package contains all development related files necessary for
developing or compiling applications/libraries that needs
internationalization capability. You also need this package if you
want to add gettext support for your project.


%package libs
Summary: Libraries for %{name}
# libasprintf is LGPLv2+
# libgettextpo is GPLv3+
License: LGPL-2.0-or-later and GPL-3.0-or-later
Requires: libtextstyle%{?_isa} = %{version}-%{release}

%description libs
This package contains libraries used internationalization support.

%package -n libtextstyle
Summary: Text styling library
License: GPL-3.0-or-later

%description -n libtextstyle
Library for producing styled text to be displayed in a terminal
emulator.

%package -n libtextstyle-devel
Summary: Development files for libtextstyle
License: GPL-3.0-or-later and GFDL-1.2-or-later
Requires: libtextstyle%{?_isa} = %{version}-%{release}

%description -n libtextstyle-devel
This package contains all development related files necessary for
developing or compiling applications/libraries that needs text
styling.

%package -n emacs-%{name}
Summary: Support for editing po files within GNU Emacs
BuildArch: noarch
# help users find po-mode.el
Provides: emacs-po-mode
Requires: emacs(bin) >= %{_emacs_version}
Provides: emacs-%{name}-el = %{version}-%{release}
Obsoletes: emacs-%{name}-el < %{version}-%{release}

%description -n emacs-%{name}
This package provides a major mode for editing po files within GNU Emacs.

%package -n msghack
Summary: Alter PO files in ways
BuildArch: noarch

%description -n msghack
This program can be used to alter .po files in ways no sane mind would
think about.


%package envsubst
Summary: Substitutes the values of environment variables
Conflicts: %{name} <= 0.21-15%{?dist}.0.20220203

%description envsubst
Substitutes the values of environment variables.


%prep
%setup -q
%patch 1 -p1 -b .orig~
autoreconf

# Defeat libtextstyle attempt to bundle libxml2.  The comments
# indicate this is done because the libtextstyle authors do not want
# applications using their code to suffer startup delays due to the
# relocations.  This is not a sufficient reason for Fedora.
sed -e 's/\(gl_cv_libxml_force_included=\)yes/\1no/' \
    -i libtextstyle/configure


%build
%if %{with java}
export JAVAC=gcj
%if %{with jar}
export JAR=fastjar
%endif
%endif
%ifarch ppc ppc64 ppc64le
# prevent test-isinf from failing with gcc-5.3.1 on ppc64le (#1294016)
export CFLAGS="$RPM_OPT_FLAGS -D__SUPPORT_SNAN__"
%endif
# Fedora's libxml2-devel package has an extra "libxml2" path component.
export CPPFLAGS="-I%{_includedir}/libxml2"
# Side effect of unbundling libxml2 from libtextstyle.
export LIBS="-lxml2"
export CFLAGS="$CFLAGS -Wformat"
%configure --enable-nls --disable-static \
    --enable-shared --disable-csharp --disable-rpath \
%if %{with java}
    --enable-java \
%else
    --disable-java --disable-native-java \
%endif
    --with-xz

# Eliminate hardcoded rpaths; workaround libtool reordering -Wl,--as-needed
# after all the libraries.
sed -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
    -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
    -e 's|CC=.g..|& -Wl,--as-needed|' \
    -i $(find . -name libtool)

%make_build %{?with_java:GCJFLAGS="-findirect-dispatch"}


%install
%make_install \
    lispdir=%{_datadir}/emacs/site-lisp/gettext \
    aclocaldir=%{_datadir}/aclocal EXAMPLESFILES=""


install -pm 755 %SOURCE2 ${RPM_BUILD_ROOT}%{_bindir}/msghack
install -pm 644 %SOURCE3 ${RPM_BUILD_ROOT}%{_mandir}/man1/msghack.1

# make preloadable_libintl.so executable
chmod 755 ${RPM_BUILD_ROOT}%{_libdir}/preloadable_libintl.so

rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir

# doc relocations
for i in gettext-runtime/man/*.html; do
  rm ${RPM_BUILD_ROOT}%{_datadir}/doc/gettext/`basename $i`
done
rm -r ${RPM_BUILD_ROOT}%{_datadir}/doc/gettext/javadoc*

rm -rf ${RPM_BUILD_ROOT}%{_datadir}/doc/gettext/examples

rm -rf htmldoc
mkdir htmldoc
mv ${RPM_BUILD_ROOT}%{_datadir}/doc/gettext/* ${RPM_BUILD_ROOT}%{_datadir}/doc/libasprintf/* htmldoc
rm -r ${RPM_BUILD_ROOT}%{_datadir}/doc/libasprintf
rm -r ${RPM_BUILD_ROOT}%{_datadir}/doc/gettext

## note libintl.jar does not build with gcj < 4.3
## since it would not be fully portable
%if %{with jar}
### this is no longer needed since examples not packaged
## set timestamp of examples ChangeLog timestamp for brp-java-repack-jars
#for i in `find ${RPM_BUILD_ROOT} examples -newer ChangeLog -type f -name ChangeLog`; do
#  touch -r ChangeLog  $i
#done
%else
# in case another java compiler is installed
rm -f ${RPM_BUILD_ROOT}%{_datadir}/%{name}/libintl.jar
%endif

rm -f ${RPM_BUILD_ROOT}%{_datadir}/%{name}/gettext.jar

# own this directory for third-party *.its files
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}/its

# remove .la files
rm ${RPM_BUILD_ROOT}%{_libdir}/lib*.la

# remove internal .so lib files
rm ${RPM_BUILD_ROOT}%{_libdir}/libgettext{src,lib}.so

# move po-mode initialization elisp file to the right place, and remove byte
# compiled file
install -d ${RPM_BUILD_ROOT}%{_emacs_sitestartdir}
mv ${RPM_BUILD_ROOT}%{_emacs_sitelispdir}/%{name}/start-po.el ${RPM_BUILD_ROOT}%{_emacs_sitestartdir}
rm ${RPM_BUILD_ROOT}%{_emacs_sitelispdir}/%{name}/start-po.elc

%find_lang %{name}-runtime
%find_lang %{name}-tools


%check
# this takes quite a lot of time to run

# adapt to rpath removal
export LD_LIBRARY_PATH=$RPM_BUILD_ROOT%{_libdir}:$PWD/gettext-runtime/intl/.libs

# override LIBUNISTRING to prevent reordering of lib objects
make check LIBUNISTRING=-lunistring

%ldconfig_scriptlets libs

%files -f %{name}-tools.lang
%doc AUTHORS NEWS README THANKS
%doc gettext-tools/misc/disclaim-translations.txt
%doc gettext-tools/man/msg*.1.html
%doc gettext-tools/man/recode*.1.html
%doc gettext-tools/man/xgettext.1.html
%doc gettext-tools/doc/FAQ.html
%doc gettext-tools/doc/tutorial.html
%{_bindir}/msgattrib
%{_bindir}/msgcat
%{_bindir}/msgcmp
%{_bindir}/msgcomm
%{_bindir}/msgconv
%{_bindir}/msgen
%{_bindir}/msgexec
%{_bindir}/msgfilter
%{_bindir}/msgfmt
%{_bindir}/msggrep
%{_bindir}/msginit
%{_bindir}/msgmerge
%{_bindir}/msgunfmt
%{_bindir}/msguniq
%{_bindir}/recode-sr-latin
%{_bindir}/xgettext
%{_infodir}/gettext*
%exclude %{_mandir}/man1/autopoint.1*
%exclude %{_mandir}/man1/envsubst.1*
%exclude %{_mandir}/man1/gettextize.1*
%exclude %{_mandir}/man1/msghack.1*
%{_mandir}/man1/msg*
%{_mandir}/man1/recode*.1*
%{_mandir}/man1/xgettext.1*
%{_libdir}/%{name}
%if %{with java}
%exclude %{_libdir}/%{name}/gnu.gettext.*
%endif
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/its
%{_datadir}/%{name}/ABOUT-NLS
%{_datadir}/%{name}/po
%{_datadir}/%{name}/styles
%{_datadir}/%{name}/disclaim-translations.txt
%dir %{_datadir}/%{name}-%{version}
%{_datadir}/%{name}-%{version}/its
%dir %{_datadir}/%{name}/schema
%{_datadir}/%{name}/schema/its*.xsd*
%{_datadir}/%{name}/schema/locating-rules.xsd*
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/cldr-plurals
%{_libexecdir}/%{name}/hostname
%{_libexecdir}/%{name}/project-id
%{_libexecdir}/%{name}/urlget
%{_libexecdir}/%{name}/user-email

%files runtime -f %{name}-runtime.lang
%license COPYING
%doc gettext-runtime/BUGS
%doc gettext-runtime/man/gettext.1.html
%doc gettext-runtime/man/ngettext.1.html
%doc gettext-runtime/intl/COPYING*
%{_bindir}/gettext
%{_bindir}/gettext.sh
%{_bindir}/ngettext
%exclude %{_mandir}/man1/autopoint.1*
%exclude %{_mandir}/man1/envsubst.1*
%exclude %{_mandir}/man1/gettextize.1*
%exclude %{_mandir}/man1/msg*
%exclude %{_mandir}/man1/recode-sr-latin.1*
%exclude %{_mandir}/man1/xgettext.1*
%{_mandir}/man1/*

%files envsubst
%license COPYING
%doc gettext-runtime/man/envsubst.1.html
%{_bindir}/envsubst
%{_mandir}/man1/envsubst.1*

%files common-devel
%{_datadir}/%{name}/archive.*.tar.xz

%files devel
%doc gettext-runtime/man/*.3.html ChangeLog
%doc gettext-tools/man/autopoint.1.html
%doc gettext-tools/man/gettextize.1.html
%{_bindir}/autopoint
%{_bindir}/gettextize
%{_datadir}/%{name}/projects/
%{_datadir}/%{name}/config.rpath
%{_datadir}/%{name}/*.h
%{_datadir}/%{name}/msgunfmt.tcl
%{_datadir}/%{name}/m4/*
%{_datadir}/aclocal/nls.m4
%{_includedir}/autosprintf.h
%{_includedir}/gettext-po.h
%{_infodir}/autosprintf*
%{_libdir}/libasprintf.so
%{_libdir}/libgettextpo.so
%{_libdir}/preloadable_libintl.so
%{_mandir}/man1/autopoint.1*
%{_mandir}/man1/gettextize.1*
%{_mandir}/man3/*
%{_datadir}/%{name}/javaversion.class
%doc gettext-runtime/intl-java/javadoc*
%if %{with java}
%{_libdir}/%{name}/gnu.gettext.*
%endif

%files libs
%{_libdir}/libasprintf.so.0*
%{_libdir}/libgettextpo.so.0*
%{_libdir}/libgettextlib-0.*.so
%{_libdir}/libgettextsrc-0.*.so
%if %{with jar}
%{_datadir}/%{name}/libintl.jar
%endif

%files -n libtextstyle
%{_libdir}/libtextstyle.so.0*

%files -n libtextstyle-devel
%{_docdir}/libtextstyle/
%{_includedir}/textstyle/
%{_includedir}/textstyle.h
%{_infodir}/libtextstyle*
%{_libdir}/libtextstyle.so

%files -n emacs-%{name}
%dir %{_emacs_sitelispdir}/%{name}
%{_emacs_sitelispdir}/%{name}/*.elc
%{_emacs_sitelispdir}/%{name}/*.el
%{_emacs_sitestartdir}/*.el

%files -n msghack
%license COPYING
%{_bindir}/msghack
%{_mandir}/man1/msghack.1*

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.25.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul 23 2025 Manish Tiwari <matiwari@redhat.com> - 0.25.1-1
- update to 0.25.1 release
- Bug fixes:
- autopoint no longer fails if configure.ac contains no AM_GNU_GETTEXT_VERSION or AM_GNU_GETTEXT_REQUIRE_VERSION invocation.
- nls.m4 is installed again under $PREFIX/share/aclocal/.

* Mon May 12 2025 Manish Tiwari <matiwari@redhat.com> - 0.25-1
- update to 0.25 release
- https://savannah.gnu.org/news/?id=10769

* Thu Feb 27 2025 Manish Tiwari <matiwari@redhat.com> - 0.24-1
- update to 0.24 release
- https://savannah.gnu.org/news/?id=10730

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.23.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jan 1 2025 Manish Tiwari <matiwari@redhat.com> - 0.23.1-1
- update to 0.23.1 release
- Remove gettext-0.23-libxml2 patch

* Wed Dec 11 2024 Manish Tiwari <matiwari@redhat.com> - 0.23-1
- update to 0.23 release
- https://savannah.gnu.org/news/?id=10699
- Add patch to fix compilation error with libxml2 >= 2.12.0 and gcc >= 14.
- Remove gettext-0.22-disable-libtextstyle patch

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.22.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jul 11 2024 Manish Tiwari <matiwari@redhat.com> - 0.22.5-5
- CI gating tests migration to tmt

* Thu Jul 4 2024 Manish Tiwari <matiwari@redhat.com> - 0.22.5-4
- Add explicit package version requirement for libtextstyle

* Tue Jul 2 2024 Manish Tiwari <matiwari@redhat.com> - 0.22.5-3
- Add back libtextstyle for f40 (#2278984)

* Fri Mar  8 2024 Jens Petersen <petersen@redhat.com> - 0.22.5-2
- condition libtextstyle obsoletes

* Mon Mar 4 2024 Manish Tiwari <matiwari@redhat.com> - 0.22.5-1
- update to 0.22.5 release
- https://savannah.gnu.org/news/?id=10597

* Wed Feb 21 2024 Manish Tiwari <matiwari@redhat.com> - 0.22.4-2
- Add back libtextstyle library for rawhide (#2264128)

* Fri Feb 9 2024 Manish Tiwari <matiwari@redhat.com> - 0.22.4-1
- update to 0.22.4 release
- https://savannah.gnu.org/news/?id=10544

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.22-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jun 23 2023 Jens Petersen <petersen@redhat.com> - 0.22-1
- update to 0.22 release
- https://savannah.gnu.org/news/?id=10378

* Wed Mar 29 2023 Sundeep Anand <suanand@redhat.com> - 0.21.1-3
- update license tag to as per SPDX identifiers

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.21.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Oct 14 2022 Sundeep Anand <suanand@redhat.com> - 0.21.1-1
- update to 0.21.1 release

* Thu Oct 13 2022 Sundeep Anand <suanand@redhat.com> - 0.21-20.0.20220203
- Include doc and man pages for envsubst subpackage.
  Move _libdir and _datadir from gettext-runtime to gettext package.

* Mon Sep 12 2022 Sundeep Anand <suanand@redhat.com> - 0.21-19.0.20220203
- Add conflicts to enable new (sub)packages installable independently of the original package.

* Wed Aug 10 2022 Honza Horak <hhorak@redhat.com> - 0.21-18.0.20220203
- Introduce envsubst sub-package for allow install envsubst with minimal
  footprint

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.21-17.0.20220203
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 8 2022 Sundeep Anand <suanand@redhat.com> - 0.21-16.0.20220203
- separate out gettext-runtime from the main package into a subpackage

* Tue Jun 7 2022 Sundeep Anand <suanand@redhat.com> - 0.21-15.0.20220203
- add Provides: gettext-runtime to gettext package for forward compatibility.
- and removed Provides: gettext-tools

* Mon Jun 6 2022 Sundeep Anand <suanand@redhat.com> - 0.21-14.0.20220203
- add Provides: gettext-tools to gettext package for forward compatibility.

* Thu Mar 31 2022 Jens Petersen <petersen@redhat.com> - 0.21-13.0.20220203
- add Java 17 support patch from Mamoru Tasaka (#2062407)

* Wed Mar 9 2022 Sundeep Anand <suanand@redhat.com> - 0.21-12.0.20220203
- fix gettext snapshot versioning issue to make it canonical (#2061646)

* Thu Mar 3 2022 Sundeep Anand <suanand@redhat.com> - 0.21-11.0.20220203
- Rebuild with gettext-snapshot-20220228 to fix ppc64le and tests (#2045414)
  Removed gettext-0.21-gnulib-perror-tests.patch as it is upstreamed.

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.21-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Nov 23 2021 Jens Petersen <petersen@redhat.com> - 0.21-9
- update autotools files with autoreconf to fix FTBFS (#2000426)

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.21-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue May 25 2021 Florian Weimer <fweimer@redhat.com> - 0.21-7
- Rebuild with new binutils to fix ppc64le corruption (#1960730)

* Tue May 11 2021 Sundeep Anand <suanand@redhat.com> - 0.21-6
- Add gettext-0.21-covscan.patch to fix issues detected by static analyzers

* Fri Apr 30 2021 Sundeep Anand <suanand@redhat.com> - 0.21-5
- Add gettext-0.21-disable-libtextstyle.patch
  Do not build libtextstyle, as it depends on libcroco
  which is now unmaintained and has known security bugs.
  Obsolete libtextstyle and libtextstyle-devel packages.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.21-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Sep  7 2020 Sundeep Anand <suanand@redhat.com> - 0.21-3
- include patch to fix gnulib perror tests (rhbz#1867021)

* Thu Aug  6 2020 Jens Petersen <petersen@redhat.com> - 0.21-2
- reenable testsuite except for armv7hl which is failing

* Mon Aug 03 2020 Sundeep Anand <suanand@redhat.com> - 0.21-1
- gettext-0.21 is available (rhbz#1860728)

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.20.2-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Michael Catanzaro <mcatanzaro@redhat.com> - 0.20.2-3
- Bundle libcroco so we can remove the system package

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.20.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Apr 14 2020 Sundeep Anand <suanand@redhat.com> - 0.20.2-1
- gettext-0.20.2 is available (rhbz#1823721)

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.20.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 06 2020 Sundeep Anand <suanand@redhat.com> - 0.20.1-3
- Add diffutils dependency on gettext-devel (rhbz#1774899)

* Tue Aug 20 2019 Daiki Ueno <dueno@redhat.com> - 0.20.1-2
- Fix misbehavior of msgmerge --for-msgfmt

* Fri Aug  9 2019 Jerry James <loganjerry@gmail.com> - 0.20.1-1
- update to 0.20.1 release, all patches upstreamed
- add GFDL to License fields due to info files
- add libtextstyle{,-devel} subpackages
- reenable testsuite
- build with libacl support
- BR various glibc langpacks wanted by the tests
- drop ancient Conflicts due to UsrMove
- prevent rpaths rather than removing them
- explicitly list binaries in the main package to avoid extra build-ids

* Fri Aug  9 2019 Jens Petersen <petersen@redhat.com> - 0.19.8.1-22
- temporarily disable testsuite (#1735245)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.8.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Mar  7 2019 Tim Landscheidt <tim@tim-landscheidt.de> - 0.19.8.1-20
- Remove obsolete requirements for %%post/%%preun scriptlets

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.8.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Nov 08 2018 Pavel Raiskup <praiskup@redhat.com> - 0.19.8.1-18
- fix CVE-2018-18751 (rhbz#1647044)
- put gettextize man page into gettext-devel (man page scan, rhbz#1611303)

* Tue Jul 31 2018 Florian Weimer <fweimer@redhat.com> - 0.19.8.1-17
- Rebuild with fixed binutils

* Sat Jul 28 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.19.8.1-16
- Replace obsolete scriptlets

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.8.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.8.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.19.8.1-13
- Switch to %%ldconfig_scriptlets

* Fri Jan 05 2018 Pavel Raiskup <praiskup@redhat.com> - 0.19.8.1-12
- xgettext --its segfault fix (rhbz#1531476)

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.8.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.8.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Mar 15 2017 Kalev Lember <klember@redhat.com> - 0.19.8.1-9
- Depend on the exact version of the library sub package

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.8.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 26 2017 Pavel Raiskup <praiskup@redhat.com> - 0.19.8.1-7
- really remove Requires: git from gettext-devel (rhbz#1161284)
- make the BuildRequires unconditional (rhbz#1416691)

* Wed Dec 21 2016 Pavel Raiskup <praiskup@redhat.com> - 0.19.8.1-6
- disable test-lock for 'gettext-tool' subdir too (rhbz#1406031)

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.19.8.1-5
- Rebuild for Python 3.6

* Fri Dec 16 2016 Petr Šabata <contyk@redhat.com> - 0.19.8.1-4
- Subpackage msghack so that gettext doesn't depend on python
- name the new sub-package 'msghack'

* Tue Nov 29 2016 Pavel Raiskup <praiskup@redhat.com> - 0.19.8.1-3
- devel subpackage to Require 'xz' (rhbz#1399270)

* Wed Aug 10 2016 Daiki Ueno <dueno@redhat.com> - 0.19.8.1-2
- utilize %%autosetup
- apply patch to fix po-send-mail when used with Emacs 25 (#1356642)

* Sat Jun 11 2016 Daiki Ueno <dueno@redhat.com> - 0.19.8.1-1
- update to 0.19.8.1 release

* Thu Jun  9 2016 Daiki Ueno <dueno@redhat.com> - 0.19.8-1
- update to 0.19.8 release

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 12 2016 Daiki Ueno <dueno@redhat.com> - 0.19.7-3
- own .../gettext/its for third-party *.its files
- add a work around for test-isinf failure on ppc64le (#1297387)

* Fri Jan  8 2016 Daiki Ueno <dueno@redhat.com> - 0.19.7-2
- apply patch to recognize .glade extension for GtkBuilder files (#1296653)

* Thu Dec 10 2015 Daiki Ueno <dueno@redhat.com> - 0.19.7-1
- update to 0.19.7 release

* Thu Sep 24 2015 Daiki Ueno <dueno@redhat.com> - 0.19.6-1
- update to 0.19.6 release

* Wed Jul 22 2015 Daiki Ueno <dueno@redhat.com> - 0.19.5.1-2
- work around version conflict between gettextize and autopoint

* Thu Jul 16 2015 Daiki Ueno <dueno@redhat.com> - 0.19.5.1-1
- update to 0.19.5.1 release

* Fri Jun 26 2015 Daiki Ueno <dueno@redhat.com> - 0.19.4-7
- drop -el subpackage (#1234583)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.19.4-5
- Rebuilt for GCC 5 C++11 ABI change

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 0.19.4-4
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Thu Feb 19 2015 Daiki Ueno <dueno@redhat.com> - 0.19.4-3
- port msghack.py to Python 3 (#1192086)

* Wed Dec 31 2014 Daiki Ueno <dueno@redhat.com> - 0.19.4-2
- remove git dependency from -devel subpackage (#1161284)

* Fri Dec 26 2014 Daiki Ueno <dueno@redhat.com> - 0.19.4-1
- update to 0.19.4 release

* Tue Oct 28 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.19.3-2
- Disable the test_lock test as it often hangs on a number of arches

* Thu Oct 16 2014 Daiki Ueno <dueno@redhat.com> - 0.19.3-1
- update to 0.19.3 release
- remove patches included in 0.19.3
- remove autoconf/automake/libtool/bison from BR, as we don't do bootstrap

* Wed Oct 15 2014 Daiki Ueno <dueno@redhat.com> - 0.19.2-5
- apply patch to fix infloop in autopoint (Closes: #1151238)
- apply patch to support newer ncurses in F-22

* Fri Oct  3 2014 Daiki Ueno <dueno@redhat.com> - 0.19.2-4
- apply patch to fix C octal character escape handling (Closes: #1147535)

* Tue Sep 02 2014 Dennis Gilmore <dennis@ausil.us> - 0.19.2-3
- rebuild for libunistring soname bump

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jul 14 2014 Daiki Ueno <dueno@redhat.com> - 0.19.2-1
- update to 0.19.2 release

* Mon Jul  7 2014 Daiki Ueno <dueno@redhat.com> - 0.19.1-2
- apply patch to msghack.py, for Python 3 compatibility (Closes: #1113425,
  thanks to Bohuslav "Slavek" Kabrda)

* Tue Jun 10 2014 Daiki Ueno <dueno@redhat.com> - 0.19.1-1
- update to 0.19.1 release
- switch to xz-compressed archive

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jun  2 2014 Daiki Ueno <dueno@redhat.com> - 0.19-2
- apply patch to workaround msgfmt bug that counts warnings as errors

* Mon Jun  2 2014 Daiki Ueno <dueno@redhat.com> - 0.19-1
- update to 0.19 release
- remove upstreamed -Wformat-security patch

* Tue Jan  7 2014 Daiki Ueno <dueno@redhat.com> - 0.18.3.2-1
- update to 0.18.3.2 release
- apply patch to suppress -Wformat-security warnings in gnulib-tests

* Sun Aug 25 2013 Daiki Ueno <dueno@redhat.com> - 0.18.3.1-1
- update to 0.18.3.1 release

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 10 2013 Daiki Ueno <dueno@redhat.com> - 0.18.3-1
- update to 0.18.3 release

* Wed Jun 26 2013 Daiki Ueno <dueno@redhat.com> - 0.18.2.1-2
- add a man page for msghack
- fix bogus date in %%changelog

* Tue Mar 12 2013 Daiki Ueno <dueno@redhat.com> - 0.18.2.1-1
- update to 0.18.2.1 release (not really necessary though)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Dec 26 2012 Daiki Ueno <dueno@redhat.com> - 0.18.2-1
- update to 0.18.2 release (based on the spec patch by Jens Petersen)

* Tue Oct  2 2012 Jens Petersen <petersen@redhat.com> - 0.18.1.1-17
- move gettextize to the devel subpackage with its source data files
- update msghack to GPL v3

* Fri Jul 27 2012 Jens Petersen <petersen@redhat.com> - 0.18.1.1-16
- patch gnulib since glibc and C11 dropped gets

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18.1.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 29 2012 Remi Collet <remi@fedoraproject.org> - 0.18.1.1-14
- add upstream patch from debian to fix xgettext segfault in
  remember_a_message_plural (#826138)

* Thu May 17 2012 Jens Petersen <petersen@redhat.com> - 0.18.1.1-13
- base package now provides bundled(gnulib) to make it clear that
  gettext is built with bundled gnulib (#821757)

* Wed Jan 25 2012 Harald Hoyer <harald@redhat.com> 0.18.1.1-12
- add filesystem guard

* Wed Jan 25 2012 Harald Hoyer <harald@redhat.com> 0.18.1.1-11
- install everything in /usr
  https://fedoraproject.org/wiki/Features/UsrMove

* Tue Jan 10 2012 Nils Philippsen <nils@redhat.com> - 0.18.1.1-10
- rebuild for gcc 4.7

* Tue Oct  4 2011 Jens Petersen <petersen@redhat.com> - 0.18.1.1-9
- correct the configure --with-pic option syntax (Gilles Espinasse)

* Wed Sep 28 2011 Jens Petersen <petersen@redhat.com> - 0.18.1.1-8
- add gettext-readlink-einval.patch to fix build on kernel >= 2.6.39 (#739188)
- add optional buildrequires suggested in the DEPENDENCIES file

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18.1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb  7 2011 Jens Petersen <petersen@redhat.com> - 0.18.1.1-6
- remove internal libgettextlib.so and libgettextsrc.so (#650471)

* Mon Feb  7 2011 Jens Petersen <petersen@redhat.com> - 0.18.1.1-5
- fix license field of gettext-libs since libgettextpo is GPLv3+ (#640158)

* Thu Sep  9 2010 Jens Petersen <petersen@redhat.com> - 0.18.1.1-4
- subpackage archive.git.tar.gz to avoid multilib conflicts (#631733)
- update msghack.py header

* Mon Aug 23 2010 Jens Petersen <petersen@redhat.com> - 0.18.1.1-3
- merge autopoint subpackage into devel to simplify deps (#625325)
- have ABOUT-NLS only in the base package datadir

* Wed Jun 23 2010 Jens Petersen <petersen@redhat.com> - 0.18.1.1-2
- correct license tag from GPLv3 to GPLv3+
- subpackage autopoint which requires git (#574031)
- no longer require cvs (#606746)
- add bcond for git

* Fri May 21 2010 Jens Petersen <petersen@redhat.com> - 0.18.1.1-1
- update to 0.18.1.1 release (#591044)
- gettext-0.17-autopoint-CVS-441481.patch, gettext-0.17-long-long-int-m4.patch
  gettext-0.17-open-args.patch, and
  gettext-xgettext-python-unicode-surrogate-473946.patch are upstream
- move libintl.jar to lib subpackage to avoid multilib problems
  (reported by Jim Radford in #595922)
- disable java for now
- use chrpath to get us out of rpath hell instead of complicated libtool hacks
- enable git support

* Fri Apr 23 2010 Jens Petersen <petersen@redhat.com> - 0.17-17
- create emacs subpackages for po-mode.el (thanks for patch from
  Jonathan Underwood, #579452)
- provide emacs-po-mode
- move libgettextlib and libgettextsrc from base to libs subpackage
  (requested by Peter Robinson for blender, #579388)

* Fri Nov 27 2009 Jens Petersen <petersen@redhat.com> - 0.17-16
- fix FTBFS by removing openmp.m4 which conflicts with recent autoconf (#539211)
- cleanup gettext-0.17-rpathFix.patch
  - separate gl_AC_TYPE_LONG_LONG replacement to another patch
  - use trailing ':' for tests LD_LIBRARY_PATH
- run autogen.sh with --quick and --skip-gnulib

* Tue Sep  1 2009 Jens Petersen <petersen@redhat.com> - 0.17-15
- bring back autopoint requires cvs (#517361)
- requires info rather than /sbin/install-info
- drop install_info and remove_install_info macros

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 24 2009 Jens Petersen <petersen@redhat.com> - 0.17-13
- buildrequire automake (#507275)
- run autogen

* Mon Jun 22 2009 Jens Petersen <petersen@redhat.com> - 0.17-12
- move intl/ and po/ to base package for gettextize
  (reported by Serge Pavlovsky, #496902)

* Fri May 22 2009 Jens Petersen <petersen@redhat.com> - 0.17-11
- use bcond's for build switches

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 12 2009 Jens Petersen <petersen@redhat.com> - 0.17-9
- add buildjava switch to allow turning off the java bits completely
- add buildcheck to allow turning off make check
- drop cvs requires for autopoint (Karl Lattimer, #469555)
- add upstream gettext-xgettext-python-unicode-surrogate-473946.patch by
  Bruno Haible to fix xgettext handling of utf16 surrogates in python (#473946)

* Fri Aug 29 2008 Ding-Yi Chen <dchen at redhat dot com> - 0.17-8
- Fix the build failure with koji.

* Fri Aug 29 2008 Ding-Yi Chen <dchen at redhat dot com> - 0.17-7
- Remove the gettext-libs docs, as they are talking about autoconf, libtool,
  which are not directly related to the gettext-libs.
- Remove unused definition and trailing space.
- Fix the build failure with mock .

* Tue Aug 19 2008 Ding-Yi Chen <dchen at redhat dot com> - 0.17-6
- Fixed Bug 456666 msghack doesn't check for mandatory cmd line params
  by adding checking statements and display usage (msghack.py modified)
- rpath patch for binary-or-shlib-defines-rpath in x86_64.

* Thu Apr 24 2008 Jens Petersen <petersen@redhat.com> - 0.17-5
- fix autopoint messing up CVS files with upstream patch (#441481)

* Mon Feb 18 2008 Jens Petersen <petersen@redhat.com> - 0.17-4
- if %%buildjar is off make sure libintl.jar does not get installed (#433210)

* Mon Feb 18 2008 Jens Petersen <petersen@redhat.com> - 0.17-3
- turn on building of libintl.jar now that we have gcc43

* Thu Feb 14 2008 Jens Petersen <petersen@redhat.com> - 0.17-2
- rebuild with gcc43

* Thu Jan 24 2008 Jens Petersen <petersen@redhat.com> - 0.17-1
- update to 0.17 release
  - update License field to GPLv3
  - add gettext-0.17-open-args.patch to fix build from upstream
  - gettext-tools-tests-lang-gawk-fail.patch, gettext-php-headers.patch,
    gettext-php-prinf-output-237241.patch, and
    gettext-xglade-define-xml-major-version-285701.patch are no longer needed
- drop superfluous po-mode-init.el source
- no need to run autoconf and autoheader when building
- pass -findirect-dispatch to gcj to make java binaries ABI independent
  (jakub,#427796)
- move autopoint, gettextize, and {_datadir}/{name}/ to main package
- force removal of emacs/ so install does not fail when no emacs

* Fri Sep 21 2007 Jens Petersen <petersen@redhat.com> - 0.16.1-12
- add a libs subpackage (suggested by Dwayne Bailey, #294891)
- move preloadable_libintl.so to the devel subpackage

* Fri Sep 14 2007 Nils Philippsen <nphilipp@redhat.com> - 0.16.1-11
- remove gettext-xglade-include-expat-285701.patch, add
  gettext-xglade-define-xml-major-version-285701.patch to determine
  XML_MAJOR_VERSION from expat.h and define it in config.h (#285701)

* Wed Sep 12 2007 Jens Petersen <petersen@redhat.com> - 0.16.1-10
- buildrequire expat-devel
- add gettext-xglade-include-expat-285701.patch to include expat.h
  to get xgettext to dl the right libexpat (Nils Philippsen, #285701)

* Thu Aug 16 2007 Jens Petersen <petersen@redhat.com>
- specify license is GPL and LGPL version 2 or later

* Wed Aug  1 2007 Jens Petersen <petersen@redhat.com> - 0.16.1-9
- fix encoding of msghack script (Dwayne Bailey, #250248)

* Mon Apr 30 2007 Jens Petersen <petersen@redhat.com> - 0.16.1-8
- add gettext-php-prinf-output-237241.patch to workaround php test failure
  (#237241)
- add gettext-php-headers.patch to correct php test headers
  (Robert Scheck, #232832)

* Thu Mar 15 2007 Jens Petersen <petersen@redhat.com> - 0.16.1-7
- set preloadable_libintl.so executable in %%install so it gets stripped
- force removal of infodir/dir since it is not there when /sbin is not in path

* Tue Mar 13 2007 Jens Petersen <petersen@redhat.com> - 0.16.1-6
- add buildjar switch for building of libintl.jar
- lots of spec file cleanup (Mamoru Tasaka, #225791):
- preserve timestamps of installed files
- disable building of static library
- use %%find_lang for .mo files
- remove examples from -devel package
- do not own en@*quot locale dirs
- set preloadable_libintl.so executable
- add ChangeLog to -devel package
- add %%check to run make check
- add gettext-tools-tests-lang-gawk-fail.patch to work around gawk test failure

* Fri Feb 23 2007 Karsten Hopp <karsten@redhat.com> 0.16.1-5
- rebuild to pick up dependency on libgcj.so.8rh instead libgcj.so.7rh

* Thu Feb  1 2007 Jens Petersen <petersen@redhat.com> - 0.16.1-4
- protect install-info in devel %%post and %%preun too (Ville Skyttä, #223689)
- forward port fix to reset of timestamp of examples ChangeLog for
  brp-java-repack-jars libintl.jar multilib conflict (#205207)

* Mon Jan 22 2007 Jens Petersen <petersen@redhat.com> - 0.16.1-3
- protect install-info in %%post and %%preun (Ville Skyttä, #223689)

* Fri Dec 22 2006 Jens Petersen <petersen@redhat.com> - 0.16.1-1
- update to 0.16.1

* Mon Nov 27 2006 Jens Petersen <petersen@redhat.com> - 0.16-2
- re-enable openmp on ia64

* Thu Nov 23 2006 Jens Petersen <petersen@redhat.com> - 0.16-1
- update to 0.16 release
- disable openmp on ia64 (#216988)

* Fri Oct 27 2006 Jens Petersen <petersen@redhat.com> - 0.15-1
- update to 0.15 release
- mkinstalldirs and libintl.jar are gone
- javaversion.class added

* Mon Oct  2 2006 Jens Petersen <petersen@redhat.com> - 0.14.6-3
- buildrequire zip and unzip to fix libintl.jar multilib conflict (#205207)

* Fri Aug 25 2006 Jens Petersen <petersen@redhat.com> - 0.14.6-2
- move libgettext*.so devel files to devel package (Patrice Dumas, #203622)

* Mon Aug  7 2006 Jens Petersen <petersen@redhat.com> - 0.14.6-1
- update to 0.14.6
- include preloadable_libintl.so again (Roozbeh Pournader, #149809)
- remove .la files (Kjartan Maraas, #172624)
- cleanup spec file

* Tue Jul 25 2006 Thomas Fitzsimmons <fitzsim@redhat.com> - 0.14.5-4
- Bump release number.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.14.5-3.1
- rebuild

* Wed Feb 22 2006 Karsten Hopp <karsten@redhat.de> 0.14.5-3
- --disable-csharp, otherwise it'll build a dll when mono is
  installed in the buildroot.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.14.5-2.2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.14.5-2.2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan  3 2006 Jesse Keating <jkeating@redhat.com> 0.14.5-2.2
- rebuilt again

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Sep 28 2005 Jindrich Novy <jnovy@redhat.com> 0.14.5-2
- convert spec to UTF-8
- remove old tarballs from sources

* Thu Aug 11 2005 Leon Ho <llch@redhat.com>
- updated to 0.14.5
- Add cvs as Requires for gettext-devel

* Mon Mar 21 2005 Leon Ho <llch@redhat.com>
- updated to 0.14.3
- fixed compiling problem on gcc4 (#150992)
- fixed Group for -devel (#138303)
- moved gettextize and autopoint to -devel (#137542, #145768)
- moved some of the man pages

* Tue Mar 01 2005 Jakub Jelinek <jakub@redhat.com>
- rebuilt with gcc 4.0

* Wed Dec 01 2004 Leon Ho <llch@redhat.com>
- Add env var to redirect use fastjar instead of jar
- BuildRequires fastjar and libgcj

* Mon Nov 01 2004 Leon Ho <llch@redhat.com>
- fix call on phase0_getc()
- fix temp file issue (#136323 - CAN-2004-0966 - mjc)

* Sun Oct 03 2004 Leon Ho <llch@redhat.com>
- fixed typo on %%preun on -devel

* Fri Oct 01 2004 Leon Ho <llch@redhat.com>
- fix install_info
- add gcc-java build requirement

* Mon Sep 13 2004 Leon Ho <llch@redhat.com>
- move java stuff to gettext-devel (#132239)
- add BuildRequires: gcc-c++ (#132518)
- add some missing install-info and ldconfig (#131272)
- fix dir ownership (#133696)
- run autotools for 1.9

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun 08 2004 Leon Ho <llch@redhat.com>
- use --without-included-gettext to avoid the need of libintl.so (#125497)
- remove preloadable_libintl.so

* Sun Jun 06 2004 Leon Ho <llch@redhat.com>
- moved some of the shared lib to main pkg
- added more build requires

* Thu Jun 03 2004 Leon Ho <llch@redhat.com>
- add conditionals for patch and requires auto* (#125216)

* Wed Jun 02 2004 Leon Ho <llch@redhat.com>
- packaged lib files for devel
- moved some of the files to different sub-pkg
- fix problem on x86_64 build

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Feb 02 2004 Leon Ho <llch@redhat.com>
- rebuilt to 0.14.1

* Fri Sep 19 2003 Leon Ho <llch@redhat.com>
- rebuilt 0.12.1
- fix including files and excludes some patches

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May 14 2003 Leon Ho <llch@redhat.com>
- 0.11.5

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Jan 16 2003 Leon Ho <llch@redhat.com> 0.11.4-6
- add online help for msghack replacement

* Thu Dec  5 2002 Leon Ho <llch@redhat.com> 0.11.4-5
- add patch to fix gettextize (#78720)

* Wed Nov 27 2002 Tim Powers <timp@redhat.com> 0.11.4-4
- remove unpackaged files from the buildroot

* Wed Aug 28 2002 Trond Eivind Glomsrød <teg@redhat.com> 0.11.4-3
- Use %%{_libdir} instead of /usr/lib (#72524)

* Fri Aug  2 2002 Nalin Dahyabhai <nalin@redhat.com> 0.11.4-2
- install ulonglong.m4, which is required by uintmax_t.m4, which is already
  being installed

* Sun Jul 28 2002 Trond Eivind Glomsrød <teg@redhat.com> 0.11.4-1
- 0.11.4

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue May 14 2002 Trond Eivind Glomsrød <teg@redhat.com> 0.11.2-1
- 0.11.2
- include some new files

* Fri Apr  5 2002 Trond Eivind Glomsrød <teg@redhat.com> 0.11.1-2
- Add patch to make it compile with C99 compilers (#62313)

* Wed Mar 13 2002 Trond Eivind Glomsrød <teg@redhat.com> 0.11.1-1
- 0.11.1

* Sun Feb 17 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- update gettext to 0.11
- disable patch4

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Dec  5 2001 Trond Eivind Glomsrød <teg@redhat.com> 0.10.40-3
- improve automake handling

* Wed Nov 14 2001 Trond Eivind Glomsrød <teg@redhat.com> 0.10.40-2
- Add URL
- Add automake workaround (#56081)

* Sun Sep 16 2001 Trond Eivind Glomsrød <teg@redhat.com> 0.10.40-1
- 0.10.40 - libintl is now LGPLed (it was GPLed). Note that RHL
  uses the glibc version, and don't include libintl from gettext.
- include new man pages
- don't include the elisp mode - bundle it into the main emacs package,
  like we do for XEmacs.
- README-alpha no longer exists, so don't list it as a doc file

* Fri Aug 24 2001 Trond Eivind Glomsrød <teg@redhat.com> 0.10.38-7
- Rebuild - this should fix #52463

* Wed Aug 22 2001 Trond Eivind Glomsrød <teg@redhat.com> 0.10.38-6
- Fix handling of multiline entries (rest of #50065)
- don't use the references of the last entry in a po file
- remove duplicates when inverting
- Own the en@quot and en@boldquot locale dirs (#52164)
- Handle entries with a first line of "" as identical to those
  without

* Thu Aug  9 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Added "--append" and "-o" to msghack, which should address
  initial concerns in #50065

* Thu Jul 19 2001 Trond Eivind Glomsrød <teg@redhat.com>
- New msghack - from scratch, in python

* Tue Jul 17 2001 Trond Eivind Glomsrød <teg@redhat.com>
- msghack is back

* Mon Jun  4 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Include some docfiles

* Sun Jun 03 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- 0.10.38
- do not include charset.alias

* Wed May  2 2001 Nalin Dahyabhai <nalin@redhat.com>
- Build statically.

* Mon Apr 30 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 0.10.37
- Disable all but two patches

* Sun Feb 25 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Initialize proper fonts when entering po-mode (#29152)

* Mon Feb 12 2001 Yukihiro Nakai <ynakai@redhat.com>
- More fix about msgmerge.

* Mon Feb 12 2001 Yukihiro Nakai <ynakai@redhat.com>
- Fix for msgmerge not to break multibyte strings
  at Japanese locale.

* Wed Jan 24 2001 Matt Wilson <msw@redhat.com>
- fixed the %%lang generator to not have "./" in the lang

* Sun Jan 14 2001 Trond Eivind Glomsrød <teg@redhat.com>
- add an init file for the emacs po-mode
- update source URL

* Thu Jan 11 2001 Bill Nottingham <notting@redhat.com>
- put gettext in /bin for initscripts use
- %%langify

* Fri Dec 29 2000 Bill Nottingham <notting@redhat.com>
- prereq /sbin/install-info

* Wed Aug 23 2000 Trond Eivind Glomsrød <teg@redhat.com>
- Added patch from Ulrich Drepper

* Fri Aug 04 2000 Trond Eivind Glomsrød <teg@redhat.com>
- update DESTDIR patch (#12072)

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jul 10 2000 Trond Eivind Glomsrød <teg@redhat.com>
- fix problems wrt to DESTDIR (#12072)

* Thu Jun 22 2000 Preston Brown <pbrown@redhat.com>
- use FHS paths
- add buildroot patch for .../intl/Makefile.in, was using abs. install path

* Fri Apr 28 2000 Bill Nottingham <notting@redhat.com>
- minor configure tweaks for ia64

* Sun Feb 27 2000 Cristian Gafton <gafton@redhat.com>
- add --comments to msghack

* Thu Feb 10 2000 Cristian Gafton <gafton@redhat.com>
- fix bug #9240 - gettextize has the right aclocal patch

* Wed Jan 12 2000 Cristian Gafton <gafton@redhat.com>
- add the --diff and --dummy options

* Wed Oct 06 1999 Cristian Gafton <gafton@redhat.com>
- add the --missing option to msghack

* Wed Sep 22 1999 Cristian Gafton <gafton@redhat.com>
- updated msghack not to merge in fuzzies in the master catalogs

* Thu Aug 26 1999 Cristian Gafton <gafton@redhat.com>
- updated msghack to understand --append

* Wed Aug 11 1999 Cristian Gafton <gafton@redhat.com>
- updated msghack to correctly deal with sorting files

* Thu May 06 1999 Cristian Gafton <gafton@redhat.com>
- msghack updates

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com>
- auto rebuild in the new build environment (release 8)

* Mon Mar 08 1999 Cristian Gafton <gafton@redhat.com>
- added patch for misc hacks to facilitate rpm translations

* Thu Dec 03 1998 Cristian Gafton <gafton@redhat.com>
- patch to allow to build on ARM

* Wed Sep 30 1998 Jeff Johnson <jbj@redhat.com>
- add Emacs po-mode.el files.

* Sun Sep 13 1998 Cristian Gafton <gafton@redhat.com>
- include the aclocal support files

* Thu Sep  3 1998 Bill Nottingham <notting@redhat.com>
- remove devel package (functionality is in glibc)

* Tue Sep  1 1998 Jeff Johnson <jbj@redhat.com>
- update to 0.10.35.

* Mon Jun 29 1998 Jeff Johnson <jbj@redhat.com>
- add gettextize.
- create devel package for libintl.a and libgettext.h.

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Sun Nov 02 1997 Cristian Gafton <gafton@redhat.com>
- added info handling
- added misc-patch (skip emacs-lisp modofications)

* Sat Nov 01 1997 Erik Troan <ewt@redhat.com>
- removed locale.aliases as we get it from glibc now
- uses a buildroot

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- Built against glibc
