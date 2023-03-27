Vendor:         Microsoft Corporation
Distribution:   Mariner
# disable prof, docs, perf build, debuginfo
# NB This must be disabled (bcond_with) for all koji production builds
%bcond_with quickbuild

# make sure ghc libraries' ABI hashes unchanged
%bcond_without abicheck

%global ghc_major 8.10

# to handle RCs
%global ghc_release %{version}

%global base_ver 4.14.3.0

# build profiling libraries
# build haddock
# perf production build (disable for quick build)
%if %{with quickbuild}
%undefine with_ghc_prof
%undefine with_haddock
%bcond_with perf_build
%undefine _enable_debug_packages
%else
%bcond_without ghc_prof
%bcond_without haddock
%bcond_without perf_build
%endif

# to enable dwarf info (only on intel archs): overrides perf
# default is off: bcond_with
%ifarch x86_64 i686
%bcond_with dwarf
%endif

# locked together since disabling haddock causes no manuals built
# and disabling haddock still created index.html
# https://ghc.haskell.org/trac/ghc/ticket/15190
%{?with_haddock:%bcond_without manual}

# no longer build testsuite (takes time and not really being used)
%bcond_with testsuite

# 8.10 can use llvm 9-12
%global llvm_major 11
%global ghc_llvm_archs armv7hl aarch64

%global ghc_unregisterized_arches s390 s390x %{mips} riscv64

Name: ghc
Version: 8.10.7
# Since library subpackages are versioned:
# - release can only be reset if *all* library versions get bumped simultaneously
#   (sometimes after a major release)
# - minor release numbers for a branch should be incremented monotonically
Release: 121%{?dist}
Summary: Glasgow Haskell Compiler

License: BSD and HaskellReport
URL: https://haskell.org/ghc/
Source0: https://downloads.haskell.org/ghc/%{ghc_release}/ghc-%{version}-src.tar.xz
%if %{with testsuite}
Source1: https://downloads.haskell.org/ghc/%{ghc_release}/ghc-%{version}-testsuite.tar.xz
%endif
Source2: https://downloads.haskell.org/ghc/%{ghc_release}/ghc-%{version}-src.tar.xz.sig
Source5: ghc-pkg.man
Source6: haddock.man
Source7: runghc.man
# absolute haddock path (was for html/libraries -> libraries)
Patch1: ghc-gen_contents_index-haddock-path.patch
Patch2: ghc-Cabal-install-PATH-warning.patch
Patch3: ghc-gen_contents_index-nodocs.patch
# https://phabricator.haskell.org/rGHC4eebc8016f68719e1ccdf460754a97d1f4d6ef05
Patch6: ghc-8.6.3-sphinx-1.8.patch

# Arch dependent patches
# arm
Patch12: ghc-armv7-VFPv3D16--NEON.patch

# for unregisterized
# https://ghc.haskell.org/trac/ghc/ticket/15689
Patch15: ghc-warnings.mk-CC-Wall.patch

# bigendian (s390x and ppc64)
# https://gitlab.haskell.org/ghc/ghc/issues/15411
# https://gitlab.haskell.org/ghc/ghc/issues/16505
# https://bugzilla.redhat.com/show_bug.cgi?id=1651448
# https://ghc.haskell.org/trac/ghc/ticket/15914
# https://gitlab.haskell.org/ghc/ghc/issues/16973
# https://bugzilla.redhat.com/show_bug.cgi?id=1733030
Patch18: Disable-unboxed-arrays.patch

# Debian patches:
Patch24: buildpath-abi-stability.patch
Patch26: no-missing-haddock-file-warning.patch

# fedora ghc has been bootstrapped on
# %%{ix86} x86_64 ppc ppc64 armv7hl s390 s390x ppc64le aarch64
# and retired arches: alpha sparcv9 armv5tel
# see also deprecated ghc_arches defined in ghc-srpm-macros
# /usr/lib/rpm/macros.d/macros.ghc-srpm

BuildRequires: ghc-compiler > 8.6
# for ABI hash checking
%if %{with abicheck}
BuildRequires: %{name}
%endif
BuildRequires: ghc-rpm-macros-extra
BuildRequires: ghc-binary-devel
BuildRequires: ghc-bytestring-devel
BuildRequires: ghc-containers-devel
BuildRequires: ghc-directory-devel
BuildRequires: ghc-pretty-devel
BuildRequires: ghc-process-devel
BuildRequires: ghc-stm-devel
BuildRequires: ghc-template-haskell-devel
BuildRequires: ghc-transformers-devel
BuildRequires: alex
BuildRequires: gmp-devel
BuildRequires: hscolour
BuildRequires: libffi-devel
BuildRequires: make
# for terminfo
BuildRequires: ncurses-devel
BuildRequires: perl-interpreter
%if %{with testsuite}
BuildRequires: python3
%endif
%if %{with manual}
BuildRequires: python3-sphinx
%endif
%ifarch %{ghc_llvm_archs}
BuildRequires: llvm%{llvm_major}
%endif
%if %{with dwarf}
BuildRequires: elfutils-devel
%endif
%ifarch armv7hl
# patch12
BuildRequires: autoconf, automake
%endif
%if %{without quickbuild}
#BuildRequires: gnupg2
%endif
Requires: %{name}-compiler = %{version}-%{release}
Requires: %{name}-devel = %{version}-%{release}
Requires: %{name}-ghc-devel = %{version}-%{release}
%if %{with haddock}
Suggests: %{name}-doc = %{version}-%{release}
Suggests: %{name}-doc-index = %{version}-%{release}
%endif
%if %{with manual}
Suggests: %{name}-manual = %{version}-%{release}
%endif
%if %{with ghc_prof}
Suggests: %{name}-prof = %{version}-%{release}
%endif

%description
GHC is a state-of-the-art, open source, compiler and interactive environment
for the functional language Haskell. Highlights:

- GHC supports the entire Haskell 2010 language plus a wide variety of
  extensions.
- GHC has particularly good support for concurrency and parallelism,
  including support for Software Transactional Memory (STM).
- GHC generates fast code, particularly for concurrent programs.
  Take a look at GHC's performance on The Computer Language Benchmarks Game.
- GHC works on several platforms including Windows, Mac, Linux,
  most varieties of Unix, and several different processor architectures.
- GHC has extensive optimisation capabilities, including inter-module
  optimisation.
- GHC compiles Haskell code either directly to native code or using LLVM
  as a back-end. GHC can also generate C code as an intermediate target for
  porting to new platforms. The interactive environment compiles Haskell to
  bytecode, and supports execution of mixed bytecode/compiled programs.
- Profiling is supported, both by time/allocation and various kinds of heap
  profiling.
- GHC comes with several libraries, and thousands more are available on Hackage.


%package compiler
Summary: GHC compiler and utilities
License: BSD
Requires: gcc%{?_isa}
Requires: %{name}-base-devel%{?_isa} = %{base_ver}-%{release}
%if %{with haddock}
Requires: %{name}-filesystem = %{version}-%{release}
%else
Obsoletes: %{name}-doc-index < %{version}-%{release}
Obsoletes: %{name}-filesystem < %{version}-%{release}
%endif
%ifarch %{ghc_llvm_archs}
Requires: llvm%{llvm_major}
%endif
Conflicts: ghc%{ghc_major}-compiler = %{version}

%description compiler
The package contains the GHC compiler, tools and utilities.

The ghc libraries are provided by %{name}-devel.
To install all of ghc (including the ghc library),
install the main ghc package.


%if %{with haddock}
%package doc
Summary: Haskell library documentation meta package
License: BSD

%description doc
Installing this package causes %{name}-*-doc packages corresponding to
%{name}-*-devel packages to be automatically installed too.


%package doc-index
Summary: GHC library documentation indexing
License: BSD
Obsoletes: ghc-doc-cron < %{version}-%{release}
Requires: %{name}-compiler = %{version}-%{release}
BuildArch: noarch

%description doc-index
The package enables re-indexing of installed library documention.


%package filesystem
Summary: Shared directories for Haskell documentation
BuildArch: noarch
Obsoletes: %{name}-filesystem < %{version}-%{release}

%description filesystem
This package provides some common directories used for
Haskell libraries documentation.
%endif


%if %{with manual}
%package manual
Summary: GHC manual
License: BSD
BuildArch: noarch
Requires: %{name}-filesystem = %{version}-%{release}

%description manual
This package provides the User Guide and Haddock manual.
%endif


# ghclibdir also needs ghc_version_override for bootstrapping
%global ghc_version_override %{version}

%global BSDHaskellReport %{quote:BSD and HaskellReport}

# use "./libraries-versions.sh" to check versions
%if %{defined ghclibdir}
%ghc_lib_subpackage -d -l BSD Cabal-3.2.1.0
%ghc_lib_subpackage -d -l %BSDHaskellReport array-0.5.4.0
%ghc_lib_subpackage -d -l %BSDHaskellReport -c gmp-devel%{?_isa},libffi-devel%{?_isa} base-%{base_ver}
%ghc_lib_subpackage -d -l BSD binary-0.8.8.0
%ghc_lib_subpackage -d -l BSD bytestring-0.10.12.0
%ghc_lib_subpackage -d -l %BSDHaskellReport containers-0.6.5.1
%ghc_lib_subpackage -d -l %BSDHaskellReport deepseq-1.4.4.0
%ghc_lib_subpackage -d -l %BSDHaskellReport directory-1.3.6.0
%ghc_lib_subpackage -d -l %BSDHaskellReport exceptions-0.10.4
%ghc_lib_subpackage -d -l BSD filepath-1.4.2.1
# in ghc not ghc-libraries:
%ghc_lib_subpackage -d -x ghc-%{ghc_version_override}
%ghc_lib_subpackage -d -x -l BSD ghc-boot-%{ghc_version_override}
%ghc_lib_subpackage -d -l BSD ghc-boot-th-%{ghc_version_override}
%ghc_lib_subpackage -d -l BSD ghc-compact-0.1.0.0
%ghc_lib_subpackage -d -l BSD ghc-heap-%{ghc_version_override}
# see below for ghc-prim
%ghc_lib_subpackage -d -l BSD -x ghci-%{ghc_version_override}
%ghc_lib_subpackage -d -l BSD haskeline-0.8.2
%ghc_lib_subpackage -d -l BSD hpc-0.6.1.0
# see below for integer-gmp
%ghc_lib_subpackage -d -l %BSDHaskellReport libiserv-%{ghc_version_override}
%ghc_lib_subpackage -d -l BSD mtl-2.2.2
%ghc_lib_subpackage -d -l BSD parsec-3.1.14.0
%ghc_lib_subpackage -d -l BSD pretty-1.1.3.6
%ghc_lib_subpackage -d -l %BSDHaskellReport process-1.6.13.2
%ghc_lib_subpackage -d -l BSD stm-2.5.0.1
%ghc_lib_subpackage -d -l BSD template-haskell-2.16.0.0
%ghc_lib_subpackage -d -l BSD -c ncurses-devel%{?_isa} terminfo-0.4.1.4
%ghc_lib_subpackage -d -l BSD text-1.2.4.1
%ghc_lib_subpackage -d -l BSD time-1.9.3
%ghc_lib_subpackage -d -l BSD transformers-0.5.6.2
%ghc_lib_subpackage -d -l BSD unix-2.7.2.2
%if %{with haddock}
%ghc_lib_subpackage -d -l BSD xhtml-3000.2.2.1
%endif
%endif

%global version %{ghc_version_override}

%package devel
Summary: GHC development libraries meta package
License: BSD and HaskellReport
Requires: %{name}-compiler = %{version}-%{release}
Obsoletes: ghc-libraries < %{version}-%{release}
Provides: ghc-libraries = %{version}-%{release}
%{?ghc_packages_list:Requires: %(echo %{ghc_packages_list} | sed -e "s/\([^ ]*\)-\([^ ]*\)/%{name}-\1-devel = \2-%{release},/g")}

%description devel
This is a meta-package for all the development library packages in GHC
except the ghc library, which is installed by the toplevel ghc metapackage.


%if %{with ghc_prof}
%package prof
Summary: GHC profiling libraries meta package
License: BSD
Requires: %{name}-compiler = %{version}-%{release}

%description prof
Installing this package causes %{name}-*-prof packages corresponding to
%{name}-*-devel packages to be automatically installed too.
%endif


%prep
%if %{without quickbuild}
#%%{gpgverify} --keyring='%{SOURCE3}' --signature='%{SOURCE2}' --data='%{SOURCE0}'
%endif
%setup -q -n ghc-%{version} %{?with_testsuite:-b1}

%patch1 -p1 -b .orig
%patch3 -p1 -b .orig

%patch2 -p1 -b .orig
%patch6 -p1 -b .orig

rm -r libffi-tarballs

%ifarch armv7hl
%patch12 -p1 -b .orig12
%endif

# remove s390x after switching to llvm
%ifarch %{ghc_unregisterized_arches} s390x
%patch15 -p1 -b .orig
%endif

# bigendian
%ifarch ppc64 s390x
%patch18 -p1 -b .orig
%endif

# debian
%patch24 -p1 -b .orig
%patch26 -p1 -b .orig

%if %{with haddock}
%global gen_contents_index gen_contents_index.orig
if [ ! -f "libraries/%{gen_contents_index}" ]; then
  echo "Missing libraries/%{gen_contents_index}, needed at end of %%install!"
  exit 1
fi
%endif

# http://ghc.haskell.org/trac/ghc/wiki/Platforms
cat > mk/build.mk << EOF
%if %{with perf_build}
%ifarch %{ghc_llvm_archs}
BuildFlavour = perf-llvm
%else
%if %{with dwarf}
BuildFlavour = dwarf
%else
BuildFlavour = perf
%endif
%endif
%else
%ifarch %{ghc_llvm_archs}
BuildFlavour = quick-llvm
%else
BuildFlavour = quick
%endif
%endif
GhcLibWays = v dyn %{?with_ghc_prof:p}
%if %{with haddock}
HADDOCK_DOCS = YES
EXTRA_HADDOCK_OPTS += --hyperlinked-source --hoogle --quickjump
%else
HADDOCK_DOCS = NO
%endif
%if %{with manual}
BUILD_MAN = YES
BUILD_SPHINX_HTML = YES
%else
BUILD_MAN = NO
BUILD_SPHINX_HTML = NO
%endif
BUILD_SPHINX_PDF = NO
EOF

%build
# for patch12
%ifarch armv7hl
autoreconf
%endif

%ghc_set_gcc_flags
export CC=%{_bindir}/gcc

# * %%configure induces cross-build due to different target/host/build platform names
./configure --prefix=%{_prefix} --exec-prefix=%{_exec_prefix} \
  --bindir=%{_bindir} --sbindir=%{_sbindir} --sysconfdir=%{_sysconfdir} \
  --datadir=%{_datadir} --includedir=%{_includedir} --libdir=%{_libdir} \
  --libexecdir=%{_libexecdir} --localstatedir=%{_localstatedir} \
  --sharedstatedir=%{_sharedstatedir} --mandir=%{_mandir} \
  --docdir=%{_docdir}/%{name} \
  --with-system-libffi \
%ifarch %{ghc_unregisterized_arches}
  --enable-unregisterised \
%endif
  %{?with_dwarf:--enable-dwarf-unwind} \
%{nil}

# avoid "ghc: hGetContents: invalid argument (invalid byte sequence)"
export LANG=C.utf8
make %{?_smp_mflags}


%install
make DESTDIR=%{buildroot} install

%if %{defined _ghcdynlibdir}
mv %{buildroot}%{ghclibdir}/*/libHS*ghc%{ghc_version}.so %{buildroot}%{_ghcdynlibdir}/
for i in $(find %{buildroot} -type f -executable -exec sh -c "file {} | grep -q 'dynamically linked'" \; -print); do
  chrpath -d $i
done
for i in %{buildroot}%{ghclibdir}/package.conf.d/*.conf; do
  sed -i -e 's!^dynamic-library-dirs: .*!dynamic-library-dirs: %{_ghcdynlibdir}!' $i
done
sed -i -e 's!^library-dirs: %{ghclibdir}/rts!&\ndynamic-library-dirs: %{_ghcdynlibdir}!' %{buildroot}%{ghclibdir}/package.conf.d/rts.conf
%endif

# containers src moved to a subdir
cp -p libraries/containers/containers/LICENSE libraries/containers/LICENSE

# libraries licenses
rm %{buildroot}%{ghc_html_libraries_dir}/{ghc-prim,integer-gmp}-*/LICENSE
mkdir -p %{buildroot}%{_ghclicensedir}
for i in $(cd %{buildroot}%{ghc_html_libraries_dir}; ls */LICENSE); do
  pkg=$(dirname $i | sed -e "s/\\(.*\\)-.*/\\1/")
  mkdir %{buildroot}%{_ghclicensedir}/ghc-$pkg
  mv %{buildroot}%{ghc_html_libraries_dir}/$i %{buildroot}%{_ghclicensedir}/ghc-$pkg/
done

for i in %{ghc_packages_list}; do
name=$(echo $i | sed -e "s/\(.*\)-.*/\1/")
ver=$(echo $i | sed -e "s/.*-\(.*\)/\1/")
%ghc_gen_filelists $name $ver
done

echo "%%dir %{ghclibdir}" >> ghc-base%{?_ghcdynlibdir:-devel}.files
echo "%{ghclibdir}/include" >> ghc-base-devel.files

%ghc_gen_filelists ghc %{ghc_version_override}
%ghc_gen_filelists ghc-boot %{ghc_version_override}
%ghc_gen_filelists ghci %{ghc_version_override}

%ghc_gen_filelists ghc-prim 0.6.1
%ghc_gen_filelists integer-gmp 1.0.3.0

%define merge_filelist()\
cp -p libraries/%1/LICENSE libraries/LICENSE.%1\
echo "%%license libraries/LICENSE.%1" >> ghc-%2.files\
cat ghc-%1.files >> ghc-%2.files\
for i in devel doc prof; do\
  cat ghc-%1-$i.files >> ghc-%2-$i.files\
done

%merge_filelist ghc-prim base
%merge_filelist integer-gmp base

# add rts libs
rm -f rts.files
touch rts.files
ls %{buildroot}%{?_ghcdynlibdir}%{!?_ghcdynlibdir:%{ghclibdir}/rts}/libHSrts*-ghc%{ghc_version}.so >> rts.files
find %{buildroot}%{ghclibdir}/rts -type d -fprintf rts-devel.files '%%%%dir %p\n' -o -name 'libHSrts*_p.a' -fprint rts-prof.files -o -fprint rts-devel.files
echo "%{ghclibdir}/package.conf.d/rts.conf" >> rts-devel.files
sed -i -e "s!%{buildroot}!!g" rts.files rts-devel.files rts-prof.files
cat rts.files >> ghc-base.files
cat rts-devel.files >> ghc-base-devel.files
cat rts-prof.files >> ghc-base-prof.files

%if %{with haddock}
# generate initial lib doc index
cd libraries
sh %{gen_contents_index} --intree --verbose
cd ..
%endif

mkdir -p %{buildroot}%{_mandir}/man1
install -p -m 0644 %{SOURCE5} %{buildroot}%{_mandir}/man1/ghc-pkg.1
install -p -m 0644 %{SOURCE6} %{buildroot}%{_mandir}/man1/haddock.1
install -p -m 0644 %{SOURCE7} %{buildroot}%{_mandir}/man1/runghc.1

%ifarch armv7hl
export RPM_BUILD_NCPUS=1
%endif


%check
export LANG=C.utf8
# stolen from ghc6/debian/rules:
GHC=inplace/bin/ghc-stage2
# Do some very simple tests that the compiler actually works
rm -rf testghc
mkdir testghc
echo 'main = putStrLn "Foo"' > testghc/foo.hs
$GHC testghc/foo.hs -o testghc/foo
[ "$(testghc/foo)" = "Foo" ]
rm testghc/*
echo 'main = putStrLn "Foo"' > testghc/foo.hs
$GHC testghc/foo.hs -o testghc/foo -O2
[ "$(testghc/foo)" = "Foo" ]
rm testghc/*
echo 'main = putStrLn "Foo"' > testghc/foo.hs
$GHC testghc/foo.hs -o testghc/foo -dynamic
[ "$(testghc/foo)" = "Foo" ]
rm testghc/*

$GHC --info

# check the ABI hashes
%if %{with abicheck}
if [ "%{version}" = "$(ghc --numeric-version)" ]; then
  echo "Checking package ABI hashes:"
  for i in %{ghc_packages_list}; do
    old=$(ghc-pkg field $i id --simple-output || :)
    if [ -n "$old" ]; then
      new=$(/usr/lib/rpm/ghc-pkg-wrapper %{buildroot}%{ghclibdir} field $i id --simple-output)
      if [ "$old" != "$new" ]; then
        echo "ABI hash for $i changed!:" >&2
        echo "  $old -> $new" >&2
        ghc_abi_hash_change=yes
      else
        echo "($old unchanged)"
      fi
    else
      echo "($i not installed)"
    fi
  done
  if [ "$ghc_abi_hash_change" = "yes" ]; then
     echo "ghc ABI hash change: aborting build!" >&2
     exit 1
  fi
else
  echo "ABI hash checks skipped: GHC changed from $(ghc --numeric-version) to %{version}"
fi
%endif

%if %{with testsuite}
make test
%endif


%if %{defined ghclibdir}
%transfiletriggerin compiler -- %{ghclibdir}/package.conf.d
%ghc_pkg_recache
%end

%transfiletriggerpostun compiler -- %{ghclibdir}/package.conf.d
%ghc_pkg_recache
%end


%if %{with haddock}
%transfiletriggerin doc-index -- %{ghc_html_libraries_dir}
env -C %{ghc_html_libraries_dir} ./gen_contents_index
%end

%transfiletriggerpostun doc-index -- %{ghc_html_libraries_dir}
env -C %{ghc_html_libraries_dir} ./gen_contents_index
%end
%endif
%endif


%files

%files compiler
%license LICENSE
%doc README.md
%{_bindir}/ghc
%{_bindir}/ghc-%{version}
%{_bindir}/ghc-pkg
%{_bindir}/ghc-pkg-%{version}
%{_bindir}/ghci
%{_bindir}/ghci-%{version}
%{_bindir}/hp2ps
%{_bindir}/hpc
%{_bindir}/hsc2hs
%{_bindir}/runghc
%{_bindir}/runghc-%{ghc_version}
%{_bindir}/runhaskell
%dir %{ghclibdir}/bin
%{ghclibdir}/bin/ghc
%{ghclibdir}/bin/ghc-pkg
%{ghclibdir}/bin/hpc
%{ghclibdir}/bin/hsc2hs
%{ghclibdir}/bin/ghc-iserv
%{ghclibdir}/bin/ghc-iserv-dyn
%if %{with ghc_prof}
%{ghclibdir}/bin/ghc-iserv-prof
%endif
%{ghclibdir}/bin/runghc
%{ghclibdir}/bin/hp2ps
%{ghclibdir}/bin/unlit
%{ghclibdir}/ghc-usage.txt
%{ghclibdir}/ghci-usage.txt
%{ghclibdir}/llvm-passes
%{ghclibdir}/llvm-targets
%dir %{ghclibdir}/package.conf.d
%ghost %{ghclibdir}/package.conf.d/package.cache
%{ghclibdir}/package.conf.d/package.cache.lock
%{ghclibdir}/platformConstants
%{ghclibdir}/settings
%{ghclibdir}/template-hsc.h
%{_mandir}/man1/ghc-pkg.1*
%{_mandir}/man1/haddock.1*
%{_mandir}/man1/runghc.1*

%if %{with haddock}
%{_bindir}/haddock
%{_bindir}/haddock-ghc-%{version}
%{ghclibdir}/bin/haddock
%{ghclibdir}/html
%{ghclibdir}/latex
%{ghc_html_libraries_dir}/prologue.txt
%verify(not size mtime) %{ghc_html_libraries_dir}/haddock-bundle.min.js
%verify(not size mtime) %{ghc_html_libraries_dir}/linuwial.css
%verify(not size mtime) %{ghc_html_libraries_dir}/quick-jump.css
%verify(not size mtime) %{ghc_html_libraries_dir}/synopsis.png
%endif
%if %{with manual}
%{_mandir}/man1/ghc.1*
%endif

%files devel

%if %{with haddock}
%files doc

%files doc-index
%{ghc_html_libraries_dir}/gen_contents_index
%verify(not size mtime) %{ghc_html_libraries_dir}/doc-index*.html
%verify(not size mtime) %{ghc_html_libraries_dir}/index*.html

%files filesystem
%dir %_ghc_doc_dir
%dir %ghc_html_dir
%dir %ghc_html_libraries_dir
%endif

%if %{with manual}
%files manual
## needs pandoc
#%%{ghc_html_dir}/Cabal
%if %{with haddock}
%{ghc_html_dir}/haddock
%{ghc_html_dir}/index.html
%{ghc_html_dir}/users_guide
%endif
%endif

%if %{with ghc_prof}
%files prof
%endif


%changelog
* Sat Aug  6 2022 Jens Petersen <petersen@redhat.com> - 8.10.7-121
- ghc-compiler conflicts with ghc8.10-compiler-8.10.7

* Sat Aug  6 2022 Jens Petersen <petersen@redhat.com> - 8.10.7-120
- conflicts with ghc8.10-8.10.7
- add ghc-filesystem obsoletes to help dnf

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 8.10.7-119
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 14 2022 Jens Petersen <petersen@redhat.com> - 8.10.7-118
- https://downloads.haskell.org/~ghc/8.10.7/docs/html/users_guide/8.10.7-notes.html
- add filesystem subpackage

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 8.10.5-117
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Jan 08 2022 Miro Hrončok <mhroncok@redhat.com> - 8.10.5-116
- Rebuilt for https://fedoraproject.org/wiki/Changes/LIBFFI34

* Fri Sep 17 2021 Jens Petersen <petersen@redhat.com>
- move zlib-devel Recommends to cabal-install

* Thu Jul 22 2021 Jens Petersen <petersen@redhat.com> - 8.10.5-115
- update to 8.10.5 with patch for missing rts symbols
- use llvm 11 for ARM
- https://downloads.haskell.org/~ghc/8.10.5/docs/html/users_guide/8.10.5-notes.html

* Thu Jul 15 2021 Jens Petersen <petersen@redhat.com> - 8.10.4-114
- perf build

* Thu Jul 15 2021 Jens Petersen <petersen@redhat.com> - 8.10.4-113
- rebase to 8.10.4 from ghc:8.10 module stream
- https://downloads.haskell.org/ghc/8.10.4/docs/html/users_guide/8.10.1-notes.html
- use llvm10 for ARM

* Wed Jun 30 2021 Jens Petersen <petersen@redhat.com> - 8.8.4-111
- fix build with sphinx4 (#1977317)

* Tue May 25 2021 Jens Petersen <petersen@redhat.com> - 8.8.4-110
- ghc-compiler now requires ghc-filesystem for html docdirs

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 8.8.4-109
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Dec 02 2020 David Abdurachmanov <david.abdurachmanov@sifive.com>
- Add riscv64 to ghc_unregisterized_arches

* Tue Aug 18 2020 Troy Dawson <tdawson@redhat.com> - 8.8.4-108
- Cleanup old %if statements

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 8.8.4-107
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul 16 2020 Jens Petersen <petersen@redhat.com> - 8.8.4-106
- 8.8.4 bugfix releases
- https://downloads.haskell.org/ghc/8.8.4/docs/html/users_guide/8.8.4-notes.html
- bytestring-0.10.10.1 and process-1.6.9.0

* Tue Jul 14 2020 Jens Petersen <petersen@redhat.com> - 8.8.3-105
- rebase to 8.8.3 from ghc:8.8 module stream
- https://downloads.haskell.org/ghc/8.8.1/docs/html/users_guide/8.8.1-notes.html
- https://downloads.haskell.org/ghc/8.8.2/docs/html/users_guide/8.8.2-notes.html
- https://downloads.haskell.org/ghc/8.8.3/docs/html/users_guide/8.8.3-notes.html

* Mon Jul  6 2020 Jens Petersen <petersen@redhat.com> - 8.6.5-104
- use python3-sphinx also for rhel8

* Thu Apr  9 2020 Jens Petersen <petersen@redhat.com> - 8.6.5-103
- fix running of gen_contents_index when no haddocks (#1813548)

* Mon Feb 10 2020 Jens Petersen <petersen@redhat.com> - 8.6.5-102
- rebuild against ghc-rpm-macros fixed for subpackage prof deps

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 8.6.5-101
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 31 2019 Jens Petersen <petersen@redhat.com> - 8.6.5-100
- update to GHC 8.6.5 (backport ghc:8.6 module stream)
- https://downloads.haskell.org/~ghc/8.6.5/docs/html/users_guide/8.6.1-notes.html
- https://downloads.haskell.org/~ghc/8.6.5/docs/html/users_guide/8.6.2-notes.html
- https://downloads.haskell.org/~ghc/8.6.5/docs/html/users_guide/8.6.3-notes.html
- https://downloads.haskell.org/~ghc/8.6.5/docs/html/users_guide/8.6.4-notes.html
- https://downloads.haskell.org/~ghc/8.6.5/docs/html/users_guide/8.6.5-notes.html
- fix process library initgroups issue
  (https://github.com/haskell/process/pull/148)
- add fix-build-using-unregisterized-v8.4.patch for s390x (#1648537)
  https://gitlab.haskell.org/ghc/ghc/issues/15913
- add bigendian patch for containers (#1651448)
  https://gitlab.haskell.org/ghc/ghc/issues/15411
- Debian patches:
  - add_-latomic_to_ghc-prim.patch,
  - rts osReserveHeapMemory block alignment

* Tue Jul 30 2019 Jens Petersen <petersen@redhat.com> - 8.4.4-99
- subpackage library haddock documentation and profiling libraries
- add ghc-doc and ghc-prof metapackages to pull in lib docs and prof libs
- rename ghc-doc-cron with ghc-doc-index using file triggers
- rename ghc-libraries to ghc-devel
- for quickbuild disable debuginfo
- lock ghc-compiler requires ghc-base-devel to ver-rel
- drop alternatives for runhaskell and hsc2hs
- use ghc_set_gcc_flags, with_ghc_prof, and with_haddock

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jun 28 2019 Jens Petersen <petersen@redhat.com> - 8.4.4-75
- add transfiletriggers that will replace individual post/postun scriptlets

* Mon Mar  4 2019 Jens Petersen <petersen@redhat.com> - 8.4.4-74
- unregisterized: fix 32bit adjacent floats issue
  (https://ghc.haskell.org/trac/ghc/ticket/15853)

* Sat Feb 16 2019 Jens Petersen <petersen@redhat.com> - 8.4.4-73
- update to GHC 8.4
- https://ghc.haskell.org/trac/ghc/blog/ghc-8.4.1-released
- new patches:
  - 6e361d895dda4600a85e01c72ff219474b5c7190.patch
  - fix-build-using-unregisterized-v8.2.patch
  - ghc-sphinx-1.8-4eebc8016.patch
- dropped patch:
  - D4159.patch
  - ghc-7.8-arm7_saner-linker-opt-handling-9873.patch
  - ghc-Debian-reproducible-tmp-names.patch
- rely on rpm to strip

* Fri Feb  8 2019 Jens Petersen <petersen@redhat.com> - 8.2.2-72
- add ghc_unregisterized_arches
- Recommends zlib-devel
- epel6 tweaks

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 8.2.2-72
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Nov 18 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 8.2.2-71
- Use C.UTF-8 locale
  See https://fedoraproject.org/wiki/Changes/Remove_glibc-langpacks-all_from_buildroot

* Mon Oct 22 2018 Jens Petersen <petersen@redhat.com>
- Recommends for ghc-manual and ghc-doc-cron

* Wed Oct 17 2018 Jens Petersen <petersen@redhat.com> - 8.2.2-70
- backport quickbuild config from 8.4 module and extend to perf_build
- disable -Wall on s390x like in 8.4 module to silence warning flood
  and simplify setting of CFLAGS
- enable buildpath-abi-stability.patch (from Debian)
- setup build.mk in setup section, taken from copr and module

* Tue Oct 16 2018 Peter Robinson <pbrobinson@fedoraproject.org>
- Update alternatives dependencies

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 8.2.2-69
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon May 28 2018 Jens Petersen <petersen@redhat.com> - 8.2.2-68
- fix sphinx-build version detection
- merge bcond for haddock and manual
- disable the testsuite to speed up builds
- version bootstrap and packaging fixes and tweaks

* Mon May 28 2018 Jens Petersen <petersen@redhat.com> - 8.2.2-67
- move manuals to new ghc-manual (noarch)
- rename ghc-doc-index to ghc-doc-cron (noarch)
- ghost the ghc-doc-index local state files
- ghost some newer libraries index files
- simplify and extend bcond for build configuration
- drop bootstrap builds and do ABI hash checks unless ghc version changed
- no longer need autotools on aarch64

* Tue Apr 10 2018 Jens Petersen <petersen@redhat.com> - 8.2.2-66
- ghc-pkg: silence the abi-depends warnings

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 8.2.2-65
- Escape macros in %%changelog

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 8.2.2-64
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 30 2018 Jens Petersen <petersen@redhat.com> - 8.2.2-63
- apply Phabricator D4159.patch to workaround
  https://ghc.haskell.org/trac/ghc/ticket/14381

* Thu Jan 25 2018 Jens Petersen <petersen@redhat.com> - 8.2.2-62
- 8.2.2 perf build
- https://downloads.haskell.org/~ghc/8.2.2/docs/html/users_guide/8.2.1-notes.html
- https://downloads.haskell.org/~ghc/8.2.2/docs/html/users_guide/8.2.2-notes.html

* Wed Jan 24 2018 Jens Petersen <petersen@redhat.com> - 8.2.2-61
- 8.2.2 bootstrap build
- install ghc libs in libdir and remove RUNPATHs
- add shadowed-deps.patch (haskell/cabal#4728)
- new ghc-compact library
- exclude ghc-boot for ghc-libraries

* Thu Oct 26 2017 Jens Petersen <petersen@redhat.com> - 8.0.2-60
- fix space in BSDHaskellReport license macro for rpm-4.14
- mark other subpackages correctly as BSD license
- drop ghc-boot from ghc-libraries

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.2-59
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.2-58
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 17 2017 Jens Petersen <petersen@redhat.com> - 8.0.2-57
- 8.0.2 perf build
- http://downloads.haskell.org/~ghc/8.0.2/docs/html/users_guide/8.0.1-notes.html
- http://downloads.haskell.org/~ghc/8.0.2/docs/html/users_guide/8.0.2-notes.html

* Fri Feb 17 2017 Jens Petersen <petersen@redhat.com> - 8.0.2-56
- update to GHC 8.0 (bootstrap build)
- backport changes from http://github.com/fedora-haskell/ghc
  adding some new patches from Debian
- use llvm3.7 on ARM archs
- user guide now built with sphinx

* Mon Feb 13 2017 Jens Petersen <petersen@redhat.com> - 7.10.3-55
- use new ghc_lib_subpackage -d option to fix handling of .files
- configure llc-3.5 and opt-3.5 explicitly for all arch's

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.10.3-54
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 7.10.3-53
- Rebuild for readline 7.x

* Wed Oct 26 2016 Jens Petersen <petersen@redhat.com> - 7.10.3-52
- use license macro
- update subpackaging for latest ghc-rpm-macros
- minor spec file cleanups
- drop old dph and feldspar obsoletes
- obsoletes ghc-doc-index when without_haddock
- BR perl

* Tue Jul 12 2016 Jens Petersen <petersen@redhat.com> - 7.10.3-51
- obsolete haskell98 and haskell2010
- add an ABI change check to prevent unexpected ghc package hash changes

* Fri Jun  3 2016 Jens Petersen <petersen@redhat.com> - 7.10.3-50
- perf build
- http://downloads.haskell.org/~ghc/7.10.3/docs/html/users_guide/release-7-10-1.html
- http://downloads.haskell.org/~ghc/7.10.3/docs/html/users_guide/release-7-10-2.html
- http://downloads.haskell.org/~ghc/7.10.3/docs/html/users_guide/release-7-10-3.html

* Wed Jun  1 2016 Jens Petersen <petersen@redhat.com> - 7.10.3-49
- quick build
- use 7.10.3b respin tarballs
- no longer need:
  - ghc-glibc-2.20_BSD_SOURCE.patch
  - ghc-7.8-arm-use-ld-gold.patch
  - ghc-7.8-arm7_saner-linker-opt-handling-9873.patch
  - ghc-config.mk.in-Enable-SMP-and-GHCi-support-for-Aarch64.patch
  - build_minimum_smp
- add Debian packages:
  - buildpath-abi-stability
  - no-missing-haddock-file-warning
  - reproducible-tmp-names
- use llvm35
- add libraries-versions.sh script
- all library versions updates except xhtml
- BR ghc-rpm-macros-extra for all OS versions
- support building on EL6
- deprecated libraries: haskell2010, haskell98, old-locale, old-time
- symlink for integer-gmp2
- add llvm_major

* Tue Mar  8 2016 Michal Toman <mtoman@fedoraproject.org> - 7.8.4-48
- do not package ghc-split on MIPS (#1294873)

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 7.8.4-47
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jun 16 2015 Jens Petersen <petersen@redhat.com> - 7.8.4-46
- rebuild

* Thu Jun 11 2015 Jens Petersen <petersen@fedoraproject.org> - 7.8.4-45
- use ld.gold on aarch64 like for armv7 (Erik de Castro Lopo, #1195231)

* Wed Apr 22 2015 Jens Petersen <petersen@redhat.com> - 7.8.4-44
- turn on SMP and ghci for aarch64 (Erik de Castro Lopo, #1203951)
- use "make -j2" for s390 (#1212374)

* Mon Mar 30 2015 Jens Petersen <petersen@redhat.com> - 7.8.4-43
- aarch64 production build

* Mon Mar 23 2015 Jens Petersen <petersen@redhat.com> - 7.8.4-42.2
- aarch64 bootstrap build
- must use "make -j16" for Intel arches to preserve ABI hashes
  (-j12 changed array's hash on i686)

* Wed Mar 18 2015 Jens Petersen <petersen@redhat.com> - 7.8.4-42.1
- fix build.mk BuildFlavour setup
- improve the smp make setup with build_minimum_smp
- bootstrap for aarch64 without ghci (#1195231)
- disable ld hardening for F23 on 64bit and armv7hl

* Sat Feb 14 2015 Jens Petersen <petersen@redhat.com> - 7.8.4-42
- try "make -j16" on Intel arches to keep ABI hashes same as -40

* Mon Feb  9 2015 Jens Petersen <petersen@redhat.com> - 7.8.4-41
- update the arm64 patch for 7.8.4
- all archs have bindir/ghci

* Sun Jan 18 2015 Jens Petersen <petersen@redhat.com> - 7.8.4-40
- production build
- version doc htmldirs again

* Sat Jan 17 2015 Jens Petersen <petersen@redhat.com> - 7.8.4-39
- update to 7.8.4
- bump release over haskell-platform xhtml
- https://www.haskell.org/ghc/docs/7.8.4/html/users_guide/release-7-8-1.html
- https://www.haskell.org/ghc/docs/7.8.4/html/users_guide/release-7-8-2.html
- https://www.haskell.org/ghc/docs/7.8.4/html/users_guide/release-7-8-3.html
- https://www.haskell.org/ghc/docs/7.8.4/html/users_guide/release-7-8-4.html
- bootstrap build
- provides haskeline, terminfo and xhtml libraries
- shared libraries on all archs
- bindir/ghci only on ghc_arches_with_ghci
- use ld.gold on ARMv7 (see https://ghc.haskell.org/trac/ghc/ticket/8976)
  [thanks to Joachim Breitner for workaround patches posted upstream]

* Tue Nov 18 2014 Jens Petersen <petersen@redhat.com> - 7.6.3-28
- remove the build hack to switch from llvm to llvm34 (#1161049)
- use rpm internal dependency generator with ghc.attr on F21+
- fix bash-ism in ghc-doc-index (#1146733)
- do "quick" build when bootstrapping
- setup LDFLAGS

* Mon Nov 17 2014 Jens Petersen <petersen@redhat.com> - 7.6.3-27
- use llvm34 instead of llvm-3.5 for arm (#1161049)

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.6.3-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 15 2014 Jens Petersen <petersen@redhat.com> - 7.6.3-25
- configure ARM with VFPv3D16 and without NEON (#995419)
- only apply the Cabal unversion docdir patch to F21 and later
- hide llvm version warning on ARM now up to 3.4

* Fri Jun  6 2014 Jens Petersen <petersen@redhat.com> - 7.6.3-24
- add aarch64 with Debian patch by Karel Gardas and Colin Watson
- patch Stg.h to define _DEFAULT_SOURCE instead of _BSD_SOURCE to quieten
  glibc 2.20 warnings (see #1067110)

* Fri May 30 2014 Jens Petersen <petersen@redhat.com> - 7.6.3-23
- bump release

* Fri May 30 2014 Jens Petersen <petersen@redhat.com> - 7.6.3-22
- add ppc64le support patch from Debian by Colin Watson
  (thanks to Jaromir Capik for Fedora ppc64le bootstrap)

* Wed Jan 29 2014 Jens Petersen <petersen@redhat.com> - 7.6.3-21
- fix segfault on i686 when using ffi double-mapping for selinux (#907515)
  see http://hackage.haskell.org/trac/ghc/ticket/7629
  (thanks Garrett Mitchener for patch committed upstream)

* Wed Oct 30 2013 Jens Petersen <petersen@redhat.com> - 7.6.3-20
- enable debuginfo for C code bits (#989593)
- back to production build

* Tue Oct 29 2013 Jens Petersen <petersen@redhat.com> - 7.6.3-19
- fix rts hang on 64bit bigendian archs (patch by Gustavo Luiz Duarte, #989593)
- generate and ship library doc index for ghc bundled libraries
- build with utf8 encoding (needed for verbose ghc output
  and makes better sense anyway)
- change ghc-cabal to make library html docdirs unversioned
- bootstrap build

* Sat Jul 27 2013 Jóhann B. Guðmundsson <johannbg@fedoraproject.org> - 7.6.3-18
- ghc-doc-index requires crontabs and mark cron file config noreplace
  (http://fedoraproject.org/wiki/Packaging:CronFiles)

* Wed Jul 24 2013 Jens Petersen <petersen@redhat.com> - 7.6.3-17
- silence warnings about unsupported llvm version (> 3.1) on ARM

* Thu Jul 11 2013 Jens Petersen <petersen@redhat.com> - 7.6.3-16
- revert the executable stack patch since it didn't fully fix the problem
  and yet changed the ghc library hash

* Wed Jul 10 2013 Jens Petersen <petersen@redhat.com> - 7.6.3-15
- turn off executable stack flag in executables (#973512)
  (thanks Edward Zhang for upstream patch and Dhiru Kholia for report)

* Tue Jun 25 2013 Jens Petersen <petersen@redhat.com> - 7.6.3-14
- fix compilation with llvm-3.3 (#977652)
  see http://hackage.haskell.org/trac/ghc/ticket/7996

* Thu Jun 20 2013 Jens Petersen <petersen@redhat.com> - 7.6.3-13
- production perf -O2 build
- see release notes:
  http://www.haskell.org/ghc/docs/7.6.3/html/users_guide/release-7-6-1.html
  http://www.haskell.org/ghc/docs/7.6.3/html/users_guide/release-7-6-2.html
  http://www.haskell.org/ghc/docs/7.6.3/html/users_guide/release-7-6-3.html

* Thu Jun 20 2013 Jens Petersen <petersen@redhat.com> - 7.6.3-12
- bootstrap 7.6.3
- all library versions bumped except pretty
- ghc-7.4-add-support-for-ARM-hard-float-ABI-fixes-5914.patch, and
  ghc-7.4-silence-gen_contents_index.patch are no longer needed
- build with ghc-rpm-macros-extra
- no longer filter type-level package from haddock index
- process obsoletes process-leksah
- do production build with BuildFlavour perf (#880135)

* Tue Feb  5 2013 Jens Petersen <petersen@redhat.com> - 7.4.2-11
- ghclibdir should be owned at runtime by ghc-base instead of ghc-compiler
  (thanks Michael Scherer, #907671)

* Thu Jan 17 2013 Jens Petersen <petersen@redhat.com> - 7.4.2-10
- rebuild for F19 libffi soname bump

* Wed Nov 21 2012 Jens Petersen <petersen@redhat.com> - 7.4.2-9
- fix permissions of ghc-doc-index and only run when root
- ghc-doc-index cronjob no longer looks at /etc/sysconfig/ghc-doc-index

* Sat Nov 17 2012 Jens Petersen <petersen@redhat.com> - 7.4.2-8
- production 7.4.2 build
  http://www.haskell.org/ghc/docs/7.4.2/html/users_guide/release-7-4-2.html

* Sat Nov 17 2012 Jens Petersen <petersen@redhat.com> - 7.4.2-7
- 7.4.2 bootstrap
- update base and unix library versions
- ARM StgCRun patches not longer needed
- use Karel Gardas' ARM hardfloat patch committed upstream
- use _smp_mflags again
- disable Cabal building ghci lib files
- silence the doc re-indexing script and move the doc indexing cronjob
  to a new ghc-doc-index subpackage (#870694)
- do not disable hscolour in build.mk
- drop the explicit hscolour BR
- without_hscolour should now be set by ghc-rpm-macros for bootstrapping

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 15 2012 Jens Petersen <petersen@redhat.com> - 7.4.1-5
- use ghc_lib_subpackage instead of ghc_binlib_package (ghc-rpm-macros 0.91)

* Wed May  2 2012 Jens Petersen <petersen@redhat.com> - 7.4.1-4
- add ghc-wrapper-libffi-include.patch to workaround "missing libffi.h"
  for prof compiling on secondary archs

* Sat Apr 28 2012 Jens Petersen <petersen@redhat.com> - 7.4.1-3
- build with llvm-3.0 on ARM
- remove ARM from unregisterised_archs
- add 4 Debian ARM patches for armel and armhf (Iain Lane)

* Wed Mar 21 2012 Jens Petersen <petersen@redhat.com> - 7.4.1-2
- full build

* Wed Feb 15 2012 Jens Petersen <petersen@redhat.com> - 7.4.1-1
- update to new 7.4.1 major release
  http://www.haskell.org/ghc/docs/7.4.1/html/users_guide/release-7-4-1.html
- all library versions bumped
- binary package replaces ghc-binary
- random library dropped
- new hoopl library
- deepseq is now included in ghc
- Cabal --enable-executable-dynamic patch is upstream
- add Cabal-fix-dynamic-exec-for-TH.patch
- sparc linking fix is upstream
- use Debian's system-libffi patch by Joachim Breitner
- setup ghc-deps.sh after ghc_version_override for bootstrapping
- drop ppc64 config, pthread and mmap patches
- do not set GhcUnregisterised explicitly
- add s390 and s390x to unregisterised_archs
- Cabal manual needs pandoc

* Thu Jan 19 2012 Jens Petersen <petersen@redhat.com> - 7.0.4-42
- move ghc-ghc-devel from ghc-libraries to the ghc metapackage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.0.4-41
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 14 2011 Jens Petersen <petersen@redhat.com> - 7.0.4-40
- do alternatives handling correctly (reported by Giam Teck Choon, #753661)
  see https://fedoraproject.org/wiki/Packaging:Alternatives

* Sat Nov 12 2011 Jens Petersen <petersen@redhat.com> - 7.0.4-39
- move ghc-doc and ghc-libs obsoletes
- add HaskellReport license also to the base and libraries subpackages

* Thu Nov 10 2011 Jens Petersen <petersen@redhat.com> - 7.0.4-38
- the post and postun scripts are now for the compiler subpackage

* Wed Nov  2 2011 Jens Petersen <petersen@redhat.com> - 7.0.4-37
- rename ghc-devel metapackage to ghc-libraries
- require ghc-rpm-macros-0.14

* Tue Nov  1 2011 Jens Petersen <petersen@redhat.com> - 7.0.4-36
- move compiler and tools to ghc-compiler
- the ghc base package is now a metapackage that installs all of ghc,
  ie ghc-compiler and ghc-devel (#750317)
- drop ghc-doc provides

* Fri Oct 28 2011 Jens Petersen <petersen@redhat.com> - 7.0.4-35.1
- rebuild against new gmp

* Fri Oct 28 2011 Jens Petersen <petersen@redhat.com> - 7.0.4-35
- add HaskellReport license tag to some of the library subpackages
  which contain some code from the Haskell Reports

* Thu Oct 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 7.0.4-34.1
- rebuild with new gmp without compat lib

* Thu Oct 20 2011 Jens Petersen <petersen@redhat.com> - 7.0.4-34
- setup ghc-deps.sh after ghc_version_override for bootstrapping

* Tue Oct 18 2011 Jens Petersen <petersen@redhat.com> - 7.0.4-33
- add armv5tel (ported by Henrik Nordström)
- also use ghc-deps.sh when bootstrapping (ghc-rpm-macros-0.13.13)

* Mon Oct 17 2011 Jens Petersen <petersen@redhat.com> - 7.0.4-32
- remove libffi_archs: not allowed to bundle libffi on any arch
- include the ghc (ghci) library in ghc-devel (Narasim)

* Tue Oct 11 2011 Peter Schiffer <pschiffe@redhat.com> - 7.0.4-31.1
- rebuild with new gmp

* Fri Sep 30 2011 Jens Petersen <petersen@redhat.com> - 7.0.4-31
- build with ghc-rpm-macros >= 0.13.11 to fix provides and obsoletes versions
  in library devel subpackages

* Thu Sep 29 2011 Jens Petersen <petersen@redhat.com> - 7.0.4-30
- no need to specify -lffi in build.mk (Henrik Nordström)

* Wed Sep 28 2011 Jens Petersen <petersen@redhat.com> - 7.0.4-29
- port to armv7hl by Henrik Nordström (#741725)

* Wed Sep 14 2011 Jens Petersen <petersen@redhat.com> - 7.0.4-28
- setup ghc-deps.sh when not bootstrapping!

* Wed Sep 14 2011 Jens Petersen <petersen@redhat.com> - 7.0.4-27
- setup dependency generation with ghc-deps.sh since it was moved to
  ghc_lib_install in ghc-rpm-macros

* Fri Jun 17 2011 Jens Petersen <petersen@redhat.com> - 7.0.4-26
- BR same ghc version unless ghc_bootstrapping defined
- add libffi_archs
- drop the quick build profile
- put dyn before p in GhcLibWays
- explain new bootstrapping mode using ghc_bootstrap (ghc-rpm-macros-0.13.5)

* Thu Jun 16 2011 Jens Petersen <petersen@redhat.com> - 7.0.4-25
- update to 7.0.4 bugfix release
  http://haskell.org/ghc/docs/7.0.4/html/users_guide/release-7-0-4.html
- strip static again (upstream #5004 fixed)
- Cabal updated to 1.10.2.0
- re-enable testsuite
- update summary and description

* Tue Jun 14 2011 Jens Petersen <petersen@redhat.com> - 7.0.2-24
- finally change from ExclusiveArch to ExcludeArch to target more archs

* Sat May 21 2011 Jens Petersen <petersen@redhat.com> - 7.0.2-23
- obsolete dph libraries and feldspar-language

* Mon May 16 2011 Jens Petersen <petersen@redhat.com> - 7.0.2-22
- merge prof subpackages into the devel subpackages with ghc-rpm-macros-0.13

* Wed May 11 2011 Jens Petersen <petersen@redhat.com> - 7.0.2-21
- configure with /usr/bin/gcc to help bootstrapping to new archs
  (otherwise ccache tends to get hardcoded as gcc, which not in koji)
- posttrans scriplet for ghc_pkg_recache is redundant

* Mon May  9 2011 Jens Petersen <petersen@redhat.com> - 7.0.2-20
- make devel and prof meta packages require libs with release
- make ghc-*-devel subpackages require ghc with release

* Wed May 04 2011 Jiri Skala <jskala@redhat.com> - 7.0.2-19.1
- fixes path to gcc on ppc64 arch

* Tue Apr 26 2011 Jens Petersen <petersen@redhat.com> - 7.0.2-19
- add upstream ghc-powerpc-linker-mmap.patch for ppc64 (Jiri Skala)

* Thu Apr 21 2011 Jiri Skala <jskala@redhat.com> - 7.0.2-18
- bootstrap to ppc64

* Fri Apr  1 2011 Jens Petersen <petersen@redhat.com> - 7.0.2-17
- rebuild against ghc-rpm-macros-0.11.14 to provide ghc-*-doc

* Fri Apr  1 2011 Jens Petersen <petersen@redhat.com> - 7.0.2-16
- provides ghc-doc again: it is still a buildrequires for libraries
- ghc-prof now requires ghc-devel
- ghc-devel now requires ghc explicitly

* Wed Mar 30 2011 Jens Petersen <petersen@redhat.com> - 7.0.2-15
- do not strip static libs since it breaks ghci-7.0.2 loading libHSghc.a
  (see http://hackage.haskell.org/trac/ghc/ticket/5004)
- no longer provide ghc-doc
- no longer obsolete old haddock

* Tue Mar 29 2011 Jens Petersen <petersen@redhat.com> - 7.0.2-14
- fix back missing LICENSE files in library subpackages
- drop ghc_reindex_haddock from install script

* Thu Mar 10 2011 Jens Petersen <petersen@redhat.com> - 7.0.2-13
- rebuild against 7.0.2

* Wed Mar  9 2011 Jens Petersen <petersen@redhat.com> - 7.0.2-12
- update to 7.0.2 release
- move bin-package-db into ghc-ghc
- disable broken testsuite

* Wed Feb 23 2011 Fabio M. Di Nitto <fdinitto@redhat.com> 7.0.1-11
- enable build on sparcv9
- add ghc-fix-linking-on-sparc.patch to fix ld being called
  at the same time with --relax and -r. The two options conflict
  on sparc.
- bump BuildRequires on ghc-rpm-macros to >= 0.11.10 that guarantees
  a correct build on secondary architectures.

* Sun Feb 13 2011 Jens Petersen <petersen@redhat.com>
- without_shared renamed to ghc_without_shared

* Thu Feb 10 2011 Jens Petersen <petersen@redhat.com> - 7.0.1-10
- rebuild

* Thu Feb 10 2011 Jens Petersen <petersen@redhat.com> - 7.0.1-9
- fix without_shared build (thanks Adrian Reber)
- disable system libffi for secondary archs
- temporarily disable ghc-*-devel BRs for ppc

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.0.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 31 2011 Jens Petersen <petersen@redhat.com> - 7.0.1-7
- include LICENSE files in the shared lib subpackages

* Sat Jan 22 2011 Jens Petersen <petersen@redhat.com> - 7.0.1-6
- patch Cabal to add configure option --enable-executable-dynamic
- exclude huge ghc API library from devel and prof metapackages

* Thu Jan 13 2011 Jens Petersen <petersen@redhat.com> - 7.0.1-5
- fix no doc and no manual builds

* Thu Jan 13 2011 Jens Petersen <petersen@redhat.com> - 7.0.1-4
- add BRs for various subpackaged ghc libraries needed to build ghc
- condition rts .so libraries for non-shared builds

* Thu Dec 30 2010 Jens Petersen <petersen@redhat.com> - 7.0.1-3
- subpackage all the libraries with ghc-rpm-macros-0.11.1
- put rts, integer-gmp and ghc-prim in base, and ghc-binary in bin-package-db
- drop the libs mega-subpackage
- prof now a meta-package for backward compatibility
- add devel meta-subpackage to easily install all ghc libraries
- store doc cronjob package cache file under /var (#664850)
- drop old extralibs bcond
- no longer need to define or clean buildroot
- ghc base package now requires ghc-base-devel
- drop ghc-time obsoletes

* Wed Nov 24 2010 Jens Petersen <petersen@redhat.com> - 7.0.1-2
- require libffi-devel

* Tue Nov 16 2010 Jens Petersen <petersen@redhat.com> - 7.0.1-1
- update to 7.0.1 release
- turn on system libffi now

* Mon Nov  8 2010 Jens Petersen <petersen@redhat.com> - 6.12.3-9
- disable the libffi changes for now since they break libHSffi*.so

* Thu Nov  4 2010 Jens Petersen <petersen@redhat.com> - 6.12.3-8
- add a cronjob for doc indexing
- disable gen_contents_index when not run with --batch for cron
- use system libffi with ghc-use-system-libffi.patch from debian
- add bcond for system libffi

* Thu Nov  4 2010 Jens Petersen <petersen@redhat.com> - 6.12.3-7
- skip huge type-level docs from haddock re-indexing (#649228)

* Thu Sep 30 2010 Jens Petersen <petersen@redhat.com> - 6.12.3-6
- move gtk2hs obsoletes to ghc-glib and ghc-gtk
- drop happy buildrequires
- smp build with max 4 cpus

* Fri Jul 30 2010 Jens Petersen <petersen@redhat.com> - 6.12.3-5
- obsolete old gtk2hs packages for smooth upgrades

* Thu Jul 15 2010 Jens Petersen <petersen@redhat.com> - 6.12.3-4
- merge ghc-doc into base package
- obsolete ghc-time and ghc-ghc-doc (ghc-rpm-macros-0.8.0)
- note that ghc-6.12.3 is part of haskell-platform-2010.2.0.0

* Thu Jun 24 2010 Jens Petersen <petersen@redhat.com> - 6.12.3-3
- drop the broken summary and description args to the ghc-ghc package
  and use ghc-rpm-macros-0.6.1

* Wed Jun 23 2010 Jens Petersen <petersen@redhat.com> - 6.12.3-2
- strip all dynlinked files not just shared objects (ghc-rpm-macros-0.5.9)

* Mon Jun 14 2010 Jens Petersen <petersen@redhat.com> - 6.12.3-1
- 6.12.3 release:
  http://darcs.haskell.org/download/docs/6.12.3/html/users_guide/release-6-12-3.html
- build with hscolour
- use ghc-rpm-macro-0.5.8 for ghc_strip_shared macro

* Fri May 28 2010 Jens Petersen <petersen@redhat.com> - 6.12.2.20100521-1
- 6.12.3 rc1
- ghost package.cache
- drop ghc-utf8-string obsoletes since it is no longer provided
- run testsuite fast
- fix description and summary of ghc internal library (John Obbele)

* Fri Apr 23 2010 Jens Petersen <petersen@redhat.com> - 6.12.2-1
- update to 6.12.2
- add testsuite with bcond, run it in check section, and BR python

* Mon Apr 12 2010 Jens Petersen <petersen@redhat.com> - 6.12.1-6
- ghc-6.12.1 is part of haskell-platform-2010.1.0.0
- drop old ghc682, ghc681, haddock09 obsoletes
- drop haddock_version and no longer provide haddock explicitly
- update ghc-rpm-macros BR to 0.5.6 for ghc_pkg_recache

* Mon Jan 11 2010 Jens Petersen <petersen@redhat.com> - 6.12.1-5
- drop ghc-6.12.1-no-filter-libs.patch and extras packages again
- filter ghc-ghc-prof files from ghc-prof
- ghc-mtl package was added to fedora

* Mon Jan 11 2010 Jens Petersen <petersen@redhat.com> - 6.12.1-4
- ghc-rpm-macros-0.5.4 fixes wrong version requires between lib subpackages

* Mon Jan 11 2010 Jens Petersen <petersen@redhat.com> - 6.12.1-3
- ghc-rpm-macros-0.5.2 fixes broken pkg_name requires for lib subpackages

* Tue Dec 22 2009 Jens Petersen <petersen@redhat.com> - 6.12.1-2
- include haskeline, mtl, and terminfo for now with
  ghc-6.12.1-no-filter-libs.patch
- use ghc_binlibpackage, grep -v and ghc_gen_filelists to generate
  the library subpackages (ghc-rpm-macros-0.5.1)
- always set GhcLibWays (Lorenzo Villani)
- use ghcdocbasedir to revert html doc path to upstream's html/ for consistency

* Wed Dec 16 2009 Jens Petersen <petersen@redhat.com> - 6.12.1-1
- pre became 6.12.1 final
- exclude ghc .conf file from package.conf.d in base package
- use ghc_reindex_haddock
- add scripts for ghc-ghc-devel and ghc-ghc-doc
- add doc bcond
- add ghc-6.12.1-gen_contents_index-haddock-path.patch to adjust haddock path
  since we removed html/ from libraries path
- require ghc-rpm-macros-0.3.1 and use ghc_version_override

* Sat Dec 12 2009 Jens Petersen <petersen@redhat.com> - 6.12.1-0.2
- remove redundant mingw and perl from ghc-tarballs/
- fix exclusion of ghc internals lib from base packages with -mindepth
- rename the final file lists to PKGNAME.files for clarity

* Fri Dec 11 2009 Jens Petersen <petersen@redhat.com> - 6.12.1-0.1
- update to ghc-6.12.1-pre
- separate bcond options into enabled and disabled for clarity
- only enable shared for intel x86 archs (Lorenzo Villani)
- add quick build profile (Lorenzo Villani)
- remove package_debugging hack (use "make install-short")
- drop sed BR (Lorenzo Villani)
- put all build.mk config into one cat block (Lorenzo Villani)
- export CFLAGS to configure (Lorenzo Villani)
- add dynamic linking test to check section (thanks Lorenzo Villani)
- remove old ghc66 obsoletes
- subpackage huge ghc internals library (thanks Lorenzo Villani)
  - BR ghc-rpm-macros >= 0.3.0
- move html docs to docdir/ghc from html subdir (Lorenzo Villani)
- disable smp build for now: broken for 8 cpus at least

* Wed Nov 18 2009 Jens Petersen <petersen@redhat.com> - 6.12.0.20091121-1
- update to 6.12.1 rc2
- build shared libs, yay! and package in standalone libs subpackage
- add bcond for manual and extralibs
- reenable ppc secondary arch
- don't provide ghc-haddock-*
- remove obsolete post requires policycoreutils
- add vanilla v to GhcLibWays when building without prof
- handle without hscolour
- can't smp make currently
- lots of filelist fixes for handling shared libs
- run ghc-pkg recache posttrans
- no need to install gen_contents_index by hand
- manpage is back

* Thu Nov 12 2009 Bryan O'Sullivan <bos@serpentine.com> - 6.12.0.20091010-8
- comprehensive attempts at packaging fixes

* Thu Nov 12 2009 Bryan O'Sullivan <bos@serpentine.com> - 6.12.0.20091010-7
- fix package.conf stuff

* Thu Nov 12 2009 Bryan O'Sullivan <bos@serpentine.com> - 6.12.0.20091010-6
- give up trying to install man pages

* Thu Nov 12 2009 Bryan O'Sullivan <bos@serpentine.com> - 6.12.0.20091010-5
- try to install man pages

* Thu Nov 12 2009 Bryan O'Sullivan <bos@serpentine.com> - 6.12.0.20091010-3
- fix %%check

* Sun Oct 11 2009 Bryan O'Sullivan <bos@serpentine.com> - 6.12.0.20091010-2
- disable ppc for now (seems unsupported)
- buildreq ncurses-devel

* Sun Oct 11 2009 Bryan O'Sullivan <bos@serpentine.com> - 6.12.0.20091010-1
- Update to 6.12 RC 1

* Thu Oct  1 2009 Jens Petersen <petersen@redhat.com>
- selinux file context no longer needed in post script
- (for ghc-6.12-shared) drop ld.so.conf.d files

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.10.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 21 2009 Bryan O'Sullivan <bos@serpentine.com> - 6.10.4-1
- update to 6.10.4

* Sat May 30 2009 Jens Petersen <petersen@redhat.com> - 6.10.3-3
- add haddock_version and use it to obsolete haddock and ghc-haddock-*

* Fri May 22 2009 Jens Petersen <petersen@redhat.com> - 6.10.3-2
- update haddock provides and obsoletes
- drop ghc-mk-pkg-install-inplace.patch: no longer needed with new 6.11 buildsys
- add bcond for extralibs
- rename doc bcond to manual

* Wed May 13 2009 Jens Petersen <petersen@redhat.com> - 6.10.3-1
- update to 6.10.3
- haskline replaces editline, so it is no longer needed to build
- macros.ghc moved to ghc-rpm-macros package
- fix handling of hscolor files in filelist generation

* Tue Apr 28 2009 Jens Petersen <petersen@redhat.com> - 6.10.2-4
- add experimental bcond hscolour
- add experimental support for building shared libraries (for ghc-6.11)
  - add libs subpackage for shared libraries
  - create a ld.conf.d file for libghc*.so
  - BR libffi-devel
- drop redundant setting of GhcLibWays in build.mk for no prof
- drop redundant setting of HADDOCK_DOCS
- simplify filelist names
- add a check section based on tests from debian's package
- be more careful about doc files in filelist

* Fri Apr 24 2009 Jens Petersen <petersen@redhat.com> - 6.10.2-3
- define ghc_version in macros.ghc in place of ghcrequires
- drop ghc-requires script for now

* Sun Apr 19 2009 Jens Petersen <petersen@redhat.com> - 6.10.2-2
- add ghc-requires rpm script to generate ghc version dependencies
  (thanks to Till Maas)
- update macros.ghc:
  - add %%ghcrequires to call above script
  - pkg_libdir and pkg_docdir obsoleted in packages and replaced
    by ghcpkgdir and ghcdocdir inside macros.ghc
  - make filelist also for docs

* Wed Apr 08 2009 Bryan O'Sullivan <bos@serpentine.com> - 6.10.2-1
- Update to 6.10.2

* Fri Feb 27 2009 Jens Petersen <petersen@redhat.com> - 6.10.1-13
- ok let's stick with ExclusiveArch for brevity

* Fri Feb 27 2009 Jens Petersen <petersen@redhat.com> - 6.10.1-12
- drop ghc_archs since it breaks koji
- fix missing -devel in ghc_gen_filelists
- change from ExclusiveArch to ExcludeArch ppc64 since alpha was bootstrapped
  by oliver

* Wed Feb 25 2009 Jens Petersen <petersen@redhat.com> - 6.10.1-11
- use %%ix86 for change from i386 to i586 in rawhide
- add ghc_archs macro in macros.ghc for other packages
- obsolete haddock09
- use %%global instead of %%define
- use bcond for doc and prof
- rename ghc_gen_filelists lib filelist to -devel.files

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.10.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 13 2009 Jens Petersen <petersen@redhat.com> - 6.10.1-9
- require and buildrequire libedit-devel > 2.11-2
- protect ghc_register_pkg and ghc_unregister_pkg

* Fri Jan 23 2009 Jens Petersen <petersen@redhat.com> - 6.10.1-8
- fix to libedit means can drop ncurses-devel BR workaround (#481252)

* Mon Jan 19 2009 Jens Petersen <petersen@redhat.com> - 6.10.1-7
- buildrequire ncurses-devel to fix build of missing editline package needed
  for ghci line-editing (#478466)
- move spec templates to cabal2spec package for easy updating
- provide correct haddock version

* Mon Dec  1 2008 Jens Petersen <petersen@redhat.com> - 6.10.1-6
- update macros.ghc to latest proposed revised packaging guidelines:
  - use runghc
  - drop trivial cabal_build and cabal_haddock macros
  - ghc_register_pkg and ghc_unregister_pkg replace ghc_preinst_script,
    ghc_postinst_script, ghc_preun_script, and ghc_postun_script
- library templates prof subpackage requires main library again
- make cabal2spec work on .cabal files too, and
  read and check name and version directly from .cabal file
- ghc-prof does not need to own libraries dirs owned by main package

* Tue Nov 25 2008 Jens Petersen <petersen@redhat.com> - 6.10.1-5
- add cabal2spec and template files for easy cabal hackage packaging
- simplify script macros: make ghc_preinst_script and ghc_postun_script no-ops
  and ghc_preun_script only unregister for uninstall

* Tue Nov 11 2008 Jens Petersen <petersen@redhat.com> - 6.10.1-4
- fix broken urls to haddock docs created by gen_contents_index script
- avoid haddock errors when upgrading by making doc post script posttrans

* Wed Nov 05 2008 Bryan O'Sullivan <bos@serpentine.com> - 6.10.1-3
- libraries/prologue.txt should not have been ghosted

* Tue Nov 04 2008 Bryan O'Sullivan <bos@serpentine.com> - 6.10.1-2
- Fix a minor packaging glitch

* Tue Nov 04 2008 Bryan O'Sullivan <bos@serpentine.com> - 6.10.1-1
- Update to 6.10.1

* Thu Oct 23 2008 Jens Petersen <petersen@redhat.com> - 6.10.0.20081007-9
- remove redundant --haddockdir from cabal_configure
- actually ghc-pkg no longer seems to create package.conf.old backups
- include LICENSE in doc

* Thu Oct 23 2008 Jens Petersen <petersen@redhat.com> - 6.10.0.20081007-8
- need to create ghost package.conf.old for ghc-6.10

* Thu Oct 23 2008 Jens Petersen <petersen@redhat.com> - 6.10.0.20081007-7
- use gen_contents_index to re-index haddock
- add %%pkg_docdir to cabal_configure
- requires(post) ghc for haddock for doc
- improve doc file lists
- no longer need to create ghost package.conf.old
- remove or rename alternatives files more consistently

* Tue Oct 14 2008 Bryan O'Sullivan <bos@serpentine.com> - 6.10.0.20081007-6
- Update macros to install html and haddock bits in the right places

* Tue Oct 14 2008 Bryan O'Sullivan <bos@serpentine.com> - 6.10.0.20081007-5
- Don't use a macro to update the docs for the main doc package

* Tue Oct 14 2008 Bryan O'Sullivan <bos@serpentine.com> - 6.10.0.20081007-4
- Add ghc_haddock_reindex macro
- Generate haddock index after installing ghc-doc package

* Mon Oct 13 2008 Jens Petersen <petersen@redhat.com> - 6.10.0.20081007-3
- provide haddock = 2.2.2
- add selinux file context for unconfined_execmem following darcs package
- post requires policycoreutils

* Sun Oct 12 2008 Bryan O'Sullivan <bos@serpentine.com> - 6.10.0.20081007-2.fc10
- Use libedit in preference to readline, for BSD license consistency
- With haddock bundled now, obsolete standalone versions (but not haddock09)
- Drop obsolete freeglut-devel, openal-devel, and haddock09 dependencies

* Sun Oct 12 2008 Bryan O'Sullivan <bos@serpentine.com> - 6.10.0.20081007-1.fc10
- Update to 6.10.1 release candidate 1

* Wed Oct  1 2008 Bryan O'Sullivan <bos@serpentine.com> - 6.10.0.20080921-1.fc10
- Drop unneeded haddock patch
- Rename hsc2hs to hsc2hs-ghc so the alternatives symlink to it will work

* Wed Sep 24 2008 Jens Petersen <petersen@redhat.com> - 6.8.3-5
- bring back including haddock-generated lib docs, now under docdir/ghc
- fix macros.ghc filepath (#460304)
- spec file cleanups:
- fix the source urls back
- drop requires chkconfig
- do not override __spec_install_post
- setup docs building in build.mk
- no longer need to remove network/include/Typeable.h
- install binaries under libdir not libexec
- remove hsc2hs and runhaskell binaries since they are alternatives

* Wed Sep 17 2008 Jens Petersen <petersen@redhat.com> - 6.8.3-4
- add macros.ghc for new Haskell Packaging Guidelines (#460304)

* Wed Jun 18 2008 Bryan O'Sullivan <bos@serpentine.com> - 6.8.3-3
- Add symlinks from _libdir, where ghc looks, to _libexecdir
- Patch libraries/gen_contents_index to use haddock-0.9

* Wed Jun 18 2008 Bryan O'Sullivan <bos@serpentine.com> - 6.8.3-2
- Remove unnecessary dependency on alex

* Wed Jun 18 2008 Bryan O'Sullivan <bos@serpentine.com> - 6.8.3-1
- Upgrade to 6.8.3
- Drop the ghc682-style naming scheme, obsolete those packages
- Manually strip binaries

* Tue Apr  8 2008 Jens Petersen <petersen@redhat.com> - 6.8.2-10
- another rebuild attempt

* Thu Feb 14 2008 Jens Petersen <petersen@redhat.com> - 6.8.2-9
- remove unrecognized --docdir and --htmldir from configure
- drop old buildrequires on libX11-devel and libXt-devel
- rebuild with gcc43

* Sun Jan 06 2008 Bryan O'Sullivan <bos@serpentine.com> - 6.8.2-7
- More attempts to fix docdir

* Sun Jan 06 2008 Bryan O'Sullivan <bos@serpentine.com> - 6.8.2-6
- Fix docdir

* Wed Dec 12 2007 Bryan O'Sullivan <bos@serpentine.com> - 6.8.2-1
- Update to 6.8.2

* Fri Nov 23 2007 Bryan O'Sullivan <bos@serpentine.com> - 6.8.1-2
- Exclude alpha

* Thu Nov  8 2007 Bryan O'Sullivan <bos@serpentine.com> - 6.8.1-2
- Drop bit-rotted attempts at making package relocatable

* Sun Nov  4 2007 Michel Salim <michel.sylvan@gmail.com> - 6.8.1-1
- Update to 6.8.1

* Sat Sep 29 2007 Bryan O'Sullivan <bos@serpentine.com> - 6.8.0.20070928-2
- add happy to BuildRequires

* Sat Sep 29 2007 Bryan O'Sullivan <bos@serpentine.com> - 6.8.0.20070928-1
- prepare for GHC 6.8.1 by building a release candidate snapshot

* Thu May 10 2007 Bryan O'Sullivan <bos@serpentine.com> - 6.6.1-3
- install man page for ghc

* Thu May 10 2007 Bryan O'Sullivan <bos@serpentine.com> - 6.6.1-2
- exclude ppc64 for now, due to lack of time to bootstrap

* Wed May  9 2007 Bryan O'Sullivan <bos@serpentine.com> - 6.6.1-1
- update to 6.6.1 release

* Mon Jan 22 2007 Jens Petersen <petersen@redhat.com> - 6.6-2
- remove truncated duplicate Typeable.h header in network package
  (Bryan O'Sullivan, #222865)

* Fri Nov  3 2006 Jens Petersen <petersen@redhat.com> - 6.6-1
- update to 6.6 release
- buildrequire haddock >= 0.8
- fix summary of ghcver package (Michel Salim, #209574)

* Thu Sep 28 2006 Jens Petersen <petersen@redhat.com> - 6.4.2-4
- turn on docs generation again

* Mon Sep 25 2006 Jens Petersen <petersen@redhat.com> - 6.4.2-3.fc6
- ghost package.conf.old (Gérard Milmeister)
- set unconfined_execmem_exec_t context on executables with ghc rts (#195821)
- turn off building docs until haddock is back

* Sat Apr 29 2006 Jens Petersen <petersen@redhat.com> - 6.4.2-2.fc6
- buildrequire libXt-devel so that the X11 package and deps get built
  (Garrett Mitchener, #190201)

* Thu Apr 20 2006 Jens Petersen <petersen@redhat.com> - 6.4.2-1.fc6
- update to 6.4.2 release

* Thu Mar  2 2006 Jens Petersen <petersen@redhat.com> - 6.4.1-3.fc5
- buildrequire libX11-devel instead of xorg-x11-devel (Kevin Fenzi, #181024)
- make ghc-doc require ghc (Michel Salim, #180449)

* Tue Oct 11 2005 Jens Petersen <petersen@redhat.com> - 6.4.1-2.fc5
- turn on build_doc since haddock is now in Extras
- no longer specify ghc version to build with (Ville Skyttä, #170176)

* Tue Sep 20 2005 Jens Petersen <petersen@redhat.com> - 6.4.1-1.fc5
- 6.4.1 release
  - the following patches are now upstream: ghc-6.4-powerpc.patch,
    rts-GCCompact.h-x86_64.patch, ghc-6.4-dsforeign-x86_64-1097471.patch,
    ghc-6.4-rts-adjustor-x86_64-1097471.patch
  - builds with gcc4 so drop %%_with_gcc32
  - x86_64 build restrictions (no ghci and split objects) no longer apply

* Tue May 31 2005 Jens Petersen <petersen@redhat.com>
- add %%dist to release

* Thu May 12 2005 Jens Petersen <petersen@redhat.com> - 6.4-8
- initial import into Fedora Extras

* Thu May 12 2005 Jens Petersen <petersen@haskell.org>
- add build_prof and build_doc switches for -doc and -prof subpackages
- add _with_gcc32 switch since ghc-6.4 doesn't build with gcc-4.0

* Wed May 11 2005 Jens Petersen <petersen@haskell.org> - 6.4-7
- make package relocatable (ghc#1084122)
  - add post install scripts to replace prefix in driver scripts
- buildrequire libxslt and docbook-style-xsl instead of docbook-utils and flex

* Fri May  6 2005 Jens Petersen <petersen@haskell.org> - 6.4-6
- add ghc-6.4-dsforeign-x86_64-1097471.patch and
  ghc-6.4-rts-adjustor-x86_64-1097471.patch from trunk to hopefully fix
  ffi support on x86_64 (Simon Marlow, ghc#1097471)
- use XMLDocWays instead of SGMLDocWays to build documentation fully

* Mon May  2 2005 Jens Petersen <petersen@haskell.org> - 6.4-5
- add rts-GCCompact.h-x86_64.patch to fix GC issue on x86_64 (Simon Marlow)

* Thu Mar 17 2005 Jens Petersen <petersen@haskell.org> - 6.4-4
- add ghc-6.4-powerpc.patch (Ryan Lortie)
- disable building interpreter rather than install and delete on x86_64

* Wed Mar 16 2005 Jens Petersen <petersen@haskell.org> - 6.4-3
- make ghc require ghcver of same ver-rel
- on x86_64 remove ghci for now since it doesn't work and all .o files

* Tue Mar 15 2005 Jens Petersen <petersen@haskell.org> - 6.4-2
- ghc requires ghcver (Amanda Clare)

* Sat Mar 12 2005 Jens Petersen <petersen@haskell.org> - 6.4-1
- 6.4 release
  - x86_64 build no longer unregisterised
- use sed instead of perl to tidy filelists
- buildrequire ghc64 instead of ghc-6.4
- no epoch for ghc64-prof's ghc64 requirement
- install docs directly in docdir

* Fri Jan 21 2005 Jens Petersen <petersen@haskell.org> - 6.2.2-2
- add x86_64 port
  - build unregistered and without splitobjs
  - specify libdir to configure and install
- rename ghc-prof to ghcXYZ-prof, which obsoletes ghc-prof

* Mon Dec  6 2004 Jens Petersen <petersen@haskell.org> - 6.2.2-1
- move ghc requires to ghcXYZ

* Wed Nov 24 2004 Jens Petersen <petersen@haskell.org> - 6.2.2-0.fdr.1
- ghc622
  - provide ghc = %%version
- require gcc, gmp-devel and readline-devel

* Fri Oct 15 2004 Gerard Milmeister <gemi@bluewin.ch> - 6.2.2-0.fdr.1
- New Version 6.2.2

* Mon Mar 22 2004 Gerard Milmeister <gemi@bluewin.ch> - 6.2.1-0.fdr.1
- New Version 6.2.1

* Tue Dec 16 2003 Gerard Milmeister <gemi@bluewin.ch> - 6.2-0.fdr.1
- New Version 6.2

* Tue Dec 16 2003 Gerard Milmeister <gemi@bluewin.ch> - 6.0.1-0.fdr.3
- A few minor specfile tweaks

* Mon Dec 15 2003 Gerard Milmeister <gemi@bluewin.ch> - 6.0.1-0.fdr.2
- Different file list generation

* Mon Oct 20 2003 Gerard Milmeister <gemi@bluewin.ch> - 6.0.1-0.fdr.1
- First Fedora release
- Added generated html docs, so that haddock is not needed

* Wed Sep 26 2001 Manuel Chakravarty
- small changes for 5.04

* Wed Sep 26 2001 Manuel Chakravarty
- split documentation off into a separate package
- adapt to new docbook setup in RH7.1

* Mon Apr 16 2001 Manuel Chakravarty
- revised for 5.00
- also runs autoconf automagically if no ./configure found

* Thu Jun 22 2000 Sven Panne
- removed explicit usage of hslibs/docs, it belongs to ghc/docs/set

* Sun Apr 23 2000 Manuel Chakravarty
- revised for ghc 4.07; added suggestions from Pixel <pixel@mandrakesoft.com>
- added profiling package

* Tue Dec 7 1999 Manuel Chakravarty
- version for use from CVS

* Thu Sep 16 1999 Manuel Chakravarty
- modified for GHC 4.04, patchlevel 1 (no more 62 tuple stuff); minimises use
  of patch files - instead emits a build.mk on-the-fly

* Sat Jul 31 1999 Manuel Chakravarty
- modified for GHC 4.04

* Wed Jun 30 1999 Manuel Chakravarty
- some more improvements from vbzoli

* Fri Feb 26 1999 Manuel Chakravarty
- modified for GHC 4.02

* Thu Dec 24 1998 Zoltan Vorosbaranyi
- added BuildRoot
- files located in /usr/local/bin, /usr/local/lib moved to /usr/bin, /usr/lib

* Tue Jul 28 1998 Manuel Chakravarty
- original version
