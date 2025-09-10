Vendor:         Microsoft Corporation
Distribution:   Azure Linux
# Run optional test
%if ! (0%{?rhel})
%bcond_without perl_Path_Tiny_enables_optional_test
%else
%bcond_with perl_Path_Tiny_enables_optional_test
%endif

Name:		perl-Path-Tiny
Version:	0.146
Release:	3%{?dist}
Summary:	File path utility
License:	Apache-2.0
URL:		https://metacpan.org/release/Path-Tiny
Source0:	https://cpan.metacpan.org/authors/id/D/DA/DAGOLDEN/Path-Tiny-%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildArch:	noarch
# Module Build
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker)
# Module Runtime
BuildRequires:	perl(Carp)
BuildRequires:	perl(Config)
BuildRequires:	perl(constant)
BuildRequires:	perl(Cwd)
BuildRequires:	perl(Digest) >= 1.03
BuildRequires:	perl(Digest::SHA) >= 5.45
BuildRequires:	perl(Encode)
BuildRequires:	perl(Exporter) >= 5.57
BuildRequires:	perl(Fcntl)
BuildRequires:	perl(File::Compare)
BuildRequires:	perl(File::Copy)
BuildRequires:	perl(File::Glob)
BuildRequires:	perl(File::Path) >= 2.07
BuildRequires:	perl(File::Spec) >= 0.86
BuildRequires:	perl(File::stat)
BuildRequires:	perl(File::Temp) >= 0.19
BuildRequires:	perl(overload)
BuildRequires:	perl(strict)
BuildRequires:	perl(threads)
BuildRequires:	perl(warnings)
BuildRequires:	perl(warnings::register)
# Test Suite
BuildRequires:	perl(blib)
BuildRequires:	perl(Digest::MD5)
BuildRequires:	perl(File::Basename)
BuildRequires:	perl(File::Spec::Functions)
BuildRequires:	perl(File::Spec::Unix)
BuildRequires:	perl(File::Temp) >= 0.19
BuildRequires:	perl(lib)
BuildRequires:	perl(open)
BuildRequires:	perl(Test::More) >= 0.96
%if %{with perl_Path_Tiny_enables_optional_test}
# Optional Tests
BuildRequires:	perl(CPAN::Meta) >= 2.120900
BuildRequires:	perl(CPAN::Meta::Prereqs)
BuildRequires:	perl(Test::FailWarnings)
%endif
# Dependencies
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	perl(Cwd)
Requires:	perl(Digest) >= 1.03
Requires:	perl(Digest::SHA) >= 5.45
Requires:	perl(Encode)
Requires:	perl(Fcntl)
Requires:	perl(File::Compare)
Requires:	perl(File::Copy)
Requires:	perl(File::Glob)
Requires:	perl(File::Path) >= 2.07
Requires:	perl(File::stat)
Requires:	perl(File::Temp) >= 0.18
Requires:	perl(threads)
Requires:	perl(warnings::register)

# For performance and consistency
%if !(0%{?rhel})
BuildRequires:	perl(PerlIO::utf8_strict) >= 0.003
Requires:	perl(PerlIO::utf8_strict) >= 0.003
%endif
BuildRequires:	perl(Unicode::UTF8) >= 0.58
Requires:	perl(Unicode::UTF8) >= 0.58

%description
This module attempts to provide a small, fast utility for working with file
paths. It is friendlier to use than File::Spec and provides easy access to
functions from several other core file handling modules.

It doesn't attempt to be as full-featured as IO::All or Path::Class, nor does
it try to work for anything except Unix-like and Win32 platforms. Even then, it
might break if you try something particularly obscure or tortuous.

All paths are forced to have Unix-style forward slashes. Stringifying the
object gives you back the path (after some clean up).

File input/output methods flock handles before reading or writing, as
appropriate.

The *_utf8 methods (slurp_utf8, lines_utf8, etc.) operate in raw mode without
CRLF translation.

%prep
%setup -q -n Path-Tiny-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

%check
make test

%files
%license LICENSE
%doc Changes CONTRIBUTING.mkdn README
%{perl_vendorlib}/Path/
%{_mandir}/man3/Path::Tiny.3*

%changelog
* Fri Dec 13 2024 Sreenivasulu Malavathula <v-smalavathu@microsoft.com> - 0.146-3
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License verified

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.146-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri May 10 2024 Paul Howarth <paul@city-fan.org> - 0.146-1
- Update to 0.146
  - Improved error message spewing to a file in a non-existent directory

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.144-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.144-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.144-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.144-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Dec  2 2022 Paul Howarth <paul@city-fan.org> - 0.144-1
- Update to 0.144
  - Fixed tilde expansion tests where ~root expands to '/'

* Wed Nov  9 2022 Paul Howarth <paul@city-fan.org> - 0.142-1
- Update to 0.142
  Deprecations
  - Tilde expansion is deprecated due to inconsistent and bug-prone behavior
  Bug fixes
  - Prevent expansion of tildes that are not the very first character (e.g.
    "./~foo")
  - Prevent unintentional tilde expansion during internal path processing
  - Escape non-tilde glob characters before tilde expansion
  - Fixed spew/edit to a long filename approaching the filesystem length limit
  - Internal calls to 'print' are checked for possible errors
  - Internal read calls are checked for errors
  Changes
  - Path stringification now adds "./" in front of paths starting with literal
    tilde so they will round-trip; FREEZE updated to use this stringification
    rule as well
  - 'move' now uses File::Copy::move internally instead of the built-in
    'rename', allowing it to work across filesystems; it also returns an object
    for the moved location, allowing chaining
  - edit_lines_raw now uses a buffered raw I/O layer
  - edit_lines_utf8 now prefers PerlIO::utf8_strict, if available
  - lines_utf8 now consistently uses a buffered I/O layer
  - open*_utf8 now prefers PerlIO::utf8_strict, if available
  - slurp_utf8 now consistently uses an unbuffered I/O layer
  Documented
  - Changed all raw/UTF-8 layer descriptions in method documentation to match
    the code
  - Fixed SYNOPSIS syntax
  - Documented how to disable TMPDIR when making temp files/dirs
  Testing
  - Add additional tilde stringification testing
  - Fixed tilde expansion tests on Windows
  - Skip a problematic test case on Cygwin

* Thu Oct 20 2022 Paul Howarth <paul@city-fan.org> - 0.130-1
- Update to 0.130
  - The 'mkdir' method no longer fails when applied to an existing directory

* Thu Oct 20 2022 Paul Howarth <paul@city-fan.org> - 0.128-1
- Update to 0.128
  - Added 'mkdir' to replace 'mkpath', but returning the path object for
    chaining
  - The 'mkpath' method is deprecated in favor of 'mkdir'
  - Added 'has_same_bytes' to efficiently compare the contents of two files
  - Edited SYNOPSIS in the POD

* Fri Sep  2 2022 Paul Howarth <paul@city-fan.org> - 0.124-1
- Update to 0.124
  - Added link to 'touchpath' in the 'mkpath' docs
  - Fixed example in `tempfile' docs
- Use SPDX-format license tag

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.122-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.122-3
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.122-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Jan 17 2022 Paul Howarth <paul@city-fan.org> - 0.122-1
- Update to 0.122
  - Adds 'size' and 'size_human' methods; the latter gives 'ls -lh' style
    output, with options to choose base2 or base10 forms

* Mon Oct 25 2021 Paul Howarth <paul@city-fan.org> - 0.120-1
- Update to 0.120
  - The 'tempdir' and 'tempfile' methods may be called on a Path::Tiny object
    representing a directory, in which case the directory will be used as the
    container for the temporary object (as if the 'DIR' argument were used)

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.118-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 23 2021 Michal Josef Spacek <mspacek@redhat.com> - 0.118-3
- Remove runtime dependency for Digest::MD5

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.118-2
- Perl 5.34 rebuild

* Fri Feb  5 2021 Paul Howarth <paul@city-fan.org> - 0.118-1
- Update to 0.118
  - Skip symlink tests on Windows by actually testing symlinks, as Perl 5.33.5
    adds notional support but it's not possible without elevated privileges

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.116-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Jan 23 2021 Paul Howarth <paul@city-fan.org> - 0.116-1
- Update to 0.116
  - Fix tests on MSYS without symlinks enabled

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.114-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.114-2
- Perl 5.32 rebuild

* Sun Apr 26 2020 Paul Howarth <paul@city-fan.org> - 0.114-1
- Update to 0.114
  - Use \z instead of $ in regular expressions

* Wed Jan 29 2020 Paul Howarth <paul@city-fan.org> - 0.112-1
- Update to 0.112
  - Another test fix on Windows, possibly due to a behavior change in
    Cwd::getdcwd

* Tue Jan 14 2020 Paul Howarth <paul@city-fan.org> - 0.110-1
- Update to 0.110
  - Fixes tests on Windows, particularly with newer File::Spec

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.108-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.108-3
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.108-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Aug  1 2018 Paul Howarth <paul@city-fan.org> - 0.108-1
- Update to 0.108
  - Fixed a bug where failure to load optional modules would trigger an
    external $SIG{__DIE__} handler

* Mon Jul 16 2018 Paul Howarth <paul@city-fan.org> - 0.106-1
- Update to 0.106
  - The PERL_PATH_TINY_NO_FLOCK environment variable has been added to allow
    users to disable file locking (and any associated warnings)
  - Detection of unsupported 'flock' is no longer BSD-specific; this allows
    detecting and warning, for example, with the Luster filesystem on Linux
  - Improve reliability and diagnostics of tests run via 'do'

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.104-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.104-6
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.104-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Dec 08 2017 Petr Pisar <ppisar@redhat.com> - 0.104-4
- Enable Test::MockRandom test

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.104-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.104-2
- Perl 5.26 rebuild

* Sat Feb 18 2017 Paul Howarth <paul@city-fan.org> - 0.104-1
- Update to 0.104
  - The 'absolute' method now always returns an absolute path, even if a user
    provided a relative path for the base path; the old, odd behavior was
    documented, but people often don't read docs so the new behavior avoids
    surprises
  - Added 'cached_temp' method

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.100-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Jan 15 2017 Paul Howarth <paul@city-fan.org> - 0.100-1
- Update to 0.100
  - Fixed tests for eventual removal of '.' from @INC in Perl
  - Fixed filehandle mode doc typo
  - Fixed doc typo in relative() that mentioned rel2abs instead of abs2rel

* Mon Oct 10 2016 Paul Howarth <paul@city-fan.org> - 0.098-1
- Update to 0.098
  - Added 'realpath' option for 'tempfile' and 'tempdir' for situations where
    an absolute temporary path just isn't enough

* Sun Jul  3 2016 Paul Howarth <paul@city-fan.org> - 0.096-1
- Update to 0.096
  - Improved method for hiding some modules during tests
- BR: perl-generators unconditionally

* Mon May 23 2016 Paul Howarth <paul@city-fan.org> - 0.094-1
- Update to 0.094
  - Path::Tiny will prefer PerlIO::utf8_strict over encoding(UTF-8) if
    available and Unicode::UTF8 is not installed
  - The 'touch' method can now set the current time on files that aren't owned,
    as long as they are writeable
  - Improved consistency of symlink support inspection; now always looks at
    $Config{d_symlink}
  - Skips impossible test on 'msys' platform.
- BR: perl-generators where possible
- Drop redundant Group: tag

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.090-2
- Perl 5.24 rebuild

* Tue May  3 2016 Paul Howarth <paul@city-fan.org> - 0.090-1
- Update to 0.090
  - Fix spew_utf8 to allow array references as input

* Mon Apr 18 2016 Paul Howarth <paul@city-fan.org> - 0.088-1
- Update to 0.088
  - Fixed bugs in relative symlink resolution for realpath, spew and edit_lines
  - Symlink resolution will detect circular loops and throw an error

* Mon Apr  4 2016 Paul Howarth <paul@city-fan.org> - 0.086-1
- Update to 0.086
  - Improved documentation of copy and move
- Simplify find command using -delete

* Fri Mar  4 2016 Paul Howarth <paul@city-fan.org> - 0.084-1
- Update to 0.084
  - Fixed relative() for the case with regex metacharacters in the path

* Wed Mar  2 2016 Paul Howarth <paul@city-fan.org> - 0.082-1
- Update to 0.082
  - The relative() method no longer uses File::Spec's buggy rel2abs method;
    the new Path::Tiny algorithm should be comparable and passes File::Spec
    rel2abs test cases, except that it correctly accounts for symlinks
  - Added 'edit' and 'edit_lines' plus _utf8 and _raw variants; this is
    similar to perl's -i flag (though without backups)
  - Fixed lines_utf8() with chomping for repeated empty lines
  - Fixed lines_utf8+chomp and relative() bugs on Windows
  - Documented that subclassing is not supported

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.076-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Nov 16 2015 Paul Howarth <paul@city-fan.org> - 0.076-1
- Update to 0.076
  - Tilde expansion on Windows was resulting in backslashes; now they are
    correctly normalized to forward slashes
  - Typos fixed
  - Fixed spewing to a symlink that crosses a filesystem boundary
  - Add Test::MockRandom to META as a recommended test prerequisite

* Tue Jul 21 2015 Paul Howarth <paul@city-fan.org> - 0.072-1
- Update to 0.072
  - Fixed incorrect error argument for File::Path functions (mkpath and
    remove_tree)

* Mon Jul 20 2015 Paul Howarth <paul@city-fan.org> - 0.070-2
- Fixed incorrect error argument for File::Path functions (mkpath and
  remove_tree) (GH#144)

* Mon Jun 29 2015 Paul Howarth <paul@city-fan.org> - 0.070-1
- Update to 0.070
  - The 'copy' method now returns the object for the copied file
  - The 'visit' method only dereferences the callback return value for scalar
    refs, avoiding some common bugs

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.068-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.068-2
- Perl 5.22 rebuild

* Tue Mar 24 2015 Paul Howarth <paul@city-fan.org> - 0.068-1
- Update to 0.068
  - Added exclusive locking option to filehandle opens; spew now exclusively
    locks tempfile used for atomic writes

* Fri Mar  6 2015 Paul Howarth <paul@city-fan.org> - 0.065-1
- Update to 0.065
  - Added 'assert' method
  - Added 'visit' method
  - Added support for a negative count for 'lines' to get the last lines of a
    file
  - Fixed tilde expansion if path has spaces
  - Make realpath non-fatal if the parent path exists and only the final path
    component does not (was fatal on Windows and some Unixes)
  - Removed redundant locking on tempfile use for spewing
  - Work around File::Temp bugs on older ActiveState Windows Perls
    https://bugs.activestate.com/show_bug.cgi?id=104767
  - Fixed SYNOPSIS example

* Fri Nov 14 2014 Paul Howarth <paul@city-fan.org> - 0.061-1
- Update to 0.061
  - Fixed append_utf8 and append_raw with 'truncate' option

* Thu Nov  6 2014 Paul Howarth <paul@city-fan.org> - 0.060-1
- Update to 0.060
  - Added 'truncate' option to append for in-place replacement of file contents

* Tue Oct 14 2014 Paul Howarth <paul@city-fan.org> - 0.059-1
- Update to 0.059
  - Fixed precedence bug in the check for Unicode::UTF8

* Thu Sep 25 2014 Paul Howarth <paul@city-fan.org> - 0.058-1
- Update to 0.058
  - Added a 'sibling' method as a more efficient form of calling
    $path->parent->child(...).
  - Documentation for every method annotated with the version number of the
    last API change

* Tue Sep 23 2014 Paul Howarth <paul@city-fan.org> - 0.057-1
- Update to 0.057
  - On AIX, reads that default to locking would fail without write permissions,
    because locking needs write permissions; the fix is only to lock reads if
    write permissions exist, otherwise locking is skipped

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.056-2
- Perl 5.20 rebuild

* Thu Aug 14 2014 Paul Howarth <paul@city-fan.org> - 0.056-1
- Update to 0.056
  - Fixed problem throwing errors from 'remove'
  - The 'digest' method now takes a 'chunk_size' option to avoid slurping files
    entirely into memory
  - The 'dirname' method is deprecated due to exposing File::Spec
    inconsistencies
- Use %%license

* Tue Jul  1 2014 Paul Howarth <paul@city-fan.org> - 0.055-1
- Update to 0.055
  - tempfile/tempdir won't warn if used as functions without arguments

* Sat Jun  7 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.054-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May  6 2014 Paul Howarth <paul@city-fan.org> - 0.054-1
- Update to 0.054
  - The 'is_file' method now does -e && ! -d and not -f because -f is often
    more restrictive than people intend or expect
  - Added 'chmod' method with symbolic chmod support ("a=r,u+rx")
  - The 'basename' method now takes a list of suffixes to remove before
    returning the name
  - Added FREEZE/THAW/TO_JSON serialization helpers
  - When constructing a Path::Tiny object from another, the original is
    returned unless it's a temp dir/file, which significantly speeds up calling
    path($path) if $path is already a Path::Tiny object
  - Constructing any path - e.g. with child() - with undef or zero-length
    parts throws an error instead of constructing an invalid path

* Wed Jan 15 2014 Paul Howarth <paul@city-fan.org> - 0.052-1
- Update to 0.052
  - Backslash-to-slash conversion now only happens on Windows (since backslash
    is legal on Unix, we must allow it)

* Sat Dec 21 2013 Paul Howarth <paul@city-fan.org> - 0.051-1
- Update to 0.051
  - Recursive iteration won't throw an exception if a directory is removed or
    unreadable during iteration

* Thu Dec 12 2013 Paul Howarth <paul@city-fan.org> - 0.049-1
- Update to 0.049
  - Added 'subsumes' method
  - The 'chomp' option for 'lines' will remove any end-of-line sequences fully
    instead of just chomping the last character
  - Fixed locking test on AIX
  - Revised locking tests for portability again: locks are now tested from a
    separate process
  - The 'flock' package will no longer indexed by PAUSE
  - Hides warnings and fixes possible fatal errors from pure-perl Cwd,
    particularly on MSWin32
  - Generates filename for atomic writes independent of thread-ID, which fixes
    crashing bug on Win32 when fork() is called

* Fri Oct 18 2013 Paul Howarth <paul@city-fan.org> - 0.044-1
- Update to 0.044
  - Fixed child path construction against the root path
  - Fixed path construction when a relative volume is provided as the first
    argument on Windows; e.g. path("C:", "lib") must be like path("C:lib"),
    not path("C:/lib")
  - On AIX, shared locking is replaced by exclusive locking on a R/W
    filehandle, as locking read handles is not supported

* Mon Oct 14 2013 Paul Howarth <paul@city-fan.org> - 0.043-1
- Update to 0.043
  - Calling 'absolute' on Windows will add the volume if it is missing (e.g.
    "/foo" will become "C:/foo"); this matches the behavior of
    File::Spec->rel2abs
  - Fixed t/00-report-prereqs.t for use with older versions of
    CPAN::Meta::Requirements

* Sun Oct 13 2013 Paul Howarth <paul@city-fan.org> - 0.042-1
- Update to 0.042
  - When 'realpath' can't be resolved (because intermediate directories don't
    exist), the exception now explains the error clearly instead of complaining
    about path() needing a defined, positive-length argument
  - On Windows, fixed resolution of relative paths with a volume, e.g. "C:foo"
    is now correctly translated into getdcwd on "C:" plus "foo"

* Fri Oct 11 2013 Paul Howarth <paul@city-fan.org> - 0.041-1
- Update to 0.041
  - Remove duplicate test dependency on File::Spec that triggers a CPAN.pm bug

* Wed Oct  9 2013 Paul Howarth <paul@city-fan.org> - 0.040-1
- Update to 0.040
  - The 'filehandle' method now offers an option to return locked handles
    based on the file mode
  - The 'filehandle' method now respects default encoding set by the caller's
    open pragma

* Wed Oct  2 2013 Paul Howarth <paul@city-fan.org> - 0.038-1
- Update to 0.038
  - Added 'is_rootdir' method to simplify testing if a path is the root
    directory

* Thu Sep 26 2013 Paul Howarth <paul@city-fan.org> - 0.037-1
- Update to 0.037
  - No longer lists 'threads' as a prerequisite; if you have a threaded perl,
    you have it and if you've not, Path::Tiny doesn't care
  - Fixed for v5.8

* Tue Sep 24 2013 Paul Howarth <paul@city-fan.org> - 0.035-1
- Update to 0.035
  - Fixed flock warning on BSD that was broken with the autodie removal; now
    also applies to all BSD flavors

* Tue Sep 24 2013 Paul Howarth <paul@city-fan.org> - 0.034-1
- Update to 0.034
  - Exceptions are now Path::Tiny::Error objects, not autodie exceptions; this
    removes the last dependency on autodie, which allows us to support Perls as
    far back as v5.8.1
  - BSD/NFS flock fix was not backwards compatible before v5.14; this fixes it
    harder
  - Lowered ExtUtils::MakeMaker configure_requires version to 6.17

* Thu Sep 12 2013 Paul Howarth <paul@city-fan.org> - 0.033-1
- Update to 0.033
  - Perl on BSD may not support locking on an NFS filesystem: if this is
    detected, Path::Tiny warns and continues in an unsafe mode (the 'flock'
    warning category may be fatalized to die instead)
  - Added 'iterator' example showing defaults

* Fri Sep  6 2013 Paul Howarth <paul@city-fan.org> - 0.032-1
- Update to 0.032
  - Removed several test dependencies; Path::Tiny now only needs core modules,
    though some must be upgraded on old Perls

* Tue Sep  3 2013 Paul Howarth <paul@city-fan.org> - 0.031-3
- BR: perl(Config) for the test suite (#1003660)

* Mon Sep  2 2013 Paul Howarth <paul@city-fan.org> - 0.031-2
- Sanitize for Fedora submission

* Mon Sep  2 2013 Paul Howarth <paul@city-fan.org> - 0.031-1
- Initial RPM version
