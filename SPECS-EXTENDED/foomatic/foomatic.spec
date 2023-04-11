Summary:        Tools for using the foomatic database of printers and printer drivers
Name:           foomatic
Version:        4.0.13
Release:        17%{?dist}
License:        GPL-2.0-or-later
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.linuxfoundation.org/collaborate/workgroups/openprinting/database/foomatic
Source0:        https://www.openprinting.org/download/foomatic/foomatic-db-engine-%{version}.tar.gz
Patch101:       foomatic-manpages.patch
Patch102:       0001-Recognize-fractional-numbers-in-PageSize.patch
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  cups
BuildRequires:  cups-devel
BuildRequires:  dbus-devel
BuildRequires:  gcc
BuildRequires:  libxml2-devel
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter >= 3:5.8.1
BuildRequires:  python3-cups
BuildRequires:  perl(ExtUtils::MakeMaker)
Requires:       colord
Requires:       cups
Requires:       cups-filters >= 1.0.42
Requires:       dbus
Requires:       foomatic-db
Requires:       ghostscript
Requires:       perl-interpreter >= 3:5.8.1
Requires:       %(eval `perl -V:version`; echo "perl(:MODULE_COMPAT_$version)")
Requires(post): coreutils
%if 0%{!?perl_bootstrap:1}
BuildRequires:  foomatic
BuildRequires:  foomatic-db
%endif

%description
Foomatic is a comprehensive, spooler-independent database of printers,
printer drivers, and driver descriptions. This package contains
utilities to generate driver description files and printer queues for
CUPS, LPD, LPRng, and PDQ using the database (packaged separately).
There is also the possibility to read the PJL options out of PJL-capable
laser printers and take them into account at the driver description
file generation.

There are spooler-independent command line interfaces to manipulate
queues (foomatic-configure) and to print files/manipulate jobs
(foomatic printjob).

The site http://www.linuxprinting.org/ is based on this database.

%prep
%setup -q -n foomatic-db-engine-%{version}

%patch101 -p1 -b .manpages
%patch102 -p1 -b .pagesize-fract

chmod a+x mkinstalldirs

%build
export LIB_CUPS=%{_cups_serverbin}
export CUPS_BACKENDS=%{_cups_serverbin}/backend
export CUPS_FILTERS=%{_cups_serverbin}/filter
export CUPS_PPDS=%{_datadir}/cups/model

aclocal
autoconf
%configure --disable-xmltest
make PREFIX=%{_prefix} CFLAGS="%{optflags}"

%install
make    DESTDIR=%{buildroot} PREFIX=%{_prefix} \
        INSTALLSITELIB=%{perl_vendorlib} \
        INSTALLSITEARCH=%{perl_vendorarch} \
        install

ln -sf ../../../bin/foomatic-ppdfile %{buildroot}%{_cups_serverbin}/driver/foomatic

mkdir -p %{buildroot}%{_var}/cache/foomatic

echo cups > %{buildroot}%{_sysconfdir}/foomatic/defaultspooler

rm -rf  \
        %{buildroot}%{_libdir}/ppr \
        %{buildroot}%{_sysconfdir}/foomatic/filter.conf.sample \
        %{buildroot}%{_datadir}/foomatic/templates
find %{buildroot} -name .packlist | xargs rm -f

%post
/bin/rm -f %{_var}/cache/foomatic/*
exit 0

%files
%license COPYING
%dir %{_sysconfdir}/foomatic
%config(noreplace) %{_sysconfdir}/foomatic/defaultspooler
%{_bindir}/foomatic-combo-xml
%{_bindir}/foomatic-compiledb
%{_bindir}/foomatic-configure
%{_bindir}/foomatic-datafile
%{_bindir}/foomatic-perl-data
%{_bindir}/foomatic-ppd-options
%{_bindir}/foomatic-ppd-to-xml
%{_bindir}/foomatic-ppdfile
%{_bindir}/foomatic-printjob
%{_bindir}/foomatic-searchprinter
%{_sbindir}/*
%{perl_vendorlib}/Foomatic
%{_cups_serverbin}/driver/*
%{_mandir}/man1/foomatic-cleanupdrivers.1*
%{_mandir}/man1/foomatic-combo-xml.1*
%{_mandir}/man1/foomatic-compiledb.1*
%{_mandir}/man1/foomatic-configure.1*
%{_mandir}/man1/foomatic-datafile.1*
%{_mandir}/man1/foomatic-extract-text.1*
%{_mandir}/man1/foomatic-fix-xml.1*
%{_mandir}/man1/foomatic-nonumericalids.1*
%{_mandir}/man1/foomatic-perl-data.1*
%{_mandir}/man1/foomatic-ppd-options.1*
%{_mandir}/man1/foomatic-ppd-to-xml.1*
%{_mandir}/man1/foomatic-ppdfile.1*
%{_mandir}/man1/foomatic-printermap-to-gutenprint-xml.1*
%{_mandir}/man1/foomatic-printjob.1*
%{_mandir}/man1/foomatic-replaceoldprinterids.1*
%{_mandir}/man1/foomatic-searchprinter.1*
%{_mandir}/man8/*
%{_var}/cache/foomatic

%changelog
* Thu Feb 02 2023 Muhammad Falak <mwani@microsoft.com> - 4.0.13-17
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.0.13-16
- Initial CBL-Mariner import from Fedora 33 (license: MIT).

* Thu Nov 05 2020 Zdenek Dohnal <zdohnal@redhat.com> - 4.0.13-15
- rebuilt with new foomatic-db, use make

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.13-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 26 2020 Jitka Plesnikova <jplesnik@redhat.com> - 4.0.13-13
- Perl 5.32 re-rebuild of bootstrapped packages

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 4.0.13-12
- Perl 5.32 rebuild

* Tue May 26 2020 Zdenek Dohnal <zdohnal@redhat.com> - 4.0.13-11
- recognize fractial numbers in PageSize (backport from upstream)

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.13-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.13-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 4.0.13-8
- Perl 5.30 re-rebuild of bootstrapped packages

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 4.0.13-7
- Perl 5.30 rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.13-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 28 2019 Zdenek Dohnal <zdohnal@redhat.com> - 4.0.13-5
- rebuilt for new foomatic-db snapshot

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 4.0.13-3
- Perl 5.28 re-rebuild of bootstrapped packages

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 4.0.13-2
- Perl 5.28 rebuild

* Mon Mar 05 2018 Zdenek Dohnal <zdohnal@redhat.com> - 4.0.13-1
- 4.0.13

* Fri Mar 02 2018 Zdenek Dohnal <zdohnal@redhat.com> - 4.0.12-23
- 1549741 - foomatic: Partial build flags injection

* Wed Feb 28 2018 Zdenek Dohnal <zdohnal@redhat.com> - 4.0.12-22
- Rebuilt for new foomatic-db snapshot

* Mon Feb 19 2018 Zdenek Dohnal <zdohnal@redhat.com> - 4.0.12-21
- gcc is no longer in buildroot by default

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.12-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 03 2018 Zdenek Dohnal <zdohnal@redhat.com> - 4.0.12-19
- Rebuilt for new foomatic-db snapshot

* Tue Nov 07 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.0.12-18
- Remove old crufty coreutils requires

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.12-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.12-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 13 2017 Petr Pisar <ppisar@redhat.com> - 4.0.12-15
- perl dependency renamed to perl-interpreter
  <https://fedoraproject.org/wiki/Changes/perl_Package_to_Install_Core_Modules>

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 4.0.12-14
- Perl 5.26 re-rebuild of bootstrapped packages

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 4.0.12-13
- Perl 5.26 rebuild

* Thu May 04 2017 Zdenek Dohnal <zdohnal@redhat.com> - 4.0.12-12
- Rebuilt for new snapshot of foomatic-db

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.12-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Oct 13 2016 Zdenek Dohnal <zdohnal@redhat.com> - 4.0.12-10
- Rebuilt for new version of ghostscript-9.20 

* Tue Oct 04 2016 Zdenek Dohnal <zdohnal@redhat.com> - 4.0.12-9
- Rebuilt for new snapshot of foomatic-db

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 4.0.12-8
- Perl 5.24 re-rebuild of bootstrapped packages

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 4.0.12-7
- Perl 5.24 rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Nov 26 2015 Jiri Popelka <jpopelka@redhat.com> - 4.0.12-5
- BuildRequires python3-cups

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 4.0.12-3
- Perl 5.22 re-rebuild of bootstrapped packages

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 4.0.12-2
- Perl 5.22 rebuild

* Thu May 21 2015 Jiri Popelka <jpopelka@redhat.com> - 4.0.12-1
- 4.0.12

* Wed Dec 17 2014 Jiri Popelka <jpopelka@redhat.com> - 4.0.11-10
- Fix unowned dir /etc/foomatic (#1175224).

* Mon Dec  1 2014 Tim Waugh <twaugh@redhat.com> - 4.0.11-9
- Fix for upstream bug #1238 (bug #1163731).

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 4.0.11-8
- Perl 5.20 re-rebuild of bootstrapped packages

* Wed Sep 03 2014 Jitka Plesnikova <jplesnik@redhat.com> - 4.0.11-7
- Perl 5.20 rebuild

* Thu Aug 28 2014 Tim Waugh <twaugh@redhat.com> - 4.0.11-6
- Put some text into foomatic-preferred-drivers man page.

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 4.0.11-5
- Perl 5.20 rebuild

* Thu Aug 21 2014 Tim Waugh <twaugh@redhat.com> - 4.0.11-4
- Ship more manpages.

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Apr 28 2014 Jiri Popelka <jpopelka@redhat.com> - 4.0.11-1
- 4.0.11

* Sat Nov 30 2013 Jiri Popelka <jpopelka@redhat.com> - 4.0.9-8
- foomatic-rip's upstream moved from foomatic-filters to cups-filters-1.0.42

* Thu Nov 28 2013 Jiri Popelka <jpopelka@redhat.com> - 4.0.9-7
- Correct Obsoletes/Provides printer-filters (bug #1035450)

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 4.0.9-6
- Perl 5.18 re-rebuild of bootstrapped packages

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 4.0.9-4
- Perl 5.18 rebuild

* Mon Jun  3 2013 Tim Waugh <twaugh@redhat.com> - 4.0.9-3
- Obsolete/provide printer-filters package now it has gone (bug #967316).

* Tue May 28 2013 Tom Callaway <spot@fedoraproject.org> - 4.0.9-2
- remove Artistic test scripts from source tarball (bz 967406)

* Tue Mar 12 2013 Jiri Popelka <jpopelka@redhat.com> - 4.0.9-1
- 4.0.9

* Fri Feb 22 2013 Jiri Popelka <jpopelka@redhat.com> - 4.0.8-16
- Fix %%doc abuse (bug #914006).
- Fix bogus dates in changelog.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.8-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug 21 2012 Jiri Popelka <jpopelka@redhat.com> - 4.0.8-14
- Updated filters to 4.0.17

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.8-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 4.0.8-12
- Perl 5.16 re-rebuild of bootstrapped packages

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 4.0.8-11
- Perl 5.16 rebuild

* Wed May 30 2012 Jiri Popelka <jpopelka@redhat.com> - 4.0.8-10
- Updated filters to 4.0.15

* Tue Apr 10 2012 Tim Waugh <twaugh@redhat.com> - 4.0.8-9
- Use perl_bootstrap macro to allow for easier perl bootstrapping
  (bug #810542).

* Tue Mar 13 2012 Jiri Popelka <jpopelka@redhat.com> - 4.0.8-8
- Updated filters to 4.0.13

* Mon Mar  5 2012 Tim Waugh <twaugh@redhat.com> - 4.0.8-7
- Rebuilt to pick up new IEEE 1284 Device IDs.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 24 2011 Jiri Popelka <jpopelka@redhat.com> - 4.0.8-5
- Use _cups_serverbin macro from cups-devel instead of hard-coded /usr/lib/cups.
- No need to define BuildRoot and clean it in clean and install section anymore.
- Add argument for format in a debugging string (bug #726384).

* Thu Aug 18 2011 Tim Waugh <twaugh@redhat.com> - 4.0.8-4
- Another fix for CVE-2011-2924 (bug #726426).

* Thu Aug 18 2011 Tim Waugh <twaugh@redhat.com> - 4.0.8-3
- Use mktemp when creating debug log file in foomatic-rip
  (CVE-2011-2924, bug #726426).

* Wed Jul 27 2011 Petr Sabata <contyk@redhat.com> - 4.0.8-2
- Rebuild for perl5.14 (#725979)

* Mon Jul 25 2011 Jiri Popelka <jpopelka@redhat.com> - 4.0.8-1
- 4.0.8 (all patches merged upstream)

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 4.0.7-6
- Perl mass rebuild

* Wed Jul 20 2011 Tim Waugh <twaugh@redhat.com> - 4.0.7-5
- Fix improper sanitization of command line options (bug #721001,
  CVE-2011-2697).

* Thu Jun 16 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4.0.7-4
- Perl mass rebuild

* Mon Mar 07 2011 Richard Hughes <rhughes@redhat.com> - 4.0.7-3
- Added BR dbus-devel.

* Fri Mar 04 2011 Richard Hughes <rhughes@redhat.com> - 4.0.7-2
- Added colord support.

* Mon Feb 21 2011 Jiri Popelka <jpopelka@redhat.com> - 4.0.7-1
- 4.0.7

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Tim Waugh <twaugh@redhat.com> - 4.0.6-2
- Use perl_vendorlib macro instead of defining our own.

* Thu Dec 16 2010 Jiri Popelka <jpopelka@redhat.com> - 4.0.6-1
- 4.0.6

* Thu Dec  9 2010 Tim Waugh <twaugh@redhat.com> - 4.0.5-5
- Rebuilt for new device IDs.

* Fri Nov 26 2010 Tim Waugh <twaugh@redhat.com> - 4.0.5-4
- The pycups requirement is now python-cups.

* Fri Oct 15 2010 Tim Waugh <twaugh@redhat.com> - 4.0.5-3
- Removed hard-coded perl paths from spec file.

* Tue Oct  5 2010 Tim Waugh <twaugh@redhat.com> - 4.0.5-2
- Updated summary and description to more accurately reflect package
  contents (bug #630651).

* Wed Aug 18 2010 Jiri Popelka <jpopelka@redhat.com> - 4.0.5-1
- 4.0.5
- fixing of installation path for perl module is no longer needed

* Tue Jun 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 4.0.4-12
- Mass rebuild with perl-5.12.0

* Wed May  5 2010 Tim Waugh <twaugh@redhat.com> - 4.0.4-11
- Moved beh backend to main package.

* Sun Apr 25 2010 Tim Waugh <twaugh@redhat.com> - 4.0.4-10
- Rebuilt for new device IDs.

* Thu Apr 15 2010 Tim Waugh <twaugh@redhat.com> - 4.0.4-9
- Split out foomatic-filters sub-package.  Main package depends on it.

* Mon Apr 12 2010 Tim Waugh <twaugh@redhat.com> - 4.0.4-8
- Rebuilt for new device IDs (bug #575063).

* Thu Mar 18 2010 Tim Waugh <twaugh@redhat.com> - 4.0.4-4
- Package requires ghostscript (used by foomatic-rip).

* Wed Mar  3 2010 Tim Waugh <twaugh@redhat.com> - 4.0.4-3
- Removed old explicit provides for perl(Foomatic::GrovePath).
- Fixed macro in changelog.
- Avoid mixed spaces and tabs.
- Ship COPYING files.
- Added comments for sources.

* Thu Feb 25 2010 Tim Waugh <twaugh@redhat.com> - 4.0.4-2
- Make it explicit that the build requires foomatic-db.  This is
  needed for postscriptdriver tags.

* Tue Feb 16 2010 Jiri Popelka <jpopelka@redhat.com> - 4.0.4-1
- 4.0.4
- build no more requires ghostscript-devel
- removed foomatic-filters-int-options.patch

* Fri Feb  5 2010 Tim Waugh <twaugh@redhat.com> - 4.0.3-13
- Use relative, not absolute, symlink for CUPS driver.

* Fri Feb  5 2010 Tim Waugh <twaugh@redhat.com> - 4.0.3-12
- Another rebuild.

* Thu Feb  4 2010 Tim Waugh <twaugh@redhat.com> - 4.0.3-11
- Rebuild for postscriptdriver tags.

* Thu Jan 21 2010 Tim Waugh <twaugh@redhat.com> - 4.0.3-10
- Use Requires not PreReq (bug #225768).

* Tue Jan 19 2010 Tim Waugh <twaugh@redhat.com> - 4.0.3-9
- Fix for handling integer options (bug #531278).

* Tue Dec 15 2009 Tim Waugh <twaugh@redhat.com> - 4.0.3-8
- Really fixed installation path for perl module (bug #547696).

* Fri Dec  4 2009 Tim Waugh <twaugh@redhat.com> - 4.0.3-7
- Fixed installation path for perl module.

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 4.0.3-6
- rebuild against perl 5.10.1

* Tue Nov 10 2009 Tim Waugh <twaugh@redhat.com> 4.0.3-5
- Build requires cups.

* Tue Nov 10 2009 Tim Waugh <twaugh@redhat.com> 4.0.3-4
- Require cups and don't own its directories (bug #534051).

* Sun Nov  8 2009 Tim Waugh <twaugh@redhat.com> 4.0.3-3
- Revert last change.

* Thu Nov  5 2009 Tim Waugh <twaugh@redhat.com> 4.0.3-2
- Correctly build foomatic custom commands (bug #531278).

* Tue Sep  1 2009 Tim Waugh <twaugh@redhat.com> 4.0.3-1
- 4.0.3.

* Tue Aug 18 2009 Tim Waugh <twaugh@redhat.com> 4.0.2-6
- Split out foomatic-db into separate source package (bug #461234).

* Tue Aug  4 2009 Tim Waugh <twaugh@redhat.com> 4.0.2-5
- Use stcolor driver for Epson Stylus Color 200 (bug #513676).
- Don't ship 3-distribution symlink as CUPS already searches
  /usr/share/ppd (bug #514244).
- Remove non-PPD files from PPD directory (bug #514242).

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul  2 2009 Tim Waugh <twaugh@redhat.com> 4.0.2-3
- Removed '-O0' compiler option for foomatic-filters, which had been
  used for debugging purposes.

* Thu Jul  2 2009 Tim Waugh <twaugh@redhat.com> 4.0.2-1
- Updated db-engine to 4.0.2 (bug #503188).
- Updated foomatic-filters to 4.0.2 (bug #496521).
- Updated db-hpijs to 20090701.
- Updated db to 4.0-20090702.
- This package obsoletes oki4linux (bug #491489).
- Don't ship ChangeLog/README/USAGE for each of the 4 packages as it
  comes to more than 1MB (bug #492449).
- Don't use mktemp in foomatic-rip.

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 15 2009 Tim Waugh <twaugh@redhat.com> 4.0.0-1
- 4.0.0.

* Mon Jan 12 2009 Tim Waugh <twaugh@redhat.com> 3.0.2-70
- Major gutenprint version is 5.2.

* Sat Jan 10 2009 Tim Waugh <twaugh@redhat.com> 3.0.2-69
- Updated db-hpijs to 20090110.
- Updated db to 20090110.
- Updated filters to 3.0-20090110.
- Updated db-engine to 3.0-20090110.

* Thu Dec  4 2008 Tim Waugh <twaugh@redhat.com> 3.0.2-68
- Updated db-hpijs to 20081124.
- Updated db to 20081124.
- Updated filters to 3.0-20081124.
- Updated db-engine to 3.0-20081124.
- Better build root.
- Fixed summary.

* Thu Oct  2 2008 Tim Waugh <twaugh@redhat.com> 3.0.2-67
- Rebuilt (bug #465298).

* Fri Sep  5 2008 Tim Waugh <twaugh@redhat.com> 3.0.2-66
- Fixed filename handling in foomatic-rip (bug #457679).

* Thu Sep  4 2008 Tim Waugh <twaugh@redhat.com> 3.0.2-65
- Removed ampathxml and xml-cflags patches.
- Updated db-hpijs to 20080904.
- Updated db to 20080904.
- Updated filters to 3.0-20080904.
- Updated db-engine to 3.0-20080904.

* Wed Sep  3 2008 Tim Waugh <twaugh@redhat.com>
- Finally remove ppdload.

* Tue Sep  2 2008 Tim Waugh <twaugh@redhat.com> 3.0.2-64
- Fixed typo in HP-Color_LaserJet_9500_MFP.xml.

* Tue Sep  2 2008 Tim Waugh <twaugh@redhat.com> 3.0.2-63
- Avoid busy-looping when trying to shorten long PPD nicknames.

* Tue Sep  2 2008 Tim Waugh <twaugh@redhat.com> 3.0.2-62
- Removed patch fuzz.
- Fixed PPD generation for HP LaserJet 4345 MFP (bug #459847).

* Thu Jul 10 2008 Tim Waugh <twaugh@redhat.com> 3.0.2-61
- Updated db-hpijs to 20080710.
- Updated db to 20080710.
- Updated filters to 3.0-20080710.
- Updated db-engine to 3.0-20080710.
- Ship a defaultspooler file to avoid the need for spooler
  auto-detection (bug #454684).

* Thu May  8 2008 Tim Waugh <twaugh@redhat.com> 3.0.2-60
- Updated filters to 3.0-20080507.

* Wed May  7 2008 Tim Waugh <twaugh@redhat.com>
- Avoid busy-looping when the CUPS backend stops (bug #445555).

* Tue Apr  1 2008 Tim Waugh <twaugh@redhat.com> 3.0.2-59
- More foo2zjs printers removed (bug #438319).

* Thu Mar 13 2008 Tim Waugh <twaugh@redhat.com> 3.0.2-58
- Applied patch from upstream to make foomatic-rip clean up correctly when
  a job is cancelled.

* Mon Mar  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> 3.0.2-57
- rebuild for new perl (again)

* Wed Feb 13 2008 Tim Waugh <twaugh@redhat.com> 3.0.2-56
- Updated filters to 3.0-20080211.
- Updated db-hpijs to 20080211.
- Updated db-engine to 3.0-20080211.
- Updated db to 3.0-20080211.

* Sat Feb  2 2008 Tom "spot" Callaway <tcallawa@redhat.com> 3.0.2-55
- rebuild for new perl

* Thu Jan 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> 3.0.2-54
- rebuild for new perl
- correct license tag

* Wed Jan  9 2008 Tim Waugh <twaugh@redhat.com> 3.0.2-53
- Updated db-hpijs to 20071218.
- Updated db to 3.0-20071218.
- Updated db-engine to 3.0-20071218.
- Updated filters to 3.0-20071218 (bug #416881).

* Mon Jan  7 2008 Tim Waugh <twaugh@redhat.com>
- Removed foo2qpdl drivers and printers (bug #208851).

* Fri Oct 12 2007 Tim Waugh <twaugh@redhat.com> 3.0.2-52
- Removed use of printconf hooks.
- Don't restart CUPS on upgrade.

* Fri Sep 21 2007 Tim Waugh <twaugh@redhat.com> 3.0.2-51
- Build requires perl(ExtUtils::MakeMaker).
- Updated filters to 3.0-20070919.
- Updated db to 20070919.

* Wed Aug 15 2007 Tim Waugh <twaugh@redhat.com> 3.0.2-50
- Removed references to unshipped drivers:
  * drv_x125
  * ml85p
  * pbm2lxwl
  * pbmtozjs
  * bjc800j

* Thu Jun 14 2007 Tim Waugh <twaugh@redhat.com> 3.0.2-49
- Safe default margins for PPDs (bug #244161).
- Added missing IEEE 1284 ID for HP Photosmart 380 (bug #241352).

* Thu Jun 14 2007 Tim Waugh <twaugh@redhat.com> 3.0.2-48
- Updated db to 3.0-20070614.
- Updated db-engine to 3.0-20070614.
- Updated db-hpijs to 20070614.
- Updated filters to 3.0-20070614.

* Mon Apr 16 2007 Tim Waugh <twaugh@redhat.com> 3.0.2-47
- Fixed %%prep (bug #208851).
- Removed now-unused with_omni code.

* Fri Mar 30 2007 Tim Waugh <twaugh@redhat.com> 3.0.2-46
- Don't ship old gimp-print data (bug #234388).

* Thu Jan 11 2007 Tim Waugh <twaugh@redhat.com> 3.0.2-45
- Leave gutenprint-recommended printers alone, rather than pointing them
  to gimp-print as before.

* Tue Jan  9 2007 Tim Waugh <twaugh@redhat.com> 3.0.2-44
- Removed m2300w files (bug #203381).

* Fri Jan  5 2007 Tim Waugh <twaugh@redhat.com> 3.0.2-43
- Updated db to 3.0-20070105 (bug #214037, bug #191661, bug #198999,
  bug #191504, bug #187387, bug #188762, bug #170373, bug #221121,
  bug #214801).

* Thu Nov 30 2006 Tim Waugh <twaugh@redhat.com> 3.0.2-42
- Updated db to 3.0-20061130.

* Fri Nov 10 2006 Tim Waugh <twaugh@redhat.com> 3.0.2-41
- Updated db-engine to 3.0-20061109 (bug #197331).

* Tue Nov  7 2006 Tim Waugh <twaugh@redhat.com> 3.0.2-40
- Clean up gimp-print-ijs/gutenprint recommended drivers.
- Updated db-hpijs to 20061031.

* Fri Nov  3 2006 Tim Waugh <twaugh@redhat.com> 3.0.2-39
- Updated db-engine to 3.0-20061031.
- Updated db to 3.0-20061031.
- Remove references to foo2zjs and foo2oak (bug #208851).

* Thu Aug  3 2006 Tim Waugh <twaugh@redhat.com> 3.0.2-38
- Change a2ps requirement to mpage.
- Make CUPS driver work with drivers containing '-' in their names
  (bug #201398).

* Thu Jul 13 2006 Karsten Hopp <karsten@redhat.de> 3.0.2-37
- buildrequires autoconf, automake

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 3.0.2-36.1
- rebuild

* Mon May 22 2006 Karsten Hopp <karsten@redhat.de> 3.0.2-36
- add buildrequires ghostscript-devel so that /usr/lib/cups/driver/foomatic
  gets built

* Fri May 19 2006 Tim Waugh <twaugh@redhat.com> 3.0.2-35
- Define CUPS_PPDS for configure (bug #192375).

* Fri Apr 21 2006 Tim Waugh <twaugh@redhat.com>
- Updated db-engine to 3.0-20060421.

* Fri Mar 24 2006 Tim Waugh <twaugh@redhat.com> 3.0.2-34
- Always use /usr/lib/cups/{backend,filter}.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 3.0.2-33.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 3.0.2-33.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 18 2006 Tim Waugh <twaugh@redhat.com> 3.0.2-33
- Make build self-hosting.

* Tue Jan 17 2006 Tim Waugh <twaugh@redhat.com> 3.0.2-32
- Fix foomatic-cleanupdrivers.
- Updated db-engine to 3.0-20060117.
- Handle PPDs with default option values of '0'.

* Mon Jan 16 2006 Tim Waugh <twaugh@redhat.com> 3.0.2-31
- Fix tag mismatch in db.
- Updated db to 3.0-20060116.

* Tue Jan 10 2006 Tim Waugh <twaugh@redhat.com>
- Don't remove the cache directory, only its contents (bug #177266).

* Tue Jan  3 2006 Tim Waugh <twaugh@redhat.com> 3.0.2-30
- Updated db to 3.0-20060103.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Dec  9 2005 Tim Waugh <twaugh@redhat.com> 3.0.2-29
- Updated db-engine to 3.0-20051209.
- Updated db-hpijs to 1.5-20051209.
- Updated filters to 3.0-20051209.  No longer need rip-cvs patch.
- Updated db to 3.0-20051209.

* Tue Sep 13 2005 Tim Waugh <twaugh@redhat.com> 3.0.2-28
- Remove explicit perl module package dependencies.  These should be
  picked up by the RPM during the build process automatically anyway.
  Fixes bug #167997.

* Mon Sep 12 2005 Tim Waugh <twaugh@redhat.com> 3.0.2-27
- Own %%{_datadir}/foomatic/db/source/PPD/Custom and %%{_var}/cache/foomatic
  (bug #168085).

* Wed Sep  7 2005 Tim Waugh <twaugh@redhat.com> 3.0.2-26
- Updated db-engine to 3.0-20050907.
- Updated db to 3.0-20050907.

* Mon Sep  5 2005 Tim Waugh <twaugh@redhat.com> 3.0.2-25
- Add IEEE 1284 ID for HP LaserJet 4200 (bug #166638).
- Add IEEE 1284 ID for HP LaserJet 5000 (bug #167154).

* Thu Aug  4 2005 Tim Waugh <twaugh@redhat.com> 3.0.2-24
- Updated db to 3.0-20050804.
- No longer need hplj5 patch.
- Conflicts with system-config-printer before the parser bug was fixed.

* Tue Jul 26 2005 Tim Waugh <twaugh@redhat.com> 3.0.2-23
- Updated db to 3.0-20050726.
- No longer need ieee1284 patch.

* Mon Jul 25 2005 Tim Waugh <twaugh@redhat.com>
- Fix IEEE 1284 ID for HP Photosmart 7260 (bug #162915).

* Mon Jul 18 2005 Tim Waugh <twaugh@redhat.com> 3.0.2-22
- Updated db to 20050718.

* Sun Jul  3 2005 Tim Waugh <twaugh@redhat.com> 3.0.2-21
- Updated db to 20050703.

* Mon Jun 13 2005 Tim Waugh <twaugh@redhat.com> 3.0.2-20
- Updated db-hpijs to 1.5-20050613.
- Updated db to 20050613.

* Fri Jun 10 2005 Tim Waugh <twaugh@redhat.com>
- Add IEEE 1284 ID for Epson Stylus Photo 915 (bug #160030).
- Add IEEE 1284 ID for Ricoh Aficio 2228C PS (bug #160036).

* Tue Jun  7 2005 Tim Waugh <twaugh@redhat.com>
- Add IEEE 1284 ID for Epson Stylus Photo 870 (bug #159717).

* Wed May 25 2005 Tim Waugh <twaugh@redhat.com>
- Add IEEE 1284 ID for HP LaserJet 4250 (bug #157883).

* Thu May 19 2005 Tim Waugh <twaugh@redhat.com>
- Add IEEE 1284 ID for HP DeskJet 3845 (bug #157760).

* Tue May  3 2005 Tim Waugh <twaugh@redhat.com> 3.0.2-19
- Add IEEE 1284 ID for Epson Stylus CX5400 (bug #156661).

* Tue Apr 12 2005 Tim Waugh <twaugh@redhat.com>
- Fix Postscript driver (bug #151645).
- Add IEEE 1284 ID for HP DeskJet 5150 (bug #154518).
- Add IEEE 1284 ID for HP LaserJet 2420 (bug #114191).

* Thu Mar 24 2005 Tim Waugh <twaugh@redhat.com>
- Add a hook to remove any foomatic data cached by system-config-printer.

* Thu Mar 10 2005 Tim Waugh <twaugh@redhat.com> 3.0.2-18
- Updated db to 20050310.

* Wed Mar  9 2005 Tim Waugh <twaugh@redhat.com> 3.0.2-17
- Make Omni optional.
- ... and disable it.

* Wed Mar  2 2005 Tim Waugh <twaugh@redhat.com> 3.0.2-16
- Rebuild for new GCC.

* Fri Feb 25 2005 Tim Waugh <twaugh@redhat.com>
- Add IEEE 1284 information for Lexmark Optra R+ (bug #149498).

* Thu Feb 17 2005 Tim Waugh <twaugh@redhat.com> 3.0.2-15
- Fixed warning patch.

* Wed Feb 16 2005 Tim Waugh <twaugh@redhat.com>
- Don't ship backup files.

* Wed Feb 16 2005 Tim Waugh <twaugh@redhat.com> 3.0.2-14
- Updated db to 20050216.

* Thu Feb 10 2005 Tim Waugh <twaugh@redhat.com>
- Added IEEE 1284 information for HP Color LaserJet 4600 (bug #147648).

* Tue Feb  8 2005 Tim Waugh <twaugh@redhat.com>
- Corrected IEEE 1284 information for HP DeskJet 6540 (bug #147288).
- Added IEEE 1284 information for Epson Stylus C82 (bug #147230).

* Mon Jan 24 2005 Tim Waugh <twaugh@redhat.com>
- Fixed last change.

* Fri Jan 21 2005 Tim Waugh <twaugh@redhat.com>
- Prevent a warning from DB.pm (bug #145605).

* Tue Jan 18 2005 Tim Waugh <twaugh@redhat.com> 3.0.2-13
- Updated db to 20050118.

* Mon Jan 10 2005 Tim Waugh <twaugh@redhat.com>
- Added IEEE 1284 information for Epson Stylus Photo R200 (bug #144631).

* Tue Jan  4 2005 Tim Waugh <twaugh@redhat.com>
- Added IEEE 1284 information for Okidata Okipage 6ex (bug #143964).
- Added IEEE 1284 information for Epson Stylus Photo R300 (bug #143939).

* Mon Dec 20 2004 Tim Waugh <twaugh@redhat.com> 3.0.2-12
- Added IEEE 1284 information for Epson Stylus CX3200 (bug #143343).

* Mon Dec  6 2004 Tim Waugh <twaugh@redhat.com> 3.0.2-11
- Updated db to 20041206.

* Thu Dec  2 2004 Tim Waugh <twaugh@redhat.com> 3.0.2-10
- Added IEEE 1284 information for HP-Color_Inkjet_Printer_CP1700 (bug #141594).
- Added IEEE 1284 information for Samsung-ML-1710 (bug #141163).
- Added IEEE 1284 information for HP-OfficeJet_G95 (bug #141057).

* Wed Nov 24 2004 Tim Waugh <twaugh@redhat.com> 3.0.2-9
- Updated db to 20041124.
- Updated hpijs-db to 1.5-20041124.
- No longer need HP DJ 6122 patch.
- No longer need ieee1284 patch.
- Updated Omni-printers to 0.9.2.

* Wed Nov 24 2004 Tim Waugh <twaugh@redhat.com> 3.0.2-8
- Minor PPD.pm fix for PPD import (bug #132625).

* Mon Nov 22 2004 Tim Waugh <twaugh@redhat.com> 3.0.2-7
- Applied some foomatic-rip fixes from CVS.

* Thu Nov 18 2004 Tim Waugh <twaugh@redhat.com>
- Add autodetect information for HP Color LaserJet 4550 (bug #139799).

* Wed Nov 17 2004 Tim Waugh <twaugh@redhat.com> 3.0.2-6
- Add autodetect information for HP LaserJet 8150 (bug #139683).
- Add autodetect information for Epson Stylus Color 777 (bug #139629).

* Tue Nov 16 2004 Tim Waugh <twaugh@redhat.com> 3.0.2-5
- Ship data as non-executable (bug #139271).
- Corrected autodetect information for HP Business InkJet 1100 (bug #139258).

* Mon Nov 15 2004 Tim Waugh <twaugh@redhat.com> 3.0.2-4
- Add autodetect information for HP Business InkJet 1100 (bug #139258).
- Add autodetect information for Epson Stylus Photo 790 (bug #139266).
- Add autodetect information for HP DJ 3820 (bug #139271).

* Wed Oct 13 2004 Tim Waugh <twaugh@redhat.com> 3.0.2-3
- Revert change for bug #133647.

* Mon Oct 11 2004 Tim Waugh <twaugh@redhat.com> 3.0.2-2
- Use gimp-print driver for HP 2000C (bug #133647).
- Add autodetect information for Lexmark Z52 (bug #135178).

* Thu Oct  7 2004 Tim Waugh <twaugh@redhat.com>
- Add autodetect information for HP DJ 640C (bug #134912).

* Fri Sep 24 2004 Tim Waugh <twaugh@redhat.com> 3.0.2-1
- Updated filters to 3.0.2.
- Updated db-engine to 3.0.2.
- No longer need Omni PageSize patch or lvalue patch.

* Tue Aug 31 2004 Tim Waugh <twaugh@redhat.com> 3.0.1-11
- Add autodetect information for Brother HL-5050 (bug #131220).

* Fri Aug 13 2004 Tim Waugh <twaugh@redhat.com> 3.0.1-10
- Add autodetect information for HP LJ 2200 (bug #129732).

* Thu Aug  5 2004 Tim Waugh <twaugh@redhat.com>
- Add autodetect information for HP DJ 1220.

* Tue Jul 27 2004 Tim Waugh <twaugh@redhat.com> 3.0.1-9
- Rebuilt.

* Wed Jul 21 2004 Tim Waugh <twaugh@redhat.com> 3.0.1-8
- Add autodetect information for HP DJ 6122 (bug #124629).

* Tue Jul 20 2004 Tim Waugh <twaugh@redhat.com> 3.0.1-7
- Updated gimp-print data to 4.2.7.

* Mon Jul 12 2004 Tim Waugh <twaugh@redhat.com> 3.0.1-6
- Updated db to 20040712.
- HPLJ4300 data is upstream now.

* Thu Jun 24 2004 Tim Waugh <twaugh@redhat.com> 3.0.1-5
- SNMP/IEEE 1284 data for HPLJ4300.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  1 2004 Tim Waugh <twaugh@redhat.com>
- Build requires a2ps, because foomatic-filters checks for a conversion
  utility (bug #124931).

* Mon Apr 19 2004 Tim Waugh <twaugh@redhat.com> 3.0.1-3
- Require appropriate perl(:MODULE_COMPAT_...) symbol (bug #121131).

* Wed Mar 10 2004 Tim Waugh <twaugh@redhat.com>
- Fix deprecated cast-as-lvalues.

* Thu Mar  4 2004 Tim Waugh <twaugh@redhat.com> 3.0.1-2
- Fix Omni PageSize problem (bug #115586).

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb 19 2004 Tim Waugh <twaugh@redhat.com> 3.0.1-1
- Upgrade db to 20040219.
- Upgrade hpijs to 1.5-20040219.
- Upgrade engine to 3.0.1.
- Upgrade filters to 3.0.1.

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Feb  9 2004 Tim Waugh <twaugh@redhat.com> 3.0.0-23
- Fix up HP Color Inkjet CP1700 support.
- Remove PrintoutMode option from gimp-print driver to avoid breaking it.
- Update filters to 3.0.1rc3.
- Update engine to 3.0.1rc2
- No long need symlink patch.

* Mon Jan 12 2004 Tim Waugh <twaugh@redhat.com> 3.0.0-22
- Updated Omni printers to 0.9.1 again.

* Mon Jan 12 2004 Tim Waugh <twaugh@redhat.com> 3.0.0-21
- Build for Fedora Core 1 printer drivers update.
- Revert Omni update temporarily.
- Downgrade engine to 20031217 to stick to the stable branch.

* Mon Jan 12 2004 Tim Waugh <twaugh@redhat.com> 3.0.0-20
- Updated Omni printers to 0.9.1.

* Mon Jan 12 2004 Tim Waugh <twaugh@redhat.com> 3.0.0-19
- Build for Fedora Core 1 printer drivers update.
- No longer need symlink patch.
- Updated fontpath patch.
- Updated engine to 20040112.
- Updated db to 20040112.
- Updated gimp-print data to 4.2.6.

* Tue Jan  6 2004 Tim Waugh <twaugh@redhat.com> 3.0.0-18
- Build for Fedora Core 1 printer drivers update.
- Explicitly state conflict with hpijs < 1.5.
- Make foomatic-ppdfile accept '-t type' like foomatic-datafile used to.

* Tue Dec 23 2003 Tim Waugh <twaugh@redhat.com> 3.0.0-17
- Fix up gimp-print XML (bug #112574).

* Fri Dec 19 2003 Tim Waugh <twaugh@redhat.com> 3.0.0-16
- Need the ppd driver too.

* Fri Dec 19 2003 Tim Waugh <twaugh@redhat.com> 3.0.0-15
- Reinstate ppdload long enough for me to work around its disappearance.

* Thu Dec 18 2003 Tim Waugh <twaugh@redhat.com>
- Updated db to 20031218.
- No longer need hpdj656, dell, mc3100 patches.

* Wed Dec 17 2003 Tim Waugh <twaugh@redhat.com> 3.0.0-14
- Updated db to 20031217.
- Updated engine to 20031217.
- Updated hpijs to 1.5-20031217.
- Use relative symlinks.

* Fri Dec 12 2003 Tim Waugh <twaugh@redhat.com> 3.0.0-13
- Add Minolta magicolor 3100.

* Tue Dec  2 2003 Tim Waugh <twaugh@redhat.com>
- Don't ship backup files.

* Sat Nov 29 2003 Tim Waugh <twaugh@redhat.com> 3.0.0-12
- Undo over-zealous percent escaping in PostScript.xml
- Build requires libxml2-devel (bug #110589).
- Use relative, not absolute, symlink for CUPS filter.

* Fri Nov  7 2003 Tim Waugh <twaugh@redhat.com> 3.0.0-11
- Add pxlmono driver for HP LaserJet 5 (bug #109378).

* Wed Nov  5 2003 Tim Waugh <twaugh@redhat.com> 3.0.0-10
- Updated db to 20031105.
- Drop filters path patch.
- Updated fontpath patch, both libdir patches.
- Updated engine and filters to 3.0-20031105.
- Updated hpijs db to 1.4-1.

* Mon Oct 27 2003 Tim Waugh <twaugh@redhat.com> 3.0.0-9
- Recommend omni-compiled for Omni drivers (bug #107965).

* Mon Sep 29 2003 Tim Waugh <twaugh@redhat.com>
- No longer requires Date::Manip (bug #105696).

* Thu Sep  4 2003 Tim Waugh <twaugh@redhat.com> 3.0.0-8
- Build requires latest perl (bug #103630).

* Tue Aug  5 2003 Elliot Lee <sopwith@redhat.com> 3.0.0-7
- Fix install to find perl modules

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  3 2003 Jeff Johnson <jbj@redhat.com>
- add explicit epoch's where needed.

* Tue Jun  3 2003 Tim Waugh <twaugh@redhat.com> 3.0.0-5
- Add some Dell printers.
- Updated foomatic-db to 20030603.
- Updated missing UPP list for ghostscript 7.07.

* Wed May 21 2003 Tim Waugh <twaugh@redhat.com> 3.0.0-4
- Fix some printer models whose recommended driver is not shipped
  (bug #89455).

* Mon May 19 2003 Tim Waugh <twaugh@redhat.com> 3.0.0-3
- Relax perl requirement.  Rebuild for perl 5.8.0.

* Mon May 19 2003 Tim Waugh <twaugh@redhat.com> 3.0.0-2
- Disable the xmltest during configure (it hangs on ppc).
- Requires newer perl (bug #91129).

* Wed Apr 30 2003 Tim Waugh <twaugh@redhat.com> 3.0.0-1
- 3.0.0.

* Fri Apr  4 2003 Tim Waugh <twaugh@redhat.com>
- Update Omni printers to 0.9.0.

* Wed Apr  2 2003 Tim Waugh <twaugh@redhat.com> 3.0.0-0.beta2.1
- 3.0.0beta2.
- Updated path patch.
- No longer need FOOMATIC_LIBDIR, generic PS, ids, postscript-duplex,
  hpijs13, psc2210, duplex184 patches.
- Add hpijs support back in.
- Fix up references to old printer IDs.

* Wed Mar 26 2003 Tim Waugh <twaugh@redhat.com> 2.0.2-18
- Fix PS/PJL conflicts in Duplex options (bug #86510).

* Fri Mar 21 2003 Tim Waugh <twaugh@redhat.com> 2.0.2-17
- Update Omni printers to 0.7.3.

* Wed Mar 19 2003 Tim Waugh <twaugh@redhat.com> 2.0.2-16
- Add autodetect info for HP PSC 2210.

* Tue Feb  4 2003 Tim Waugh <twaugh@redhat.com> 2.0.2-15
- Update data-generators to CVS.

* Thu Jan 30 2003 Tim Waugh <twaugh@redhat.com> 2.0.2-14
- Use hpijs, not hpijs-rss (we don't ship the RSS patch now).

* Thu Jan 23 2003 Tim Waugh <twaugh@redhat.com> 2.0.2-13
- Pacify printers that don't understand duplex (bug #82385).

* Wed Jan 22 2003 Tim Powers <timp@redhat.com> 2.0.2-12
- rebuilt

* Tue Jan 21 2003 Tim Waugh <twaugh@redhat.com> 2.0.2-11
- Add autodetect info for HP DeskJet 656C.  It doesn't really do
  IEEE 1284 IDs, but since it's a USB device we can figure out its
  manufacturer and model anyway.

* Thu Jan  9 2003 Tim Waugh <twaugh@redhat.com> 2.0.2-10
- Set GS_FONTPATH in gs wrapper (bug #81410).

* Sat Jan  4 2003 Jeff Johnson <jbj@redhat.com> 2.0.2-9
- use internal dep generator.

* Sun Dec 15 2002 Tim Waugh <twaugh@redhat.com> 2.0.2-8
- Add several device IDs.

* Sat Dec 14 2002 Tim Waugh <twaugh@redhat.com> 2.0.2-7
- Update Omni printers to 0.7.2.
- No longer need Omni badxml patch.

* Sat Dec 14 2002 Tim Powers <timp@redhat.com> 2.0.2-6
- don't use rpms internal dep generator

* Fri Dec  6 2002 Tim Waugh <twaugh@redhat.com> 2.0.2-5
- Omni XML wasn't well-formed.

* Wed Nov 20 2002 Tim Waugh <twaugh@redhat.com> 2.0.2-4
- Update gimp-print data.
- Add 'generic postscript' model.

* Mon Nov 11 2002 Tim Waugh <twaugh@redhat.com> 2.0.2-3
- Update Omni printers to 0.7.1.

* Tue Oct 22 2002 Tim Waugh <twaugh@redhat.com> 2.0.2-2
- Fix file manifest for perl modules.
- Add autodetect information for HP DeskJet 990C.

* Mon Oct 21 2002 Tim Waugh <twaugh@redhat.com> 2.0.2-1
- 2.0.2.
- No longer need 67973, 970c patches.
- Remove cups-drivers-* packages (no longer needed).
- Remove files not shipped.  Ship filter.conf.
- Conditionally restart cups.
- Use libdir.
- Don't put things in site_perl; use vendor_perl instead (bug #73528).

* Fri Aug  9 2002 Tim Waugh <twaugh@redhat.com> 1.9-1.20020617.6
- Fix autodetect information for HPDJ970C.

* Thu Aug  8 2002 Tim Waugh <twaugh@redhat.com> 1.9-1.20020617.5
- For gimp-print, use the Ghostscript stp driver in preference to the
  IJS interface.

* Thu Jul 25 2002 Tim Waugh <twaugh@redhat.com> 1.9-1.20020617.4
- Quieten scriptlets.

* Fri Jul  5 2002 Tim Waugh <twaugh@redhat.com> 1.9-1.20020617.3
- Fix autodetect information for HPLJ2100/2100M.

* Fri Jun 21 2002 Tim Powers <timp@redhat.com> 1.9-1.20020617.2
- automated rebuild

* Wed Jun 19 2002 Tim Waugh <twaugh@redhat.com> 1.9-0.20020617.2
- Omni 0.7.0 printers.

* Mon Jun 17 2002 Tim Waugh <twaugh@redhat.com> 1.9-0.20020617.1
- Update to CVS.
- Remove some more explicit perl dependencies that are picked up
  automatically.

* Wed May 29 2002 Tim Waugh <twaugh@redhat.com> 1.9-0.20020517.3
- Remove explicit perl-Storable dependency; it should be perl(Storable),
  and that is picked up automatically.

* Tue May 28 2002 Tim Waugh <twaugh@redhat.com> 1.9-0.20020517.2
- Fix release number.
- Drop gen-ppds from the file manifest---use foomatic-compiledb instead
  (bug #63622).

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Waugh <twaugh@redhat.com> 1.9-0.20020517.1
- Remove ghostscript UPP drivers that are gone in 7.05.

* Sat May 18 2002 Tim Waugh <twaugh@redhat.com> 1.9-0.20020517.0.1
- Update to CVS.
- Updated requirements.
- Updated path and libdir patches.
- Drop hpijs 1.0.2 patch.
- foomatic-datafile has moved to %%{_bindir}.
- Update gimp-print data to 4.2.1.
- Update Omni printer data to 0.6.1.

* Thu Apr  4 2002 Tim Waugh <twaugh@redhat.com> 1.1-0.20020313.3
- Fix the hpijs option data too (bug #62587).

* Wed Apr  3 2002 Tim Waugh <twaugh@redhat.com> 1.1-0.20020313.2
- Back off to 1.0.2 for hpijs driver data (bug #62587).

* Thu Mar 14 2002 Tim Waugh <twaugh@redhat.com> 1.1-0.20020313.1
- Update to CVS.

* Wed Mar  6 2002 Tim Waugh <twaugh@redhat.com> 1.1-0.20020306.1
- Update to CVS.
- Patches no longer needed: conffile, sys, cachedir, fd0.
- Adapted path patch.

* Tue Mar  5 2002 Tim Waugh <twaugh@redhat.com> 1.1-0.20020130.10
- Fix bug #58319.
- Drop dbg patch.

* Mon Feb 25 2002 Tim Waugh <twaugh@redhat.com> 1.1-0.20020130.9
- Fix file lists.

* Mon Feb 25 2002 Tim Waugh <twaugh@redhat.com> 1.1-0.20020130.8
- Fix %%post scriplet bug (bug #59942).

* Thu Feb 21 2002 Tim Waugh <twaugh@redhat.com> 1.1-0.20020130.7
- Rebuild in new environment.

* Wed Feb 13 2002 Tim Waugh <twaugh@redhat.com> 1.1-0.20020130.6
- Merge cups-drivers.  No epoch needed.
- Require perl-URI.

* Wed Feb 06 2002 Tim Waugh <twaugh@redhat.com> 1.1-0.20020130.5
- Cache fix.

* Mon Feb  4 2002 Tim Waugh <twaugh@redhat.com> 1.1-0.20020130.4
- Don't ship backup files.

* Mon Feb  4 2002 Tim Waugh <twaugh@redhat.com> 1.1-0.20020130.3
- Rebuild to pick up new perl installsitelib.

* Thu Jan 31 2002 Tim Waugh <twaugh@redhat.com> 1.1-0.20020130.2
- Fix a thinko in DB.pl.

* Wed Jan 30 2002 Tim Waugh <twaugh@redhat.com> 1.1-0.20020130.1
- Update to CVS.
- No longer need the cachedir patch.
- Fix config file path.
- Look in /usr/local/bin last, not first, in lpdomatic (bug #57915).

* Tue Jan 29 2002 Tim Waugh <twaugh@redhat.com> 1.1-0.20020129.1
- Update to CVS.
- Patches no longer needed: prepend, fd3.
- Use RPM_OPT_FLAGS.
- Allow non-root users to use foomatic-datafile (bug #58956).

* Sat Jan 26 2002 Jeff Johnson <jbj@redhat.com> 1.1-0.20020124.2
- added Provides: perl(Foomatic::GrovePath)

* Thu Jan 24 2002 Tim Waugh <twaugh@redhat.com> 1.1-0.20020124.1
- Update to CVS.
- Updated Omni printers to those in Omni 0.5.1.
- Updated patches: prepend, fd3.
- Patches no longer needed: utf8, lpdomatic.
- Added gimp-print (formerly stp) foomatic db info, and removed the old
  stp.xml file.
- Conflict with ghostscript if it doesn't have gimp-print-4.2.0 yet.

* Fri Jan 18 2002 Tim Waugh <twaugh@redhat.com> 1.1-0.20011218.2
- REALLY fix PCL fixup code (bug #55909, others).
- PreReq fileutils, initscripts (bug #56984).
- Fix prepends in lpdomatic (bug #57371).
- Run foomatic-cleanupdrivers during install, to remove driver entries
  with no command line.
- Put lpdomatic in /usr/sbin again.
- Fix foomatic-gswrapper's file descriptor manipulations (bug #56871).

* Mon Dec 17 2001 Crutcher Dunnavant <crutcher@redhat.com> 1.1-0.20011218.1
- re-imported from upstream to fix some perl fixup code on pcl printers.

* Mon Dec 17 2001 Crutcher Dunnavant <crutcher@redhat.com> 1.1-0.20011217.2
- fix the rest of the quoting issues with foomatic-combo-xml with the patch
- foomatic-1.1-20011217-quotes.patch. This has been sent upstream.

* Mon Dec 17 2001 Crutcher Dunnavant <crutcher@redhat.com> 1.1-0.20011217.1
- respin to pull in latest foomatic database, fixes:
  - properly use the cache in relation to foomatic-combo-xml's output
  - fix _some_ of the quoting issues with calling foomatic-combo-xml

* Wed Dec  5 2001 Crutcher Dunnavant <crutcher@redhat.com> 1.1-0.20011205.1
- respin to pull in latest foomatic database, fixes:
  - droping half of a large job
  - -Mutf8 added to the upstream filters
  - miscelaneous printer db updates

* Thu Nov 29 2001 Crutcher Dunnavant <crutcher@redhat.com> 1.1-0.20011018.8
- added Requires: fileutils for the 'rm' in post

* Mon Nov 26 2001 Crutcher Dunnavant <crutcher@redhat.com> 1.1-0.20011018.7
- /var/chache => /var/cache, doh!

* Fri Nov 16 2001 Nalin Dahyabhai <nalin@redhat.com> 1.1-0.20011018.6
- fix %%post scriptlet

* Tue Nov 13 2001 Crutcher Dunnavant <crutcher@redhat.com> 1.1-0.20011018.5
- changed the patch to use the -Mutf8 command line option,
- and to restart the printserver, after rebuilding the settings.

* Fri Nov  9 2001 Crutcher Dunnavant <crutcher@redhat.com> 1.1-0.20011018.4
- grumble. Some drivers use inline perl scripts, and need the 'use utf8;'
- pragma. Without it, they break on _some_ of their options.

* Wed Oct 31 2001 Crutcher Dunnavant <crutcher@redhat.com> 1.1-0.20011018.3
- patched lpdomatic to prepend PostScript options in the _right_ place.

* Thu Oct 25 2001 Crutcher Dunnavant <crutcher@redhat.com> 1.1-0.20011018.2
- zap the foomatic cache on install

* Thu Oct 18 2001 Crutcher Dunnavant <crutcher@redhat.com> 1.1-0.20011018.1
- rolled to pull in latest information.
- added Omni printers to the printer list.

* Fri Oct 05 2001 Crutcher Dunnavant <crutcher@redhat.com> 1.1-0.20011005.1
- rolled to pull in an ia64 fix to foomatic-combo-xml.c

* Mon Oct 01 2001 Crutcher Dunnavant <crutcher@redhat.com> 1.1-0.20011001.1
- rolled to pull in foomatic fixes to foomatic-combo-xml.c

* Wed Sep 05 2001 Crutcher Dunnavant <crutcher@redhat.com> 1.1-0.20010905.1
- upgraded to latest foomatic, we now have fast overview generation!
- this means that there is no prebuilt overview file.

* Tue Aug 28 2001 Crutcher Dunnavant <crutcher@redhat.com> 1.1-0.20010828.1
- WOW! The latest foomatic uses Till Kamppeter's C based combo compiler.
- It is now fast enough that there is no real benifit to precompiling.
- NOTE: this forces the package to stop being noarched.

* Mon Aug 27 2001 Crutcher Dunnavant <crutcher@redhat.com> 1.1-0.20010827.1
- fresh pull, maybe it fixes the build errors.

* Sat Aug 25 2001 Crutcher Dunnavant <crutcher@redhat.com> 1.1-0.20010825.1
- did a fresh database pull, which contains the old japanese printers as well.
- removed japanese hack.

* Tue Aug 14 2001 Akira TAGOH <tagoh@redhat.com> 1.1-0.20010717.5
- Add Japanese printer entry.

* Mon Aug  6 2001 Crutcher Dunnavant <crutcher@redhat.com> 1.1-0.20010717.4
- move the cache back to /var, sigh.

* Mon Jul 23 2001 Crutcher Dunnavant <crutcher@redhat.com> 1.1-0.20010717.2
- made foomatic pre-compute its db

* Wed Jul 18 2001 Crutcher Dunnavant <crutcher@redhat.com> 1.1-0.20010717.1
- imported from mandrake.

* Tue Jul 17 2001 Till Kamppeter <till@mandrakesoft.com> 1.1-0.20010717mdk
- Added job listing/removal/manipulation and queue control to
  foomatic-printjob
- Support for printing multiple copies with PDQ

* Sat Jul 14 2001 Till Kamppeter <till@mandrakesoft.com> 1.1-0.20010714mdk
- Included the cupsomatic filter script
- When a queue is set up, default options can be set now
- Help messages of foomatic-configure and foomatic-printjob cleaned up.

* Fri Jul 13 2001 Till Kamppeter <till@mandrakesoft.com> 1.1-0.20010713mdk
- Many bugfixes in "foomatic-printjob".
- "foomatic-configure" adds the Foomatic config file directory automatically
  to the search paths of PDQ.
- Printing a help page under PDQ was broken.

* Thu Jul 12 2001 Stefan van der Eijk <stefan@eijk.nu> 1.1-0.20010712mdk
- BuildRequires: perl-devel

* Wed Jul 11 2001 Till Kamppeter <till@mandrakesoft.com> 1.1-0.20010711mdk
- initial release.
- Deleted the obsolete drivers "stp", "cZ11", and "hpdj".
- Patch applied which flushes the memory cache regularly, otherwise
  foomatic-configure would hang when the Foomatic data of GIMP-Print is
  installed. 
