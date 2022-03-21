# work around upstream versioning being decimal rather than v-string
%global upstream_version 4.76
%global extraversion %{nil}

Summary:        Asynchronous Input/Output
Name:           perl-IO-AIO
Version:        %{upstream_version}%{extraversion}
Release:        2%{?dist}
License:        GPL+ OR Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/IO-AIO
Source0:        https://cpan.metacpan.org/modules/by-module/IO/IO-AIO-%{upstream_version}.tar.gz
Patch0:         IO-AIO-4.4-shellbang.patch

# Module Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Canary::Stability) >= 2001
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
# Script Runtime
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(Pod::Usage)
BuildRequires:  perl(Time::HiRes)
BuildRequires:  perl(XSLoader)
BuildRequires:  perl(base)
BuildRequires:  perl(common::sense)

%if %{with_check}
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Test)
BuildRequires:  perl(lib)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
%endif

Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(XSLoader)
# Avoid provides for private shared objects
%{?perl_default_filter}
%if "%{upstream_version}%{extraversion}" != "%{upstream_version}"
Provides:       perl(IO::AIO) = %{upstream_version}%{extraversion}
%endif

%description
This module implements asynchronous I/O using whatever means your operating
system supports.

%package -n treescan
Summary:        Scan directory trees, list dirs/files, stat, sync, grep
Requires:       %{name} = %{version}-%{release}
Requires:       perl(Pod::Usage)
BuildArch:      noarch

%description -n treescan
The treescan command scans directories and their contents recursively. By
default it lists all files and directories (with trailing /), but it can
optionally do various other things.

If no paths are given, treescan will use the current directory.

%prep
%setup -q -n IO-AIO-%{upstream_version}

# Fix shellbang in treescan
%patch0

%build
PERL_CANARY_STABILITY_NOPROMPT=1 perl Makefile.PL \
	INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name '*.bs' -empty -delete
%{_fixperms} -c %{buildroot}

%check
make test

%files
%license COPYING
%doc Changes README
%{perl_vendorarch}/auto/IO/
%{perl_vendorarch}/IO/
%{_mandir}/man3/IO::AIO.3*

%files -n treescan
%{_bindir}/treescan
%{_mandir}/man1/treescan.1*

%changelog
* Thu Jan 27 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.76-2
- Initial CBL-Mariner import from Fedora 36 (license: MIT).
- License verified.

* Wed Jul 28 2021 Paul Howarth <paul@city-fan.org> - 4.76-1
- Update to 4.76
  - Add autoconf test for siginfo_t, which is, of course, not available on
    Windows
  - Disable syscalls on Solaris, as perl seems to provide an incompatible
    syscall prototype that clashes with sys/syscall.h
  - Add MAP_FIXED_NOREPLACE, MAP_SHARED_VALIDATE, MAP_SYNC and MAP_UNINITIALIZED

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.75-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 4.75-3
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.75-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Dec 30 2020 Paul Howarth <paul@city-fan.org> - 4.75-1
- Update to 4.75
  - Added pidfd_open, pidfd_getfd and pidfd_send_signal functions
  - Rework bin/treescan to avoid recursion; this fixes two bugs where a deep
    directory traversal or a lot of command line arguments could cause it to
    crash
  - Support defining syscall numbers in gendef0
  - Added (but not documented) open_tree, AT_* and move_mount flags
  - Added (but not documented) waitid-P_*, FSPICK_*, FSOPEN_*, FSCONFIG_*,
    MOUNT_ATTR_* constants

* Fri Dec  4 2020 Paul Howarth <paul@city-fan.org> - 4.73-1
- Update to 4.73
  - def0.h was not up-to-date, running into musl problems
  - IO::AIO::splice and IO::AIO::tee didn't properly return 64 bit values
  - Added IO::AIO::accept4
  - Added various F_SEAL-related fcntl constants
  - Removed experimental marker for fdlimit functions
  - fiemap now includes the last segment even if it overflows the end offset,
    which is arguably the correct behaviour
- Use %%license unconditionally

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.72-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 4.72-5
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.72-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.72-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 4.72-2
- Perl 5.30 rebuild

* Wed Apr  3 2019 Paul Howarth <paul@city-fan.org> - 4.72-1
- Update to 4.72
  - libeio: If fd 0 is available do not use it for aio_wd, as it collides with
    IO::AIO::CWD
  - Added IO::AIO::memfd_create
  - Correctly include <sys/uio.h> in the vmsplice test
  - Reduce code size by ~7%% on amd64 by declaring more functions as noinline
  - Documentation fixes and updates
  - Experimental and undocumented preliminary support for synchronous statx

* Sun Mar 10 2019 Paul Howarth <paul@city-fan.org> - 4.71-1
- Update to 4.71
  - Due to an error in the linux manpages, the configure tests for readahead,
    sync_file_range, splice etc. failed; this has been fixed

* Mon Mar  4 2019 Paul Howarth <paul@city-fan.org> - 4.70-1
- Update to 4.7
  - Significantly speed up scandir for the very special case of a non-POSIX
    filesystem that nevertheless reports valid dt_type information; the only
    known filesystem of this type is currently btrfs, which didn't get its act
    together to implement POSIX semantics in all these years
  - Add IO::AIO::MCL_ONFAULT for mlockall, add IO::AIO::mlockall
  - Neither sys/mkdev.h nor sys/sysmacros.h were included, even when they were
    detected by autoconf

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.60-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Aug 28 2018 Paul Howarth <paul@city-fan.org> - 4.60-1
- Update to 4.6
  - Add st_btime, st_btimesec, st_btimensec and st_gen accessors, mostly for
    bsds that expose birthtime and st_gen members (netbsd, freebsd but only
    st_gen on openbsd because they compiled their perl without support for
    birthtimes)
  - Fix madvise and munlock to properly support negative offsets
  - Allocate fd for the aio_close at boot time, to guarantee it working later,
    rather than calling abort when it fails; this also avoids close-on-exec
    race issues after module load
  - #undef utime on win32, which might help some reports of utime hangs
  - Minor documentation improvements
  - Minor configure clean-ups
  - Use $Config{perllibs} instead of libs for configure, which might help
    people who didn't install all perl dependencies (might break things as
    well)
- Remove buildreqs needed only due to use of $Config{libs}

* Wed Aug 15 2018 Paul Howarth <paul@city-fan.org> - 4.54-1
- Update to 4.54
  - Include sys/mkdev.h or sys/sysmacros.h if available
  - Further tweaks to configure invocation for systems requiring --rpath
  - No longer rely on custom paths on win32 platforms
  - Try to work around buggy PAGESIZE macro on solaris

* Tue Aug 14 2018 Paul Howarth <paul@city-fan.org> - 4.53-1
- Update to 4.53
  - Add $Config{libs} to LIBS for configure, to work around systems with broken
    library dependencies
- Add missing include for prctl()
- Add buildreqs needed due to overspecification of libraries in $Config{libs}

* Mon Aug 13 2018 Paul Howarth <paul@city-fan.org> - 4.52-1
- Update to 4.52
  - Complete rework of the autoconf framework: IO::AIO now uses its own
    config.h, separate from libeio, and tries to test the actual perl
    environment, not the standard system environment
  - Provide nanosecond-accuracy stat time accessors for both perl and IO::AIO
    stat functions
  - Removed non-portable C++ functions from eio.c
  - Try to fix readdir tests on cygwin spuriously failing

* Wed Aug  1 2018 Paul Howarth <paul@city-fan.org> - 4.50-1
- Update to 4.5
  - aio_mtouch: touch all pages as requested, not just the first page
  - New function: IO::AIO::mremap - linux-specific mremap, with constants
    MREMAP_MAYMOVE and MREMAP_FIXED
  - Add O_ACCMODE
  - Add (undocumented) MSG_CMSG_CLOEXEC and SOCK_CLOEXEC constants

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.40-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 4.40-2
- Perl 5.28 rebuild

* Wed Feb 21 2018 Paul Howarth <paul@city-fan.org> - 4.40-1
- Update to 4.4
  - New aio_slurp request
  - Add (experimental) IO::AIO::eventfd and timerfd* function
  - Add (experimental) IO::AIO::get_fdlimit and IO::AIO::min_fdlimit
  - Point out that aio_copy overwrites existing files
  - Remove filesystem magic number table from aio_statvfs docs as statvfs
    doesn't actually return this info at all (statfs does)
  - Add a bunch of (mostly linux-specific) constants for use in ioctls (see
    aio_ioctl docs)
  - treescan now has a proper manpage and useful --help output
  - New option --sync in treescan, to sync everything in a subtree
  - Changed default for aio_msync flags to MSYNC_SYNC
  - Document offset/length behaviour of mprotect/madvise
  - Support linux's renameat2 (via aio_rename2)
  - Add aio_rename2, an aio_rename with flags
  - Add F_DUPPFD_CLOEXEC, F_OFD_[SG]ETLKW? constants
  - Add FALLOC_FL_INSERT_RANGE, FALLOC_FL_UNSHARE_RANGE
  - libeio: Use posix_close if available
  - libeio: Internal close() calls no longer disturb errno
  - Add IO:AIO::FALLOC_FL_UNSHARE
  - Update schmorp.h for removal of USE_SOCKETS_AS_HANDLES and better eventfd
    detection
- Package treescan, in its own package
- Change license to GPLV2+, since parts of libeio are GPLv2+
- Drop EL-5 support
  - Drop BuildRoot: and Group: tags
  - Drop explicit buildroot cleaning in %%install section
  - Drop explicit %%clean section

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.34-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.34-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.34-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 4.34-4
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.34-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 4.34-2
- Perl 5.24 rebuild

* Tue May  3 2016 Paul Howarth <paul@city-fan.org> - 4.34-1
- Update to 4.34
  - def0.h was not properly generated during previous release, causing compile
    errors on various platforms
  - major/minor were accidentally switched
  - Removed duplicate definition of MAP_HUGETLB
  - Added (untested!) aio_fcntl, aio_ioctl requests
  - (libeio) Names set via prctl are truncated to 15 chars + nul, not 16, as
    manpages-dev originally claimed
- Drop def0.h patch from previous release, no longer needed
- Simplify find commands using -empty and -delete

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.33-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 18 2016 Paul Howarth <paul@city-fan.org> - 4.33-1
- Update to 4.33
  - Add IO::AIO::pipe2 function
  - Added support for FALLOC_FL_COLLAPSE_RANGE and FALLOC_FL_ZERO_RANGE
    constants
  - Added support for O_TMPFILE and O_PATH constants
  - Added support for MAP_FIXED, MAP_GROWSDOWN, MAP_32BIT, MAP_HUGETLB,
    MAP_STACK constants, whether they can be sensibly used or not
  - Use NO_INIT where applicable
  - Update libecb
  - Added stability canary support
  - Updated linux super magic table to 4.3.3
- Explicitly BR: perl-devel, needed for EXTERN.h
- Add patch to support building on systems without MAP_STACK or MAP_32BIT

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.32-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 4.32-2
- Perl 5.22 rebuild

* Thu Feb 12 2015 Paul Howarth <paul@city-fan.org> - 4.32-1
- Update to 4.32
  - Replace off_t by STRLEN where appropriate; should not result in
    user-visible changes
  - Update ecb.h for C11 compatibility
- Classify buildreqs by usage
- Use %%license where possible

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 4.31-3
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.31-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jun 10 2014 Paul Howarth <paul@city-fan.org> - 4.31-1
- Update to 4.31
  - Work around more 5.20 bugs

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.30-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Apr 11 2014 Paul Howarth <paul@city-fan.org> - 4.30-1
- Update to 4.3
  - perl5porters broke Async::Interrupt, BDB, EV, IO::AIO and OpenCL without
    warning by switching the meaning of USE_SOCKETS_AS_HANDLES in 5.18
- Drop %%defattr, redundant since rpm 4.4

* Sat Jan 25 2014 Paul Howarth <paul@city-fan.org> - 4.20-1
- Update to 4.2 (see Changes file for details)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.15-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 4.15-5
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 4.15-2
- Perl 5.16 rebuild

* Tue Apr 10 2012 Paul Howarth <paul@city-fan.org> - 4.15-1
- Update to 4.15:
  - Always include linux/types.h for fiemap, for compatibility with ancient
    systems
  - Experimental support for IO::AIO::splice and ::tee (no aio_...)
  - Provide SEEK_HOLE and SEEK_DATA, if available
  - Work around (again!) an immensely stupid bug in RHEL, defining autoconf
    macros in linux system headers

* Sat Apr  7 2012 Paul Howarth <paul@city-fan.org> - 4.14-1
- Update to 4.14:
  - Fix stat structure usage on windows, which caused bogus stat results
  - (libeio) make readahead emulation behave more like actual readahead by
    never failing
  - New request aio_seek
  - New request aio_fiemap
  - Auto-generate the #ifdef/#define 0 blocks for symbols we export
- BR:/R: Perl core modules that might be dual-lived
- Don't need to remove empty directories from buildroot

* Thu Feb  2 2012 Paul Howarth <paul@city-fan.org> - 4.12-1
- Update to 4.12 (see Changes file for details)
  - INCOMPATIBLE CHANGE: fork is no longer supported (indeed, it never was);
    see FORK BEHAVIOUR in manpage for details
- BR: perl(Carp)
- Reinstate compatibility with old distributions such as EL-5
  - Add back BuildRoot definition and cleaning
- Use DESTDIR rather than PERL_INSTALL_ROOT
- Don't use macros for commands
- Use tabs

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.71-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jun 19 2011 Marcela Mašláňová <mmaslano@redhat.com> - 3.71-3
- Perl mass rebuild

* Thu Mar 10 2011 Paul Howarth <paul@city-fan.org> - 3.71-2
- Spec cleanup
- Use %%{?perl_default_filter} instead of our own custom provides filter

* Wed Feb  9 2011 Ruben Kerkhof <ruben@rubenkerkhof.com> - 3.71-1
- Upstream released new version

* Tue Feb  8 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.65-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 17 2010 Marcela Maslanova <mmaslano@redhat.com> - 3.65-2
- Rebuild to fix problems with vendorarch/lib (#661697)

* Thu Jun 24 2010 Ruben Kerkhof <ruben@rubenkerkhof.com> - 3.65-1
- Upstream released new version

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 3.17-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 3.17-4
- Rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec 18 2008 Nicolas Chauvet <kwizart@gmail.com> - 3.17-1
- Update to 3.17

* Sun Nov 09 2008 Ruben Kerkhof <ruben@rubenkerkhof.com> - 3.16-1
- Upstream release new version

* Mon Mar 03 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.51-2
- Rebuild for new perl (again)

* Sat Feb 09 2008 Ruben Kerkhof <ruben@rubenkerkhof.com> - 2.51-1
- Sync with upstream

* Thu Feb  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.33-2
- Rebuild for new perl

* Sun May 13 2007 Ruben Kerkhof <ruben@rubenkerkhof.com> - 2.33-1
- Initial import
