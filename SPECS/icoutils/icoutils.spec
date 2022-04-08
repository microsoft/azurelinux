Summary:        Utility for extracting and converting Microsoft icon and cursor files
Name:           icoutils
Version:        0.32.3
Release:        8%{?dist}
License:        GPLv3
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.nongnu.org/icoutils/
Source0:        http://savannah.nongnu.org/download/%{name}/%{name}-%{version}.tar.bz2
# Possible security fix, at minimum it's a DoS.
# Upstream commit d72956a6de228c91d1fc48fd15448fadea9ab6cf
Patch1:         0001-wrestool-Fix-get_resource_id_quoted-to-return-heap-a.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  libpng-devel
BuildRequires:  perl-generators
Provides:       bundled(gnulib)

%description
The icoutils are a set of programs for extracting and converting images in
Microsoft Windows icon and cursor files. These files usually have the
extension .ico or .cur, but they can also be embedded in executables or
libraries.

%prep
%setup -q

%patch1 -p1

autoreconf -i

for f in AUTHORS NEWS; do
  iconv -f ISO88592 -t UTF8 < $f > $f.utf8 && \
  touch -r $f $f.utf8 && \
  mv $f.utf8 $f
done

%build
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
%find_lang %{name}

%files -f %{name}.lang
%license COPYING
%doc README AUTHORS NEWS TODO ChangeLog
%{_bindir}/extresso
%{_bindir}/genresscript
%{_bindir}/icotool
%{_bindir}/wrestool
%{_mandir}/man1/*.1*

%changelog
* Thu Mar 31 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.32.3-8
- Cleaning-up spec. License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.32.3-7
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.32.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.32.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.32.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.32.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Mar 13 2018 Richard W.M. Jones <rjones@redhat.com> - 0.32.3-2
- Add upstream post-0.32.3 commit which appears to fix crash/DoS.

* Mon Mar 12 2018 Martin Gieseking <martin.gieseking@uos.de> - 0.32.3-1
- Updated to version 0.32.3.
- Dropped patch to fix https://savannah.nongnu.org/bugs/?52319 (applied upstream)

* Mon Feb 19 2018 Martin Gieseking <martin.gieseking@uos.de> - 0.32.2-3
- Added BR: gcc according to new packaging guidelines

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.32.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Nov 01 2017 Martin Gieseking <martin.gieseking@uos.de> - 0.32.2-1
- Updated to version 0.32.2.
- Added patch to fix https://savannah.nongnu.org/bugs/?52319

* Sat Sep 02 2017 Martin Gieseking <martin.gieseking@uos.de> - 0.32.0-1
- Updated to version 0.32.0.

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.31.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.31.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Mar 12 2017 Richard W.M. Jones <rjones@redhat.com> - 0.31.3-1
- New upstream version 0.31.3.
- This includes all the previous upstream patches, and reverts the
  check which broke processing of PE binaries.

* Fri Mar 10 2017 Richard W.M. Jones <rjones@redhat.com> - 0.31.2-3
- Add a series of upstream patches to enable compiler warnings and
  fix multiple issues.
- Revert one of the checks which breaks processing of PE binaries.
- Removed the 'Group' line, not needed with modern Fedora/RPM.

* Tue Mar 07 2017 Martin Gieseking <martin.gieseking@uos.de> - 0.31.2-1
- Updated to version 0.31.2.
- Fixes RHBZ #1422906, #1422907, and #1422908

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.31.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 09 2017 Martin Gieseking <martin.gieseking@uos.de> - 0.31.1-1
- Updated to version 0.31.1.
- Dropped wrestool patch because it has been applied upstream.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.31.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Sep 08 2015 Martin Gieseking <martin.gieseking@uos.de> 0.31.0-8
- Added patch to prevent wrestool to segfault when reading inconsistent resource data

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 01 2014 Martin Gieseking <martin.gieseking@uos.de> 0.31.0-4
- Fixed autoreconf issue (RHBZ #1083081)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 0.31.0-2
- Perl 5.18 rebuild

* Mon Jun 17 2013 Martin Gieseking <martin.gieseking@uos.de> 0.31.0-1
- Updated to version 0.31.0.
- Dropped patches as they have been applied upstream.

* Thu May 16 2013 Richard W.M. Jones <rjones@redhat.com> 0.30.0-3
- Documentation fixes (RHBZ#948882).

* Sat Mar 23 2013 Martin Gieseking <martin.gieseking@uos.de> 0.30.0-2
- Rebuilt with recent autoconf for https://bugzilla.redhat.com/show_bug.cgi?id=925575

* Wed Mar 20 2013 Martin Gieseking <martin.gieseking@uos.de> 0.30.0-1
- updated to release 0.30.0
- dropped patch as it has been applied upstream
- removed old buildroot stuff

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.29.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.29.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat May 19 2012 Martin Gieseking <martin.gieseking@uos.de> 0.29.1-6
- added missing Provides: bundled(gnulib): https://bugzilla.redhat.com/show_bug.cgi?id=821764

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.29.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.29.1-4
- Rebuild for new libpng

* Mon May 16 2011 Martin Gieseking <martin.gieseking@uos.de> - 0.29.1-3
- fixed http://bugzilla.redhat.com/show_bug.cgi?id=701855
- minor spec cleanup

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.29.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Mar 20 2010 - Martin Gieseking <martin.gieseking@uos.de> - 0.29.1-1
- new upstream release fixes a segfault occurred in icotool
- fixed encoding of file AUTHORS

* Wed Feb 24 2010 - Martin Gieseking <martin.gieseking@uos.de> - 0.29.0-1
- updated to latest upstream release
- added newly available locales to package

* Mon Aug 17 2009 - Martin Gieseking <martin.gieseking@uos.de> - 0.28.0-1
- updated to latest upstream release
- changed license tag to GPLv3+

* Fri Aug 14 2009 - Martin Gieseking <martin.gieseking@uos.de> - 0.27.0-1
- updated to latest upstream release
- added missing BuildRequires
- patched wrestool/Makefile.am to fix ppc build failures

* Fri Apr 17 2009 - Eric Moret <eric.moret@gmail.com> - 0.26.0-1
- Initial spec
