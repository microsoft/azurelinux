# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:             gengetopt
Version:          2.23
Release:          16%{dist}
Summary:          Tool to write command line option parsing code for C programs
# Automatically converted from old format: GPLv3+ - review is highly recommended.
License:          GPL-3.0-or-later
URL:              http://www.gnu.org/software/gengetopt/
Source0:          ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz

BuildRequires:  gcc-c++
BuildRequires:  gcc
%ifarch %{valgrind_arches}
BuildRequires:  valgrind
%endif
BuildRequires:  texinfo
BuildRequires: make
Provides:         bundled(gnulib)

%description
Gengetopt is a tool to generate C code to parse the command line arguments
argc and argv that are part of every C or C++ program. The generated code uses
the C library function getopt_long to perform the actual command line parsing.

%prep
%setup -q

# Suppress rpmlint error.
chmod 644 ./AUTHORS
chmod 644 ./ChangeLog
chmod 644 ./COPYING
chmod 644 ./LICENSE
chmod 644 ./NEWS
chmod 644 ./README
chmod 644 ./THANKS
chmod 644 ./TODO
chmod 644 ./doc/README.example
chmod 644 ./doc/index.html
chmod 644 ./src/parser.yy
chmod 644 ./src/scanner.ll
find . -name '*.c' -exec chmod 644 {} ';'
find . -name '*.cc' -exec chmod 644 {} ';'
find . -name '*.cpp' -exec chmod 644 {} ';'
find . -name '*.h' -exec chmod 644 {} ';'
find . -name '*.ggo' -exec chmod 644 {} ';'

%build
%configure
# Parallel build doesn't work.
make

%install
%make_install INSTALL="%{__install} -p"
rm -frv %{buildroot}%{_infodir}/dir
# Use %%doc macro to install instead.
rm -frv %{buildroot}%{_docdir}/%{name}

mkdir ./examples
pushd ./doc
  cp -p README.example ../examples
  cp -p main1.cc sample1.ggo ../examples
  cp -p main2.c sample2.ggo ../examples
popd

%check
make check

%files
%doc AUTHORS ChangeLog NEWS README THANKS TODO
%doc doc/index.html doc/%{name}.html
%doc examples/
%license COPYING LICENSE
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_infodir}/*.info*
%{_mandir}/man1/%{name}.1*

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.23-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.23-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 25 2024 Miroslav Suchý <msuchy@redhat.com> - 2.23-14
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.23-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Mar 06 2024 Richard W.M. Jones <rjones@redhat.com> - 2.23-12
- Bump and rebuild package (for riscv64)

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.23-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.23-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.23-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.23-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.23-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.23-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.23-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.23-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Sep 9 2019 Mosaab Alzoubi <moceap[At]hotmail[Dot]com> - 2.23 -1
- Update to 2.23

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.22.6-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Mar  7 2019 Tim Landscheidt <tim@tim-landscheidt.de> - 2.22.6-14%{dist}
- Remove obsolete requirements for %%post/%%preun scriptlets

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.22.6-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.22.6-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.22.6-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.22.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.22.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.22.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.22.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Aug 24 2015 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 2.22.6-6
- Valgrind is not available only on s/390

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.22.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 2.22.6-4
- Rebuilt for GCC 5 C++11 ABI change

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.22.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.22.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Feb 20 2014 Christopher Meng <rpm@cicku.me> - 2.22.6-1
- Update to 2.22.6

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.22.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.22.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.22.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat May  5 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 2.22.5-1
- Update to 2.22.5-1 to fix FTBFS
- valgrind supported on ARM too

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.22.3-4
- Rebuilt for c++ ABI breakage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.22.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.22.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 04 2009 Debarshi Ray <rishi@fedoraproject.org> - 2.22.3-1
- Version bump to 2.22.3. (Red Hat Bugzilla #512414)
  * enum option values can contain + and -.
  * Fixed compilation problems due to macro FIX_UNUSED which was not in the
    right place.
  * New command line switches --header-output-dir and --src_output-dir to
    store cmdline.h separately from cmdline.c.
  * Use #include <getopt.h> in the generated files, instead of "getopt.h".
  * Generated functions use prototypes with char ** instead of char *const *.
  * Removed compilation warnings for generated files.
  * Fixed a compilation problem for files generated with --include-getopt
    with some versions of stdlib.h.
  * Use PACKAGE_NAME, if defined, for printing help and version.
- Encoding of ChangeLog and THANKS fixed by upstream.
- Removed spurious executable permissions from a bunch of files.

* Fri Jul 24 2009 Release Engineering <rel-eng@fedoraproject.org> - 2.22.1-3
- Autorebuild for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Release Engineering <rel-eng@fedoraproject.org> - 2.22.1-2
- Autorebuild for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jun 02 2008 Debarshi Ray <rishi@fedoraproject.org> - 2.22.1-1
- Version bump to 2.22.1. (Red Hat Bugzilla #444335)
  * Removed compilation warnings for generated files.
  * Fixed a bug with --long-help and enum options.
  * The outputs of --help and output of --show-help correspond with each other.
  * Fixed a compilation problem in generated output with mode options.
- Parallel build problems fixed by upstream.

* Fri Mar 07 2008 Debarshi Ray <rishi@fedoraproject.org> - 2.22-1
- Version bump to 2.22. (Red Hat Bugzilla #428641)
- Fixed build failure with gcc-4.3.
- Trimmed the 'BuildRequires' list.
- Changed character encodings from ISO8859-1 to UTF-8.
- Disabled parallel make to prevent failure with -j2.
- Added 'make check-valgrind' for ix86, x86_64, ppc and ppc64 in check stanza.
- Fixed Texinfo scriptlets according to Fedora packaging guidelines.

* Tue Aug 07 2007 Debarshi Ray <rishi@fedoraproject.org> - 2.21-2
- Removed 'BuildRequires: source-highlight' to prevent build failure.

* Sat Aug 04 2007 Debarshi Ray <rishi@fedoraproject.org> - 2.21-1
- Version bump to 2.21. (Red Hat Bugzilla #250817)
- License changed to GPLv3 or later.
- Parallel build problems fixed by upstream.
- README.example added by upstream.

* Tue Jun 12 2007 Debarshi Ray <rishi@fedoraproject.org> - 2.20-1
- Version bump to 2.20.

* Tue Jun 12 2007 Debarshi Ray <rishi@fedoraproject.org> - 2.19.1-3
- Added 'BuildRequires: ...' for check stanza.
- Added a check stanza.
- Removed -devel package.

* Mon Jun 11 2007 Debarshi Ray <rishi@fedoraproject.org> - 2.19.1-2
- Used variables name and version in Source0.
- Mentioned /sbin/install-info as a requirement for post and preun.
- Used _datadir instead of defining sharedir.
- Disabled parallel make to prevent failure with -j2.
- Removing /usr/share/info/dir in the install stanza.
- Replaced '$RPM_BUILD_DIR' with '.' in the install stanza.

* Sun Jun 10 2007 Debarshi Ray <rishi@fedoraproject.org> - 2.19.1-1
- Initial build.
- Added README.example from Debian.
- Changed version and date in online manual page to 2.19.1 from 2.19rc.
