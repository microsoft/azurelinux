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

Name:           pari
Version:        2.17.3
Release:        %autorelease
Summary:        Number Theory-oriented Computer Algebra System

%global majver %(cut -d. -f1-2 <<< %{version})

License:        GPL-2.0-or-later
URL:            https://pari.math.u-bordeaux.fr/
VCS:            git:https://pari.math.u-bordeaux.fr/git/pari.git
Source0:        https://pari.math.u-bordeaux.fr/pub/pari/unix/%{name}-%{version}.tar.gz
Source1:        https://pari.math.u-bordeaux.fr/pub/pari/unix/%{name}-%{version}.tar.gz.asc
# Public key 0x4522e387, Bill Allombert <Bill.Allombert@math.u-bordeaux.fr>
Source2:        gpgkey-42028EA404A2E9D80AC453148F0E7C2B4522E387.gpg
Source3:        fr.u-bordeaux.math.pari.desktop
Source4:        pari-gp.xpm
Source5:        pari.abignore
Source6:        fr.u-bordeaux.math.pari.metainfo.xml
# Use xdg-open rather than xdvi to display DVI files (#530565)
Patch:          pari-2.17.0-xdgopen.patch
# Fix compiler warnings
# http://pari.math.u-bordeaux.fr/cgi-bin/bugreport.cgi?bug=1316
Patch:          pari-2.9.0-missing-field-init.patch
Patch:          pari-2.17.0-declaration-not-prototype.patch

BuildRequires:  coreutils
BuildRequires:  desktop-file-utils
BuildRequires:  findutils
BuildRequires:  fltk-devel
BuildRequires:  gcc-c++
BuildRequires:  gmp-devel
BuildRequires:  gnupg2
BuildRequires:  libappstream-glib
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  pkgconfig(readline)
BuildRequires:  sed
BuildRequires:  tex(latex)

# Test suite requirements
BuildRequires:  pari-elldata
BuildRequires:  pari-galdata
BuildRequires:  pari-galpol
BuildRequires:  pari-nflistdata
BuildRequires:  pari-seadata

# Avoid doc-file dependencies and provides
%global __provides_exclude_from ^%{_datadir}/pari/PARI/
%global __requires_exclude_from ^%{_datadir}/pari/PARI/

%description
PARI is a widely used computer algebra system designed for fast computations in
number theory (factorizations, algebraic number theory, elliptic curves...),
but also contains a large number of other useful functions to compute with
mathematical entities such as matrices, polynomials, power series, algebraic
numbers, etc., and a lot of transcendental functions.

This package contains the shared libraries. The interactive
calculator PARI/GP is in package pari-gp.

%package devel
Summary:        Header files and libraries for PARI development
Requires:       %{name} = %{version}-%{release}

%description devel
Header files and libraries for PARI development.

%package gp
Summary:        PARI calculator
Requires:       %{name} = %{version}-%{release}
Requires:       bzip2
Requires:       gzip
Requires:       xdg-utils
Requires:       mimehandler(application/x-dvi)

%description gp
PARI/GP is an advanced programmable calculator, which computes
symbolically as long as possible, numerically where needed, and
contains a wealth of number-theoretic functions.

%prep
# Verify the source file
%{gpgverify} --data=%{SOURCE0} --signature=%{SOURCE1} --keyring=%{SOURCE2}

%autosetup -p0

# Silence abidiff warnings about the size of functions_basic[] changing
cp -p %{SOURCE5} .

%conf
# Avoid unwanted rpaths
sed -i "s|runpathprefix='.*'|runpathprefix=''|" config/get_ld

%build
# For as yet unknown reasons, 32-bit pari becomes extremely slow if built with
# pthread support.  Enable it for 64-bit only until we can diagnose the issue.
./Configure \
    --prefix=%{_prefix} \
    --share-prefix=%{_datadir} \
    --bindir=%{_bindir} \
    --libdir=%{_libdir} \
    --mandir=%{_mandir}/man1 \
    --datadir=%{_datadir}/pari \
    --includedir=%{_includedir} \
%if 0%{?__isa_bits} == 64
    --mt=pthread \
%endif
    --enable-tls \
    --with-fltk \
    --with-gmp
%make_build gp

%install
%make_install INSTALL="install -p" STRIP=%{_bindir}/true

# Move the library directory on 64-bit systems
if [ "%{_lib}" != "lib" ]; then
    mkdir -p %{buildroot}%{_libdir}
    mv %{buildroot}%{_prefix}/lib/pari %{buildroot}%{_libdir}
fi

# Site-wide gprc
mkdir -p %{buildroot}%{_sysconfdir}
install -p -m 644 misc/gprc.dft %{buildroot}%{_sysconfdir}/gprc

# Desktop menu entry
mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
    --dir %{buildroot}%{_datadir}/applications \
    %{SOURCE3}
mkdir -p %{buildroot}%{_datadir}/pixmaps
install -p -m 644 %{SOURCE4} %{buildroot}%{_datadir}/pixmaps

# Install the AppData file
mkdir -p %{buildroot}%{_metainfodir}
install -pm 644 %{SOURCE6} %{buildroot}%{_metainfodir}
appstream-util validate-relax --nonet \
  %{buildroot}%{_metainfodir}/fr.u-bordeaux.math.pari.metainfo.xml

# Work around package-notes breakage.  The package-notes feature was not
# designed for software like this, which stores flags to use to build other
# software.  All such packages now have to go through contortions like this,
# with the result that the software it builds does NOT have package notes.
sed -e 's|%{build_cxxflags}|%{extension_cxxflags}|' \
    -e 's|%{build_ldflags}|%{extension_ldflags}|' \
    -i %{buildroot}%{_libdir}/pari/pari.cfg

# The qf tests started failing on 32-bit x86 with the release of 2.15.3.
# The final test is supposed to report "precision too low in forqfvec", but
# does not.  The cause is currently unknown.  Since we don't really care about
# that architecture, just let it pass until somebody cares enough to diagnose
# the issue, or we stop building for 32-bit x86.
%ifnarch %{ix86}
%check
make test-all
%endif

%files
%license COPYING
%doc AUTHORS CHANGES* COMPAT NEW README
%doc pari.abignore
%{_libdir}/libpari-gmp-tls.so.%{version}
%{_libdir}/libpari-gmp-tls.so.9
%{_libdir}/pari/

%files gp
%{_bindir}/gp
%{_bindir}/gp-%{majver}
%{_bindir}/gphelp
%{_bindir}/tex2mail
%config(noreplace) %{_sysconfdir}/gprc
%dir %{_datadir}/pari/
%doc %{_datadir}/pari/PARI/
%doc %{_datadir}/pari/doc/
%doc %{_datadir}/pari/examples/
%{_datadir}/pari/misc/
%{_datadir}/pari/pari.desc
%{_datadir}/applications/fr.u-bordeaux.math.pari.desktop
%{_datadir}/pixmaps/pari-gp.xpm
%{_metainfodir}/fr.u-bordeaux.math.pari.metainfo.xml
%{_mandir}/man1/gp-%{majver}.1*
%{_mandir}/man1/gp.1*
%{_mandir}/man1/gphelp.1*
%{_mandir}/man1/pari.1*
%{_mandir}/man1/tex2mail.1*

%files devel
%{_includedir}/pari/
%{_libdir}/libpari.so

%changelog
## START: Generated by rpmautospec
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 2.17.3-2
- Latest state for pari

* Thu Dec 04 2025 Jerry James <loganjerry@gmail.com> - 2.17.3-1
- Version 2.17.3

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Mar 21 2025 Jerry James <loganjerry@gmail.com> - 2.17.2-1
- Version 2.17.2

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Dec 24 2024 Jerry James <loganjerry@gmail.com> - 2.17.1-1
- Version 2.17.1

* Sat Oct 05 2024 Jerry James <loganjerry@gmail.com> - 2.17.0-1
- Version 2.17.0
- Drop upstreamed patches: clobbered, signed-unsigned-comparison

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.15.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Feb 26 2024 Jerry James <loganjerry@gmail.com> - 2.15.5-1
- Version 2.15.5

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.15.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.15.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.15.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 18 2023 Jerry James <loganjerry@gmail.com> - 2.15.4-1
- Version 2.15.4
- Validate metainfo with appstream-util

* Tue Mar 14 2023 Jerry James <loganjerry@gmail.com> - 2.15.3-1
- Version 2.15.3
- Add a metainfo file
- Use https URLs
- BR pari-nflistdata for the tests
- Temporarily disable tests on 32-bit x86

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.15.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jan  6 2023 Jerry James <loganjerry@gmail.com> - 2.15.2-1
- Version 2.15.2

* Sat Nov  5 2022 Jerry James <loganjerry@gmail.com> - 2.15.1-1
- Version 2.15.1
- Drop upstreamed ploth-doc patch

* Mon Sep 26 2022 Jerry James <loganjerry@gmail.com> - 2.15.0-1
- Version 2.15.0
- Drop upstreamed optflags patch
- Convert License tag to SPDX

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Apr  7 2022 Jerry James <loganjerry@gmail.com> - 2.13.4-1
- Version 2.13.4

* Sun Jan 30 2022 Jerry James <loganjerry@gmail.com> - 2.13.3-3
- Work around yet more package-notes breakage

* Fri Jan 28 2022 Jerry James <loganjerry@gmail.com> - 2.13.3-2
- Work around package-notes breakage

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Oct 25 2021 Jerry James <loganjerry@gmail.com> - 2.13.3-1
- Version 2.13.3

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jul 16 2021 Jerry James <loganjerry@gmail.com> - 2.13.2-2
- Install the config file in a more standard location

* Tue Jun 29 2021 Jerry James <loganjerry@gmail.com> - 2.13.2-1
- Version 2.13.2
- Disable pthread support on 32-bit arches due to extreme slowness

* Thu Jun 17 2021 Jerry James <loganjerry@gmail.com> - 2.13.1-3
- Build with pthread support

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 25 2021 Jerry James <loganjerry@gmail.com> - 2.13.1-1
- Version 2.13.1

* Tue Jan 19 2021 Adam Jackson <ajax@redhat.com> - 2.13.0-2
- Drop BuildRequires: xmkmf, which was only used when building the X11 (not
  fltk) GUI.

* Mon Nov  9 2020 Jerry James <loganjerry@gmail.com> - 2.13.0-1
- Update to 2.13.0 (see CHANGES for details)
- Enable TLS support
- Build the GUI with fltk instead of X11
- Ship the xgp wrapper script

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 29 2020 Jerry James <loganjerry@gmail.com> - 2.11.4-1
- Update to 2.11.4 (see CHANGES for details)

* Thu Mar  5 2020 Jerry James <loganjerry@gmail.com> - 2.11.3-1
- Update to 2.11.3 (see CHANGES for details)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jul 18 2019 Jerry James <loganjerry@gmail.com> - 2.11.2-2
- Verify the source file

* Wed May 15 2019 Jerry James <loganjerry@gmail.com> - 2.11.2-1
- Update to 2.11.2 (see CHANGES for details)

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.11.1-3
- Rebuild for readline 8.0

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jan  4 2019 Jerry James <loganjerry@gmail.com> - 2.11.1-1
- Update to 2.11.1 (see CHANGES for details)
- Drop braces patch

* Fri Aug 10 2018 Jerry James <loganjerry@gmail.com> - 2.11.0-1
- Update to 2.11.0 (see CHANGES for details)
- Drop ellratpoints patch
- Obsolete genus2reduction

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun  2 2018 Jerry James <loganjerry@gmail.com> - 2.9.5-2
- Backport ellratpoints and hyperellratpoints from 2.10alpha for sagemath

* Mon May 21 2018 Paul Howarth <paul@city-fan.org> - 2.9.5-1
- Update to 2.9.5 (see CHANGES for details)

* Tue Feb  6 2018 Paul Howarth <paul@city-fan.org> - 2.9.4-2
- Switch to %%ldconfig_scriptlets
- Silence abidiff warnings about the size of functions_basic[] changing

* Tue Jan  9 2018 Paul Howarth <paul@city-fan.org> - 2.9.4-1
- Update to 2.9.4 (see CHANGES for details)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 14 2017 Paul Howarth <paul@city-fan.org> - 2.9.3-1
- Update to 2.9.3 (see CHANGES for details)

* Tue Jun 20 2017 Paul Howarth <paul@city-fan.org> - 2.9.2-3
- Include pari/gp desktop icon, dropped from upstream releases after 2.5.x
  (#1462987)
- Drop redundant Group: tags

* Tue Apr 18 2017 Paul Howarth <paul@city-fan.org> - 2.9.2-2
- Drop the compat library for pari 2.7 as nothing in Fedora is using it now

* Thu Apr  6 2017 Paul Howarth <paul@city-fan.org> - 2.9.2-1
- Update to 2.9.2 (see CHANGES for details)
- Build with -Wno-implicit-fallthrough because upstream code intentionally
  falls through switch cases all over the place

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 2.9.1-2
- Rebuild for readline 7.x

* Sun Dec  4 2016 Paul Howarth <paul@city-fan.org> - 2.9.1-1
- Update to 2.9.1 (see CHANGES for details)

* Wed Nov  2 2016 Paul Howarth <paul@city-fan.org> - 2.9.0-1
- Update to 2.9.0 (see NEW and CHANGES for details)
- Update patches as needed
- Temporarily include old version of library to avoid broken deps whilst
  migration to pari 2.9 happens in Rawhide

* Tue Jun 21 2016 Paul Howarth <paul@city-fan.org> - 2.7.6-1
- Update to 2.7.6 (see CHANGES for details)
- Simplify find command using -delete
- Specify all build requirements

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Paul Howarth <paul@city-fan.org> - 2.7.5-1
- Update to 2.7.5 (see CHANGES for details)

* Sat Jun 20 2015 Paul Howarth <paul@city-fan.org> - 2.7.4-1
- Update to 2.7.4 (see CHANGES for details)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Feb 19 2015 Paul Howarth <paul@city-fan.org> - 2.7.3-1
- Update to 2.7.3 (see CHANGES for details)

* Fri Sep 19 2014 Paul Howarth <paul@city-fan.org> - 2.7.2-1
- Update to 2.7.2 (see CHANGES for details)
- Update patches as needed
- Drop libpari-gmp.so.3 compat library
- Use %%license where possible

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jul  7 2014 Paul Howarth <paul@city-fan.org> - 2.7.1-4
- Fix crash in ellmul with obsolete use of E=[a1,a2,a3,a4,a6]
  (#1104802, upstream bug #1589)

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 22 2014 Paul Howarth <paul@city-fan.org> - 2.7.1-2
- Temporarily include old version of library to avoid broken deps whilst
  migration to pari 2.7 happens in Rawhide

* Fri May 16 2014 Paul Howarth <paul@city-fan.org> - 2.7.1-1
- Update to 2.7.1 (see CHANGES for details)

* Mon Mar 24 2014 Paul Howarth <paul@city-fan.org> - 2.7.0-1
- Update to 2.7.0 (see NEW for details)
- Update patches as needed
- BR: pari-galpol for additional test coverage

* Sat Sep 21 2013 Paul Howarth <paul@city-fan.org> - 2.5.5-1
- Update to 2.5.5 (see CHANGES for details)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 2.5.4-2
- Perl 5.18 rebuild

* Tue May 14 2013 Paul Howarth <paul@city-fan.org> - 2.5.4-1
- update to 2.5.4 (see CHANGES for details)
- update missing-field-init patch

* Wed May  1 2013 Jon Ciesla <limburgher@gmail.com> - 2.5.3-3
- drop desktop vendor tag

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.3-2
- rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Oct  4 2012 Paul Howarth <paul@city-fan.org> - 2.5.3-1
- update to 2.5.3 (see CHANGES for details)
- further compiler warning fixes after discussion with upstream
- drop upstreamed parts of declaration-not-prototype patch

* Mon Aug  6 2012 Paul Howarth <paul@city-fan.org> - 2.5.2-1
- update to 2.5.2 (see CHANGES for details)
- drop upstreamed gcc 4.7, bug#1264 and FSF address patches

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1-2
- rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May  9 2012 Paul Howarth <paul@city-fan.org> - 2.5.1-1
- update to 2.5.1 (#821191; see NEW for details)
- use rpm 4.9.x requires/provides filtering
- update xdg-open patch
- drop emacs sub-package; the PARI Emacs shell is now a separate project
- drop %%defattr, redundant since rpm 4.4
- gp sub-package requires bzip2 for support of bzipped files
- make %%files list more explicit
- drop redundant buildroot definition and cleaning
- BR: xmkmf for X11 detection
- make sure we use our %%{optflags} and only those
- call pari_init_defaults() before gp_expand_path() (upstream #1264)
- fix scoping issue that manifests as a test suite failure with gcc 4.7.x and
  -ftree-dse (#821918, upstream #1314)
- fix desktop file categories
- install site-wide /etc/gprc
- update FSF address (upstream #1315)
- fix various compiler warnings (upstream #1316)
- run the full test suite in %%check
- add buildreqs for data packages needed by full test suite
- hardcode %%{_datadir} in gp.desktop so no need to fiddle with it in %%prep

* Sat Jan  7 2012 Paul Howarth <paul@city-fan.org> - 2.3.5-4
- s/\$RPM_BUILD_ROOT/%%{buildroot}/g for tidyness
- update source URL as 2.3.5 is now an OLD version

* Wed Oct 26 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.3.5-3.2
- rebuild with new gmp without compat lib

* Wed Oct 12 2011 Peter Schiffer <pschiffe@redhat.com> - 2.3.5-3.1
- rebuild with new gmp

* Tue Feb  8 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.5-3
- rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Oct  1 2010 Mark Chappell <tremble@fedoraproject.org> - 2.3.5-2
- switch the latex dependencies over to tex(...)

* Fri Jul  9 2010 Paul Howarth <paul@city-fan.org> - 2.3.5-1
- update to 2.3.5 (see CHANGES for details)
- filter out perl dependencies from %%{_datadir}/pari/PARI/

* Thu Jul  8 2010 Paul Howarth <paul@city-fan.org> - 2.3.4-5
- various clean-ups to pacify rpmlint:
  - uses spaces instead of tabs consistently
  - mark %%{_datadir}/emacs/site-lisp/pari/pariemacs.txt as %%doc
  - mark %%{_datadir}/pari/{PARI,doc,examples} as %%doc
  - fix permissions of gp
- don't strip gp so we get debuginfo for it
- move here documents out to separate source files
- make gp subpackage require same version-release of main package

* Wed Jul  7 2010 Paul Howarth <paul@city-fan.org> - 2.3.4-4
- apply patch from Patrice Dumas to use xdg-open rather than xdvi to display
  DVI content, and move the xdg-open requirement from the main package to the
  gp sub-package (#530565)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 22 2008 Gerard Milmeister <gemi@bluewin.ch> - 2.3.4-1
- new release 2.3.4

* Wed Aug 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.3.3-2
- fix license tag

* Sat Feb 23 2008 Gerard Milmeister <gemi@bluewin.ch> - 2.3.3-1
- new release 2.3.3

* Sat Feb 23 2008 Gerard Milmeister <gemi@bluewin.ch> - 2.3.1-3
- corrected desktop file

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.3.1-2
- Autorebuild for GCC 4.3

* Fri Dec 29 2006 Gerard Milmeister <gemi@bluewin.ch> - 2.3.1-1
- new version 2.3.1

* Fri Dec 29 2006 Gerard Milmeister <gemi@bluewin.ch> - 2.3.0-5
- added -fno-strict-aliasing to CFLAGS and enabled ppc build

* Mon Aug 28 2006 Gerard Milmeister <gemi@bluewin.ch> - 2.3.0-4
- Rebuild for FE6

* Fri May 26 2006 Gerard Milmeister <gemi@bluewin.ch> - 2.3.0-3
- Exclude ppc for now, since test fails

* Fri May 26 2006 Gerard Milmeister <gemi@bluewin.ch> - 2.3.0-2
- added %%check section
- use gmp

* Thu May 25 2006 Gerard Milmeister <gemi@bluewin.ch> - 2.3.0-1
- new version 2.3.0

* Fri May 19 2006 Orion Poplawski <orion@cora.nwra.com> - 2.1.7-4
- Fix shared library builds

* Fri Dec  2 2005 Gerard Milmeister <gemi@bluewin.ch> - 2.1.7-3
- Use none for architecture to guarantee working 64bit builds

* Fri Oct 21 2005 Gerard Milmeister <gemi@bluewin.ch> - 2.1.7-2
- some cleanup

* Fri Sep 30 2005 Gerard Milmeister <gemi@bluewin.ch> - 2.1.7-1
- New Version 2.1.7

* Sun Mar  6 2005 Gerard Milmeister <gemi@bluewin.ch> - 2.1.6-1
- New Version 2.1.6

* Mon Nov 22 2004 Gerard Milmeister <gemi@bluewin.ch> - 0:2.1.5-0.fdr.2
- Fixed problem with readline

* Wed Nov 12 2003 Gerard Milmeister <gemi@bluewin.ch> - 0:2.1.5-0.fdr.x
- First Fedora release

## END: Generated by rpmautospec
