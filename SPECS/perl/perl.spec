# use "lib", not %%{_lib}, for privlib, sitelib, and vendorlib
# To build production version, we would need -DDEBUGGING=-g

# Perl INC path (perl -V) in search order:
# - /usr/local/share/perl5            -- for CPAN     (site lib)
# - /usr/local/lib[64]/perl5          -- for CPAN     (site arch)
# - /usr/share/perl5/vendor_perl      -- 3rd party    (vendor lib)
# - /usr/lib[64]/perl5/vendor_perl    -- 3rd party    (vendor arch)
# - /usr/share/perl5                  -- Fedora       (priv lib)
# - /usr/lib[64]/perl5                -- Fedora       (arch lib)

%global privlib     %{_prefix}/share/perl5
%global archlib     %{_libdir}/perl5

%global perl_vendorlib  %{privlib}/vendor_perl
%global perl_vendorarch %{archlib}/vendor_perl

%define _unpackaged_files_terminate_build 0

%global perl_version    5.34.1
%global perl_epoch      4
%global perl_arch_stem -thread-multi
%global perl_archname %{_arch}-%{_os}%{perl_arch_stem}

%global perl_bootstrap 1

%global multilib_64_archs aarch64 x86_64
%global parallel_tests 1
%global tapsetdir   %{_datadir}/systemtap/tapset

%global dual_life 0
%global rebuild_from_scratch %{defined perl_bootstrap}

# This overrides filters from build root (/usr/lib/rpm/macros.d/macros.perl)
# intentionally (unversioned perl(DB) is removed and versioned one is kept).
%global __provides_exclude_from .*(%{_docdir}|%{archlib}/.*\\.pl|%{privlib}/.*\\.pl)$
%global __requires_exclude_from %{_docdir}
%global __provides_exclude perl\\((VMS|Win32|BSD::|DB\\)$)
%global __requires_exclude perl\\((VMS|BSD::|Win32|Tk|Mac::|Your::Module::Here)
# same as we provide in /usr/lib/rpm/macros.d/macros.perl
%global perl5_testdir   %{_libexecdir}/perl5-tests

# Optional features
# Run C++ tests
%bcond_without perl_enables_cplusplus_test
# We can bootstrap without gdbm
%bcond_without gdbm
# Support for groff, bug #135101
%bcond_with perl_enables_groff
# Run Turkish locale tests
%bcond_with perl_enables_turkish_test
# Run syslog tests
%bcond_with perl_enables_syslog_test
# SystemTap support
%bcond_with perl_enables_systemtap
# <> operator uses File::Glob nowadays. CSH is not needed.
%bcond_with perl_enables_tcsh
# We can skip %%check phase
%bcond_with test

# The additional linker flags break binary perl- packages.
# https://bugzilla.redhat.com/show_bug.cgi?id=2043092
%undefine _package_note_file

# Skip module metadata notes for perl due to issue with embedded build ldflags
%undefine mariner_module_ldflags

Name:           perl
# These are all found licenses. They are distributed among various
# subpackages.
# dist/Tie-File/lib/Tie/File.pm:        GPLv2+ or Artistic
# cpan/Getopt-Long/lib/Getopt/Long.pm:  GPLv2+ or Artistic
# cpan/Compress-Raw-Zlib/Zlib.xs:       (GPL+ or Artistic) and zlib
# cpan/Digest-MD5/MD5.xs:               (GPL+ or Artistic) and BSD
# cpan/Time-Piece/Piece.xs:             (GPL+ or Artistic) and BSD
# dist/PathTools/Cwd.xs:                (GPL+ or Artistic) and BSD
# util.c:                               (GPL+ or Artistic) and BSD
# cpan/perlfaq/lib/perlfaq4.pod:        (GPL+ or Artistic) and Public Domain
# cpan/Test-Simple/lib/Test/Tutorial.pod:   (GPL+ or Artistic) and
#                                           Public Domain
# cpan/MIME-Base64/Base64.xs:           (GPL+ or Artistic) and MIT
# cpan/Test-Simple/lib/ok.pm:           CC0
# cpan/Text-Tabs/lib/Text/Wrap.pm:      TTWL
# cpan/Encode/bin/encguess:             Artistic 2.0
# cpan/libnet/lib/Net/libnetFAQ.pod:    Artistic    (CPAN RT#117888)
# cpan/Unicode-Collate/Collate/allkeys.txt:     Unicode
# inline.h:                             MIT
# lib/unicore:                          UCD
# ext/SDBM_File/sdbm.{c,h}:             Public domain
# regexec.c, regcomp.c:                 HSRL
# cpan/Locale-Maketext-Simple/lib/Locale/Maketext/Simple.pm:    MIT (with
#                                       exception for Perl)
# time64.c:                             MIT
# perly.h:                              GPLv3+ with Bison exception
# pod/perlpodstyle.pod:                 MIT
# pod/perlunicook.pod:                  (GPL+ or Artistic) and Public Domain
# pod/perlgpl.pod:                      GPL text
# pod/perlartistic.pod:                 Artistic text
# ext/File-Glob/bsd_glob.{c,h}:         BSD
# Other files:                          GPL+ or Artistic
## Not in a binary package
# ebcdic_tables.h:                                  MIT
# cpan/podlators/t/docs/pod.t:                      MIT
# cpan/podlators/t/docs/pod-spelling.t:             MIT
# cpan/podlators/t/docs/spdx-license.t:             MIT
# cpan/podlators/t/docs/synopsis.t:                 MIT
# cpan/podlators/t/docs/urls.t :                    MIT
# cpan/podlators/t/lib/Test/RRA.pm:                 MIT
# cpan/podlators/t/lib/Test/RRA/Config.pm:          MIT
# cpan/podlators/t/lib/Test/RRA/ModuleVersion.pm:   MIT
# cpan/podlators/t/style/minimum-version.t:         MIT
# cpan/podlators/t/style/module-version.t:          MIT
# cpan/podlators/t/style/strict.t:                  MIT
# cpan/Term-ANSIColor/t/lib/Test/RRA/Config.pm:     MIT
## Unbundled
# cpan/Compress-Raw-Bzip2/bzip2-src:    BSD
# cpan/Compress-Raw-Zlib/zlib-src:      zlib
# perl.h (EBDIC parts)                              MIT
## perl sub-package notice
# perluniprops.pod is generated from lib/unicore sources:   UCD
# uni_keywords.h is generated from lib/unicore sources:     UCD
#
# This sub-subpackage doesn't contain any copyrightable material.
# Nevertheless, it needs a License tag, so we'll use the generic
# "perl" license.
License:        GPL+ or Artistic
Epoch:          %{perl_epoch}
Version:        %{perl_version}
# release number must be even higher, because dual-lived modules will be broken otherwise
Release:        489%{?dist}
Summary:        Practical Extraction and Report Language
Url:            https://www.perl.org/
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://www.cpan.org/src/5.0/perl-%{perl_version}.tar.xz
Source3:        macros.perl
# Tom Christiansen confirms Pod::Html uses the same license as perl
Source6:        Pod-Html-license-clarification

# Pregenerated dependencies for bootstrap.
# If your RPM tool fails on including the source file, then you forgot to
# define _sourcedir macro to point to the directory with the sources.
Source7:        gendep.macros
%if %{defined perl_bootstrap}
%include %{SOURCE7}
%endif

# Provide maybe_command independently, bug #1129443
Patch5:         perl-5.22.1-Provide-ExtUtils-MM-methods-as-standalone-ExtUtils-M.patch

# Define SONAME for libperl.so
Patch8:         perl-5.16.3-create_libperl_soname.patch

# Install libperl.so to -Dshrpdir value
Patch9:         perl-5.22.0-Install-libperl.so-to-shrpdir-on-Linux.patch

# Make *DBM_File desctructors thread-safe, bug #1107543, RT#61912
Patch10:        perl-5.34.0-Destroy-GDBM-NDBM-ODBM-SDBM-_File-objects-only-from-.patch

# Replace ExtUtils::MakeMaker dependency with ExtUtils::MM::Utils.
# This allows not to require perl-devel. Bug #1129443
Patch11:        perl-5.22.1-Replace-EU-MM-dependnecy-with-EU-MM-Utils-in-IPC-Cmd.patch

# Link XS modules to pthread library to fix linking with -z defs,
# <https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/message/3RHZEHLRUHJFF2XGHI5RB6YPDNLDR4HG/>
Patch12:        perl-5.27.8-hints-linux-Add-lphtread-to-lddlflags.patch

# Pass the correct CFLAGS to dtrace
Patch13:        perl-5.28.0-Pass-CFLAGS-to-dtrace.patch

# Link XS modules to libperl.so with EU::CBuilder on Linux, bug #960048
Patch200:       perl-5.16.3-Link-XS-modules-to-libperl.so-with-EU-CBuilder-on-Li.patch

# Link XS modules to libperl.so with EU::MM on Linux, bug #960048
Patch201:       perl-5.16.3-Link-XS-modules-to-libperl.so-with-EU-MM-on-Linux.patch

# Update some of the bundled modules
# see http://fedoraproject.org/wiki/Perl/perl.spec for instructions

BuildRequires:  bash
BuildRequires:  bzip2-devel
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
%if %{with gdbm}
BuildRequires:  gdbm-devel
%endif
# glibc-common for iconv
BuildRequires:  glibc-common
%if %{with perl_enables_groff}
# Build-require groff tools for populating %%Config correctly, bug #135101
BuildRequires:  groff-base
%endif
BuildRequires:  make
%if !%{defined perl_bootstrap}
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
%endif
BuildRequires:  sed
%if %{with perl_enables_systemtap}
BuildRequires:  systemtap-sdt-devel
%endif
BuildRequires:  tar
%if %{with perl_enables_tcsh}
BuildRequires:  tcsh
%endif
BuildRequires:  zlib-devel

# For tests
%if %{with test}
%if %{with perl_enables_cplusplus_test}
# An optional ExtUtils-CBuilder's test
BuildRequires:  gcc-c++
%endif
BuildRequires:  procps
%if %{with perl_enables_turkish_test}
# An optional t/re/fold_grind_T.t test
BuildRequires:  glibc-langpack-tr
%endif
%if %{with perl_enables_syslog_test}
BuildRequires:  rsyslog
%endif
%endif


# compat macro needed for rebuild
%global perl_compat perl(:MODULE_COMPAT_5.34.1)

Requires:       %perl_compat
Requires:       perl-interpreter%{?_isa} = %{perl_epoch}:%{perl_version}-%{release}
Requires:       perl-libs%{?_isa} = %{perl_epoch}:%{perl_version}-%{release}
Requires:       perl-devel%{?_isa} = %{perl_epoch}:%{perl_version}-%{release}
Requires:       perl-macros
Requires:       perl-utils
%if %{defined perl_bootstrap}
%gendep_perl
%endif

Requires:       perl-Archive-Tar, perl-Attribute-Handlers, perl-autodie,
Requires:       perl-AutoLoader, perl-AutoSplit, perl-autouse,
Requires:       perl-B, perl-base, perl-Benchmark, perl-bignum, perl-blib,
Requires:       perl-Carp, perl-Class-Struct,
Requires:       perl-Compress-Raw-Bzip2, perl-Compress-Raw-Zlib,
Requires:       perl-Config-Extensions, perl-Config-Perl-V, perl-constant,
Requires:       perl-CPAN, perl-CPAN-Meta, perl-CPAN-Meta-Requirements,
Requires:       perl-CPAN-Meta-YAML,
Requires:       perl-Data-Dumper, perl-DBM_Filter,
Requires:       perl-debugger, perl-deprecate,
Requires:       perl-Devel-Peek, perl-Devel-PPPort, perl-Devel-SelfStubber,
Requires:       perl-diagnostics, perl-Digest, perl-Digest-MD5, perl-Digest-SHA,
Requires:       perl-DirHandle,
Requires:       perl-doc,
Requires:       perl-Dumpvalue,
Requires:       perl-DynaLoader,
Requires:       perl-Encode, perl-Encode-devel, perl-encoding,
Requires:       perl-encoding-warnings, perl-English,
Requires:       perl-Env, perl-Errno, perl-experimental, perl-Exporter,
Requires:       perl-ExtUtils-CBuilder, perl-ExtUtils-Constant,
Requires:       perl-ExtUtils-Command,
Requires:       perl-ExtUtils-Embed, perl-ExtUtils-Install,
Requires:       perl-ExtUtils-MakeMaker, perl-ExtUtils-Manifest,
Requires:       perl-ExtUtils-Miniperl, perl-ExtUtils-MM-Utils,
Requires:       perl-ExtUtils-ParseXS,
Requires:       perl-Fcntl, perl-fields,
Requires:       perl-File-Basename, perl-File-Compare, perl-File-Copy,
Requires:       perl-File-DosGlob, perl-File-Fetch,
Requires:       perl-File-Find, perl-File-Path, perl-File-stat, perl-File-Temp,
Requires:       perl-FileCache, perl-FileHandle, perl-filetest,
Requires:       perl-Filter, perl-Filter-Simple,
Requires:       perl-FindBin,
%if %{with gdbm}
Requires:       perl-GDBM_File,
%endif
Requires:       perl-Getopt-Long, perl-Getopt-Std,
Requires:       perl-Hash-Util, perl-Hash-Util-FieldHash, perl-HTTP-Tiny,
Requires:       perl-if, perl-IO, perl-IO-Compress, perl-IO-Socket-IP,
Requires:       perl-IO-Zlib, perl-IPC-Cmd, perl-IPC-Open3, perl-IPC-SysV,
Requires:       perl-I18N-Collate, perl-I18N-Langinfo, perl-I18N-LangTags,
Requires:       perl-JSON-PP,
Requires:       perl-less,
Requires:       perl-lib, perl-libnet, perl-libnetcfg,
Requires:       perl-locale, perl-Locale-Maketext, perl-Locale-Maketext-Simple,
Requires:       perl-Math-BigInt, perl-Math-BigInt-FastCalc, perl-Math-BigRat,
Requires:       perl-Math-Complex, perl-Memoize, perl-meta-notation,
Requires:       perl-MIME-Base64,
Requires:       perl-Module-CoreList, perl-Module-CoreList-tools,
Requires:       perl-Module-Load, perl-Module-Load-Conditional,
Requires:       perl-Module-Loaded, perl-Module-Metadata,
Requires:       perl-mro,
%if %{with gdbm}
Requires:       perl-NDBM_File,
%endif
Requires:       perl-Net, perl-Net-Ping, perl-NEXT,
%if %{with gdbm}
Requires:       perl-ODBM_File,
%endif
Requires:       perl-Opcode, perl-open, perl-overload, perl-overloading,
Requires:       perl-parent, perl-PathTools, perl-Params-Check, perl-perlfaq,
Requires:       perl-PerlIO-via-QuotedPrint, perl-Perl-OSType,
Requires:       perl-ph,
Requires:       perl-Pod-Checker, perl-Pod-Escapes, perl-Pod-Functions,
Requires:       perl-Pod-Html, perl-Pod-Perldoc,
Requires:       perl-Pod-Simple, perl-Pod-Usage, perl-podlators, perl-POSIX,
Requires:       perl-Safe, perl-Scalar-List-Utils,
Requires:       perl-Search-Dict, perl-SelectSaver,
Requires:       perl-SelfLoader, perl-sigtrap, perl-Socket, perl-sort,
Requires:       perl-Storable,
Requires:       perl-subs,
Requires:       perl-Symbol, perl-Sys-Hostname, perl-Sys-Syslog,
Requires:       perl-Term-ANSIColor, perl-Term-Cap, perl-Term-Complete,
Requires:       perl-Term-ReadLine,
Requires:       perl-Test, perl-Test-Harness, perl-Test-Simple,
Requires:       perl-Text-Abbrev, perl-Text-Balanced, perl-Text-ParseWords,
Requires:       perl-Text-Tabs+Wrap,
Requires:       perl-Thread, perl-Thread-Queue, perl-Thread-Semaphore,
Requires:       perl-threads, perl-threads-shared,
Requires:       perl-Tie, perl-Tie-File, perl-Tie-Memoize, perl-Tie-RefHash,
Requires:       perl-Time, perl-Time-HiRes, perl-Time-Local, perl-Time-Piece,
Requires:       perl-Unicode-Collate, perl-Unicode-Normalize, perl-Unicode-UCD,
Requires:       perl-User-pwent,
Requires:       perl-vars, perl-version, perl-vmsish,

# Full EVR is for compatibility with systems that swapped perl and perl-core
# <https://fedoraproject.org/wiki/Changes/perl_Package_to_Install_Core_Modules>,
# bug #1464903.
Provides:       perl-core = %{perl_version}-%{release}
Provides:       perl-core%{?_isa} = %{perl_version}-%{release}


%description
Perl is a high-level programming language with roots in C, sed, awk and shell
scripting. Perl is good at handling processes and files, and is especially
good at handling text. Perl's hallmarks are practicality and efficiency.
While it is used to do a lot of different things, Perl's most common
applications are system administration utilities and web programming.

This is a metapackage with all the Perl bits and core modules that can be
found in the upstream tarball from perl.org.

If you need only a specific feature, you can install a specific package
instead. E.g. to handle Perl scripts with %{_bindir}/perl interpreter,
install perl-interpreter package. See perl-interpreter description for more
details on the Perl decomposition into packages.


%package interpreter
Summary:        Standalone executable Perl interpreter
License:        GPL+ or Artistic
# perl-interpreter denotes a package with the perl executable.
# Full EVR is for compatibility with systems that swapped perl and perl-core
# <https://fedoraproject.org/wiki/Changes/perl_Package_to_Install_Core_Modules>,
# bug #1464903.
Version:        %{perl_version}
Epoch:          %{perl_epoch}

Requires:       perl-libs%{?_isa} = %{perl_epoch}:%{perl_version}-%{release}
# Require this till perl-interpreter sub-package provides any modules
Requires:       %perl_compat
Suggests:       perl-doc = %{perl_version}-%{release}
%if %{defined perl_bootstrap}
%gendep_perl_interpreter
%endif

# We need this to break the dependency loop, and ensure that perl-libs 
# gets installed before perl-interpreter.
Requires(post): perl-libs
# Same as perl-libs. We need macros in basic buildroot.
Requires(post): perl-macros

Provides: /bin/perl


%description interpreter
This is a Perl interpreter as a standalone executable %{_bindir}/perl
required for handling Perl scripts. It does not provide all the other Perl
modules or tools.

Install this package if you want to program in Perl or enable your system to
handle Perl scripts with %{_bindir}/perl interpreter.

If your script requires some Perl modules, you can install them with
"perl(MODULE)" where "MODULE" is a name of required module. E.g. install
"perl(Test::More)" to make Test::More Perl module available.

If you need all the Perl modules that come with upstream Perl sources, so
called core modules, install perl package.

If you only need perl run-time as a shared library, i.e. Perl interpreter
embedded into another application, the only essential package is perl-libs.

Perl header files can be found in perl-devel package.

Perl utils like "h2ph" or "perlbug" can be found in perl-utils package.

Perl debugger, usually invoked with "perl -d", is available in perl-debugger
package.


%package libs
Summary:        The libraries for the perl run-time
License:        (GPL+ or Artistic) and BSD and HSRL and MIT and UCD and Public domain
# Compat provides
Provides:       %perl_compat
Provides:       perl(:MODULE_COMPAT_5.34.0)
# Interpreter version to fulfil required genersted from "require 5.006;"
Provides:       perl(:VERSION) = %{perl_version}
# Integeres are 64-bit on all platforms
Provides:       perl(:WITH_64BIT)
# Threading provides
Provides:       perl(:WITH_ITHREADS)
Provides:       perl(:WITH_THREADS)
# Largefile provides
Provides:       perl(:WITH_LARGEFILES)
# PerlIO provides
Provides:       perl(:WITH_PERLIO)
# A file provide for bytes module
Provides:       perl(bytes_heavy.pl)
# Loaded by charnames, unicore/Name.pm does not declare unicore::Name module
Provides:       perl(unicore::Name)
# Keep utf8 modules in perl-libs because a sole regular expression like /\pN/
# causes loading utf8 and unicore/Heave.pl and unicore/lib files.
Provides:       perl(utf8_heavy.pl)
# utf8 and utf8_heavy.pl require Carp, re, strict, warnings, XSLoader
# XSLoader requires DynaLoder
Requires:       perl(DynaLoader)
# Encode is loaded in BOOT section of PerlIO::encoding
Requires:       perl(Encode)
# File::Spec loaded by _charnames.pm that is loaded by \N{}
Requires:       perl(File::Spec)
%if %{with gdbm}
# For AnyDBM_File
Suggests:       perl(GDBM_File)
Recommends:     perl(NDBM_File)
Suggests:       perl(ODBM_File)
%endif
# Term::Cap is optional
%if %{defined perl_bootstrap}
%gendep_perl_libs
%endif

# Remove private redefinitions
# XSLoader redefines DynaLoader name space for compatibility, but it still
# loads DynaLoader.pm (though DynaLoader.xs is compiled into libperl).
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\((charnames|DynaLoader)\\)$

%description libs
The is a perl run-time (interpreter as a shared library and include
directories).


%package devel
Summary:        Header files for use in perl development
# l1_char_class_tab.h is generated from lib/unicore sources:    UCD
License:        (GPL+ or Artistic) and UCD
%if %{with perl_enables_systemtap}
Requires:       systemtap-sdt-devel
%endif
Requires:       perl(ExtUtils::ParseXS)
Requires:       %perl_compat
# Match library and header files when downgrading releases
Requires:       perl-libs%{?_isa} = %{perl_epoch}:%{perl_version}-%{release}
Recommends:     perl-doc = %{perl_version}-%{release}
# Devel::PPPort for h2xs script
Requires:       perl(Devel::PPPort)
# Compiler and linker options stored into perl and used when building XS
# modules refer to hardening profiles like
# /usr/lib/rpm/mariner/default-hardened-cc1 that are delivered by
# mariner-rpm-macros. Bug #1557667.
Requires:       mariner-rpm-macros

%if %{defined perl_bootstrap}
%gendep_perl_devel
%endif

%description devel
This package contains header files and development modules.
Most perl packages will need to install perl-devel to build.


%package macros
Summary:        Macros for rpmbuild
License:        GPL+ or Artistic
BuildArch:      noarch
Requires:       %perl_compat
Requires:       perl-interpreter
%if %{defined perl_bootstrap}
%gendep_perl_macros
%endif

%description macros
RPM macros that are handy when building binary RPM packages.


%package tests
Summary:        The Perl test suite
License:        GPL+ or Artistic
# right?
AutoReqProv:    0
Requires:       %perl_compat
# FIXME - note this will need to change when doing the core/minimal swizzle
Requires:       perl
%if %{defined perl_bootstrap}
%gendep_perl_tests
%endif

%description tests
This package contains the test suite included with Perl %{perl_version}.

Install this if you want to test your Perl installation (binary and core
modules).


%package utils
Summary:        Utilities packaged with the Perl distribution
License:        GPL+ or Artistic
Epoch:          0
Version:        %{perl_version}
BuildArch:      noarch
# Match library exactly for perlbug version string
Requires:       perl-libs = %{perl_epoch}:%{perl_version}-%{release}
# Keep /usr/sbin/sendmail and Module::CoreList optional for the perlbug tool
%if %{defined perl_bootstrap}
%gendep_perl_utils
%endif

%description utils
Several utilities which come with Perl distribution like h2ph, perlbug,
perlthanks, and pl2pm. Some utilities are provided by more specific
packages like perldoc by perl-Pod-Perldoc and splain by perl-diagnostics.

%if %{dual_life} || %{rebuild_from_scratch}
%package Archive-Tar
Summary:        A module for Perl manipulation of .tar files
License:        GPL+ or Artistic
Epoch:          0
Version:        2.38
BuildArch:      noarch
Requires:       %perl_compat
Requires:       perl(IO::Zlib) >= 1.01
# Optional run-time:
Requires:       perl(IO::Compress::Bzip2) >= 2.015
# IO::String not used if perl supports useperlio which is true
# Use Compress::Zlib's version for IO::Uncompress::Bunzip2
Requires:       perl(IO::Uncompress::Bunzip2) >= 2.015
%if !%{defined perl_bootstrap}
Requires:       perl(Text::Diff)
%endif
%if %{defined perl_bootstrap}
%gendep_perl_Archive_Tar
%endif

%description Archive-Tar
Archive::Tar provides an object oriented mechanism for handling tar files.  It
provides class methods for quick and easy files handling while also allowing
for the creation of tar file objects for custom manipulation.  If you have the
IO::Zlib module installed, Archive::Tar will also support compressed or
gzipped tar files.
%endif

%package Attribute-Handlers
Summary:        Simpler definition of attribute handlers
License:        GPL+ or Artistic
Epoch:          0
Version:        1.01
BuildArch:      noarch
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Attribute_Handlers
%endif

%description Attribute-Handlers
This Perl module, when inherited by a package, allows that package's class to
define attribute handler subroutines for specific attributes. Variables and
subroutines subsequently defined in that package, or in packages derived from
that package may be given attributes with the same names as the attribute
handler subroutines, which will then be called in one of the compilation
phases (i.e. in a "BEGIN", "CHECK", "INIT", or "END" block).

%if %{dual_life} || %{rebuild_from_scratch}
%package autodie
Summary:        Replace functions with ones that succeed or die
License:        GPL+ or Artistic
Epoch:          0
Version:        2.34
Requires:       %perl_compat
BuildArch:      noarch
Requires:       perl(B)
Requires:       perl(Fcntl)
Requires:       perl(overload)
Requires:       perl(POSIX)
%if %{defined perl_bootstrap}
%gendep_perl_autodie
%endif

%description autodie
The "autodie" and "Fatal" pragma provides a convenient way to replace
functions that normally return false on failure with equivalents that throw an
exception on failure.

However "Fatal" has been obsoleted by the new autodie pragma. Please use
autodie in preference to "Fatal".
%endif

%package AutoLoader
Summary:        Load subroutines only on demand
License:        GPL+ or Artistic
Epoch:          0
Version:        5.74
BuildArch:      noarch
Requires:       %perl_compat
Requires:       perl(Carp)
%if %{defined perl_bootstrap}
%gendep_perl_AutoLoader
%endif

%description AutoLoader
The AutoLoader module works with the AutoSplit module and the "__END__" token
to defer the loading of some subroutines until they are used rather than
loading them all at once.

%package AutoSplit
Summary:        Split a package for automatic loading
License:        GPL+ or Artistic
Epoch:          0
# Real version 1.06
Version:        5.74
BuildArch:      noarch
Requires:       %perl_compat
Requires:       perl(Carp)
%if %{defined perl_bootstrap}
%gendep_perl_AutoSplit
%endif

%description AutoSplit
Split up your program into files that the AutoLoader module can handle. It is
used by both the standard Perl libraries and by the ExtUtils::MakeMaker
utility, to automatically configure libraries for automatic loading.

%package autouse
Summary:        Postpone load of modules until a function is used
License:        GPL+ or Artistic
Epoch:          0
Version:        1.11
BuildArch:      noarch
Requires:       %perl_compat
Requires:       perl(Carp)
Requires:       perl(warnings)
%if %{defined perl_bootstrap}
%gendep_perl_autouse
%endif

%description autouse
If a module is not loaded yet, then the autouse declaration declares functions
in the current package. When these functions are called, they load the package
and substitute themselves with the correct definitions.

%package B
Summary:        Perl compiler backend
License:        GPL+ or Artistic
Epoch:          0
Version:        1.82
Requires:       %perl_compat
Requires:       perl(Data::Dumper)
Requires:       perl(overloading)
Requires:       perl(XSLoader)
%if %{defined perl_bootstrap}
%gendep_perl_B
%endif


%description B
The "B" module supplies classes which allow a Perl program to delve into its
own innards. It is the module used to implement the backends of the Perl
compiler.

%package base
Summary:        Establish an ISA relationship with base classes at compile time
License:        GPL+ or Artistic
Epoch:          0
Version:        2.27
BuildArch:      noarch
Requires:       %perl_compat
Requires:       perl(Carp)
%if %{defined perl_bootstrap}
%gendep_perl_base
%endif

%description base
"base" module allows you to both load one or more modules, while setting up
inheritance from those modules at the same time.  Unless you are using the
"fields" pragma, consider this module discouraged in favor of the
lighter-weight "parent".

%package Benchmark
Summary:        Benchmark running times of Perl code
License:        GPL+ or Artistic
Epoch:          0
Version:        1.23
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Benchmark
%endif
BuildArch:      noarch


%description Benchmark
The Benchmark module encapsulates a number of routines to help you figure out
how long it takes to execute some code.

%if %{dual_life} || %{rebuild_from_scratch}
%package bignum
Summary:        Transparent big number support for Perl
License:        GPL+ or Artistic
Epoch:          0
Version:        0.51
Requires:       %perl_compat
Requires:       perl(Carp)
# Math::BigInt::Lite is optional
Requires:       perl(Math::BigRat)
Requires:       perl(warnings)
BuildArch:      noarch
%if %{defined perl_bootstrap}
%gendep_perl_bignum
%endif

%description bignum
This package attempts to make it easier to write scripts that use BigInts and
BigFloats in a transparent way.
%endif

%package blib
Summary:        Use uninstalled version of a package
License:        GPL+ or Artistic
Epoch:          0
Version:        1.07
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_blib
%endif
BuildArch:      noarch


%description blib
This module looks for MakeMaker-like "blib" directory structure starting in
given or current directory and working back up to five levels of directories.
It is intended for use on command line with -M option as a way of testing
arbitrary scripts against an uninstalled version of a package.

%if %{dual_life} || %{rebuild_from_scratch}
%package Carp
Summary:        Alternative warn and die for modules
Epoch:          0
# Real version 1.52
Version:        1.52
License:        GPL+ or Artistic
Requires:       %perl_compat
Provides:       perl(Carp::Heavy) = %{version}
%if %{defined perl_bootstrap}
%gendep_perl_Carp
%endif
BuildArch:      noarch

# Do not export unversioned module
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(Carp\\)\\s*$

%description Carp
The Carp routines are useful in your own modules because they act like
die() or warn(), but with a message which is more likely to be useful to a
user of your module. In the case of cluck, confess, and longmess that
context is a summary of every call in the call-stack. For a shorter message
you can use carp or croak which report the error as being from where your
module was called. There is no guarantee that that is where the error was,
but it is a good educated guess.
%endif

%package Class-Struct
Summary:        Declare struct-like data types as Perl classes
License:        GPL+ or Artistic
Epoch:          0
Version:        0.66
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Class_Struct
%endif
BuildArch:      noarch


%description Class-Struct
Class::Struct module exports a single function struct(). Given a list of
element names and types, and optionally a class name, struct() creates a
Perl 5 class that implements a struct-like data structure.

%if %{dual_life} || %{rebuild_from_scratch}
%package Compress-Raw-Bzip2
Summary:        Low-Level Interface to bzip2 compression library
License:        GPL+ or Artistic
Epoch:          0
Version:        2.101
Requires:       perl(Exporter), perl(File::Temp)
%if %{defined perl_bootstrap}
%gendep_perl_Compress_Raw_Bzip2
%endif

%description Compress-Raw-Bzip2
This module provides a Perl interface to the bzip2 compression library.
It is used by IO::Compress::Bzip2.

%package Compress-Raw-Zlib
Summary:        Low-Level Interface to the zlib compression library
License:        (GPL+ or Artistic) and zlib
Epoch:          0
Version:        2.101
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Compress_Raw_Zlib
%endif

%description Compress-Raw-Zlib
This module provides a Perl interface to the zlib compression library.
It is used by IO::Compress::Zlib.
%endif

%package Config-Extensions
Summary:        Hash lookup of which Perl core extensions were built
License:        GPL+ or Artistic
Epoch:          0
Version:        0.03
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Config_Extensions
%endif
BuildArch:      noarch


%description Config-Extensions
The Config::Extensions module provides a hash %%Extensions containing all the
core extensions that were enabled for this perl.

%if %{dual_life} || %{rebuild_from_scratch}
%package Config-Perl-V
Summary:        Structured data retrieval of perl -V output
License:        GPL+ or Artistic
Epoch:          0
Version:        0.33
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Config_Perl_V
%endif
BuildArch:      noarch

%description Config-Perl-V
The command "perl -V" will return you an excerpt from the %%Config::Config
hash combined with the output of "perl -V" that is not stored inside the hash,
but only available to the perl binary itself. This package provides Perl
module that will return you the output of "perl -V" in a structure.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package constant
Summary:        Perl pragma to declare constants
License:        GPL+ or Artistic
Epoch:          0
Version:        1.33
Requires:       %perl_compat
Requires:       perl(Carp)
%if %{defined perl_bootstrap}
%gendep_perl_constant
%endif
BuildArch:      noarch

%description constant
This pragma allows you to declare constants at compile-time:

use constant PI => 4 * atan2(1, 1);

When you declare a constant such as "PI" using the method shown above,
each machine your script runs upon can have as many digits of accuracy
as it can use. Also, your program will be easier to read, more likely
to be maintained (and maintained correctly), and far less likely to
send a space probe to the wrong planet because nobody noticed the one
equation in which you wrote 3.14195.

When a constant is used in an expression, Perl replaces it with its
value at compile time, and may then optimize the expression further.
In particular, any code in an "if (CONSTANT)" block will be optimized
away if the constant is false.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package CPAN
Summary:        Query, download and build perl modules from CPAN sites
License:        GPL+ or Artistic
Epoch:          0
Version:        2.28
Requires:       make
Requires:       %perl_compat
# Some subpackaged modules are not dual-lived. E.g. "open". If a distribution
# on CPAN declares a dependency on such module, CPAN client will fail,
# because the only provider is a perl distribution.
# Another issue is with dual-lived modules whose distribution actually does
# not declare all needed core dependencies and the installation would also
# fail.
# As a result, any CPAN client must run-require the complete perl.
Requires:       perl
# Prefer Archive::Tar and Compress::Zlib over tar and gzip
Requires:       perl(Archive::Tar) >= 1.50
Requires:       perl(base)
Requires:       perl(Data::Dumper)
%if !%{defined perl_bootstrap}
Requires:       perl(Devel::Size)
%endif
Requires:       perl(ExtUtils::Manifest)
%if !%{defined perl_bootstrap}
Requires:       perl(File::HomeDir) >= 0.65
%endif
Requires:       perl(File::Temp) >= 0.16
Requires:       perl(lib)
Requires:       perl(Net::Config)
Requires:       perl(Net::FTP)
Requires:       perl(POSIX)
Requires:       perl(Term::ReadLine)
%if !%{defined perl_bootstrap}
Requires:       perl(URI)
Requires:       perl(URI::Escape)
%endif
Requires:       perl(User::pwent)
# Optional but higly recommended:
%if !%{defined perl_bootstrap}
Requires:       perl(Archive::Zip)
Requires:       perl(Compress::Bzip2)
Requires:       perl(CPAN::Meta) >= 2.110350
%endif
Requires:       perl(Compress::Zlib)
Requires:       perl(Digest::MD5)
# CPAN encourages Digest::SHA strongly because of integrity checks
Requires:       perl(Digest::SHA)
Requires:       perl(Dumpvalue)
Requires:       perl(ExtUtils::CBuilder)
%if ! %{defined perl_bootstrap}
# Avoid circular deps local::lib -> Module::Install -> CPAN when bootstraping
# local::lib recommended by CPAN::FirstTime default choice, bug #1122498
Requires:       perl(local::lib)
%endif
%if ! %{defined perl_bootstrap}
Requires:       perl(Module::Build)
%endif
%if ! %{defined perl_bootstrap}
Requires:       perl(Text::Glob)
%endif
Provides:       cpan = %{version}
%if %{defined perl_bootstrap}
%gendep_perl_CPAN
%endif
BuildArch:      noarch

%description CPAN
The CPAN module automates or at least simplifies the make and install of
perl modules and extensions. It includes some primitive searching
capabilities and knows how to use LWP, HTTP::Tiny, Net::FTP and certain
external download clients to fetch distributions from the net.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package CPAN-Meta
Summary:        Distribution metadata for a CPAN dist
Epoch:          0
Version:        2.150010
License:        GPL+ or Artistic
Requires:       %perl_compat
Requires:       perl(CPAN::Meta::YAML) >= 0.011
Requires:       perl(Encode)
Requires:       perl(JSON::PP) >= 2.27300
%if %{defined perl_bootstrap}
%gendep_perl_CPAN_Meta
%endif
BuildArch:      noarch

%description CPAN-Meta
Software distributions released to the CPAN include a META.json or, for
older distributions, META.yml, which describes the distribution, its
contents, and the requirements for building and installing the
distribution. The data structure stored in the META.json file is described
in CPAN::Meta::Spec.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package CPAN-Meta-Requirements
Summary:        Set of version requirements for a CPAN dist
Epoch:          0
# Real version 2.140
Version:        2.140
License:        GPL+ or Artistic
Requires:       %perl_compat
BuildArch:      noarch
# CPAN-Meta-Requirements used to have six decimal places
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(CPAN::Meta::Requirements\\)
Provides:       perl(CPAN::Meta::Requirements) = %{version}000
%if %{defined perl_bootstrap}
%gendep_perl_CPAN_Meta_Requirements
%endif

%description CPAN-Meta-Requirements
A CPAN::Meta::Requirements object models a set of version constraints like
those specified in the META.yml or META.json files in CPAN distributions.
It can be built up by adding more and more constraints, and it will reduce
them to the simplest representation.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package CPAN-Meta-YAML
Version:        0.018
Epoch:          0
Summary:        Read and write a subset of YAML for CPAN Meta files
License:        GPL+ or Artistic
BuildArch:      noarch
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_CPAN_Meta_YAML
%endif

%description CPAN-Meta-YAML
This module implements a subset of the YAML specification for use in reading
and writing CPAN metadata files like META.yml and MYMETA.yml. It should not be
used for any other general YAML parsing or generation task.
%endif


%if %{dual_life} || %{rebuild_from_scratch}
%package Data-Dumper
Summary:        Stringify perl data structures, suitable for printing and eval
License:        GPL+ or Artistic
Epoch:          0
Version:        2.179
Requires:       %perl_compat
Requires:       perl(B::Deparse)
Requires:       perl(bytes)
Requires:       perl(Scalar::Util)
Requires:       perl(XSLoader)
%if %{defined perl_bootstrap}
%gendep_perl_Data_Dumper
%endif

%description Data-Dumper
Given a list of scalars or reference variables, writes out their contents
in perl syntax. The references can also be objects. The content of each
variable is output in a single Perl statement. Handles self-referential
structures correctly.
%endif

%package DBM_Filter
Summary:        Filter DBM keys and values
License:        GPL+ or Artistic
Epoch:          0
Version:        0.06
Requires:       %perl_compat
Requires:       perl(Compress::Zlib)
Requires:       perl(Encode)
%if %{defined perl_bootstrap}
%gendep_perl_DBM_Filter
%endif
BuildArch:      noarch


# Remove private redefinitions
# DBM_Filter redefines Tie::Hash, but does not load it.
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(Tie::Hash\\)$

%description DBM_Filter
This module provides an interface that allows filters to be applied to tied
hashes associated with DBM files.

%package debugger
Summary:        Perl debugger
License:        GPL+ or Artistic
Epoch:          0
Version:        1.60
BuildArch:      noarch
# File provides
Provides:       perl(dumpvar.pl) = %{perl_version}
Provides:       perl(perl5db.pl) = %{version}
Requires:       %perl_compat
Recommends:     perl(Carp)
Recommends:     perl(Config)
Requires:       perl(Cwd)
Recommends:     perl(Devel::Peek)
Requires:       perl(feature)
Recommends:     perl(IO::Handle)
Recommends:     perl(File::Basename)
Recommends:     perl(File::Path)
Requires:       perl(IO::Socket)
Requires:       perl(meta_notation) = %{perl_version}
Requires:       perl(mro)
%if !%{defined perl_bootstrap}
Suggests:       perl(PadWalker) >= 0.08
%endif
Recommends:     perl(POSIX)
Requires:       perl(Term::ReadLine)
# ??? Term::Rendezvous
Requires:       perl(threads)
Requires:       perl(threads::shared)
Requires:       perl(vars)
Requires:       perl(warnings)
%if %{defined perl_bootstrap}
%gendep_perl_debugger
%endif

%description debugger
This is the perl debugger. It is loaded automatically by Perl when you invoke
a script with "perl -d". There is also "DB" module contained for
a programmatic interface to the debugging API.

%package deprecate
Summary:        Perl pragma for deprecating the inclusion of a module in core
License:        GPL+ or Artistic
Epoch:          0
Version:        0.04
Requires:       %perl_compat
Requires:       perl(Carp)
Requires:       perl(Config)
%if %{defined perl_bootstrap}
%gendep_perl_deprecate
%endif
BuildArch:      noarch


%description deprecate
"deprecate" pragma simplifies the maintenance of dual-life modules that will no
longer be included in the Perl core in a future Perl release, but are
still included currently. The purpose of the pragma is to alert users to the
status of such a module by issuing a warning that encourages them to install
the module from CPAN, so that a future upgrade to a perl which omits the
module will not break their code.

%package Devel-Peek
Summary:        A data debugging tool for the XS programmer
License:        GPL+ or Artistic
Epoch:          0
Version:        1.30
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Devel_Peek
%endif

%description Devel-Peek
Devel::Peek contains functions which allows raw Perl data types to be
manipulated from a Perl script. This is used by those who do XS programming to
check that the data they are sending from C to Perl looks as they think it
should look.

%if %{dual_life} || %{rebuild_from_scratch}
%package Devel-PPPort
Summary:        Perl Pollution Portability header generator
License:        GPL+ or Artistic
Epoch:          0
Version:        3.62
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Devel_PPPort
%endif

%description Devel-PPPort
Perl's API has changed over time, gaining new features, new functions,
increasing its flexibility, and reducing the impact on the C name space
environment (reduced pollution). The header file written by this module,
typically ppport.h, attempts to bring some of the newer Perl API features
to older versions of Perl, so that you can worry less about keeping track
of old releases, but users can still reap the benefit.
%endif

%package Devel-SelfStubber
Summary:        Generate stubs for a SelfLoading module
License:        GPL+ or Artistic
Epoch:          0
Version:        1.06
BuildArch:      noarch
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Devel_SelfStubber
%endif

%description Devel-SelfStubber
Devel::SelfStubber prints the stubs you need to put in the module before the
__DATA__ token (or you can get it to print the entire module with stubs
correctly placed). The stubs ensure that if a method is called, it will get
loaded. They are needed specifically for inherited autoloaded methods.

%package diagnostics
Summary:        Produce verbose warning diagnostics
License:        GPL+ or Artistic
Epoch:          0
Version:        1.37
BuildArch:      noarch
Requires:       %perl_compat
# Match library exactly for diagnostics messages
Requires:       perl-libs = %{perl_epoch}:%{perl_version}-%{release}
Requires:       perl(Getopt::Std)
%if %{defined perl_bootstrap}
%gendep_perl_diagnostics
%endif


%description diagnostics
The diagnostics module extends the terse diagnostics normally emitted by both
the perl compiler and the perl interpreter (from running perl with a -w switch
or "use warnings"), augmenting them with the more explicative and endearing
descriptions found in perldiag. splain tool explains perl messages found on
standard input.

%if %{dual_life} || %{rebuild_from_scratch}
%package Digest
Summary:        Modules that calculate message digests
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          0
Version:        1.19
BuildArch:      noarch
Requires:       %perl_compat
Requires:       perl(MIME::Base64)
%if %{defined perl_bootstrap}
%gendep_perl_Digest
%endif

%description Digest
The Digest:: modules calculate digests, also called "fingerprints" or
"hashes", of some data, called a message. The digest is (usually)
some small/fixed size string. The actual size of the digest depend of
the algorithm used. The message is simply a sequence of arbitrary
bytes or bits.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Digest-MD5
Summary:        Perl interface to the MD5 Algorithm
License:        (GPL+ or Artistic) and BSD
# Epoch bump for clean upgrade over old standalone package
Epoch:          0
# Real version 2.58
Version:        2.58
Requires:       %perl_compat
Requires:       perl(XSLoader)
# Recommended
Requires:       perl(Digest::base) >= 1.00
%if %{defined perl_bootstrap}
%gendep_perl_Digest_MD5
%endif

%description Digest-MD5
The Digest::MD5 module allows you to use the RSA Data Security Inc. MD5
Message Digest algorithm from within Perl programs. The algorithm takes as
input a message of arbitrary length and produces as output a 128-bit
"fingerprint" or "message digest" of the input.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Digest-SHA
Summary:        Perl extension for SHA-1/224/256/384/512
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        6.02
Requires:       %perl_compat
Requires:       perl(Carp)
# Recommended
Requires:       perl(Digest::base)
%if %{defined perl_bootstrap}
%gendep_perl_Digest_SHA
%endif

%description Digest-SHA
Digest::SHA is a complete implementation of the NIST Secure Hash
Standard.  It gives Perl programmers a convenient way to calculate
SHA-1, SHA-224, SHA-256, SHA-384, and SHA-512 message digests.  The
module can handle all types of input, including partial-byte data.
%endif

%package DirHandle
Summary:        Supply object methods for directory handles
License:        GPL+ or Artistic
Epoch:          0
Version:        1.05
BuildArch:      noarch
Requires:       %perl_compat
Requires:       perl(warnings)
%if %{defined perl_bootstrap}
%gendep_perl_DirHandle
%endif

%description DirHandle
There is no reason to use this module nowadays. The DirHandle module provides
an alternative interface to the opendir(), closedir(), readdir(), and
rewinddir() functions. Since Perl 5.6, opendir() alone has been all you need
for lexical handles.

%package doc
Summary:        Perl language documentation
License:        (GPL+ or Artistic) and UCD and Public Domain
Epoch:          0
Version:        %{perl_version}
BuildArch:      noarch
Requires:       %perl_compat
# For perldoc tool
Recommends:     perl-Pod-Perldoc

%description doc
This is a documentation for Perl language. It's provided in POD and manual
page format.

%package Dumpvalue
Summary:        Screen dump of Perl data
License:        GPL+ or Artistic
Epoch:          0
# Real version 1.21
Version:        2.27
BuildArch:      noarch
Requires:       %perl_compat
Recommends:     perl(Devel::Peek)
%if %{defined perl_bootstrap}
%gendep_perl_Dumpvalue
%endif

%description Dumpvalue
Dumpvalue module enables you to print a content of variables and other Perl
data structures.

%package DynaLoader
Summary:        Dynamically load C libraries into Perl code
License:        GPL+ or Artistic
Epoch:          0
Version:        1.50
Requires:       %perl_compat
Requires:       perl(Carp)
%if %{defined perl_bootstrap}
%gendep_perl_DynaLoader
%endif

%description DynaLoader
The DynaLoader module defines a standard generic interface to the dynamic
linking mechanisms available on many platforms. Its primary purpose is to
implement automatic dynamic loading of Perl modules. For a simpler interface,
see XSLoader module.

%if %{dual_life} || %{rebuild_from_scratch}
%package Encode
Summary:        Character encodings in Perl
License:        (GPL+ or Artistic) and Artistic 2.0 and UCD
Epoch:          4
Version:        3.08
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Encode
%endif

%description Encode
The Encode module provides the interface between Perl strings and the rest
of the system. Perl strings are sequences of characters.

%package encoding
Summary:        Write your Perl script in non-ASCII or non-UTF-8
License:        GPL+ or Artistic
Epoch:          4
Version:        3.00
# Keeping this sub-package arch-specific because it installs files into
# arch-specific directories.
Requires:       %perl_compat
Requires:       perl(Carp)
# Config not needed on perl ≥ 5.008
# Consider Filter::Util::Call as mandatory, bug #1165183, CPAN RT#100427
Requires:       perl(Filter::Util::Call)
# I18N::Langinfo is optional
# PerlIO::encoding is optional
Requires:       perl(utf8)
%if %{defined perl_bootstrap}
%gendep_perl_encoding
%endif

%description encoding
With the encoding pragma, you can write your Perl script in any encoding you
like (so long as the Encode module supports it) and still enjoy Unicode
support.

However, this encoding module is deprecated under perl 5.18. It uses
a mechanism provided by perl that is deprecated under 5.18 and higher, and may
be removed in a future version.

The easiest and the best alternative is to write your script in UTF-8.

%package Encode-devel
Summary:        Character encodings in Perl
License:        (GPL+ or Artistic) and UCD
Epoch:          4
Version:        3.08
Requires:       %perl_compat
Requires:       %{name}-Encode = %{epoch}:%{version}-%{release}
Recommends:     perl-devel
%if %{defined perl_bootstrap}
%gendep_perl_Encode_devel
%endif
BuildArch:      noarch

%description Encode-devel
enc2xs builds a Perl extension for use by Encode from either Unicode Character
Mapping files (.ucm) or Tcl Encoding Files (.enc). You can use enc2xs to add
your own encoding to perl. No knowledge of XS is necessary.
%endif

%package encoding-warnings
Summary:        Warn on implicit encoding conversions
License:        GPL+ or Artistic
Epoch:          0
Version:        0.13
BuildArch:      noarch
Requires:       %perl_compat
Requires:       perl(Carp)
%if %{defined perl_bootstrap}
%gendep_perl_encoding_warnings
%endif

%description encoding-warnings
As of Perl 5.26.0, this module has no effect. The internal Perl feature that
was used to implement this module has been removed.  Hence, if you load this
module on Perl 5.26.0, you will get one warning that the module is no longer
supported; and the module will do nothing thereafter.

%package English
Summary:        Nice English or awk names for ugly punctuation variables
License:        GPL+ or Artistic
Epoch:          0
Version:        1.11
Requires:       %perl_compat
Requires:       perl(Carp)
Requires:       perl(warnings)
%if %{defined perl_bootstrap}
%gendep_perl_English
%endif
BuildArch:      noarch


%description English
This module provides aliases for the built-in variables whose names no one
seems to like to read.

%if %{dual_life} || %{rebuild_from_scratch}
%package Env
Summary:        Perl module that imports environment variables as scalars or arrays
License:        GPL+ or Artistic
Epoch:          0
Version:        1.05
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Env
%endif
BuildArch:      noarch

%description Env
Perl maintains environment variables in a special hash named %%ENV. For when
this access method is inconvenient, the Perl module Env allows environment
variables to be treated as scalar or array variables.
%endif

%package Errno
Summary:        System errno constants
License:        GPL+ or Artistic
Epoch:          0
Version:        1.33
Requires:       %perl_compat
# Errno.pm bakes in kernel version at build time and compares it against
# $Config{osvers} at run time. Match exact interpreter build. Bug #1393421.
Requires:       perl-libs%{?_isa} = %{perl_epoch}:%{perl_version}-%{release}
Requires:       perl(Carp)
%if %{defined perl_bootstrap}
%gendep_perl_Errno
%endif

%description Errno
"Errno" defines and conditionally exports all the error constants defined in
your system "errno.h" include file. It has a single export tag, ":POSIX",
which will export all POSIX defined error numbers.

%if %{dual_life} || %{rebuild_from_scratch}
%package experimental
Summary:        Experimental features made easy
License:        GPL+ or Artistic
Epoch:          0
Version:        0.024
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_experimental
%endif
BuildArch:      noarch

%description experimental
This pragma provides an easy and convenient way to enable or disable
experimental features.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Exporter
Summary:        Implements default import method for modules
License:        GPL+ or Artistic
Epoch:          0
Version:        5.76
Requires:       %perl_compat
Requires:       perl(Carp) >= 1.05
%if %{defined perl_bootstrap}
%gendep_perl_Exporter
%endif
BuildArch:      noarch

%description Exporter
The Exporter module implements an import method which allows a module to
export functions and variables to its users' name spaces. Many modules use
Exporter rather than implementing their own import method because Exporter
provides a highly flexible interface, with an implementation optimized for
the common case.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package ExtUtils-CBuilder
Summary:        Compile and link C code for Perl modules
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        0.280236
BuildArch:      noarch
# C and C++ compilers are highly recommended because compiling code is the
# purpose of ExtUtils::CBuilder, bug #1547165
Requires:       gcc
Requires:       gcc-c++
Requires:       perl-devel
Requires:       %perl_compat
Requires:       perl(DynaLoader)
Requires:       perl(ExtUtils::Mksymlists)
Requires:       perl(File::Spec) >= 3.13
Requires:       perl(Perl::OSType) >= 1
%if %{defined perl_bootstrap}
%gendep_perl_ExtUtils_CBuilder
%endif

%description ExtUtils-CBuilder
This module can build the C portions of Perl modules by invoking the
appropriate compilers and linkers in a cross-platform manner. It was motivated
by the Module::Build project, but may be useful for other purposes as well.
%endif

%package ExtUtils-Constant
Summary:        Generate XS code to import C header constants
License:        GPL+ or Artistic
Epoch:          0
Version:        0.25
BuildArch:      noarch
Requires:       %perl_compat
Requires:       perl(Data::Dumper)
# ExtUtils::Constant::Aaargh56Hash not used on recent Perls
# FileHandle not used on recent Perls
# POSIX not used on recent Perls

%if %{defined perl_bootstrap}
%gendep_perl_ExtUtils_Constant
%endif

%description ExtUtils-Constant
ExtUtils::Constant facilitates generating C and XS wrapper code to allow
Perl modules to AUTOLOAD constants defined in C library header files.

%if %{dual_life} || %{rebuild_from_scratch}
%package ExtUtils-Command
Summary:        Perl routines to replace common UNIX commands in Makefiles
License:        GPL+ or Artistic
Epoch:          2
Version:        7.62
BuildArch:      noarch
Requires:       %perl_compat
Requires:       perl(File::Find)
%if %{defined perl_bootstrap}
%gendep_perl_ExtUtils_Command
%endif

%description ExtUtils-Command
This Perl module is used to replace common UNIX commands. In all cases the
functions work with @ARGV rather than taking arguments. This makes them
easier to deal with in Makefiles.
%endif

%package ExtUtils-Embed
Summary:        Utilities for embedding Perl in C/C++ applications
License:        GPL+ or Artistic
Epoch:          0
Version:        1.35
Requires:       perl-devel
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_ExtUtils_Embed
%endif
BuildArch:      noarch

%description ExtUtils-Embed
Utilities for embedding Perl in C/C++ applications.


%if %{dual_life} || %{rebuild_from_scratch}
%package ExtUtils-Install
Summary:        Install files from here to there
License:        GPL+ or Artistic
Epoch:          0
Version:        2.20
BuildArch:      noarch
Requires:       %perl_compat
Requires:       perl(AutoSplit)
Requires:       perl(File::Compare)
Requires:       perl(Data::Dumper)
Recommends:     perl(POSIX)
%if %{defined perl_bootstrap}
%gendep_perl_ExtUtils_Install
%endif

%description ExtUtils-Install
Handles the installing and uninstalling of perl modules, scripts, man
pages, etc.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package ExtUtils-MakeMaker
Summary:        Create a module Makefile
License:        GPL+ or Artistic
Epoch:          2
Version:        7.62
# These dependencies are weak in order to relieve building noarch
# packages from perl-devel and gcc. See bug #1547165.
# If an XS module is built, the generated Makefile executes gcc.
Recommends:     gcc
# If an XS module is built, code generated from XS will be compiled and it
# includes Perl header files.
Recommends:     perl-devel
Requires:       %perl_compat
Requires:       perl(Data::Dumper)
Requires:       perl(DynaLoader)
Requires:       perl(ExtUtils::Command)
Requires:       perl(ExtUtils::Install)
Requires:       perl(ExtUtils::Manifest)
Requires:       perl(File::Find)
Requires:       perl(Getopt::Long)
# Optional Pod::Man is needed for generating manual pages from POD
Requires:       perl(Pod::Man)
Requires:       perl(POSIX)
Requires:       perl(Test::Harness)
Requires:       perl(version)
# If an XS module is compiled, xsubpp(1) is needed
Requires:       perl-ExtUtils-ParseXS
%if %{defined perl_bootstrap}
%gendep_perl_ExtUtils_MakeMaker
%endif
BuildArch:      noarch

# Filter false DynaLoader provides. Versioned perl(DynaLoader) keeps
# unfiltered on perl package, no need to reinject it.
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(DynaLoader\\)\\s*$
%global __provides_exclude %__provides_exclude|^perl\\(ExtUtils::MakeMaker::_version\\)

%description ExtUtils-MakeMaker
Create a module Makefile.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package ExtUtils-Manifest
Summary:        Utilities to write and check a MANIFEST file
License:        GPL+ or Artistic
Epoch:          1
Version:        1.73
Requires:       %perl_compat
Requires:       perl(File::Path)
%if %{defined perl_bootstrap}
%gendep_perl_ExtUtils_Manifest
%endif
BuildArch:      noarch

%description ExtUtils-Manifest
%{summary}.
%endif

%package ExtUtils-Miniperl
Summary:        Write the C code for perlmain.c
License:        GPL+ or Artistic
Epoch:          0
Version:        1.10
Requires:       perl-devel
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_ExtUtils_Miniperl
%endif
BuildArch:      noarch

%description ExtUtils-Miniperl
writemain() takes an argument list of directories containing archive libraries
that relate to perl modules and should be linked into a new perl binary. It
writes a corresponding perlmain.c file that is a plain C file containing all
the bootstrap code to make the If the first argument to writemain() is a
reference to a scalar it is used as the file name to open for output. Any other
reference is used as the file handle to write to. Otherwise output defaults to
STDOUT.

%if %{dual_life} || %{rebuild_from_scratch}
%package ExtUtils-MM-Utils
Summary:        ExtUtils::MM methods without dependency on ExtUtils::MakeMaker
License:        GPL+ or Artistic
Epoch:          1
# Real version 7.11
# Dual-life ExtUtils-MakeMaker generate it with its version
Version:        7.44
BuildArch:      noarch
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_ExtUtils_MM_Utils
%endif

%description ExtUtils-MM-Utils
This is a collection of ExtUtils::MM subroutines that are used by many
other modules but that do not need full-featured ExtUtils::MakeMaker. The
issue with ExtUtils::MakeMaker is it pulls in Perl header files and that
is an overkill for small subroutines.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package ExtUtils-ParseXS
Summary:        Module and a script for converting Perl XS code into C code
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        3.43
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_ExtUtils_ParseXS
%endif

BuildArch:      noarch

%description ExtUtils-ParseXS
ExtUtils::ParseXS will compile XS code into C code by embedding the constructs
necessary to let C functions manipulate Perl values and creates the glue
necessary to let Perl access those functions.
%endif

%package Fcntl
Summary:        File operation options
License:        GPL+ or Artistic
Epoch:          0
Version:        1.14
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Fcntl
%endif


%description Fcntl
Fcntl module provides file operation related options.

%package fields
Summary:        Compile-time class fields
License:        GPL+ or Artistic
Epoch:          0
# Real version 2.24
Version:        2.27
BuildArch:      noarch
Requires:       %perl_compat
Requires:       perl(base)
Requires:       perl(Carp)
Requires:       perl(Hash::Util)
%if %{defined perl_bootstrap}
%gendep_perl_fields
%endif

%description fields
The "fields" pragma enables compile-time and run-time verified class fields.

%package File-Basename
Summary:        Parse file paths into directory, file name, and suffix
License:        GPL+ or Artistic
Epoch:          0
Version:        2.85
BuildArch:      noarch
Requires:       %perl_compat
Requires:       perl(Carp)
Requires:       perl(re)
%if %{defined perl_bootstrap}
%gendep_perl_File_Basename
%endif

%description File-Basename
These routines allow you to parse file paths into their directory, file name,
and suffix.

%package File-Compare
Summary:        Compare files or file handles
License:        GPL+ or Artistic
Epoch:          0
# Normalized version
Version:        1.100.600
BuildArch:      noarch
Requires:       %perl_compat
Requires:       perl(Carp)
%if %{defined perl_bootstrap}
%gendep_perl_File_Compare
%endif

%description File-Compare
A File::Compare Perl module provides functions for comparing a content of two
files specified by a file name or a file handle.

%package File-Copy
Summary:        Copy files or file handles
License:        GPL+ or Artistic
Epoch:          0
Version:        2.35
BuildArch:      noarch
Requires:       %perl_compat
Requires:       perl(Carp)
Requires:       perl(File::Basename)
%if %{defined perl_bootstrap}
%gendep_perl_File_Copy
%endif

%description File-Copy
A File::Copy module provides two basic functions, copy and move, which are
useful for getting the contents of a file from one place to another.

%package File-DosGlob
Summary:        DOS-like globbing
License:        GPL+ or Artistic
Epoch:          0
Version:        1.12
Requires:       %perl_compat
Requires:       perl(Text::ParseWords)
%if %{defined perl_bootstrap}
%gendep_perl_File_DosGlob
%endif


%description File-DosGlob
This Perl module implements DOS-like globbing with a few enhancements. It
is largely compatible with perlglob.exe in all but one respect--it understands
wild cards in directory components.

%if %{dual_life} || %{rebuild_from_scratch}
%package File-Fetch
Summary:        Generic file fetching mechanism
License:        GPL+ or Artistic
Epoch:          0
Version:        1.00
Requires:       perl(IPC::Cmd) >= 0.36
Requires:       perl(Module::Load::Conditional) >= 0.04
Requires:       perl(Params::Check) >= 0.07
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_File_Fetch
%endif
BuildArch:      noarch

%description File-Fetch
File::Fetch is a generic file fetching mechanism.
%endif

%package File-Find
Summary:        Traverse a directory tree
License:        GPL+ or Artistic
Epoch:          0
Version:        1.39
Requires:       %perl_compat
Recommends:     perl(Scalar::Util)
%if %{defined perl_bootstrap}
%gendep_perl_File_Find
%endif
BuildArch:      noarch


%description File-Find
These are functions for searching through directory trees doing work on each
file found similar to the Unix find command.

%if %{dual_life} || %{rebuild_from_scratch}
%package File-Path
Summary:        Create or remove directory trees
License:        GPL+ or Artistic
Epoch:          0
Version:        2.18
Requires:       %perl_compat
Requires:       perl(Carp)
%if %{defined perl_bootstrap}
%gendep_perl_File_Path
%endif
BuildArch:      noarch

%description File-Path
This module provides a convenient way to create directories of arbitrary
depth and to delete an entire directory subtree from the file system.
%endif

%package File-stat
Summary:        By-name interface to Perl built-in stat functions
License:        GPL+ or Artistic
Epoch:          0
Version:        1.09
BuildArch:      noarch
Requires:       %perl_compat
Requires:       perl(Symbol)
%if %{defined perl_bootstrap}
%gendep_perl_File_stat
%endif

%description File-stat
This module overrides the core stat() and lstat() functions, replacing them
with versions that return File::stat objects. This object has methods that
return the similarly named structure field name from the stat(2) function.

%if %{dual_life} || %{rebuild_from_scratch}
%package File-Temp
Summary:        Return name and handle of a temporary file safely
License:        GPL+ or Artistic
Epoch:          1
# Normalized version
Version:        0.231.100
Requires:       %perl_compat
BuildArch:      noarch
Requires:       perl(File::Path) >= 2.06
Requires:       perl(POSIX)
%if %{defined perl_bootstrap}
%gendep_perl_File_Temp
%endif

%description File-Temp
File::Temp can be used to create and open temporary files in a safe way.
There is both a function interface and an object-oriented interface. The
File::Temp constructor or the tempfile() function can be used to return the
name and the open file handle of a temporary file. The tempdir() function
can be used to create a temporary directory.
%endif

%package FileCache
Summary:        Keep more files open than the system permits
License:        GPL+ or Artistic
Epoch:          0
Version:        1.10
BuildArch:      noarch
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_FileCache
%endif


%description FileCache
The "cacheout" function will make sure that there's a file handle open
for reading or writing available as the path name you give it. It
automatically closes and re-opens files if you exceed your system
maximum number of file descriptors, or the suggested maximum.

%package FileHandle
Summary:        Object methods for file handles
License:        GPL+ or Artistic
Epoch:          0
Version:        2.03
BuildArch:      noarch
Requires:       %perl_compat
Requires:       perl(Exporter)
Recommends:     perl(Fcntl)
%if %{defined perl_bootstrap}
%gendep_perl_FileHandle
%endif


%description FileHandle
This is an object-oriented interface for opening files and performing
input/output operations on them.

%package filetest
Summary:        Perl pragma to control the filetest permission operators
License:        GPL+ or Artistic
Epoch:          0
Version:        1.03
BuildArch:      noarch
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_filetest
%endif

%description filetest
The default behavior of file test operators (e.g. "-r") is to use the simple
mode bits as returned by the stat() family of system calls. However, many
operating systems have additional features to define more complex access
rights, for example ACLs (Access Control Lists). For such environments, "use
filetest" may help the permission operators to return results more consistent
with other tools.

%if %{dual_life} || %{rebuild_from_scratch}
# FIXME Filter-Simple? version?
%package Filter
Summary:        Perl source filters
License:        GPL+ or Artistic
Epoch:          2
Version:        1.59
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Filter
%endif

%description Filter
Source filters alter the program text of a module before Perl sees it, much as
a C preprocessor alters the source text of a C program before the compiler
sees it.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Filter-Simple
Summary:        Simplified Perl source filtering
License:        GPL+ or Artistic
Epoch:          0
Version:        0.96
BuildArch:      noarch
Requires:       %perl_compat
Requires:       perl(Text::Balanced) >= 1.97
Requires:       perl(warnings)
%if %{defined perl_bootstrap}
%gendep_perl_Filter_Simple
%endif

%description Filter-Simple
The Filter::Simple Perl module provides a simplified interface to
Filter::Util::Call; one that is sufficient for most common cases.
%endif

%package FindBin
Summary:        Locate a directory of an original Perl script
License:        GPL+ or Artistic
Epoch:          0
Version:        1.52
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_FindBin
%endif
BuildArch:      noarch


%description FindBin
Locates the full path to the script bin directory to allow the use of paths
relative to the bin directory.

%if %{with gdbm}
%package GDBM_File
Summary:        Perl5 access to the gdbm library
License:        GPL+ or Artistic
Epoch:          1
Version:        1.19
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_GDBM_File
%endif


%description GDBM_File
GDBM_File is a module which allows Perl programs to make use of the facilities
provided by the GNU gdbm library.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Getopt-Long
Summary:        Extended processing of command line options
License:        GPLv2+ or Artistic
Epoch:          1
Version:        2.52
Requires:       %perl_compat
Requires:       perl(overload)
Requires:       perl(Text::ParseWords)
# Recommended:
Requires:       perl(Pod::Usage) >= 1.14
%if %{defined perl_bootstrap}
%gendep_perl_Getopt_Long
%endif
BuildArch:      noarch

%description Getopt-Long
The Getopt::Long module implements an extended getopt function called
GetOptions(). It parses the command line from @ARGV, recognizing and removing
specified options and their possible values.  It adheres to the POSIX syntax
for command line options, with GNU extensions. In general, this means that
options have long names instead of single letters, and are introduced with
a double dash "--". Support for bundling of command line options, as was the
case with the more traditional single-letter approach, is provided but not
enabled by default.
%endif

%package Getopt-Std
Summary:        Process single-character switches with switch clustering
License:        GPL+ or Artistic
Epoch:          0
Version:        1.13
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Getopt_Std
%endif
BuildArch:      noarch


%description Getopt-Std
The Getopt::Std module provides functions for processing single-character
switches with switch clustering. Pass one argument which is a string
containing all switches to be recognized.

%package Hash-Util
Summary:        General-utility hash subroutines
License:        GPL+ or Artistic
Epoch:          0
Version:        0.25
Requires:       %perl_compat
Requires:       perl(Hash::Util::FieldHash)
Requires:       perl(XSLoader)
%if %{defined perl_bootstrap}
%gendep_perl_Hash_Util
%endif


%description Hash-Util
Hash::Util contains special functions for manipulating hashes that don't
really warrant a keyword.

%package Hash-Util-FieldHash
Summary:        Support for inside-out classes
License:        GPL+ or Artistic
Epoch:          0
Version:        1.21
Requires:       %perl_compat
Requires:       perl(XSLoader)
%if %{defined perl_bootstrap}
%gendep_perl_Hash_Util_FieldHash
%endif


%description Hash-Util-FieldHash
Hash::Util::FieldHash offers a number of functions in support of the
inside-out technique of class construction.

%package if
Summary:        Use a Perl module if a condition holds
License:        GPL+ or Artistic
Epoch:          0
# Normalized 0.0609
Version:        0.60.900
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_if
%endif
BuildArch:      noarch


%description if
The "if" module is used to conditionally load another module.

%package IO
Summary:        Perl input/output modules
License:        GPL+ or Artistic
Epoch:          0
Version:        1.46
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_IO
%endif

%description IO
This is a collection of Perl input/output modules.

%if %{dual_life} || %{rebuild_from_scratch}
%package IO-Compress
Summary:        IO::Compress wrapper for modules
License:        GPL+ or Artistic
Epoch:          0
Version:        2.102
Requires:       %perl_compat
Provides:       perl(IO::Uncompress::Bunzip2)
%if %{defined perl_bootstrap}
%gendep_perl_IO_Compress
%endif
BuildArch:      noarch

%description IO-Compress
This module is the base class for all IO::Compress and IO::Uncompress modules.
This module is not intended for direct use in application code. Its sole
purpose is to to be sub-classed by IO::Compress modules.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package IO-Socket-IP
Summary:        Drop-in replacement for IO::Socket::INET supporting both IPv4 and IPv6
License:        GPL+ or Artistic
Epoch:          0
Version:        0.41
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_IO_Socket_IP
%endif
BuildArch:      noarch

%description IO-Socket-IP
This module provides a protocol-independent way to use IPv4 and IPv6
sockets, as a drop-in replacement for IO::Socket::INET. Most constructor
arguments and methods are provided in a backward-compatible way.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package IO-Zlib
Summary:        Perl IO:: style interface to Compress::Zlib
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        1.11
BuildRequires:  gzip
# The code defaults to Compress::Zlib, but a user can override it to gzip by
# importing :gzip_external symbol
Requires:       gzip
Requires:       perl(Compress::Zlib) >= 2
# IO::Handle used if gzip backend is requested
Requires:       perl(IO::Handle)
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_IO_Zlib
%endif
BuildArch:      noarch

%description IO-Zlib
IO::Zlib provides an IO:: style interface to Compress::Zlib and hence to
gzip/zlib-compressed files. It provides many of the same methods as the
IO::Handle interface.
%endif


%if %{dual_life} || %{rebuild_from_scratch}
%package IPC-Cmd
Summary:        Finding and running system commands made easy
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          2
Version:        1.04
Requires:       perl(ExtUtils::MM::Utils)
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_IPC_Cmd
%endif
BuildArch:      noarch

%description IPC-Cmd
IPC::Cmd allows you to run commands, interactively if desired, in a platform
independent way, but have them still work.
%endif

%package IPC-Open3
Summary:        Open a process for reading, writing, and error handling
License:        GPL+ or Artistic
Epoch:          0
Version:        1.21
Requires:       %perl_compat
Requires:       perl(Fcntl)
Requires:       perl(IO::Pipe)
Requires:       perl(POSIX)
Requires:       perl(warnings)
%if %{defined perl_bootstrap}
%gendep_perl_IPC_Open3
%endif
BuildArch:      noarch


%description IPC-Open3
These are functions that spawn a given command and connects the standard
output of the command for reading, standard output for writing, and standard
error output for handling the errors.

%if %{dual_life} || %{rebuild_from_scratch}
%package IPC-SysV
Summary:        Object interface to System V IPC
License:        GPL+ or Artistic
Epoch:          0
Version:        2.09
Requires:       %perl_compat
Requires:       perl(DynaLoader)
%if %{defined perl_bootstrap}
%gendep_perl_IPC_SysV
%endif

%description IPC-SysV
This is an object interface for System V messages, semaphores, and
inter-process calls.
%endif

%package I18N-Collate
Summary:        Compare 8-bit scalar data according to the current locale
License:        GPL+ or Artistic
Epoch:          0
Version:        1.02
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_I18N_Collate
%endif
BuildArch:      noarch


%description I18N-Collate
This module provides you with objects that will collate according to your
national character set. This module is deprecated. See the perllocale manual
page for further information.

%package I18N-Langinfo
Summary:        Query locale information
License:        GPL+ or Artistic
Epoch:          0
Version:        0.19
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_I18N_Langinfo
%endif


%description I18N-Langinfo
The langinfo() function queries various locale information that can be used to
localize output and user interfaces. It uses the current underlying locale,
regardless of whether or not it was called from within the scope of "use
locale".

%package I18N-LangTags
Summary:        Functions for dealing with RFC 3066 language tags
License:        GPL+ or Artistic
Epoch:          0
Version:        0.45
Requires:       %perl_compat
Requires:       perl(integer)
Requires:       perl(warnings)
%if %{defined perl_bootstrap}
%gendep_perl_I18N_LangTags
%endif
BuildArch:      noarch


%description I18N-LangTags
Language tags are a formalism, described in RFC 3066, for declaring what
language form (language and possibly dialect) a given chunk of information is
in. This library provides functions for common tasks involving language tags
as they are needed in a variety of protocols and applications.

%if %{dual_life} || %{rebuild_from_scratch}
%package HTTP-Tiny
Summary:        A small, simple, correct HTTP/1.1 client
License:        GPL+ or Artistic
Epoch:          0
Version:        0.076
Requires:       perl(bytes)
Requires:       perl(Carp)
Requires:       perl(IO::Socket)
Requires:       perl(Time::Local)
%if %{defined perl_bootstrap}
%gendep_perl_HTTP_Tiny
%endif
BuildArch:      noarch

%description HTTP-Tiny
This is a very simple HTTP/1.1 client, designed primarily for doing simple GET 
requests without the overhead of a large framework like LWP::UserAgent.
It is more correct and more complete than HTTP::Lite. It supports proxies 
(currently only non-authenticating ones) and redirection. It also correctly 
resumes after EINTR.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package JSON-PP
Summary:        JSON::XS compatible pure-Perl module
Epoch:          1
Version:        4.06
License:        GPL+ or Artistic
BuildArch:      noarch
Requires:       %perl_compat 
Requires:       perl(Data::Dumper)
Requires:       perl(Encode)
Requires:       perl(Math::BigFloat)
Requires:       perl(Math::BigInt)
Requires:       perl(Scalar::Util)
Requires:       perl(subs)
%if %{defined perl_bootstrap}
%gendep_perl_JSON_PP
%endif

%description JSON-PP
JSON::XS is the fastest and most proper JSON module on CPAN. It is written by
Marc Lehmann in C, so must be compiled and installed in the used environment.
JSON::PP is a pure-Perl module and is compatible with JSON::XS.
%endif

%package less
Summary:        Perl pragma to request less of something
License:        GPL+ or Artistic
Epoch:          0
Version:        0.03
BuildArch:      noarch
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_less
%endif

%description less
"use less ...;" is a Perl user-pragma. If you're very lucky some code you're
using will know that you asked for less CPU usage or RAM or fat or... we just
can't know.

%package lib
Summary:        Manipulate @INC at compile time
License:        GPL+ or Artistic
Epoch:          0
Version:        0.65
Requires:       %perl_compat
Requires:       perl(Carp)
%if %{defined perl_bootstrap}
%gendep_perl_lib
%endif


%description lib
This module simplifies the manipulation of @INC at compile time.

%if %{dual_life} || %{rebuild_from_scratch}
%package libnet
Summary:        Perl clients for various network protocols
License:        (GPL+ or Artistic) and Artistic
Epoch:          0
Version:        3.13
Requires:       %perl_compat
Requires:       perl(File::Basename)
Requires:       perl(IO::Socket) >= 1.05
# Prefer IO::Socket::IP over IO::Socket::INET6 and IO::Socket::INET
Requires:       perl(IO::Socket::IP) >= 0.20
Requires:       perl(POSIX)
Requires:       perl(Socket) >= 2.016
Requires:       perl(utf8)
%if %{defined perl_bootstrap}
%gendep_perl_libnet
%endif
BuildArch:      noarch

%description libnet
This is a collection of Perl modules which provides a simple and
consistent programming interface (API) to the client side of various
protocols used in the internet community.
%endif

%package libnetcfg
Summary:        Configure libnet
License:        GPL+ or Artistic
Epoch:          %perl_epoch
Version:        %perl_version
# Net::Config is optional
BuildArch:      noarch
%if %{defined perl_bootstrap}
%gendep_perl_libnetcfg
%endif

%description libnetcfg
The libnetcfg utility can be used to configure the libnet.

%package locale
Summary:        Pragma to use or avoid POSIX locales for built-in operations
License:        GPL+ or Artistic
Epoch:          0
Version:        1.10
Requires:       %perl_compat
Requires:       perl(Carp)
Requires:       perl(POSIX)
%if %{defined perl_bootstrap}
%gendep_perl_locale
%endif
BuildArch:      noarch


%description locale
This pragma tells the compiler to enable (or disable) the use of POSIX locales
for built-in operations (for example, LC_CTYPE for regular expressions,
LC_COLLATE for string comparison, and LC_NUMERIC for number formatting). Each
"use locale" or "no locale" affects statements to the end of the enclosing
block.

%if %{dual_life} || %{rebuild_from_scratch}
%package Locale-Maketext
Summary:        Framework for localization
License:        GPL+ or Artistic
Epoch:          0
Version:        1.29
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Locale_Maketext
%endif
BuildArch:      noarch

%description Locale-Maketext
It is a common feature of applications (whether run directly, or via the Web)
for them to be "localized" -- i.e., for them to present an English interface
to an English-speaker, a German interface to a German-speaker, and so on for
all languages it's programmed with. Locale::Maketext is a framework for
software localization; it provides you with the tools for organizing and
accessing the bits of text and text-processing code that you need for
producing localized applications.
%endif

%package Locale-Maketext-Simple
Summary:        Simple interface to Locale::Maketext::Lexicon
License:        MIT
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        0.21
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Locale_Maketext_Simple
%endif
BuildArch:      noarch

%description Locale-Maketext-Simple
This module is a simple wrapper around Locale::Maketext::Lexicon, designed
to alleviate the need of creating Language Classes for module authors.

%if %{dual_life} || %{rebuild_from_scratch}
%package Math-BigInt
Summary:        Arbitrary-size integer and float mathematics
License:        GPL+ or Artistic
Epoch:          1
# Real version 1.999818
Version:        1.9998.18
Requires:       %perl_compat
Requires:       perl(Carp)
# File::Spec not used on recent perl
%if %{defined perl_bootstrap}
%gendep_perl_Math_BigInt
%endif
BuildArch:      noarch

# Do not export unversioned module
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(Math::BigInt\\)\\s*$

%description Math-BigInt
This provides Perl modules for arbitrary-size integer and float mathematics.

%package Math-BigInt-FastCalc
Summary:        Math::BigInt::Calc XS implementation
License:        GPL+ or Artistic
Epoch:          0
# Version normalized to dot format
# Real version 0.5009
Version:        0.500.900
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Math_BigInt_FastCalc
%endif

%description Math-BigInt-FastCalc
This package provides support for faster big integer calculations.

%package Math-BigRat
Summary:        Arbitrary big rational numbers
License:        GPL+ or Artistic
Epoch:          0
# Real version 0.2614
Version:        0.2614
Requires:       %perl_compat
Requires:       perl(Math::BigInt)
%if %{defined perl_bootstrap}
%gendep_perl_Math_BigRat
%endif
BuildArch:      noarch

%description Math-BigRat
Math::BigRat complements Math::BigInt and Math::BigFloat by providing support
for arbitrary big rational numbers.
%endif

%package Math-Complex
Summary:        Complex numbers and trigonometric functions
License:        GPL+ or Artistic
Epoch:          0
Version:        1.59
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Math_Complex
%endif
BuildArch:      noarch

%description Math-Complex
This package lets you create and manipulate complex numbers. By default, Perl
limits itself to real numbers, but an extra "use" statement brings full
complex support, along with a full set of mathematical functions typically
associated with and/or extended to complex numbers.

%package Memoize
Summary:        Transparently speed up functions by caching return values
License:        GPL+ or Artistic
Epoch:          0
Version:        1.03
Requires:       %perl_compat
# Keep Time::HiRes optional
%if %{defined perl_bootstrap}
%gendep_perl_Memoize
%endif
BuildArch:      noarch

%description Memoize
Memoizing a function makes it faster by trading space for time. It does
this by caching the return values of the function in a table. If you call
the function again with the same arguments, memoize jumps in and gives
you the value out of the table, instead of letting the function compute
the value all over again.

%package meta-notation
Summary:        Change nonprintable characters below 0x100 into printables
License:        GPL+ or Artistic
Epoch:          0
Version:        %{perl_version}
BuildArch:      noarch
Provides:       perl(meta_notation) = %{perl_version}
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_meta_notation
%endif

%description meta-notation
Returns a copy of the input string with the nonprintable characters below
0x100 changed into printables. Any ASCII printables or above 0xFF are
unchanged.

%if %{dual_life} || %{rebuild_from_scratch}
%package MIME-Base64
Summary:        Encoding and decoding of Base64 and quoted-printable strings
# cpan/MIME-Base64/Base64.xs:   (GPL+ or Artistic) and MIT (Bellcore's part)
# Other files:                  GPL+ or Artistic
License:        (GPL+ or Artistic) and MIT
Epoch:          0
Version:        3.16
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_MIME_Base64
%endif

%description MIME-Base64
This package contains a Base64 encoder/decoder and a quoted-printable
encoder/decoder. These encoding methods are specified in RFC 2045 - MIME
(Multipurpose Internet Mail Extensions).
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Module-CoreList
Summary:        What modules are shipped with versions of perl
License:        GPL+ or Artistic
Epoch:          1
Version:        5.20220313
Requires:       %perl_compat
Requires:       perl(List::Util)
Requires:       perl(version) >= 0.88
%if %{defined perl_bootstrap}
%gendep_perl_Module_CoreList
%endif
BuildArch:      noarch

%description Module-CoreList
Module::CoreList provides information on which core and dual-life modules
are shipped with each version of perl.


%package Module-CoreList-tools
Summary:        Tool for listing modules shipped with perl
License:        GPL+ or Artistic
Epoch:          1
Version:        5.20220313
Requires:       %perl_compat
Requires:       perl(feature)
Requires:       perl(version) >= 0.88
Requires:       perl-Module-CoreList = %{epoch}:%{version}-%{release}
%if %{defined perl_bootstrap}
%gendep_perl_Module_CoreList_tools
%endif
# The files were distributed with perl.spec's subpackage
# perl-Module-CoreList <= 1:5.020001-309
BuildArch:      noarch

%description Module-CoreList-tools
This package provides a corelist(1) tool which can be used to query what
modules were shipped with given perl version.
%endif


%if %{dual_life} || %{rebuild_from_scratch}
%package Module-Load
Summary:        Runtime require of both modules and files
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        0.36
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Module_Load
%endif
BuildArch:      noarch

%description Module-Load
Module::Load eliminates the need to know whether you are trying to require
either a file or a module.
%endif


%if %{dual_life} || %{rebuild_from_scratch}
%package Module-Load-Conditional
Summary:        Looking up module information / loading at runtime
License:        GPL+ or Artistic
Epoch:          0
Version:        0.74
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Module_Load_Conditional
%endif
BuildArch:      noarch

%description Module-Load-Conditional
Module::Load::Conditional provides simple ways to query and possibly load any
of the modules you have installed on your system during runtime.
%endif


%package Module-Loaded
Summary:        Mark modules as loaded or unloaded
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        0.08
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Module_Loaded
%endif
BuildArch:      noarch

%description Module-Loaded
When testing applications, often you find yourself needing to provide
functionality in your test environment that would usually be provided by
external modules. Rather than munging the %%INC by hand to mark these external
modules as loaded, so they are not attempted to be loaded by perl, this module
offers you a very simple way to mark modules as loaded and/or unloaded.


%if %{dual_life} || %{rebuild_from_scratch}
%package Module-Metadata
Summary:        Gather package and POD information from perl module files
Epoch:          0
Version:        1.000037
License:        GPL+ or Artistic
BuildArch:      noarch
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Module_Metadata
%endif

%description Module-Metadata
Gather package and POD information from perl module files
%endif

%package mro
Summary:        Method resolution order
License:        GPL+ or Artistic
Epoch:          0
Version:        1.25
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_mro
%endif


%description mro
The "mro" name space provides several utilities for dealing with method
resolution order and method caching in general.

%if %{with gdbm}
%package NDBM_File
Summary:        Tied access to ndbm files
License:        GPL+ or Artistic
Epoch:          0
Version:        1.15
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_NDBM_File
%endif


%description NDBM_File
NDBM_File establishes a connection between a Perl hash variable and a file in
ndbm format. You can manipulate the data in the file just as if it were in
a Perl hash, but when your program exits, the data will remain in the file, to
be used the next time your program runs.
%endif

%package Net
Summary:        By-name interface to Perl built-in network resolver
License:        GPL+ or Artistic
Epoch:          0
Version:        1.02
BuildArch:      noarch
Requires:       %perl_compat
Requires:       perl(Socket)
%if %{defined perl_bootstrap}
%gendep_perl_Net
%endif


%description Net
This package provide object-oriented interface to Perl built-in gethost*(),
getnet*(), getproto*(), and getserv*() functions.

%if %{dual_life} || %{rebuild_from_scratch}
%package Net-Ping
Summary:        Check a remote host for reachability
License:        GPL+ or Artistic
Epoch:          0
Version:        2.74
Requires:       %perl_compat
Requires:       perl(IO::Socket::INET)
# Keep Net::Ping::External optional
Suggests:       perl(Net::Ping::External)
%if %{defined perl_bootstrap}
%gendep_perl_Net_Ping
%endif
BuildArch:      noarch

%description Net-Ping
Net::Ping module contains methods to test the reachability of remote hosts on
a network.
%endif

%package NEXT
Summary:        Pseudo-class that allows method redispatch
License:        GPL+ or Artistic
Epoch:          0
Version:        0.68
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_NEXT
%endif
BuildArch:      noarch


%description NEXT
The NEXT module adds a pseudo-class named "NEXT" to any program that uses it.
If a method "m" calls "$self->NEXT::m()", the call to "m" is redispatched as
if the calling method had not originally been found.

%if %{with gdbm}
%package ODBM_File
Summary:        Tied access to odbm files
License:        GPL+ or Artistic
Epoch:          0
Version:        1.17
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_ODBM_File
%endif


%description ODBM_File
ODBM_File establishes a connection between a Perl hash variable and a file in
odbm format. You can manipulate the data in the file just as if it were in
a Perl hash, but when your program exits, the data will remain in the file, to
be used the next time your program runs.
%endif

%package Opcode
Summary:        Disable named opcodes when compiling a perl code
License:        GPL+ or Artistic
Epoch:          0
Version:        1.50
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Opcode
%endif


%description Opcode
The Opcode module allows you to define an operator mask to be in effect when
perl next compiles any code. Attempting to compile code which contains
a masked opcode will cause the compilation to fail with an error. The code
will not be executed.

%package open
Summary:        Perl pragma to set default PerlIO layers for input and output
License:        GPL+ or Artistic
Epoch:          0
Version:        1.12
Requires:       %perl_compat
Requires:       perl(Carp)
Requires:       perl(Encode)
Requires:       perl(encoding)
%if %{defined perl_bootstrap}
%gendep_perl_open
%endif
BuildArch:      noarch

%description open
The "open" pragma serves as one of the interfaces to declare default "layers"
(also known as "disciplines") for all I/O.

%package overload
Summary:        Overloading Perl operations
License:        GPL+ or Artistic
Epoch:          0
Version:        1.33
BuildArch:      noarch
Requires:       %perl_compat
Requires:       perl(mro)
Requires:       perl(Scalar::Util)
Requires:       perl(overloading)
%if %{defined perl_bootstrap}
%gendep_perl_overload
%endif


%description overload
The "overload" pragma allows overloading of Perl operators for a class. To
overload built-in functions, see "Overriding Built-in Functions" in perlsub
POD instead.

%package overloading
Summary:        Perl pragma to lexically control overloading
License:        GPL+ or Artistic
Epoch:          0
Version:        0.02
BuildArch:      noarch
Requires:       %perl_compat
Requires:       perl(Carp)
%if %{defined perl_bootstrap}
%gendep_perl_overloading
%endif


%description overloading
Overloading pragma allows you to lexically disable or enable overloading.

%if %{dual_life} || %{rebuild_from_scratch}
%package parent
Summary:        Establish an ISA relationship with base classes at compile time
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        0.238
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_parent
%endif
BuildArch:      noarch

%description parent
parent allows you to both load one or more modules, while setting up
inheritance from those modules at the same time. Mostly similar in effect to:

    package Baz;

    BEGIN {
        require Foo;
        require Bar;

        push @ISA, qw(Foo Bar);
    }
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Params-Check
Summary:        Generic input parsing/checking mechanism
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        0.38
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Params_Check
%endif
BuildArch:      noarch

%description Params-Check
Params::Check is a generic input parsing/checking mechanism.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package PathTools
Summary:        PathTools Perl module (Cwd, File::Spec)
License:        (GPL+ or Artistic) and BSD
Epoch:          0
Version:        3.80
Requires:       %perl_compat
Requires:       perl(Carp)
Requires:       perl(Errno)
Requires:       perl(Scalar::Util)
# XSLoader is optional only because miniperl does not support XS. With perl we
# almost certainly want it.
Recommends:     perl(XSLoader)
%if %{defined perl_bootstrap}
%gendep_perl_PathTools
%endif

%description PathTools
PathTools Perl module (Cwd, File::Spec).
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package perlfaq
Summary:        Frequently asked questions about Perl
# Code examples are Public Domain
License:        (GPL+ or Artistic) and Public Domain
Epoch:          0
Version:        5.20210411
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_perlfaq
%endif
BuildArch:      noarch

%description perlfaq
The perlfaq comprises several documents that answer the most commonly asked
questions about Perl and Perl programming.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package PerlIO-via-QuotedPrint
Summary:        PerlIO layer for quoted-printable strings
License:        GPL+ or Artistic
Epoch:          0
Version:        0.09
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_PerlIO_via_QuotedPrint
%endif
BuildArch:      noarch

%description PerlIO-via-QuotedPrint
This module implements a PerlIO layer that works on files encoded in the
quoted-printable format. It will decode from quoted-printable while
reading from a handle, and it will encode as quoted-printable while
writing to a handle.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Perl-OSType
Summary:        Map Perl operating system names to generic types
Version:        1.010
Epoch:          0
License:        GPL+ or Artistic
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Perl_OSType
%endif
BuildArch:      noarch

%description Perl-OSType
Modules that provide OS-specific behaviors often need to know if the current
operating system matches a more generic type of operating systems. For example,
'linux' is a type of 'Unix' operating system and so is 'freebsd'.
This module provides a mapping between an operating system name as given by $^O
and a more generic type. The initial version is based on the OS type mappings
provided in Module::Build and ExtUtils::CBuilder (thus, Microsoft operating
systems are given the type 'Windows' rather than 'Win32').
%endif

%package ph
Summary:        Selected system header files converted to Perl headers
License:        GPL+ or Artistic
Epoch:          0
Version:        %{perl_version}
Requires:       %perl_compat
# Match header files used when building perl.
Requires:       perl-libs%{?_isa} = %{perl_epoch}:%{perl_version}-%{release}
Requires:       perl(warnings)
# We deliver this package only for these three files mentioned in
# a documentation.
Provides:       perl(sys/ioctl.ph) = %{perl_version}
Provides:       perl(sys/syscall.ph) = %{perl_version}
Provides:       perl(syscall.ph) = %{perl_version}
%if %{defined perl_bootstrap}
%gendep_perl_ph
%endif

%description ph
Contemporary Perl still refers to some Perl header (ph) files although it does
not build them anymore. This is a prebuilt collection of the referred files.
If you miss other ones, you can generate them with h2ph tool from perl-utils
package.

%if %{dual_life} || %{rebuild_from_scratch}
%package Pod-Checker
Summary:        Check POD documents for syntax errors
Epoch:          4
Version:        1.74
License:        GPL+ or Artistic
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Pod_Checker
%endif
BuildArch:      noarch

%description Pod-Checker
Module and tools to verify POD documentation contents for compliance with the
Plain Old Documentation format specifications.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Pod-Escapes
Summary:        Resolve POD escape sequences
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        1.07
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Pod_Escapes
%endif
BuildArch:      noarch

%description Pod-Escapes
This module provides things that are useful in decoding Pod E<...> sequences.
%endif

%package Pod-Functions
Summary:        Group Perl functions as in perlfunc POD
License:        GPL+ or Artistic
Epoch:          0
Version:        1.13
BuildArch:      noarch
Requires:       %perl_compat
# Match perl the functions come from
Requires:       perl-libs = %{perl_epoch}:%{perl_version}-%{release}
%if %{defined perl_bootstrap}
%gendep_perl_Pod_Functions
%endif

%description Pod-Functions
This module enumerates the Perl functions that are documented in perlfunc POD.

%package Pod-Html
Summary:        Convert POD files to HTML
License:        GPL+ or Artistic
Epoch:          0
Version:        1.27
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Pod_Html
%endif
BuildArch:      noarch

%description Pod-Html
This package converts files from POD format (see perlpod) to HTML format. It
can automatically generate indexes and cross-references, and it keeps a cache
of things it knows how to cross-reference.

%if %{dual_life} || %{rebuild_from_scratch}
%package Pod-Perldoc
Summary:        Look up Perl documentation in Pod format
License:        GPL+ or Artistic
Epoch:          0
# Real version 3.2801
Version:        3.28.01
%if %{with perl_enables_groff}
# Pod::Perldoc::ToMan executes roff
Requires:       groff-base
%endif
Requires:       %perl_compat
Requires:       perl(File::Temp) >= 0.22
Requires:       perl(HTTP::Tiny)
Requires:       perl(IO::Handle)
Requires:       perl(IPC::Open3)
# POD2::Base is optional
# Pod::Checker is not needed if Pod::Simple::Checker is available
Requires:       perl(Pod::Simple::Checker)
Requires:       perl(Pod::Simple::RTF) >= 3.16
Requires:       perl(Pod::Simple::XMLOutStream) >= 3.16
Requires:       perl(Text::ParseWords)
# Tk is optional
Requires:       perl(Symbol)
%if %{defined perl_bootstrap}
%gendep_perl_Pod_Perldoc
%endif
BuildArch:      noarch

%description Pod-Perldoc
perldoc looks up a piece of documentation in .pod format that is embedded
in the perl installation tree or in a perl script, and displays it via
"groff -man | $PAGER". This is primarily used for the documentation for
the perl library modules.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Pod-Simple
Summary:        Framework for parsing POD documentation
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          1
Version:        3.42
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Pod_Simple
%endif
BuildArch:      noarch

%description Pod-Simple
Pod::Simple is a Perl library for parsing text in the Pod ("plain old
documentation") markup language that is typically used for writing
documentation for Perl and for Perl modules.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Pod-Usage
Summary:        Print a usage message from embedded pod documentation
License:        GPL+ or Artistic
Epoch:          4
Version:        2.01
Requires:       %perl_compat
# Pod::Usage executes perldoc from perl-Pod-Perldoc by default
Requires:       perl-Pod-Perldoc
Requires:       perl(Pod::Text)
%if %{defined perl_bootstrap}
%gendep_perl_Pod_Usage
%endif
BuildArch:      noarch

%description Pod-Usage
pod2usage will print a usage message for the invoking script (using its
embedded POD documentation) and then exit the script with the desired exit
status. The usage message printed may have any one of three levels of
"verboseness": If the verbose level is 0, then only a synopsis is printed.
If the verbose level is 1, then the synopsis is printed along with a
description (if present) of the command line options and arguments. If the
verbose level is 2, then the entire manual page is printed.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package podlators
Summary:        Format POD source into various output formats
License:        (GPL+ or Artistic) and MIT
Epoch:          1
Version:        4.14
BuildArch:      noarch
Requires:       %perl_compat
Requires:       perl(File::Spec) >= 0.8
Requires:       perl(Pod::Simple) >= 3.06
%if %{defined perl_bootstrap}
%gendep_perl_podlators
%endif

%description podlators
This package contains Pod::Man and Pod::Text modules which convert POD input
to *roff source output, suitable for man pages, or plain text.  It also
includes several sub-classes of Pod::Text for formatted output to terminals
with various capabilities.
%endif

%package POSIX
Summary:        Perl interface to IEEE Std 1003.1
License:        GPL+ or Artistic
Epoch:          0
Version:        1.97
Requires:       %perl_compat
Requires:       perl(Carp)
%if %{defined perl_bootstrap}
%gendep_perl_POSIX
%endif


%description POSIX
The POSIX module permits you to access all (or nearly all) the standard POSIX
1003.1 identifiers. Many of these identifiers have been given Perl interfaces.

%package Safe
Summary:        Compile and execute code in restricted compartments
License:        GPL+ or Artistic
Epoch:          0
Version:        2.43
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Safe
%endif
BuildArch:      noarch


%description Safe
The Safe extension module allows the creation of compartments in which Perl
code can be evaluated. Please note that the restriction is not suitable for
security purposes.

%if %{dual_life} || %{rebuild_from_scratch}
%package Scalar-List-Utils
Summary:        A selection of general-utility scalar and list subroutines
License:        GPL+ or Artistic
Epoch:          5
Version:        1.55
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Scalar_List_Utils
%endif

%description Scalar-List-Utils
Scalar::Util and List::Util contain a selection of subroutines that people have
expressed would be nice to have in the perl core, but the usage would not
really be high enough to warrant the use of a keyword, and the size so small
such that being individual extensions would be wasteful.
%endif

%package Search-Dict
Summary:        Search for a key in a dictionary file
License:        GPL+ or Artistic
Epoch:          0
Version:        1.07
Requires:       %perl_compat
Requires:       perl(feature)
%if %{defined perl_bootstrap}
%gendep_perl_Search_Dict
%endif
BuildArch:      noarch


%description Search-Dict
This module sets file position in a file handle to be first line greater than
or equal (string-wise) to a key.

%package SelectSaver
Summary:        Save and restore selected file handle
License:        GPL+ or Artistic
Epoch:          0
Version:        1.02
BuildArch:      noarch
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_SelectSaver
%endif

%description SelectSaver
A "SelectSaver" object contains a reference to the file handle that was
selected when it was created. When the object is destroyed, it re-selects the
file handle that was selected when it was created.

%package SelfLoader
Summary:        Load functions only on demand
License:        GPL+ or Artistic
Epoch:          0
Version:        1.26
BuildArch:      noarch
Requires:       %perl_compat
Requires:       perl(Carp)
%if %{defined perl_bootstrap}
%gendep_perl_SelfLoader
%endif

%description SelfLoader
This Perl module tells its users that functions in a package are to be
autoloaded from after the "__DATA__" token. See also "Autoloading" in
perlsub.

%package sigtrap
Summary:        Perl pragma to enable simple signal handling
License:        GPL+ or Artistic
Epoch:          0
Version:        1.09
BuildArch:      noarch
Requires:       %perl_compat
Requires:       perl(meta_notation) = %{perl_version}
Requires:       perl(Symbol)
%if %{defined perl_bootstrap}
%gendep_perl_sigtrap
%endif

%description sigtrap
The sigtrap pragma is a simple interface for installing signal handlers.

%if %{dual_life} || %{rebuild_from_scratch}
%package Socket
Summary:        C socket.h defines and structure manipulators
License:        GPL+ or Artistic
Epoch:          4
Version:        2.031
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Socket
%endif

%description Socket
This module is just a translation of the C socket.h file.  Unlike the old
mechanism of requiring a translated socket.ph file, this uses the h2xs program
(see the Perl source distribution) and your native C compiler.  This means
that it has a far more likely chance of getting the numbers right.  This
includes all of the commonly used pound-defines like AF_INET, SOCK_STREAM, etc.
%endif

%package sort
Summary:        Perl pragma to control sort() behavior
License:        GPL+ or Artistic
Epoch:          0
Version:        2.04
BuildArch:      noarch
Requires:       %perl_compat
Requires:       perl(Carp)
Requires:       perl(warnings)
%if %{defined perl_bootstrap}
%gendep_perl_sort
%endif

%description sort
With the "sort" pragma you can control the behavior of the builtin "sort()"
function.

%if %{dual_life} || %{rebuild_from_scratch}
%package Storable
Summary:        Persistence for Perl data structures
License:        GPL+ or Artistic
Epoch:          1
Version:        3.23
Requires:       %perl_compat
# Carp substitutes missing Log::Agent
Requires:       perl(Carp)
Requires:       perl(Config)
# Fcntl is optional, but locking is good
Requires:       perl(Fcntl)
Requires:       perl(IO::File)
%if %{defined perl_bootstrap}
%gendep_perl_Storable
%endif

%description Storable
The Storable package brings persistence to your Perl data structures
containing scalar, array, hash or reference objects, i.e. anything that
can be conveniently stored to disk and retrieved at a later time.
%endif

%package subs
Summary:        Perl pragma to predeclare subroutine names
License:        GPL+ or Artistic
Epoch:          0
Version:        1.04
BuildArch:      noarch
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_subs
%endif

%description subs
This will predeclare all the subroutines whose names are in the list,
allowing you to use them without parentheses (as list operators) even
before they're declared.

%package Symbol
Summary:        Manipulate Perl symbols and their names
License:        GPL+ or Artistic
Epoch:          0
Version:        1.09
BuildArch:      noarch
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Symbol
%endif

%description Symbol
The Symbol module provides functions for manipulating Perl symbols.

%package Sys-Hostname
Summary:        Try every conceivable way to get a hostname
License:        GPL+ or Artistic
Epoch:          0
Version:        1.23
Requires:       %perl_compat
Suggests:       perl(POSIX)
Requires:       perl(XSLoader)
%if %{defined perl_bootstrap}
%gendep_perl_Sys_Hostname
%endif


%description Sys-Hostname
It attempts several methods of getting the system hostname and then caches the
result.

%if %{dual_life} || %{rebuild_from_scratch}
%package Sys-Syslog
Summary:        Perl interface to the UNIX syslog(3) calls
License:        GPL+ or Artistic
Epoch:          0
Version:        0.36
Requires:       %perl_compat
Requires:       perl(XSLoader)
%if %{defined perl_bootstrap}
%gendep_perl_Sys_Syslog
%endif

%description Sys-Syslog
Sys::Syslog is an interface to the UNIX syslog(3) function. Call syslog() with
a string priority and a list of printf() arguments just like at syslog(3).
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Term-ANSIColor
Summary:        Color screen output using ANSI escape sequences
License:        GPL+ or Artistic
Epoch:          0
Version:        5.01
Requires:       %perl_compat
Requires:       perl(Carp)
%if %{defined perl_bootstrap}
%gendep_perl_Term_ANSIColor
%endif
BuildArch:      noarch

%description Term-ANSIColor
This module has two interfaces, one through color() and colored() and the
other through constants. It also offers the utility functions uncolor(),
colorstrip(), colorvalid(), and coloralias(), which have to be explicitly
imported to be used.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Term-Cap
Summary:        Perl termcap interface
License:        GPL+ or Artistic
Epoch:          0
Version:        1.17
Requires:       %perl_compat
# ncurses for infocmp tool
Requires:       ncurses
Requires:       perl(Carp)
%if %{defined perl_bootstrap}
%gendep_perl_Term_Cap
%endif
BuildArch:      noarch

%description Term-Cap
These are low-level functions to extract and use capabilities from a terminal
capability (termcap) database.
%endif

%package Term-Complete
Summary:        Perl word completion
License:        GPL+ or Artistic
Epoch:          0
Version:        1.403
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Term_Complete
%endif
BuildArch:      noarch


%description Term-Complete
"Complete" routine provides word completion on a list of words in the array.

%package Term-ReadLine
Summary:        Perl interface to various read-line packages
License:        GPL+ or Artistic
Epoch:          0
Version:        1.17
Requires:       %perl_compat
Requires:       perl(Term::Cap)
%if %{defined perl_bootstrap}
%gendep_perl_Term_ReadLine
%endif
BuildArch:      noarch


%description Term-ReadLine
This package is just a front end to some other packages. It's a stub to
set up a common interface to the various read-line implementations found
on CPAN (under the "Term::ReadLine::*" name space).

%package Test
Summary:        Simple framework for writing test scripts
License:        GPL+ or Artistic
Epoch:          0
Version:        1.31
Requires:       %perl_compat
# Algorithm::Diff 1.15 is optional
Requires:       perl(File::Temp)
%if %{defined perl_bootstrap}
%gendep_perl_Test
%endif
BuildArch:      noarch

%description Test
The Test Perl module simplifies the task of writing test files for Perl modules,
such that their output is in the format that Test::Harness expects to see.

%if %{dual_life} || %{rebuild_from_scratch}
%package Test-Harness
Summary:        Run Perl standard test scripts with statistics
License:        GPL+ or Artistic
Epoch:          1
Version:        3.43
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Test_Harness
%endif
BuildArch:      noarch

%description Test-Harness
Run Perl standard test scripts with statistics.
Use TAP::Parser, Test::Harness package was whole rewritten.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Test-Simple
Summary:        Basic utilities for writing tests
License:        (GPL+ or Artistic) and CC0 and Public Domain
Epoch:          3
Version:        1.302183
Requires:       %perl_compat
Requires:       perl(Data::Dumper)
%if %{defined perl_bootstrap}
%gendep_perl_Test_Simple
%endif
BuildArch:      noarch

%description Test-Simple
Basic utilities for writing tests.
%endif

%package Text-Abbrev
Summary:        Create an abbreviation table from a list
License:        GPL+ or Artistic
Epoch:          0
Version:        1.02
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Text_Abbrev
%endif
BuildArch:      noarch


%description Text-Abbrev
It stores all unambiguous truncations of each element of a list as keys in
an associative array. The values are the original list elements.

%if %{dual_life} || %{rebuild_from_scratch}
%package Text-Balanced
Summary:        Extract delimited text sequences from strings
License:        GPL+ or Artistic
Epoch:          0
Version:        2.04
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Text_Balanced
%endif
BuildArch:      noarch

%description Text-Balanced
These Perl subroutines may be used to extract a delimited substring, possibly
after skipping a specified prefix string.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Text-ParseWords
Summary:        Parse text into an array of tokens or array of arrays
License:        GPL+ or Artistic
Epoch:          0
Version:        3.30
Requires:       %perl_compat
Requires:       perl(Carp)
%if %{defined perl_bootstrap}
%gendep_perl_Text_ParseWords
%endif
BuildArch:      noarch

%description Text-ParseWords
Parse text into an array of tokens or array of arrays.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Text-Tabs+Wrap
Summary:        Expand tabs and do simple line wrapping
License:        TTWL
Epoch:          0
Version:        2013.0523
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Text_Tabs_Wrap
%endif
BuildArch:      noarch

%description Text-Tabs+Wrap
Text::Tabs performs the same job that the UNIX expand(1) and unexpand(1)
commands do: adding or removing tabs from a document.

Text::Wrap::wrap() will reformat lines into paragraphs. All it does is break
up long lines, it will not join short lines together.
%endif

%package Thread
Summary:        Manipulate threads in Perl (for old code only)
License:        GPL+ or Artistic
Epoch:          0
Version:        3.05
BuildArch:      noarch
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Thread
%endif

%description Thread
This Thread module served as the front end to the old-style thread model,
called 5005threads, that has been removed in version 5.10.

For old code and interim backwards compatibility, the Thread module has been
reworked to function as a front end for the new interpreter threads (ithreads)
model. However, some previous functionality is not available. Further, the
data sharing models between the two thread models are completely different,
and anything to do with data sharing has to be thought differently.

You are strongly encouraged to migrate any existing threaded code to the new
model (i.e., use the threads and threads::shared modules) as soon as possible.

%if %{dual_life} || %{rebuild_from_scratch}
%package Thread-Queue
Summary:        Thread-safe queues
License:        GPL+ or Artistic
Epoch:          0
Version:        3.14
Requires:       %perl_compat
Requires:       perl(Carp)
%if %{defined perl_bootstrap}
%gendep_perl_Thread_Queue
%endif
BuildArch:      noarch

%description Thread-Queue
This module provides thread-safe FIFO queues that can be accessed safely by
any number of threads.
%endif

%package Tie
Summary:        Base classes for tying variables
License:        GPL+ or Artistic
Epoch:          0
# Version from Tie::StdHandle
Version:        4.6
BuildArch:      noarch
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Tie
%endif

%description Tie
These are Perl modules that helps connecting classes with arrays, hashes,
handles, and scalars.

%package Tie-File
Summary:        Access the lines of a disk file via a Perl array
License:        GPLv2+ or Artistic
Epoch:          0
Version:        1.06
Requires:       %perl_compat
# Symbol is not used on Perl >= 5.6.0
%if %{defined perl_bootstrap}
%gendep_perl_Tie_File
%endif
BuildArch:      noarch


%description Tie-File
Tie::File represents a regular text file as a Perl array. Each element in the
array corresponds to a record in the file. The first line of the file is
element 0 of the array; the second line is element 1, and so on.  The file is
not loaded into memory, so this will work even for gigantic files.  Changes to
the array are reflected in the file immediately.

%package Tie-Memoize
Summary:        Add data to a hash when needed
License:        GPLv2+ or Artistic
Epoch:          0
Version:        1.1
Requires:       %perl_compat
Requires:       perl(Carp)
Requires:       perl(Tie::ExtraHash)
%if %{defined perl_bootstrap}
%gendep_perl_Tie_Memoize
%endif
BuildArch:      noarch


%description Tie-Memoize
This package allows a tied hash to load its values automatically on the first
access, and to use the cached value on the following accesses.

%if %{dual_life} || %{rebuild_from_scratch}
%package Tie-RefHash
Summary:        Use references as hash keys
License:        GPL+ or Artistic
Epoch:          0
Version:        1.40
Requires:       %perl_compat
# Scalar::Util || overload
Requires:       perl(overload)
Suggests:       perl(Scalar::Util)
%if %{defined perl_bootstrap}
%gendep_perl_Tie_RefHash
%endif
BuildArch:      noarch


%description Tie-RefHash
This module provides the ability to use references as hash keys if you first
"tie" the hash variable to this module. Normally, only the keys of the tied
hash itself are preserved as references; to use references as keys in
hashes-of-hashes, use Tie::RefHash::Nestable, included as part of
Tie::RefHash.
%endif

%package Time
Summary:        By-name interface to Perl built-in time functions
License:        GPL+ or Artistic
Epoch:          0
Version:        1.03
BuildArch:      noarch
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Time
%endif


%description Time
This package provides an object-oriented interface to Perl built-in gmtime()
and localtime () functions.

%if %{dual_life} || %{rebuild_from_scratch}
%package Time-HiRes
Summary:        High resolution alarm, sleep, gettimeofday, interval timers
License:        GPL+ or Artistic
Epoch:          4
Version:        1.9767
Requires:       %perl_compat
Requires:       perl(Carp)
%if %{defined perl_bootstrap}
%gendep_perl_Time_HiRes
%endif

%description Time-HiRes
The Time::HiRes module implements a Perl interface to the usleep, nanosleep,
ualarm, gettimeofday, and setitimer/getitimer system calls, in other words,
high resolution time and timers.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Time-Local
Summary:        Efficiently compute time from local and GMT time
License:        GPL+ or Artistic
Epoch:          2
# Real version 1.30
Version:        1.300
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Time_Local
%endif
BuildArch:      noarch

%description Time-Local
This module provides functions that are the inverse of built-in perl functions
localtime() and gmtime(). They accept a date as a six-element array, and
return the corresponding time(2) value in seconds since the system epoch
(Midnight, January 1, 1970 GMT on Unix, for example). This value can be
positive or negative, though POSIX only requires support for positive values,
so dates before the system's epoch may not work on all operating systems.
%endif

%package Time-Piece
Summary:        Time objects from localtime and gmtime
License:        (GPL+ or Artistic) and BSD
Epoch:          0
Version:        1.3401
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_Time_Piece
%endif

%description Time-Piece
The Time::Piece module replaces the standard localtime and gmtime functions
with implementations that return objects.  It does so in a backwards compatible
manner, so that using localtime or gmtime as documented in perlfunc still
behave as expected.

%package Thread-Semaphore
Summary:        Thread-safe semaphores
License:        GPL+ or Artistic
Epoch:          0
Version:        2.13
Requires:       %perl_compat
Requires:       perl(Carp)
%if %{defined perl_bootstrap}
%gendep_perl_Thread_Semaphore
%endif
BuildArch:      noarch


%description Thread-Semaphore
Semaphores provide a mechanism to regulate access to resources. Unlike locks,
semaphores aren't tied to particular scalars, and so may be used to control
access to anything you care to use them for. Semaphores don't limit their
values to zero and one, so they can be used to control access to some resource
that there may be more than one of (e.g., file handles). Increment and
decrement amounts aren't fixed at one either, so threads can reserve or return
multiple resources at once.

%if %{dual_life} || %{rebuild_from_scratch}
%package threads
Summary:        Perl interpreter-based threads
License:        GPL+ or Artistic
Epoch:          1
Version:        2.26
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_threads
%endif

%description threads
Since Perl 5.8, thread programming has been available using a model called
interpreter threads  which provides a new Perl interpreter for each thread,
and, by default, results in no data or state information being shared between
threads.

(Prior to Perl 5.8, 5005threads was available through the Thread.pm API. This
threading model has been deprecated, and was removed as of Perl 5.10.0.)

As just mentioned, all variables are, by default, thread local. To use shared
variables, you need to also load threads::shared.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package threads-shared
Summary:        Perl extension for sharing data structures between threads
License:        GPL+ or Artistic
Epoch:          0
Version:        1.62
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_threads_shared
%endif

%description threads-shared
By default, variables are private to each thread, and each newly created thread
gets a private copy of each existing variable. This module allows you to share
variables across different threads (and pseudo-forks on Win32). It is used
together with the threads module.  This module supports the sharing of the
following data types only: scalars and scalar refs, arrays and array refs, and
hashes and hash refs.
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Unicode-Collate
Summary:        Unicode Collation Algorithm
License:        (GPL+ or Artistic) and Unicode
Epoch:          0
Version:        1.29
Requires:       %perl_compat
Requires:       perl(Unicode::Normalize)
%if %{defined perl_bootstrap}
%gendep_perl_Unicode_Collate
%endif

%description Unicode-Collate
This package is Perl implementation of Unicode Technical Standard #10 (Unicode
Collation Algorithm).
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%package Unicode-Normalize
Summary:        Unicode Normalization Forms
License:        GPL+ or Artistic
Epoch:          0
Version:        1.28
Requires:       %perl_compat
# unicore/CombiningClass.pl and unicore/Decomposition.pl from perl, perl is
# auto-detected.
%if %{defined perl_bootstrap}
%gendep_perl_Unicode_Normalize
%endif

%description Unicode-Normalize
This package provides Perl functions that can convert strings into various
Unicode normalization forms as defined in Unicode Standard Annex #15.
%endif

%package Unicode-UCD
Summary:        Unicode character database
License:        GPL+ or Artistic
Epoch:          0
Version:        0.75
BuildArch:      noarch
Requires:       %perl_compat
Requires:       perl(Storable)
%if %{defined perl_bootstrap}
%gendep_perl_Unicode_UCD
%endif

%description Unicode-UCD
The Unicode::UCD module offers a series of functions that provide a simple
interface to the Unicode Character Database.

%package User-pwent
Summary:        By-name interface to Perl built-in user name resolver
License:        GPL+ or Artistic
Epoch:          0
Version:        1.03
BuildArch:      noarch
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_User_pwent
%endif


%description User-pwent
This package provides an object-oriented interface to Perl build-in getgr*()
and getpw*() functions.

%package vars
Summary:        Perl pragma to predeclare global variable names
License:        GPL+ or Artistic
Epoch:          0
Version:        1.05
BuildArch:      noarch
Requires:       %perl_compat
Requires:       perl(Carp)
%if %{defined perl_bootstrap}
%gendep_perl_vars
%endif

%description vars
This pragma will predeclare all the variables whose names are in the
list, allowing you to use them under "use strict", and disabling any
typo warnings for them.

For use with variables in the current package for a single scope, the
functionality provided by this pragma has been superseded by "our"
declarations, available in Perl v5.6.0 or later, and use of this pragma is
discouraged.

%if %{dual_life} || %{rebuild_from_scratch}
%package version
Summary:        Perl extension for Version Objects
License:        GPL+ or Artistic
# Epoch bump for clean upgrade over old standalone package
Epoch:          8
# real version 0.9928
Version:        0.99.28
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_version
%endif
BuildArch:      noarch

%description version
Perl extension for Version Objects
%endif

%package vmsish
Summary:        Perl pragma to control VMS-specific language features
License:        GPL+ or Artistic
Epoch:          0
Version:        1.04
BuildArch:      noarch
Requires:       %perl_compat
%if %{defined perl_bootstrap}
%gendep_perl_vmsish
%endif

%description vmsish
The "vmsish" pragma control VMS-specific features of the Perl language. If
you're not running VMS, this module does nothing.

%prep
%setup -q -n perl-%{perl_version}
%patch5 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch200 -p1
%patch201 -p1

#copy Pod-Html license clarification
cp %{SOURCE6} .

#
# Candidates for doc recoding (need case by case review):
# find . -name "*.pod" -o -name "README*" -o -name "*.pm" | xargs file -i | grep charset= | grep -v '\(us-ascii\|utf-8\)'
recode()
{
        iconv -f "${2:-iso-8859-1}" -t utf-8 < "$1" > "${1}_"
        touch -r "$1" "${1}_"
        mv -f "${1}_" "$1"
}
# TODO iconv fail on this one
##recode README.tw big5
#recode pod/perlebcdic.pod
#recode pod/perlhack.pod
#recode pod/perlhist.pod
#recode pod/perlthrtut.pod
#recode AUTHORS

find . -name \*.orig -exec rm -fv {} \;

# Configure Compress::Zlib to use system zlib
sed -i 's|BUILD_ZLIB      = True|BUILD_ZLIB      = False|
    s|INCLUDE         = ./zlib-src|INCLUDE         = %{_includedir}|
    s|LIB             = ./zlib-src|LIB             = %{_libdir}|' \
    cpan/Compress-Raw-Zlib/config.in

# Ensure that we never accidentally bundle zlib or bzip2
rm -rf cpan/Compress-Raw-Zlib/zlib-src
rm -rf cpan/Compress-Raw-Bzip2/bzip2-src
sed -i '/\(bzip2\|zlib\)-src/d' MANIFEST

%if !%{with gdbm}
# Do not install anything requiring NDBM_File if NDBM is not available.
rm -rf 'cpan/Memoize/Memoize/NDBM_File.pm'
sed -i '\|cpan/Memoize/Memoize/NDBM_File.pm|d' MANIFEST
%endif


%build
echo "RPM Build arch: %{_arch}"

%global perl_abi    %(echo '%{perl_version}' | sed 's/^\\([^.]*\\.[^.]*\\).*/\\1/')

# ldflags is not used when linking XS modules.
# Only ldflags is used when linking miniperl.
# Only ccflags and ldflags are used for Configure's compiler checks.
# Set optimize=none to prevent from injecting upstream's value.
/bin/sh Configure -des \
        -Doptimize="none" \
        -Dccflags="$RPM_OPT_FLAGS" \
        -Dldflags="$RPM_LD_FLAGS" \
        -Dccdlflags="-Wl,--enable-new-dtags $RPM_LD_FLAGS" \
        -Dlddlflags="-shared $RPM_LD_FLAGS" \
        -Dshrpdir="%{_libdir}" \
        -DDEBUGGING=-g \
        -Dversion=%{perl_version} \
        -Dmyhostname=localhost \
        -Dperladmin=root@localhost \
        -Dcc='%{__cc}' \
        -Dcf_by='Red Hat, Inc.' \
        -Dprefix=%{_prefix} \
%if %{without perl_enables_groff}
        -Dman1dir="%{_mandir}/man1" \
        -Dman3dir="%{_mandir}/man3" \
%endif
        -Dvendorprefix=%{_prefix} \
        -Dsiteprefix=%{_prefix}/local \
        -Dsitelib="%{_prefix}/local/share/perl5/%{perl_abi}" \
        -Dsitearch="%{_prefix}/local/%{_lib}/perl5/%{perl_abi}" \
        -Dprivlib="%{privlib}" \
        -Dvendorlib="%{perl_vendorlib}" \
        -Darchlib="%{archlib}" \
        -Dvendorarch="%{perl_vendorarch}" \
        -Darchname=%{perl_archname} \
%ifarch %{multilib_64_archs}
        -Dlibpth="/usr/local/lib64 /lib64 %{_prefix}/lib64" \
%endif
%ifarch sparc sparcv9
        -Ud_longdbl \
%endif
        -Duseshrplib \
        -Dusethreads \
        -Duseithreads \
%if %{with perl_enables_systemtap}
        -Dusedtrace='/usr/bin/dtrace' \
%else
        -Uusedtrace \
%endif
        -Duselargefiles \
        -Dd_semctl_semun \
        -Di_db \
%if %{with gdbm}
        -Ui_ndbm \
        -Di_gdbm \
%endif
        -Di_shadow \
        -Di_syslog \
        -Dman3ext=3pm \
        -Duseperlio \
        -Dinstallusrbinperl=n \
        -Ubincompat5005 \
        -Uversiononly \
        -Dpager='/usr/bin/less -isr' \
        -Dd_gethostent_r_proto -Ud_endhostent_r_proto -Ud_sethostent_r_proto \
        -Ud_endprotoent_r_proto -Ud_setprotoent_r_proto \
        -Ud_endservent_r_proto -Ud_setservent_r_proto \
        -Dscriptdir='%{_bindir}' \
        -Dusesitecustomize \
        -Duse64bitint

# -Duseshrplib creates libperl.so, -Ubincompat5005 help create DSO -> libperl.so

BUILD_BZIP2=0
BZIP2_LIB=%{_libdir}
export BUILD_BZIP2 BZIP2_LIB

# Prepare a symlink from proper DSO name to libperl.so now so that new perl
# can be executed from make.
%global soname libperl.so.%{perl_abi}
test -L %soname || ln -s libperl.so %soname

%ifarch sparc64 %{arm}
make
%else
make %{?_smp_mflags}
%endif

%install
make install DESTDIR=$RPM_BUILD_ROOT

%global build_archlib $RPM_BUILD_ROOT%{archlib}
%global build_privlib $RPM_BUILD_ROOT%{privlib}
%global build_bindir  $RPM_BUILD_ROOT%{_bindir}
%global new_perl LD_PRELOAD="%{build_archlib}/CORE/libperl.so" \\\
    LD_LIBRARY_PATH="%{build_archlib}/CORE" \\\
    PERL5LIB="%{build_archlib}:%{build_privlib}" \\\
    %{build_bindir}/perl

# Make proper DSO names, move libperl to standard path.
mv "%{build_archlib}/CORE/libperl.so" \
    "$RPM_BUILD_ROOT%{_libdir}/libperl.so.%{perl_version}"
ln -s "libperl.so.%{perl_version}" "$RPM_BUILD_ROOT%{_libdir}/%{soname}"
ln -s "libperl.so.%{perl_version}" "$RPM_BUILD_ROOT%{_libdir}/libperl.so"
# XXX: Keep symlink from original location because various code glues
# $archlib/CORE/$libperl to get the DSO.
ln -s "../../libperl.so.%{perl_version}" "%{build_archlib}/CORE/libperl.so"
# XXX: Remove the soname named file from CORE directory that was created as
# a symlink in build section and installed as a regular file by perl build
# system.
rm -f "%{build_archlib}/CORE/%{soname}"

install -p -m 755 utils/pl2pm %{build_bindir}/pl2pm

# perlfunc/ioctl() recommends sys/ioctl.ph.
# perlfaq5 recommends sys/syscall.ph.
# perlfunc/syscall() recommends syscall.ph.
for i in sys/ioctl.h sys/syscall.h syscall.h
do
    %{new_perl} %{build_bindir}/h2ph -a -d %{build_archlib} $i || true
done

# vendor directories (in this case for third party rpms)
# perl doesn't create the auto subdirectory, but modules put things in it,
# so we need to own it.

mkdir -p $RPM_BUILD_ROOT%{perl_vendorarch}/auto
mkdir -p $RPM_BUILD_ROOT%{perl_vendorlib}

#
# perl RPM macros
#
mkdir -p ${RPM_BUILD_ROOT}%{_rpmmacrodir}
install -p -m 644 %{SOURCE3} ${RPM_BUILD_ROOT}%{_rpmmacrodir}

#
# Core modules removal
#
# Dual-living binaries clashes on debuginfo files between perl and standalone
# packages. Excluding is not enough, we need to remove them. This is
# a work-around for rpmbuild bug #878863.
find $RPM_BUILD_ROOT -type f -name '*.bs' -empty -delete
chmod -R u+w $RPM_BUILD_ROOT/*

# miniperl? As an interpreter? How odd. Anyway, a symlink does it:
rm %{build_privlib}/ExtUtils/xsubpp
ln -s ../../../bin/xsubpp %{build_privlib}/ExtUtils/

# Don't need the .packlist
rm %{build_archlib}/.packlist

# Do not distribute File::Spec::VMS as it works on VMS only (bug #973713)
# We cannot remove it in %%prep because dist/Cwd/t/Spec.t test needs it.
rm %{build_archlib}/File/Spec/VMS.pm
rm $RPM_BUILD_ROOT%{_mandir}/man3/File::Spec::VMS.3*

# Do not distribute ExtUtils-PL2Bat, it is used only for Windows
rm %{build_privlib}/ExtUtils/PL2Bat.pm
rm $RPM_BUILD_ROOT%{_mandir}/man3/ExtUtils::PL2Bat.3*

# Fix some manpages to be UTF-8
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1/
pushd $RPM_BUILD_ROOT%{_mandir}/man1/
  for i in perl588delta.1 perldelta.1 ; do
    iconv -f MS-ANSI -t UTF-8 $i --output new-$i
    rm $i
    mv new-$i $i
  done
popd

# for now, remove Bzip2:
# Why? Now is missing Bzip2 files and provides
##find $RPM_BUILD_ROOT -name Bzip2 | xargs rm -r
##find $RPM_BUILD_ROOT -name '*B*zip2*'| xargs rm

# tests -- FIXME need to validate that this all works as expected
mkdir -p %{buildroot}%{perl5_testdir}/perl-tests

# "core"
tar -cf - t/ | ( cd %{buildroot}%{perl5_testdir}/perl-tests && tar -xf - )

# "dual-lifed"
for dir in `find ext/ -type d -name t -maxdepth 2` ; do

    tar -cf - $dir | ( cd %{buildroot}%{perl5_testdir}/perl-tests/t && tar -xf - )
done

# Normalize shell bangs in tests.
# brp-mangle-shebangs executed by rpm-build chokes on t/TEST.
%{new_perl} -MConfig -i -pn \
    -e 's"\A#!(?:perl|\./perl|/perl|/usr/bin/perl|/usr/bin/env perl)\b"$Config{startperl}"' \
    $(find %{buildroot}%{perl5_testdir}/perl-tests -type f)

%if %{with perl_enables_systemtap}
# Systemtap tapset install
mkdir -p %{buildroot}%{tapsetdir}
%ifarch %{multilib_64_archs}
%global libperl_stp libperl%{perl_version}-64.stp
%else
%global libperl_stp libperl%{perl_version}-32.stp
%endif

sed \
  -e "s|LIBRARY_PATH|%{_libdir}/%{soname}|" \
  %{SOURCE4} \
  > %{buildroot}%{tapsetdir}/%{libperl_stp}
%endif

%if ! %{dual_life} && ! %{rebuild_from_scratch}
# All dual_life files/directories are deleted here instead of %%exclude in
# %%files. So that debuginfo does not find unpacked binaries and blindly
# symlinks to them at random packages.

# Archive-Tar
rm %{buildroot}%{_bindir}/ptar
rm %{buildroot}%{_bindir}/ptardiff
rm %{buildroot}%{_bindir}/ptargrep
rm -rf %{buildroot}%{privlib}/Archive/Tar
rm %{buildroot}%{privlib}/Archive/Tar.pm
rm -rf %{buildroot}%{privlib}/Archive
rm %{buildroot}%{_mandir}/man1/ptar.1*
rm %{buildroot}%{_mandir}/man1/ptardiff.1*
rm %{buildroot}%{_mandir}/man1/ptargrep.1*
rm %{buildroot}%{_mandir}/man3/Archive::Tar*

# autodie
rm -rf %{buildroot}%{privlib}/autodie/
rm %{buildroot}%{privlib}/autodie.pm
rm %{buildroot}%{privlib}/Fatal.pm
rm %{buildroot}%{_mandir}/man3/autodie.3*
rm %{buildroot}%{_mandir}/man3/autodie::*
rm %{buildroot}%{_mandir}/man3/Fatal.3*

# bignum
rm %{buildroot}%{privlib}/bigint.pm
rm %{buildroot}%{privlib}/bignum.pm
rm %{buildroot}%{privlib}/bigrat.pm
rm -rf %{buildroot}%{privlib}/Math/BigFloat
rm %{buildroot}%{privlib}/Math/BigInt/Trace.pm
rm %{buildroot}%{_mandir}/man3/bigint.*
rm %{buildroot}%{_mandir}/man3/bignum.*
rm %{buildroot}%{_mandir}/man3/bigrat.*

# Carp
rm -rf %{buildroot}%{privlib}/Carp
rm %{buildroot}%{privlib}/Carp.*
rm %{buildroot}%{_mandir}/man3/Carp.*

# Compress-Raw-Bzip2
rm %{buildroot}%{archlib}/Compress/Raw/Bzip2.pm
rm -rf %{buildroot}%{archlib}/auto/Compress/Raw/Bzip2
rm %{buildroot}%{_mandir}/man3/Compress::Raw::Bzip2*

# Compress-Raw-Zlib
rm %{buildroot}%{archlib}/Compress/Raw/Zlib.pm
rm -rf %{buildroot}%{archlib}/Compress/Raw
rm -rf %{buildroot}%{archlib}/Compress
rm -rf %{buildroot}%{archlib}/auto/Compress/Raw/Zlib
rm -rf %{buildroot}%{archlib}/auto/Compress/Raw
rm -rf %{buildroot}%{archlib}/auto/Compress
rm %{buildroot}%{_mandir}/man3/Compress::Raw::Zlib*

# Config-Perl-V
rm -rf %{buildroot}%{privlib}/Config/Perl
rm %{buildroot}%{_mandir}/man3/Config::Perl::V.*

# constant
rm %{buildroot}%{privlib}/constant.pm
rm %{buildroot}%{_mandir}/man3/constant.3*

# CPAN-Meta-Requirements
rm %{buildroot}%{privlib}/CPAN/Meta/Requirements.pm
rm %{buildroot}%{_mandir}/man3/CPAN::Meta::Requirements.3*

# CPAN-Meta-YAML
rm %{buildroot}%{privlib}/CPAN/Meta/YAML.pm
rm %{buildroot}%{_mandir}/man3/CPAN::Meta::YAML*

# CPAN-Meta
rm %{buildroot}%{privlib}/CPAN/Meta.pm
rm %{buildroot}%{privlib}/CPAN/Meta/Converter.pm
rm %{buildroot}%{privlib}/CPAN/Meta/Feature.pm
rm -rf %{buildroot}%{privlib}/CPAN/Meta/History
rm %{buildroot}%{privlib}/CPAN/Meta/History.pm
rm %{buildroot}%{privlib}/CPAN/Meta/Merge.pm
rm %{buildroot}%{privlib}/CPAN/Meta/Prereqs.pm
rm %{buildroot}%{privlib}/CPAN/Meta/Spec.pm
rm %{buildroot}%{privlib}/CPAN/Meta/Validator.pm
rm -rf %{buildroot}%{privlib}/CPAN/Meta
rm %{buildroot}%{privlib}/Parse/CPAN/Meta.pm
rm -rf %{buildroot}%{privlib}/Parse/CPAN
rm -rf %{buildroot}%{privlib}/Parse
rm %{buildroot}%{_mandir}/man3/CPAN::Meta*
rm %{buildroot}%{_mandir}/man3/Parse::CPAN::Meta.3*

# CPAN
rm %{buildroot}%{_bindir}/cpan
rm %{buildroot}%{privlib}/App/Cpan.pm
rm -rf %{buildroot}%{privlib}/CPAN
rm %{buildroot}%{privlib}/CPAN.pm
rm %{buildroot}%{_mandir}/man1/cpan.1*
rm %{buildroot}%{_mandir}/man3/App::Cpan.*
rm %{buildroot}%{_mandir}/man3/CPAN.*
rm %{buildroot}%{_mandir}/man3/CPAN:*

# Data-Dumper
rm %{buildroot}%{archlib}/auto/Data/Dumper/Dumper.so
rm %{buildroot}%{archlib}/Data/Dumper.pm
rm -rf %{buildroot}%{archlib}/auto/Data/Dumper
rm -rf %{buildroot}%{archlib}/auto/Data
rm -rf %{buildroot}%{archlib}/Data
rm %{buildroot}%{_mandir}/man3/Data::Dumper.3*

# Devel-PPPort
rm %{buildroot}%{archlib}/Devel/PPPort.pm
rm %{buildroot}%{_mandir}/man3/Devel::PPPort.3*

# Digest
rm %{buildroot}%{privlib}/Digest.pm
rm %{buildroot}%{privlib}/Digest/base.pm
rm %{buildroot}%{privlib}/Digest/file.pm
rm -rf %{buildroot}%{privlib}/Digest
rm %{buildroot}%{_mandir}/man3/Digest.3*
rm %{buildroot}%{_mandir}/man3/Digest::base.3*
rm %{buildroot}%{_mandir}/man3/Digest::file.3*

# Digest-MD5
rm %{buildroot}%{archlib}/Digest/MD5.pm
rm -rf %{buildroot}%{archlib}/auto/Digest/MD5
rm %{buildroot}%{_mandir}/man3/Digest::MD5.3*

# Digest-SHA
rm %{buildroot}%{_bindir}/shasum
rm %{buildroot}%{archlib}/Digest/SHA.pm
rm -rf %{buildroot}%{archlib}/Digest
rm -rf %{buildroot}%{archlib}/auto/Digest/SHA
rm -rf %{buildroot}%{archlib}/auto/Digest
rm %{buildroot}%{_mandir}/man1/shasum.1*
rm %{buildroot}%{_mandir}/man3/Digest::SHA.3*

# Encode
rm %{buildroot}%{_bindir}/encguess
rm %{buildroot}%{_bindir}/piconv
rm -rf %{buildroot}%{archlib}/Encode*
rm -rf %{buildroot}%{archlib}/auto/Encode*
rm %{buildroot}%{_mandir}/man1/encguess.1*
rm %{buildroot}%{_mandir}/man1/piconv.1*
rm %{buildroot}%{_mandir}/man3/Encode*.3*

# encoding
rm %{buildroot}%{archlib}/encoding.pm
rm %{buildroot}%{_mandir}/man3/encoding.3*

# Encode-devel
rm %{buildroot}%{_bindir}/enc2xs
rm %{buildroot}%{privlib}/Encode/*.e2x
rm %{buildroot}%{privlib}/Encode/encode.h
rm -rf %{buildroot}%{privlib}/Encode
rm %{buildroot}%{_mandir}/man1/enc2xs.1*

# Env
rm %{buildroot}%{privlib}/Env.pm
rm %{buildroot}%{_mandir}/man3/Env.3*

# Exporter
rm -rf %{buildroot}%{privlib}/Exporter*
rm %{buildroot}%{_mandir}/man3/Exporter*

# experimental
rm %{buildroot}%{privlib}/experimental*
rm %{buildroot}%{_mandir}/man3/experimental*

# ExtUtils-CBuilder
rm %{buildroot}%{privlib}/ExtUtils/CBuilder.pm
rm -rf %{buildroot}%{privlib}/ExtUtils/CBuilder
rm %{buildroot}%{_mandir}/man3/ExtUtils::CBuilder*

# ExtUtils-Command
rm %{buildroot}%{privlib}/ExtUtils/Command.pm
rm %{buildroot}%{_mandir}/man3/ExtUtils::Command.*

# ExtUtils-Install
rm %{buildroot}%{privlib}/ExtUtils/Install.pm
rm %{buildroot}%{privlib}/ExtUtils/Installed.pm
rm %{buildroot}%{privlib}/ExtUtils/Packlist.pm
rm %{buildroot}%{_mandir}/man3/ExtUtils::Install.3*
rm %{buildroot}%{_mandir}/man3/ExtUtils::Installed.3*
rm %{buildroot}%{_mandir}/man3/ExtUtils::Packlist.3*

# ExtUtils-Manifest
rm %{buildroot}%{privlib}/ExtUtils/Manifest.pm
rm %{buildroot}%{privlib}/ExtUtils/MANIFEST.SKIP
rm %{buildroot}%{_mandir}/man3/ExtUtils::Manifest.3*

# ExtUtils-MakeMaker
rm %{buildroot}%{_bindir}/instmodsh
rm -rf %{buildroot}%{privlib}/ExtUtils/Command
rm -rf %{buildroot}%{privlib}/ExtUtils/Liblist
rm %{buildroot}%{privlib}/ExtUtils/Liblist.pm
rm -rf %{buildroot}%{privlib}/ExtUtils/MakeMaker
rm %{buildroot}%{privlib}/ExtUtils/MakeMaker.pm
rm %{buildroot}%{privlib}/ExtUtils/MM.pm
rm %{buildroot}%{privlib}/ExtUtils/MM_*.pm
rm %{buildroot}%{privlib}/ExtUtils/MY.pm
rm %{buildroot}%{privlib}/ExtUtils/Mkbootstrap.pm
rm %{buildroot}%{privlib}/ExtUtils/Mksymlists.pm
rm %{buildroot}%{privlib}/ExtUtils/testlib.pm
rm %{buildroot}%{_mandir}/man1/instmodsh.1*
rm %{buildroot}%{_mandir}/man3/ExtUtils::Command::MM*
rm %{buildroot}%{_mandir}/man3/ExtUtils::Liblist.3*
rm %{buildroot}%{_mandir}/man3/ExtUtils::MM.3*
rm %{buildroot}%{_mandir}/man3/ExtUtils::MM_*
rm %{buildroot}%{_mandir}/man3/ExtUtils::MY.3*
rm %{buildroot}%{_mandir}/man3/ExtUtils::MakeMaker*
rm %{buildroot}%{_mandir}/man3/ExtUtils::Mkbootstrap.3*
rm %{buildroot}%{_mandir}/man3/ExtUtils::Mksymlists.3*
rm %{buildroot}%{_mandir}/man3/ExtUtils::testlib.3*

# ExtUtils-MM-Utils
rm %{buildroot}%{privlib}/ExtUtils/MM/Utils.pm
rm -rf %{buildroot}%{privlib}/ExtUtils/MM
rm %{buildroot}%{_mandir}/man3/ExtUtils::MM::Utils.*

# ExtUtils-ParseXS
rm %{buildroot}%{privlib}/ExtUtils/ParseXS.pm
rm %{buildroot}%{privlib}/ExtUtils/ParseXS.pod
rm %{buildroot}%{privlib}/ExtUtils/ParseXS/Constants.pm
rm %{buildroot}%{privlib}/ExtUtils/ParseXS/CountLines.pm
rm %{buildroot}%{privlib}/ExtUtils/ParseXS/Eval.pm
rm %{buildroot}%{privlib}/ExtUtils/ParseXS/Utilities.pm
rm -rf %{buildroot}%{privlib}/ExtUtils/ParseXS
rm %{buildroot}%{privlib}/ExtUtils/Typemaps.pm
rm %{buildroot}%{privlib}/ExtUtils/Typemaps/Cmd.pm
rm %{buildroot}%{privlib}/ExtUtils/Typemaps/InputMap.pm
rm %{buildroot}%{privlib}/ExtUtils/Typemaps/OutputMap.pm
rm %{buildroot}%{privlib}/ExtUtils/Typemaps/Type.pm
rm -rf %{buildroot}%{privlib}/ExtUtils/Typemaps
rm %{buildroot}%{privlib}/ExtUtils/xsubpp
rm %{buildroot}%{privlib}/pod/perlxs.pod
rm %{buildroot}%{privlib}/pod/perlxstut.pod
rm %{buildroot}%{privlib}/pod/perlxstypemap.pod
rm %{buildroot}%{_bindir}/xsubpp
rm %{buildroot}%{_mandir}/man1/perlxs*
rm %{buildroot}%{_mandir}/man1/xsubpp*
rm %{buildroot}%{_mandir}/man3/ExtUtils::ParseXS.3*
rm %{buildroot}%{_mandir}/man3/ExtUtils::ParseXS::Constants.3*
rm %{buildroot}%{_mandir}/man3/ExtUtils::ParseXS::Eval.3*
rm %{buildroot}%{_mandir}/man3/ExtUtils::ParseXS::Utilities.3*
rm %{buildroot}%{_mandir}/man3/ExtUtils::Typemaps.3*
rm %{buildroot}%{_mandir}/man3/ExtUtils::Typemaps::Cmd.3*
rm %{buildroot}%{_mandir}/man3/ExtUtils::Typemaps::InputMap.3*
rm %{buildroot}%{_mandir}/man3/ExtUtils::Typemaps::OutputMap.3*
rm %{buildroot}%{_mandir}/man3/ExtUtils::Typemaps::Type.3*

# File-Fetch
rm %{buildroot}%{privlib}/File/Fetch.pm
rm %{buildroot}%{_mandir}/man3/File::Fetch.3*

# File-Path
rm %{buildroot}%{privlib}/File/Path.pm
rm %{buildroot}%{_mandir}/man3/File::Path.3*

# File-Temp
rm %{buildroot}%{privlib}/File/Temp.pm
rm %{buildroot}%{_mandir}/man3/File::Temp.3*

# Filter
rm -rf %{buildroot}%{archlib}/auto/Filter/Util
rm -rf %{buildroot}%{archlib}/auto/Filter
rm -rf %{buildroot}%{archlib}/Filter/Util
rm -rf %{buildroot}%{archlib}/Filter
rm %{buildroot}%{privlib}/pod/perlfilter.pod
rm %{buildroot}%{_mandir}/man1/perlfilter.*
rm %{buildroot}%{_mandir}/man3/Filter::Util::*

# Filter-Simple
rm %{buildroot}%{privlib}/Filter/Simple.pm
rm -rf %{buildroot}%{privlib}/Filter
rm %{buildroot}%{_mandir}/man3/Filter::Simple.3*

# Getopt-Long
rm %{buildroot}%{privlib}/Getopt/Long.pm
rm %{buildroot}%{_mandir}/man3/Getopt::Long.3*

# IO-Compress
rm %{buildroot}%{_bindir}/streamzip
rm %{buildroot}%{_bindir}/zipdetails
rm %{buildroot}%{privlib}/IO/Compress/FAQ.pod
rm %{buildroot}%{_mandir}/man1/streamzip.*
rm %{buildroot}%{_mandir}/man1/zipdetails.*
rm %{buildroot}%{_mandir}/man3/IO::Compress::FAQ.*
# Compress-Zlib
rm %{buildroot}%{privlib}/Compress/Zlib.pm
rm -rf %{buildroot}%{privlib}/Compress
rm %{buildroot}%{_mandir}/man3/Compress::Zlib*
# IO-Compress-Base
rm %{buildroot}%{privlib}/File/GlobMapper.pm
rm %{buildroot}%{privlib}/IO/Compress/Base.pm
rm -rf %{buildroot}%{privlib}/IO/Compress/Base
rm %{buildroot}%{privlib}/IO/Uncompress/AnyUncompress.pm
rm %{buildroot}%{privlib}/IO/Uncompress/Base.pm
rm %{buildroot}%{_mandir}/man3/File::GlobMapper.*
rm %{buildroot}%{_mandir}/man3/IO::Compress::Base.*
rm %{buildroot}%{_mandir}/man3/IO::Uncompress::AnyUncompress.*
rm %{buildroot}%{_mandir}/man3/IO::Uncompress::Base.*
# IO-Compress-Zlib
rm %{buildroot}%{privlib}/IO/Compress/Bzip2.pm
rm %{buildroot}%{privlib}/IO/Compress/Deflate.pm
rm %{buildroot}%{privlib}/IO/Compress/Gzip.pm
rm %{buildroot}%{privlib}/IO/Compress/RawDeflate.pm
rm %{buildroot}%{privlib}/IO/Compress/Zip.pm
rm -rf %{buildroot}%{privlib}/IO/Compress/Adapter
rm -rf %{buildroot}%{privlib}/IO/Compress/Gzip
rm -rf %{buildroot}%{privlib}/IO/Compress/Zip
rm -rf %{buildroot}%{privlib}/IO/Compress/Zlib
rm -rf %{buildroot}%{privlib}/IO/Compress
rm %{buildroot}%{privlib}/IO/Uncompress/AnyInflate.pm
rm %{buildroot}%{privlib}/IO/Uncompress/Bunzip2.pm
rm %{buildroot}%{privlib}/IO/Uncompress/Gunzip.pm
rm %{buildroot}%{privlib}/IO/Uncompress/Inflate.pm
rm %{buildroot}%{privlib}/IO/Uncompress/RawInflate.pm
rm %{buildroot}%{privlib}/IO/Uncompress/Unzip.pm
rm -rf %{buildroot}%{privlib}/IO/Uncompress/Adapter
rm -rf %{buildroot}%{privlib}/IO/Uncompress
rm %{buildroot}%{_mandir}/man3/IO::Compress::Deflate*
rm %{buildroot}%{_mandir}/man3/IO::Compress::Bzip2*
rm %{buildroot}%{_mandir}/man3/IO::Compress::Gzip*
rm %{buildroot}%{_mandir}/man3/IO::Compress::RawDeflate*
rm %{buildroot}%{_mandir}/man3/IO::Compress::Zip*
rm %{buildroot}%{_mandir}/man3/IO::Uncompress::AnyInflate*
rm %{buildroot}%{_mandir}/man3/IO::Uncompress::Bunzip2*
rm %{buildroot}%{_mandir}/man3/IO::Uncompress::Gunzip*
rm %{buildroot}%{_mandir}/man3/IO::Uncompress::Inflate*
rm %{buildroot}%{_mandir}/man3/IO::Uncompress::RawInflate*
rm %{buildroot}%{_mandir}/man3/IO::Uncompress::Unzip*

# IO-Socket-IP
rm %{buildroot}%{privlib}/IO/Socket/IP.pm
rm -rf %{buildroot}%{privlib}/IO/Socket
rm %{buildroot}%{_mandir}/man3/IO::Socket::IP.*

# IO-Zlib
rm %{buildroot}%{privlib}/IO/Zlib.pm
rm -rf %{buildroot}%{privlib}/IO
rm %{buildroot}%{_mandir}/man3/IO::Zlib.*

# HTTP-Tiny
rm %{buildroot}%{privlib}/HTTP/Tiny.pm
rm -rf %{buildroot}%{privlib}/HTTP
rm %{buildroot}%{_mandir}/man3/HTTP::Tiny*

# IPC-Cmd
rm %{buildroot}%{privlib}/IPC/Cmd.pm
rm %{buildroot}%{_mandir}/man3/IPC::Cmd.3*

# IPC-SysV
rm -rf %{buildroot}%{archlib}/auto/IPC
rm %{buildroot}%{archlib}/IPC/Msg.pm
rm %{buildroot}%{archlib}/IPC/Semaphore.pm
rm %{buildroot}%{archlib}/IPC/SharedMem.pm
rm %{buildroot}%{archlib}/IPC/SysV.pm
rm -rf %{buildroot}%{archlib}/IPC
rm %{buildroot}%{_mandir}/man3/IPC::Msg.*
rm %{buildroot}%{_mandir}/man3/IPC::Semaphore.*
rm %{buildroot}%{_mandir}/man3/IPC::SharedMem.*
rm %{buildroot}%{_mandir}/man3/IPC::SysV.*

# JSON-PP
rm %{buildroot}%{_bindir}/json_pp
rm %{buildroot}%{privlib}/JSON/PP.pm
rm -rf %{buildroot}%{privlib}/JSON/PP
rm -rf %{buildroot}%{privlib}/JSON
rm %{buildroot}%{_mandir}/man1/json_pp.1*
rm %{buildroot}%{_mandir}/man3/JSON::PP.3*
rm %{buildroot}%{_mandir}/man3/JSON::PP::Boolean.3pm*

# libnet
rm %{buildroot}%{privlib}/Net/Cmd.pm
rm %{buildroot}%{privlib}/Net/Config.pm
rm %{buildroot}%{privlib}/Net/Domain.pm
rm %{buildroot}%{privlib}/Net/FTP.pm
rm -rf %{buildroot}%{privlib}/Net/FTP
rm %{buildroot}%{privlib}/Net/libnetFAQ.pod
rm %{buildroot}%{privlib}/Net/NNTP.pm
rm %{buildroot}%{privlib}/Net/Netrc.pm
rm %{buildroot}%{privlib}/Net/POP3.pm
rm %{buildroot}%{privlib}/Net/SMTP.pm
rm %{buildroot}%{privlib}/Net/Time.pm
rm %{buildroot}%{_mandir}/man3/Net::Cmd.*
rm %{buildroot}%{_mandir}/man3/Net::Config.*
rm %{buildroot}%{_mandir}/man3/Net::Domain.*
rm %{buildroot}%{_mandir}/man3/Net::FTP.*
rm %{buildroot}%{_mandir}/man3/Net::libnetFAQ.*
rm %{buildroot}%{_mandir}/man3/Net::NNTP.*
rm %{buildroot}%{_mandir}/man3/Net::Netrc.*
rm %{buildroot}%{_mandir}/man3/Net::POP3.*
rm %{buildroot}%{_mandir}/man3/Net::SMTP.*
rm %{buildroot}%{_mandir}/man3/Net::Time.*

# Locale-Maketext
rm %{buildroot}%{privlib}/Locale/Maketext.*
rm %{buildroot}%{privlib}/Locale/Maketext/Cookbook.*
rm %{buildroot}%{privlib}/Locale/Maketext/Guts.*
rm %{buildroot}%{privlib}/Locale/Maketext/GutsLoader.*
rm %{buildroot}%{privlib}/Locale/Maketext/TPJ13.*
rm %{buildroot}%{_mandir}/man3/Locale::Maketext.*
rm %{buildroot}%{_mandir}/man3/Locale::Maketext::Cookbook.*
rm %{buildroot}%{_mandir}/man3/Locale::Maketext::Guts.*
rm %{buildroot}%{_mandir}/man3/Locale::Maketext::GutsLoader.*
rm %{buildroot}%{_mandir}/man3/Locale::Maketext::TPJ13.*

# Math-BigInt
rm %{buildroot}%{privlib}/Math/BigFloat.pm
rm %{buildroot}%{privlib}/Math/BigInt.pm
rm %{buildroot}%{privlib}/Math/BigInt/Calc.pm
rm %{buildroot}%{privlib}/Math/BigInt/Lib.pm
rm -rf %{buildroot}%{privlib}/Math/BigInt
rm %{buildroot}%{_mandir}/man3/Math::BigFloat.*
rm %{buildroot}%{_mandir}/man3/Math::BigInt.*
rm %{buildroot}%{_mandir}/man3/Math::BigInt::Calc.*
rm %{buildroot}%{_mandir}/man3/Math::BigInt::Lib.*

# Math-BigInt-FastCalc
rm -rf %{buildroot}%{archlib}/Math
rm -rf %{buildroot}%{archlib}/auto/Math
rm %{buildroot}%{_mandir}/man3/Math::BigInt::FastCalc.*

# Math-BigRat
rm %{buildroot}%{privlib}/Math/BigRat.pm
rm %{buildroot}%{_mandir}/man3/Math::BigRat.*

# MIME-Base64
rm -rf %{buildroot}%{archlib}/auto/MIME
rm -rf %{buildroot}%{archlib}/MIME
rm %{buildroot}%{_mandir}/man3/MIME::*

# Module-CoreList
rm -rf %{buildroot}%{privlib}/Module/CoreList
rm %{buildroot}%{privlib}/Module/CoreList.pm
rm %{buildroot}%{privlib}/Module/CoreList.pod
rm %{buildroot}%{_mandir}/man3/Module::CoreList*

# Module-CoreList-tools
rm %{buildroot}%{_bindir}/corelist
rm %{buildroot}%{_mandir}/man1/corelist*

# Module-Load
rm %{buildroot}%{privlib}/Module/Load.pm
rm %{buildroot}%{_mandir}/man3/Module::Load.*

# Module-Load-Conditional
rm -rf %{buildroot}%{privlib}/Module/Load
rm %{buildroot}%{_mandir}/man3/Module::Load::Conditional*

# Module-Metadata
rm %{buildroot}%{privlib}/Module/Metadata.pm
rm %{buildroot}%{_mandir}/man3/Module::Metadata.3pm*

# Net-Ping
rm %{buildroot}%{privlib}/Net/Ping.pm
rm %{buildroot}%{_mandir}/man3/Net::Ping.*

# parent
rm %{buildroot}%{privlib}/parent.pm
rm %{buildroot}%{_mandir}/man3/parent.3*

# Params-Check
rm -rf %{buildroot}%{privlib}/Params/
rm %{buildroot}%{_mandir}/man3/Params::Check*

# PathTools
rm %{buildroot}%{archlib}/Cwd.pm
rm -rf %{buildroot}%{archlib}/File/Spec*
rm -rf %{buildroot}%{archlib}/auto/Cwd/
rm %{buildroot}%{_mandir}/man3/Cwd*
rm %{buildroot}%{_mandir}/man3/File::Spec*

# Perl-OSType
rm %{buildroot}%{privlib}/Perl/OSType.pm
rm -rf %{buildroot}%{privlib}/Perl
rm %{buildroot}%{_mandir}/man3/Perl::OSType.3pm*

# perlfaq
rm %{buildroot}%{privlib}/perlfaq.pm
rm %{buildroot}%{privlib}/pod/perlfaq*
rm %{buildroot}%{privlib}/pod/perlglossary.pod
rm %{buildroot}%{_mandir}/man1/perlfaq*
rm %{buildroot}%{_mandir}/man1/perlglossary.*

# PerlIO-via-QuotedPrint
rm -rf %{buildroot}%{privlib}/PerlIO
rm %{buildroot}%{_mandir}/man3/PerlIO::via::QuotedPrint.*

# Pod-Checker
rm %{buildroot}%{_bindir}/podchecker
rm %{buildroot}%{privlib}/Pod/Checker.pm
rm %{buildroot}%{_mandir}/man1/podchecker.*
rm %{buildroot}%{_mandir}/man3/Pod::Checker.*

# Pod-Escapes
rm %{buildroot}%{privlib}/Pod/Escapes.pm
rm %{buildroot}%{_mandir}/man3/Pod::Escapes.*

# Pod-Perldoc
rm %{buildroot}%{_bindir}/perldoc
rm %{buildroot}%{privlib}/pod/perldoc.pod
rm %{buildroot}%{privlib}/Pod/Perldoc.pm
rm -rf %{buildroot}%{privlib}/Pod/Perldoc/
rm %{buildroot}%{_mandir}/man1/perldoc.1*
rm %{buildroot}%{_mandir}/man3/Pod::Perldoc*

# Pod-Usage
rm %{buildroot}%{_bindir}/pod2usage
rm %{buildroot}%{privlib}/Pod/Usage.pm
rm %{buildroot}%{_mandir}/man1/pod2usage.*
rm %{buildroot}%{_mandir}/man3/Pod::Usage.*

# podlators
rm %{buildroot}%{_bindir}/pod2man
rm %{buildroot}%{_bindir}/pod2text
rm %{buildroot}%{privlib}/pod/perlpodstyle.pod
rm %{buildroot}%{privlib}/Pod/Man.pm
rm %{buildroot}%{privlib}/Pod/ParseLink.pm
rm %{buildroot}%{privlib}/Pod/Text.pm
rm -rf %{buildroot}%{privlib}/Pod/Text
rm %{buildroot}%{_mandir}/man1/pod2man.1*
rm %{buildroot}%{_mandir}/man1/pod2text.1*
rm %{buildroot}%{_mandir}/man1/perlpodstyle.1*
rm %{buildroot}%{_mandir}/man3/Pod::Man*
rm %{buildroot}%{_mandir}/man3/Pod::ParseLink*
rm %{buildroot}%{_mandir}/man3/Pod::Text*

# Pod-Simple
rm %{buildroot}%{privlib}/Pod/Simple.pm
rm %{buildroot}%{privlib}/Pod/Simple.pod
rm -rf %{buildroot}%{privlib}/Pod/Simple/
rm %{buildroot}%{_mandir}/man3/Pod::Simple*

# Scalar-List-Utils
rm -rf %{buildroot}%{archlib}/List/
rm -rf %{buildroot}%{archlib}/Scalar/
rm -rf %{buildroot}%{archlib}/Sub/
rm -rf %{buildroot}%{archlib}/auto/List/
rm %{buildroot}%{_mandir}/man3/List::Util*
rm %{buildroot}%{_mandir}/man3/Scalar::Util*
rm %{buildroot}%{_mandir}/man3/Sub::Util*

# Socket
rm %{buildroot}%{archlib}/auto/Socket/Socket.*
rm -rf %{buildroot}%{archlib}/auto/Socket
rm %{buildroot}%{archlib}/Socket.pm
rm %{buildroot}%{_mandir}/man3/Socket.3*

# Storable
rm %{buildroot}%{archlib}/Storable.pm
rm -rf %{buildroot}%{archlib}/auto/Storable/
rm %{buildroot}%{_mandir}/man3/Storable.*

# Sys-Syslog
# %%dir %%{archlib}/Sys not excluded. It would be removed from the previous package.
rm %{buildroot}%{archlib}/Sys/Syslog.pm
# %%dir %%{archlib}/auto/Sys not excluded. It would be removed from the previous package.
rm -rf %{buildroot}%{archlib}/auto/Sys/Syslog/
rm %{buildroot}%{_mandir}/man3/Sys::Syslog.*

# Term-ANSIColor
rm %{buildroot}%{privlib}/Term/ANSIColor.pm
rm %{buildroot}%{_mandir}/man3/Term::ANSIColor*

# Term-Cap
rm %{buildroot}%{privlib}/Term/Cap.pm
rm %{buildroot}%{_mandir}/man3/Term::Cap.*

# Test-Harness
rm %{buildroot}%{_bindir}/prove
rm -rf %{buildroot}%{privlib}/App/Prove*
rm -rf %{buildroot}%{privlib}/App
rm -rf %{buildroot}%{privlib}/TAP*
rm %{buildroot}%{privlib}/Test/Harness*
rm %{buildroot}%{_mandir}/man1/prove.1*
rm %{buildroot}%{_mandir}/man3/App::Prove*
rm %{buildroot}%{_mandir}/man3/TAP*
rm %{buildroot}%{_mandir}/man3/Test::Harness*

# Test-Simple
rm %{buildroot}%{privlib}/ok*
rm %{buildroot}%{privlib}/Test/More*
rm -rf %{buildroot}%{privlib}/Test/Builder*
rm -rf %{buildroot}%{privlib}/Test/Tester*
rm %{buildroot}%{privlib}/Test/Simple*
rm %{buildroot}%{privlib}/Test/Tutorial*
rm -rf %{buildroot}%{privlib}/Test/use
rm -rf %{buildroot}%{privlib}/Test
rm -rf %{buildroot}%{privlib}/Test2*
rm %{buildroot}%{_mandir}/man3/ok*
rm %{buildroot}%{_mandir}/man3/Test::More*
rm %{buildroot}%{_mandir}/man3/Test::Builder*
rm %{buildroot}%{_mandir}/man3/Test::Tester*
rm %{buildroot}%{_mandir}/man3/Test::Simple*
rm %{buildroot}%{_mandir}/man3/Test::Tutorial*
rm %{buildroot}%{_mandir}/man3/Test::use::*
rm %{buildroot}%{_mandir}/man3/Test2*

# Text-Balanced
rm %{buildroot}%{privlib}/Text/Balanced.pm
rm %{buildroot}%{_mandir}/man3/Text::Balanced.*

# Text-ParseWords
rm %{buildroot}%{privlib}/Text/ParseWords.pm
rm %{buildroot}%{_mandir}/man3/Text::ParseWords.*

# Text-Tabs+Wrap
rm %{buildroot}%{privlib}/Text/Tabs.pm
rm %{buildroot}%{privlib}/Text/Wrap.pm
rm %{buildroot}%{_mandir}/man3/Text::Tabs.*
rm %{buildroot}%{_mandir}/man3/Text::Wrap.*

# Thread-Queue
rm %{buildroot}%{privlib}/Thread/Queue.pm
rm %{buildroot}%{_mandir}/man3/Thread::Queue.*

# Tie-RefHash
rm %{buildroot}%{privlib}/Tie/RefHash.pm
rm %{buildroot}%{_mandir}/man3/Tie::RefHash.*

# Time-HiRes
rm %{buildroot}%{archlib}/Time/HiRes.pm
rm -rf %{buildroot}%{archlib}/auto/Time/HiRes
rm %{buildroot}%{_mandir}/man3/Time::HiRes.*

# Time-Local
rm %{buildroot}%{privlib}/Time/Local.pm
rm %{buildroot}%{_mandir}/man3/Time::Local.*

# threads
rm %{buildroot}%{archlib}/auto/threads/threads*
rm %{buildroot}%{archlib}/threads.pm
rm %{buildroot}%{_mandir}/man3/threads.3*

# threads-shared
rm -rf %{buildroot}%{archlib}/auto/threads/shared*
rm -rf %{buildroot}%{archlib}/auto/threads
rm %{buildroot}%{archlib}/threads/shared*
rm -rf %{buildroot}%{archlib}/threads
rm %{buildroot}%{_mandir}/man3/threads::shared*

# Unicode-Collate
rm -rf %{buildroot}%{archlib}/auto/Unicode/Collate
rm -rf %{buildroot}%{archlib}/auto/Unicode
rm %{buildroot}%{archlib}/Unicode/Collate.pm
rm -rf %{buildroot}%{archlib}/Unicode/Collate
rm -rf %{buildroot}%{privlib}/Unicode/Collate
rm %{buildroot}%{_mandir}/man3/Unicode::Collate.*
rm %{buildroot}%{_mandir}/man3/Unicode::Collate::*

# Unicode-Normalize
rm -rf %{buildroot}%{archlib}/auto/Unicode/Normalize
rm %{buildroot}%{archlib}/Unicode/Normalize.pm
rm -rf %{buildroot}%{archlib}/Unicode
rm %{buildroot}%{_mandir}/man3/Unicode::Normalize.*

# version
rm %{buildroot}%{privlib}/version.pm
rm %{buildroot}%{privlib}/version.pod
rm -rf %{buildroot}%{privlib}/version/
rm %{buildroot}%{_mandir}/man3/version.3*
rm %{buildroot}%{_mandir}/man3/version::Internals.3*
%endif


# TODO: Canonicalize test files (rewrite intrerpreter path, fix permissions)
# XXX: We cannot rewrite ./perl before %%check phase. Otherwise the test
# would run against system perl at build-time.
# See __spec_check_pre global macro in macros.perl.
#T_FILES=`find %%{buildroot}%%{perl5_testdir} -type f -name '*.t'`
#%%fix_shbang_line $T_FILES
#%%{__chmod} +x $T_FILES
#%%{_fixperms} %%{buildroot}%%{perl5_testdir}
#
# lib/perl5db.t will fail if Term::ReadLine::Gnu is available
%check
%if %{with test}
%{new_perl} -I/lib regen/lib_cleanup.pl
pushd t
%{new_perl} -I../lib porting/customized.t --regen
popd
%if %{parallel_tests}
    JOBS=$(printf '%%s' "%{?_smp_mflags}" | sed 's/.*-j\([0-9][0-9]*\).*/\1/')
    LC_ALL=C TEST_JOBS=$JOBS make test_harness
%else
    LC_ALL=C make test
%endif
%endif

%ldconfig_scriptlets libs

%files
# Main perl package is an empty meta package.

%files interpreter
%{_bindir}/perl
%{_bindir}/perl%{perl_version}
%{_mandir}/man1/perl.1*
%{_mandir}/man1/perlrun.1*
%dir %{privlib}/pod
%{privlib}/pod/perl.pod
%{privlib}/pod/perlrun.pod

%files libs
%license Artistic Copying
%doc AUTHORS README Changes
%dir %{archlib}
%{archlib}/attributes.pm
%dir %{archlib}/auto
%dir %{archlib}/auto/attributes
%{archlib}/auto/attributes/attributes.so
%dir %{archlib}/auto/File
%dir %{archlib}/auto/File/Glob
%{archlib}/auto/File/Glob/Glob.so
%{archlib}/auto/PerlIO
%{archlib}/auto/re
%{archlib}/auto/SDBM_File
%{archlib}/Config.*
%{archlib}/Config_git.pl
%{archlib}/Config_heavy.pl
%dir %{archlib}/CORE
%{archlib}/CORE/libperl.so
%dir %{archlib}/File
%{archlib}/File/Glob.pm
%{archlib}/PerlIO
%{archlib}/re.pm
%{archlib}/SDBM_File.pm
%{_libdir}/libperl.so.*
%dir %{perl_vendorarch}
%dir %{perl_vendorarch}/auto
%dir %{privlib}
%{privlib}/AnyDBM_File.pm
%{privlib}/bytes.pm
%{privlib}/bytes_heavy.pl
%{privlib}/_charnames.pm
%{privlib}/charnames.pm
%{privlib}/CORE.pod
%{privlib}/feature.pm
%{privlib}/integer.pm
%{privlib}/Internals.pod
%{privlib}/PerlIO.pm
%{privlib}/strict.pm
%{privlib}/unicore
%{privlib}/UNIVERSAL.pm
%{privlib}/utf8.pm
%{privlib}/warnings
%{privlib}/warnings.pm
%dir %{privlib}/Tie
%{privlib}/Tie/Hash.pm
%dir %{privlib}/Tie/Hash
%{privlib}/Tie/Hash/NamedCapture.pm
%{privlib}/XSLoader.pm
%dir %{perl_vendorlib}
%{_mandir}/man3/AnyDBM_File.*
%{_mandir}/man3/attributes.*
%{_mandir}/man3/bytes.*
%{_mandir}/man3/charnames.*
%{_mandir}/man3/Config.*
%{_mandir}/man3/CORE.*
%{_mandir}/man3/feature.3*
%{_mandir}/man3/File::Glob.*
%{_mandir}/man3/integer.*
%{_mandir}/man3/Internals.*
%{_mandir}/man3/PerlIO.*
%{_mandir}/man3/PerlIO::encoding.*
%{_mandir}/man3/PerlIO::mmap.*
%{_mandir}/man3/PerlIO::scalar.*
%{_mandir}/man3/PerlIO::via.*
%{_mandir}/man3/re.*
%{_mandir}/man3/SDBM_File.3*
%{_mandir}/man3/strict.*
%{_mandir}/man3/Tie::Hash.*
%{_mandir}/man3/Tie::Hash::*
%{_mandir}/man3/utf8.*
%{_mandir}/man3/warnings.*
%{_mandir}/man3/warnings::*
%{_mandir}/man3/UNIVERSAL.*
%{_mandir}/man3/XSLoader.*

%files devel
%{_bindir}/h2xs
%{_mandir}/man1/h2xs*
%{_bindir}/perlivp
%{_mandir}/man1/perlivp*
%{archlib}/CORE/*.h
%dir %{privlib}/ExtUtils
%{privlib}/ExtUtils/typemap
%{_libdir}/libperl.so
%if %{with perl_enables_systemtap}
%dir %{_datadir}/systemtap
%dir %{_datadir}/systemtap/tapset
%{tapsetdir}/%{libperl_stp}
%doc perl-example.stp
%endif

%files macros
%{_rpmmacrodir}/macros.perl

%files tests
%{perl5_testdir}/

%files utils
%{_bindir}/h2ph
%{_bindir}/perlbug
%{_bindir}/perlthanks
%{_bindir}/pl2pm
%dir %{privlib}/pod
%{privlib}/pod/perlutil.pod
%{_mandir}/man1/h2ph.*
%{_mandir}/man1/perlbug.*
%{_mandir}/man1/perlthanks.*
%{_mandir}/man1/perlutil.*
%{_mandir}/man1/pl2pm.*

%if %{dual_life} || %{rebuild_from_scratch}
%files Archive-Tar
%{_bindir}/ptar
%{_bindir}/ptardiff
%{_bindir}/ptargrep
%dir %{privlib}/Archive
%{privlib}/Archive/Tar 
%{privlib}/Archive/Tar.pm
%{_mandir}/man1/ptar.1*
%{_mandir}/man1/ptardiff.1*
%{_mandir}/man1/ptargrep.1*
%{_mandir}/man3/Archive::Tar* 
%endif

%files Attribute-Handlers
%{privlib}/Attribute
%{_mandir}/man3/Attribute::Handlers.*

%if %{dual_life} || %{rebuild_from_scratch}
%files autodie
%{privlib}/autodie/
%{privlib}/autodie.pm
%{privlib}/Fatal.pm
%{_mandir}/man3/autodie.3*
%{_mandir}/man3/autodie::*
%{_mandir}/man3/Fatal.3*
%endif

%files AutoLoader
%{privlib}/AutoLoader.pm
%{_mandir}/man3/AutoLoader.3*

%files AutoSplit
%{privlib}/AutoSplit.pm
%{_mandir}/man3/AutoSplit.3*

%files autouse
%{privlib}/autouse.pm
%{_mandir}/man3/autouse.3*

%files B
%{archlib}/auto/B
%{archlib}/B
%{archlib}/B.pm
%{archlib}/O.pm
%{privlib}/B
%{_mandir}/man3/B.*
%{_mandir}/man3/B::*
%{_mandir}/man3/O.*

%files base
%{privlib}/base.pm
%{_mandir}/man3/base.3*

%files Benchmark
%{privlib}/Benchmark.pm
%{_mandir}/man3/Benchmark.*

%if %{dual_life} || %{rebuild_from_scratch}
%files bignum
%{privlib}/bigint.pm
%{privlib}/bignum.pm
%{privlib}/bigrat.pm
%dir %{privlib}/Math
%{privlib}/Math/BigFloat
%dir %{privlib}/Math/BigInt
%{privlib}/Math/BigInt/Trace.pm
%{_mandir}/man3/bigint.*
%{_mandir}/man3/bignum.*
%{_mandir}/man3/bigrat.*
%endif

%files blib
%{privlib}/blib.pm
%{_mandir}/man3/blib.*

%if %{dual_life} || %{rebuild_from_scratch}
%files Carp
%{privlib}/Carp
%{privlib}/Carp.*
%{_mandir}/man3/Carp.*
%endif

%files Class-Struct
%{privlib}/Class
%{_mandir}/man3/Class::Struct.*

%if %{dual_life} || %{rebuild_from_scratch}
%files Compress-Raw-Bzip2
%dir %{archlib}/Compress
%dir %{archlib}/Compress/Raw
%{archlib}/Compress/Raw/Bzip2.pm
%dir %{archlib}/auto/Compress
%dir %{archlib}/auto/Compress/Raw
%{archlib}/auto/Compress/Raw/Bzip2
%{_mandir}/man3/Compress::Raw::Bzip2*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Compress-Raw-Zlib
%dir %{archlib}/Compress
%dir %{archlib}/Compress/Raw
%{archlib}/Compress/Raw/Zlib.pm
%dir %{archlib}/auto/Compress
%dir %{archlib}/auto/Compress/Raw
%{archlib}/auto/Compress/Raw/Zlib
%{_mandir}/man3/Compress::Raw::Zlib*
%endif

%files Config-Extensions
%dir %{privlib}/Config
%{privlib}/Config/Extensions.pm
%{_mandir}/man3/Config::Extensions.*

%if %{dual_life} || %{rebuild_from_scratch}
%files Config-Perl-V
%dir %{privlib}/Config
%{privlib}/Config/Perl
%{_mandir}/man3/Config::Perl::V.*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files constant
%{privlib}/constant.pm
%{_mandir}/man3/constant.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files CPAN
%{_bindir}/cpan
%dir %{privlib}/App
%{privlib}/App/Cpan.pm
%{privlib}/CPAN
%{privlib}/CPAN.pm
%{_mandir}/man1/cpan.1*
%{_mandir}/man3/App::Cpan.*
%{_mandir}/man3/CPAN.*
%{_mandir}/man3/CPAN:*
%exclude %{privlib}/CPAN/Meta/
%exclude %{privlib}/CPAN/Meta.pm
%exclude %{_mandir}/man3/CPAN::Meta*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files CPAN-Meta
%dir %{privlib}/CPAN/Meta
%{privlib}/CPAN/Meta.pm
%{privlib}/CPAN/Meta/Converter.pm
%{privlib}/CPAN/Meta/Feature.pm
%dir %{privlib}/CPAN/Meta/History
%{privlib}/CPAN/Meta/History/Meta*
%{privlib}/CPAN/Meta/History.pm
%{privlib}/CPAN/Meta/Merge.pm
%{privlib}/CPAN/Meta/Prereqs.pm
%{privlib}/CPAN/Meta/Spec.pm
%{privlib}/CPAN/Meta/Validator.pm
%dir %{privlib}/Parse/
%dir %{privlib}/Parse/CPAN/
%{privlib}/Parse/CPAN/Meta.pm
%{_mandir}/man3/CPAN::Meta*
%{_mandir}/man3/Parse::CPAN::Meta.3*
%exclude %{_mandir}/man3/CPAN::Meta::YAML*
%exclude %{_mandir}/man3/CPAN::Meta::Requirements*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files CPAN-Meta-Requirements
%dir %{privlib}/CPAN
%dir %{privlib}/CPAN/Meta
%{privlib}/CPAN/Meta/Requirements.pm
%{_mandir}/man3/CPAN::Meta::Requirements.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files CPAN-Meta-YAML
%dir %{privlib}/CPAN
%dir %{privlib}/CPAN/Meta
%{privlib}/CPAN/Meta/YAML.pm
%{_mandir}/man3/CPAN::Meta::YAML*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Data-Dumper
%dir %{archlib}/auto/Data
%dir %{archlib}/auto/Data/Dumper
%{archlib}/auto/Data/Dumper/Dumper.so
%dir %{archlib}/Data
%{archlib}/Data/Dumper.pm
%{_mandir}/man3/Data::Dumper.3*
%endif

%files DBM_Filter
%{privlib}/DBM_Filter
%{privlib}/DBM_Filter.pm
%{_mandir}/man3/DBM_Filter.*
%{_mandir}/man3/DBM_Filter::*

%files debugger
%{privlib}/DB.pm
%{privlib}/dumpvar.pl
%{privlib}/perl5db.pl
%dir %{privlib}/pod
%{privlib}/pod/perldebug.pod
%{_mandir}/man1/perldebug.*
%{_mandir}/man3/DB.*

%files deprecate
%{privlib}/deprecate.pm
%{_mandir}/man3/deprecate.*

%files Devel-Peek
%dir %{archlib}/Devel
%{archlib}/Devel/Peek.pm
%dir %{archlib}/auto/Devel
%{archlib}/auto/Devel/Peek
%{_mandir}/man3/Devel::Peek.*

%if %{dual_life} || %{rebuild_from_scratch}
%files Devel-PPPort
%dir %{archlib}/Devel
%{archlib}/Devel/PPPort.pm
%{_mandir}/man3/Devel::PPPort.3*
%endif

%files Devel-SelfStubber
%dir %{privlib}/Devel
%{privlib}/Devel/SelfStubber.pm
%{_mandir}/man3/Devel::SelfStubber.*

%files diagnostics
%{_bindir}/splain
%{privlib}/diagnostics.pm
%dir %{privlib}/pod
%{privlib}/pod/perldiag.pod
%{_mandir}/man1/perldiag.*
%{_mandir}/man1/splain.*
%{_mandir}/man3/diagnostics.*

%if %{dual_life} || %{rebuild_from_scratch}
%files Digest
%{privlib}/Digest.pm
%dir %{privlib}/Digest
%{privlib}/Digest/base.pm
%{privlib}/Digest/file.pm
%{_mandir}/man3/Digest.3*
%{_mandir}/man3/Digest::base.3*
%{_mandir}/man3/Digest::file.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Digest-MD5
%dir %{archlib}/Digest
%{archlib}/Digest/MD5.pm
%dir %{archlib}/auto/Digest
%{archlib}/auto/Digest/MD5
%{_mandir}/man3/Digest::MD5.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Digest-SHA
%{_bindir}/shasum
%dir %{archlib}/Digest
%{archlib}/Digest/SHA.pm
%dir %{archlib}/auto/Digest
%{archlib}/auto/Digest/SHA
%{_mandir}/man1/shasum.1*
%{_mandir}/man3/Digest::SHA.3*
%endif

%files DirHandle
%{privlib}/DirHandle.pm
%{_mandir}/man3/DirHandle.3*

%files doc
%dir %{privlib}/pod
%{privlib}/pod/perl5*delta.pod
%{privlib}/pod/perlaix.pod
%{privlib}/pod/perlamiga.pod
%{privlib}/pod/perlandroid.pod
%{privlib}/pod/perlapi.pod
%{privlib}/pod/perlapio.pod
%{privlib}/pod/perlartistic.pod
%{privlib}/pod/perlbook.pod
%{privlib}/pod/perlboot.pod
%{privlib}/pod/perlbot.pod
%{privlib}/pod/perlbs2000.pod
%{privlib}/pod/perlcall.pod
%{privlib}/pod/perlcheat.pod
%{privlib}/pod/perlclib.pod
%{privlib}/pod/perlcn.pod
%{privlib}/pod/perlcommunity.pod
%{privlib}/pod/perlcygwin.pod
%{privlib}/pod/perldata.pod
%{privlib}/pod/perldbmfilter.pod
%{privlib}/pod/perldebguts.pod
%{privlib}/pod/perldebtut.pod
%{privlib}/pod/perldelta.pod
%{privlib}/pod/perldeprecation.pod
%{privlib}/pod/perldocstyle.pod
%{privlib}/pod/perldos.pod
%{privlib}/pod/perldsc.pod
%{privlib}/pod/perldtrace.pod
%{privlib}/pod/perlebcdic.pod
%{privlib}/pod/perlembed.pod
%{privlib}/pod/perlexperiment.pod
%{privlib}/pod/perlfork.pod
%{privlib}/pod/perlform.pod
%{privlib}/pod/perlfreebsd.pod
%{privlib}/pod/perlfunc.pod
%{privlib}/pod/perlgit.pod
%{privlib}/pod/perlgov.pod
%{privlib}/pod/perlgpl.pod
%{privlib}/pod/perlguts.pod
%{privlib}/pod/perlhack.pod
%{privlib}/pod/perlhacktips.pod
%{privlib}/pod/perlhacktut.pod
%{privlib}/pod/perlhaiku.pod
%{privlib}/pod/perlhist.pod
%{privlib}/pod/perlhpux.pod
%{privlib}/pod/perlhurd.pod
%{privlib}/pod/perlintern.pod
%{privlib}/pod/perlinterp.pod
%{privlib}/pod/perlintro.pod
%{privlib}/pod/perliol.pod
%{privlib}/pod/perlipc.pod
%{privlib}/pod/perlirix.pod
%{privlib}/pod/perljp.pod
%{privlib}/pod/perlko.pod
%{privlib}/pod/perllexwarn.pod
%{privlib}/pod/perllinux.pod
%{privlib}/pod/perllocale.pod
%{privlib}/pod/perllol.pod
%{privlib}/pod/perlmacos.pod
%{privlib}/pod/perlmacosx.pod
%{privlib}/pod/perlmod.pod
%{privlib}/pod/perlmodinstall.pod
%{privlib}/pod/perlmodlib.pod
%{privlib}/pod/perlmodstyle.pod
%{privlib}/pod/perlmroapi.pod
%{privlib}/pod/perlnetware.pod
%{privlib}/pod/perlnewmod.pod
%{privlib}/pod/perlnumber.pod
%{privlib}/pod/perlobj.pod
%{privlib}/pod/perlootut.pod
%{privlib}/pod/perlop.pod
%{privlib}/pod/perlopenbsd.pod
%{privlib}/pod/perlopentut.pod
%{privlib}/pod/perlos2.pod
%{privlib}/pod/perlos390.pod
%{privlib}/pod/perlos400.pod
%{privlib}/pod/perlpacktut.pod
%{privlib}/pod/perlperf.pod
%{privlib}/pod/perlplan9.pod
%{privlib}/pod/perlpod.pod
%{privlib}/pod/perlpodspec.pod
%{privlib}/pod/perlpolicy.pod
%{privlib}/pod/perlport.pod
%{privlib}/pod/perlpragma.pod
%{privlib}/pod/perlqnx.pod
%{privlib}/pod/perlre.pod
%{privlib}/pod/perlreapi.pod
%{privlib}/pod/perlrebackslash.pod
%{privlib}/pod/perlrecharclass.pod
%{privlib}/pod/perlref.pod
%{privlib}/pod/perlreftut.pod
%{privlib}/pod/perlreguts.pod
%{privlib}/pod/perlrepository.pod
%{privlib}/pod/perlrequick.pod
%{privlib}/pod/perlreref.pod
%{privlib}/pod/perlretut.pod
%{privlib}/pod/perlriscos.pod
%{privlib}/pod/perlsec.pod
%{privlib}/pod/perlsecpolicy.pod
%{privlib}/pod/perlsolaris.pod
%{privlib}/pod/perlsource.pod
%{privlib}/pod/perlstyle.pod
%{privlib}/pod/perlsub.pod
%{privlib}/pod/perlsyn.pod
%{privlib}/pod/perlsynology.pod
%{privlib}/pod/perlthrtut.pod
%{privlib}/pod/perltie.pod
%{privlib}/pod/perltoc.pod
%{privlib}/pod/perltodo.pod
%{privlib}/pod/perltooc.pod
%{privlib}/pod/perltoot.pod
%{privlib}/pod/perltrap.pod
%{privlib}/pod/perltru64.pod
%{privlib}/pod/perltw.pod
%{privlib}/pod/perlunicode.pod
%{privlib}/pod/perlunicook.pod
%{privlib}/pod/perlunifaq.pod
%{privlib}/pod/perluniintro.pod
%{privlib}/pod/perluniprops.pod
%{privlib}/pod/perlunitut.pod
%{privlib}/pod/perlvar.pod
%{privlib}/pod/perlvms.pod
%{privlib}/pod/perlvos.pod
%{privlib}/pod/perlwin32.pod
%{_mandir}/man1/perl5*delta.*
%{_mandir}/man1/perlaix.*
%{_mandir}/man1/perlamiga.*
%{_mandir}/man1/perlandroid.*
%{_mandir}/man1/perlapi.*
%{_mandir}/man1/perlapio.*
%{_mandir}/man1/perlartistic.*
%{_mandir}/man1/perlbook.*
%{_mandir}/man1/perlboot.*
%{_mandir}/man1/perlbot.*
%{_mandir}/man1/perlbs2000.*
%{_mandir}/man1/perlcall.*
%{_mandir}/man1/perlcheat.*
%{_mandir}/man1/perlclib.*
%{_mandir}/man1/perlcn.*
%{_mandir}/man1/perlcommunity.*
%{_mandir}/man1/perlcygwin.*
%{_mandir}/man1/perldata.*
%{_mandir}/man1/perldbmfilter.*
%{_mandir}/man1/perldebguts.*
%{_mandir}/man1/perldebtut.*
%{_mandir}/man1/perldelta.*
%{_mandir}/man1/perldeprecation.*
%{_mandir}/man1/perldocstyle.*
%{_mandir}/man1/perldos.*
%{_mandir}/man1/perldsc.*
%{_mandir}/man1/perldtrace.*
%{_mandir}/man1/perlebcdic.*
%{_mandir}/man1/perlembed.*
%{_mandir}/man1/perlexperiment.*
%{_mandir}/man1/perlfork.*
%{_mandir}/man1/perlform.*
%{_mandir}/man1/perlfreebsd.*
%{_mandir}/man1/perlfunc.*
%{_mandir}/man1/perlgit.*
%{_mandir}/man1/perlgov.*
%{_mandir}/man1/perlgpl.*
%{_mandir}/man1/perlguts.*
%{_mandir}/man1/perlhack.*
%{_mandir}/man1/perlhacktips.*
%{_mandir}/man1/perlhacktut.*
%{_mandir}/man1/perlhaiku.*
%{_mandir}/man1/perlhist.*
%{_mandir}/man1/perlhpux.*
%{_mandir}/man1/perlhurd.*
%{_mandir}/man1/perlintern.*
%{_mandir}/man1/perlinterp.*
%{_mandir}/man1/perlintro.*
%{_mandir}/man1/perliol.*
%{_mandir}/man1/perlipc.*
%{_mandir}/man1/perlirix.*
%{_mandir}/man1/perljp.*
%{_mandir}/man1/perlko.*
%{_mandir}/man1/perllexwarn.*
%{_mandir}/man1/perllinux.*
%{_mandir}/man1/perllocale.*
%{_mandir}/man1/perllol.*
%{_mandir}/man1/perlmacos.*
%{_mandir}/man1/perlmacosx.*
%{_mandir}/man1/perlmod.*
%{_mandir}/man1/perlmodinstall.*
%{_mandir}/man1/perlmodlib.*
%{_mandir}/man1/perlmodstyle.*
%{_mandir}/man1/perlmroapi.*
%{_mandir}/man1/perlnetware.*
%{_mandir}/man1/perlnewmod.*
%{_mandir}/man1/perlnumber.*
%{_mandir}/man1/perlobj.*
%{_mandir}/man1/perlootut.*
%{_mandir}/man1/perlop.*
%{_mandir}/man1/perlopenbsd.*
%{_mandir}/man1/perlopentut.*
%{_mandir}/man1/perlos2.*
%{_mandir}/man1/perlos390.*
%{_mandir}/man1/perlos400.*
%{_mandir}/man1/perlpacktut.*
%{_mandir}/man1/perlperf.*
%{_mandir}/man1/perlplan9.*
%{_mandir}/man1/perlpod.*
%{_mandir}/man1/perlpodspec.*
%{_mandir}/man1/perlpolicy.*
%{_mandir}/man1/perlport.*
%{_mandir}/man1/perlpragma.*
%{_mandir}/man1/perlqnx.*
%{_mandir}/man1/perlre.*
%{_mandir}/man1/perlreapi.*
%{_mandir}/man1/perlrebackslash.*
%{_mandir}/man1/perlrecharclass.*
%{_mandir}/man1/perlref.*
%{_mandir}/man1/perlreftut.*
%{_mandir}/man1/perlreguts.*
%{_mandir}/man1/perlrepository.*
%{_mandir}/man1/perlrequick.*
%{_mandir}/man1/perlreref.*
%{_mandir}/man1/perlretut.*
%{_mandir}/man1/perlriscos.*
%{_mandir}/man1/perlsec.*
%{_mandir}/man1/perlsecpolicy.*
%{_mandir}/man1/perlsolaris.*
%{_mandir}/man1/perlsource.*
%{_mandir}/man1/perlstyle.*
%{_mandir}/man1/perlsub.*
%{_mandir}/man1/perlsyn.*
%{_mandir}/man1/perlsynology.*
%{_mandir}/man1/perlthrtut.*
%{_mandir}/man1/perltie.*
%{_mandir}/man1/perltoc.*
%{_mandir}/man1/perltodo.*
%{_mandir}/man1/perltooc.*
%{_mandir}/man1/perltoot.*
%{_mandir}/man1/perltrap.*
%{_mandir}/man1/perltru64.*
%{_mandir}/man1/perltw.*
%{_mandir}/man1/perlunicode.*
%{_mandir}/man1/perlunicook.*
%{_mandir}/man1/perlunifaq.*
%{_mandir}/man1/perluniintro.*
%{_mandir}/man1/perluniprops.*
%{_mandir}/man1/perlunitut.*
%{_mandir}/man1/perlvar.*
%{_mandir}/man1/perlvms.*
%{_mandir}/man1/perlvos.*
%{_mandir}/man1/perlwin32.*

%files Dumpvalue
%{privlib}/Dumpvalue.pm
%{_mandir}/man3/Dumpvalue.3*

%files DynaLoader
%{archlib}/DynaLoader.pm
%{_mandir}/man3/DynaLoader.3*

%if %{dual_life} || %{rebuild_from_scratch}
%files Encode
%{_bindir}/encguess
%{_bindir}/piconv
%{archlib}/Encode*
%{archlib}/auto/Encode*
%{privlib}/Encode
%exclude %{privlib}/Encode/*.e2x
%exclude %{privlib}/Encode/encode.h
%{_mandir}/man1/encguess.1*
%{_mandir}/man1/piconv.1*
%{_mandir}/man3/Encode*.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files encoding
%{archlib}/encoding.pm
%{_mandir}/man3/encoding.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Encode-devel
%{_bindir}/enc2xs
%dir %{privlib}/Encode
%{privlib}/Encode/*.e2x
%{privlib}/Encode/encode.h
%{_mandir}/man1/enc2xs.1*
%endif

%files encoding-warnings
%dir %{privlib}/encoding
%{privlib}/encoding/warnings.pm
%{_mandir}/man3/encoding::warnings.3*

%files English
%{privlib}/English.pm
%{_mandir}/man3/English.3*

%if %{dual_life} || %{rebuild_from_scratch}
%files Env
%{privlib}/Env.pm
%{_mandir}/man3/Env.3*
%endif

%files Errno
%{archlib}/Errno.pm
%{_mandir}/man3/Errno.*

%if %{dual_life} || %{rebuild_from_scratch}
%files Exporter
%{privlib}/Exporter*
%{_mandir}/man3/Exporter*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files experimental
%{privlib}/experimental*
%{_mandir}/man3/experimental*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files ExtUtils-CBuilder
%dir %{privlib}/ExtUtils
%{privlib}/ExtUtils/CBuilder
%{privlib}/ExtUtils/CBuilder.pm
%{_mandir}/man3/ExtUtils::CBuilder*
%endif

%files ExtUtils-Constant
%dir %{privlib}/ExtUtils
%{privlib}/ExtUtils/Constant
%{privlib}/ExtUtils/Constant.pm
%{_mandir}/man3/ExtUtils::Constant::*
%{_mandir}/man3/ExtUtils::Constant.3*

%if %{dual_life} || %{rebuild_from_scratch}
%files ExtUtils-Command
%dir %{privlib}/ExtUtils
%{privlib}/ExtUtils/Command.pm
%{_mandir}/man3/ExtUtils::Command.*
%endif

%files ExtUtils-Embed
%dir %{privlib}/ExtUtils
%{privlib}/ExtUtils/Embed.pm
%{_mandir}/man3/ExtUtils::Embed*

%if %{dual_life} || %{rebuild_from_scratch}
%files ExtUtils-Install
%dir %{privlib}/ExtUtils
%{privlib}/ExtUtils/Install.pm
%{privlib}/ExtUtils/Installed.pm
%{privlib}/ExtUtils/Packlist.pm
%{_mandir}/man3/ExtUtils::Install.3*
%{_mandir}/man3/ExtUtils::Installed.3*
%{_mandir}/man3/ExtUtils::Packlist.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files ExtUtils-Manifest
%dir %{privlib}/ExtUtils
%{privlib}/ExtUtils/Manifest.pm
%{privlib}/ExtUtils/MANIFEST.SKIP
%{_mandir}/man3/ExtUtils::Manifest.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files ExtUtils-MakeMaker
%{_bindir}/instmodsh
%dir %{privlib}/ExtUtils
%{privlib}/ExtUtils/Command/
%{privlib}/ExtUtils/Liblist
%{privlib}/ExtUtils/Liblist.pm
%{privlib}/ExtUtils/MakeMaker
%{privlib}/ExtUtils/MakeMaker.pm
%{privlib}/ExtUtils/MM.pm
%{privlib}/ExtUtils/MM_*.pm
%{privlib}/ExtUtils/MY.pm
%{privlib}/ExtUtils/Mkbootstrap.pm
%{privlib}/ExtUtils/Mksymlists.pm
%{privlib}/ExtUtils/testlib.pm
%{_mandir}/man1/instmodsh.1*
%{_mandir}/man3/ExtUtils::Command::MM*
%{_mandir}/man3/ExtUtils::Liblist.3*
%{_mandir}/man3/ExtUtils::MM.3*
%{_mandir}/man3/ExtUtils::MM_*
%{_mandir}/man3/ExtUtils::MY.3*
%{_mandir}/man3/ExtUtils::MakeMaker*
%{_mandir}/man3/ExtUtils::Mkbootstrap.3*
%{_mandir}/man3/ExtUtils::Mksymlists.3*
%{_mandir}/man3/ExtUtils::testlib.3*
%endif

%files ExtUtils-Miniperl
%dir %{privlib}/ExtUtils
%{privlib}/ExtUtils/Miniperl.pm
%{_mandir}/man3/ExtUtils::Miniperl.3*

%if %{dual_life} || %{rebuild_from_scratch}
%files ExtUtils-MM-Utils
%dir %{privlib}/ExtUtils
%dir %{privlib}/ExtUtils/MM
%{privlib}/ExtUtils/MM/Utils.pm
%{_mandir}/man3/ExtUtils::MM::Utils.*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files ExtUtils-ParseXS
%dir %{privlib}/ExtUtils
%dir %{privlib}/ExtUtils/ParseXS
%{privlib}/ExtUtils/ParseXS.pm
%{privlib}/ExtUtils/ParseXS.pod
%{privlib}/ExtUtils/ParseXS/Constants.pm
%{privlib}/ExtUtils/ParseXS/CountLines.pm
%{privlib}/ExtUtils/ParseXS/Eval.pm
%{privlib}/ExtUtils/ParseXS/Utilities.pm
%dir %{privlib}/ExtUtils/Typemaps
%{privlib}/ExtUtils/Typemaps.pm
%{privlib}/ExtUtils/Typemaps/Cmd.pm
%{privlib}/ExtUtils/Typemaps/InputMap.pm
%{privlib}/ExtUtils/Typemaps/OutputMap.pm
%{privlib}/ExtUtils/Typemaps/Type.pm
%{privlib}/ExtUtils/xsubpp
%dir %{privlib}/pod
%{privlib}/pod/perlxs.pod
%{privlib}/pod/perlxstut.pod
%{privlib}/pod/perlxstypemap.pod
%{_bindir}/xsubpp
%{_mandir}/man1/perlxs*
%{_mandir}/man1/xsubpp*
%{_mandir}/man3/ExtUtils::ParseXS.3*
%{_mandir}/man3/ExtUtils::ParseXS::Constants.3*
%{_mandir}/man3/ExtUtils::ParseXS::Eval.3*
%{_mandir}/man3/ExtUtils::ParseXS::Utilities.3*
%{_mandir}/man3/ExtUtils::Typemaps.3*
%{_mandir}/man3/ExtUtils::Typemaps::Cmd.3*
%{_mandir}/man3/ExtUtils::Typemaps::InputMap.3*
%{_mandir}/man3/ExtUtils::Typemaps::OutputMap.3*
%{_mandir}/man3/ExtUtils::Typemaps::Type.3*
%endif

%files Fcntl
%{archlib}/Fcntl.pm
%{archlib}/auto/Fcntl
%{_mandir}/man3/Fcntl.3*

%files fields
%{privlib}/fields.pm
%{_mandir}/man3/fields.3*

%files File-Basename
%dir %{privlib}/File
%{privlib}/File/Basename.pm
%{_mandir}/man3/File::Basename.3*

%files File-Compare
%dir %{privlib}/File
%{privlib}/File/Compare.pm
%{_mandir}/man3/File::Compare.3*

%files File-Copy
%dir %{privlib}/File
%{privlib}/File/Copy.pm
%{_mandir}/man3/File::Copy.3*

%files File-DosGlob
%dir %{archlib}/File
%{archlib}/File/DosGlob.pm
%dir %{archlib}/auto/File
%{archlib}/auto/File/DosGlob
%{_mandir}/man3/File::DosGlob.3*

%if %{dual_life} || %{rebuild_from_scratch}
%files File-Fetch
%dir %{privlib}/File
%{privlib}/File/Fetch.pm
%{_mandir}/man3/File::Fetch.3*
%endif

%files File-Find
%dir %{privlib}/File
%{privlib}/File/Find.pm
%{_mandir}/man3/File::Find.3*

%if %{dual_life} || %{rebuild_from_scratch}
%files File-Path
%dir %{privlib}/File
%{privlib}/File/Path.pm
%{_mandir}/man3/File::Path.3*
%endif

%files File-stat
%dir %{privlib}/File
%{privlib}/File/stat.pm
%{_mandir}/man3/File::stat.3*

%if %{dual_life} || %{rebuild_from_scratch}
%files File-Temp
%dir %{privlib}/File
%{privlib}/File/Temp.pm
%{_mandir}/man3/File::Temp.3*
%endif

%files FileCache
%{privlib}/FileCache.pm
%{_mandir}/man3/FileCache.3*

%files FileHandle
%{privlib}/FileHandle.pm
%{_mandir}/man3/FileHandle.3*

%files filetest
%{privlib}/filetest.pm
%{_mandir}/man3/filetest.3*

%if %{dual_life} || %{rebuild_from_scratch}
%files Filter
%dir %{archlib}/auto/Filter
%{archlib}/auto/Filter/Util
%dir %{archlib}/Filter
%{archlib}/Filter/Util
%{privlib}/pod/perlfilter.pod
%{_mandir}/man1/perlfilter.*
%{_mandir}/man3/Filter::Util::*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Filter-Simple
%dir %{privlib}/Filter
%{privlib}/Filter/Simple.pm
%{_mandir}/man3/Filter::Simple.3*
%endif

%files FindBin
%{privlib}/FindBin.pm
%{_mandir}/man3/FindBin.*

%if %{with gdbm}
%files GDBM_File
%{archlib}/GDBM_File.pm
%{archlib}/auto/GDBM_File
%{_mandir}/man3/GDBM_File.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Getopt-Long
%dir %{privlib}/Getopt
%{privlib}/Getopt/Long.pm
%{_mandir}/man3/Getopt::Long.3*
%endif

%files Getopt-Std
%dir %{privlib}/Getopt
%{privlib}/Getopt/Std.pm
%{_mandir}/man3/Getopt::Std.3*

%files Hash-Util
%dir %{archlib}/Hash
%{archlib}/Hash/Util.pm
%dir %{archlib}/auto/Hash
%dir %{archlib}/auto/Hash/Util
%{archlib}/auto/Hash/Util/Util.so
%{_mandir}/man3/Hash::Util.3*

%files Hash-Util-FieldHash
%dir %{archlib}/auto/Hash
%dir %{archlib}/auto/Hash/Util
%{archlib}/auto/Hash/Util/FieldHash
%dir %{archlib}/Hash
%dir %{archlib}/Hash/Util
%{archlib}/Hash/Util/FieldHash.pm
%{_mandir}/man3/Hash::Util::FieldHash.3*

%files if
%{privlib}/if.pm
%{_mandir}/man3/if.3*

%files IO
%dir %{archlib}/IO
%{archlib}/IO.pm
%{archlib}/IO/Dir.pm
%{archlib}/IO/File.pm
%{archlib}/IO/Handle.pm
%{archlib}/IO/Pipe.pm
%{archlib}/IO/Poll.pm
%{archlib}/IO/Seekable.pm
%{archlib}/IO/Select.pm
%dir %{archlib}/IO/Socket
%{archlib}/IO/Socket/INET.pm
%{archlib}/IO/Socket/UNIX.pm
%{archlib}/IO/Socket.pm
%dir %{archlib}/auto/IO
%{archlib}/auto/IO/IO.so
%{_mandir}/man3/IO.*
%{_mandir}/man3/IO::Dir.*
%{_mandir}/man3/IO::File.*
%{_mandir}/man3/IO::Handle.*
%{_mandir}/man3/IO::Pipe.*
%{_mandir}/man3/IO::Poll.*
%{_mandir}/man3/IO::Seekable.*
%{_mandir}/man3/IO::Select.*
%{_mandir}/man3/IO::Socket::INET.*
%{_mandir}/man3/IO::Socket::UNIX.*
%{_mandir}/man3/IO::Socket.*

%if %{dual_life} || %{rebuild_from_scratch}
%files IO-Compress
# IO-Compress
%{_bindir}/streamzip
%{_bindir}/zipdetails
%dir %{privlib}/IO
%dir %{privlib}/IO/Compress
%{privlib}/IO/Compress/FAQ.pod
%{_mandir}/man1/streamzip.*
%{_mandir}/man1/zipdetails.*
%{_mandir}/man3/IO::Compress::FAQ.*
# Compress-Zlib
%dir %{privlib}/Compress
%{privlib}/Compress/Zlib.pm
%{_mandir}/man3/Compress::Zlib*
#IO-Compress-Base
%dir %{privlib}/File
%{privlib}/File/GlobMapper.pm
%{privlib}/IO/Compress/Base
%{privlib}/IO/Compress/Base.pm
%dir %{privlib}/IO/Uncompress
%{privlib}/IO/Uncompress/AnyUncompress.pm
%{privlib}/IO/Uncompress/Base.pm
%{_mandir}/man3/File::GlobMapper.*
%{_mandir}/man3/IO::Compress::Base.*
%{_mandir}/man3/IO::Uncompress::AnyUncompress.*
%{_mandir}/man3/IO::Uncompress::Base.*
# IO-Compress-Zlib
%{privlib}/IO/Compress/Adapter
%{privlib}/IO/Compress/Deflate.pm
%{privlib}/IO/Compress/Bzip2.pm
%{privlib}/IO/Compress/Gzip
%{privlib}/IO/Compress/Gzip.pm
%{privlib}/IO/Compress/RawDeflate.pm
%{privlib}/IO/Compress/Zip
%{privlib}/IO/Compress/Zip.pm
%{privlib}/IO/Compress/Zlib
%{privlib}/IO/Uncompress/Adapter/
%{privlib}/IO/Uncompress/AnyInflate.pm
%{privlib}/IO/Uncompress/Bunzip2.pm
%{privlib}/IO/Uncompress/Gunzip.pm
%{privlib}/IO/Uncompress/Inflate.pm
%{privlib}/IO/Uncompress/RawInflate.pm
%{privlib}/IO/Uncompress/Unzip.pm
%{_mandir}/man3/IO::Compress::Deflate*
%{_mandir}/man3/IO::Compress::Gzip*
%{_mandir}/man3/IO::Compress::Bzip2*
%{_mandir}/man3/IO::Compress::RawDeflate*
%{_mandir}/man3/IO::Compress::Zip*
%{_mandir}/man3/IO::Uncompress::AnyInflate*
%{_mandir}/man3/IO::Uncompress::Bunzip2*
%{_mandir}/man3/IO::Uncompress::Gunzip*
%{_mandir}/man3/IO::Uncompress::Inflate*
%{_mandir}/man3/IO::Uncompress::RawInflate*
%{_mandir}/man3/IO::Uncompress::Unzip*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files IO-Socket-IP
%dir %{privlib}/IO
%dir %{privlib}/IO/Socket
%{privlib}/IO/Socket/IP.pm
%{_mandir}/man3/IO::Socket::IP.*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files IO-Zlib
%dir %{privlib}/IO
%{privlib}/IO/Zlib.pm
%{_mandir}/man3/IO::Zlib.*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files HTTP-Tiny
%dir %{privlib}/HTTP
%{privlib}/HTTP/Tiny.pm
%{_mandir}/man3/HTTP::Tiny*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files IPC-Cmd
%dir %{privlib}/IPC
%{privlib}/IPC/Cmd.pm
%{_mandir}/man3/IPC::Cmd.3*
%endif

%files IPC-Open3
%dir %{privlib}/IPC
%{privlib}/IPC/Open2.pm
%{privlib}/IPC/Open3.pm
%{_mandir}/man3/IPC::Open2.3*
%{_mandir}/man3/IPC::Open3.3*

%if %{dual_life} || %{rebuild_from_scratch}
%files IPC-SysV
%{archlib}/auto/IPC
%dir %{archlib}/IPC
%{archlib}/IPC/Msg.pm
%{archlib}/IPC/Semaphore.pm
%{archlib}/IPC/SharedMem.pm
%{archlib}/IPC/SysV.pm
%{_mandir}/man3/IPC::Msg.*
%{_mandir}/man3/IPC::Semaphore.*
%{_mandir}/man3/IPC::SharedMem.*
%{_mandir}/man3/IPC::SysV.*
%endif

%files I18N-Collate
%dir %{privlib}/I18N
%{privlib}/I18N/Collate.pm
%{_mandir}/man3/I18N::Collate.*

%files I18N-Langinfo
%{archlib}/auto/I18N
%{archlib}/I18N
%{_mandir}/man3/I18N::Langinfo.*

%files I18N-LangTags
%dir %{privlib}/I18N
%{privlib}/I18N/LangTags
%{privlib}/I18N/LangTags.pm
%{_mandir}/man3/I18N::LangTags.*
%{_mandir}/man3/I18N::LangTags::*

%if %{dual_life} || %{rebuild_from_scratch}
%files JSON-PP
%{_bindir}/json_pp
%dir %{privlib}/JSON
%{privlib}/JSON/PP
%{privlib}/JSON/PP.pm
%{_mandir}/man1/json_pp.1*
%{_mandir}/man3/JSON::PP.3*
%{_mandir}/man3/JSON::PP::Boolean.3pm*
%endif

%files less
%{privlib}/less.pm
%{_mandir}/man3/less.*

%files lib
%{archlib}/lib.pm
%{_mandir}/man3/lib.*

%if %{dual_life} || %{rebuild_from_scratch}
%files libnet
%dir %{privlib}/Net
%{privlib}/Net/Cmd.pm
%{privlib}/Net/Config.pm
%{privlib}/Net/Domain.pm
%{privlib}/Net/FTP
%{privlib}/Net/FTP.pm
%{privlib}/Net/libnetFAQ.pod
%{privlib}/Net/NNTP.pm
%{privlib}/Net/Netrc.pm
%{privlib}/Net/POP3.pm
%{privlib}/Net/SMTP.pm
%{privlib}/Net/Time.pm
%{_mandir}/man3/Net::Cmd.*
%{_mandir}/man3/Net::Config.*
%{_mandir}/man3/Net::Domain.*
%{_mandir}/man3/Net::FTP.*
%{_mandir}/man3/Net::libnetFAQ.*
%{_mandir}/man3/Net::NNTP.*
%{_mandir}/man3/Net::Netrc.*
%{_mandir}/man3/Net::POP3.*
%{_mandir}/man3/Net::SMTP.*
%{_mandir}/man3/Net::Time.*
%endif

%files libnetcfg
%{_bindir}/libnetcfg
%{_mandir}/man1/libnetcfg*

%files locale
%{privlib}/locale.pm
%{_mandir}/man3/locale.*

%if %{dual_life} || %{rebuild_from_scratch}
%files Locale-Maketext
%dir %{privlib}/Locale
%dir %{privlib}/Locale/Maketext
%{privlib}/Locale/Maketext.*
%{privlib}/Locale/Maketext/Cookbook.*
%{privlib}/Locale/Maketext/Guts.*
%{privlib}/Locale/Maketext/GutsLoader.*
%{privlib}/Locale/Maketext/TPJ13.*
%{_mandir}/man3/Locale::Maketext.*
%{_mandir}/man3/Locale::Maketext::Cookbook.*
%{_mandir}/man3/Locale::Maketext::Guts.*
%{_mandir}/man3/Locale::Maketext::GutsLoader.*
%{_mandir}/man3/Locale::Maketext::TPJ13.*
%endif

%files Locale-Maketext-Simple
%dir %{privlib}/Locale
%dir %{privlib}/Locale/Maketext
%{privlib}/Locale/Maketext/Simple.pm
%{_mandir}/man3/Locale::Maketext::Simple.*

%if %{dual_life} || %{rebuild_from_scratch}
%files Math-BigInt
%dir %{privlib}/Math
%{privlib}/Math/BigFloat.pm
%{privlib}/Math/BigInt.pm
%dir %{privlib}/Math/BigInt
%{privlib}/Math/BigInt/Calc.pm
%{privlib}/Math/BigInt/Lib.pm
%{_mandir}/man3/Math::BigFloat.*
%{_mandir}/man3/Math::BigInt.*
%{_mandir}/man3/Math::BigInt::Calc.*
%{_mandir}/man3/Math::BigInt::Lib.*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Math-BigInt-FastCalc
%{archlib}/Math
%{archlib}/auto/Math
%{_mandir}/man3/Math::BigInt::FastCalc.*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Math-BigRat
%dir %{privlib}/Math
%{privlib}/Math/BigRat.pm
%{_mandir}/man3/Math::BigRat.*
%endif

%files Math-Complex
%dir %{privlib}/Math
%{privlib}/Math/Complex.pm
%{privlib}/Math/Trig.pm
%{_mandir}/man3/Math::Complex.*
%{_mandir}/man3/Math::Trig.*

%files Memoize
%{privlib}/Memoize
%{privlib}/Memoize.pm
%{_mandir}/man3/Memoize::*
%{_mandir}/man3/Memoize.*

%files meta-notation
%{privlib}/meta_notation.pm

%if %{dual_life} || %{rebuild_from_scratch}
%files MIME-Base64
%{archlib}/auto/MIME
%{archlib}/MIME
%{_mandir}/man3/MIME::*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Module-CoreList
%dir %{privlib}/Module
%{privlib}/Module/CoreList
%{privlib}/Module/CoreList.pm
%{privlib}/Module/CoreList.pod
%{_mandir}/man3/Module::CoreList*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Module-CoreList-tools
%{_bindir}/corelist
%{_mandir}/man1/corelist*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Module-Load
%dir %{privlib}/Module
%{privlib}/Module/Load.pm
%{_mandir}/man3/Module::Load.*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Module-Load-Conditional
%dir %{privlib}/Module
%{privlib}/Module/Load
%{_mandir}/man3/Module::Load::Conditional* 
%endif

%files Module-Loaded
%dir %{privlib}/Module
%{privlib}/Module/Loaded.pm
%{_mandir}/man3/Module::Loaded*

%if %{dual_life} || %{rebuild_from_scratch}
%files Module-Metadata
%dir %{privlib}/Module
%{privlib}/Module/Metadata.pm
%{_mandir}/man3/Module::Metadata.3pm*
%endif

%files mro
%{archlib}/auto/mro
%{archlib}/mro.pm
%{_mandir}/man3/mro.3*

%if %{with gdbm}
%files NDBM_File
%{archlib}/NDBM_File.pm
%{archlib}/auto/NDBM_File
%{_mandir}/man3/NDBM_File.3*
%endif

%files Net
%dir %{privlib}/Net
%{privlib}/Net/hostent.pm
%{privlib}/Net/netent.pm
%{privlib}/Net/protoent.pm
%{privlib}/Net/servent.pm
%{_mandir}/man3/Net::hostent.3*
%{_mandir}/man3/Net::netent.3*
%{_mandir}/man3/Net::protoent.3*
%{_mandir}/man3/Net::servent.3*

%if %{dual_life} || %{rebuild_from_scratch}
%files Net-Ping
%dir %{privlib}/Net
%{privlib}/Net/Ping.pm
%{_mandir}/man3/Net::Ping.*
%endif

%files NEXT
%{privlib}/NEXT.pm
%{_mandir}/man3/NEXT.*

%if %{with gdbm}
%files ODBM_File
%{archlib}/ODBM_File.pm
%{archlib}/auto/ODBM_File
%{_mandir}/man3/ODBM_File.3*
%endif

%files open
%{privlib}/open.pm
%{_mandir}/man3/open.3*

%files Opcode
%{archlib}/auto/Opcode
%{archlib}/Opcode.pm
%{archlib}/ops.pm
%{_mandir}/man3/Opcode.3*
%{_mandir}/man3/ops.3*

%files overload
%{privlib}/overload.pm
%{_mandir}/man3/overload.3*

%files overloading
%dir %{privlib}/overload
%{privlib}/overload/numbers.pm
%{privlib}/overloading.pm
%{_mandir}/man3/overloading.3*

%if %{dual_life} || %{rebuild_from_scratch}
%files parent
%{privlib}/parent.pm
%{_mandir}/man3/parent.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Params-Check
%{privlib}/Params/
%{_mandir}/man3/Params::Check*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files PathTools
%{archlib}/Cwd.pm
%dir %{archlib}/File
%{archlib}/File/Spec*
%{archlib}/auto/Cwd
%{_mandir}/man3/Cwd*
%{_mandir}/man3/File::Spec*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Perl-OSType
%dir %{privlib}/Perl
%{privlib}/Perl/OSType.pm
%{_mandir}/man3/Perl::OSType.3pm*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files perlfaq
%{privlib}/perlfaq.pm
%dir %{privlib}/pod
%{privlib}/pod/perlfaq*
%{privlib}/pod/perlglossary.pod
%{_mandir}/man1/perlfaq*
%{_mandir}/man1/perlglossary.*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files PerlIO-via-QuotedPrint
%{privlib}/PerlIO
%{_mandir}/man3/PerlIO::via::QuotedPrint.*
%endif

%files ph
%{archlib}/asm
%{archlib}/asm-generic
%{archlib}/bits
%{archlib}/features*.ph
%{archlib}/gnu
%{archlib}/_h2ph_pre.ph
%ifnarch ppc64le
%{archlib}/linux
%endif
%{archlib}/stdc-predef.ph
%{archlib}/sys
%{archlib}/syscall.ph

%if %{dual_life} || %{rebuild_from_scratch}
%files Pod-Checker
%{_bindir}/podchecker
%dir %{privlib}/Pod
%{privlib}/Pod/Checker.pm
%{_mandir}/man1/podchecker.*
%{_mandir}/man3/Pod::Checker.*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Pod-Escapes
%dir %{privlib}/Pod
%{privlib}/Pod/Escapes.pm
%{_mandir}/man3/Pod::Escapes.*
%endif

%files Pod-Functions
%dir %{privlib}/Pod
%{privlib}/Pod/Functions.pm

%files Pod-Html
%license Pod-Html-license-clarification
%dir %{privlib}/Pod
%{_bindir}/pod2html
%{privlib}/Pod/Html.pm
%{_mandir}/man1/pod2html.1*
%{_mandir}/man3/Pod::Html.*

%if %{dual_life} || %{rebuild_from_scratch}
%files Pod-Perldoc
%{_bindir}/perldoc
%{privlib}/pod/perldoc.pod
%dir %{privlib}/Pod
%{privlib}/Pod/Perldoc
%{privlib}/Pod/Perldoc.pm
%{_mandir}/man1/perldoc.1*
%{_mandir}/man3/Pod::Perldoc*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Pod-Usage
%{_bindir}/pod2usage
%dir %{privlib}/Pod
%{privlib}/Pod/Usage.pm
%{_mandir}/man1/pod2usage.*
%{_mandir}/man3/Pod::Usage.*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files podlators
%{_bindir}/pod2man
%{_bindir}/pod2text
%{privlib}/pod/perlpodstyle.pod
%dir %{privlib}/Pod
%{privlib}/Pod/Man.pm
%{privlib}/Pod/ParseLink.pm
%{privlib}/Pod/Text
%{privlib}/Pod/Text.pm
%{_mandir}/man1/pod2man.1*
%{_mandir}/man1/pod2text.1*
%{_mandir}/man1/perlpodstyle.1*
%{_mandir}/man3/Pod::Man*
%{_mandir}/man3/Pod::ParseLink*
%{_mandir}/man3/Pod::Text*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Pod-Simple
%dir %{privlib}/Pod
%{privlib}/Pod/Simple
%{privlib}/Pod/Simple.pm
%{privlib}/Pod/Simple.pod
%{_mandir}/man3/Pod::Simple*
%endif

%files POSIX
%{archlib}/auto/POSIX
%{archlib}/POSIX.*
%{_mandir}/man3/POSIX.*

%files Safe
%{privlib}/Safe.pm
%{_mandir}/man3/Safe.*

%if %{dual_life} || %{rebuild_from_scratch}
%files Scalar-List-Utils
%{archlib}/List
%{archlib}/Scalar
%{archlib}/Sub
%{archlib}/auto/List
%{_mandir}/man3/List::Util*
%{_mandir}/man3/Scalar::Util*
%{_mandir}/man3/Sub::Util*
%endif

%files Search-Dict
%{privlib}/Search
%{_mandir}/man3/Search::*

%files SelectSaver
%{privlib}/SelectSaver.pm
%{_mandir}/man3/SelectSaver.*

%files SelfLoader
%{privlib}/SelfLoader.pm
%{_mandir}/man3/SelfLoader.*

%files sigtrap
%{privlib}/sigtrap.pm
%{_mandir}/man3/sigtrap.*

%if %{dual_life} || %{rebuild_from_scratch}
%files Socket
%dir %{archlib}/auto/Socket
%{archlib}/auto/Socket/Socket.*
%{archlib}/Socket.pm
%{_mandir}/man3/Socket.3*
%endif

%files sort
%{privlib}/sort.pm
%{_mandir}/man3/sort.*

%if %{dual_life} || %{rebuild_from_scratch}
%files Storable
%{archlib}/Storable.pm
%{archlib}/auto/Storable
%{_mandir}/man3/Storable.*
%endif

%files subs
%{privlib}/subs.pm
%{_mandir}/man3/subs.*

%files Symbol
%{privlib}/Symbol.pm
%{_mandir}/man3/Symbol.*

%files Sys-Hostname
%dir %{archlib}/auto/Sys
%{archlib}/auto/Sys/Hostname
%dir %{archlib}/Sys
%{archlib}/Sys/Hostname.pm
%{_mandir}/man3/Sys::Hostname.*

%if %{dual_life} || %{rebuild_from_scratch}
%files Sys-Syslog
%dir %{archlib}/Sys
%{archlib}/Sys/Syslog.pm
%dir %{archlib}/auto/Sys
%{archlib}/auto/Sys/Syslog
%{_mandir}/man3/Sys::Syslog.*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Term-ANSIColor
%dir %{privlib}/Term
%{privlib}/Term/ANSIColor.pm
%{_mandir}/man3/Term::ANSIColor*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Term-Cap
%dir %{privlib}/Term
%{privlib}/Term/Cap.pm
%{_mandir}/man3/Term::Cap.*
%endif

%files Term-Complete
%dir %{privlib}/Term
%{privlib}/Term/Complete.pm
%{_mandir}/man3/Term::Complete.*

%files Term-ReadLine
%dir %{privlib}/Term
%{privlib}/Term/ReadLine.pm
%{_mandir}/man3/Term::ReadLine.*

%files Test
%{privlib}/Test.pm
%{_mandir}/man3/Test.*

%if %{dual_life} || %{rebuild_from_scratch}
%files Test-Harness
%{_bindir}/prove
%dir %{privlib}/App
%{privlib}/App/Prove*
%{privlib}/TAP*
%dir %{privlib}/Test
%{privlib}/Test/Harness*
%{_mandir}/man1/prove.1*
%{_mandir}/man3/App::Prove*
%{_mandir}/man3/TAP*
%{_mandir}/man3/Test::Harness*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Test-Simple
%{privlib}/ok*
%dir %{privlib}/Test
%{privlib}/Test/More*
%{privlib}/Test/Builder*
%{privlib}/Test/Tester*
%{privlib}/Test/Simple*
%{privlib}/Test/Tutorial*
%{privlib}/Test/use
%{privlib}/Test2*
%{_mandir}/man3/ok*
%{_mandir}/man3/Test::More*
%{_mandir}/man3/Test::Builder*
%{_mandir}/man3/Test::Tester*
%{_mandir}/man3/Test::Simple*
%{_mandir}/man3/Test::Tutorial*
%{_mandir}/man3/Test::use::*
%{_mandir}/man3/Test2*
%endif

%files Text-Abbrev
%dir %{privlib}/Text
%{privlib}/Text/Abbrev.pm
%{_mandir}/man3/Text::Abbrev.*

%if %{dual_life} || %{rebuild_from_scratch}
%files Text-Balanced
%dir %{privlib}/Text
%{privlib}/Text/Balanced.pm
%{_mandir}/man3/Text::Balanced.*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Text-ParseWords
%dir %{privlib}/Text
%{privlib}/Text/ParseWords.pm
%{_mandir}/man3/Text::ParseWords.*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Text-Tabs+Wrap
%dir %{privlib}/Text
%{privlib}/Text/Tabs.pm
%{privlib}/Text/Wrap.pm
%{_mandir}/man3/Text::Tabs.*
%{_mandir}/man3/Text::Wrap.*
%endif

%files Thread
%{privlib}/Thread.pm
%{_mandir}/man3/Thread.*

%if %{dual_life} || %{rebuild_from_scratch}
%files Thread-Queue
%dir %{privlib}/Thread
%{privlib}/Thread/Queue.pm
%{_mandir}/man3/Thread::Queue.*
%endif

%files Thread-Semaphore
%dir %{privlib}/Thread
%{privlib}/Thread/Semaphore.pm
%{_mandir}/man3/Thread::Semaphore.*

%files Tie
%dir %{privlib}/Tie
%{privlib}/Tie/Array.pm
%{privlib}/Tie/Handle.pm
%{privlib}/Tie/Scalar.pm
%{privlib}/Tie/StdHandle.pm
%{privlib}/Tie/SubstrHash.pm
%{_mandir}/man3/Tie::Array.*
%{_mandir}/man3/Tie::Handle.*
%{_mandir}/man3/Tie::Scalar.*
%{_mandir}/man3/Tie::StdHandle.*
%{_mandir}/man3/Tie::SubstrHash.*

%files Tie-File
%dir %{privlib}/Tie
%{privlib}/Tie/File.pm
%{_mandir}/man3/Tie::File.*

%files Tie-Memoize
%dir %{privlib}/Tie
%{privlib}/Tie/Memoize.pm
%{_mandir}/man3/Tie::Memoize.*

%if %{dual_life} || %{rebuild_from_scratch}
%files Tie-RefHash
%dir %{privlib}/Tie
%{privlib}/Tie/RefHash.pm
%{_mandir}/man3/Tie::RefHash.*
%endif

%files Time
%dir %{privlib}/Time
%{privlib}/Time/gmtime.pm
%{privlib}/Time/localtime.pm
%{privlib}/Time/tm.pm
%{_mandir}/man3/Time::gmtime.*
%{_mandir}/man3/Time::localtime.*
%{_mandir}/man3/Time::tm.*

%if %{dual_life} || %{rebuild_from_scratch}
%files Time-HiRes
%dir %{archlib}/Time
%{archlib}/Time/HiRes.pm
%dir %{archlib}/auto/Time
%{archlib}/auto/Time/HiRes
%{_mandir}/man3/Time::HiRes.*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Time-Local
%dir %{privlib}/Time
%{privlib}/Time/Local.pm
%{_mandir}/man3/Time::Local.*
%endif

%files Time-Piece
%dir %{archlib}/Time
%{archlib}/Time/Piece.pm 
%{archlib}/Time/Seconds.pm
%dir %{archlib}/auto/Time
%{archlib}/auto/Time/Piece
%{_mandir}/man3/Time::Piece.3*
%{_mandir}/man3/Time::Seconds.3*

%if %{dual_life} || %{rebuild_from_scratch}
%files threads
%dir %{archlib}/auto/threads
%{archlib}/auto/threads/threads*
%{archlib}/threads.pm
%{_mandir}/man3/threads.3*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files threads-shared
%dir %{archlib}/auto/threads
%{archlib}/auto/threads/shared*
%dir %{archlib}/threads
%{archlib}/threads/shared*
%{_mandir}/man3/threads::shared*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Unicode-Collate
%dir %{archlib}/auto/Unicode
%{archlib}/auto/Unicode/Collate
%dir %{archlib}/Unicode
%{archlib}/Unicode/Collate
%{archlib}/Unicode/Collate.pm
%dir %{privlib}/Unicode
%{privlib}/Unicode/Collate
%{_mandir}/man3/Unicode::Collate.*
%{_mandir}/man3/Unicode::Collate::*
%endif

%if %{dual_life} || %{rebuild_from_scratch}
%files Unicode-Normalize
%dir %{archlib}/auto/Unicode
%{archlib}/auto/Unicode/Normalize
%dir %{archlib}/Unicode
%{archlib}/Unicode/Normalize.pm
%{_mandir}/man3/Unicode::Normalize.*
%endif

%files Unicode-UCD
%dir %{privlib}/Unicode
%{privlib}/Unicode/UCD.pm
%{_mandir}/man3/Unicode::UCD.*

%files User-pwent
%{privlib}/User
%{_mandir}/man3/User::*

%files vars
%{privlib}/vars.pm
%{_mandir}/man3/vars.*

%if %{dual_life} || %{rebuild_from_scratch}
%files version
%{privlib}/version.pm
%{privlib}/version.pod
%{privlib}/version/
%{_mandir}/man3/version.3*
%{_mandir}/man3/version::Internals.3*
%endif

%files vmsish
%{privlib}/vmsish.pm
%{_mandir}/man3/vmsish.*

# Old changelog entries are preserved in CVS.
%changelog
* Thu Dec 14 2023 Nicolas Guibourge <micolasg@microsoft.com> - 4:5.34.1-489
- Bump release for testing

* Fri May 20 2022 Andrew Phelps <anphel@microsoft.com> - 4:5.34.1-488
- Undefine "mariner_module_ldflags" to remove references to module_info.ld in embedded ldflags

* Wed Mar 30 2022 Andrew Phelps <anphel@microsoft.com> - 4:5.34.1-487
- Upgrade to version 5.34.1 referencing Fedora 37 (license: MIT)
- Removed duplicate requires for perl(:VERSION) from gendep.macros
- Align Module-CoreList and Module-CoreList-tools to version 5.20220313
- Switch to bcond_with for perl_enables_groff, perl_enables_turkish_test, perl_enables_systemtap, test
- Remove unncessary sources and patches

* Fri Jan 28 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 4:5.32.0-465
- Removed the "perl-DB_File" subpackage.
- Fixing macro usage.

* Tue Oct 26 2021 Pawel Winogrodzki <pawel.winogrodzki@microsoft.com> - 4:5.32.0-464
- Removing unused dependency on 'libdb-devel'.

* Mon Oct 12 2020 Joe Schmitt <joschmit@microsoft.com> - 4:5.32.0-463
- Initial CBL-Mariner import from Fedora 34 (license: MIT)
- Remove redhat rpm macros requirement.
- Remove libxcrypt requirement.
- Explicitly provide /bin/perl from perl-interpreter.
- Remove patches and options that do not apply to CBL-Mariner.
- License verified.

* Thu Aug 27 2020 Petr Pisar <ppisar@redhat.com> - 4:5.32.0-462
- Fix inheritance resolution of lexial objects in a debugger (GH#17661)
- Fix a misoptimization when assignig a list in a list context (GH#17816)
- Fix handling left-hand-side undef when assigning a list (GH#16685)
- Fix a memory leak when compiling a long regular expression (GH#18054)
- Fix handling exceptions in a global destruction (GH#18063)
- Fix sorting with a block that calls return (GH#18081)

* Fri Aug 21 2020 Jeff Law <law@redhat.com> - 4:5.32.0-461
- Re-enable LTO

* Thu Aug 06 2020 Petr Pisar <ppisar@redhat.com> - 4:5.32.0-460
- Fix an IO::Handle spurious error reported for regular file handles (GH#18019)

* Wed Aug 05 2020 Petr Pisar <ppisar@redhat.com> - 4:5.32.0-459
- Do not use a C compiler reserved identifiers
- Fix SvUV_nomg() macro definition
- Fix SvTRUE() documentation
- Fix ext/XS-APItest/t/utf8_warn_base.pl tests
- Fix IO::Handle::error() to report write errors (GH#6799)
- Fix a link to Unicode Technical Standard #18 (GH#17881)
- Fix setting a non-blocking mode in IO::Socket::UNIX (GH#17787)
- Fix running actions after stepping in a debugger (GH#17901)
- Fix a buffer size for asctime_r() and ctime_r() functions
- Prevent from an integer overflow in RenewDouble() macro
- Fix a buffer overread in when reallocating formats (GH#17844)
- Fix a number of arguments passed to a BOOT XS subroutine (GH#17755)

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4:5.32.0-458
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 30 2020 Jeff Law <law@redhat.com> - 4:5.32.0-457
- Disable LTO

* Fri Jun 26 2020 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.32.0-456
- Perl 5.32 re-rebuild of bootstrapped packages

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.32.0-455
- 5.32.0 bump (see <https://metacpan.org/pod/release/XSAWYERX/perl-5.32.0/pod/perldelta.pod>
  or release notes)

* Tue Jun 02 2020 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.30.3-454
- 5.30.3 bump (see <https://metacpan.org/pod/release/XSAWYERX/perl-5.30.3/pod/perldelta.pod>
  for release notes)
- Security release fixes CVE-2020-10543, CVE-2020-10878 and CVE-2020-12723

* Fri Mar 27 2020 Petr Pisar <ppisar@redhat.com> - 4:5.30.2-453
- Make perl-macros package noarch
- Fix a directory ownership in perl-Sys-Hostname
- Work around a glibc bug in caching LC_MESSAGES (GH#17081)
- Fix POSIX:setlocale() documentation
- Prevent from an integer overflow in POSIX::SigSet()
- Fix thread-safety of IO::Handle (GH#14816)
- Close :unix PerlIO layers properly (bug #987118)
- Fix sorting tied arrays (GH#17496)
- Fix a spurious warning about a multidimensional syntax (GH#16535)
- Normalize "#!/perl" shebangs in the tests
- Fix a warning about an uninitialized value in B::Deparse (GH#17537)

* Mon Mar 16 2020 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.30.2-452
- 5.30.2 bump (see <https://metacpan.org/pod/release/SHAY/perl-5.30.2/pod/perldelta.pod>
  for release notes)

* Mon Feb 03 2020 Petr Pisar <ppisar@redhat.com> - 4:5.30.1-451
- Subpackage AutoLoader and AutoSplit
- Subpackage ExtUtils-Constant
- Subpackage NEXT
- Subpackage Tie-RefHash
- Subpackage autouse
- Subpackage base and fields
- Subpackage Dumpvalue
- Subpackage encoding-warnings
- Subpackage if
- Subpackage I18N-Collate
- Subpackage I18N-LangTags
- Subpackage lib
- Subpackage Safe
- Subpackage Search-Dict
- Subpackage Term-Complete
- Subpackage Term-ReadLine
- Subpackage Text-Abbrev
- Subpackage Thread-Semaphore
- Subpackage Tie-File
- Move attributes module into perl-libs
- Subpackage GDBM_File
- Subpackage NDBM_File
- Subpackage ODBM_File
- Move File::Glob module into perl-libs
- Subpackage File-DosGlob
- Subpackage File-Find
- Subpackage IPC-Open3
- Subpackage B
- Subpackage Fcntl
- Subpackage FileCache
- Subpackage Hash-Util
- Subpackage Hash-Util-FieldHash
- Subpackage I18N-Langinfo
- Subpackage mro
- Subpackage Opcode
- Move PerlIO to perl-libs
- Subpackage POSIX
- Subpackage Sys-Hostname
- Move Tie::Hash::NamedCapture to perl-libs
- Subpackage Tie-Memoize
- Subpackage Benchmark
- Subpackage blib
- Move charnames to perl-libs
- Subpackage File-stat
- Subpackage Class-Struct
- Subpackage Net::*ent modules into perl-Net
- Subpackage User::* modules into perl-User-pwent
- Subpackage Time
- Subpackage base Tie::* modules into perl-Tie
- Move Config to perl-libs
- Move warnings::register to perl-libs
- Subpackage DBM_Filter modules
- Subpackage FileHandle
- Subpackage Thread
- Subpackage Unicode::UCD
- Subpackage diagnostics and move splain tool from perl-utils there
- Subpackage FindBin
- Subpackage File::Basename
- Subpackage File::Compare
- Subpackage File::Copy
- Subpackage overload
- Subpackage overloading
- Subpackage Config::Extensions
- Subpackage English
- Subpackage Getopt::Std
- Subpackage locale
- Subpackage deprecate
- Move AnyDBM_File, SDBM_File, Tie::Hash to perl-libs because of dbmopen function
- Subpackage DirHandle
- Subpackage Symbol
- Subpackage SelectSaver
- Move UNIVERSAL to perl-libs
- Subpackage DynaLoader
- Subpackage filetest
- Subpackage less
- Subpackage meta_notation
- Subpackage sigtrap
- Subpackage sort
- Subpackage subs
- Subpackage vars
- Subpackage vmsish
- Subpackage Pod-Functions
- Move feature to perl-libs
- Move debugger files into perl-debugger
- Move perlxs* POD to perl-ExtUtils-ParseXS
- Move ExtUtils/typemap to perl-devel
- Remove ExtUtils::XSSymSet manual without the code (GH#17424)
- Reduce and move remaining ph files to perl-ph
- Move most of the generic POD files to perl-doc

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4:5.30.1-450
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov 29 2019 Petr Pisar <ppisar@redhat.com> - 4:5.30.1-449
- Fix a memory leak when compiling a regular expression with a non-word class
  (GH#17218)

* Tue Nov 12 2019 Petr Pisar <ppisar@redhat.com> - 4:5.30.1-448
- Fix overloading for binary and octal floats (RT#125557)
- Fix handling undefined array members in Dumpvalue (RT#134441)
- Fix taint mode documentation regarding @INC
- Fix handling a layer argument in Tie::StdHandle::BINMODE() (RT#132475)
- Fix an unintended upgrade to UTF-8 in the middle of a transliteration
- Fix a race in File::stat() tests (GH#17234)
- Fix a buffer overread when parsing a number (GH#17279)
- Fix GCC 10 version detection (GH#17295)

* Mon Nov 11 2019 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.30.1-447
- 5.30.1 bump (see <https://metacpan.org/pod/release/SHAY/perl-5.30.1/pod/perldelta.pod>
  for release notes)

* Wed Sep 11 2019 Petr Pisar <ppisar@redhat.com> - 4:5.30.0-446
- Fix a memory leak when matching a UTF-8 regular expression (RT#134390)
- Fix a detection for futimes (RT#134432)

* Mon Sep 02 2019 Petr Pisar <ppisar@redhat.com> - 4:5.30.0-445
- Adjust spec file to rpm-build-4.15.0-0.rc1.1
- Fix parsing a Unicode property name when compiling a regular expression
- Fix a buffer overread when parsing a Unicode property while compiling
  a regular expression (RT#134133)
- Do not interpret 0x and 0b prefixes when numifying strings (RT#134230)
- Fix a buffer overread when compiling a regular expression with many escapes
  (RT#134325)
- Fix a buffer overflow when compiling a regular expression with many branches
  (RT#134329)
- Correct a misspelling in perlrebackslash documentation (RT#134395)

* Thu Aug 22 2019 Petr Pisar <ppisar@redhat.com> - 4:5.30.0-444
- Fix a NULL pointer dereference in PerlIOVia_pushed()
- Fix a crash when setting $@ on unwinding a call stack (RT#134266)
- Fix parsing a denominator when parsing a Unicode property name
- Fix a documentation about a future API change
- Do not run File-Find tests in parallel

* Wed Aug 07 2019 Petr Pisar <ppisar@redhat.com> - 4:5.30.0-443
- Fix propagating non-string variables in an exception value (RT#134291)
- Include trailing zero in scalars holding trie data (RT#134207)
- Fix a use after free in /(?{...})/ (RT#134208)
- Fix a use after free in debugging output of a collation
- Fix file mode of a perl-example.stp example

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4:5.30.0-442
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 17 2019 Petr Pisar <ppisar@redhat.com> - 4:5.30.0-441
- Fix a test for a crash in SIGALARM handler when waiting on a child process to
  be closed (RT#122112)
- Fix a crash on an uninitialized warning when processing a multideref node
  (RT#134275)
- Preserve append mode when opening anonymous files (RT#134221)
- Run Turkish locale tests

* Tue Jun 25 2019 Petr Pisar <ppisar@redhat.com> - 4:5.30.0-440
- Fix an out-of-buffer read while parsing a Unicode property name (RT#134134)
- Do not panic when outputting a warning (RT#134059)
- Fix memory handling when parsing string literals
- Fix an undefined behavior in shifting IV variables
- Fix stacking file test operators (CPAN RT#127073)
- Fix a crash in SIGALARM handler when waiting on a child process to be closed
  (RT#122112)
- Fix a crash with a negative precision in sprintf function (RT#134008)
- Fix an erroneous assertion on OP_SCALAR (RT#134048)
- Prevent from wrapping a width in a numeric format string (RT#133913)
- Fix subroutine protypes to track reference aliases (RT#134072)
- Improve retrieving a scalar value of a variable modified in a signal handler
  (RT#134035)
- Fix changing packet destination sent from a UDP IO::Socket object (RT#133936)
- Fix a stack underflow in readline() if passed an empty array as an argument
  (#RT133989)
- Fix setting supplementar group IDs (RT#134169)
- Fix %%{^CAPTURE_ALL} to be an alias for %%- variable (RT#131867)
- Fix %%{^CAPTURE} value when used after @{^CAPTURE} (RT#134193)

* Tue Jun 11 2019 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.30.0-439
- Define %%perl_vendor*, %%perl_archlib, %%perl_privlib, because in rpm
  4.15 those are no longer defined

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.30.0-438
- Perl 5.30 re-rebuild of bootstrapped packages

* Wed May 22 2019 Jitka Plesnikova <jplesnik@redhat.com>, Petr Pisar <ppisar@redhat.com> - 4:5.30.0-437
- 5.30.0 bump (see <https://metacpan.org/pod/release/XSAWYERX/perl-5.30.0/pod/perldelta.pod>
  for release notes)
- Make site paths specific to Perl minor version (e.g.
  /usr/local/share/perl5/5.30) to prevent from an ABI clash after upgrade
  to an ABI-incompatible Perl

* Tue Apr 23 2019 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.28.2-436
- 5.28.2 bump (see <https://metacpan.org/pod/release/SHAY/perl-5.28.2/pod/perldelta.pod>
  for release notes)

* Fri Apr 05 2019 Petr Pisar <ppisar@redhat.com> - 4:5.28.1-435
- Fix a leak when compiling a typed hash dereference
- Fix a buffer overread when handling a scope error in qr/\(?{/ (RT#133879)
- Fix a buffer overread when parsing a regular expression with an unknown
  character name (RT#133880)
- Fix mbstate_t initialization in POSIX::mblen (RT#133928)
- Fix a memory leak when cloning a regular expression
- Fix a memory leak when spawning threads in a BEGIN phase
- Fix a memory leak when assigning a regular expression to a non-copy-on-write string
- Fix a memory leak when assignig to a localized ${^WARNING_BITS}
- Fix a memory leak when parsing misindented here-documents
- Fix a memory leak in package name lookup (RT#133977)
- Fix a memory leak when deletion in a tied hash dies
- Fix a crash when matching case insensitively (RT#133892)
- Fix a memory leak when warning about malformed UTF-8 string

* Tue Mar 05 2019 Björn Esser <besser82@fedoraproject.org> - 4:5.28.1-434
- Add explicit Requires: libxcrypt-devel to devel sub-package (bug #1666098)

* Fri Feb 22 2019 Petr Pisar <ppisar@redhat.com> - 4:5.28.1-433
- Fix a crash when parsing #line directives with large numbers in eval
  (RT#131562)
- Fix setting magic when changing $^R (RT#133782)
- Fix a race when loading XS modules
- Fix extending a stack in Perl parser (RT#133778)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4:5.28.1-432
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 16 2019 Petr Pisar <ppisar@redhat.com> - 4:5.28.1-431
- Remove a fix for un undefined C behavior in NULL pointer arithmetics
  (RT#133223) because it changes perl ABI

* Mon Jan 14 2019 Petr Pisar <ppisar@redhat.com> - 4:5.28.1-430
- Adjust tests to gdbm-1.15 using an upstream fix (RT#133295)
- Do not close an IPC pipe that already has a desired descriptor (RT#133726)
- Fix reporting a line number for non-terminated prototypes (RT#133524)
- Fix first eof() return value (RT#133721)
- Fix a crash when compiling a malformed form (RT#132158)
- Fix un undefined C behavior in NULL pointer arithmetics (RT#133223)
- Prevent long jumps from clobbering local variables (RT#133575)
- Fix a mismatch with a case-insesitive regular expression on a text with ligatures
  (RT#133756)
- Fix the interpreter path if procfs is not mounted (RT#133573)

* Mon Jan 14 2019 Björn Esser <besser82@fedoraproject.org> - 4:5.28.1-429
- Rebuilt for libcrypt.so.2 (#1666033)

* Sun Jan 13 2019 Björn Esser <besser82@fedoraproject.org> - 4:5.28.1-428
- Add BuildRequires: gcc-c++ for tests

* Fri Nov 30 2018 Petr Pisar <ppisar@redhat.com> - 4:5.28.1-427
- Fix script run matching to allow ASCII digits in scripts that use their own in
  addition (RT#133547)
- Fix PathTools tests to cope with ESTALE error (RT#133534)
- Fix an undefined behaviour in S_hv_delete_common()
- Fix in-place edit to replace files on a successful perl exit status
  (bug #1650041)
- Fix compiling regular expressions that contain both compile- and run-time
  compiled code blocks (RT#133687)

* Fri Nov 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.28.1-426
- 5.28.1 bump
- Fix CVE-2018-18312 (heap-buffer-overflow write in regcomp.c)

* Fri Nov 02 2018 Petr Pisar <ppisar@redhat.com> - 4:5.28.0-425
- Install Encode developmental files when installing complete Perl

* Thu Oct 25 2018 Jitka Plesnikova <jplesnik@redhat.com> -  4:5.28.0-424
- Fix annocheck failure by passing CFLAGS to dtrace

* Mon Sep 24 2018 Petr Pisar <ppisar@redhat.com> - 4:5.28.0-423
- Fix upack "u" of invalid data (RT#132655)

* Mon Sep 10 2018 Petr Pisar <ppisar@redhat.com> - 4:5.28.0-422
- Revert a fix for a buffer overrun in deprecated S_is_utf8_common()
  (bug #1627091)

* Wed Sep 05 2018 Petr Pisar <ppisar@redhat.com> - 4:5.28.0-421
- Fix a buffer overrun in deprecated S_is_utf8_common()
- Fix a buffer overrun in deprecated utf8_to_uvchr()
- Fix a time race in Time-HiRes/t/itimer.t test
- Fix matching an ASCII digit followed by a non-ASCII digit using a script run
- Fix Time::Piece to handle objects in overloaded methods correctly
- Fix an assignment to a lexical variable in multiconcatenation expressions
  (RT#133441)
- Fix a spurious warning about uninitialized value in warn (RT#132683)
- Require Devel::PPPort by perl-devel for h2xs script

* Wed Aug 01 2018 Petr Pisar <ppisar@redhat.com> - 4:5.28.0-420
- Fix a file descriptor leak in in-place edits (RT#133314)

* Tue Jul 17 2018 Petr Pisar <ppisar@redhat.com> - 4:5.28.0-419
- Fix index() and rindex() optimization in given-when boolean context
  (RT#133368)
- Fix build conditions in locale.c

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4:5.28.0-418
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 09 2018 Petr Pisar <ppisar@redhat.com> - 4:5.28.0-417
- Adjust tests to gdbm-1.15 (RT#133295)
- Fix an integer wrap when allocating memory for an environment variable
  (RT#133204)
- Fix printing a warning about a wide character when matching a regular
  expression while ISO-8859-1 locale is in effect
- Fix invoking a check for wide characters while ISO-8859-1 locale is in effect

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.28.0-416
- Stop providing old perl(MODULE_COMPAT_5.26.*)

* Tue Jun 26 2018 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.28.0-415
- 5.28.0 bump (see <https://metacpan.org/pod/release/XSAWYERX/perl-5.28.0/pod/perldelta.pod>
  for release notes)

* Fri May 25 2018 Petr Pisar <ppisar@redhat.com> - 4:5.26.2-414
- Fix an infinite loop in the regular expression compiler (RT#133185)

* Fri May 18 2018 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.26.2-413
- Correct license tags of perl-libs (bug #1579524)

* Thu Apr 19 2018 Petr Pisar <ppisar@redhat.com> - 4:5.26.2-412
- perl-devel requires redhat-rpm-config because of hardened compiler profiles
  (bug #1557667)
- Do not clobber file bytes in :encoding layer (RT#132833)
- Fix line numbers in multi-line s/// (RT#131930)
- Fix parsing extended bracketed character classes (RT#132167)
- Fix a possibly unitialized memory read in the Perl parser (RT#133074)

* Mon Apr 16 2018 Petr Pisar <ppisar@redhat.com> - 4:5.26.2-411
- 5.26.2 bump

* Mon Mar 26 2018 Petr Pisar <ppisar@redhat.com> - 4:5.26.2-410.RC1
- 5.26.2-RC1 bump
- Fix CVE-2018-6913 (heap buffer overflow in pp_pack.c) (bug #1567776)
- Fix CVE-2018-6798 (heap read overflow in regexec.c) (bug #1567777)
- Fix CVE-2018-6797 (heap write overflow in regcomp.c) (bug #1567778)

* Thu Mar  1 2018 Florian Weimer <fweimer@redhat.com> - 4:5.26.1-409
- Rebuild to pick up new build flags from redhat-rpm-config

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4:5.26.1-408
- Escape macros in %%changelog

* Tue Feb 06 2018 Petr Pisar <ppisar@redhat.com> - 4:5.26.1-407
- Fix parsing braced subscript after parentheses (RT#8045)
- Fix a heap use after free when moving a stack (RT#131954)
- Call ldconfig scriptlets using a macro

* Thu Feb 01 2018 Petr Pisar <ppisar@redhat.com> - 4:5.26.1-406
- Correct shell bangs in tests

* Mon Jan 29 2018 Petr Pisar <ppisar@redhat.com> - 4:5.26.1-405
- Link XS modules to pthread library to fix linking with -z defs

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 4:5.26.1-404
- Add patch to conditionalize a fix for an old and long fixed bug
  in libcrypt / glibc (rhbz#1536752)

* Mon Jan 15 2018 Petr Pisar <ppisar@redhat.com> - 4:5.26.1-403
- Rebuild against glibc without nsl library

* Tue Jan 09 2018 Petr Pisar <ppisar@redhat.com> - 4:5.26.1-402
- Remove invalid macro definitions from macros.perl (bug #1532539)
- Fix an overflow in the lexer when reading a new line (RT#131793)
- Fix Term::ReadLine not to create spurious &STDERR files (RT#132008)
- Fix a crash when a match for inversely repeated group fails (RT#132017)
- Fix an overflow when parsing a character range with no preceding character
  (RT#132245)
- Fix walking symbol table for ISA in Carp
- Fix handling file names with null bytes in stat and lstat functions
  (RT#131895)
- Fix a crash when untying an object witout a stash
- Fix deparsing of transliterations with unprintable characters (RT#132405)
- Fix error reporting on do() on a directory (RT#125774)
- Fix stack manipulation when a lexical subroutine is defined in a do block in
  a member of an iteration list (RT#132442)
- Fix setting $! when statting a closed file handle (RT#108288)
- Fix tainting of s/// with overloaded replacement (RT#115266)
- Expand system() arguments before a fork (RT#121105)
- Avoid undefined behavior when copying memory in Glob and pp_caller (RT#131746)

* Mon Sep 25 2017 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.26.1-401
- Update perl(:MODULE_COMPAT)

* Mon Sep 25 2017 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.26.1-400
- 5.26.1 bump (see <http://search.cpan.org/dist/perl-5.26.1/pod/perldelta.pod>
  for release notes)

* Tue Aug 22 2017 Petr Pisar <ppisar@redhat.com> - 4:5.26.0-399
- Fix unreliable Time-HiRes tests (CPAN RT#122819)
- Do not require $Config{libs} providers by perl-devel package (bug #1481324)

* Tue Aug 08 2017 Petr Pisar <ppisar@redhat.com> - 4:5.26.0-398
- Fix reporting malformed UTF-8 character (RT#131646)
- Fix File::Glob rt131211.t test random failures
- Fix t/op/hash.t test random failures
- Parse caret variables with subscripts as normal variables inside ${...}
  escaping (RT#131664)
- Do not display too many bytes when reporting malformed UTF-8 character
- Fix select called with a repeated magical variable (RT#131645)
- Fix error message for "our sub foo::bar" (RT#131679)
- Fix executing arybase::_tie_it() in Safe compartement (RT#131588)
- Fix handling attribute specification on our variables (RT#131597)
- Fix splitting non-ASCII strings if unicode_strings feature is enabled (RT#130907)
- Fix compiler warnings in code generated by ExtUtils::Constant
  (CPAN RT#63832, CPAN RT#101487)
- Fix GCC version detection for -D_FORTIFY_SOURCE override (RT#131809)

* Sat Jul 29 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4:5.26.0-397
- Enable separate debuginfo back

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4:5.26.0-396
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 28 2017 Petr Pisar <ppisar@redhat.com> - 4:5.26.0-395
- perl package installs all core modules, interpreter moved to
  perl-interpreter package, perl-core package is obsolete
  <https://fedoraproject.org/wiki/Changes/perl_Package_to_Install_Core_Modules>
  (bug #1464903)

* Mon Jun 19 2017 Petr Pisar <ppisar@redhat.com> - 4:5.26.0-394
- Make File::Glob more resistant against degenerative matching (RT#131211)
- Fix a crash when calling a subroutine from a stash (RT#131085)
- Fix an improper cast of a negative integer to an unsigned 8-bit type (RT#131190)
- Fix cloning :via handles on thread creation (RT#131221)
- Fix glob UTF-8 flag on a glob reassignment (RT#131263)
- Fix a buffer overflow in my_atof2() (RT#131526)
- Fix handling backslashes in PATH environment variable when executing
  "perl -S" (RT#129183)
- Fix a conditional jump on uninitilized memory in re_intuit_start() (RT#131575)
- Fix spurious "Assuming NOT a POSIX class" warning (RT#131522)
- Provide perl-interpreter RPM dependency symbol
  <https://fedoraproject.org/wiki/Changes/perl_Package_to_Install_Core_Modules>

* Tue Jun 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.26.0-393
- Stop providing old perl(MODULE_COMPAT_5.24.*)

* Thu Jun 01 2017 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.26.0-392
- 5.26.0 bump (see <http://search.cpan.org/dist/perl-5.26.0/pod/perldelta.pod>
  for release notes)
- Update sub-packages
- Update or remove patches
- Enable hardening (bug #1238804)
- Use 64 bit ints on 32 bit platforms (bug #1268828)

* Fri Mar 31 2017 Petr Pisar <ppisar@redhat.com> - 4:5.24.1-391
- Introduce build-conditions for groff, systemtap, syslog tests, and tcsh

* Wed Mar 08 2017 Petr Pisar <ppisar@redhat.com> - 4:5.24.1-390
- Fix a null-pointer dereference on malformed code (RT#130815)
- Fix an use-after-free in substr() that modifies a magic variable (RT#129340)
- Fix a memory leak leak in Perl_reg_named_buff_fetch() (RT#130822)
- Fix an invalid memory read when parsing a loop variable (RT#130814)
- Fix a heap-use-after-free in four-arguments substr call (RT#130624)

* Fri Feb 17 2017 Petr Pisar <ppisar@redhat.com> - 4:5.24.1-389
- Adapt Compress::Raw::Zlib to zlib-1.2.11 (bug #1420326)
- Fix a heap buffer overflow when evaluating regexps with embedded code blocks
  from more than one source (RT#129881)
- Fix a memory leak in list assignment from or to magic values (RT#130766)

* Fri Feb 10 2017 Petr Pisar <ppisar@redhat.com> - 4:5.24.1-388
- Adapt tests to zlib-1.2.11 (bug #1420326)
- Fix a crash when compiling a regexp with impossible quantifiers (RT#130561)
- Fix a buffer overrun with format and "use bytes" (RT#130703)
- Fix a buffer overflow when studying some regexps repeatedly
  (RT#129281, RT#129061)

* Thu Jan 26 2017 Petr Pisar <ppisar@redhat.com> - 4:5.24.1-387
- Fix UTF-8 string handling in & operator (RT#129287)
- Fix recreation of *:: (RT#129869)
- Fix a memory leak in B::RHE->HASH method (RT#130504)
- Fix parsing goto statements in multicalled subroutine (RT#113938)
- Fix a heap overlow in parsing $# (RT#129274)

* Fri Jan 20 2017 Petr Pisar <ppisar@redhat.com> - 4:5.24.1-386
- Fix a buffer overflow in split in scalar context (RT#130262)
- Fix a heap overflow with pack "W" (RT129149)
- Fix a use-after-free when processing scalar variables in forms (RT#129125)
- Fix a heap overflow if invalid octal or hexadecimal number is used in
  transliteration expression (RT#129342)
- Fix out-of-bound read in case of unmatched regexp backreference (RT#129377)

* Mon Jan 16 2017 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.24.1-385
- 5.24.1 bump (see <http://search.cpan.org/dist/perl-5.24.1/pod/perldelta.pod>
  for release notes)

* Thu Jan 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 4:5.24.0-384
- Rebuild for readline 7.x

* Fri Jan 06 2017 Petr Pisar <ppisar@redhat.com> - 4:5.24.0-383
- Remove bundled Math-BigInt-FastCalc (bug #1408463)
- Remove bundled Math-BigRat (bug #1408467)
- Remove bundled bignum (bug #1409585)

* Mon Dec 19 2016 Petr Pisar <ppisar@redhat.com> - 4:5.24.0-382
- Fix a crash in optimized evaluation of "or ((0) x 0))" (RT#130247)
- Fix a memory leak in IO::Poll (RT#129788)
- Fix regular expression matching (RT#130307)

* Thu Dec 01 2016 Petr Pisar <ppisar@redhat.com> - 4:5.24.0-381
- Fix crash in Storable when deserializing malformed code reference
  (RT#68348, RT#130098)
- Fix crash on explicit return from regular expression substitution (RT#130188)
- Tighten dependencies between architecture specific sub-packages to ISA
- Fix assigning split() return values to an array
- Fix const correctness in hv_func.h (bug #1242980)

* Wed Nov 09 2016 Petr Pisar <ppisar@redhat.com> - 4:5.24.0-380
- Tie perl-Errno release to interpreter build because of kernel version check
  (bug #1393421)

* Thu Nov 03 2016 Petr Pisar <ppisar@redhat.com> - 4:5.24.0-379
- Fix crash in "evalbytes S" (RT#129196)
- Fix crash in splice (RT#129164, RT#129166, RT#129167)
- Fix string overrun in Perl_gv_fetchmethod_pvn_flags (RT#129267)
- Fix crash when matching UTF-8 string with non-UTF-8 substrings (RT#129350)
- Fix parsing perl options in shell bang line (RT#129336)
- Fix firstchar bitmap under UTF-8 with prefix optimization (RT#129950)
- Avoid infinite loop in h2xs tool if enum and type have the same name
  (RT130001)
- Fix stack handling when calling chdir without an argument (RT#129130)

* Fri Sep 02 2016 Petr Pisar <ppisar@redhat.com> - 4:5.24.0-378
- perl-core depends on Parse::CPAN::Meta module instead of package name to allow
  upgrading perl-CPAN-Meta to 2.150010 (bug #1370681)

* Tue Aug 02 2016 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.24.0-377
- Avoid loading of modules from current directory, CVE-2016-1238, (bug #1360425)

* Thu Jul 28 2016 Petr Pisar <ppisar@redhat.com> - 4:5.24.0-376
- Fix handling \N{} in tr for characters in range 128--255 (RT#128734)

* Tue Jul 26 2016 Petr Pisar <ppisar@redhat.com> - 4:5.24.0-375
- Fix building without perl in the build root
- Own systemtap directories by perl-devel

* Tue Jul 12 2016 Petr Pisar <ppisar@redhat.com> - 4:5.24.0-374
- Fix a crash in lexical scope warnings (RT#128597)

* Fri Jul 08 2016 Petr Pisar <ppisar@redhat.com> - 4:5.24.0-373
- Fix a crash in "Subroutine redefined" warning (RT#128257)

* Thu Jul 07 2016 Petr Pisar <ppisar@redhat.com> - 4:5.24.0-372
- Fix a crash when vivifying a stub in a deleted package (RT#128532)

* Thu Jul 07 2016 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.24.0-371
- Do not let XSLoader load relative paths (CVE-2016-6185)

* Mon Jul 04 2016 Petr Pisar <ppisar@redhat.com> - 4:5.24.0-370
- Fix line numbers with perl -x (RT#128508)

* Fri Jun 24 2016 Petr Pisar <ppisar@redhat.com> - 4:5.24.0-369
- Do not crash when inserting a non-stash into a stash (RT#128238)

* Wed Jun 22 2016 Petr Pisar <ppisar@redhat.com> - 4:5.24.0-368
- Do not use unitialized memory in $h{\const} warnings (RT#128189)
- Fix precedence in hv_ename_delete (RT#128086)
- Do not treat %%: as a stash (RT#128238)

* Mon Jun 20 2016 Petr Pisar <ppisar@redhat.com> - 4:5.24.0-367
- Fix compiling regular expressions like /\X*(?0)/ (RT#128109)

* Thu Jun 16 2016 Petr Pisar <ppisar@redhat.com> - 4:5.24.0-366
- Do not mangle errno from failed socket calls (RT#128316)

* Tue Jun 14 2016 Petr Pisar <ppisar@redhat.com> - 4:5.24.0-365
- Fix a memory leak when compiling a regular expression with a POSIX class
  (RT#128313)

* Thu May 19 2016 Petr Pisar <ppisar@redhat.com> - 4:5.24.0-364
- Remove reflexive dependencies
- Use pregenerated dependencies on bootstrapping
- Specify more build-time dependencies

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.24.0-363
- Stop providing old perl(MODULE_COMPAT_5.22.*)
- Update license tags

* Wed May 11 2016 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.24.0-362
- 5.24.0 bump (see <http://search.cpan.org/dist/perl-5.24.0/pod/perldelta.pod>
  for release notes)
- Update sub-packages; Update or remove patches

* Mon May 02 2016 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.22.6-361
- 5.22.2 bump (see <http://search.cpan.org/dist/perl-5.22.2/pod/perldelta.pod>
  for release notes)

* Mon Apr 18 2016 Petr Pisar <ppisar@redhat.com> - 4:5.22.1-360
- Weak perl-Encode-devel dependency on perl-devel to Recommends level
  (bug #1129443)
- Remove perl-ExtUtils-ParseXS dependency on perl-devel (bug #1129443)
- Require perl-devel by perl-ExtUtils-MakeMaker
- Provide MM::maybe_command independently (bug #1129443)
- Replace ExtUtils::MakeMaker dependency with ExtUtils::MM::Utils in IPC::Cmd
  (bug #1129443)
- Remove perl-ExtUtils-Install dependency on perl-devel (bug #1129443)
- Remove perl-ExtUtils-Manifest dependency on perl-devel (bug #1129443)

* Tue Mar 15 2016 Petr Pisar <ppisar@redhat.com> - 4:5.22.1-359
- Do not filter FCGI dependency, CGI is non-core now

* Fri Mar 04 2016 Petr Pisar <ppisar@redhat.com> - 4:5.22.1-358
- Remove bundled perl-IPC-SysV (bug #1308527)

* Wed Mar 02 2016 Petr Pisar <ppisar@redhat.com> - 4:5.22.1-357
- Fix CVE-2016-2381 (ambiguous environment variables handling) (bug #1313702)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4:5.22.1-356
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Dec 15 2015 Petr Pisar <ppisar@redhat.com> - 4:5.22.1-355
- Remove bundled Math-BigInt (bug #1277203)

* Mon Dec 14 2015 Jitka Plesnikova <jplesnik@redhat.com> - 5.22.1-354
- 5.22.1 bump (see <http://search.cpan.org/dist/perl-5.22.1/pod/perldelta.pod>
  for release notes)

* Tue Oct 20 2015 Petr Pisar <ppisar@redhat.com> - 4:5.22.0-353
- Rebuild to utilize perl(:VERSION) dependency symbol

* Tue Oct 13 2015 Petr Pisar <ppisar@redhat.com> - 4:5.22.0-352
- Do not own IO::Socket::IP manual page by perl-IO

* Fri Oct 09 2015 Petr Pisar <ppisar@redhat.com> - 4:5.22.0-351
- Sub-package Attribute-Handlers
- Sub-package Devel-Peek
- Sub-package Devel-SelfStubber
- Sub-package SelfLoader
- Sub-package IO
- Sub-package Errno
- Correct perl-Digest-SHA dependencies
- Correct perl-Pod-Perldoc dependencies
- Move utf8 and dependencies to perl-libs
- Correct perl-devel and perl-CPAN dependencies
- Sub-package IPC-SysV
- Sub-package Test
- Sub-package utilities (splain) into perl-utils
- Provide perl version in perl(:VERSION) dependency symbol

* Fri Aug 07 2015 Petr Pisar <ppisar@redhat.com> - 4:5.22.0-350
- Sub-package Memoize
- Sub-package Net-Ping
- Sub-package Pod-Html

* Thu Jul 16 2015 Petr Pisar <ppisar@redhat.com> - 4:5.22.0-349
- Disable hardening due to some run-time failures (bug #1238804)

* Mon Jul 13 2015 Petr Pisar <ppisar@redhat.com> - 4:5.22.0-348
- Sub-package bignum
- Sub-package Math-BigRat
- Sub-package Math-BigInt-FastCalc
- Sub-package Math-Complex
- Remove bundled perl-Config-Perl-V (bug #1238203)
- Remove bundled perl-MIME-Base64 (bug #1238222)
- Remove bundled perl-PerlIO-via-QuotedPrint (bug #1238229)
- Remove bundled perl-Pod-Escapes (bug #1238237)
- Remove bundled perl-Term-Cap (bug #1238248)
- Remove bundled perl-Text-Balanced (bug #1238269)
- Remove bundled perl-libnet (bug #1238689)
- Remove bundled perl-perlfaq (bug #1238703)
- Remove bundled perl-Unicode-Normalize (bug #1238730)
- Remove bundled perl-Unicode-Collate (bug #1238760)

* Wed Jul 08 2015 Petr Pisar <ppisar@redhat.com> - 4:5.22.0-347
- Store distribution's linker and compiler flags to more Config's options
  in order to apply them when linking executable programs (bug #1238804)
- Sub-package Config-Perl-V (bug #1238203)
- Sub-package MIME-Base64 (bug #1238222)
- Sub-package PerlIO-via-QuotedPrint (bug #1238229)
- Update Pod-Escapes metadata (bug #1238237)
- Sub-package Term-Cap (bug #1238248)
- Sub-package Text-Balanced (bug #1238269)
- Sub-package libnet (bug #1238689)
- Sub-package perlfaq (bug #1238703)
- Sub-package Unicode-Normalize (bug #1238730)
- Sub-package Unicode-Collate (bug #1238760)
- Sub-package Math-BigInt
- Do not provide Net/libnet.cfg (bug #1238689)
- Revert downstream change in Net::Config default configuration
- Move libnetcfg tool from perl-devel into perl-libnetcfg sub-package

* Thu Jun 18 2015 Petr Pisar <ppisar@redhat.com> - 4:5.22.0-346
- Subpackage "open" module in order to keep deprecated "encoding" module
  optional (bug #1228378)
- Control building dual-lived sub-packages by perl_bootstrap macro
- Make PadlistNAMES() lvalue again (bug #1231165)
- Make magic vtable writable as a work-around for Coro (bug #1231165)
- Explain file break-down into RPM packages in perl package description

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4:5.22.0-345
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.22.0-244
- Stop providing old perl(MODULE_COMPAT_5.20.*)

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.22.0-243
- Move ok and Test::Use::ok to perl-Test-Simple

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.22.0-242
- Move bin/encguess to perl-Encode

* Mon Jun 01 2015 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.22.0-241
- 5.22.0 bump (see <http://search.cpan.org/dist/perl-5.22.0/pod/perldelta.pod>
  for release notes)
- Update sub-packages and erase the removed modules from the core
- Clean patches, not needed with new version
- Update patches to work with new version

* Wed Apr 15 2015 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.20.2-328
- Sub-package perl-CGI-Fast and perl-Module-Build-Deprecated
- Add missing dual-life modules to perl-core

* Thu Apr 02 2015 Petr Šabata <contyk@redhat.com> - 4:5.20.2-327
- Bump to make koji happy

* Thu Apr 02 2015 Petr Šabata <contyk@redhat.com> - 4:5.20.2-326
- Correct license tags of the main package, CGI, Compress-Raw-Zlib,
  Digest-MD5, Test-Simple and Time-Piece
- Package a Pod-Html license clarification email

* Wed Mar 25 2015 Petr Pisar <ppisar@redhat.com> - 4:5.20.2-325
- Sub-package Text-Tabs+Wrap (bug #910798)

* Thu Mar 19 2015 Lubomir Rintel <lkundrak@v3.sk> - 4:5.20.2-324
- Add systemtap probes for new dtrace markers

* Mon Mar 16 2015 Petr Pisar <ppisar@redhat.com> - 4:5.20.2-323
- Move perl(:MODULE_COMPAT_*) symbol and include directories to perl-libs
  package (bug #1174951)

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 4:5.20.2-322
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Wed Feb 18 2015 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.20.2-321
- Provide 5.20.2 MODULE_COMPAT
- Clean list of provided files
- Update names of changed patches

* Tue Feb 17 2015 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.20.2-320
- 5.20.2 bump (see <http://search.cpan.org/dist/perl-5.20.2/pod/perldelta.pod>
  for release notes)
- Regenerate a2p.c (BZ#1177672)

* Mon Feb 16 2015 Petr Pisar <ppisar@redhat.com> - 4:5.20.1-319
- Improve h2ph fix for GCC 5.0

* Thu Feb 12 2015 Petr Pisar <ppisar@redhat.com> - 4:5.20.1-318
- Fix regressions with GCC 5.0

* Tue Feb 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.20.1-317
- Sub-package inc-latest module

* Fri Jan 23 2015 Petr Pisar <ppisar@redhat.com> - 4:5.20.1-316
- Delete dual-living programs clashing on debuginfo files (bug #878863)

* Mon Dec 01 2014 Petr Pisar <ppisar@redhat.com> - 4:5.20.1-315
- Report inaccesible file on failed require (bug #1166504)
- Use stronger algorithm needed for FIPS in t/op/taint.t (bug #1128032)

* Wed Nov 19 2014 Petr Pisar <ppisar@redhat.com> - 4:5.20.1-314
- Consider Filter::Util::Call dependency as mandatory (bug #1165183)
- Sub-package encoding module
- Own upper directories by each package that installs a file there and
  remove empty directories (bug #1165013)

* Thu Nov 13 2014 Petr Pisar <ppisar@redhat.com> - 4:5.20.1-313
- Freeze epoch at perl-Pod-Checker and perl-Pod-Usage (bug #1163490)
- Remove bundled perl-ExtUtils-Command (bug #1158536)
- Remove bundled perl-Filter-Simple (bug #1158542)

* Wed Nov 12 2014 Petr Pisar <ppisar@redhat.com> - 4:5.20.1-312
- Do not double-own perl-Pod-Usage' and perl-Pod-Checker' files by
  perl-Pod-Parser on bootstrap
- Sub-package ExtUtils-Command (bug #1158536)
- Sub-package Filter-Simple (bug #1158542)
- Build-require groff-base instead of big groff

* Wed Oct 29 2014 Petr Pisar <ppisar@redhat.com> - 4:5.20.1-311
- Remove bundled perl-Devel-PPPort (bug #1143999)
- Remove bundled perl-B-Debug (bug #1142952)
- Remove bundled perl-ExtUtils-CBuilder (bug #1144033)
- Remove bundled perl-ExtUtils-Install (bug #1144068)

* Thu Oct 23 2014 Petr Pisar <ppisar@redhat.com> - 4:5.20.1-310
- Move all Module-CoreList files into perl-Module-CoreList
- Sub-package corelist(1) into perl-Module-CoreList-tools (bug #1142757)
- Remove bundled perl-Module-CoreList, and perl-Module-CoreList-tools
  (bug #1142757)
- Sub-package Devel-PPPort (bug #1143999)
- Sub-package B-Debug (bug #1142952)
- Use native version for perl-ExtUtils-CBuilder
- Specify all dependencies for perl-ExtUtils-Install (bug #1144068)
- Require perl-ExtUtils-ParseXS by perl-ExtUtils-MakeMaker because of xsubpp

* Tue Sep 16 2014 Petr Šabata <contyk@redhat.com> - 4:5.20.1-309
- Provide 5.20.0 MODULE_COMPAT

* Mon Sep 15 2014 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.20.1-308
- 5.20.1 bump (see <http://search.cpan.org/dist/perl-5.20.1/pod/perldelta.pod>
  for release notes)
- Sub-package perl-ExtUtils-Miniperl (bug #1141222)

* Wed Sep 10 2014 Petr Pisar <ppisar@redhat.com> - 4:5.20.0-307
- Specify all dependencies for perl-CPAN (bug #1090112)
- Disable non-core modules at perl-CPAN when bootstrapping
- Remove bundled perl-CPAN (bug #1090112)

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.20.0-306
- Stop providing old perl(MODULE_COMPAT_5.18.*)

* Mon Aug 18 2014 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.20.0-305
- Update to Perl 5.20.0
- Clean patches, not needed with new version
- Update patches to work with new version
- Update version of sub-packages, remove the deleted sub-packages
- Sub-package perl-IO-Socket-IP, perl-experimental
- Disable BR perl(local::lib) for cpan tool when bootstraping

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4:5.18.2-304
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 08 2014 Petr Pisar <ppisar@redhat.com> - 4:5.18.2-303
- Declare dependencies for cpan tool (bug #1122498)
- Use stronger algorithm needed for FIPS in t/op/crypt.t (bug #1128032)
- Make *DBM_File desctructors thread-safe (bug #1107543)

* Tue Jul 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.18.2-302
- Sub-package perl-Term-ANSIColor and remove it (bug #1121924)

* Fri Jun 27 2014 Petr Pisar <ppisar@redhat.com> - 4:5.18.2-301
- Remove bundled perl-App-a2p, perl-App-find2perl, perl-App-s2p, and
  perl-Package-Constants
- Correct perl-App-s2p license to ((GPL+ or Artistic) and App-s2p)

* Thu Jun 19 2014 Petr Pisar <ppisar@redhat.com> - 4:5.18.2-300
- Sub-package perl-App-find2perl (bug #1111196)
- Sub-package perl-App-a2p (bug #1111232)
- Sub-package perl-App-s2p (bug #1111242)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4:5.18.2-299
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 10 2014 Petr Pisar <ppisar@redhat.com> - 4:5.18.2-298
- Pass -fwrapv to stricter GCC 4.9 (bug #1082957)

* Fri Apr 04 2014 Petr Pisar <ppisar@redhat.com> - 4:5.18.2-297
- Fix t/comp/parser.t not to load system modules (bug #1084399)

* Mon Feb 03 2014 Petr Pisar <ppisar@redhat.com> - 4:5.18.2-296
- Move macro files into %%{_rpmconfigdir}/macros.d

* Wed Jan 29 2014 Petr Pisar <ppisar@redhat.com> - 4:5.18.2-295
- Provide perl(CPAN::Meta::Requirements) with six decimal places

* Tue Jan 21 2014 Petr Pisar <ppisar@redhat.com> - 4:5.18.2-294
- Drop perl-Test-Simple-tests package is it is not delivered by dual-lived
  version
- Hide dual-lived perl-Object-Accessor

* Tue Jan 14 2014 Petr Pisar <ppisar@redhat.com> - 4:5.18.2-293
- Use a macro to cover all 64-bit PowerPC architectures (bug #1052709)

* Tue Jan 14 2014 Petr Pisar <ppisar@redhat.com> - 4:5.18.2-292
- Use upstream patch to fix a test failure in perl5db.t when TERM=vt100

* Tue Dec 10 2013 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.18.2-291
- 5.18.2 bump (see <http://search.cpan.org/dist/perl-5.18.2/pod/perldelta.pod>
  for release notes)

* Mon Dec 02 2013 Petr Pisar <ppisar@redhat.com> - 4:5.18.1-290
- Document Math::BigInt::CalcEmu requires Math::BigInt (bug #959096)

* Tue Oct 22 2013 Petr Pisar <ppisar@redhat.com> - 4:5.18.1-289
- perl_default_filter macro does not need to filter private libraries from
  provides (bug #1020809)
- perl_default_filter anchors the filter regular expressions
- perl_default_filter appends the filters instead of redefining them

* Mon Sep 09 2013 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.18.1-288
- Fix rules for parsing numeric escapes in regexes (bug #978233)
- Fix crash with \&$glob_copy (bug #989486)
- Fix coreamp.t's rand test (bug #970567)
- Reap child in case where exception has been thrown (bug #988805)
- Fix using regexes with multiple code blocks (bug #982131)

* Tue Aug 13 2013 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.18.1-287
- 5.18.1 bump (see <http://search.cpan.org/dist/perl-5.18.1/pod/perldelta.pod>
  for release notes)
- Disable macro %%{rebuild_from_scratch}
- Fix regex seqfault 5.18 regression (bug #989921)
- Fixed interpolating downgraded variables into upgraded (bug #970913)
- SvTRUE returns correct value (bug #967463)
- Fixed doc command in perl debugger (bug #967461)
- Fixed unaligned access in slab allocator (bug #964950)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4:5.18.0-286
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Petr Pisar <ppisar@redhat.com> - 4:5.18.0-285
- Stop providing old perl(MODULE_COMPAT_5.16.*)

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 4:5.18.0-284
- Perl 5.18 rebuild

* Tue Jul 09 2013 Petr Pisar <ppisar@redhat.com> - 4:5.18.0-283
- Define SONAME for libperl.so and move the libary into standard path
- Link XS modules to libperl.so on Linux (bug #960048)

* Mon Jul 08 2013 Petr Pisar <ppisar@redhat.com> - 4:5.18.0-282
- Do not load system Term::ReadLine::Gnu while running tests
- Disable ornaments on perl5db AutoTrace tests

* Thu Jul 04 2013 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.18.0-281
- Update to Perl 5.18.0
- Clean patches, not needed with new version

* Wed Jun 26 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-280
- Edit local patch level before compilation

* Fri Jun 14 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-279
- Do not distribute File::Spec::VMS (bug #973713)
- Remove bundled CPANPLUS-Dist-Build (bug #973041)

* Wed Jun 12 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-278
- Update SystemTap scripts to recognize new phase__change marker and new probe
  arguments (bug #971094)
- Update h2ph(1) documentation (bug #948538)
- Update pod2html(1) documentation (bug #948538)
- Do not double-own archlib directory (bug #894195)

* Tue Jun 11 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-277
- Move CPANPLUS-Dist-Build files from perl-CPANPLUS
- Move CPAN-Meta-Requirements files from CPAN-Meta
- Add perl-Scalar-List-Utils to perl-core dependencies

* Thu Jun 06 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-276
- Require $Config{libs} providers (bug #905482)

* Thu May 30 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-275
- Correct typo in perl-Storable file list (bug #966865)
- Remove bundled Storable (bug #966865)

* Wed May 29 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-274
- Sub-package Storable (bug #966865)

* Mon May 13 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-273
- Use lib64 directories on aarch64 architecture (bug #961900)

* Fri May 10 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-272
- Make regular expression engine safe in a signal handler (bug #849703)
- Remove bundled ExtUtils-ParseXS, and Time-HiRes

* Fri Apr 26 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-271
- Sub-package Time-HiRes (bug #957048)
- Remove bundled Getopt-Long, Locale-Maketext, and Sys-Syslog

* Wed Apr 10 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-270
- Fix leaking tied hashes (bug #859910)
- Fix dead lock in PerlIO after fork from thread (bug #947444)
- Add proper conflicts to perl-Getopt-Long, perl-Locale-Maketext, and
  perl-Sys-Syslog

* Tue Apr 09 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-269
- Sub-package Sys-Syslog (bug #950057)

* Fri Apr 05 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-268
- Sub-package Getopt-Long (bug #948855)
- Sub-package Locale-Maketext (bug #948974)

* Fri Apr 05 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-267
- Remove bundled constant, DB_File, Digest-MD5, Env, Exporter, File-Path,
  File-Temp, Module-Load, Log-Message-Simple, Pod-Simple, Test-Harness,
  Text-ParseWords

* Mon Mar 25 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-266
- Filter provides from *.pl files (bug #924938)

* Fri Mar 22 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-265
- Conflict perl-autodie with older perl (bug #911226)
- Sub-package Env (bug #924619)
- Sub-package Exporter (bug #924645)
- Sub-package File-Path (bug #924782)
- Sub-package File-Temp (bug #924822)

* Thu Mar 21 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-264
- Sub-package constant (bug #924169)
- Sub-package DB_File (bug #924351)

* Tue Mar 19 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-263
- Correct perl-Digest-MD5 dependencies
- Remove bundled Archive-Extract, File-Fetch, HTTP-Tiny,
  Module-Load-Conditional, Time-Local

* Fri Mar 15 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-262
- Correct dependencies of perl-HTTP-Tiny
- Sub-package Time-Local (bug #922054)

* Thu Mar 14 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.3-261
- 5.16.3 bump (see <http://search.cpan.org/dist/perl-5.16.3/pod/perldelta.pod>
  for release notes)
- Remove bundled autodie, B-Lint, CPANPLUS, Encode, File-CheckTree, IPC-Cmd,
  Params-Check, Text-Soundex, Thread-Queue

* Tue Mar 05 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.2-260
- Fix CVE-2013-1667 (DoS in rehashing code) (bug #918008)

* Mon Feb 18 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.2-259
- Sub-package autodie (bug #911226)
- Add NAME headings to CPAN modules (bug #908113)

* Thu Feb 14 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.2-258
- Fix perl-Encode-devel dependency declaration

* Thu Feb 14 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.2-257
- Sub-package Thread-Queue (bug #911062)

* Wed Feb 13 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.2-256
- Sub-package File-CheckTree (bug #909144)
- Sub-package Text-ParseWords
- Sub-package Encode (bug #859149)

* Fri Feb 08 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.2-255
- Remove bundled Log-Message
- Remove bundled Term-UI

* Thu Feb 07 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.2-254
- Correct perl-podlators dependencies
- Obsolete perl-ExtUtils-Typemaps by perl-ExtUtils-ParseXS (bug #891952)

* Tue Feb 05 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.2-253
- Sub-package Pod-Checker and Pod-Usage (bugs #907546, #907550)

* Mon Feb 04 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.2-252
- Remove bundled PathTools

* Wed Jan 30 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.2-251
- Sub-package B-Lint (bug #906015)

* Wed Jan 30 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.2-250
- Sub-package Text-Soundex (bug #905889)
- Fix conflict declaration at perl-Pod-LaTeX (bug #904085)
- Remove bundled Module-Pluggable (bug #903624)

* Tue Jan 29 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.2-249
- Run-require POD convertors by Module-Build and ExtUtils-MakeMaker to
  generate documentation when building other packages

* Fri Jan 25 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.2-248
- Sub-package Pod-LaTeX (bug #904085)

* Wed Jan 16 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.2-247
- Remove bundled Pod-Parser

* Fri Jan 11 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.2-246
- Fix CVE-2012-6329 (misparsing of maketext strings) (bug #884354)

* Thu Jan 10 2013 Petr Pisar <ppisar@redhat.com> - 4:5.16.2-245
- Do not package App::Cpan(3pm) to perl-Test-Harness (bug #893768)

* Tue Dec 18 2012 Petr Pisar <ppisar@redhat.com> - 4:5.16.2-244
- Remove bundled Archive-Tar
- Remove bundled CPAN-Meta-YAML
- Remove bundled Module-Metadata

* Tue Dec 18 2012 Petr Pisar <ppisar@redhat.com> - 4:5.16.2-243
- Remove bundled Filter modules

* Mon Nov 05 2012 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.16.2-242
- 5.16.2 bump (see
  http://search.cpan.org/dist/perl-5.16.1/pod/perldelta.pod for release
  notes)

* Wed Oct 31 2012 Petr Pisar <ppisar@redhat.com> - 4:5.16.1-241
- Remove bundled podlators (bug #856516)

* Wed Oct 17 2012 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.16.1-240
- Do not crash when vivifying $| (bug #865296)

* Mon Sep 24 2012 Petr Pisar <ppisar@redhat.com> - 4:5.16.1-239
- Conflict perl-podlators with perl before sub-packaging (bug #856516)

* Fri Sep 21 2012 Petr Pisar <ppisar@redhat.com> - 4:5.16.1-238
- Do not leak with attribute on my variable (bug #858966)
- Allow operator after numeric keyword argument (bug #859328)
- Extend stack in File::Glob::glob (bug #859332)

* Thu Sep 20 2012 Petr Pisar <ppisar@redhat.com> - 4:5.16.1-237
- Put perl-podlators into perl-core list (bug #856516)

* Tue Sep 18 2012 Petr Pisar <ppisar@redhat.com> - 4:5.16.1-236
- Remove bundled perl-ExtUtils-Manifest
- perl-PathTools uses Carp

* Fri Sep 14 2012 Petr Pisar <ppisar@redhat.com> - 4:5.16.1-235
- Override the Pod::Simple::parse_file to set output to STDOUT by default
  (bug #826872)

* Wed Sep 12 2012 Petr Pisar <ppisar@redhat.com> - 4:5.16.1-234
- Sub-package perl-podlators (bug #856516)

* Tue Sep 11 2012 Petr Pisar <ppisar@redhat.com> - 4:5.16.1-233
- Do not access freed memory when cloning thread (bug #825749)
- Match non-breakable space with /[\h]/ in ASCII mode (bug #844919)
- Clear $@ before `do' I/O error (bug #834226)
- Do not truncate syscall() return value to 32 bits (bug #838551)

* Wed Sep 05 2012 Petr Pisar <ppisar@redhat.com> - 4:5.16.1-232
- Move App::Cpan from perl-Test-Harness to perl-CPAN (bug #854577)

* Fri Aug 24 2012 Petr Pisar <ppisar@redhat.com> - 4:5.16.1-231
- Remove perl-devel dependency from perl-Test-Harness and perl-Test-Simple

* Mon Aug 13 2012 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.16.0-230
- define perl_compat by macro for rebuilds
- sub-packages depend on compat rather than on nvr

* Thu Aug  9 2012 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.16.0-229
- apply conditionals for dual life patches

* Thu Aug 09 2012 Jitka Plesnikova <jplesnik@redhat.com> 4:5.16.1-228
- 5.16.1 bump (see
  http://search.cpan.org/dist/perl-5.16.1/pod/perldelta.pod for release
  notes)
- Fixed reopening by scalar handle (bug #834221)
- Fixed tr/// multiple transliteration (bug #831679)
- Fixed heap-overflow in gv_stashpv (bug #826516)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4:5.16.0-227
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jul 13 2012 Paul Howarth <paul@city-fan.org> 4:5.16.0-226
- Move the rest of ExtUtils-ParseXS into its sub-package, so that the main
  perl package doesn't need to pull in perl-devel (bug #839953)

* Mon Jul 02 2012 Jitka Plesnikova <jplesnik@redhat.com> 4:5.16.0-225
- Fix broken atof (bug #835452)

* Wed Jun 27 2012 Petr Pisar <ppisar@redhat.com> - 4:5.16.0-224
- perl-Pod-Perldoc must require groff-base because Pod::Perldoc::ToMan executes
  roff

* Mon Jun 25 2012 Petr Pisar <ppisar@redhat.com> - 4:5.16.0-223
- Test::Build requires Data::Dumper
- Sub-package perl-Pod-Parser

* Thu Jun 07 2012 Petr Pisar <ppisar@redhat.com> - 4:5.16.0-222
- Remove MODULE_COMPAT_5.14.* Provides

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 4:5.16.0-221
- Perl 5.16 rebuild

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 4:5.16.0-220
- perl_bootstrap macro is distributed in perl-srpm-macros now

* Fri Jun 01 2012 Petr Pisar <ppisar@redhat.com> - 4:5.16.0-219
- Own zipdetails and IO::Compress::FAQ by perl-IO-Compress

* Fri Jun  1 2012 Jitka Plesnikova <jplesnik@redhat.com> - 4:5.16.0-218
- Fix find2perl to translate ? glob properly (bug #825701)

* Thu May 31 2012 Petr Pisar <ppisar@redhat.com> - 4:5.16.0-218
- Shorten perl-Module-Build version to 2 digits to follow upstream

* Fri May 25 2012 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.16.0-217
- upload the stable 5.16.0

* Wed May 16 2012 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.16.0-RC2-217
- clean patches, not needed with new version
- regen by podcheck list of failed pods. cn, jp, ko pods failed. I can't decide
  whether it's a real problem or false positives.

* Mon Apr 30 2012 Petr Pisar <ppisar@redhat.com> - 4:5.14.2-216
- Enable usesitecustomize

* Thu Apr 19 2012 Petr Pisar <ppisar@redhat.com> - 4:5.14.2-215
- Rebuild perl against Berkeley database version 5 (bug #768846)

* Fri Apr 13 2012 Petr Pisar <ppisar@redhat.com> - 4:5.14.2-214
- perl-Data-Dumper requires Scalar::Util (bug #811239)

* Tue Apr 10 2012 Petr Pisar <ppisar@redhat.com> - 4:5.14.2-213
- Sub-package Data::Dumper (bug #811239)

* Tue Feb 21 2012 Petr Pisar <ppisar@redhat.com> - 4:5.14.2-212
- Sub-package Filter (bug #790349)

* Mon Feb 06 2012 Petr Pisar <ppisar@redhat.com> - 4:5.14.2-211
- Fix searching for Unicode::Collate::Locale data (bug #756118)
- Run safe signal handlers before returning from sigsuspend() and pause()
  (bug #771228)
- Correct perl-Scalar-List-Utils files list
- Stop !$^V from leaking (bug #787613)

* Tue Jan 10 2012 Paul Howarth <paul@city-fan.org> - 4:5.14.2-210
- Rebuild again now that perl dependency generator is fixed (#772632, #772699)

* Fri Jan 06 2012 Iain Arnell <iarnell@gmail.com> -4:5.14.2-209
- perl-ExtUtils-MakeMaker sub-package requires ExtUtils::Install

* Fri Jan  6 2012 Paul Howarth <paul@city-fan.org> - 4:5.14.2-208
- Rebuild for gcc 4.7

* Tue Dec 20 2011 Petr Pisar <ppisar@redhat.com> - 4:5.14.2-207
- Fix interrupted reading. Thanks to Šimon Lukašík for reporting this issue
  and thanks to Marcela Mašláňová for finding fix. (bug #767931)

* Wed Dec 14 2011 Petr Pisar <ppisar@redhat.com> - 4:5.14.2-206
- Fix leak with non-matching named captures (bug #767597)

* Tue Nov 29 2011 Petr Pisar <ppisar@redhat.com> - 4:5.14.2-205
- Sub-package ExtUtils::Install
- Sub-package ExtUtils::Manifest
- Do not provide private perl(ExtUtils::MakeMaker::_version)

* Thu Nov 24 2011 Ville Skyttä <ville.skytta@iki.fi> - 4:5.14.2-204
- Add $RPM_LD_FLAGS to lddlflags.

* Wed Nov 23 2011 Petr Pisar <ppisar@redhat.com> - 4:5.14.2-203
- Sub-package Socket

* Mon Nov 21 2011 Petr Pisar <ppisar@redhat.com> - 4:5.14.2-202
- Sub-package Pod::Perldoc

* Fri Nov 18 2011 Petr Pisar <ppisar@redhat.com> - 4:5.14.2-201
- Increase epoch of perl-Module-CoreList to overcome version regression in
  upstream (bug #754641)

* Thu Nov  3 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.14.2-200
- perl(DBIx::Simple) is not needed in spec requirement in CPANPLUS. It's generated
  automatically.

* Wed Nov 02 2011 Petr Pisar <ppisar@redhat.com> - 4:5.14.2-199
- Provide perl(DB) by perl

* Mon Oct 24 2011 Petr Pisar <ppisar@redhat.com> - 4:5.14.2-198
- Do not warn about missing site directories (bug #732799)

* Thu Oct 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.14.2-197
- cleaned spec (thanks to Grigory Batalov)
-  Module-Metadata sub-package contained perl_privlib instead of privlib
-  %%files parent section was repeated twice

* Fri Oct 14 2011 Petr Pisar <ppisar@redhat.com> - 4:5.14.2-196
- Filter false perl(DynaLoader) provide from perl-ExtUtils-MakeMaker
  (bug #736714)
- Change Perl_repeatcpy() prototype to allow repeat count above 2^31
  (bug #720610)
- Do not own site directories located in /usr/local (bug #732799)

* Tue Oct 04 2011 Petr Pisar <ppisar@redhat.com> - 4:5.14.2-195
- Fix CVE-2011-3597 (code injection in Digest) (bug #743010)
- Sub-package Digest and thus Digest::MD5 module (bug #743247)

* Tue Oct 04 2011 Iain Arnell <iarnell@gmail.com> 4:5.14.2-194
- add provide for perl(:MODULE_COMPAT_5.14.2)

* Mon Oct 03 2011 Petr Pisar <ppisar@redhat.com> - 4:5.14.2-193
- 5.14.2 bump (see
  https://metacpan.org/module/FLORA/perl-5.14.2/pod/perldelta.pod for release
  notes).
- Fixes panics when processing regular expression with \b class and /aa
  modifier (bug #731062)
- Fixes CVE-2011-2728 (File::Glob bsd_glob() crash with certain glob flags)
  (bug #742987)

* Mon Oct 03 2011 Petr Pisar <ppisar@redhat.com> - 4:5.14.1-192
- Enable GDBM support again to build against new gdbm 1.9.1

* Fri Sep 30 2011 Petr Pisar <ppisar@redhat.com> - 4:5.14.1-191
- Disable NDBM support temporarily too as it's provided by gdbm package

* Wed Sep 21 2011 Petr Pisar <ppisar@redhat.com> - 4:5.14.1-190
- Disable GDBM support temporarily to build new GDBM

* Thu Sep 15 2011 Petr Pisar <ppisar@redhat.com> - 4:5.14.1-189
- Correct perl-CGI list of Provides
- Make tests optional
- Correct perl-ExtUtils-ParseXS Provides
- Correct perl-Locale-Codes Provides
- Correct perl-Module-CoreList version
- Automate perl-Test-Simple-tests Requires version

* Tue Sep 13 2011 Petr Pisar <ppisar@redhat.com> - 4:5.14.1-188
- Make gdbm support optional to bootstrap with new gdbm
- Split Carp into standalone sub-package to dual-live with newer versions
  (bug #736768)

* Tue Aug 30 2011 Petr Pisar <ppisar@redhat.com> - 4:5.14.1-187
- Split Locale::Codes into standalone sub-package to dual-live with newer
  versions (bug #717863)

* Sun Aug 14 2011 Iain Arnell <iarnell@gmail.com> 4:5.14.1-186
- perl needs to own vendorarch/auto directory

* Fri Aug 05 2011 Petr Sabata <contyk@redhat.com> - 4:5.14.1-185
- Move xsubpp to ExtUtils::ParseXS (#728393)

* Fri Jul 29 2011 Iain Arnell <iarnell@gmail.com> 4:5.14.1-184
- fix Compress-Raw-Bzip2 pacakging
- ensure that we never bundle bzip2 or zlib

* Tue Jul 26 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.14.1-183
- remove from provides MODULE_COMPAT 5.12.*

* Fri Jul 22 2011 Paul Howarth <paul@city-fan.org> - 4:5.14.1-182
- Have perl-Module-Build explicitly require perl(CPAN::Meta) >= 2.110420,
  needed for creation of MYMETA files by Build.PL; the dual-life version of
  the package already has this dependency

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 4:5.14.1-181
- Temporarily provide 5.12.* MODULE_COMPAT

* Sat Jul 16 2011 Iain Arnell <iarnell@gmail.com> 4:5.14.1-180
- fix escaping of the __provides_exclude_from macro

* Wed Jul 13 2011 Iain Arnell <iarnell@gmail.com> 4:5.14.1-179
- Parse-CPAN-Meta explicitly requires CPAN::Meta::YAML and JSON::PP
- Exclude CPAN::Meta* from CPAN sub-package
- Don't try to normalize CPAN-Meta, JSON-PP, and Parse-CPAN-Meta versions;
  their dual-life packages aren't and have much higher numbers already

* Mon Jun 27 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.14.1-178
- update macros -> add %%perl_bootstrap 1 and example for readability
- add into Module::Build dependency on perl-devel (contains macros.perl)
- create new sub-package macros, because we need macros in minimal buildroot

* Thu Jun 23 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.14.1-175
- remove from macros BSD, because there exists BSD::Resources

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.14.1-174
- remove old MODULE_COMPATs

* Mon Jun 20 2011 Iain Arnell <iarnell@gmail.com> 4:5.14.1-173
- move ptargrep to Archive-Tar sub-package
- fix version numbers in last two changelog entries

* Mon Jun 20 2011 Paul Howarth <paul@city-fan.org> - 4:5.14.1-172
- add provide for perl(:MODULE_COMPAT_5.14.1)

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.14.1-171
- update to 5.14.1 - no new modules, just serious bugfixes and doc
- switch off fork test, which is failing only on koji

* Thu Jun 16 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.14.0-170
- try to update to latest ExtUtils::MakeMaker, no luck -> rebuild with current 
  version, fix bug RT#67618 in modules

* Wed Jun 15 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.14.0-169
- filter even Mac:: requires, polish filter again for correct installation
- add sub-package Compress-Raw-Bzip2, solve Bzip2 conflicts after install
- and add IO::Uncompress::Bunzip2 correctly into IO-Compress

* Mon Jun 13 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.14.0-167
- Perl 5.14 mass rebuild, bump release, remove releases in subpackages

* Thu Jun 09 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.14.0-165
- Perl 5.14 mass rebuild

* Thu Jun 09 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.14.0-163
- Perl 5.14 mass rebuild

* Thu Jun  9 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.14.0-162
- add new sub-packages, remove BR in them

* Wed Jun  1 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.14.0-161
- arm can't do parallel builds
- add require EE::MM into IPC::Cmd 711486

* Mon May 16 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.14.0-161
- test build of released 5.14.0
- remove Class::ISA from sub-packages
- patches 8+ are part of new release
- remove vendorarch/auto/Compress/Zlib

* Wed Apr 13 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.3-160
- add provides UNIVERSAL and DB back into perl

* Thu Apr 07 2011 Petr Pisar <ppisar@redhat.com> - 4:5.12.3-159
- Remove rpath-make patch because we use --enable-new-dtags linker option

* Fri Apr  1 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.3-158
- 692900 - lc launders tainted flag, RT #87336

* Fri Apr  1 2011 Robin Lee <cheeselee@fedoraproject.org> - 4:5.12.3-157
- Cwd.so go to the PathTools sub-package

* Tue Mar 15 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.3-156
- sub-package Path-Tools

* Sat Feb 19 2011 Iain Arnell <iarnell@gmail.com> 4:5.12.3-154
- sub-package Scalar-List-Utils

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4:5.12.3-153
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 27 2011 Petr Pisar <ppisar@redhat.com> - 4:5.12.3-152
- Document ExtUtils::ParseXS upgrade in local patch tracking

* Wed Jan 26 2011 Tom Callaway <spot@fedoraproject.org> - 4:5.12.3-151
- update ExtUtils::ParseXS to 2.2206 (current) to fix Wx build

* Wed Jan 26 2011 Petr Pisar <ppisar@redhat.com> - 4:5.12.3-150
- Make %%global perl_default_filter lazy
- Do not hard-code tapsetdir path

* Tue Jan 25 2011 Lukas Berk <lberk@redhat.com> - 4:5.12.3-149
- added systemtap tapset to make use of systemtap-sdt-devel
- added an example systemtap script

* Mon Jan 24 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.3-148
- stable update 5.12.3
- add COMPAT

* Thu Dec  9 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.2-146
- 463773 revert change. txt files are needed for example by UCD::Unicode,
 PDF::API2,...

* Thu Dec  9 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.2-145
- required systemtap-sdt-devel on request in 661553

* Mon Nov 29 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.2-144
- create sub-package for CGI 3.49

* Tue Nov 09 2010 Petr Pisar <ppisar@redhat.com> - 4:5.12.2-143
- Sub-package perl-Class-ISA (bug #651317)

* Mon Nov 08 2010 Petr Pisar <ppisar@redhat.com> - 4:5.12.2-142
- Make perl(ExtUtils::ParseXS) version 4 digits long (bug #650882)

* Tue Oct 19 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.2-141
- 643447 fix redefinition of constant C in h2ph (visible in git send mail,
  XML::Twig test suite)
- remove ifdef for s390

* Thu Oct 07 2010 Petr Pisar <ppisar@redhat.com> - 4:5.12.2-140
- Package Test-Simple tests to dual-live with standalone package (bug #640752)
 
* Wed Oct  6 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.2-139
- remove removal of NDBM

* Tue Oct 05 2010 Petr Pisar <ppisar@redhat.com> - 4:5.12.2-138
- Consolidate Requires filtering
- Consolidate libperl.so* Provides

* Fri Oct  1 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.2-137
- filter useless requires, provide libperl.so

* Fri Oct 01 2010 Petr Pisar <ppisar@redhat.com> - 4:5.12.2-136
- Reformat perl-threads description
- Fix threads directories ownership

* Thu Sep 30 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.2-135
- sub-package threads

* Thu Sep 23 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.2-134
- add vendor path, clean paths in Configure in spec file
- create sub-package threads-shared

* Tue Sep  7 2010 Petr Pisar <ppisar@redhat.com> - 4:5.12.2-133
- Do not leak when destroying thread (RT #77352, RHBZ #630667)

* Tue Sep  7 2010 Petr Sabata <psabata@redhat.com> - 5:5.12.2-132
- Fixing release number for modules

* Tue Sep  7 2010 Petr Sabata <psabata@redhat.com> - 4:5.12.2-1
- Update to 5.12.2
- Removed one hardcoded occurence of perl version in build process
- Added correct path to dtrace binary
- BuildRequires: systemtap-sdt-devel

* Tue Sep  7 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.1-131
- run Configure with -Dusedtrace for systemtap support

* Wed Aug 18 2010 Petr Pisar <ppisar@redhat.com> - 4:5.12.1-130
- Run tests in parallel
- Add "-Wl,--enable-new-dtags" to linker to allow to override perl's rpath by
  LD_LIBRARY_PATH used in tests. Otherwise tested perl would link to old
  in-system libperl.so.
- Normalize spec file indentation

* Mon Jul 26 2010  Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.1-129
- 617956 move perlxs* docs files into perl-devel

* Thu Jul 15 2010  Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.1-128
- 614662 wrong perl-suidperl version in obsolete

* Sun Jul 11 2010 Dan Horák <dan[at]danny.cz> - 4:5.12.1-127
- add temporary compat provides needed on s390(x)

* Fri Jul 09 2010 Petr Pisar <ppisar@redhat.com> - 4:5.12.1-126
- Add Digest::SHA requirement to perl-CPAN and perl-CPANPLUS (bug #612563)

* Thu Jul  8 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.1-125
- 607505 add another dir into Module::Build (thanks to Paul Howarth)

* Mon Jun 28 2010 Ralf Corsépius <corsepiu@fedoraproject.org> -  4:5.12.1-124
- Address perl-Compress-Raw directory ownership (BZ 607881).

* Thu Jun 10 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.1-123
- remove patch with debugging symbols, which should be now ok without it
- update to 5.12.1
- MODULE_COMPAT

* Tue Apr 27 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.0-122
- packages in buildroot needs MODULE_COMPAT 5.10.1, add it back for rebuild

* Sun Apr 25 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.0-121
- rebuild with tests in test buildroot

* Fri Apr 23 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.0-120-test
- MODULE_COMPAT 5.12.0
- remove BR man
- clean configure
- fix provides/requires in IO-Compress

* Wed Apr 14 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.0-119.1
- rebuild 5.12.0 without MODULE_COMPAT

* Wed Apr 14 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.12.0-119
- initial 5.12.0 build

* Tue Apr  6 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.10.1-118
- 463773 remove useless txt files from installation
- 575842 remove PERL_USE_SAFE_PUTENV, use perl putenv

* Tue Mar 16 2010 Chris Weyl <cweyl@alumni.drew.edu> - 4:5.10.1-117
- package tests in their own subpackage

* Mon Mar 15 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.10.1-116
- add noarch into correct sub-packages
- move Provides/Obsoletes into correct modules from main perl

* Thu Mar 11 2010 Paul Howarth <paul@city-fan.org> - 4:5.10.1-115
- restore missing version macros for Compress::Raw::Zlib, IO::Compress::Base
  and IO::Compress::Zlib

* Thu Mar 11 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.10.1-114
- clean spec a little more
- rebuild with new gdbm

* Fri Mar  5 2010 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.10.1-112
- fix license according to advice from legal
- clean unused patches

* Wed Feb 24 2010 Chris Weyl <cweyl@alumni.drew.edu> - 4:5.10.1-111
- update subpackage tests macros to handle packages with an epoch properly

* Fri Feb 05 2010 Chris Weyl <cweyl@alumni.drew.edu> - 4:5.10.1-110
- add initial EXPERIMENTAL tests subpackage rpm macros to macros.perl

* Tue Dec 22 2009 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.10.1-109
- 547656 CVE-2009-3626 perl: regexp matcher crash on invalid UTF-8 characters  
- 549306 version::Internals should be packaged in perl-version subpackage
- Parse-CPAN-Meta updated and separate package is dead

* Mon Dec 21 2009 Chris Weyl <cweyl@alumni.drew.edu> - 4:5.10.1-107
- subpackage parent and Parse-CPAN-Meta; add them to core's dep list

* Fri Dec 18 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 4:5.10.1-106
- exclude "parent".

* Fri Dec 18 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 4:5.10.1-105
- exclude Parse-CPAN-Meta.

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.1-104
- do not pack Bzip2 manpages either (#544582)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.1-103
- do not pack Bzip2 modules (#544582)
- hack: cheat about Compress::Raw::Zlib version (#544582)

* Thu Dec  3 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.1-102
- switch off check for ppc64 and s390x
- remove the hack for "make test," it is no longer needed

* Thu Dec  3 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.1-101
- be more careful with the libperl.so compatibility symlink (#543936)

* Wed Dec  2 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.1-100
- new upstream version
- release number must be high, because of stale version numbers of some
  of the subpackages
- drop upstreamed patches
- update the versions of bundled modules
- shorten the paths in @INC
- build without DEBUGGING
- implement compatibility measures for the above two changes, for a short
  transition period
- provide perl(:MODULE_COMPAT_5.10.0), for that transition period only

* Tue Dec  1 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.0-87
- fix patch-update-Compress-Raw-Zlib.patch (did not patch Zlib.pm)
- update Compress::Raw::Zlib to 2.023
- update IO::Compress::Base, and IO::Compress::Zlib to 2.015 (#542645)

* Mon Nov 30 2009 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.10.0-86
- 542645 update IO-Compress-Base

* Tue Nov 24 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.0-85
- back out perl-5.10.0-spamassassin.patch (#528572)

* Thu Oct 01 2009 Chris Weyl <cweyl@alumni.drew.edu> - 4:5.10.0-84
- add /perl(UNIVERSAL)/d; /perl(DB)/d to perl_default_filter auto-provides
  filtering

* Thu Oct  1 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.0-83
- update Storable to 2.21

* Mon Aug 31 2009 Chris Weyl <cweyl@alumni.drew.edu> - 4:5.10.0-82
- update our Test-Simple update to 0.92 (patch by Iain Arnell), #519417
- update Module-Pluggable to 3.9

* Thu Aug 27 2009 Chris Weyl <cweyl@alumni.drew.edu> - 4:5.10.0-81
- fix macros.perl *sigh*

* Mon Aug 24 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.0-80
- Remove -DDEBUGGING=-g, we are not ready yet.

* Fri Aug 21 2009 Chris Weyl <cweyl@alumni.drew.edu> - 4:5.10.0-79
- add helper filtering macros to -devel, for perl-* package invocation
  (#502402)

* Fri Jul 31 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.0-78
- Add configure option -DDEBUGGING=-g (#156113)

* Tue Jul 28 2009 arcela Mašláňová <mmaslano@redhat.com> - 4:5.10.0-77
- 510127 spam assassin suffer from tainted bug

* Mon Jul 27 2009 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.10.0-76
- 494773 much better swap logic to support reentrancy and fix assert failure (rt #60508)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4:5.10.0-75
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 10 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.0-74
- fix generated .ph files so that they no longer cause warnings (#509676)
- remove PREREQ_FATAL from Makefile.PL's processed by miniperl
- update to latest Scalar-List-Utils (#507378)
- perl-skip-prereq.patch: skip more prereq declarations in Makefile.PL files

* Tue Jul  7 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.0-73
- re-enable tests

* Tue Jul  7 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.0-72
- move -DPERL_USE_SAFE_PUTENV to ccflags (#508496)

* Mon Jun  8 2009 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.10.0-71
- #504386 update of Compress::Raw::Zlib 2.020

* Thu Jun  4 2009 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.10.0-70
- update File::Spec (PathTools) to 3.30

* Wed Jun  3 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.0-69
- fix #221113, $! wrongly set when EOF is reached

* Fri Apr 10 2009 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.10.0-68
- do not use quotes in patchlevel.h; it breaks installation from cpan (#495183)

* Tue Apr  7 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.0-67
- update CGI to 3.43, dropping upstreamed perl-CGI-escape.patch

* Tue Apr  7 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.0-66
- fix CGI::escape for all strings (#472571)
- perl-CGI-t-util-58.patch: Do not distort lib/CGI/t/util-58.t
  http://rt.perl.org/rt3/Ticket/Display.html?id=64502

* Fri Mar 27 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.0-65
- Move the gargantuan Changes* collection to -devel (#492605)

* Tue Mar 24 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.0-64
- update module autodie

* Mon Mar 23 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.0-63
- update Digest::SHA (fixes 489221)

* Wed Mar 11 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 4:5.10.0-62
- drop 26_fix_pod2man_upgrade (don't need it)
- fix typo in %%define ExtUtils_CBuilder_version

* Wed Mar 11 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 4:5.10.0-61
- apply Change 34507: Fix memory leak in single-char character class optimization
- Reorder @INC, based on b9ba2fadb18b54e35e5de54f945111a56cbcb249
- fix Archive::Extract to fix test failure caused by tar >= 1.21
- Merge useful Debian patches

* Tue Mar 10 2009 Stepan Kasal <skasal@redhat.com> - 4:5.10.0-60
- remove compatibility obsolete sitelib directories
- use a better BuildRoot
- drop a redundant mkdir in %%install
- call patchlevel.h only once; rm patchlevel.bak
- update modules Sys::Syslog, Module::Load::Conditional, Module::CoreList,
  Test::Harness, Test::Simple, CGI.pm (dropping the upstreamed patch),
  File::Path (that includes our perl-5.10.0-CVE-2008-2827.patch),
  constant, Pod::Simple, Archive::Tar, Archive::Extract, File::Fetch,
  File::Temp, IPC::Cmd, Time::HiRes, Module::Build, ExtUtils::CBuilder
- standardize the patches for updating embedded modules
- work around a bug in Module::Build tests bu setting TMPDIR to a directory
  inside the source tree

* Sun Mar 08 2009 Robert Scheck <robert@fedoraproject.org> - 4:5.10.0-59
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 16 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 4:5.10.0-58
- add /usr/lib/perl5/site_perl to otherlibs (bz 484053)

* Mon Feb 16 2009 Dennis Gilmore <dennis@ausil.us> - 4:5.10.0-57
- build sparc64 without _smp_mflags

* Sat Feb 07 2009 Dennis Gilmore <dennis@ausil.us> - 4:5.10.0-56
- limit sparc builds to -j12

* Tue Feb  3 2009 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.10.0-55
- update IPC::Cmd to v 0.42

* Mon Jan 19 2009 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.10.0-54
- 455410 http://rt.perl.org/rt3/Public/Bug/Display.html?id=54934
  Attempt to free unreferenced scalar fiddling with the symbol table
  Keep the refcount of the globs generated by PerlIO::via balanced.

* Mon Dec 22 2008 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.10.0-53
- add missing XHTML.pm into Pod::Simple

* Fri Dec 12 2008 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.10.0-52
- 295021 CVE-2007-4829 perl-Archive-Tar directory traversal flaws
- add another source for binary files, which test untaring links

* Fri Nov 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 4:5.10.0-51
- to fix Fedora bz 473223, which is really perl bug #54186 (http://rt.perl.org/rt3//Public/Bug/Display.html?id=54186)
  we apply Changes 33640, 33881, 33896, 33897

* Mon Nov 24 2008 Marcela Mašláňová <mmaslano@redhat.com> - 4:5.10.0-50
- change summary according to RFC fix summary discussion at fedora-devel :)

* Thu Oct 23 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 4:5.10.0-49
- update File::Temp to 0.20

* Sun Oct 12 2008 Lubomir Rintel <lkundrak@v3.sk> - 4:5.10.0-48
- Include fix for rt#52740 to fix a crash when using Devel::Symdump and
  Compress::Zlib together

* Tue Oct 07 2008 Marcela Mašláňová <mmaslano@redhat.com> 4:5.10.0-47.fc10
- rt#33242, rhbz#459918. Segfault after reblessing objects in Storable.
- rhbz#465728 upgrade Simple::Pod to 3.07

* Wed Oct  1 2008 Stepan Kasal <skasal@redhat.com> - 4:5.10.0-46
- also preserve the timestamp of AUTHORS; move the fix to the recode
  function, which is where the stamps go wrong

* Wed Oct  1 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4:5.10.0-45
- give Changes*.gz the same datetime to avoid multilib conflict

* Wed Sep 17 2008 Marcela Maslanova <mmaslano@redhat.com> 4:5.10.0-44.fc10
- remove Tar.pm from Archive-Extract
- fix version of Test::Simple in spec
- update Test::Simple
- update Archive::Tar to 1.38

* Tue Sep 16 2008 Marcela Maslanova <mmaslano@redhat.com> 4:5.10.0-43.fc10
- 462444 update Test::Simple to 0.80

* Thu Aug 14 2008 Stepan Kasal <skasal@redhat.com> - 4:5.10.0-42.fc10
- move libnet to the right directory, along Net/Config.pm

* Wed Aug 13 2008 Stepan Kasal <skasal@redhat.com> - 4:5.10.0-41.fc10
- do not create directory .../%%{version}/auto

* Tue Aug  5 2008 Marcela Maslanova <mmaslano@redhat.com> 4:5.10.0-40.fc10
- 457867 remove required IPC::Run from CPANPLUS - needed only by win32
- 457771 add path

* Fri Aug  1 2008 Stepan Kasal <skasal@redhat.com> 4:5.10.0-39.fc10
- CGI.pm bug in exists() on tied param hash (#457085)
- move the enc2xs templates (../Encode/*.e2x) to -devel, (#456534)

* Mon Jul 21 2008 Marcela Maslanova <mmaslano@redhat.com> 4:5.10.0-38
- 455933 update to CGI-3.38
- fix fuzz problems (patch6)
- 217833 pos() function handle unicode characters correct

* Thu Jul 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4:5.10.0-36
- rebuild for new db4 4.7

* Wed Jul  9 2008 Stepan Kasal <skasal@redhat.com> 4:5.10.0-35
- remove db4 require, it is handled automatically

* Thu Jul  3 2008 Stepan Kasal <skasal@redhat.com> 4:5.10.0-34
- 453646 use -DPERL_USE_SAFE_PUTENV. Without fail some modules f.e. readline.

* Tue Jul  1 2008 Marcela Maslanova <mmaslano@redhat.com> 4:5.10.0-33
- 451078 update Test::Harness to 3.12 for more testing. Removed verbose 
test, new Test::Harness has possibly verbose output, but updated package
has a lot of features f.e. TAP::Harness. Carefully watched all new bugs 
related to tests!

* Fri Jun 27 2008 Stepan Kasal <skasal@redhat.com> 4:5.10.0-32
- bump the release number, so that it is not smaller than in F-9

* Tue Jun 24 2008 Marcela Maslanova <mmaslano@redhat.com> 4:5.10.0-28
- CVE-2008-2827 perl: insecure use of chmod in rmtree

* Wed Jun 11 2008 Marcela Maslanova <mmaslano@redhat.com> 4:5.10.0-27
- 447371 wrong access permission rt49003

* Tue Jun 10 2008 Stepan Kasal <skasal@redhat.com> 4:5.10.0-26
- make config parameter list consistent for 32bit and 64bit platforms,
  add config option -Dinc_version_list=none (#448735)
- use perl_archname consistently
- cleanup of usage of *_lib macros in %%install

* Fri Jun  6 2008 Marcela Maslanova <mmaslano@redhat.com> 4:5.10.0-25
- 449577 rebuild for FTBFS

* Mon May 26 2008 Marcela Maslanova <mmaslano@redhat.com> 4:5.10.0-24
- 448392 upstream fix for assertion

* Thu May 22 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4:5.10.0-23
- sparc64 breaks with the rpath hack patch applied

* Mon May 19 2008 Marcela Maslanova <mmaslano@redhat.com>
- 447142 upgrade CGI to 3.37 (this actually happened in -21 in rawhide.)

* Sat May 17 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4:5.10.0-21
- sparc64 fails two tests under mysterious circumstances. we need to get the
  rest of the tree moving, so we temporarily disable the tests on that arch.

* Tue Mar 18 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4:5.10.0-20
- create the vendor_perl/%%{perl_version}/%%{perl_archname}/auto directory 
  in %%{_libdir} so we own it properly

* Tue Mar 18 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4:5.10.0-19
- fix CPANPLUS-Dist-Build Provides/Obsoletes (bz 437615)
- bump version on Module-CoreList subpackage

* Tue Mar 18 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4:5.10.0-18
- forgot to create the auto directory for multilib vendor_perl dirs

* Tue Mar 18 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4:5.10.0-17
- own multilib vendor_perl directories
- mark Module::CoreList patch in patchlevel.h

* Tue Mar 18 2008 Marcela Maslanova <mmaslano@redhat.com> 4:5.10.0-16
- 437817: RFE: Upgrade Module::CoreList to 2.14

* Wed Mar 12 2008 Marcela Maslanova <mmaslano@redhat.com> 4:5.10.0-15
- xsubpp now lives in perl-devel instead of perl.

* Sat Mar  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4:5.10.0-14
- back out Archive::Extract patch, causing odd test failure

* Sat Mar  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4:5.10.0-13
- add missing lzma test file

* Fri Mar  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4:5.10.0-12
- conditionalize multilib patch report in patchlevel.h
- Update Archive::Extract to 0.26
- Update Module::Load::Conditional to 0.24

* Fri Mar  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4:5.10.0-11
- only do it once, and do it for all our patches

* Fri Mar  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4:5.10.0-10
- note 32891 in patchlevel.h

* Fri Mar  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4:5.10.0-9
- get rid of bad conflicts on perl-File-Temp

* Fri Mar  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4:5.10.0-8
- use /usr/local for sitelib/sitearch dirs
- patch 32891 for significant performance improvement

* Fri Feb 22 2008 Stepan Kasal <skasal@redhat.com> - 4:5.10.0-7
- Add perl-File-Temp provides/obsoletes/conflicts (#433836),
  reported by Bill McGonigle <bill@bfccomputing.com>
- escape the macros in Jan 30 entry

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 4:5.10.0-6
- Autorebuild for GCC 4.3

* Wed Jan 30 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 4:5.10.0-5
- disable some futime tests in t/io/fs.t because they started failing on x86_64
  in the Fedora builders, and no one can figure out why. :/

* Wed Jan 30 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 4:5.10.0-4
- create %%{_prefix}/lib/perl5/vendor_perl/%%{perl_version}/auto and own it
  in base perl (resolves bugzilla 214580)

* Thu Jan 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 4:5.10.0-3
- Update Sys::Syslog to 0.24, to fix test failures

* Wed Jan 9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 4:5.10.0-2
- add some BR for tests

* Tue Jan 8 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 4:5.10.0-1
- 5.10.0 final
- clear out all the unnecessary patches (down to 8 patches!)
- get rid of super perl debugging mode
- add new subpackages

* Thu Nov 29 2007 Robin Norwood <rnorwood@redhat.com> - 4:5.10.0_RC2-0.1
- first attempt at building 5.10.0


