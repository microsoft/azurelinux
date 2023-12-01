Summary:        Library for writing UNIX daemons
Name:           libdaemon
Version:        0.14
Release:        21%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://0pointer.de/lennart/projects/libdaemon/
Source0:        https://0pointer.de/lennart/projects/libdaemon/%{name}-%{version}.tar.gz
# Requires lynx to build the docs
BuildRequires:  gcc
BuildRequires:  lynx

%description
libdaemon is a lightweight C library which eases the writing of UNIX daemons.
It consists of the following parts:
* A wrapper around fork() which does the correct daemonization
  procedure of a process
* A wrapper around syslog() for simpler and compatible log output to
  Syslog or STDERR
* An API for writing PID files
* An API for serializing UNIX signals into a pipe for usage with
  select() or poll()
* An API for running subprocesses with STDOUT and STDERR redirected
  to syslog.

%package        devel
Summary:        Libraries and header files for libdaemon development
Requires:       libdaemon = %{version}-%{release}

%description devel
The libdaemon-devel package contains the header files and libraries
necessary for developing programs using libdaemon.

%prep
%setup -q

%build
%configure --disable-static
%make_build

%install
%make_install
find %{buildroot} \( -name *.a -o -name *.la \) -exec rm {} \;

rm %{buildroot}/%{_docdir}/libdaemon/README
rm %{buildroot}/%{_docdir}/libdaemon/README.html
rm %{buildroot}/%{_docdir}/libdaemon/style.css

%ldconfig_scriptlets

%files
%license LICENSE
%doc README
%{_libdir}/*so.*

%files devel
%doc doc/README.html doc/style.css
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Wed Dec 08 2021 Olivia Crain <oliviacrain@microsoft.com> - 0.14-21
- License verified
- Lint spec

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.14-20
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.14-14
- Switch to %%ldconfig_scriptlets

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Sep 10 2010 Parag Nemade <paragn AT fedoraproject.org> - 0.14-2
- Merge-review cleanup (#225995)

* Sun Oct 18 2009 Lennart Poettering <lpoetter@redhat.com> - 0.14-1
- New release 0.14

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul 29 2008 Lennart Poettering <lpoetter@redhat.com> - 0.13-1
- New release 0.13

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.12-3
- Autorebuild for GCC 4.3

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 0.12-2
- Rebuild for selinux ppc32 issue.

* Wed Jul 11 2007 Lennart Poettering <lpoetter@redhat.com> - 0.12-1
- Update to upstream 0.12. (Basically just includes patch from 0.11-2)

* Mon Jul  2 2007 Dan Williams <dcbw@redhat.com> - 0.11-2
- Fix double-free bug when closing daemon file descriptor (avahi.org #148)

* Fri Jun 22 2007 Martin Bacovsky <mbacovsk@redhat.com> - 0.11-1
- Upgrade to new upstream version 0.11

* Thu Apr  5 2007 Martin Bacovsky <mbacovsk@redhat.com> - 0.10-4
- Resolves: #222855: fileconflict for /usr/share/doc/libdaemon-devel-0.10/Makefile 

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - sh: line 0: fg: no job control
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.10-3.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jason Vas Dias <jvdias@redhat.com> - 0.10-3
- rebuild for new gcc, glibc, glibc-kernheaders

* Mon Jan 06 2006 Jason Vas Dias <jvdias@redhat.com> - 0.10-2
- rebuild for new gcc / glibc

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com> - 0.10-1.1
- rebuild on new gcc

* Wed Dec  7 2005 Jason Vas Dias <jvdias@redhat.com> - 0.10-1
- Update to 0.10

* Thu Oct 20 2005 Alexander Larsson <alexl@redhat.com> - 0.8-1
- Update to 0.8, move from extras to core, split out devel package

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 0.6-6
- rebuild on all arches

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Thu May 13 2004 Aaron Bennett <aaron.bennett@olin.edu> 0:0.6-0.fdr.4
- Added post and postun scripts to run ldconfig
- changed group to standard System/Libraries group
- removed libtool *.la files

* Tue May 4 2004 Aaron Bennett <aaron.bennett@olin.edu> 0:0.6.-0.fdr.3
- Signed packaged with GPG key

* Tue May 4 2004 Aaron Bennett <aaron.bennett@olin.edu> - 0:0.6-0.fdr.2
- Changed URL and Source tag for Fedora.us packaging compliance
- Incremented release tag

* Thu Apr 29 2004 Aaron Bennett <abennett@olin.edu> - 0:0.6-1
- Changed to version 0.6 of libdaemon

* Wed Mar 31 2004 Aaron Bennett <abennett@olin.edu>
- Initial build.
