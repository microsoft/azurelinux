%global source_dir  %{_datadir}/%{name}-source
%global inst_srcdir %{buildroot}/%{source_dir}

Summary:        High-performance event loop/event model with lots of features
Name:           libev
Version:        4.33
Release:        5%{?dist}
License:        BSD OR GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://software.schmorp.de/pkg/libev.html
Source0:        https://dist.schmorp.de/libev/Attic/%{name}-%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  tar

Provides:       bundled(libecb) = 1.05

%description
Libev is modeled (very loosely) after libevent and the Event Perl
module, but is faster, scales better and is more correct, and also more
featureful. And also smaller.

%package devel
Summary:        Development headers for libev
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the development headers and libraries for libev.

%package libevent-devel
Summary:        Compatibility development header with libevent for %{name}.
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}
# The event.h file actually conflicts with the one from libevent-devel
Conflicts:      libevent-devel

%description libevent-devel
This package contains a development header to make libev compatible with
libevent.

%package source
Summary:        High-performance event loop/event model with lots of features
Provides:       bundled(libecb) = 1.05
BuildArch:      noarch

%description source
This package contains the source code for libev.

%prep
%autosetup -p0
autoreconf -vfi

%build
%configure --disable-static --with-pic
%make_build

%check
make check

%install
%make_install
rm -vf %{buildroot}%{_libdir}/%{name}.la

# Make the source package
mkdir -p %{inst_srcdir}
find . -type f | grep -E '.*\.(c|h|am|ac|inc|m4|h.in|man.pre|pl|txt)$' | xargs tar cf - | (cd %{inst_srcdir} && tar xf -)
install -p -m 0644 Changes ev.pod LICENSE README %{inst_srcdir}

%ldconfig_scriptlets

%files
%license LICENSE
%doc Changes README
%{_libdir}/%{name}.so.4*

%files devel
%{_includedir}/ev++.h
%{_includedir}/ev.h
%{_libdir}/%{name}.so
%{_mandir}/man?/*

%files libevent-devel
%{_includedir}/event.h

%files source
%{source_dir}

%changelog
* Thu Jan 27 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.33-5
- Initial CBL-Mariner import from Fedora 36 (license: MIT).
- License verified.

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.33-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.33-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.33-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Mar 19 2020  Fabian Affolter <mail@fabian-.affolter.ch> - 4.33-1
- Update to latest upstream release 4.33 (rhbz#1814655)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.31-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 09 2020  Fabian Affolter <mail@fabian-.affolter.ch> - 4.31-1
- Update to latest upstream release 4.31 (rhbz#1785861)

* Sun Jul 28 2019 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 4.27-1            
- Update to 4.27 (#1724817)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.25-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.25-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Dec 24 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.25-7
- Update to 4.25

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.24-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.24-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.24-5
- Switch to %%ldconfig_scriptlets

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.24-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.24-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Dec 28 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 4.24-1
- Update to 4.24 (RHBZ #1408954)

* Thu Nov 17 2016  Fabian Affolter <mail@fabian-.affolter.ch> - 4.23-1
- Update to latest upstream release 4.23 (rhbz#1395925)

* Mon Mar 28 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 4.22-1
- Update to 4.22 (RHBZ #1234039)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Oct 17 2015  Fabian Affolter <mail@fabian-.affolter.ch> - 4.20-2
- Remove patch

* Sat Jun 20 2015 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 4.20-1
- Update to 4.20 (#1234039)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Sep 29 2014 Mathieu Bridon <bochecha@fedoraproject.org> - 4.19-1
- Update to 4.19.

* Tue Sep 23 2014 Mathieu Bridon <bochecha@fedoraproject.org> - 4.18-2
- Fix C++ function definitions
  https://bugzilla.redhat.com/show_bug.cgi?id=1145190

* Mon Sep 08 2014 Mathieu Bridon <bochecha@fedoraproject.org> - 4.18-1
- Update to 4.18.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Nov 26 2013 Mathieu Bridon <bochecha@fedoraproject.org> - 4.15-3
- Get the package closer to what upstream intended:
  - Do not move the headers into a subfolder of /usr/include
  - Make a libev-libevent-devel subpackage to contain the libevent
    compatibility header, so that only this subpackage conflicts with
    libevent-devel, not all of libev-devel
  - Drop the pkgconfig file, as upstream rejected it several times already.

* Sun Sep  8 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 4.15-2
- Bump (koji was broken)

* Sun Sep  8 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 4.15-1
- Update to 4.15 (rhbz 987489)
- Fix dates in spec

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 08 2013 Mathieu Bridon <bochecha@fedoraproject.org> - 4.11-2
- Make a patch out of Michal's pkgconfig support.
- Modernize the configure.ac file for Automake >= 1.13.
- Respect the Fedora CFLAGS
  https://bugzilla.redhat.com/show_bug.cgi?id=908096

* Fri Sep 28 2012 Mathieu Bridon <bochecha@fedoraproject.org> - 4.11-1
- Update to 4.11

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.04-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.04-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Aug  9 2011 Tom Callaway <spot@fedoraproject.org> - 4.04-1
- move man page
- cleanup spec
- update to 4.04

* Mon Jun 13 2011 Matěj Cepl <mcepl@redhat.com> - 4.03-2
- EL5 cannot have noarch subpackages.

* Sat Feb  5 2011 Michal Nowak <mnowak@redhat.com> - 4.03-1
- 4.03; RHBZ#674022
- add a -source subpackage (Mathieu Bridon); RHBZ#672153

* Mon Jan 10 2011 Michal Nowak <mnowak@redhat.com> - 4.01-1
- 4.01
- fix grammar in %%description

* Sat Jan  2 2010 Michal Nowak <mnowak@redhat.com> - 3.90-1
- 3.9

* Mon Aug 10 2009 Michal Nowak <mnowak@redhat.com> - 3.80-1
- 3.8
- always use the most recent automake
- BuildRequires now libtool

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.70-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 17 2009 Michal Nowak <mnowak@redhat.com> - 3.70-2
- spec file change, which prevented uploading most recent tarball
  so the RPM was "3.70" but tarball was from 3.60

* Fri Jul 17 2009 Michal Nowak <mnowak@redhat.com> - 3.70-1
- v3.7
- list libev soname explicitly

* Mon Jun 29 2009 Michal Nowak <mnowak@redhat.com> - 3.60-1
- previous version was called "3.6" but this is broken update
  path wrt version "3.53" -- thus bumping to "3.60"

* Thu Apr 30 2009 Michal Nowak <mnowak@redhat.com> - 3.6-1
- 3.60
- fixed few mixed-use-of-spaces-and-tabs warnings in spec file

* Thu Mar 19 2009 Michal Nowak <mnowak@redhat.com> - 3.53-1
- 3.53

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.52-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 07 2009 Michal Nowak <mnowak@redhat.com> - 3.52-1
- 3.52

* Wed Dec 24 2008 Michal Nowak <mnowak@redhat.com> - 3.51-1
- 3.51

* Thu Nov 20 2008 Michal Nowak <mnowak@redhat.com> - 3.49-1
- version bump: 3.49

* Sun Nov  9 2008 Michal Nowak <mnowak@redhat.com> - 3.48-1
- version bump: 3.48

* Mon Oct  6 2008 kwizart <kwizart at gmail.com> - 3.44-1
- bump to 3.44

* Tue Sep  2 2008 kwizart <kwizart at gmail.com> - 3.43-4
- Fix pkgconfig support

* Tue Aug 12 2008 Michal Nowak <mnowak@redhat.com> - 3.43-2
- removed libev.a
- installing with "-p"
- event.h is removed intentionaly, because is there only for 
  backward compatibility with libevent

* Mon Aug 04 2008 Michal Nowak <mnowak@redhat.com> - 3.43-1
- initial package
