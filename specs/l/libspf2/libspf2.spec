# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# NOTE THAT THE TEST SUITE IS CURRENTLY BROKEN
# USE rpmbuild --with checks TO SEE THIS FOR YOURSELF

# While the library and perlmod each have different versions, there is
# only one release number for both the library and the perlmod, as
# both are in the same source code.

%global git 4915c308

# Use rpmbuild --with checks to try running the broken test suite (disabled by default)
%{!?_without_checks:	%{!?_with_checks: %global _without_checks --without-checks}}
%{?_with_checks:	%global enable_checks 1}
%{?_without_checks:	%global enable_checks 0}

Name:		libspf2
Version:	1.2.11
Release: 20.20210922git%{git}%{?dist}
Summary:	An implementation of the SPF specification
License:	BSD or LGPLv2+
Url:		http://www.libspf2.org/

#Source0:	http://www.libspf2.org/spf/libspf2-%{version}.tar.gz
# Upstream source tree at https://github.com/shevek/libspf2/
# git archive --format tar --prefix libspf2-1.2.10-0e23f41e/ HEAD | xz -c > libspf2-1.2.10-0e23f41e.tar.xz
Source0:	libspf2-%{version}-%{git}.tar.xz
Patch1:	0001-remove-libreplace-unneeded-on-Linux.patch
Patch2:	0002-add-include-string-for-memset.patch
Patch3:	CVE-2023-42118-and-other-fixes.patch

BuildRequires:	gcc
BuildRequires:	automake autoconf libtool
BuildRequires:	doxygen, graphviz
# For perl bindings (Makefile.PL claims Mail::SPF is needed, but it isn't)
BuildRequires:	perl-devel
BuildRequires:	perl-generators
BuildRequires:	perl(ExtUtils::MakeMaker)
# For perl test suite
BuildRequires:	perl(Test::Pod), perl(String::Escape)
BuildRequires: make
# POD Coverage is non-existent, causes test suite to fail
BuildConflicts:	perl(Test::Pod::Coverage)
# Perl module fails the standard test suite
BuildConflicts:	perl(Mail::SPF::Test)

Patch4: disable-call-graphs.patch
%description
libspf2 is an implementation of the SPF (Sender Policy Framework)
specification as found at:
http://www.ietf.org/internet-drafts/draft-mengwong-spf-00.txt
SPF allows email systems to check SPF DNS records and make sure that
an email is authorized by the administrator of the domain name that
it is coming from. This prevents email forgery, commonly used by
spammers, scammers, and email viruses/worms.

A lot of effort has been put into making it secure by design, and a
great deal of effort has been put into the regression tests.

%package devel
Summary:	Development tools needed to build programs that use libspf2
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
The libspf2-devel package contains the header files necessary for
developing programs using the libspf2 (Sender Policy Framework)
library.

If you want to develop programs that will look up and process SPF records,
you should install libspf2-devel.

API documentation is in the separate libspf2-apidocs package.

%package apidocs
Summary:	API documentation for the libspf2 library
Requires:	%{name} = %{version}-%{release}
BuildArch: noarch

%description apidocs
The libspf2-apidocs package contains the API documentation for creating
applications that use the libspf2 (Sender Policy Framework) library.

%package -n perl-Mail-SPF_XS
Summary:	An XS implementation of Mail::SPF
# Automatically converted from old format: GPL+ or Artistic - review is highly recommended.
License:	GPL-1.0-or-later OR Artistic-1.0-Perl
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description -n perl-Mail-SPF_XS
This is an interface to the C library libspf2 for the purpose of
testing. While it can be used as an SPF implementation, you can also
use Mail::SPF, which is a little more perlish.

%package progs
Summary:	Programs for making SPF queries using libspf2
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires(post): /usr/sbin/alternatives
Requires(preun): /usr/sbin/alternatives
Requires(postun): /usr/sbin/alternatives, /usr/bin/readlink

%description progs
Programs for making SPF queries and checking their results using libspf2.

%prep
%setup -q -n libspf2-%{version}-%{git}
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1


%patch -P4 -p1
%build
# The configure script checks for the existence of __ns_get16 and uses the
# system-supplied version if found, otherwise one from src/libreplace.
# However, this function is marked GLIBC_PRIVATE in recent versions of glibc
# and shouldn't be called even if the configure script finds it. So we make
# sure that the configure script always uses the version in src/libreplace.
# This prevents us getting an unresolvable dependency in the built RPM.
ac_cv_func___ns_get16=no
export ac_cv_func___ns_get16

autoreconf -vif
%configure --enable-perl --disable-dependency-tracking

# Kill bogus RPATHs
sed -i 's|^sys_lib_dlsearch_path_spec="/lib /usr/lib|sys_lib_dlsearch_path_spec="/%{_lib} %{_libdir}|' libtool

make %{?_smp_mflags} CFLAGS="%{optflags} -fno-strict-aliasing"

# Generate API docs
# SHORT_NAMES left at default (NO) for reproducible noarch builds
/usr/bin/doxygen

%install
make \
	DESTDIR=%{buildroot} \
	PERL_INSTALL_ROOT=$(grep DESTDIR perl/Makefile &> /dev/null && echo "" || echo %{buildroot}) \
	INSTALLDIRS=vendor \
	INSTALL="install -p" \
	install

# Clean up after impure perl installation
find %{buildroot} \( -name perllocal.pod -o -name .packlist \) -delete
find %{buildroot} -type f -name '*.bs' -a -size 0 -delete
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'
chmod -R u+w %{buildroot}/*

# Don't want statically-linked binaries
rm -f %{buildroot}%{_bindir}/spf*_static

# Rename binaries that will be accessed via alternatives
mv -f %{buildroot}%{_bindir}/spfquery	%{buildroot}%{_bindir}/spfquery.libspf2
mv -f %{buildroot}%{_bindir}/spfd	%{buildroot}%{_bindir}/spfd.libspf2

# Remove libtool archive and static
rm -rf %{buildroot}%{_libdir}/*.a
rm -rf %{buildroot}%{_libdir}/*.la

%check
%if %{enable_checks}
make -C tests check
LD_PRELOAD=$(pwd)/src/libspf2/.libs/libspf2.so make -C perl test
%endif

%ldconfig_scriptlets

%post progs
/usr/sbin/alternatives --install %{_bindir}/spfquery spf %{_bindir}/spfquery.libspf2 20 \
	--slave %{_bindir}/spfd spf-daemon %{_bindir}/spfd.libspf2
exit 0

%preun progs
if [ $1 = 0 ]; then
	/usr/sbin/alternatives --remove spf %{_bindir}/spfquery.libspf2
fi
exit 0

%postun progs
if [ "$1" -ge "1" ]; then
	spf=`readlink /etc/alternatives/spf`
	if [ "$spf" == "%{_bindir}/spfquery.libspf2" ]; then
		/usr/sbin/alternatives --set spf %{_bindir}/spfquery.libspf2
	fi
fi
exit 0

%files
%license LICENSES
%doc README INSTALL TODO
%{_libdir}/libspf2.so.*

%files devel
%{_includedir}/spf2/
%{_libdir}/libspf2.so

%files apidocs
%doc doxygen/html

%files progs
%{_bindir}/spfd.libspf2
%{_bindir}/spfquery.libspf2
%{_bindir}/spftest
%{_bindir}/spf_example

%files -n perl-Mail-SPF_XS
%{perl_vendorarch}/Mail/
%{perl_vendorarch}/auto/Mail/
%{_mandir}/man3/Mail::SPF_XS.3pm*

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.11-19.20210922git4915c308
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1.2.11-18.20210922git4915c308
- Perl 5.42 rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.11-17.20210922git4915c308
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Aug  5 2024 Miroslav Suchý <msuchy@redhat.com> - 1.2.11-16.20210922git4915c308
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.11-15.20210922git4915c308
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1.2.11-14.20210922git4915c308
- Perl 5.40 rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.11-13.20210922git4915c308
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.11-12.20210922git4915c308
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Oct  3 2023 Bojan Smojver <bojan@rexursive.com> - 1.2.11-11.20210922git4915c308
- Add fixes from pull request 47

* Mon Oct  2 2023 Bojan Smojver <bojan@rexursive.com> - 1.2.11-10.20210922git4915c308
- CVE-2023-42118

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.11-8.20210922git4915c308
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1.2.11-7.20210922git4915c308
- Perl 5.38 rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.11-6.20210922git4915c308
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jan 06 2023 Peter Fordham <peter.fordham@gmail.com> - 1.2.11-5.20210922git4915c308
- Add missing include of string.h for memset in spf_utils.c
  https://github.com/shevek/libspf2/issues/41

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.11-4.20210922git4915c308
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.2.11-3.20210922git4915c308
- Perl 5.36 rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.11-2.20210922git4915c308
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Sep 22 2021 Bojan Smojver <bojan@rexursive.com> - 1.2.11-1.20210922git4915c308
- Build latest upstream git HEAD
- CVE-2021-20314
- CVE-2021-33912
- CVE-2021-33913

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.10-30.20150405gitd57d79fd
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.2.10-29.20150405gitd57d79fd
- Perl 5.34 rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.10-28.20150405gitd57d79fd
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.10-27.20150405gitd57d79fd
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.2.10-26.20150405gitd57d79fd
- Perl 5.32 rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.10-25.20150405gitd57d79fd
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.10-24.20150405gitd57d79fd
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.2.10-23.20150405gitd57d79fd
- Perl 5.30 rebuild

* Wed Mar 20 2019 Peter Robinson <pbrobinson@fedoraproject.org> 1.2.10-22.20150405gitd57d79fd
- Fix FTBFS, remove legacy bits and general cleanup

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.10-21.20150405gitd57d79fd
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.10-20.20150405gitd57d79fd
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jul 06 2018 Petr Pisar <ppisar@redhat.com> - 1.2.10-19.20150405gitd57d79fd
- Perl 5.28 rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.2.10-18.20150405gitd57d79fd
- Perl 5.28 rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.10-17.20150405gitd57d79fd
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.10-16.20150405gitd57d79fd
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.10-15.20150405gitd57d79fd
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.2.10-14.20150405gitd57d79fd
- Perl 5.26 rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.10-13.20150405gitd57d79fd
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue May 31 2016 Matt Domsch <matt@domsch.com> -  1.2.10-12.20150405gitd57d79fd
- Simplify release numbers (same for both library and perl module)

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.2.10-7.20150405gitd57d79fd.1
- Perl 5.24 rebuild

* Fri Feb 12 2016 Petr Pisar <ppisar@redhat.com> - 1.2.10-7.20150405gitd57d79fd
- Correct release numbers

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.10-6.20150405gitd57d79fd.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Matt Domsch <matt@domsch.com> - 1.2.10-6.20150405gitd57d79fd
- Fix self-Requires in perl mod

* Tue Jun 16 2015 Matt Domsch <matt@domsch.com> - 1.2.10-5.20150405gitd57d79fd.2
- bump for rebuild with newer perl

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.2.10-5.20150405gitd57d79fd.1
- Perl 5.22 rebuild

* Tue Apr  7 2015 Matt Domsch <mdomsch@domsch.com> - 1.2.10-5
- import into fedpkg
- drop isa requires for apidocs, it caused rpmdiff failures
  being noarch

* Sun Apr  5 2015 Matt Domsch <matt@domsch.com> - 1.2.10-4
- update for review comments

* Sun Apr  5 2015 Matt Domsch <matt@domsch.com> - 1.2.10-3
- update for review comments

* Sat Apr  4 2015 Matt Domsch <matt@domsch.com> - 1.2.10-2
- update to upstream 1.2.10+git
- update automake / autoconf for Fedora 21

* Sat Jan 25 2014 Matt Domsch <matt@domsch.com> - 1.2.10-1
- update to upstream 1.2.10+git

* Fri Jun 25 2010 Paul Howarth <paul@city-fan.org> 1.2.9-3
- Rebuild for perl 5.12.1 in Rawhide
- Build with -fno-strict-aliasing

* Mon May 11 2009 Paul Howarth <paul@city-fan.org> 1.2.9-2
- Define RPM macros in global scope
- apidocs subpackage no longer requires devel subpackage
- apidocs is noarch from Fedora 10 onwards

* Mon Nov 10 2008 Paul Howarth <paul@city-fan.org> 1.2.9-1
- New upstream version 1.2.9
- Perl module has changed but its version number hasn't
- docs directory no longer included in release tarball

* Wed Oct 15 2008 Paul Howarth <paul@city-fan.org> 1.2.8-1
- New upstream version 1.2.8, includes fix for CVE-2008-2469
  (buffer overflows handling DNS responses)
- Drop all patches, all included upstream (or equivalent fixes)
- Fix bogus RPATHs on x86_64
- Enable perl bindings (in perl-Mail-SPF_XS subpackage)
- No upstream Changelog anymore
- Add buildreqs doxygen and graphviz for building API docs, which are large
  and now in an -apidocs subpackage (Fedora 3, RHEL 4 onwards)
- Add buildreq perl(ExtUtils::MakeMaker) for perl bindings
- Add buildreqs perl(Test::Pod) and perl(String::Escape) for perl module test
  suite
- BuildConflict with perl(Mail::SPF::Test) and perl(Test::Pod::Coverage) as
  the associated tests are beyond simple repair

* Thu Jul 31 2008 Paul Howarth <paul@city-fan.org> 1.2.5-4
- Incorporate patches for res_ninit() setup and malloc() usage from
  Johann Klasek <johann AT klasek DOT at>
  (see http://milter-greylist.wikidot.com/libspf2)
- Clarify license as BSD OR LGPL (v2.1 or later)
- Add dist tag so that we can build distro-specific RPM packages instead of a
  single generic package; the benefit of this is that recent distributions can
  take advantages of improvements in their compilers
- Use regular %%configure macro to pick up distro-specific compiler flags
- Don't package static library (--disable-static configure option is broken)
- Dispense with pointless provide of `spf'

* Mon Feb 12 2007 Paul Howarth <paul@city-fan.org> 1.2.5-3
- Cosmetic spec file cleanup
- Use patch instead of scripted edit to remove bogus include file reference
- Patch to make 64-bit clean
  (http://permalink.gmane.org/gmane.mail.spam.spf.devel/1212)
- Remove buildroot unconditionally in %%clean and %%install
- Don't include libtool archive in -devel package
- Disable running of test suite by default

* Wed Aug  3 2005 Paul Howarth <paul@city-fan.org> 1.2.5-2
- Workaround for %%check with rpm-build <= 4.1.1
- Remove reference to not-installed spf_dns_internal.h in spf_server.h
- Minimize rpmlint issues

* Thu Feb 24 2005 Paul Howarth <paul@city-fan.org> 1.2.5-1
- Update to 1.2.5
- Patches removed; now included upstream

* Sun Feb 20 2005 Paul Howarth <paul@city-fan.org> 1.2.1-1
- Update to 1.2.1
- Remove case-sensitivity patch
- spf_example_2mx no longer included

* Sun Feb 20 2005 Paul Howarth <paul@city-fan.org> 1.0.4-9
- Enhance detection of Mandrake build system
- Add support for building compat-libspf2 package
- alternatives is a prerequisite for the -progs subpackage only

* Thu Oct 28 2004 Paul Howarth <paul@city-fan.org> 1.0.4-8
- Downgrade alternatives priority to 20 so that other implementations
  of spfquery will be preferred; there is still a case-sensitivity bug
  in libspf2 and no sign of an imminent fix

* Mon Aug 16 2004 Paul Howarth <paul@city-fan.org> 1.0.4-7
- Configure fix to find -lresolv on x64_64
- Portability fixes for x64_64

* Sun Aug  1 2004 Paul Howarth <paul@city-fan.org> 1.0.4-6
- Fix case-sensitivity bug.

* Wed Jul 28 2004 Paul Howarth <paul@city-fan.org> 1.0.4-5
- Revert -pthread option as it didn't improve anything.

* Tue Jul 27 2004 Paul Howarth <paul@city-fan.org> 1.0.4-4
- Use `alternatives' so that the spfquery and spfd programs can co-exist
  with versions from other implementations.
- Ensure thread-safe operation by building with -pthread.

* Thu Jul 15 2004 Paul Howarth <paul@city-fan.org> 1.0.4-3
- Install the libtool library in the devel package so that
  dependent libraries are found properly.
- Use the libtool supplied with the package rather than the
  system libtool.

* Tue Jul 13 2004 Paul Howarth <paul@city-fan.org> 1.0.4-2
- Cosmetic changes for building on Mandrake Linux
- Require rpm-build >= 4.1.1 for building to avoid strange error messages
  from old versions of rpm when they see %%check
- Require glibc-devel and make for building
- Require perl for building with checks enabled
- Improved description text for the packages

* Fri Jul 09 2004 Paul Howarth <paul@city-fan.org> 1.0.4-1
- Update to 1.0.4
- Added facility to build without running test suite
  (rpmbuild --without checks)

* Sat Jul 03 2004 Paul Howarth <paul@city-fan.org> 1.0.3-1
- Initial RPM build.
