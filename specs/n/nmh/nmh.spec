# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:          nmh
Version:       1.8
Release:       9%{?dist}
Summary:       A capable MIME-email-handling system with a command-line interface
# Automatically converted from old format: BSD - review is highly recommended.
License:       LicenseRef-Callaway-BSD
URL:           https://savannah.nongnu.org/projects/nmh
Source0:       https://download-mirror.savannah.gnu.org/releases/%{name}/%{name}-1.8.tar.gz
Patch0:        nmh-use-smtp-port.patch
BuildRequires: cyrus-sasl-devel
BuildRequires: gcc
BuildRequires: gdbm-devel
BuildRequires: libcurl-devel
BuildRequires: make
BuildRequires: ncurses-devel
BuildRequires: openssl-devel
BuildRequires: readline-devel
BuildRequires: w3m
Requires:      w3m
Suggests:      %{_bindir}/vi
Suggests:      %{_sbindir}/sendmail
# pick also provides /usr/bin/pick and its man page, Bug 2027139
Conflicts:     pick
# scalasca also provides /usr/bin/scan and its man page
Conflicts:     scalasca

%description
nmh is a collection of single-purpose programs that send, receive,
show, search, and otherwise manipulate emails, including MIME.
They combine well with other Unix programs, easing the development
of custom shorthand commands as shell scripts.
Optional GUI interfaces are provided by the external xmh and exmh
projects.  nmh is a descendant of the RAND MH, Mail Handler, project.

%prep
%setup -q -n %{name}-1.8
%patch -P 0 -p1

# Avoid regenerating autotools machinery.
touch aclocal.m4 Makefile.in config.h.in configure

%build
CFLAGS="$RPM_OPT_FLAGS"
%configure
%make_build

%install
%make_install INSTALL="install -p"

%files
%{_bindir}/*
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/*
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/*
%{_mandir}/man[8751]/*
%doc %{_pkgdocdir}/*

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Sep  2 2024 Miroslav Suchý <msuchy@redhat.com> - 1.8-7
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jul 30 2023 David Levine  <par.packager@gmail.com> - 1.8-3
- Replaced deprecated patch0 with patch -P 0.

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Feb 18 2023 David Levine  <par.packager@gmail.com> - 1.8-1
- With upstream 1.8.

* Sun Feb  5 2023 David Levine  <par.packager@gmail.com> - 1.8RC3-1
- With upstream 1.8-RC3.

* Sat Jan 21 2023 David Levine  <par.packager@gmail.com> - 1.8RC2-1
- With upstream 1.8-RC2.

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.8RC1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Jan  1 2023 David Levine  <par.packager@gmail.com> - 1.8RC1-1
- With upstream 1.8-RC1.

* Wed Dec  7 2022 Florian Weimer <fweimer@redhat.com> - 1.7.1-19
- Backport patch from upstream to fix detection of _GNU_SOURCE

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Dec 18 2021 David Levine  <par.packager@gmail.com> - 1.7.1-16
- Added Conflicts:pick to support new pick package.

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 1.7.1-15
- Rebuilt with OpenSSL 3.0.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Nov  4 2020 David Levine  <par.packager@gmail.com> - 1.7.1-12
- Added BuildRequires: make.

* Sun Aug  9 2020 David Levine  <par.packager@gmail.com> - 1.7.1-11
- Replaced ='s in changelog with -'s.

* Tue Jul 28 2020 David Levine  <par.packager@gmail.com> - 1.7.1-10
- Replace make invocations with macros.

* Tue Jul 28 2020 David Levine  <par.packager@gmail.com> - 1.7.1-9
- Updated BuildRequires to use gdbm-devel instead of libdb-devel.

- It would use gdbm if it was installed anyway.  This allows nmh to
  be removed from Bug 1361971.

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.7.1-5
- Rebuild for readline 8.0

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Apr 04 2018 Bryan Wright <bkw1a@virginia.edu> 1.7.1-2
- Changed default send port from 587 back to original 25.

* Wed Apr 04 2018 David Levine  <par.packager@gmail.com>
- Changed Requires of vi and sendmail to Suggests.
- Removed explicit Requires of libcurl, and some explicit BuildRequires,
  because they are implied by others.

* Wed Mar 07 2018 David Levine  <par.packager@gmail.com> 1.7.1-1
- Updated nmh to 1.7.1.

* Thu Mar 01 2018 David Levine  <par.packager@gmail.com> 1.7-6
- Changed /bin/vi to /usr/bin/vi, hoping that will fix the F28 build.

* Mon Feb 19 2018 David Levine  <par.packager@gmail.com> 1.7-5
- Added libcurl and libcurl-devel BuildRequires to enable OAuth support.
- Added BuildRequires: gcc.

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.7-4
- Escape macros in %%changelog

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Nov 26 2017 David Levine  <par.packager@gmail.com> 1.7-2
- Removed configure --sysconfdir to fix /etc/nmh/ install dir.
- Removed autoconf dependencies because autoreconf is no longer used.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 30 2017 David Levine <par.packager@gmail.com> 1.6-11
- Added automake dependency.

* Sun Jan 29 2017 David Levine <par.packager@gmail.com> 1.6-10
- Added autoreconf because nmh uses unsupported automake version.

* Thu Jan 12 2017 David Levine <levinedl@acm.org> 1.6-9
- Patched configure.ac to look for SSL_new() instead of SSL_library_init().

* Thu Jan 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.6-8
- Rebuild for readline 7.x

* Tue Sep 27 2016 David Levine <levinedl@acm.org> 1.6-7
- Try libdb instead of db4.

* Tue Sep 27 2016 David Levine <levinedl@acm.org> 1.6-7
- Removed autoreconf its dependencies.

* Tue Sep 27 2016 David Levine <levinedl@acm.org> 1.6-6
- Need autoconf268.

* Tue Sep 27 2016 David Levine <levinedl@acm.org> 1.6-6
- That should have been db4{,-devel} instead of libdb4{,-devel}.

* Tue Sep 27 2016 David Levine <levinedl@acm.org> 1.6-6
- Use libdb4{,-devel} on EPEL6.

* Mon Feb 22 2016 David Levine <levinedl@acm.org> 1.6-6
- Added build dependency on w3m, and changed Requires to be on that package.

* Sun Feb 21 2016 David Levine <levinedl@acm.org> 1.6-5
- Added dependency on /bin/w3m.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 29 2014 David Levine <levinedl@acm.org> 1.6-1
- Update nmh to 1.6
- Configure with SASL and TLS support
- Replaced patch of autoconf files with autoreconf --force
- Updated run-time and build dependencies

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Aug 09 2013 Josh Bressers <bressers@redhat.com> 0:1.5-8
- Switch to unversioned docdir

* Fri Aug 09 2013 Josh Bressers <bressers@redhat.com> 0:1.5-7
- Re-run autoconf to pick 2.69 changes
- Properly package the doc directory

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.5-5
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Aug 04 2012 Parag Nemade <paragn AT fedoraproject DOT org> - 1.5-3
- Change BR: db4-devel to libdb-devel

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 David Levine <levinedl@acm.org> 0:1.5-1
- Update nmh to 1.5

* Sun Jan 15 2012 Josh Bressers <bressers@redhat.com> 0:1.4-1
- Update nmh to 1.4

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jun 19 2008 Josh Bressers <bressers@redhat.com> 0:1.3-1
- Update nmh to 1.3

* Wed Apr 30 2008 Josh Bressers <bressers@redhat.com> 0:1.3-RC1.1
- Update nmh to 1.3-RC1

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.2-20070116cvs.4
- Autorebuild for GCC 4.3

* Tue Aug 21 2007 Josh Bressers <bressers@redhat.com> 0:1.2_20070115cvs.4
- Fix inc when the -silent flag is used

* Sun Feb 04 2007 Josh Bressers <bressers@redhat.com> 0:1.2_20070115cvs.3
- Use double quotes not single quotes for CFLAGS

* Sun Feb 04 2007 Josh Bressers <bressers@redhat.com> 0:1.2_20070115cvs.2
- Use $RPM_OPT_FLAGS when building the source bz#227243

* Mon Jan 15 2007 Josh Bressers <bressers@redhat.com> 0:1.2_CVS_20070115
- Update to nmh 1.2 post CVS (thanks to Horst H. von Brand for assistance
  in this task)

* Wed Jan 10 2007 Josh Bressers <bressers@redhat.com> 0:1.1-20
- Replace the libtermcap-devel buildrequires with ncurses-devel

* Mon Sep 11 2006 Josh Bressers <bressers@redhat.com> 0:1.1-19.fc6
- Use %%\dist tag
- Place helper programs in /usr/libexec
- Rebuild for FC6

* Sun Feb 19 2006 Josh Bressers <bressers@redhat.com> 0:1.1-18.fc5
- Fix a broken spec file.

* Sun Feb 19 2006 Josh Bressers <bressers@redhat.com> 0:1.1-17.fc5
- Stop trying to install inc sgid.

* Mon Feb 13 2006 Josh Bressers <bressers@redhat.com> 0:1.1-16.fc5
- Rebuild for Fedora Extras 5.

* Fri Dec 16 2005 Josh Bressers <bressers@redhat.com> 0:1.1-15.fc5
- Add the -fno-builtin-strcasecmp cflag.

* Tue Dec 13 2005 Josh Bressers <bressers@redhat.com> 0:1.1-14.fc5
- Add a patch to prevent multiple calls to context_read from squashing
  settings.

* Mon Dec 12 2005 Josh Bressers <bressers@redhat.com> 0:1.1-13.fc5
- Add a patch to allow repl to properly annotate messages.

* Mon Dec 05 2005 Josh Bressers <bressers@redhat.com> 0:1.1-12.fc5
- Add a buildrequires on /bin/vi
- Modify the sendmail buildrequires to use /usr/sbin/sendmail

* Thu Nov 10 2005 Josh Bressers <bressers@redhat.com> 0:1.1-11.fc5
- Add a sendmail buildrequires to make spost work properly

* Thu Nov 03 2005 Josh Bressers <bressers@redhat.com> 0:1.1-10.fc5
- Prevent mhshow from trying to close a file stream twice

* Thu Aug 25 2005 Josh Bressers <bressers@redhat.com> 0:1.1-9.fc5
- Fix the specfile to honor the $RPM_OPT_FLAGS

* Tue May 10 2005 Josh Bressers <bressers@redhat.com> 0:1.1-8.fc4
- Use fcntl for filelocking instead of the default dotlocks.

* Sun Apr 24 2005 Josh Bressers <bressers@redhat.com> 0:1.1-7.fc4
- Add patch from Jason Venner to avoid trying to lock files in /dev

* Sun Apr 17 2005 Josh Bressers <bressers@redhat.com> 0:1.1-6.fc4
- Remove what should have been commented out redinitions of the _sysconfdir
  and _libdir macros.

* Thu Apr 14 2005 Josh Bressers <bressers@redhat.com> 0:1.1-5
- Make the spec file much more sane.

* Wed Apr 13 2005 Josh Bressers <bressers@redhat.com> 0:1.1-3
- Initial build
