# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global use_x11_tests 1
%if 0%{?fedora} || 0%{?rhel} > 9
%global use_xwayland_run 1
%endif
%bcond perl_Tk_enables_optional_test %{undefined rhel}

Name:           perl-Tk
Version:        804.036
Release: 24%{?dist}
Summary:        Perl Graphical User Interface ToolKit

License:        (GPL-1.0-or-later OR Artistic-1.0-Perl) AND SWL
URL:            https://metacpan.org/release/Tk
Source0:        https://cpan.metacpan.org/authors/id/S/SR/SREZIC/Tk-%{version}.tar.gz
Patch0:         perl-Tk-widget.patch
# modified version of http://ftp.de.debian.org/debian/pool/main/p/perl-tk/perl-tk_804.027-8.diff.gz
Patch1:         perl-Tk-debian.patch.gz
# fix segfaults as in #235666 because of broken cashing code
Patch2:         perl-Tk-seg.patch
Patch3:         perl-Tk-c99.patch
# Fix STRLEN vs int pointer confusion in Tcl_GetByteArrayFromObj()
# It breaks tests with Perl 5.38 on s390* (BZ#2222638)
Patch4:         perl-Tk-Fix-STRLEN-vs-int-pointer-confusion-in-Tcl_GetByteAr.patch

# Fix build with clang 16
# https://bugs.freebsd.org/bugzilla/show_bug.cgi?id=271521
Patch5:         perl-Tk-Fix-build-with-clang-16.patch
# Avoid using incompatible pointer type in pregcomp2.c
Patch6:         perl-Tk-pregcomp2.c-Avoid-using-incompatible-pointer-type.patch
# Avoid using incompatible pointer type for `old_warn`
# https://github.com/eserte/perl-tk/issues/98
Patch7:         perl-Tk-Avoid-using-incompatible-pointer-type-for-old_warn.patch
# Avoid using incompatible pointer type in function 'GetTextIndex'
# https://github.com/eserte/perl-tk/issues/103
Patch8:         perl-Tk-Fix-incompatible-pointer-type-in-function-GetTextIndex.patch

# Versions before this have Unicode issues
BuildRequires:  make
BuildRequires:  gcc-c++
BuildRequires:  perl-devel >= 3:5.8.3
BuildRequires:  perl-generators
BuildRequires:  freetype-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libpng-devel
BuildRequires:  libX11-devel
BuildRequires:  libXft-devel
BuildRequires:  perl(Config)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(lib)
BuildRequires:  perl(open)
BuildRequires:  perl(strict)
BuildRequires:  perl(Test)

%if %{use_x11_tests}
# Run-time:
BuildRequires:  perl(AutoLoader)
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(DirHandle)
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(Encode)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(if)
BuildRequires:  perl(locale)
# Image::Info is optional
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(overload)
BuildRequires:  perl(subs)
BuildRequires:  perl(Symbol)
BuildRequires:  perl(Text::Tabs)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
BuildRequires:  perl(XSLoader)

# Tests:
# X11 tests:
%if 0%{?use_xwayland_run}
BuildRequires:  xwayland-run
BuildRequires:  mutter
BuildRequires:  mesa-dri-drivers
%else
BuildRequires:  xorg-x11-server-Xvfb
%endif
BuildRequires:  google-noto-sans-fonts
BuildRequires:  font(:lang=en)
# Specific font is needed for tests, bug #1141117, CPAN RT#98831
BuildRequires:  liberation-sans-fonts
BuildRequires:  perl(blib)
BuildRequires:  perl(constant)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Devel::Peek)
BuildRequires:  perl(ExtUtils::Command::MM)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(IO::Socket)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(utf8)
# Optional tests:
%if %{with perl_Tk_enables_optional_test}
BuildRequires:  perl(Devel::Leak)
%endif
BuildRequires:  perl(MIME::Base64)
BuildRequires:  perl(Test::Pod)
%endif

Requires:       perl(locale)
Provides:       perl(Tk::LabRadio) = 4.004
Provides:       perl(Tk) = %{version}

%{?perl_default_filter}
# Explicity filter "useless" unversioned provides. For some reason, rpm is
# detecting these both with and without version.
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}perl\\(Tk\\)
%global __provides_exclude %__provides_exclude|perl\\(Tk::Clipboard\\)$
%global __provides_exclude %__provides_exclude|perl\\(Tk::Frame\\)$
%global __provides_exclude %__provides_exclude|perl\\(Tk::Listbox\\)$
%global __provides_exclude %__provides_exclude|perl\\(Tk::Scale\\)$
%global __provides_exclude %__provides_exclude|perl\\(Tk::Scrollbar\\)$
%global __provides_exclude %__provides_exclude|perl\\(Tk::Table\\)$
%global __provides_exclude %__provides_exclude|perl\\(Tk::Toplevel\\)$
%global __provides_exclude %__provides_exclude|perl\\(Tk::Widget\\)$
%global __provides_exclude %__provides_exclude|perl\\(Tk::Wm\\)$

# Filter modules bundled for tests
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}^%{_libexecdir}
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(TkTest\\)

%description
This a re-port of a perl interface to Tk8.4.
C code is derived from Tcl/Tk8.4.5.
It also includes all the C code parts of Tix8.1.4 from SourceForge.
The perl code corresponding to Tix's Tcl code is not fully implemented.

Perl API is essentially the same as Tk800 series Tk800.025 but has not
been verified as compliant. There ARE differences see pod/804delta.pod.

%package devel
Summary: perl-Tk ExtUtils::MakeMaker support module
Requires: perl-Tk = %{version}-%{release}

%description devel
%{summary}

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness
# X11 tests:
%if 0%{?use_xwayland_run}
Requires:       xwayland-run
Requires:       mutter
Requires:       mesa-dri-drivers
%else
Requires:       xorg-x11-server-Xvfb
%endif
Requires:       google-noto-sans-fonts
Requires:       font(:lang=en)
Requires:       liberation-sans-fonts

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n Tk-%{version}
find . -type f -exec perl -MConfig -pi -e \
's,^(#!)(/usr/local)?/bin/perl\b,$Config{startperl}, if ($. == 1)' {} \;
chmod -x pod/Popup.pod Tixish/lib/Tk/balArrow.xbm
# fix for widget as docs
%patch -P 0
perl -pi -e \
's,\@demopath\@,%{?_pkgdocdir}%{!?_pkgdocdir:%{_docdir}/%{name}-%{version}}/demos,g' demos/widget
# debian patch
#%%patch -P 1 -p1
# patch to fix #235666 ... seems like caching code is broken
%patch -P 2 -p1 -b .seg
%patch -P 3 -p1 -b .c99
%patch -P 4 -p1
%patch -P 5 -p1
%patch -P 6 -p1
%patch -P 7 -p1
%patch -P 8 -p1

# Help generators to recognize Perl scripts
for F in t/*.t; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!.*perl\b}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
perl Makefile.PL INSTALLDIRS=vendor X11LIB=%{_libdir} XFT=1 NO_PACKLIST=1 NO_PERLLOCAL=1
find . -name Makefile | xargs perl -pi -e 's/$/ -std=gnu99/ if /^CCFLAGS/;s/^\tLD_RUN_PATH=[^\s]+\s*/\t/'
%{make_build}

%check
%if %{use_x11_tests}
    export HARNESS_OPTIONS=j$(perl -e 'if ($ARGV[0] =~ /.*-j([0-9][0-9]*).*/) {print $1} else {print 1}' -- '%{?_smp_mflags}')
    %if 0%{?use_xwayland_run}
        xwfb-run -c mutter -- make test
    %else
        xvfb-run -d make test
    %endif
%endif

%install
%{make_install}

find %{buildroot} -type f -name '*.bs' -size 0 -delete

chmod -R u+rwX,go+rX,go-w %{buildroot}/*
mkdir __demos
cp -pR %{buildroot}%{perl_vendorarch}/Tk/demos __demos
find __demos/ -type f -exec chmod -x {} \;

# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
rm %{buildroot}%{_libexecdir}/%{name}/t/pod.t
mkdir -p %{buildroot}%{_libexecdir}/%{name}/demos/demos/images
cp demos/demos/images/cursor* %{buildroot}%{_libexecdir}/%{name}/demos/demos/images
perl -i -pe 's{-Mblib", "blib/script}{%{_bindir}}' %{buildroot}%{_libexecdir}/%{name}/t/exefiles.t
perl -i -ne 'print $_ unless m{gedi}' %{buildroot}%{_libexecdir}/%{name}/t/exefiles.t

cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/bash
set -e
# Some tests write into temporary files/directories
DIR=$(mktemp -d)
pushd "$DIR"
cp -a %{_libexecdir}/%{name}/* ./
%if 0%{?use_xwayland_run}
    xwfb-run -c mutter -- prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
%else
    xvfb-run -d prove -I . -j "$(getconf _NPROCESSORS_ONLN)"
%endif
popd
rm -rf "$DIR"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%files
%doc Changes README README.linux ToDo pTk/*license* __demos/demos demos/widget COPYING
%doc blib/man1/widget.1
%{_bindir}/p*
%{_bindir}/tkjpeg
%{perl_vendorarch}/auto/Tk
%{perl_vendorarch}/Tie*
%{perl_vendorarch}/Tk*
%exclude %{perl_vendorarch}/Tk/MMutil.pm
%exclude %{perl_vendorarch}/Tk/install.pm
%exclude %{perl_vendorarch}/Tk/MakeDepend.pm
%{_mandir}/man1/ptked*
%{_mandir}/man1/ptksh*
%{_mandir}/man1/tkjpeg*
%{_mandir}/man3/Tie*
%{_mandir}/man3/Tk*
%exclude %{_mandir}/man1/widget.1*
%exclude %{_bindir}/gedi
%exclude %{_bindir}/widget
%exclude %{perl_vendorarch}/Tk/demos

%files devel
%dir %{perl_vendorarch}/Tk
%{perl_vendorarch}/Tk/MMutil.pm
%{perl_vendorarch}/Tk/install.pm
%{perl_vendorarch}/Tk/MakeDepend.pm

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 804.036-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 804.036-22
- Perl 5.42 rebuild

* Wed Apr 02 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 804.036-21
- Avoid perl-Devel-Leak dependency on RHEL

* Thu Mar 20 2025 Xavier Bachelot <xavier@bachelot.org> - 804.036-20
- Fix build with gcc 15
- BR: perl-Devel-Leak and perl-Test-Pod to increase tests coverage

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 804.036-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 804.036-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 804.036-17
- Perl 5.40 rebuild

* Tue Mar 05 2024 Jitka Plesnikova <jplesnik@redhat.com> - 804.036-16
- Package tests

* Thu Feb 08 2024 Jitka Plesnikova <jplesnik@redhat.com> - 804.036-15
- Fix tests failing on s390* (rhbz#2222638)

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 804.036-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 804.036-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 804.036-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 804.036-11
- Perl 5.38 rebuild

* Thu Jun 01 2023 Michal Josef Špaček <mspacek@redhat.com> - 804.036-10
- Fix %patch macro
- Update license to SPDX format

* Fri Feb 24 2023 Florian Weimer <fweimer@redhat.com> - 804.036-9
- Port to C99

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 804.036-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 804.036-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 804.036-6
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 804.036-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 804.036-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jun 28 2021 Xavier Bachelot <xavier@bachelot.org> - 804.036-3
- Add specfile patch from Mauro Carvalho Chehab to fix building with FreeType
  support (RHBZ#1803711, RHBZ#1853802)

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 804.036-2
- Perl 5.34 rebuild

* Wed Feb 17 2021 Xavier Bachelot <xavier@bachelot.org> - 804.036-1
- Update to 0.36 (RHBZ#1928507)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 804.035-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 804.035-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 10 2020 Petr Pisar <ppisar@redhat.com> - 804.035-3
- Run-require locale module

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 804.035-2
- Perl 5.32 rebuild

* Wed Jun 17 2020 Jitka Plesnikova <jplesnik@redhat.com> - 804.035-1
- 804.035 bump

* Mon Feb 17 2020 Petr Pisar <ppisar@redhat.com> - 804.034-9
- Build-require blib module for tests

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 804.034-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 804.034-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 804.034-6
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 804.034-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 804.034-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 804.034-3
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 804.034-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Aug 28 2017 Jitka Plesnikova <jplesnik@redhat.com> - 804.034-1
- 804.034 bump

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 804.033-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 804.033-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 804.033-7
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 804.033-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 804.033-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 804.033-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 804.033-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 804.033-2
- Perl 5.22 rebuild

* Wed May 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 804.033-1
- 804.033 bump

* Fri Nov 07 2014 Petr Pisar <ppisar@redhat.com> - 804.032-5
- Restore compatibility with perl-ExtUtils-MakeMaker-7.00 (bug #1161470)

* Fri Sep 12 2014 Petr Pisar <ppisar@redhat.com> - 804.032-4
- Fix freetype detection
- Fix creating a window with perl 5.20 (bug #1141117)
- Enable X11 tests
- Specify all dependencies
- Fix t/fileevent2.t failure with /dev/null on stdin (bug #1141117)

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 804.032-3
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 804.032-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 31 2014 Jitka Plesnikova <jplesnik@redhat.com> - 804.032-1
- 804.032 bump

* Fri Jun 20 2014 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 804.031-6
- add patch from Yaakov Selkowitz to fix freetype detection (rhbz#1110872)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 804.031-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 10 2013 Ville Skyttä <ville.skytta@iki.fi> - 804.031-4
- Use %%{_pkgdocdir} where available.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 804.031-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 30 2013 Jitka Plesnikova <jplesnik@redhat.com> - 804.031-2
- Update license
- Package COPYING
- Specify all dependencies
- Replace PERL_INSTALL_ROOT with DESTDIR

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 804.031-1
- 804.031 bump

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 804.030-5
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 804.030-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 21 2013 Adam Tkac <atkac redhat com> - 804.030-3
- rebuild due to "jpeg8-ABI" feature drop

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 804.030-2
- rebuild against new libjpeg

* Wed Aug 29 2012 Jitka Plesnikova <jplesnik@redhat.com> - 804.030-1
- 804.030 bump, update source link

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 804.029-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 07 2012 Petr Pisar <ppisar@redhat.com> - 804.029-8
- Perl 5.16 rebuild

* Thu Jun 07 2012 Petr Pisar <ppisar@redhat.com> - 804.029-7
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 804.029-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 10 2011 Iain Arnell <iarnell@gmail.com> 804.029-5
- Rebuild for libpng 1.5

* Fri Oct 21 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 804.029-4
- Split out Tk/MMutil.pm, Tk/install.pm, Tk/MakeDepend.pm into perl-Tk-devel.
  (Avoid dependency on perl-devel - BZ 741777).

* Tue Jun 21 2011 Iain Arnell <iarnell@gmail.com> 804.029-3
- Perl mass rebuild

* Tue Jun 21 2011 Iain Arnell <iarnell@gmail.com> 804.029-2
- properly filter useless provides

* Fri Jun 17 2011 Iain Arnell <iarnell@gmail.com> 804.029-1
- update to 804.029_500 development version to fix FTBFS with perl 5.14
- clean up spec for modern rpmbuild
- use perl_default_filter and filter useless provides

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 804.028-16
- Perl mass rebuild

* Thu Jun 09 2011 Marcela Mašláňová <mmaslano@redhat.com> - 804.028-15
- Perl 5.14 mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 804.028-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 23 2010 Marcela Maslanova <mmaslano@redhat.com> - 804.028-13
- 661697 rebuild for fixing problems with vendorach/lib

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 804.028-12
- Mass rebuild with perl-5.12.0 & update to development release

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 804.028-11
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 804.028-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 22 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 804.028-9
- fix getOpenFile (#487122)

* Mon Jun 15 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 804.028-8
- fix events (#489228, #491536, #506496) 

* Thu Mar 19 2009 Stepan Kasal <skasal@redhat.com> - 804.028-7
- perl-Tk-XIM.patch (#489228)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 804.028-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Mar 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> 804.028-5
- rework patch2 to fix menu and test case failures (bz 431330, upstream 33880)

* Tue Feb 05 2008 Tom "spot" Callaway <tcallawa@redhat.com>
- 804.028-4
- rebuild for new perl

* Tue Feb 05 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 804.028-3
- fix #431529 gif overflow in tk (see also #431518)

* Fri Jan 04 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 804.028-2
- add relevant parts of debian patch
- add patch for #235666

* Wed Jan 02 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 804.028-1
- version upgrade
- fix #210718 SIGSEGV on exit from texdoctk
- fix #234404 Cannot manage big listboxes
- fix #235666 Segfault occurs when using Perl-Tk on FC6

* Wed Dec 19 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 804.027-13
- fix BR

* Wed Aug 22 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 804.027-12
- rebuild for buildid

* Sun Apr 01 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
804.027-11
- F7 rebuild (#234404)

* Fri Sep 15 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
804.027-10
- FE6 rebuild

* Thu Feb 16 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
804.027-9
- Rebuild for Fedora Extras 5

* Fri Nov 25 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
804.027-8
- modular xorg integration

* Sun Jul 31 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
804.027-7
- fix #164716

* Mon Jun 20 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
804.027-6
- some small cleanups
- add dist tag

* Thu Jun 16 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
804.027-5
- exclude gedi
- move widget to doc dir and patch it to work from there

* Wed Jun 15 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
804.027-4
- more cleanups from Ville Skyttä

* Wed Jun 15 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
804.027-3
- more cleanups

* Tue Jun 14 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
804.027-2
- add some stuff (e.g. xft) suggested by Steven Pritchard

* Tue Jun 14 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
804.027-1
- rebuild for fc4

* Fri Jun 04 2004 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0:804.027-0.fdr.1
- Initial Version (thanks to perl-Archive-Zip spec)
